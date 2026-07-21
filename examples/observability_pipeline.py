"""Local observability pipeline with safe telemetry contracts and self-tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import argparse
import json
import math
import re
from typing import Any

ALLOWED_ATTRIBUTES = {"tool", "outcome", "duration_ms", "policy_version"}
FORBIDDEN_LABELS = {"request_id", "run_id", "prompt", "email"}
SENSITIVE_KEY = re.compile(r"secret|token|password|api[_-]?key|credential", re.IGNORECASE)
SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?i)(?:[\"']?)(?:token|secret|password|api[_-]?key|apikey|access[_-]?token|"
        r"refresh[_-]?token|client[_-]?secret)(?:[\"']?)\s*[:=：＝]\s*"
        r"(?:\"[^\"\r\n]*\"|'[^'\r\n]*'|[^\s,;&}#\]]+)"
    ),
    re.compile(
        r"(?i)\b(?:token|secret|password|api[_-]?key|apikey|access[_-]?token|"
        r"refresh[_-]?token|client[_-]?secret)\s+"
        r"(?=[A-Za-z0-9._~+/=-]{6,}\b)(?=[A-Za-z0-9._~+/=-]*\d)"
        r"[A-Za-z0-9._~+/=-]+"
    ),
    re.compile(
        r"(?i)\b(?:bearer|basic)\s+"
        r"(?=[A-Za-z0-9._~+/=-]{6,}\b)(?=[A-Za-z0-9._~+/=-]*[0-9._~+/=-])"
        r"[A-Za-z0-9._~+/=-]+"
    ),
    re.compile(r"\beyJ[A-Za-z0-9_-]{2,}\.[A-Za-z0-9_-]{2,}\.[A-Za-z0-9_-]{2,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{8,}\b"),
    re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
)
URL_CREDENTIAL = re.compile(
    r"(?i)\b([a-z][a-z0-9+.-]*://[^:/@\s]+:)([^@\s/?#]+)(@)"
)
SUPPORTED_SCHEMA = "nexus.telemetry.v1"
REDACTED = "[REDACTED]"
MAX_DEPTH = 24
MAX_NODES = 2_048
MAX_STRING_LENGTH = 8_192
METRIC_NAME = re.compile(r"^[a-z][a-z0-9_.-]{0,127}$")
OWNER_NAME = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,127}$")
RUNBOOK_REF = re.compile(
    r"^(?:https://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+|[A-Za-z0-9._/-]+\.md)$"
)
ALLOWED_SEVERITIES = {"debug", "info", "warning", "error", "critical"}


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
        if isinstance(sample_rate, bool) or not isinstance(sample_rate, (int, float)):
            raise TypeError("sample_rate must be a number")
        if not math.isfinite(sample_rate):
            raise ValueError("sample_rate must be finite")
        if not 0.0 <= sample_rate <= 1.0:
            raise ValueError("sample_rate must be between 0 and 1")
        if isinstance(buffer_limit, bool) or not isinstance(buffer_limit, int):
            raise TypeError("buffer_limit must be an integer")
        if buffer_limit < 1:
            raise ValueError("buffer_limit must be positive")
        self.sample_rate = float(sample_rate)
        self.buffer_limit = buffer_limit
        self.collector_available = True
        self.persisted: list[dict[str, Any]] = []
        self.buffer: list[dict[str, Any]] = []
        self.quarantine: list[dict[str, Any]] = []
        self.seen_ids: set[str] = set()
        self._fingerprints: dict[str, str] = {}
        self._buffer_event_keys: list[str] = []
        self.metrics: dict[str, int] = {}
        self.alerts: list[Alert] = []

    @staticmethod
    def _redact_text(value: str) -> str:
        redacted = URL_CREDENTIAL.sub(r"\1[REDACTED]\3", value)
        for pattern in SENSITIVE_VALUE_PATTERNS:
            redacted = pattern.sub(REDACTED, redacted)
        return redacted

    @staticmethod
    def _require_text(value: Any, field_name: str, *, allow_empty: bool = False) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if len(value) > MAX_STRING_LENGTH:
            raise ValueError(f"{field_name} exceeds the size limit")
        if not allow_empty and not value.strip():
            raise ValueError(f"{field_name} is required")
        return value

    def _copy_json_safe(
        self,
        value: Any,
        *,
        depth: int = 0,
        active: set[int] | None = None,
        nodes: list[int] | None = None,
    ) -> Any:
        if depth > MAX_DEPTH:
            raise ValueError("telemetry attributes exceed the depth limit")
        active = set() if active is None else active
        nodes = [0] if nodes is None else nodes
        nodes[0] += 1
        if nodes[0] > MAX_NODES:
            raise ValueError("telemetry attributes exceed the node limit")
        if value is None or isinstance(value, (bool, int)):
            return value
        if isinstance(value, float):
            if not math.isfinite(value):
                raise ValueError("telemetry numbers must be finite")
            return value
        if isinstance(value, str):
            if len(value) > MAX_STRING_LENGTH:
                raise ValueError("telemetry string exceeds the size limit")
            return value
        if not isinstance(value, (dict, list, tuple)):
            raise TypeError("telemetry attributes must contain only JSON-safe values")
        identity = id(value)
        if identity in active:
            raise ValueError("cyclic telemetry attributes are not allowed")
        active.add(identity)
        try:
            if isinstance(value, dict):
                copied: dict[str, Any] = {}
                for key, item in value.items():
                    if not isinstance(key, str):
                        raise TypeError("telemetry attribute keys must be strings")
                    if len(key) > MAX_STRING_LENGTH:
                        raise ValueError("telemetry attribute key exceeds the size limit")
                    copied[key] = self._copy_json_safe(
                        item, depth=depth + 1, active=active, nodes=nodes
                    )
                return copied
            copied_items = [
                self._copy_json_safe(item, depth=depth + 1, active=active, nodes=nodes)
                for item in value
            ]
            return tuple(copied_items) if isinstance(value, tuple) else copied_items
        finally:
            active.remove(identity)

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

    def _sampled(self, event_id: str, severity: str) -> bool:
        if severity == "critical":
            return True
        if self.sample_rate == 0.0:
            return False
        if self.sample_rate == 1.0:
            return True
        bucket = int(sha256(event_id.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        return bucket < self.sample_rate

    def _prepare(self, event: Event) -> tuple[dict[str, Any], str, str, str]:
        if not isinstance(event, Event):
            raise TypeError("event must be an Event")
        event_id = self._require_text(event.event_id, "event_id")
        schema = self._require_text(event.schema, "schema")
        event_type = self._require_text(event.event_type, "event_type").casefold()
        if not METRIC_NAME.fullmatch(event_type):
            raise ValueError("event_type must be a stable low-cardinality name")
        severity = self._require_text(event.severity, "severity").casefold()
        if severity not in ALLOWED_SEVERITIES:
            raise ValueError("unsupported severity")
        request_id = self._require_text(event.request_id, "request_id")
        run_id = self._require_text(event.run_id, "run_id")
        if not isinstance(event.attributes, dict):
            raise TypeError("attributes must be a dictionary")
        detached_attributes = self._copy_json_safe(event.attributes)
        attributes = {
            key: self._redact(value, key)
            for key, value in detached_attributes.items()
            if key in ALLOWED_ATTRIBUTES or SENSITIVE_KEY.search(key)
        }
        normalized = {
            "event_id": self._redact_text(event_id),
            "schema": self._redact_text(schema),
            "event_type": event_type,
            "severity": severity,
            "request_id": self._redact_text(request_id),
            "run_id": self._redact_text(run_id),
            "attributes": attributes,
        }
        canonical = json.dumps(
            normalized,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        fingerprint = sha256(canonical.encode("utf-8")).hexdigest()
        event_key = sha256(event_id.encode("utf-8")).hexdigest()
        return normalized, event_key, fingerprint, schema

    def _increment_metric(self, name: str) -> None:
        self.metrics[name] = self.metrics.get(name, 0) + 1

    def _remember(self, event_key: str, fingerprint: str) -> None:
        self.seen_ids.add(event_key)
        self._fingerprints[event_key] = fingerprint

    def _forget(self, event_key: str) -> None:
        self.seen_ids.discard(event_key)
        self._fingerprints.pop(event_key, None)

    def _quarantine_event(
        self, normalized: dict[str, Any], reason: str, fingerprint: str
    ) -> None:
        self.quarantine.append(
            {
                **normalized,
                "quarantine_reason": reason,
                "content_fingerprint": fingerprint,
            }
        )

    def ingest(self, event: Event) -> str:
        normalized, event_key, fingerprint, schema = self._prepare(event)
        previous_fingerprint = self._fingerprints.get(event_key)
        if previous_fingerprint is not None:
            if previous_fingerprint == fingerprint:
                self._increment_metric("events.duplicate")
                return "duplicate"
            self._quarantine_event(normalized, "event_id_collision", fingerprint)
            self._increment_metric("events.event_id_collision")
            return "event_id_collision"
        if schema != SUPPORTED_SCHEMA:
            self._quarantine_event(normalized, "unsupported_schema", fingerprint)
            self._remember(event_key, fingerprint)
            self._increment_metric("events.quarantined")
            return "quarantined"
        severity = normalized["severity"]
        if not self._sampled(event.event_id, severity):
            self._remember(event_key, fingerprint)
            self._increment_metric("events.sampled_out")
            return "sampled_out"
        if self.collector_available:
            self.persisted.append(normalized)
            self._remember(event_key, fingerprint)
            self._increment_metric(f"events.{normalized['event_type']}")
            self._increment_metric("events.persisted")
            return "persisted"
        if len(self.buffer) >= self.buffer_limit:
            if severity == "critical":
                common_index = next(
                    (i for i, item in enumerate(self.buffer) if item["severity"] != "critical"),
                    None,
                )
                if common_index is None:
                    self._increment_metric("events.dropped")
                    return "critical_buffer_full"
                self.buffer.pop(common_index)
                evicted_key = self._buffer_event_keys.pop(common_index)
                self._forget(evicted_key)
                self._increment_metric("events.evicted")
            else:
                self._increment_metric("events.dropped")
                return "buffer_full"
        self.buffer.append(normalized)
        self._buffer_event_keys.append(event_key)
        self._remember(event_key, fingerprint)
        self._increment_metric(f"events.{normalized['event_type']}")
        self._increment_metric("events.buffered")
        return "buffered"

    def record_metric(self, name: str, labels: dict[str, str]) -> None:
        safe_name = self._require_text(name, "metric name").casefold()
        if not METRIC_NAME.fullmatch(safe_name) or self._redact_text(safe_name) != safe_name:
            raise ValueError("metric name must be stable and non-sensitive")
        if not isinstance(labels, dict):
            raise TypeError("metric labels must be a dictionary")
        if any(not isinstance(key, str) for key in labels):
            raise TypeError("metric label keys must be strings")
        forbidden = FORBIDDEN_LABELS.intersection(key.casefold() for key in labels)
        if forbidden:
            raise ValueError(f"forbidden labels: {sorted(forbidden)}")
        for key, value in labels.items():
            normalized_key = key.casefold()
            if not METRIC_NAME.fullmatch(normalized_key) or SENSITIVE_KEY.search(normalized_key):
                raise ValueError("metric label keys must be stable and non-sensitive")
            safe_value = self._require_text(value, "metric label value", allow_empty=True)
            if self._redact_text(safe_value) != safe_value:
                raise ValueError("metric labels must not contain sensitive values")
        self._increment_metric(safe_name)

    def create_alert(self, alert: Alert) -> None:
        if not isinstance(alert, Alert):
            raise TypeError("alert must be an Alert")
        raw = {
            field_name: self._require_text(getattr(alert, field_name), f"alert {field_name}")
            for field_name in ("name", "owner", "runbook", "condition")
        }
        sanitized = {name: self._redact_text(value) for name, value in raw.items()}
        owner = raw["owner"]
        email_match = re.fullmatch(r"(?i)([A-Z0-9._+-]+)@[A-Z0-9.-]+\.[A-Z]{2,}", owner)
        if email_match:
            owner = email_match.group(1).casefold()
        elif sanitized["owner"] != owner:
            raise ValueError("alert owner must be a stable non-sensitive operational identifier")
        owner = owner.casefold()
        if not OWNER_NAME.fullmatch(owner):
            raise ValueError("alert owner must be a stable non-sensitive operational identifier")
        sanitized["owner"] = owner
        if not RUNBOOK_REF.fullmatch(sanitized["runbook"]):
            raise ValueError("alert runbook must be a stable non-sensitive path or HTTPS URL")
        self.alerts.append(Alert(**sanitized))


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
    original = make_event("o15", schema="nexus.telemetry.v0", tool='{"token":"quarantineSecret123"}')
    status = p.ingest(original)
    q = p.quarantine[0]
    results.append(("O15 quarantine sanitized and input immutable", status == "quarantined" and "quarantineSecret123" not in json.dumps(q) and "quarantineSecret123" in original.attributes["tool"]))
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
