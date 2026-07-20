"""Run mandatory NEXUS quality gates and emit machine-readable evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
COMMANDS = (
    ("repository-validator", (sys.executable, "tests/validate_repository.py")),
    ("unit-tests", (sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v")),
    ("compileall", (sys.executable, "-m", "compileall", "-q", "examples", "tests")),
    ("minimal-readonly-agent", (sys.executable, "examples/minimal_readonly_agent.py", "--demo")),
    ("context-retriever", (sys.executable, "examples/context_retriever.py")),
    ("safe-tool-boundary", (sys.executable, "examples/safe_tool_boundary.py", "--self-test")),
    ("deterministic-loop", (sys.executable, "examples/deterministic_loop.py", "--self-test")),
    ("governed-memory", (sys.executable, "examples/governed_memory_store.py", "--self-test")),
    ("governed-multi-agent", (sys.executable, "examples/governed_multi_agent_orchestrator.py", "--self-test")),
    ("evaluation-harness", (sys.executable, "examples/evaluation_harness.py", "--self-test")),
    ("security-guardrails", (sys.executable, "examples/security_guardrails.py", "--self-test")),
    ("production-runtime", (sys.executable, "examples/production_runtime.py", "--self-test")),
    ("observability-pipeline", (sys.executable, "examples/observability_pipeline.py", "--self-test")),
)


def git_sha() -> str:
    configured = os.environ.get("GITHUB_SHA")
    if configured:
        return configured
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def run_gate(name: str, command: tuple[str, ...]) -> dict[str, object]:
    started = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    print(f"\n===== {name} =====")
    print(output, end="" if output.endswith("\n") or not output else "\n")
    print(f"result={result.returncode}")
    return {
        "name": name,
        "command": list(command),
        "exit_code": result.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "output": output,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("validation-evidence.json"))
    args = parser.parse_args()

    results = [run_gate(name, command) for name, command in COMMANDS]
    evidence = {
        "schema": "nexus.validation-evidence.v1",
        "commit_sha": git_sha(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "platform": platform.platform(),
            "python": sys.version,
            "github_runner_os": os.environ.get("RUNNER_OS", "local"),
        },
        "results": results,
        "failures": [item["name"] for item in results if item["exit_code"] != 0],
        "limitations": [
            "TypeScript strict is executed and evidenced by the independent CI job.",
            "External-link availability and formal ABNT conformance are outside this automated suite.",
            "Secret scanning is pattern-based and cannot prove universal secret detection.",
        ],
    }
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Evidence written to {output_path}")
    return 1 if evidence["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
