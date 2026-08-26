"""Normalized experimental adapter contracts for NEXUS Provider Adapters V3.

This module is deliberately stdlib-only and performs no provider network calls.
It records verified upstream versions and exercises the same NEXUS control-plane
invariants for OpenAI Agents SDK, Google ADK and MCP.

It is a contract/conformance layer, not evidence of real SDK performance.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable

from agent_reliability_runtime import (
    ActionLedger,
    Approval,
    BoundedChannel,
    TransportClosed,
    may_override,
)


@dataclass(frozen=True)
class AdapterSpec:
    adapter_id: str
    upstream: str
    version: str
    verified_at: str
    kind: str
    tool_calls: bool
    hitl: bool
    tracing: bool
    state: bool
    mcp: bool
    notes: tuple[str, ...] = ()


SPECS: tuple[AdapterSpec, ...] = (
    AdapterSpec(
        adapter_id="openai-agents-sdk",
        upstream="openai/openai-agents-python",
        version="0.22.0",
        verified_at="2026-08-26",
        kind="sdk",
        tool_calls=True,
        hitl=True,
        tracing=True,
        state=True,
        mcp=True,
        notes=("contract adapter; no provider request in CI",),
    ),
    AdapterSpec(
        adapter_id="google-adk-python",
        upstream="google/adk-python",
        version="2.7.1",
        verified_at="2026-08-26",
        kind="sdk",
        tool_calls=True,
        hitl=True,
        tracing=True,
        state=True,
        mcp=True,
        notes=("A2A/HITL upstream issue remains MONITORING/POTENTIALLY_APPLICABLE",),
    ),
    AdapterSpec(
        adapter_id="mcp-2026-07-28",
        upstream="modelcontextprotocol/modelcontextprotocol",
        version="2026-07-28",
        verified_at="2026-08-26",
        kind="protocol",
        tool_calls=True,
        hitl=False,
        tracing=False,
        state=False,
        mcp=True,
        notes=("stateless protocol core; host owns approval/policy/tracing",),
    ),
)


@dataclass(frozen=True)
class ScenarioResult:
    adapter_id: str
    verified_action_rate: float
    recovery_success_rate: float
    duplicate_side_effect_rate: float
    context_trust_violation_rate: float
    claims_scope: str = "nexus-contract-layer-only"


def _verified_action_scenario() -> float:
    ledger = ActionLedger()
    ledger.request("op-verified", "publish", "human-1")
    ledger.approve(Approval("approval-1", "op-verified", "human-1", True))
    receipt = ledger.execute_once(
        "op-verified", "publish", lambda: ("resource-1", {"ok": True})
    )
    if receipt.status != "EXECUTED":
        return 0.0
    return 1.0 if ledger.verify("op-verified", "resource-1").status == "VERIFIED" else 0.0


def _recovery_scenario() -> float:
    """Verify that a terminal transport failure becomes a bounded observable error."""
    channel: BoundedChannel[str] = BoundedChannel()
    channel.fail(ConnectionError("synthetic transport failure"))
    try:
        channel.get(0.05)
    except TransportClosed:
        return 1.0
    except TimeoutError:
        return 0.0
    return 0.0


def _duplicate_side_effect_scenario() -> float:
    ledger = ActionLedger()
    ledger.request("op-once", "delete", "human-1")
    ledger.approve(Approval("approval-2", "op-once", "human-1", True))
    calls = {"count": 0}

    def effect() -> tuple[str, object]:
        calls["count"] += 1
        return "resource-x", {"deleted": True}

    ledger.execute_once("op-once", "delete", effect)
    ledger.execute_once("op-once", "delete", effect)
    return 0.0 if calls["count"] == 1 else 1.0


def _context_trust_scenario() -> float:
    # T6 external/MCP content must not override repository-controlled T1.
    return 0.0 if not may_override("T6", "T1") else 1.0


def run_contract(adapter: AdapterSpec) -> ScenarioResult:
    """Run the same deterministic NEXUS invariants for one adapter declaration."""
    return ScenarioResult(
        adapter_id=adapter.adapter_id,
        verified_action_rate=_verified_action_scenario(),
        recovery_success_rate=_recovery_scenario(),
        duplicate_side_effect_rate=_duplicate_side_effect_scenario(),
        context_trust_violation_rate=_context_trust_scenario(),
    )


def benchmark(specs: Iterable[AdapterSpec] = SPECS) -> dict[str, object]:
    materialized = tuple(specs)
    results = [run_contract(spec) for spec in materialized]
    return {
        "schema": "nexus.provider-adapter-contract-benchmark.v1",
        "scope": "deterministic NEXUS contract parity; not real provider performance",
        "specs": [asdict(spec) for spec in materialized],
        "results": [asdict(result) for result in results],
        "limitations": [
            "No provider SDK is installed or invoked by this benchmark.",
            "No model/API call is made and no latency/token/cost claim is produced.",
            "Identical scores mean the NEXUS wrapper contract is identical, not that frameworks are equivalent.",
        ],
    }


def main() -> int:
    payload = benchmark()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    failures = [
        item
        for item in payload["results"]
        if item["verified_action_rate"] != 1.0
        or item["recovery_success_rate"] != 1.0
        or item["duplicate_side_effect_rate"] != 0.0
        or item["context_trust_violation_rate"] != 0.0
    ]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
