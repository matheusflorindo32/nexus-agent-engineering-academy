"""Static guards for Provider Runtime Trial V1 protocol and pins."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProviderRuntimeTrialV1StaticTests(unittest.TestCase):
    def test_common_case_is_versioned_and_deterministic(self) -> None:
        payload = json.loads(
            (ROOT / "benchmarks" / "provider_runtime_trial_v1_cases.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema"], "nexus.provider-runtime-trial.cases.v1")
        self.assertEqual(payload["task"]["expected_marker"], "NEXUS_RUNTIME_OK")
        self.assertEqual(payload["adversarial_context"]["trust_level"], "T6")

    def test_runtime_top_level_dependencies_are_exactly_pinned(self) -> None:
        expected = {
            "openai.txt": "openai-agents==0.22.0",
            "google-adk.txt": "google-adk==2.8.0",
            "mcp.txt": "mcp==2.1.1",
        }
        for filename, pin in expected.items():
            value = (ROOT / "requirements" / "runtime" / filename).read_text(encoding="utf-8").strip()
            self.assertEqual(value, pin)

    def test_protocol_forbids_provider_claims_from_offline_trial(self) -> None:
        protocol = (ROOT / "docs" / "research" / "PROTOCOL_PROVIDER_RUNTIME_COMPARISON_V1.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Runtime Trial com SDK/protocolo real e modelo simulado/in-process", protocol)
        self.assertIn("Provider/Model Trial", protocol)
        self.assertIn("nenhuma credencial real", protocol)

    def test_runtime_evidence_binds_pr_head_sha(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "provider-runtime-trial.yml").read_text(
            encoding="utf-8"
        )
        common = (ROOT / "runtime_trials" / "common.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(workflow.count("NEXUS_HEAD_SHA"), 3)
        self.assertIn('github.event.pull_request.head.sha', workflow)
        self.assertIn('"workflow_sha"', common)


if __name__ == "__main__":
    unittest.main()
