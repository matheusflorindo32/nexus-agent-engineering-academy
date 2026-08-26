"""Contract tests for Provider Adapters V3."""
from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
if str(EXAMPLES) not in sys.path:
    sys.path.insert(0, str(EXAMPLES))

import provider_adapter_contracts as adapters


class ProviderAdapterContractTests(unittest.TestCase):
    def test_versions_are_pinned_to_verified_baseline(self) -> None:
        versions = {spec.adapter_id: spec.version for spec in adapters.SPECS}
        self.assertEqual(versions["openai-agents-sdk"], "0.22.0")
        self.assertEqual(versions["google-adk-python"], "2.7.1")
        self.assertEqual(versions["mcp-2026-07-28"], "2026-07-28")

    def test_same_contract_is_applied_to_all_adapters(self) -> None:
        results = [adapters.run_contract(spec) for spec in adapters.SPECS]
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertEqual(result.verified_action_rate, 1.0)
            self.assertEqual(result.recovery_success_rate, 1.0)
            self.assertEqual(result.duplicate_side_effect_rate, 0.0)
            self.assertEqual(result.context_trust_violation_rate, 0.0)
            self.assertEqual(result.claims_scope, "nexus-contract-layer-only")

    def test_benchmark_refuses_provider_performance_claims(self) -> None:
        payload = adapters.benchmark()
        self.assertIn("not real provider performance", payload["scope"])
        self.assertTrue(payload["limitations"])
        self.assertNotIn("latency", payload["results"][0])
        self.assertNotIn("tokens", payload["results"][0])
        self.assertNotIn("cost", payload["results"][0])

    def test_mcp_does_not_claim_native_hitl_or_state(self) -> None:
        mcp = next(spec for spec in adapters.SPECS if spec.adapter_id.startswith("mcp"))
        self.assertFalse(mcp.hitl)
        self.assertFalse(mcp.state)
        self.assertFalse(mcp.tracing)


if __name__ == "__main__":
    unittest.main()
