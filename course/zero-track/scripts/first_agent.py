"""Primeiro agente NEXUS: local, determinístico, read-only e sem credenciais."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from typing import Any

ALLOWED_FIELDS = {"mission", "max_steps"}
ALLOWED_MISSIONS = {"explain_capabilities", "check_readiness"}
MAX_STEPS = 3


@dataclass(frozen=True)
class AgentResult:
    status: str
    mission: str
    steps_used: int
    tool: str | None
    output: dict[str, Any]
    reason: str


def validate_request(payload: dict[str, Any]) -> tuple[str, int]:
    unknown = set(payload) - ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"unknown fields: {sorted(unknown)}")

    mission = payload.get("mission")
    max_steps = payload.get("max_steps", MAX_STEPS)

    if not isinstance(mission, str) or not mission:
        raise ValueError("mission must be a non-empty string")
    if not isinstance(max_steps, int) or isinstance(max_steps, bool):
        raise ValueError("max_steps must be an integer")
    if not 1 <= max_steps <= MAX_STEPS:
        raise ValueError(f"max_steps must be between 1 and {MAX_STEPS}")

    return mission, max_steps


def tool_explain_capabilities() -> dict[str, Any]:
    return {
        "capabilities": [
            "validate a bounded request",
            "select one allowlisted read-only tool",
            "record a structured decision",
            "refuse unsupported missions",
        ],
        "limitations": [
            "no model inference",
            "no network",
            "no file or environment access",
            "no system commands",
            "no side effects",
        ],
    }


def tool_check_readiness() -> dict[str, Any]:
    return {
        "ready_for_module_00": False,
        "required_evidence": [
            "complete Z00-Z09",
            "pass exit assessment",
            "finish the integrative project",
            "document one refusal and one limitation",
        ],
        "note": "This local result does not replace pedagogical review.",
    }


def run_agent(payload: dict[str, Any]) -> AgentResult:
    mission, max_steps = validate_request(payload)
    steps = 1  # validate request

    if mission not in ALLOWED_MISSIONS:
        return AgentResult(
            status="refused",
            mission=mission,
            steps_used=steps,
            tool=None,
            output={},
            reason="mission is outside the allowlist",
        )

    if steps >= max_steps:
        return AgentResult(
            status="stopped",
            mission=mission,
            steps_used=steps,
            tool=None,
            output={},
            reason="step budget exhausted before tool execution",
        )

    steps += 1
    if mission == "explain_capabilities":
        tool = "explain_capabilities"
        output = tool_explain_capabilities()
    else:
        tool = "check_readiness"
        output = tool_check_readiness()

    return AgentResult(
        status="completed",
        mission=mission,
        steps_used=steps,
        tool=tool,
        output=output,
        reason="mission completed with an allowlisted read-only tool",
    )


def demo() -> None:
    result = run_agent({"mission": "explain_capabilities", "max_steps": 3})
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))


def self_test() -> None:
    completed = run_agent({"mission": "explain_capabilities", "max_steps": 3})
    assert completed.status == "completed"
    assert completed.tool == "explain_capabilities"
    assert completed.steps_used == 2

    refused = run_agent({"mission": "read_credentials", "max_steps": 3})
    assert refused.status == "refused"
    assert refused.tool is None

    stopped = run_agent({"mission": "check_readiness", "max_steps": 1})
    assert stopped.status == "stopped"
    assert stopped.tool is None

    try:
        run_agent({"mission": "check_readiness", "max_steps": 3, "command": "rm -rf"})
    except ValueError as exc:
        assert "unknown fields" in str(exc)
    else:
        raise AssertionError("unknown fields must be rejected")

    try:
        run_agent({"mission": "check_readiness", "max_steps": 9})
    except ValueError as exc:
        assert "between 1 and 3" in str(exc)
    else:
        raise AssertionError("invalid step budget must be rejected")

    print("first_agent self-test: 5/5 passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
    elif args.demo:
        demo()
    else:
        parser.error("use --demo or --self-test")


if __name__ == "__main__":
    main()
