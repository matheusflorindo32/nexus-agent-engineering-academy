"""Contract test for the persistent Repository Indexer V1 schema."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / ".nexus" / "traceability" / "repository-indexer-v1.schema.json"


class RepositoryIndexerV1SchemaTest(unittest.TestCase):
    def test_schema_persists_read_only_index_contract(self):
        self.assertTrue(SCHEMA.is_file())
        doc = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", doc["$schema"])
        self.assertEqual("nexus.repository-index.v1", doc["properties"]["schema"]["const"])
        self.assertEqual("read-only", doc["properties"]["root_mode"]["const"])
        self.assertIn("graph", doc["required"])
        self.assertIn("fingerprint", doc["required"])
        self.assertIn("security", doc["required"])
        self.assertFalse(doc["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
