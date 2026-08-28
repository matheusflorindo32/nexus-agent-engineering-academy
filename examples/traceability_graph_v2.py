"""NEXUS Traceability Graph V2: deterministic, bounded and stdlib-only."""
from __future__ import annotations

from collections import defaultdict, deque
import hashlib
import json
from pathlib import PurePosixPath
from typing import Any

NODE_TYPES = {"requirement", "spec", "task", "file", "symbol", "test", "evidence"}
EDGE_TYPES = {
    "REFINED_BY", "PLANNED_BY", "TOUCHES_FILE", "TOUCHES_SYMBOL",
    "CONTAINS_SYMBOL", "DEPENDS_ON", "VERIFIED_BY", "PRODUCES_EVIDENCE",
}
MAX_NODES = 2000
MAX_EDGES = 8000
MAX_FANOUT = 256
MAX_DEPTH = 16
MAX_METADATA_STRING = 2048
INJECTION_MARKERS = (
    "ignore previous", "ignore all previous", "system prompt", "execute tool",
    "call tool", "reveal secret", "developer message", "override instructions",
)


class GraphValidationError(ValueError):
    """Raised when graph input violates a bounded NEXUS contract."""


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _safe_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise GraphValidationError("invalid path")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        raise GraphValidationError("unsafe path")
    return str(path)


def _validate_metadata(value: Any, depth: int = 0) -> None:
    if depth > 8:
        raise GraphValidationError("metadata too deep")
    if isinstance(value, str):
        if len(value) > MAX_METADATA_STRING:
            raise GraphValidationError("metadata string too long")
        return
    if value is None or isinstance(value, (bool, int, float)):
        return
    if isinstance(value, list):
        for item in value:
            _validate_metadata(item, depth + 1)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or len(key) > 128:
                raise GraphValidationError("invalid metadata key")
            _validate_metadata(item, depth + 1)
        return
    raise GraphValidationError("metadata must be JSON-compatible")


