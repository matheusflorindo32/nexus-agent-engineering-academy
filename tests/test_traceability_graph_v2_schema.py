"""TDD contract for the persistent NEXUS Traceability Graph V2 schema."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / ".nexus" / "traceability" / "graph-v2.schema.json"


class TraceabilityGraphV2SchemaTest(unittest.TestCase):
    def test_schema_persists_authoritative_graph_contract(self):
        self.assertTrue(SCHEMA.is_file(), "Graph V2 schema must live in the NEXUS Control Plane")
        data = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual("nexus.traceability-graph.v2", data["schema_version"])
        self.assertEqual(
            ["requirement", "spec", "task", "file", "symbol", "test", "evidence"],
            data["node_types"],
        )
        self.assertEqual(256, data["limits"]["max_fanout"])
        self.assertEqual(16, data["limits"]["max_depth"])
        self.assertIn("DEPENDS_ON", data["edge_types"])
        self.assertIn("PRODUCES_EVIDENCE", data["edge_types"])
        self.assertEqual("human_authority_preserved", data["authority"])


if __name__ == "__main__":
    unittest.main()
