"""Regression tests for validated PR #59 Codex review findings."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "examples" / "traceability_graph_v2.py"


def load_graph():
    spec = importlib.util.spec_from_file_location("traceability_graph_v2_review", GRAPH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TraceabilityGraphV2ReviewRegressions(unittest.TestCase):
    def test_long_valid_dependency_chain_does_not_raise_recursion_error(self):
        module = load_graph()
        count = 1200
        nodes = [{"id": f"file:{i}", "type": "file", "path": f"src/{i}.py"} for i in range(count)]
        edges = [
            {"source": f"file:{i}", "target": f"file:{i+1}", "type": "DEPENDS_ON"}
            for i in range(count - 1)
        ]
        graph = module.TraceabilityGraph.from_document({"nodes": nodes, "edges": edges})
        audit = graph.audit()
        self.assertNotIn("CYCLE", {item["code"] for item in audit["diagnostics"]})

    def test_cycle_diagnostics_only_mark_members_of_actual_cycle(self):
        module = load_graph()
        document = {
            "nodes": [
                {"id": "req:1", "type": "requirement"},
                {"id": "spec:1", "type": "spec"},
                {"id": "task:1", "type": "task"},
                {"id": "file:1", "type": "file", "path": "src/1.py"},
                {"id": "file:2", "type": "file", "path": "src/2.py"},
            ],
            "edges": [
                {"source": "req:1", "target": "spec:1", "type": "REFINED_BY"},
                {"source": "spec:1", "target": "task:1", "type": "PLANNED_BY"},
                {"source": "task:1", "target": "file:1", "type": "TOUCHES_FILE"},
                {"source": "file:1", "target": "file:2", "type": "DEPENDS_ON"},
                {"source": "file:2", "target": "file:1", "type": "DEPENDS_ON"},
            ],
        }
        diagnostics = module.TraceabilityGraph.from_document(document).audit()["diagnostics"]
        cycle_nodes = {item["node_id"] for item in diagnostics if item["code"] == "CYCLE"}
        self.assertEqual({"file:1", "file:2"}, cycle_nodes)


if __name__ == "__main__":
    unittest.main()
