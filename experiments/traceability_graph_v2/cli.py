"""CLI for NEXUS Traceability Graph V2."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "examples"))
from traceability_graph_v2 import GraphValidationError, TraceabilityGraph  # noqa: E402


def _read(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str, value: dict) -> None:
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _text(value: dict) -> str:
    lines = []
    for key, item in value.items():
        if isinstance(item, list):
            lines.append(f"{key}: {', '.join(str(x) for x in item)}")
        elif not isinstance(item, (dict, list)):
            lines.append(f"{key}: {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="NEXUS Traceability Graph V2")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build")
    build.add_argument("--input", required=True)
    build.add_argument("--output", required=True)
    build.add_argument("--receipt")

    impact = sub.add_parser("impact")
    impact.add_argument("--graph", required=True)
    impact.add_argument("--node", required=True)
    impact.add_argument("--direction", choices=["downstream", "upstream", "both"], default="both")
    impact.add_argument("--depth", type=int, default=16)
    impact.add_argument("--format", choices=["json", "text"], default="json")

    audit = sub.add_parser("audit")
    audit.add_argument("--graph", required=True)
    audit.add_argument("--format", choices=["json", "text"], default="json")

    args = parser.parse_args()
    try:
        if args.command == "build":
            graph = TraceabilityGraph.from_document(_read(args.input))
            document = graph.to_document()
            _write_json(args.output, document)
            result = {"graph_fingerprint": graph.fingerprint(), "node_count": len(graph.nodes), "edge_count": len(graph.edges)}
            if args.receipt:
                output = Path(args.output)
                receipt = {
                    "schema": "nexus.execution-receipt.traceability-graph-v2",
                    "evidence_class": "DETERMINISTIC_CONTROL_EVIDENCE",
                    "operation": "build",
                    "decision": "PASS",
                    "graph_fingerprint": graph.fingerprint(),
                    "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                    "runtime_dependencies_added": 0,
                }
                _write_json(args.receipt, receipt)
        elif args.command == "impact":
            graph = TraceabilityGraph.from_document(_read(args.graph))
            result = graph.impact(args.node, args.direction, args.depth)
        else:
            graph = TraceabilityGraph.from_document(_read(args.graph))
            result = graph.audit()
    except (GraphValidationError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"decision": "BLOCKED", "error": type(exc).__name__, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2

    if getattr(args, "format", "json") == "text":
        sys.stdout.write(_text(result))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
