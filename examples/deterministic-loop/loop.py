"""Minimal deterministic agent loop used for teaching and tests."""

from __future__ import annotations

from dataclasses import dataclass
import sys


@dataclass(frozen=True)
class Result:
    status: str
    reason: str
    steps: int


def run(scenario: str, max_steps: int = 5, no_progress_limit: int = 2) -> Result:
    if max_steps <= 0:
        return Result("stopped", "budget_exhausted", 0)

    previous = None
    stagnant = 0
    for step in range(1, max_steps + 1):
        observation = "done" if scenario == "success" and step == 2 else "unchanged"
        if observation == "done":
            return Result("complete", "objective_met", step)
        stagnant = stagnant + 1 if observation == previous else 0
        if stagnant >= no_progress_limit:
            return Result("stopped", "no_progress", step)
        previous = observation
    return Result("stopped", "budget_exhausted", max_steps)


if __name__ == "__main__":
    selected = sys.argv[1] if len(sys.argv) > 1 else "success"
    print(run(selected))

