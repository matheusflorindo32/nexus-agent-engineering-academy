"""Stdlib tests for the deterministic loop example."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).parents[1] / "examples" / "deterministic-loop" / "loop.py"
SPEC = spec_from_file_location("nexus_loop", MODULE_PATH)
assert SPEC and SPEC.loader
LOOP = module_from_spec(SPEC)
sys.modules[SPEC.name] = LOOP
SPEC.loader.exec_module(LOOP)


class LoopTests(unittest.TestCase):
    def test_success(self) -> None:
        self.assertEqual(LOOP.run("success").reason, "objective_met")

    def test_no_progress(self) -> None:
        result = LOOP.run("stalled")
        self.assertEqual((result.status, result.reason), ("stopped", "no_progress"))

    def test_zero_budget(self) -> None:
        self.assertEqual(LOOP.run("success", max_steps=0).reason, "budget_exhausted")


if __name__ == "__main__":
    unittest.main()
