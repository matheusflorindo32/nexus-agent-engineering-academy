"""Offline real-runtime trial for OpenAI Agents SDK 0.22.0.

The actual SDK runner/tool pipeline is executed. The model boundary is the official
ScriptedModel testing utility, so there is no OpenAI API request or model-performance claim.
"""
from __future__ import annotations

import argparse
import asyncio
from importlib.metadata import version
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
sys.path.insert(0, str(ROOT / "runtime_trials"))

from agent_reliability_runtime import ActionLedger, Approval, may_override
from common import evidence_base, load_cases, write_evidence


async def run_trial() -> dict[str, object]:
    from agents import Agent, RunConfig, Runner
    from agents.decorators import tool
    from agents.testing import ModelStep, ScriptedModel, assistant_message, function_call

    cases = load_cases()
    marker = cases["task"]["expected_marker"]
    package_version = version("openai-agents")
    if package_version != "0.22.0":
        raise RuntimeError(f"unexpected openai-agents version: {package_version}")

    ledger = ActionLedger()
    ledger.request("openai-op-1", "synthetic_write", "nexus-human")
    ledger.approve(Approval("openai-approval-1", "openai-op-1", "nexus-human", True))
    effect_calls = {"count": 0}

    @tool
    def synthetic_write(operation_id: str) -> str:
        """Perform one synthetic idempotent side effect for a pre-approved operation."""
        if operation_id != "openai-op-1":
            raise ValueError("unknown operation_id")

        def effect() -> tuple[str, object]:
            effect_calls["count"] += 1
            return "synthetic-resource-1", {"marker": marker}

        receipt = ledger.execute_once(operation_id, "synthetic_write", effect)
        return f"{receipt.status}:{receipt.resource_id}"

    model = ScriptedModel(
        [
            [function_call("synthetic_write", {"operation_id": "openai-op-1"}, call_id="call_1")],
            [function_call("synthetic_write", {"operation_id": "openai-op-1"}, call_id="call_2")],
            [assistant_message(marker)],
        ]
    )
    agent = Agent(name="NEXUS runtime trial", model=model, tools=[synthetic_write])

    started = time.monotonic()
    result = await asyncio.wait_for(
        Runner.run(
            agent,
            cases["task"]["input"],
            run_config=RunConfig(tracing_disabled=True),
        ),
        timeout=5.0,
    )
    duration_ms = round((time.monotonic() - started) * 1000, 3)
    model.assert_complete()

    verified = ledger.verify("openai-op-1", "synthetic-resource-1")
    task_success = 1.0 if result.final_output == marker else 0.0
    var = 1.0 if verified.status == "VERIFIED" else 0.0
    dser = 0.0 if effect_calls["count"] == 1 else 1.0

    failure_model = ScriptedModel(
        [ModelStep.raise_error(RuntimeError("nexus-injected-runtime-failure"))]
    )
    failure_agent = Agent(name="NEXUS failure trial", model=failure_model)
    failure_bounded = 0.0
    try:
        await asyncio.wait_for(
            Runner.run(
                failure_agent,
                cases["task"]["input"],
                run_config=RunConfig(tracing_disabled=True),
            ),
            timeout=5.0,
        )
    except asyncio.TimeoutError:
        failure_bounded = 0.0
    except Exception:
        failure_bounded = 1.0

    ctvr = 0.0 if not may_override("T6", "T1") else 1.0

    payload = evidence_base(
        adapter="openai-agents-sdk",
        package="openai-agents",
        package_version=package_version,
        boundary="real-sdk-runtime/official-scripted-model/no-external-provider",
    )
    payload["metrics"].update(
        {
            "task_success_rate": task_success,
            "verified_action_rate": var,
            "recovery_success_rate": failure_bounded,
            "duplicate_side_effect_rate": dser,
            "context_trust_violation_rate": ctvr,
            "runtime_duration_ms": duration_ms,
        }
    )
    payload["details"] = {
        "tool_calls_observed": 2,
        "synthetic_side_effect_count": effect_calls["count"],
        "failure_scenario": "official ScriptedModel injected error; bounded by asyncio timeout",
        "ctvr_scope": "NEXUS host policy only, not intrinsic SDK prompt-injection resistance",
    }
    payload["limitations"] = [
        "No OpenAI API request was made.",
        "No real model was used; ScriptedModel is the official deterministic SDK testing boundary.",
        "Provider latency, tokens and cost are NOT_EXECUTED.",
        "The idempotency/receipt authority is the NEXUS ActionLedger, exercised through the real SDK tool pipeline.",
    ]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="validation-evidence/runtime-openai.json")
    args = parser.parse_args()
    payload = asyncio.run(run_trial())
    write_evidence(payload, args.output)
    metrics = payload["metrics"]
    required = (
        metrics["task_success_rate"] == 1.0
        and metrics["verified_action_rate"] == 1.0
        and metrics["recovery_success_rate"] == 1.0
        and metrics["duplicate_side_effect_rate"] == 0.0
        and metrics["context_trust_violation_rate"] == 0.0
    )
    return 0 if required else 1


if __name__ == "__main__":
    raise SystemExit(main())
