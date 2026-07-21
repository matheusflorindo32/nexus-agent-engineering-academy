"""Deterministic local workflow for the NEXUS Zero Track.

No network, environment-variable, credential, shell-command, or user-file access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass

ALLOWED_FIELDS = {"operation_id", "value"}


@dataclass(frozen=True)
class Result:
    status: str
    operation_id: str
    checksum: str
    steps: tuple[str, ...]


class Workflow:
    def __init__(self) -> None:
        self._effects: dict[str, str] = {}

    def run(self, payload: dict[str, object]) -> Result:
        unknown = set(payload) - ALLOWED_FIELDS
        if unknown:
            raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")

        operation_id = payload.get("operation_id")
        value = payload.get("value")
        if not isinstance(operation_id, str) or not operation_id.strip():
            raise ValueError("operation_id must be a non-empty string")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("value must be a non-empty string")

        normalized = value.strip()
        checksum = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]
        previous = self._effects.get(operation_id)
        if previous is not None:
            if previous != checksum:
                raise ValueError("idempotency conflict")
            return Result("duplicate-safe", operation_id, checksum, ("validate", "deduplicate"))

        steps = ("validate", "prepare", "apply-effect", "verify", "record-evidence")
        self._effects[operation_id] = checksum
        return Result("completed", operation_id, checksum, steps)


def self_test() -> None:
    workflow = Workflow()
    first = workflow.run({"operation_id": "demo-001", "value": "safe synthetic value"})
    assert first.status == "completed"
    repeated = workflow.run({"operation_id": "demo-001", "value": "safe synthetic value"})
    assert repeated.status == "duplicate-safe"
    try:
        workflow.run({"operation_id": "demo-001", "value": "different"})
    except ValueError as exc:
        assert "idempotency conflict" in str(exc)
    else:
        raise AssertionError("conflicting retry must fail")
    try:
        workflow.run({"operation_id": "x", "value": "ok", "command": "echo unsafe"})
    except ValueError as exc:
        assert "unknown fields" in str(exc)
    else:
        raise AssertionError("unknown field must fail")
    print("first_workflow self-test: 4/4 passed")


def demo() -> None:
    workflow = Workflow()
    results = [
        workflow.run({"operation_id": "lesson-001", "value": "first safe workflow"}),
        workflow.run({"operation_id": "lesson-001", "value": "first safe workflow"}),
    ]
    print(json.dumps([result.__dict__ for result in results], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.demo:
        demo()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
