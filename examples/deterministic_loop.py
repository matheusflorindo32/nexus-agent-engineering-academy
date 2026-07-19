"""Deterministic loop reference for NEXUS. Standard library only."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import hashlib
import json


class State(str, Enum):
    INITIALIZE = "initialize"
    PLAN = "plan"
    EXECUTE = "execute"
    OBSERVE = "observe"
    EVALUATE = "evaluate"
    COMPLETE = "complete"
    AWAIT_APPROVAL = "await_approval"
    STOPPED = "stopped"


@dataclass
class Budgets:
    max_steps: int = 8
    max_tool_calls: int = 5
    max_failures: int = 2
    max_no_progress: int = 2
    max_external_effects: int = 1


@dataclass
class Run:
    run_id: str
    scenario: str
    state: State = State.INITIALIZE
    step: int = 0
    tool_calls: int = 0
    failures: int = 0
    no_progress: int = 0
    external_effects: int = 0
    effects: set[str] = field(default_factory=set)
    last_fingerprint: str = ""
    reason: str | None = None
    budgets: Budgets = field(default_factory=Budgets)

    def fingerprint(self, value: object) -> str:
        return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

    def stop(self, reason: str) -> None:
        self.state = State.STOPPED
        self.reason = reason

    def checkpoint(self) -> dict[str, object]:
        data = asdict(self)
        data["state"] = self.state.value
        data["effects"] = sorted(self.effects)
        return data

    @classmethod
    def restore(cls, checkpoint: dict[str, object]) -> "Run":
        data = dict(checkpoint)
        budgets = Budgets(**dict(data.pop("budgets")))
        effects = set(data.pop("effects"))
        data["state"] = State(data["state"])
        return cls(**data, budgets=budgets, effects=effects)

    def apply_effect_once(self, key: str) -> None:
        if key in self.effects:
            return
        if self.external_effects >= self.budgets.max_external_effects:
            self.stop("budget_exhausted")
            return
        self.effects.add(key)
        self.external_effects += 1

    def tick(self) -> None:
        if self.state in {State.COMPLETE, State.STOPPED, State.AWAIT_APPROVAL}:
            return
        if self.step >= self.budgets.max_steps:
            self.stop("budget_exhausted")
            return
        self.step += 1
        self.state = State.PLAN

        if self.scenario == "operator_stop":
            self.stop("operator_stop")
            return
        if self.scenario == "schema_error":
            self.stop("non_retryable_failure")
            return
        if self.scenario == "approval_expired":
            self.stop("approval_expired")
            return

        self.state = State.EXECUTE
        self.tool_calls += 1
        if self.tool_calls > self.budgets.max_tool_calls:
            self.stop("budget_exhausted")
            return

        if self.scenario == "transient_failures":
            self.failures += 1
            if self.failures >= 3:
                self.stop("circuit_open")
            return

        if self.scenario == "crash_resume":
            self.apply_effect_once("effect-001")
            self.state = State.OBSERVE
            self.state = State.EVALUATE
            self.state = State.COMPLETE
            self.reason = "objective_complete"
            return

        progress = {"goal": self.step >= 3} if self.scenario == "success" else {"goal": False}
        fp = self.fingerprint(progress)
        if fp == self.last_fingerprint:
            self.no_progress += 1
        else:
            self.no_progress = 0
            self.last_fingerprint = fp

        self.state = State.EVALUATE
        if progress["goal"]:
            self.state = State.COMPLETE
            self.reason = "objective_complete"
        elif self.no_progress >= self.budgets.max_no_progress:
            self.stop("no_progress")

    def run(self) -> dict[str, object]:
        while self.state not in {State.COMPLETE, State.STOPPED, State.AWAIT_APPROVAL}:
            self.tick()
        return {
            "run_id": self.run_id,
            "terminal_state": self.state.value,
            "reason": self.reason,
            "steps": self.step,
            "tool_calls": self.tool_calls,
            "external_effects": self.external_effects,
        }


def self_test() -> None:
    expected = {
        "success": ("complete", "objective_complete"),
        "no_progress": ("stopped", "no_progress"),
        "schema_error": ("stopped", "non_retryable_failure"),
        "transient_failures": ("stopped", "circuit_open"),
        "approval_expired": ("stopped", "approval_expired"),
        "operator_stop": ("stopped", "operator_stop"),
    }
    for name, target in expected.items():
        result = Run(f"test-{name}", name).run()
        assert (result["terminal_state"], result["reason"]) == target, result

    budget_result = Run(
        "test-budget-exhaustion",
        "budget_exhaustion",
        budgets=Budgets(max_steps=0),
    ).run()
    assert (
        budget_result["terminal_state"],
        budget_result["reason"],
    ) == ("stopped", "budget_exhausted"), budget_result

    original = Run("test-resume", "crash_resume")
    original.apply_effect_once("effect-001")
    checkpoint = original.checkpoint()
    restored = Run.restore(checkpoint)
    result = restored.run()
    assert result["external_effects"] == 1, result
    assert checkpoint["effects"] == ["effect-001"], "restore mutated the checkpoint"
    print("deterministic_loop self-test passed: 8 scenarios; 0 duplicate effects")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", nargs="?", default="success")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print(json.dumps(Run("demo", args.scenario).run(), indent=2))


if __name__ == "__main__":
    main()
