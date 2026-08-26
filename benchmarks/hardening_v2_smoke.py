"""Deterministic smoke benchmark for NEXUS Hardening V2 controls.

This benchmark measures the reference control plane only. It is not evidence
that any external framework is safer or more reliable.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "agent_reliability_runtime.py"
SPEC = importlib.util.spec_from_file_location("agent_reliability_runtime_benchmark", MODULE_PATH)
assert SPEC and SPEC.loader
runtime = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime
SPEC.loader.exec_module(runtime)


def run(iterations: int) -> dict[str, object]:
    if iterations < 1:
        raise ValueError("iterations must be >= 1")

    declared_actions = 0
    verified_actions = 0
    side_effect_calls = 0
    duplicate_side_effects = 0
    recovery_attempts = 0
    recovery_successes = 0
    trust_cases = 0
    trust_violations = 0
    started = time.perf_counter()

    for index in range(iterations):
        ledger = runtime.ActionLedger()
        operation_id = f"op-{index}"
        ledger.request(operation_id, "publish", "human")
        ledger.approve(runtime.Approval(f"ap-{index}", operation_id, "human", True))
        declared_actions += 1
        calls = {"count": 0}

        def effect():
            nonlocal side_effect_calls
            calls["count"] += 1
            side_effect_calls += 1
            return f"resource-{index}", {"iteration": index, "ok": True}

        ledger.execute_once(operation_id, "publish", effect)
        ledger.execute_once(operation_id, "publish", effect)
        if calls["count"] > 1:
            duplicate_side_effects += calls["count"] - 1
        receipt = ledger.verify(operation_id, f"resource-{index}")
        if receipt.status == "VERIFIED":
            verified_actions += 1

        recovery_attempts += 1
        channel = runtime.BoundedChannel()
        channel.fail(ConnectionError("synthetic terminal transport failure"))
        try:
            channel.get(0.01)
        except runtime.TransportClosed:
            recovery_successes += 1

        trust_cases += 1
        if runtime.may_override("T6", "T1"):
            trust_violations += 1

    duration = time.perf_counter() - started
    return {
        "schema": "nexus.hardening-v2-benchmark.v1",
        "benchmark_type": "deterministic-control-plane-smoke",
        "iterations": iterations,
        "duration_seconds": round(duration, 6),
        "metrics": {
            "verified_action_rate": verified_actions / declared_actions,
            "recovery_success_rate": recovery_successes / recovery_attempts,
            "duplicate_side_effect_rate": duplicate_side_effects / max(side_effect_calls, 1),
            "context_trust_violation_rate": trust_violations / trust_cases,
        },
        "counts": {
            "declared_actions": declared_actions,
            "verified_actions": verified_actions,
            "side_effect_calls": side_effect_calls,
            "duplicate_side_effects": duplicate_side_effects,
            "recovery_attempts": recovery_attempts,
            "recovery_successes": recovery_successes,
            "trust_cases": trust_cases,
            "trust_violations": trust_violations,
        },
        "limitations": [
            "No LLM, provider, network, database or external framework is used.",
            "Results validate only the deterministic NEXUS reference controls.",
            "Do not compare these values directly with framework benchmarks.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.iterations)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        path = args.output if args.output.is_absolute() else ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    print(payload, end="")
    metrics = result["metrics"]
    return 0 if (
        metrics["verified_action_rate"] == 1.0
        and metrics["recovery_success_rate"] == 1.0
        and metrics["duplicate_side_effect_rate"] == 0.0
        and metrics["context_trust_violation_rate"] == 0.0
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
