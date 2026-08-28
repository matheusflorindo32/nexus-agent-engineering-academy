"""NEXUS Repository Indexer V1: read-only, deterministic, Python-only and stdlib-only."""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

MAX_FILE_BYTES = 262_144
MAX_FILES = 2_000
MAX_SYMBOLS_PER_FILE = 512
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "vendor", "generated", "dist", "build", "__pycache__"}
INJECTION_MARKERS = (
    "ignore previous", "ignore all previous", "system prompt", "execute tool",
    "call tool", "reveal secret", "developer message", "override instructions",
)


class IndexerValidationError(ValueError):
    """Raised when an indexing request violates the bounded read-only contract."""


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_relative_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise IndexerValidationError("invalid relative path")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        raise IndexerValidationError("unsafe relative path")
    return str(path)


def _module_for_path(path: str) -> str:
    value = path[:-3] if path.endswith(".py") else path
    parts = value.split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _contains_untrusted_text(text: str) -> int:
    lowered = text.lower()
    return sum(lowered.count(marker) for marker in INJECTION_MARKERS)


class _SymbolVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.symbols: list[str] = []
        self.class_stack: list[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if not self.class_stack:
            self.symbols.append(node.name)
        self.class_stack.append(node.name)
        for child in node.body:
            self.visit(child)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self.class_stack:
            if len(self.class_stack) == 1:
                self.symbols.append(f"{self.class_stack[0]}.{node.name}")
        else:
            self.symbols.append(node.name)

    visit_AsyncFunctionDef = visit_FunctionDef


class RepositoryIndexer:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise IndexerValidationError("repository root must be a directory")

    def index_relative_path(self, relative_path: str) -> dict[str, Any]:
        safe = _safe_relative_path(relative_path)
        path = self.root / safe
        if path.is_symlink():
            raise IndexerValidationError("symlinks are not indexed")
        try:
            resolved = path.resolve(strict=True)
        except FileNotFoundError as exc:
            raise IndexerValidationError("file does not exist") from exc
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise IndexerValidationError("path escapes repository root") from exc
        return self._parse_file(resolved, safe)

    def _discover_python_files(self) -> tuple[list[tuple[str, Path]], list[str]]:
        files: list[tuple[str, Path]] = []
        symlinks: list[str] = []
        for current, dirs, names in os.walk(self.root, topdown=True, followlinks=False):
            current_path = Path(current)
            dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS and not (current_path / d).is_symlink())
            for name in sorted(names):
                path = current_path / name
                rel = path.relative_to(self.root).as_posix()
                if path.is_symlink():
                    symlinks.append(rel)
                    continue
                if path.suffix != ".py":
                    continue
                files.append((_safe_relative_path(rel), path))
                if len(files) > MAX_FILES:
                    raise IndexerValidationError("file count limit exceeded")
        files.sort(key=lambda item: item[0])
        return files, sorted(symlinks)

    def _resolve_import(self, source_path: str, module: str, level: int, known_modules: dict[str, str]) -> str | None:
        if level:
            current_module = _module_for_path(source_path)
            package_parts = current_module.split(".")[:-1]
            if source_path.endswith("/__init__.py"):
                package_parts = current_module.split(".") if current_module else []
            up = max(0, level - 1)
            if up > len(package_parts):
                return None
            base = package_parts[: len(package_parts) - up]
            if module:
                base.extend(module.split("."))
            target_module = ".".join(part for part in base if part)
        else:
            target_module = module
        if not target_module:
            return None
        if target_module in known_modules:
            return known_modules[target_module]
        parts = target_module.split(".")
        while len(parts) > 1:
            parts.pop()
            candidate = ".".join(parts)
            if candidate in known_modules:
                return known_modules[candidate]
        return None

    def _parse_file(self, path: Path, rel: str) -> dict[str, Any]:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            return {"path": rel, "status": "oversized", "size": size}
        raw = path.read_bytes()
        digest = _sha256_bytes(raw)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return {"path": rel, "status": "decode_error", "hash": digest, "size": size}
        try:
            tree = ast.parse(text, filename=rel)
        except SyntaxError as exc:
            return {"path": rel, "status": "parse_error", "hash": digest, "size": size, "error_line": exc.lineno}
        visitor = _SymbolVisitor()
        visitor.visit(tree)
        symbols = sorted(set(visitor.symbols))[:MAX_SYMBOLS_PER_FILE]
        imports: list[dict[str, Any]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"module": alias.name, "level": 0})
            elif isinstance(node, ast.ImportFrom):
                imports.append({"module": node.module or "", "level": int(node.level or 0)})
        unique_imports = sorted({(item["module"], item["level"]) for item in imports})
        return {
            "path": rel,
            "status": "indexed",
            "hash": digest,
            "size": size,
            "symbols": symbols,
            "imports": [{"module": module, "level": level} for module, level in unique_imports],
            "untrusted_text_markers": _contains_untrusted_text(text),
        }

    def build_index(self, previous: dict[str, Any] | None = None) -> dict[str, Any]:
        discovered, symlinks = self._discover_python_files()
        previous_records = (previous or {}).get("file_records", {})
        records: dict[str, dict[str, Any]] = {}
        changed = 0
        reused = 0
        oversized: list[str] = []
        parse_errors: list[str] = []
        decode_errors: list[str] = []
        untrusted_count = 0

        for rel, path in discovered:
            stat_size = path.stat().st_size
            if stat_size > MAX_FILE_BYTES:
                record = {"path": rel, "status": "oversized", "size": stat_size}
            else:
                raw = path.read_bytes()
                current_hash = _sha256_bytes(raw)
                prior = previous_records.get(rel)
                if prior and prior.get("hash") == current_hash and prior.get("status") == "indexed":
                    record = dict(prior)
                    reused += 1
                else:
                    record = self._parse_file(path, rel)
                    changed += 1
            records[rel] = record
            if record["status"] == "oversized":
                oversized.append(rel)
            elif record["status"] == "parse_error":
                parse_errors.append(rel)
            elif record["status"] == "decode_error":
                decode_errors.append(rel)
            elif record["status"] == "indexed":
                untrusted_count += int(record.get("untrusted_text_markers", 0))

        indexed_records = {p: r for p, r in records.items() if r.get("status") == "indexed"}
        known_modules = {_module_for_path(path): path for path in indexed_records}
        nodes: list[dict[str, Any]] = []
        edges_set: set[tuple[str, str, str]] = set()
        dependencies: dict[str, list[str]] = {}
        reverse_dependencies: dict[str, list[str]] = {path: [] for path in indexed_records}

        for rel, record in sorted(indexed_records.items()):
            nodes.append({"id": f"file:{rel}", "type": "file", "path": rel, "metadata": {"language": "python", "content_hash": record["hash"]}})
            for symbol in record.get("symbols", []):
                symbol_id = f"symbol:{rel}:{symbol}"
                nodes.append({"id": symbol_id, "type": "symbol", "path": rel, "symbol": symbol})
                edges_set.add((f"file:{rel}", symbol_id, "CONTAINS_SYMBOL"))
            deps: set[str] = set()
            for item in record.get("imports", []):
                target = self._resolve_import(rel, item["module"], int(item["level"]), known_modules)
                if target and target != rel:
                    deps.add(target)
            dependencies[rel] = sorted(deps)
            for target in sorted(deps):
                edges_set.add((f"file:{rel}", f"file:{target}", "DEPENDS_ON"))
                reverse_dependencies.setdefault(target, []).append(rel)

        reverse_dependencies = {key: sorted(set(value)) for key, value in sorted(reverse_dependencies.items())}
        edges = [{"source": s, "target": t, "type": typ} for s, t, typ in sorted(edges_set)]
        graph = {"schema": "nexus.traceability-graph.v2", "nodes": sorted(nodes, key=lambda n: n["id"]), "edges": edges}
        fingerprint = hashlib.sha256(_canonical_json(graph).encode("utf-8")).hexdigest()
        removed = sorted(set(previous_records) - set(records)) if previous else []
        return {
            "schema": "nexus.repository-index.v1",
            "root_mode": "read-only",
            "language_scope": ["python"],
            "graph": graph,
            "fingerprint": fingerprint,
            "file_records": {key: records[key] for key in sorted(records)},
            "dependencies": {key: dependencies.get(key, []) for key in sorted(indexed_records)},
            "reverse_dependencies": reverse_dependencies,
            "incremental": {"changed_files": changed, "reused_files": reused, "removed_files": removed},
            "skipped": {"oversized_files": sorted(oversized), "symlinks": symlinks, "parse_errors": sorted(parse_errors), "decode_errors": sorted(decode_errors)},
            "security": {"instructions_executed": 0, "untrusted_text_markers": untrusted_count, "network_calls": 0, "repository_writes": 0},
            "stats": {"indexed_files": len(indexed_records), "symbols": sum(len(r.get("symbols", [])) for r in indexed_records.values()), "dependency_edges": sum(len(v) for v in dependencies.values())},
        }
