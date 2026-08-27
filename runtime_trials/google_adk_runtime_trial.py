"""Offline real-runtime trial for Google ADK Python 2.8.0.

The actual ADK Runner and session service are executed with a custom BaseLlm that
never reaches an external provider. This is runtime evidence, not model/provider evidence.
"""
from __future__ import annotations

import argparse
import asyncio
from collections.abc import AsyncIterator
from importlib.metadata import version
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
sys.path.insert(0, str(ROOT / "runtime_trials"))

from agent_reliability_runtime import may_override
from common import evidence_base, load_cases, write_evidence


async def run_trial() -> dict[str, object]:
    from google.adk.agents import LlmAgent
    from google.adk.models.base_llm import BaseLlm
    from google.adk.models.llm_response import LlmResponse
    from google.adk.runners import Runner
    from google.adk.sessions.in_memory_session_service import InMemorySessionService
    from google.genai import types

    cases = load_cases()
    marker = cases["task"]["expected_marker"]
    package_version = version("google-adk")
    if package_version != "2.8.0":
        raise RuntimeError(f"unexpected google-adk version: {package_version}")

    class OfflineMarkerLlm(BaseLlm):
        model: str = "nexus-offline-marker"

        async def generate_content_async(
            self, llm_request: Any, stream: bool = False
        ) -> AsyncIterator[LlmResponse]:
            del llm_request, stream
            yield LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=marker)],
                ),
                turn_complete=True,
            )

    service = InMemorySessionService()
    session = await service.create_session(
        app_name="nexus_runtime_trial",
        user_id="nexus-user",
    )
    runner = Runner(
        agent=LlmAgent(name="nexus_root", model=OfflineMarkerLlm()),
        app_name="nexus_runtime_trial",
        session_service=service,
    )

    started = time.monotonic()
    texts: list[str] = []

    async def consume() -> None:
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(
                role="user",
                parts=[types.Part.from_text(text=cases["task"]["input"])],
            ),
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if getattr(part, "text", None):
                        texts.append(part.text)

    await asyncio.wait_for(consume(), timeout=5.0)
    duration_ms = round((time.monotonic() - started) * 1000, 3)
    task_success = 1.0 if marker in texts else 0.0

    class FailingLlm(BaseLlm):
        model: str = "nexus-offline-failure"

        async def generate_content_async(
            self, llm_request: Any, stream: bool = False
        ) -> AsyncIterator[LlmResponse]:
            del llm_request, stream
            raise RuntimeError("nexus-injected-runtime-failure")
            if False:
                yield LlmResponse()  # pragma: no cover

    fail_service = InMemorySessionService()
    fail_session = await fail_service.create_session(
        app_name="nexus_failure_trial",
        user_id="nexus-user",
    )
    fail_runner = Runner(
        agent=LlmAgent(name="nexus_failure_root", model=FailingLlm()),
        app_name="nexus_failure_trial",
        session_service=fail_service,
    )

    async def consume_failure() -> None:
        async for _ in fail_runner.run_async(
            user_id=fail_session.user_id,
            session_id=fail_session.id,
            new_message=types.Content(
                role="user",
                parts=[types.Part.from_text(text=cases["task"]["input"])],
            ),
        ):
            pass

    failure_bounded = 0.0
    try:
        await asyncio.wait_for(consume_failure(), timeout=5.0)
    except asyncio.TimeoutError:
        failure_bounded = 0.0
    except Exception:
        failure_bounded = 1.0

    ctvr = 0.0 if not may_override("T6", "T1") else 1.0

    payload = evidence_base(
        adapter="google-adk-python",
        package="google-adk",
        package_version=package_version,
        boundary="real-sdk-runtime/custom-BaseLlm-offline/no-external-provider",
    )
    payload["metrics"].update(
        {
            "task_success_rate": task_success,
            "verified_action_rate": None,
            "recovery_success_rate": failure_bounded,
            "duplicate_side_effect_rate": None,
            "context_trust_violation_rate": ctvr,
            "runtime_duration_ms": duration_ms,
        }
    )
    payload["details"] = {
        "session_events_with_text": len(texts),
        "failure_scenario": "custom BaseLlm raises deterministic RuntimeError; bounded by asyncio timeout",
        "var_status": "NOT_EXECUTED_NOT_EQUIVALENT",
        "dser_status": "NOT_EXECUTED_NOT_EQUIVALENT",
        "ctvr_scope": "NEXUS host policy only, not intrinsic ADK prompt-injection resistance",
    }
    payload["limitations"] = [
        "No Gemini/Vertex/third-party provider request was made.",
        "The real ADK Runner and InMemorySessionService were used with an offline BaseLlm.",
        "A2A/HITL pause-resume is NOT_EXECUTED in this first smoke boundary.",
        "VAR/DSER are not scored because an equivalent side-effect tool scenario is not implemented in this adapter yet.",
    ]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="validation-evidence/runtime-google-adk.json")
    args = parser.parse_args()
    payload = asyncio.run(run_trial())
    write_evidence(payload, args.output)
    metrics = payload["metrics"]
    required = (
        metrics["task_success_rate"] == 1.0
        and metrics["recovery_success_rate"] == 1.0
        and metrics["context_trust_violation_rate"] == 0.0
    )
    return 0 if required else 1


if __name__ == "__main__":
    raise SystemExit(main())
