"""Contract tests for SpecD Isolated Runtime Trial V1."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "specd_isolated_v1"
WORKFLOW = ROOT / ".github" / "workflows" / "specd-isolated-runtime-trial.yml"
UPSTREAM_COMMIT = "14422dba5c1cc64f04205f3ebfa3d435cd790aa0"
BASE_SHA = "d712c03dc5a97e3e349f884d6bb79e5900341208"
ALLOWED_EVIDENCE = {
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
    spec = importlib.util.spec_from_file_location("specd_trial", EXP / "trial.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SpecDIsolatedRuntimeTrialV1Tests(unittest.TestCase):
    def test_required_trial_artifacts_exist(self):
        required = [
            EXP / "protocol.json",
            EXP / "fixture_manifest.json",
            EXP / "trial.py",
            EXP / "fixture" / "oracle.json",
            EXP / "fixture" / "src" / "core.ts",
            EXP / "fixture" / "src" / "service.ts",
            EXP / "fixture" / "src" / "controller.ts",
            EXP / "fixture" / "src" / "unrelated.ts",
            WORKFLOW,
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_protocol_pins_base_upstream_and_repetitions(self):
        protocol = load_json("protocol.json")
        self.assertEqual(BASE_SHA, protocol["base_sha"])
        self.assertEqual(UPSTREAM_COMMIT, protocol["upstream"]["commit"])
        self.assertEqual("specd-sdd/SpecD", protocol["upstream"]["repository"])
        self.assertEqual(5, protocol["repetitions"])
        self.assertEqual("source-pinned", protocol["upstream"]["runtime_mode"])

    def test_protocol_bounds_non_equivalent_metrics(self):
        protocol = load_json("protocol.json")
        self.assertGreater(len(protocol["not_comparable_metrics"]), 0)
        self.assertNotIn("global_framework_score", protocol["comparable_metrics"])
        self.assertTrue(
            set(protocol["not_comparable_evidence_classes"]).issubset(ALLOWED_EVIDENCE)
        )

    def test_fixture_manifest_hashes_are_sha256(self):
        manifest = load_json("fixture_manifest.json")
        self.assertGreaterEqual(len(manifest["files"]), 5)
        for item in manifest["files"]:
            digest = item["sha256"]
            self.assertEqual(64, len(digest))
            int(digest, 16)

    def test_oracle_separates_affected_and_unaffected_files(self):
        oracle = json.loads((EXP / "fixture" / "oracle.json").read_text(encoding="utf-8"))
        self.assertEqual("src/core.ts", oracle["target_file"])
        self.assertIn("src/service.ts", oracle["expected_affected_files"])
        self.assertIn("src/controller.ts", oracle["expected_affected_files"])
        self.assertIn("src/unrelated.ts", oracle["expected_unaffected_files"])

    def test_workflow_builds_exact_upstream_commit_and_invokes_real_cli(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(UPSTREAM_COMMIT, text)
        self.assertIn("pnpm install --frozen-lockfile", text)
        self.assertIn("graph index", text)
        self.assertIn("graph impact", text)
        self.assertNotIn("@specd/cli@latest", text)

    def test_unexpected_affected_file_counts_against_precision(self):
        module = load_trial_module()
        oracle = {
            "target_file": "src/core.ts",
            "expected_affected_files": ["src/service.ts", "src/controller.ts"],
            "expected_unaffected_files": ["src/unrelated.ts"],
        }
        payload = {
            "affectedFiles": [
                "src/core.ts",
                "src/service.ts",
                "src/controller.ts",
                "src/extra.ts",
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw"
            raw.mkdir()
            oracle_path = root / "oracle.json"
            oracle_path.write_text(json.dumps(oracle), encoding="utf-8")
            for index in range(1, 6):
                (raw / f"impact-{index}.json").write_text(json.dumps(payload), encoding="utf-8")
            result = module.evaluate(raw, oracle_path, 5)
        self.assertEqual(0.666667, result["metrics"]["affected_file_precision"])
        self.assertEqual(0.0, result["metrics"]["false_positive_rate"])
        self.assertEqual(1, result["metrics"]["unexpected_affected_files"])

    def test_workflow_preserves_failure_phase_and_graph_blockers(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for marker in [
            "UPSTREAM_PACKAGE_MANAGER_SETUP_FAILED",
            "UPSTREAM_FROZEN_LOCKFILE_MISMATCH",
            "UPSTREAM_DEPENDENCY_INSTALL_FAILED",
            "UPSTREAM_BUILD_FAILED",
            "UPSTREAM_CLI_SMOKE_FAILED",
            "UPSTREAM_GRAPH_INDEX_FAILED",
            "UPSTREAM_GRAPH_IMPACT_FAILED",
            "failure_phase",
        ]:
            self.assertIn(marker, text)

    def test_workflow_does_not_rerun_known_blocked_pin_without_recheck_candidate(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("SPECD_RECHECK_ENABLED", text)
        self.assertIn("MONITOR", text)
        self.assertIn("known_blocked_commit", text)


if __name__ == "__main__":
    unittest.main()
