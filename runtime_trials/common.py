"""Shared evidence helpers for Provider Runtime Trial V1."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "benchmarks" / "provider_runtime_trial_v1_cases.json"


def load_cases() -> dict[str, Any]:
    return json.loads(CASES.read_text(encoding="utf-8"))


def evidence_base(adapter: str, package: str, package_version: str, boundary: str) -> dict[str, Any]:
    return {
        "schema": "nexus.provider-runtime-trial.evidence.v1",
        "adapter": adapter,
        "package": package,
        "package_version": package_version,
        "test_boundary": boundary,
        "commit_sha": os.environ.get("NEXUS_HEAD_SHA") or os.environ.get(
            "GITHUB_SHA", "local-unverified"
        ),
        "workflow_sha": os.environ.get("GITHUB_SHA", "local-unverified"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "runner_os": os.environ.get("RUNNER_OS", "local"),
        },
        "metrics": {
            "task_success_rate": None,
            "verified_action_rate": None,
            "recovery_success_rate": None,
            "duplicate_side_effect_rate": None,
            "context_trust_violation_rate": None,
            "runtime_duration_ms": None,
            "provider_latency_ms": None,
            "tokens": None,
            "estimated_cost": None,
        },
        "claims": {
            "real_sdk_runtime": True,
            "real_external_provider": False,
            "real_model": False,
            "provider_performance_comparison_allowed": False,
        },
        "limitations": [],
    }


def write_evidence(payload: dict[str, Any], output: str) -> None:
    path = Path(output)
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
