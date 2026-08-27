"""In-process real-runtime trial for MCP Python SDK 2.1.1 / spec 2026-07-28."""
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

from agent_reliability_runtime import may_override
from common import evidence_base, load_cases, write_evidence


async def run_trial() -> dict[str, object]:
    from mcp import Client
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError

    cases = load_cases()
    marker = cases["task"]["expected_marker"]
    package_version = version("mcp")
    if package_version != "2.1.1":
        raise RuntimeError(f"unexpected mcp version: {package_version}")

    server = MCPServer("NEXUSRuntimeTrial")

    @server.tool()
    def runtime_marker() -> str:
        """Return the deterministic NEXUS marker."""
        return marker

    @server.tool()
    def injected_failure() -> str:
        """Raise a deterministic, model-readable tool error."""
        raise ToolError("nexus-injected-runtime-failure")

    started = time.monotonic()
    async with Client(server, mode="2026-07-28") as client:
        result = await asyncio.wait_for(client.call_tool("runtime_marker", {}), timeout=5.0)
        protocol_version = client.protocol_version
        text = "\n".join(
            getattr(block, "text", "")
            for block in result.content
            if getattr(block, "text", None)
        )
        task_success = 1.0 if (not result.is_error and marker in text) else 0.0

        failure_result = await asyncio.wait_for(
            client.call_tool("injected_failure", {}),
            timeout=5.0,
        )
        failure_bounded = 1.0 if failure_result.is_error else 0.0

    duration_ms = round((time.monotonic() - started) * 1000, 3)
    protocol_success = protocol_version == "2026-07-28"
    ctvr = 0.0 if not may_override("T6", "T1") else 1.0

    payload = evidence_base(
        adapter="mcp-python-sdk",
        package="mcp",
        package_version=package_version,
        boundary="real-sdk-client-server-in-process/protocol-2026-07-28",
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
        "negotiated_protocol_version": protocol_version,
        "protocol_version_match": protocol_success,
        "failure_scenario": "real MCP tool raises ToolError; client receives is_error result within timeout",
        "var_status": "NOT_EXECUTED_NOT_EQUIVALENT",
        "dser_status": "NOT_EXECUTED_NOT_EQUIVALENT",
        "ctvr_scope": "NEXUS host policy only; MCP payload itself is treated as T6",
    }
    payload["limitations"] = [
        "The MCP server/client are real SDK objects but run in-process; no HTTP/DNS/OAuth boundary is exercised.",
        "MRTR, server/discover over HTTP, auth and network chaos are NOT_EXECUTED in this smoke trial.",
        "VAR/DSER are not scored because no side-effecting remote tool is used.",
        "Historical 1.x advisories are not treated as reproduced against 2.1.1.",
    ]
    if not protocol_success:
        payload["limitations"].append("The expected 2026-07-28 protocol version was not observed.")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="validation-evidence/runtime-mcp.json")
    args = parser.parse_args()
    payload = asyncio.run(run_trial())
    write_evidence(payload, args.output)
    metrics = payload["metrics"]
    required = (
        metrics["task_success_rate"] == 1.0
        and metrics["recovery_success_rate"] == 1.0
        and metrics["context_trust_violation_rate"] == 0.0
        and payload["details"]["protocol_version_match"] is True
    )
    return 0 if required else 1


if __name__ == "__main__":
    raise SystemExit(main())
