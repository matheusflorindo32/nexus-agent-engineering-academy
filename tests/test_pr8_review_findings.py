"""Regression tests for findings raised during the adversarial review of PR #8."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).parents[1] / "examples" / "observability_pipeline.py"
SPEC = spec_from_file_location("nexus_observability_pr8_review", MODULE_PATH)
assert SPEC and SPEC.loader
OBS = module_from_spec(SPEC)
sys.modules[SPEC.name] = OBS
SPEC.loader.exec_module(OBS)


class PR8ReviewFindingTests(unittest.TestCase):
    def test_evicted_event_can_be_retried_instead_of_becoming_false_duplicate(self) -> None:
        pipeline = OBS.ObservabilityPipeline(buffer_limit=1)
        pipeline.collector_available = False
        evicted = OBS.make_event("evicted-common", tool="catalog.read")

        self.assertEqual(pipeline.ingest(evicted), "buffered")
        self.assertEqual(
            pipeline.ingest(OBS.make_event("critical-replacement", severity="critical")),
            "buffered",
        )
        self.assertEqual(pipeline.metrics["events.evicted"], 1)

        pipeline.collector_available = True
        self.assertEqual(pipeline.ingest(evicted), "persisted")
        self.assertEqual(pipeline.persisted[0]["event_id"], "evicted-common")
        self.assertNotEqual(pipeline.metrics.get("events.duplicate", 0), 1)

    def test_alert_owner_remains_operational_and_sensitive_owner_is_rejected(self) -> None:
        pipeline = OBS.ObservabilityPipeline()
        pipeline.create_alert(
            OBS.Alert(
                "policy violation",
                "security-on-call@example.invalid",
                "runbooks/policy.md",
                "count > 0",
            )
        )
        self.assertEqual(pipeline.alerts[0].owner, "security-on-call")
        self.assertNotIn("@", pipeline.alerts[0].owner)

        with self.assertRaisesRegex(ValueError, "operational identifier"):
            pipeline.create_alert(
                OBS.Alert(
                    "policy violation",
                    "token=syntheticOwner123",
                    "runbooks/policy.md",
                    "count > 0",
                )
            )

    def test_runbook_with_embedded_credential_is_sanitized_but_remains_actionable(self) -> None:
        pipeline = OBS.ObservabilityPipeline()
        pipeline.create_alert(
            OBS.Alert(
                "collector failure",
                "sre-primary",
                "https://user:syntheticPassword123@example.invalid/runbook",
                "collector unavailable",
            )
        )
        runbook = pipeline.alerts[0].runbook
        self.assertIn("[REDACTED]", runbook)
        self.assertNotIn("syntheticPassword123", runbook)
        self.assertTrue(runbook.startswith("https://"))


if __name__ == "__main__":
    unittest.main()
