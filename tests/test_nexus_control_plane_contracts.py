"""Contract tests for the declarative NEXUS Spec-Driven Control Plane V1."""
from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
NEXUS = ROOT / ".nexus"


def load_json(relative: str) -> dict[str, object]:
    return json.loads((NEXUS / relative).read_text(encoding="utf-8"))


class NexusControlPlaneContractsTest(unittest.TestCase):
    def test_required_control_plane_artifacts_exist(self) -> None:
        required = (
            "constitution.md",
            "rigor-levels.json",
            "standards/registry.json",
            "traceability/model.json",
            "schemas/spec.schema.json",
            "schemas/task.schema.json",
            "schemas/execution-receipt.schema.json",
            "hooks/hooks.json",
            "gates/release-gates.json",
        )
        missing = [name for name in required if not (NEXUS / name).is_file()]
        self.assertEqual([], missing, f"missing control-plane artifacts: {missing}")

    def test_rigor_levels_are_complete_and_ordered(self) -> None:
        data = load_json("rigor-levels.json")
        ids = [item["id"] for item in data["levels"]]
        self.assertEqual(
            [
                "L0_TRIVIAL",
                "L1_STANDARD",
                "L2_CRITICAL",
                "L3_HIGH_ASSURANCE",
                "L4_RESEARCH_SAFETY_CRITICAL",
            ],
            ids,
        )
        self.assertTrue(all(item["required_gates"] for item in data["levels"]))

    def test_standards_registry_has_unique_ids_and_valid_decisions(self) -> None:
        data = load_json("standards/registry.json")
        standards = data["standards"]
        ids = [item["id"] for item in standards]
        self.assertEqual(len(ids), len(set(ids)))
        allowed = {"ADOPT", "ADAPT", "STUDY", "MONITOR", "REJECT", "NOT_APPLICABLE"}
        self.assertTrue(standards)
        self.assertTrue(all(item["decision"] in allowed for item in standards))
        self.assertTrue(all(item["applies_when"] and item["controls"] for item in standards))

    def test_schemas_are_versioned_closed_and_have_core_fields(self) -> None:
        expectations = {
            "schemas/spec.schema.json": {"schema_version", "spec_id", "requirements", "acceptance_criteria", "rigor_level"},
            "schemas/task.schema.json": {"schema_version", "task_id", "spec_id", "requirements", "tests", "status"},
            "schemas/execution-receipt.schema.json": {"schema_version", "task_id", "commit_sha", "timestamp", "tests", "results", "decision"},
        }
        for path, fields in expectations.items():
            with self.subTest(path=path):
                schema = load_json(path)
                self.assertEqual("object", schema["type"])
                self.assertFalse(schema["additionalProperties"])
                self.assertTrue(fields.issubset(set(schema["required"])))
                self.assertIn("$id", schema)

    def test_traceability_requires_full_chain_and_bounded_statuses(self) -> None:
        data = load_json("traceability/model.json")
        self.assertEqual(
            ["requirement", "spec", "task", "files_or_symbols", "tests", "evidence"],
            data["chain"],
        )
        self.assertEqual(
            {"PLANNED", "IMPLEMENTED", "VERIFIED", "BLOCKED", "NOT_APPLICABLE"},
            set(data["statuses"]),
        )

    def test_hooks_default_to_non_destructive_actions(self) -> None:
        data = load_json("hooks/hooks.json")
        forbidden = {"merge", "deploy", "delete", "rotate_credentials"}
        for hook in data["hooks"]:
            self.assertTrue(hook["enabled_by_default"])
            self.assertTrue(set(hook["actions"]).isdisjoint(forbidden))
        self.assertTrue(forbidden.issubset(set(data["requires_explicit_human_authorization"])))

    def test_release_gates_preserve_human_merge_authority(self) -> None:
        data = load_json("gates/release-gates.json")
        self.assertEqual({"PASS", "BLOCKED", "GO"}, set(data["decisions"]))
        self.assertTrue(data["human_merge_authority"])
        self.assertFalse(data["auto_merge_allowed"])
        self.assertTrue(data["evidence_required_for"]["PASS"])
        self.assertTrue(data["evidence_required_for"]["GO"])

    def test_constitution_contains_non_negotiable_invariants(self) -> None:
        text = (NEXUS / "constitution.md").read_text(encoding="utf-8")
        for phrase in (
            "Evidence Before Assertion",
            "No Fabricated Results",
            "Human Authority",
            "Independent Verification",
            "Minimal Complexity",
            "Requirement → Spec → Task → Code → Test → Evidence",
        ):
            self.assertIn(phrase, text)

    def test_agents_entrypoint_routes_to_control_plane(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for phrase in (
            "NEXUS Spec-Driven Control Plane",
            ".nexus/constitution.md",
            ".nexus/rigor-levels.json",
            ".nexus/standards/registry.json",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
