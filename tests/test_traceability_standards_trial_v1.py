"""Contract and reproducibility tests for Traceability & Standards Runtime Trial V1."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "traceability_standards_v1"
ALLOWED = {
    "REAL_RUNTIME_EVIDENCE",
    "DETERMINISTIC_CONTROL_EVIDENCE",
    "DOCUMENTED_UPSTREAM_CAPABILITY",
    "INFERRED",
    "NOT_TESTED",
    "NOT_APPLICABLE",
}


def load_json(name: str):
    return json.loads((EXP / name).read_text(encoding="utf-8"))


def load_trial_module():
    path = EXP / "trial.py"
    spec = importlib.util.spec_from_file_location("traceability_trial_v1", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TraceabilityStandardsTrialV1Tests(unittest.TestCase):
    def test_frozen_artifacts_exist(self):
        required = ["protocol.json", "fixtures.json", "upstream_capabilities.json", "trial.py"]
        missing = [name for name in required if not (EXP / name).is_file()]
        self.assertEqual([], missing)

    def test_fixture_ids_and_expected_faults_are_bounded(self):
        fixtures = load_json("fixtures.json")
        ids = [case["case_id"] for case in fixtures["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 8)
        allowed_faults = {
            "none", "orphan_requirement", "orphan_implementation", "spec_drift",
            "change_impact", "wrong_standard", "missing_provenance", "prompt_injection",
            "tool_poisoning", "duplicate_effect", "regression"
        }
        self.assertTrue(all(case["fault"] in allowed_faults for case in fixtures["cases"]))

    def test_upstream_runtime_claims_are_explicitly_not_tested(self):
        data = load_json("upstream_capabilities.json")
        for item in data["projects"]:
            self.assertIn(item["evidence_class"], ALLOWED)
            self.assertEqual("NOT_TESTED", item["runtime_evidence"])
            self.assertNotIn("runtime_score", item)

    def test_identical_fixtures_are_used_by_both_executable_conditions(self):
        module = load_trial_module()
        fixtures = load_json("fixtures.json")
        result = module.run_trial(fixtures)
        self.assertEqual(
            result["conditions"]["baseline_ungoverned"]["case_ids"],
            result["conditions"]["nexus_control_plane_v1"]["case_ids"],
        )

    def test_result_evidence_classes_and_metrics_are_bounded(self):
        module = load_trial_module()
        result = module.run_trial(load_json("fixtures.json"))
        protocol = load_json("protocol.json")
        expected_metrics = set(protocol["metrics"])
        for condition in result["conditions"].values():
            self.assertEqual("DETERMINISTIC_CONTROL_EVIDENCE", condition["evidence_class"])
            self.assertEqual(expected_metrics, set(condition["metrics"]))

    def test_nexus_detects_more_governance_faults_without_duplicate_effects(self):
        module = load_trial_module()
        result = module.run_trial(load_json("fixtures.json"))
        base = result["conditions"]["baseline_ungoverned"]["metrics"]
        nexus = result["conditions"]["nexus_control_plane_v1"]["metrics"]
        self.assertGreater(nexus["traceability_coverage"], base["traceability_coverage"])
        self.assertGreater(nexus["spec_drift_detection_rate"], base["spec_drift_detection_rate"])
        self.assertGreater(nexus["hostile_input_rejection_rate"], base["hostile_input_rejection_rate"])
        self.assertEqual(0.0, nexus["duplicate_side_effect_rate"])

    def test_protocol_repetitions_are_executed(self):
        module = load_trial_module()
        protocol = load_json("protocol.json")
        result = module.run_trial(load_json("fixtures.json"))
        repetitions = protocol["repetitions"]
        self.assertEqual(repetitions, result["repetitions"])
        for condition in result["conditions"].values():
            self.assertEqual(repetitions, len(condition["runs"]))
            self.assertTrue(all(run == condition["metrics"] for run in condition["runs"]))

    def test_trial_is_deterministic(self):
        module = load_trial_module()
        fixtures = load_json("fixtures.json")
        self.assertEqual(module.run_trial(fixtures), module.run_trial(fixtures))


if __name__ == "__main__":
    unittest.main()
