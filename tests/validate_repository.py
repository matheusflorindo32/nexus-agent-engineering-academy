"""Validate the NEXUS Premium Elite foundation using Python's stdlib only."""
from __future__ import annotations

from pathlib import Path
import ast
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOTS = (
    "agents", "course", "docs", "examples", "labs", "loops",
    "platforms", "projects", "templates",
)
REQUIRED_ROOT_ENTRIES = {
    "README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md",
    "CHANGELOG.md", "LICENSE", "CODE_OF_CONDUCT.md", ".github", "tests",
    "AGENTS.md", "datasets", *CONTENT_ROOTS,
}
REQUIRED_EXECUTABLES = {
    "examples/minimal_readonly_agent.py",
    "examples/context_retriever.py",
    "examples/safe_tool_boundary.py",
    "examples/safe_tool_boundary.ts",
    "examples/deterministic_loop.py",
    "examples/governed_memory_store.py",
    "examples/governed_multi_agent_orchestrator.py",
    "examples/evaluation_harness.py",
    "examples/security_guardrails.py",
    "examples/production_runtime.py",
    "examples/observability_pipeline.py",
    "tests/run_quality_gates.py",
    "datasets/lab-201-context-fixtures.json",
    ".github/workflows/quality.yml",
}
EXPECTED_MODULES = {f"{number:02d}" for number in range(13)}
EXPECTED_LABS = {"000", "101", "201", "301", "401", "501", "601", "701", "801", "901", "1001", "1101"}
REQUIRED_FRONTMATTER = {"id", "title", "lang", "status"}
ALLOWED_LANGS = {"pt-BR", "en", "es"}
ALLOWED_STATUS = {"foundation", "draft", "review", "accepted", "active", "stable", "deprecated"}
REQUIRED_MODULE_SECTIONS = {
    "## Objetivos", "## Pré-requisitos", "## Projeto", "## Checklist", "## Referências",
}
REQUIRED_LAB_SECTIONS = {
    "## Missão", "## Critérios de aprovação", "## Evidências",
}
REQUIRED_AGENT_FIELDS = {
    "objective", "non_goals", "inputs", "outputs", "tools", "permissions",
    "budgets", "stop_conditions", "failure_modes", "evaluation",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key ID": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def document_slug(path: Path, data: dict[str, str]) -> str:
    """Return an explicit slug or a stable repository-relative derived slug."""
    explicit = data.get("slug", "").strip()
    if explicit:
        return explicit
    relative = path.relative_to(ROOT).with_suffix("")
    parts = list(relative.parts)
    if len(parts) == 1 and parts[0].lower() == "readme":
        return "repository"
    if parts and parts[-1].lower() == "readme":
        parts[-1] = "index"
    raw_slug = "-".join(part.lower() for part in parts)
    return re.sub(r"[^a-z0-9]+", "-", raw_slug).strip("-")


def parse_inline_list(value: str) -> list[str] | None:
    """Parse the flat YAML list syntax used by curriculum prerequisites."""
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    body = value[1:-1].strip()
    if not body:
        return []
    return [item.strip().strip("\"'") for item in body.split(",") if item.strip()]


def markdown_files() -> list[Path]:
    roots = [ROOT / name for name in CONTENT_ROOTS]
    files = [ROOT / name for name in (
        "README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md",
        "CHANGELOG.md", "CODE_OF_CONDUCT.md", "AGENTS.md",
    )]
    for root in roots:
        if root.exists():
            files.extend(root.rglob("*.md"))
    return sorted(set(path for path in files if path.exists()))


def check_frontmatter(files: list[Path], errors: list[str]) -> None:
    seen_ids: dict[str, Path] = {}
    seen_slugs: dict[str, Path] = {}
    records: list[tuple[Path, dict[str, str]]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        data = parse_frontmatter(text)
        relative = path.relative_to(ROOT)
        if data is None:
            errors.append(f"{relative}: frontmatter YAML ausente ou mal delimitado")
            continue
        missing = REQUIRED_FRONTMATTER - data.keys()
        if missing:
            errors.append(f"{relative}: campos ausentes: {', '.join(sorted(missing))}")
        doc_id = data.get("id", "")
        if doc_id and not ID_RE.fullmatch(doc_id):
            errors.append(f"{relative}: id inválido: {doc_id}")
        if doc_id in seen_ids:
            errors.append(f"{relative}: id duplicado com {seen_ids[doc_id].relative_to(ROOT)}: {doc_id}")
        elif doc_id:
            seen_ids[doc_id] = path
        slug = document_slug(path, data)
        if not slug or not SLUG_RE.fullmatch(slug):
            errors.append(f"{relative}: slug inválido: {slug}")
        elif slug in seen_slugs:
            errors.append(
                f"{relative}: slug duplicado com "
                f"{seen_slugs[slug].relative_to(ROOT)}: {slug}"
            )
        else:
            seen_slugs[slug] = path
        lang = data.get("lang")
        if lang and lang not in ALLOWED_LANGS:
            errors.append(f"{relative}: lang não suportado: {lang}")
        status = data.get("status")
        if status and status not in ALLOWED_STATUS:
            errors.append(f"{relative}: status não suportado: {status}")
        records.append((path, data))

    known_ids = set(seen_ids)
    for path, data in records:
        raw_prerequisites = data.get("prerequisites")
        if raw_prerequisites is None:
            continue
        prerequisites = parse_inline_list(raw_prerequisites)
        relative = path.relative_to(ROOT)
        if prerequisites is None:
            errors.append(f"{relative}: prerequisites deve usar lista YAML inline")
            continue
        for prerequisite in prerequisites:
            if prerequisite not in known_ids:
                errors.append(
                    f"{relative}: pré-requisito inexistente: {prerequisite}"
                )


def normalized_link_target(raw: str) -> str:
    target = raw.strip().split(maxsplit=1)[0].strip("<>")
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


def check_links(files: list[Path], errors: list[str]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            if raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = normalized_link_target(raw)
            if not target or "<" in target or ">" in target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: link escapa do repositório: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: link interno quebrado: {raw}")


def check_modules(errors: list[str]) -> None:
    modules_root = ROOT / "course" / "modules"
    present: set[str] = set()
    owners: dict[str, Path] = {}
    for path in sorted(modules_root.glob("*/README.md")):
        prefix = path.parent.name.split("-", 1)[0]
        if prefix in owners:
            errors.append(
                f"número de módulo duplicado {prefix}: "
                f"{owners[prefix].relative_to(ROOT)} e {path.relative_to(ROOT)}"
            )
        else:
            owners[prefix] = path
        present.add(prefix)
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED_MODULE_SECTIONS if heading not in text]
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: seções ausentes: {', '.join(sorted(missing))}")
        if "## Laboratório" not in text and "## Laboratórios" not in text:
            errors.append(f"{path.relative_to(ROOT)}: referência de laboratório ausente")
        if "## Critérios de excelência" not in text and "## Avaliação" not in text:
            errors.append(f"{path.relative_to(ROOT)}: módulo sem critérios explícitos de avaliação")
    missing_modules = EXPECTED_MODULES - present
    if missing_modules:
        errors.append(f"módulos obrigatórios ausentes: {', '.join(sorted(missing_modules))}")


def check_labs(errors: list[str]) -> None:
    present: set[str] = set()
    owners: dict[str, Path] = {}
    for path in sorted((ROOT / "labs").glob("LAB-*.md")):
        match = re.match(r"LAB-(\d{3,4})-", path.name)
        if match:
            lab_number = match.group(1)
            if lab_number in owners:
                errors.append(
                    f"número de laboratório duplicado {lab_number}: "
                    f"{owners[lab_number].relative_to(ROOT)} e {path.relative_to(ROOT)}"
                )
            else:
                owners[lab_number] = path
            present.add(lab_number)
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED_LAB_SECTIONS if heading not in text]
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: seções ausentes: {', '.join(sorted(missing))}")
        if "## Comando" not in text and "## Procedimento" not in text:
            errors.append(f"{path.relative_to(ROOT)}: procedimento ou comando ausente")
    missing_labs = EXPECTED_LABS - present
    if missing_labs:
        errors.append(f"laboratórios obrigatórios ausentes: {', '.join(sorted(missing_labs))}")


def check_agent_specs(errors: list[str]) -> None:
    for path in sorted((ROOT / "agents").rglob("*.yml")) + sorted((ROOT / "agents").rglob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        keys = {
            line.split(":", 1)[0].strip()
            for line in text.splitlines()
            if ":" in line and not line.startswith((" ", "\t", "-", "#"))
        }
        missing = REQUIRED_AGENT_FIELDS - keys
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: agent spec incompleta: {', '.join(sorted(missing))}")


def check_executables(errors: list[str]) -> None:
    for relative in sorted(REQUIRED_EXECUTABLES):
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"artefato executável obrigatório ausente ou vazio: {relative}")
    for path in sorted((ROOT / "examples").glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(ROOT)}: Python inválido: {exc}")
            continue
        if ast.get_docstring(tree) is None:
            errors.append(f"{path.relative_to(ROOT)}: docstring de módulo ausente")
    dataset = ROOT / "datasets/lab-201-context-fixtures.json"
    if dataset.exists():
        try:
            data = json.loads(dataset.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{dataset.relative_to(ROOT)}: JSON inválido: {exc}")
        else:
            if not isinstance(data, dict) or "chunks" not in data:
                errors.append(f"{dataset.relative_to(ROOT)}: contrato exige objeto com campo chunks")


def check_secrets(errors: list[str]) -> None:
    text_extensions = {
        ".cfg", ".ini", ".json", ".md", ".py", ".toml", ".ts",
        ".txt", ".yaml", ".yml",
    }
    ignored = {".git", ".venv", "node_modules"}
    for path in ROOT.rglob("*"):
        is_env_file = path.name == ".env" or path.name.startswith(".env.")
        if not path.is_file() or (path.suffix.lower() not in text_extensions and not is_env_file):
            continue
        if any(part in ignored for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: possível segredo detectado ({label})")


def check_structure(errors: list[str]) -> None:
    for entry in sorted(REQUIRED_ROOT_ENTRIES):
        if not (ROOT / entry).exists():
            errors.append(f"estrutura obrigatória ausente: {entry}")


def main() -> int:
    errors: list[str] = []
    files = markdown_files()
    check_structure(errors)
    check_frontmatter(files, errors)
    check_links(files, errors)
    check_modules(errors)
    check_labs(errors)
    check_agent_specs(errors)
    check_executables(errors)
    check_secrets(errors)
    if errors:
        print(f"NEXUS validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "NEXUS Premium Elite validation passed: "
        f"{len(files)} Markdown files; Modules 00-12; LAB-000 through LAB-1101; "
        "unique numbering, structure, metadata, IDs, links, contracts, executables and secret scan OK."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
