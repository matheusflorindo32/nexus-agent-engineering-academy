"""Adversarial verification for NEXUS Traceability Graph V2."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "examples" / "traceability_graph_v2.py"
MODEL = ROOT / ".nexus" / "traceability" / "model.json"


def load_engine():
    spec = importlib.util.spec_from_file_location("traceability_graph_v2_adversarial", ENGINE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TraceabilityGraphV2AdversarialTests(unittest.TestCase):
    def test_known_relation_with_wrong_node_types_is_rejected_as_graph_poisoning(self):
        module = load_engine()
        poisoned = {
            "nodes": [
                {"id": "req:1", "type": "requirement"},
                {"id": "evidence:1", "type": "evidence"},
            ],
            "edges": [
                {"source": "req:1", "target": "evidence:1", "type": "DEPENDS_ON"}
            ],
        }
        with self.assertRaises(module.GraphValidationError):
            module.TraceabilityGraph.from_document(poisoned)

    def test_orphan_spec_task_and_implementation_drift_are_diagnosed(self):
        module = load_engine()
        document = {
            "nodes": [
                {"id": "spec:o", "type": "spec"},
                {"id": "task:o", "type": "task"},
                {"id": "file:d", "type": "file", "path": "src/drift.py", "expected_hash": "a", "current_hash": "b"},
            ],
            "edges": [],
        }
        codes = {item["code"] for item in module.TraceabilityGraph.from_document(document).audit()["diagnostics"]}
        self.assertTrue({"ORPHAN_SPEC", "ORPHAN_TASK", "ORPHAN_IMPLEMENTATION", "IMPLEMENTATION_DRIFT"}.issubset(codes))

    def test_control_plane_model_routes_to_v2_schema(self):
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        self.assertEqual(".nexus/traceability/graph-v2.schema.json", model["graph_schema"])
        self.assertEqual("nexus.traceability.v2", model["schema_version"])


if __name__ == "__main__":
    unittest.main()
