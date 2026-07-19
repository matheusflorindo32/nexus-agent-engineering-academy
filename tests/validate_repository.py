"""Validate the NEXUS documentation foundation using only Python's stdlib."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOTS = (
    "agents",
    "course",
    "docs",
    "examples",
    "labs",
    "loops",
    "platforms",
    "projects",
    "templates",
)
REQUIRED_ROOT_ENTRIES = {
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    ".github",
    "tests",
    *CONTENT_ROOTS,
}
REQUIRED_FRONTMATTER = {"id", "title", "lang", "status"}
REQUIRED_MODULE_SECTIONS = {
    "## Objetivos",
    "## Pré-requisitos",
    "## Laboratórios",
    "## Projeto",
    "## Checklist",
    "## Bibliografia",
    "## Referências",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")


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


def markdown_files() -> list[Path]:
    roots = [ROOT / name for name in CONTENT_ROOTS]
    files = [ROOT / name for name in (
        "README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md",
        "CHANGELOG.md", "CODE_OF_CONDUCT.md"
    )]
    for root in roots:
        files.extend(root.rglob("*.md"))
    return sorted(set(files))


def check_frontmatter(files: list[Path], errors: list[str]) -> None:
    seen: dict[str, Path] = {}
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
        if doc_id in seen:
            errors.append(f"{relative}: id duplicado com {seen[doc_id].relative_to(ROOT)}: {doc_id}")
        elif doc_id:
            seen[doc_id] = path


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
    for path in sorted((ROOT / "course" / "modules").glob("*/README.md")):
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED_MODULE_SECTIONS if heading not in text]
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: seções ausentes: {', '.join(sorted(missing))}")


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
    if errors:
        print(f"NEXUS validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"NEXUS validation passed: {len(files)} Markdown files, unique IDs, links and module contracts OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

