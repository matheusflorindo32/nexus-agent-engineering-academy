"""Local observability pipeline with safe telemetry contracts and self-tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import argparse
import json
import re
from typing import Any

ALLOWED_ATTRIBUTES = {"tool", "outcome", "duration_ms", "policy_version"}
FORBIDDEN_LABELS = {"request_id", "run_id", "prompt", "email"}
SENSITIVE_KEY = re.compile(r"secret|token|password|api[_-]?key|credential", re.IGNORECASE)
SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?i)\b(?:token|secret|password|api[_-]?key|apikey|access[_-]?token|"
        r"refresh[_-]?token|client[_-]?secret)\s*[:=]\s*[^\s,;]+"
    ),
    re.compile(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{8,}\b"),
)
SUPPORTED_SCHEMA = "nexus.telemetry.v1"
REDACTED = "[REDACTED]"


@dataclass(frozen=True)
class Event:
    event_id: str
    schema: str
    event_type: str
    severity: str
    request_id: str
    run_id: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Alert:
    name: str
    owner: str
    runbook: str
    condition: str


class ObservabilityPipeline:
    """Collect, sanitize, sample and persist telemetry deterministically."""

    def __init__(self, sample_rate: float = 1.0, buffer_limit: int = 4) -> None:
        if not 0.0 <= sample_rate <= 1.0:
            raise ValueError("sample_rate must be between 0 and 1")
        if buffer_limit < 1:
            raise ValueError("buffer_limit must be positive")
        self.sample_rate = sample_rate
        self.buffer_limit = buffer_limit
        self.collector_available = True
        self.persisted: list[dict[str, Any]] = []
        self.buffer: list[dict[str, Any]] = []
        self.quarantine: list[dict[str, Any]] = []
        self.seen_ids: set[str] = set()
        self.metrics: dict[str, int] = {}
        self.alerts: list[Alert] = []

    @staticmethod
    def _redact_text(value: str) -> str:
        redacted = value
        for pattern in SENSITIVE_VALUE_PATTERNS:
            redacted = pattern.sub(REDACTED, redacted)
        return redacted

    def _redact(self, value: Any, key: str = "") -> Any:
        if SENSITIVE_KEY.search(key):
            return REDACTED
        if isinstance(value, dict):
            return {k: self._redact(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [self._redact(item, key) for item in value]
        if isinstance(value, tuple):
            return tuple(self._redact(item, key) for item in value)
        if isinstance(value, str):
            return self._redact_text(value)
        return value

    def _sampled(self, event: Event) -> bool:
        if event.severity == "critical":
            return True
        if self.sample_rate == 0.0:
            return False
        if self.sample_rate == 1.0:
            return True
        bucket = int(sha256(event.event_id.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        return bucket < self.sample_rate

    def _normalized(self, event: Event) -> dict[str, Any]:
        attributes = {
            key: self._redact(value, key)
            for key, value in event.attributes.items()
            if key in ALLOWED_ATTRIBUTES or SENSITIVE_KEY.search(key)
        }
        return {
            "event_id": self._redact_text(event.event_id),
            "schema": self._redact_text(event.schema),
            "event_type": self._redact_text(event.event_type),
            "severity": self._redact_text(event.severity),
            "request_id": self._redact_text(event.request_id),
            "run_id": self._redact_text(event.run_id),
            "attributes": attributes,
        }

    def ingest(self, event: Event) -> str:
        if event.event_id in self.seen_ids:
            return "duplicate"
        self.seen_ids.add(event.event_id)

        normalized = self._normalized(event)
        if event.schema != SUPPORTED_SCHEMA:
            self.quarantine.append(normalized)
            return "quarantined"
        if not event.request_id or not event.run_id:
            raise ValueError("correlation IDs are required")
        if not self._sampled(event):
            return "sampled_out"

        self.metrics[f"events.{event.event_type}"] = self.metrics.get(
            f"events.{event.event_type}", 0
        ) + 1

        if self.collector_available:
            self.persisted.append(normalized)
            return "persisted"

        if len(self.buffer) >= self.buffer_limit:
            if event.severity == "critical":
                common_index = next(
                    (i for i, item in enumerate(self.buffer) if item["severity"] != "critical"),
                    None,
                )
                if common_index is None:
                    return "critical_buffer_full"
                self.buffer.pop(common_index)
            else:
                return "buffer_full"
        self.buffer.append(normalized)
        return "buffered"

    def record_metric(self, name: str, labels: dict[str, str]) -> None:
        forbidden = FORBIDDEN_LABELS.intersection(labels)
        if forbidden:
            raise ValueError(f"forbidden labels: {sorted(forbidden)}")
        self.metrics[name] = self.metrics.get(name, 0) + 1

    def create_alert(self, alert: Alert) -> None:
        if not alert.owner.strip() or not alert.runbook.strip() or not alert.condition.strip():
            raise ValueError("alert requires owner, runbook and condition")
        self.alerts.append(alert)


def make_event(
    event_id: str,
    event_type: str = "run.completed",
    severity: str = "info",
    schema: str = SUPPORTED_SCHEMA,
    **attributes: Any,
) -> Event:
    return Event(
        event_id=event_id,
        schema=schema,
        event_type=event_type,
        severity=severity,
        request_id="req_demo",
        run_id="run_demo",
        attributes=attributes,
    )


def run_self_tests() -> None:
    results: list[tuple[str, bool]] = []

    p = ObservabilityPipeline()
    results.append(("O1 healthy execution", p.ingest(make_event("o1")) == "persisted"))

    p = ObservabilityPipeline()
    p.ingest(make_event("o2", token="sensitive-value", tool="catalog.read"))
    results.append(("O2 sensitive key redaction", p.persisted[0]["attributes"]["token"] == REDACTED))

    p = ObservabilityPipeline()
    try:
        p.record_metric("runs", {"request_id": "req_1"})
        ok = False
    except ValueError:
        ok = True
    results.append(("O3 forbidden metric label", ok))

    p = ObservabilityPipeline(sample_rate=0.0)
    results.append(("O4 critical preserved", p.ingest(make_event("o4", severity="critical")) == "persisted"))

    p = ObservabilityPipeline(sample_rate=0.0)
    results.append(("O5 common sampled out", p.ingest(make_event("o5")) == "sampled_out"))

    p = ObservabilityPipeline()
    p.ingest(make_event("o6", event_type="tool.timeout", outcome="error"))
    results.append(("O6 timeout metric", p.metrics.get("events.tool.timeout") == 1))

    p = ObservabilityPipeline()
    p.ingest(make_event("o7", event_type="policy.violation", severity="critical", policy_version="12"))
    p.create_alert(Alert("policy violation", "security-on-call", "runbooks/policy.md", "count > 0"))
    results.append(("O7 critical audit alert", len(p.alerts) == 1 and len(p.persisted) == 1))

    p = ObservabilityPipeline(buffer_limit=2)
    p.collector_available = False
    results.append(("O8 collector degradation", p.ingest(make_event("o8")) == "buffered"))

    p = ObservabilityPipeline(buffer_limit=2)
    p.collector_available = False
    p.ingest(make_event("o9a"))
    p.ingest(make_event("o9b"))
    status = p.ingest(make_event("o9c", severity="critical"))
    results.append(("O9 critical buffer priority", status == "buffered" and any(e["severity"] == "critical" for e in p.buffer)))

    p = ObservabilityPipeline()
    results.append(("O10 incompatible schema", p.ingest(make_event("o10", schema="nexus.telemetry.v0")) == "quarantined"))

    p = ObservabilityPipeline()
    p.ingest(make_event("o11"))
    results.append(("O11 duplicate ignored", p.ingest(make_event("o11")) == "duplicate" and len(p.persisted) == 1))

    p = ObservabilityPipeline()
    try:
        p.create_alert(Alert("bad", "", "", "count > 0"))
        ok = False
    except ValueError:
        ok = True
    results.append(("O12 invalid alert rejected", ok))

    p = ObservabilityPipeline()
    p.ingest(make_event("o13", tool="catalog.read token=abc123", outcome="success"))
    tool_value = p.persisted[0]["attributes"]["tool"]
    results.append(("O13 embedded key-value secret redacted", "abc123" not in tool_value and REDACTED in tool_value))

    p = ObservabilityPipeline()
    p.ingest(make_event("o14", tool="catalog.read", outcome="Bearer demoCredential123"))
    outcome_value = p.persisted[0]["attributes"]["outcome"]
    results.append(("O14 authorization credential redacted", "demoCredential123" not in outcome_value and REDACTED in outcome_value))

    p = ObservabilityPipeline()
    original = make_event(
        "o15",
        schema="nexus.telemetry.v0",
        tool="catalog.read client_secret=synthetic-only",
    )
    status = p.ingest(original)
    quarantined_tool = p.quarantine[0]["attributes"]["tool"]
    results.append((
        "O15 quarantine sanitized without mutating input",
        status == "quarantined"
        and "synthetic-only" not in quarantined_tool
        and REDACTED in quarantined_tool
        and original.attributes["tool"].endswith("synthetic-only"),
    ))

    failed = [name for name, passed in results if not passed]
    for name, passed in results:
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
    if failed:
        raise SystemExit(f"self-test failed: {', '.join(failed)}")
    print(f"Observability self-test passed: {len(results)}/{len(results)} scenarios.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        run_self_tests()
        return
    pipeline = ObservabilityPipeline()
    pipeline.ingest(make_event("demo", tool="catalog.read", outcome="success", duration_ms=42))
    print(json.dumps(pipeline.persisted, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
