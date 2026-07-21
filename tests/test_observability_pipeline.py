"""Security and reliability tests for the pedagogical observability pipeline."""

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import random
import sys
import unittest


MODULE_PATH = Path(__file__).parents[1] / "examples" / "observability_pipeline.py"
SPEC = spec_from_file_location("nexus_observability", MODULE_PATH)
assert SPEC and SPEC.loader
OBS = module_from_spec(SPEC)
sys.modules[SPEC.name] = OBS
SPEC.loader.exec_module(OBS)


def event_with_correlations(event_id: str, **changes: object):
    values = {
        "event_id": event_id,
        "schema": OBS.SUPPORTED_SCHEMA,
        "event_type": "run.completed",
        "severity": "info",
        "request_id": "req_test",
        "run_id": "run_test",
        "attributes": {},
    }
    values.update(changes)
    return OBS.Event(**values)


class ObservabilityPipelineTests(unittest.TestCase):
    def assert_secret_absent(self, value: object, secret: str) -> None:
        serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
        self.assertNotIn(secret, serialized)

    def test_redacts_structured_quoted_and_authorization_secrets_in_all_channels(self) -> None:
        corpus = (
            ("token=abc123", "abc123"),
            ("token: abc124", "abc124"),
            ("token abc125", "abc125"),
            ("secret=abc126", "abc126"),
            ("password=abc127", "abc127"),
            ("api_key=abc128", "abc128"),
            ("apikey=abc129", "abc129"),
            ("access_token=abc130", "abc130"),
            ("refresh_token=abc131", "abc131"),
            ("client_secret=abc132", "abc132"),
            ("Authorization: Bearer abc133", "abc133"),
            ("Bearer abc134", "abc134"),
            ("Basic abc135", "abc135"),
            ("sk-abc123456", "sk-abc123456"),
            ("ghp_abc123456", "ghp_abc123456"),
            (
                "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.syntheticSig123",
                "syntheticSig123",
            ),
            ("https://user:password@example.com/api", "password"),
            ("https://example.com/api?token=querySecret123&status=ok", "querySecret123"),
            ("postgresql://user:password@localhost/db", "password"),
            ('{"token":"syntheticJson123"}', "syntheticJson123"),
            ('password="synthetic secret tail"', "synthetic secret tail"),
            ("catalog.read client_secret='synthetic quoted value'", "synthetic quoted value"),
            ("ToKeN：unicodeSecret123", "unicodeSecret123"),
            ("token:\nlineSecret123", "lineSecret123"),
            (
                "token=multiOne123; password=multiTwo456, Bearer multiThree789",
                "multiOne123",
            ),
            (
                "token=multiOne123; password=multiTwo456, Bearer multiThree789",
                "multiTwo456",
            ),
            (
                "token=multiOne123; password=multiTwo456, Bearer multiThree789",
                "multiThree789",
            ),
        )
        for index, (payload, secret) in enumerate(corpus):
            with self.subTest(payload=payload):
                pipeline = OBS.ObservabilityPipeline()
                pipeline.ingest(OBS.make_event(f"persist-{index}", tool=payload))
                self.assert_secret_absent(pipeline.persisted, secret)

                pipeline = OBS.ObservabilityPipeline()
                pipeline.collector_available = False
                pipeline.ingest(OBS.make_event(f"buffer-{index}", tool=payload))
                self.assert_secret_absent(pipeline.buffer, secret)

                pipeline = OBS.ObservabilityPipeline()
                pipeline.ingest(
                    OBS.make_event(f"quarantine-{index}", schema="unsupported", tool=payload)
                )
                self.assert_secret_absent(pipeline.quarantine, secret)

    def test_redaction_is_idempotent_and_preserves_safe_text_and_scalar_types(self) -> None:
        safe_texts = (
            "token expires soon",
            "catalog.read completed successfully",
            "https://example.com/public/path",
            "basic authentication is disabled",
            "empty token documentation without a value",
        )
        for safe_text in safe_texts:
            self.assertEqual(OBS.ObservabilityPipeline._redact_text(safe_text), safe_text)

        sensitive = "prefix token=abc123 and Bearer def456789 suffix"
        once = OBS.ObservabilityPipeline._redact_text(sensitive)
        twice = OBS.ObservabilityPipeline._redact_text(once)
        self.assertEqual(once, twice)

        pipeline = OBS.ObservabilityPipeline()
        pipeline.ingest(
            OBS.make_event(
                "scalar-types",
                tool={"number": 42, "ratio": 1.5, "enabled": True, "empty": None},
            )
        )
        stored = pipeline.persisted[0]["attributes"]["tool"]
        self.assertEqual(stored, {"number": 42, "ratio": 1.5, "enabled": True, "empty": None})

    def test_nested_values_are_detached_and_sensitive_keys_are_redacted(self) -> None:
        attributes = {
            "tool": {
                "safe": ["catalog.read", {"token": "syntheticNested123"}],
                "tuple": ("ok", "password=syntheticTuple123"),
            }
        }
        pipeline = OBS.ObservabilityPipeline()
        pipeline.ingest(event_with_correlations("nested", attributes=attributes))
        attributes["tool"]["safe"][0] = "mutated-after-ingest"

        stored = pipeline.persisted[0]["attributes"]["tool"]
        self.assertEqual(stored["safe"][0], "catalog.read")
        self.assertIsInstance(stored["safe"], list)
        self.assertIsInstance(stored["tuple"], tuple)
        self.assertEqual(stored["safe"][1]["token"], OBS.REDACTED)
        self.assert_secret_absent(stored, "syntheticTuple123")

    def test_rejects_non_json_types_cycles_non_finite_values_and_excess_depth(self) -> None:
        invalid_values = [{"value"}, float("nan")]
        for index, value in enumerate(invalid_values):
            with self.subTest(value=type(value).__name__):
                pipeline = OBS.ObservabilityPipeline()
                with self.assertRaises((TypeError, ValueError)):
                    pipeline.ingest(OBS.make_event(f"invalid-{index}", tool=value))

        cycle: list[object] = []
        cycle.append(cycle)
        with self.assertRaisesRegex(ValueError, "cyclic"):
            OBS.ObservabilityPipeline().ingest(OBS.make_event("cycle", tool=cycle))

        deep: object = "safe"
        for _ in range(OBS.MAX_DEPTH + 2):
            deep = [deep]
        with self.assertRaisesRegex(ValueError, "depth"):
            OBS.ObservabilityPipeline().ingest(OBS.make_event("deep", tool=deep))

    def test_duplicate_is_distinct_from_event_id_collision(self) -> None:
        pipeline = OBS.ObservabilityPipeline()
        original = OBS.make_event("same-id", tool="catalog.read")
        self.assertEqual(pipeline.ingest(original), "persisted")
        self.assertEqual(pipeline.ingest(original), "duplicate")

        status = pipeline.ingest(OBS.make_event("same-id", tool="catalog.write"))
        self.assertEqual(status, "event_id_collision")
        self.assertEqual(pipeline.quarantine[0]["quarantine_reason"], "event_id_collision")
        self.assertEqual(pipeline.metrics["events.event_id_collision"], 1)
        self.assertEqual(len(pipeline.persisted), 1)

    def test_validation_and_capacity_failures_do_not_poison_event_id(self) -> None:
        pipeline = OBS.ObservabilityPipeline()
        with self.assertRaisesRegex(ValueError, "run_id"):
            pipeline.ingest(event_with_correlations("retry-validation", run_id=""))
        self.assertEqual(pipeline.ingest(OBS.make_event("retry-validation")), "persisted")

        pipeline = OBS.ObservabilityPipeline(buffer_limit=1)
        pipeline.collector_available = False
        self.assertEqual(pipeline.ingest(OBS.make_event("occupy")), "buffered")
        self.assertEqual(pipeline.ingest(OBS.make_event("retry-capacity")), "buffer_full")
        pipeline.buffer.clear()
        self.assertEqual(pipeline.ingest(OBS.make_event("retry-capacity")), "buffered")

    def test_quarantine_has_explicit_sanitized_metadata(self) -> None:
        pipeline = OBS.ObservabilityPipeline()
        original = OBS.make_event(
            "schema-event",
            schema="nexus.telemetry.v0",
            tool='{"token":"syntheticQuarantine123"}',
        )
        self.assertEqual(pipeline.ingest(original), "quarantined")
        quarantined = pipeline.quarantine[0]
        self.assertEqual(quarantined["quarantine_reason"], "unsupported_schema")
        self.assertRegex(quarantined["content_fingerprint"], r"^[0-9a-f]{64}$")
        self.assert_secret_absent(quarantined, "syntheticQuarantine123")
        self.assertIn("syntheticQuarantine123", original.attributes["tool"])

    def test_metrics_and_alerts_reject_or_redact_sensitive_values(self) -> None:
        pipeline = OBS.ObservabilityPipeline()
        with self.assertRaises(ValueError):
            pipeline.record_metric("token=syntheticMetric123", {})
        with self.assertRaises(ValueError):
            pipeline.record_metric("runs", {"Request_ID": "req_1"})
        with self.assertRaises(ValueError):
            pipeline.record_metric("runs", {"result": "Bearer syntheticLabel123"})
        with self.assertRaises(ValueError):
            pipeline.record_metric("runs", {"status": "person@example.invalid"})
        with self.assertRaises(ValueError):
            pipeline.record_metric("runs", {"token": "safe-looking-value"})
        pipeline.record_metric("runs", {"result": "success"})
        self.assertEqual(pipeline.metrics["runs"], 1)

        pipeline.create_alert(
            OBS.Alert(
                "token=syntheticAlert123",
                "person@example.invalid",
                "https://user:alertPassword123@example.com/runbook",
                'password="synthetic condition value"',
            )
        )
        self.assert_secret_absent(pipeline.alerts[0].__dict__, "syntheticAlert123")
        self.assert_secret_absent(pipeline.alerts[0].__dict__, "synthetic condition value")
        self.assert_secret_absent(pipeline.alerts[0].__dict__, "person@example.invalid")
        self.assert_secret_absent(pipeline.alerts[0].__dict__, "alertPassword123")

    def test_aggregate_serialization_of_every_channel_and_exception_is_sanitized(self) -> None:
        pipeline = OBS.ObservabilityPipeline(buffer_limit=2)
        pipeline.ingest(OBS.make_event("persisted-all", tool="token=aggregatePersist123"))
        pipeline.collector_available = False
        pipeline.ingest(OBS.make_event("buffer-all", tool="Bearer aggregateBuffer123"))
        pipeline.ingest(
            OBS.make_event(
                "quarantine-all",
                schema="unsupported",
                tool="postgresql://user:aggregateDatabase123@localhost/db",
            )
        )
        pipeline.create_alert(
            OBS.Alert(
                "password=aggregateAlert123",
                "security-on-call",
                "runbooks/security.md",
                "token=aggregateCondition123",
            )
        )
        errors = []
        try:
            pipeline.record_metric("runs", {"status": "aggregate@example.invalid"})
        except ValueError as error:
            errors.append(str(error))

        aggregate = {
            "persisted": pipeline.persisted,
            "buffer": pipeline.buffer,
            "quarantine": pipeline.quarantine,
            "metrics": pipeline.metrics,
            "alerts": [alert.__dict__ for alert in pipeline.alerts],
            "exceptions": errors,
        }
        serialized = json.dumps(aggregate, ensure_ascii=False, sort_keys=True)
        for secret in (
            "aggregatePersist123",
            "aggregateBuffer123",
            "aggregateDatabase123",
            "aggregateAlert123",
            "aggregateCondition123",
            "aggregate@example.invalid",
        ):
            self.assertNotIn(secret, serialized)

    def test_critical_severity_is_normalized_before_sampling_and_buffer_priority(self) -> None:
        pipeline = OBS.ObservabilityPipeline(sample_rate=0.0)
        self.assertEqual(pipeline.ingest(OBS.make_event("critical", severity="CRITICAL")), "persisted")
        self.assertEqual(pipeline.persisted[0]["severity"], "critical")

        pipeline = OBS.ObservabilityPipeline(sample_rate=0.0, buffer_limit=1)
        pipeline.collector_available = False
        pipeline.sample_rate = 1.0
        pipeline.ingest(OBS.make_event("common"))
        pipeline.sample_rate = 0.0
        self.assertEqual(
            pipeline.ingest(OBS.make_event("critical-buffer", severity="Critical")),
            "buffered",
        )
        self.assertEqual(pipeline.buffer[0]["severity"], "critical")
        self.assertEqual(pipeline.metrics["events.evicted"], 1)

    def test_event_type_and_constructor_contracts_are_bounded(self) -> None:
        with self.assertRaises(ValueError):
            OBS.ObservabilityPipeline().ingest(
                OBS.make_event("bad-type", event_type="token=syntheticType123")
            )
        with self.assertRaises(TypeError):
            OBS.ObservabilityPipeline(sample_rate=True)
        with self.assertRaises(ValueError):
            OBS.ObservabilityPipeline(sample_rate=float("inf"))
        with self.assertRaises(TypeError):
            OBS.ObservabilityPipeline(buffer_limit=1.5)

    def test_deterministic_light_fuzz_corpus_never_persists_generated_secret(self) -> None:
        generator = random.Random(20_260_719)
        templates = (
            "token={secret}",
            "token: {secret}",
            "token {secret}",
            '"api_key":"{secret}"',
            "password='{secret}'",
            "Bearer {secret}",
            "client-secret = \"{secret}\"",
            "TOKEN：{secret}",
            "https://user:{secret}@example.invalid/path",
            "https://example.invalid/path?access_token={secret}&ok=true",
            "token:\n{secret}",
        )
        for index in range(100):
            secret = "fuzz" + "".join(
                generator.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(18)
            )
            payload = generator.choice(templates).format(secret=secret)
            nested: object = payload
            for _ in range(generator.randrange(4)):
                nested = [nested]
            pipeline = OBS.ObservabilityPipeline()
            pipeline.ingest(OBS.make_event(f"fuzz-{index}", tool=nested))
            self.assert_secret_absent(pipeline.persisted, secret)


if __name__ == "__main__":
    unittest.main()