def _contains_injection(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in INJECTION_MARKERS)
    if isinstance(value, list):
        return any(_contains_injection(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_injection(item) for item in value.values())
    return False


class TraceabilityGraph:
    def __init__(self, nodes: dict[str, dict[str, Any]], edges: tuple[dict[str, str], ...]):
        self.nodes = nodes
        self.edges = edges
        self.forward: dict[str, list[str]] = defaultdict(list)
        self.reverse: dict[str, list[str]] = defaultdict(list)
        self.edge_types_by_pair: dict[tuple[str, str], set[str]] = defaultdict(set)
        for edge in edges:
            source, target = edge["source"], edge["target"]
            self.forward[source].append(target)
            self.reverse[target].append(source)
            self.edge_types_by_pair[(source, target)].add(edge["type"])
        for mapping in (self.forward, self.reverse):
            for key in mapping:
                mapping[key].sort()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "TraceabilityGraph":
        if not isinstance(document, dict):
            raise GraphValidationError("graph document must be an object")
        raw_nodes = document.get("nodes")
        raw_edges = document.get("edges")
        if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
            raise GraphValidationError("nodes and edges must be arrays")
        if len(raw_nodes) > MAX_NODES or len(raw_edges) > MAX_EDGES:
            raise GraphValidationError("graph size limit exceeded")

        nodes: dict[str, dict[str, Any]] = {}
        for raw in raw_nodes:
            if not isinstance(raw, dict):
                raise GraphValidationError("node must be object")
            node = dict(raw)
            node_id = node.get("id")
            node_type = node.get("type")
            if not isinstance(node_id, str) or not node_id or len(node_id) > 256:
                raise GraphValidationError("invalid node id")
            if node_id in nodes:
                raise GraphValidationError("duplicate node id")
            if node_type not in NODE_TYPES:
                raise GraphValidationError("unknown node type")
            if "path" in node:
                node["path"] = _safe_path(node["path"])
            if "metadata" in node:
                if not isinstance(node["metadata"], dict):
                    raise GraphValidationError("metadata must be object")
                _validate_metadata(node["metadata"])
            if "symbol" in node and (not isinstance(node["symbol"], str) or len(node["symbol"]) > 512):
                raise GraphValidationError("invalid symbol")
            nodes[node_id] = node

        seen_edges: set[tuple[str, str, str]] = set()
        fanout: dict[str, int] = defaultdict(int)
        edges: list[dict[str, str]] = []
        for raw in raw_edges:
            if not isinstance(raw, dict):
                raise GraphValidationError("edge must be object")
            source, target, edge_type = raw.get("source"), raw.get("target"), raw.get("type")
            if source not in nodes or target not in nodes:
                raise GraphValidationError("edge references missing node")
            if edge_type not in EDGE_TYPES:
                raise GraphValidationError("unknown edge type")
            key = (source, target, edge_type)
            if key in seen_edges:
                raise GraphValidationError("duplicate edge")
            seen_edges.add(key)
            fanout[source] += 1
            if fanout[source] > MAX_FANOUT:
                raise GraphValidationError("fanout limit exceeded")
            edges.append({"source": source, "target": target, "type": edge_type})

        ordered_nodes = {key: nodes[key] for key in sorted(nodes)}
        ordered_edges = tuple(sorted(edges, key=lambda e: (e["source"], e["target"], e["type"])))
        return cls(ordered_nodes, ordered_edges)

    def to_document(self) -> dict[str, Any]:
        return {"schema": "nexus.traceability-graph.v2", "nodes": list(self.nodes.values()), "edges": list(self.edges)}

    def fingerprint(self) -> str:
        return hashlib.sha256(_canonical_json(self.to_document()).encode("utf-8")).hexdigest()

    def impact(self, node_id: str, direction: str = "both", depth: int = MAX_DEPTH) -> dict[str, Any]:
        if node_id not in self.nodes:
            raise GraphValidationError("unknown impact node")
        if direction not in {"downstream", "upstream", "both"}:
            raise GraphValidationError("invalid direction")
        if not isinstance(depth, int) or depth < 0 or depth > MAX_DEPTH:
            raise GraphValidationError("invalid depth")
        mappings = []
        if direction in {"downstream", "both"}:
            mappings.append(("downstream", self.forward))
        if direction in {"upstream", "both"}:
            mappings.append(("upstream", self.reverse))
        affected: set[str] = set()
        paths: list[dict[str, Any]] = []
        for label, mapping in mappings:
            queue = deque([(node_id, 0)])
            visited = {node_id}
            while queue:
                current, level = queue.popleft()
                if level >= depth:
                    continue
                for neighbor in mapping.get(current, []):
                    affected.add(neighbor)
                    paths.append({"from": current, "to": neighbor, "direction": label, "depth": level + 1})
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, level + 1))
        return {
            "schema": "nexus.traceability-impact.v2",
            "source": node_id,
            "direction": direction,
            "max_depth": depth,
            "affected_nodes": sorted(affected),
            "paths": sorted(paths, key=lambda p: (p["depth"], p["direction"], p["from"], p["to"])),
        }

    def _has_edge_type(self, node_id: str, outgoing: set[str] | None = None, incoming: set[str] | None = None) -> bool:
        if outgoing:
            for target in self.forward.get(node_id, []):
                if self.edge_types_by_pair[(node_id, target)] & outgoing:
                    return True
        if incoming:
            for source in self.reverse.get(node_id, []):
                if self.edge_types_by_pair[(source, node_id)] & incoming:
                    return True
        return False

    def _cycle_nodes(self) -> set[str]:
        visited: set[str] = set()
        active: set[str] = set()
        cycle: set[str] = set()

        def visit(node: str) -> None:
            if node in active:
                cycle.add(node)
                return
            if node in visited:
                return
            visited.add(node)
            active.add(node)
            for nxt in self.forward.get(node, []):
                if nxt in active:
                    cycle.update({node, nxt})
                else:
                    visit(nxt)
                    if nxt in cycle:
                        cycle.add(node)
            active.remove(node)

        for node_id in sorted(self.nodes):
            visit(node_id)
        return cycle

    def audit(self) -> dict[str, Any]:
        diagnostics: list[dict[str, Any]] = []

        def add(code: str, node_id: str, detail: str = "") -> None:
            diagnostics.append({"code": code, "node_id": node_id, "detail": detail})

        for node_id, node in self.nodes.items():
            node_type = node["type"]
            if node_type == "requirement" and not self._has_edge_type(node_id, outgoing={"REFINED_BY"}):
                add("ORPHAN_REQUIREMENT", node_id)
            elif node_type == "spec" and not self._has_edge_type(node_id, outgoing={"PLANNED_BY", "TOUCHES_FILE", "TOUCHES_SYMBOL"}):
                add("ORPHAN_SPEC", node_id)
            elif node_type == "task" and not self._has_edge_type(node_id, outgoing={"TOUCHES_FILE", "TOUCHES_SYMBOL", "PRODUCES_EVIDENCE"}):
                add("ORPHAN_TASK", node_id)
            elif node_type == "file" and not self._has_edge_type(node_id, incoming={"TOUCHES_FILE"}):
                add("ORPHAN_IMPLEMENTATION", node_id)
            elif node_type == "symbol" and not self._has_edge_type(node_id, incoming={"TOUCHES_SYMBOL", "CONTAINS_SYMBOL"}):
                add("ORPHAN_IMPLEMENTATION", node_id)
            elif node_type == "test" and not self._has_edge_type(node_id, incoming={"VERIFIED_BY"}):
                add("ORPHAN_TEST", node_id)
            elif node_type == "evidence" and not self._has_edge_type(node_id, incoming={"PRODUCES_EVIDENCE"}):
                add("ORPHAN_EVIDENCE", node_id)

            if node.get("expected_hash") is not None and node.get("current_hash") is not None and node["expected_hash"] != node["current_hash"]:
                add("SPEC_DRIFT" if node_type == "spec" else "IMPLEMENTATION_DRIFT", node_id)
            if node_type == "file" and node.get("exists") is False:
                add("STALE_FILE", node_id)
            if node_type == "symbol" and node.get("exists") is False:
                add("STALE_SYMBOL", node_id)
            if _contains_injection(node.get("metadata", {})):
                add("UNTRUSTED_METADATA", node_id, "metadata retained as data only")

        for node_id in sorted(self._cycle_nodes()):
            add("CYCLE", node_id)

        diagnostics.sort(key=lambda d: (d["code"], d["node_id"], d["detail"]))
        counts: dict[str, int] = defaultdict(int)
        for item in diagnostics:
            counts[item["code"]] += 1
        return {
            "schema": "nexus.traceability-audit.v2",
            "graph_fingerprint": self.fingerprint(),
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "diagnostics": diagnostics,
            "counts": dict(sorted(counts.items())),
        }
