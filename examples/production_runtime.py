"""Production-readiness reference runtime for NEXUS Module 09.

This stdlib-only example models version compatibility, health checks, canary
promotion, hard gates, safe degradation, kill switch and complete rollback.
It performs no network calls and no real external effects.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import argparse
import json
from typing import Iterable


@dataclass(frozen=True)
class ReleaseState:
    artifact_digest: str
    config_version: int
    policy_version: int
    schema_version: int
    model_route: str = "approved-default"


@dataclass(frozen=True)
class SLO:
    min_success_rate: float = 0.97
    max_p95_latency_ms: int = 2500
    max_cost_per_success: float = 0.08
    max_critical_policy_violations: int = 0


@dataclass(frozen=True)
class Metrics:
    success_rate: float
    p95_latency_ms: int
    cost_per_success: float
    critical_policy_violations: int = 0


@dataclass(frozen=True)
class HealthReport:
    startup: bool
    liveness: bool
    readiness: bool
    deep_health: bool
    backup_restore_verified: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Decision:
    action: str
    reason: str
    rollout_percent: int


class ProductionRuntime:
    """Deterministic control-plane simulation with deny-by-default promotion."""

    def __init__(self, stable: ReleaseState, candidate: ReleaseState, slo: SLO | None = None) -> None:
        self.stable = stable
        self.candidate = candidate
        self.active = stable
        self.slo = slo or SLO()
        self.rollout_percent = 0
        self.kill_switch = False
        self.degraded_read_only = False
        self.audit: list[dict[str, object]] = []

    def _record(self, event: str, **fields: object) -> None:
        self.audit.append({"event": event, **fields})

    def health(self, *, dependency_ok: bool = True, deep_probe_ok: bool = True,
               backup_restore_verified: bool = True) -> HealthReport:
        reasons: list[str] = []
        compatible = (
            self.candidate.config_version > 0
            and self.candidate.policy_version > 0
            and self.candidate.schema_version == self.stable.schema_version
            and self.candidate.artifact_digest.startswith("sha256:")
        )
        if not compatible:
            reasons.append("incompatible_release_contract")
        if not dependency_ok:
            reasons.append("dependency_unavailable")
        if not deep_probe_ok:
            reasons.append("deep_health_failed")
        if not backup_restore_verified:
            reasons.append("backup_restore_unverified")
        report = HealthReport(
            startup=True,
            liveness=True,
            readiness=compatible and dependency_ok and deep_probe_ok and backup_restore_verified,
            deep_health=deep_probe_ok,
            backup_restore_verified=backup_restore_verified,
            reasons=tuple(reasons),
        )
        self._record("health", **asdict(report))
        return report

    def evaluate(self, metrics: Metrics) -> tuple[bool, str]:
        if metrics.critical_policy_violations > self.slo.max_critical_policy_violations:
            return False, "critical_policy_violation"
        if metrics.success_rate < self.slo.min_success_rate:
            return False, "success_rate_below_slo"
        if metrics.p95_latency_ms > self.slo.max_p95_latency_ms:
            return False, "p95_latency_above_slo"
        if metrics.cost_per_success > self.slo.max_cost_per_success:
            return False, "cost_per_success_above_slo"
        return True, "all_release_gates_passed"

    def start_canary(self, health: HealthReport, initial_percent: int = 5) -> Decision:
        if self.kill_switch:
            return Decision("blocked", "kill_switch_enabled", self.rollout_percent)
        if not health.readiness:
            return Decision("blocked", "readiness_failed", self.rollout_percent)
        if initial_percent not in {1, 5, 10}:
            return Decision("blocked", "unsafe_initial_canary_percent", self.rollout_percent)
        self.active = self.candidate
        self.rollout_percent = initial_percent
        decision = Decision("canary_started", "readiness_passed", self.rollout_percent)
        self._record("rollout", **asdict(decision))
        return decision

    def advance(self, metrics: Metrics, next_percent: int) -> Decision:
        passed, reason = self.evaluate(metrics)
        if self.kill_switch:
            return self.rollback("kill_switch_enabled")
        if not passed:
            return self.rollback(reason)
        if next_percent <= self.rollout_percent or next_percent > 100:
            return Decision("blocked", "invalid_rollout_transition", self.rollout_percent)
        self.rollout_percent = next_percent
        action = "promoted" if next_percent == 100 else "advanced"
        decision = Decision(action, reason, self.rollout_percent)
        self._record("rollout", **asdict(decision))
        return decision

    def rollback(self, reason: str) -> Decision:
        self.active = self.stable
        self.rollout_percent = 0
        self.degraded_read_only = False
        decision = Decision("rolled_back", reason, 0)
        self._record("rollback", **asdict(decision), restored_state=asdict(self.active))
        return decision

    def degrade(self, dependency_ok: bool) -> str:
        if dependency_ok:
            self.degraded_read_only = False
            return "normal"
        self.degraded_read_only = True
        self._record("degradation", mode="read_only", privilege_expansion=False)
        return "read_only"

    def enable_kill_switch(self) -> None:
        self.kill_switch = True
        self._record("kill_switch", enabled=True)

    def external_effect_allowed(self) -> bool:
        return not self.kill_switch and not self.degraded_read_only

    def report(self) -> dict[str, object]:
        return {
            "active": asdict(self.active),
            "stable": asdict(self.stable),
            "candidate": asdict(self.candidate),
            "slo": asdict(self.slo),
            "rollout_percent": self.rollout_percent,
            "kill_switch": self.kill_switch,
            "degraded_read_only": self.degraded_read_only,
            "audit": self.audit,
        }


def _runtime(*, candidate_schema: int = 5) -> ProductionRuntime:
    stable = ReleaseState("sha256:stable", 16, 11, 5)
    candidate = ReleaseState("sha256:candidate", 17, 12, candidate_schema)
    return ProductionRuntime(stable, candidate)


def run_self_tests() -> int:
    tests: list[tuple[str, bool]] = []

    runtime = _runtime()
    tests.append(("P1 compatible readiness", runtime.health().readiness))
    tests.append(("P2 incompatible schema blocked", not _runtime(candidate_schema=6).health().readiness))

    runtime = _runtime()
    runtime.start_canary(runtime.health())
    d = runtime.advance(Metrics(0.99, 1500, 0.04), 25)
    tests.append(("P3 healthy canary advances", d.action == "advanced" and d.rollout_percent == 25))

    runtime = _runtime(); runtime.start_canary(runtime.health())
    d = runtime.advance(Metrics(0.99, 1500, 0.04, 1), 25)
    tests.append(("P4 critical violation rolls back", d.action == "rolled_back" and runtime.active == runtime.stable))

    runtime = _runtime(); runtime.start_canary(runtime.health())
    tests.append(("P5 success regression rolls back", runtime.advance(Metrics(0.90, 1500, 0.04), 25).action == "rolled_back"))

    runtime = _runtime(); runtime.start_canary(runtime.health())
    tests.append(("P6 latency regression rolls back", runtime.advance(Metrics(0.99, 3000, 0.04), 25).action == "rolled_back"))

    runtime = _runtime(); runtime.start_canary(runtime.health())
    tests.append(("P7 excessive cost rejected", runtime.advance(Metrics(0.99, 1500, 0.12), 25).action == "rolled_back"))

    runtime = _runtime()
    tests.append(("P8 dependency failure degrades read-only", runtime.degrade(False) == "read_only" and not runtime.external_effect_allowed()))

    stable = ReleaseState("sha256:stable", 16, 11, 5)
    incomplete = replace(stable, config_version=17)
    tests.append(("P9 code-only rollback is detectably incomplete", incomplete != stable))

    runtime = _runtime(); runtime.start_canary(runtime.health()); runtime.rollback("test")
    tests.append(("P10 complete rollback restores state", runtime.active == runtime.stable and runtime.rollout_percent == 0))

    tests.append(("P11 unverified restore blocks readiness", not _runtime().health(backup_restore_verified=False).readiness))

    runtime = _runtime(); runtime.enable_kill_switch()
    tests.append(("P12 kill switch blocks effects", not runtime.external_effect_allowed()))

    failed = [name for name, passed in tests if not passed]
    for name, passed in tests:
        print(f"{'PASS' if passed else 'FAIL'} - {name}")
    print(json.dumps({"passed": len(tests) - len(failed), "total": len(tests), "failed": failed}, ensure_ascii=False))
    return 1 if failed else 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.self_test:
        return run_self_tests()
    runtime = _runtime()
    health = runtime.health()
    runtime.start_canary(health)
    runtime.advance(Metrics(0.99, 1700, 0.05), 25)
    print(json.dumps(runtime.report(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
