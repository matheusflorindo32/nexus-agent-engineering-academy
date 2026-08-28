---
id: audit.nexus-traceability-graph-v2-results
content_id: audit.nexus-traceability-graph-v2-results
version: 1.0.0
title: NEXUS Traceability Graph V2 — Design Trial Results
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Traceability Graph V2 — Design Trial Results

## Evidence boundary

Este relatório registra somente `DETERMINISTIC_CONTROL_EVIDENCE` do grafo NEXUS-native sobre um corpus sintético congelado. O resultado **não é** benchmark de produção, benchmark com LLM nem comparação runtime com SpecD. SpecD permanece `NOT_TESTED` neste escopo e `MONITOR` no upstream.

## Base and isolation

- Base PR: #58
- Base SHA: `f997419541c6611293087a4a840865c7a0e100c0`
- Branch: `feat/nexus-traceability-graph-v2-design-trial`
- Runtime dependencies added: 0
- Python: 3.12 stdlib only
- Benchmark repetitions: 5
- Human merge authority: preserved

## TDD evidence

### RED 1 — trial and inherited review contracts

Head: `a8896d252353e639757f3d4c57b639b5e04da91d`

- NEXUS Quality run: `33199827781`
- repository validator: PASS
- tests executed: 90
- result: 5 failures + 8 errors
- scope: three inherited P1 review findings plus deliberately absent Graph V2 implementation artifacts
- artifact: `9697277399`
- artifact SHA-256: `5ee78d619e3b52bc5e5de835d4d691e875792e9bb5473f2e53a5067b2c93bd5b`

### RED 2 — persistent Control Plane schema

A contract test was added before `.nexus/traceability/graph-v2.schema.json`; Documentation Quality became red before the schema was created. This cycle proved the persistent schema was required rather than retrofitted after implementation.

### RED 3 — adversarial semantic graph poisoning

Head: `9c9f7c8d497ace4471dc9b99c9911d9355a01b97`

- NEXUS Quality run: `33200536433`
- tests executed: 94
- result: 1 failure + 1 error
- failure 1: a syntactically known `DEPENDS_ON` relation was accepted between incompatible `requirement → evidence` endpoints
- error 1: `.nexus/traceability/model.json` did not yet route to the Graph V2 schema
- artifact: `9697558111`
- artifact SHA-256: `b4e780f71119253ae608c165e83180c3b8e879c8a09d251108c78d9ed290b78d`

The graph was then hardened with explicit endpoint-type constraints and the Control Plane model was advanced to `nexus.traceability.v2`.

## Executed architecture

```text
requirement
    ↓ REFINED_BY
spec
    ↓ PLANNED_BY
 task ──TOUCHES_FILE──→ file ──CONTAINS_SYMBOL──→ symbol
  │                        │                          │
  └────TOUCHES_SYMBOL──────┘                          │
                                                     ↓ VERIFIED_BY
                                                    test
                                                     ↓ PRODUCES_EVIDENCE
                                                  evidence
```

`DEPENDS_ON` is restricted to `file|symbol → file|symbol`. Every edge type now has explicit source and target type constraints.

## Dedicated benchmark evidence

First fully executable Graph V2 benchmark run after the core implementation:

- workflow: NEXUS Traceability Graph V2
- run: `33200363291`
- artifact: `9697488818`
- artifact SHA-256: `d390fc9cd7b4de6f0d7986375896a61c50d993c9ed7997b0e404d7cd25e0fb4c`
- dedicated contracts: 10/10 PASS
- fixture/protocol hashes: PASS
- evidence boundary assertion: PASS

The final branch verification is expected to supersede this artifact after the reports are committed; this record is preserved as the first GREEN evidence rather than overwritten.

## Raw metrics from the frozen 18-case control corpus

| Metric | Executed value |
|---|---:|
| Precision | 1.000000 |
| Recall | 1.000000 |
| F1 | 1.000000 |
| False positives | 0 |
| False negatives | 0 |
| Orphan detection rate | 1.000000 |
| Stale-link detection rate | 1.000000 |
| Regression detection rate | 1.000000 |
| Security detection rate | 1.000000 |
| Deterministic rerun equality | 1.000000 |
| Graph fingerprint equality | 1.000000 |
| Nodes in canonical timing fixture | 7 |
| Edges in canonical timing fixture | 7 |
| Canonical graph bytes | 926 |
| Median graph build time in that CI run | 0.122239 ms |
| Median impact query time in that CI run | 0.024920 ms |
| Python tracemalloc peak allocation | 8,299 bytes |
| Runtime third-party dependencies added | 0 |

The measured timing and memory values describe only that tiny synthetic CI fixture. They are not production latency, RSS, scalability or real-repository performance claims.

## Score

`benchmark_score_0_100 = 100.0` **only inside the frozen synthetic 18-case control corpus**.

This score means that the implementation matched every frozen expected diagnostic and the executed deterministic/reproducibility controls. It must not be presented as:

- general Graph V2 quality = 100/100;
- production readiness = 100/100;
- NEXUS > SpecD;
- performance superiority;
- security proof beyond the frozen cases.

## Example impact queries

### Requirement changes

For the canonical chain, `impact(req:1, downstream)` reaches:

`spec:1 → task:1 → file:1/symbol:1 → test:1 → evidence:1`.

This identifies implementation, tests and evidence requiring review or regeneration.

### Symbol changes

`impact(symbol:1, upstream)` reaches upstream file/task/spec/requirement nodes according to the explicit graph relations. The traversal is bounded by depth 16 and cycle-safe.

### Evidence regeneration

A requirement/spec/task change can be followed downstream to evidence nodes, allowing release tooling to identify evidence that may be stale after an upstream change.

## Frozen inputs

- `protocol.json` SHA-256: `d8b035b72411014e0ed76c10a4ca4145703453f9c0be8b45f1092b1b80952720`
- `fixtures.json` SHA-256: `0896ce39650fec0c8f40cf12d37460da50c3c4adcaa6eb726a5d76fbd03348ff`

The dedicated workflow recomputes and verifies these hashes before running the benchmark.

## Inherited PR #58 findings addressed on this stacked branch

1. precision now penalizes any unexpected affected file, including files outside the explicit negative universe;
2. future SpecD rechecks preserve phase-specific setup/install/build/CLI/index/impact failure evidence;
3. the unchanged known-bad SpecD commit is now MONITOR-short-circuited rather than repeatedly rerun without a new reproducible candidate.

PR #58 itself was not modified or merged.

## Non-executed metrics

- SpecD graph runtime comparison: `NOT_TESTED`
- LLM tokens/context: `NOT_APPLICABLE`
- human maintenance hours: `NOT_TESTED`
- production RSS memory: `NOT_TESTED`
- real repository multi-language source indexing: `NOT_TESTED`

## Provisional gate

The executable design trial is eligible for `PASS` only after fresh final-head repository verification, dedicated Graph V2 evidence, security checks and review closure. Merge remains human-authority only.