---
id: plan.nexus-traceability-graph-v2-design-trial
content_id: plan.nexus-traceability-graph-v2-design-trial
version: 1.0.0
title: NEXUS Traceability Graph V2 Design Trial Implementation Plan
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Traceability Graph V2 Design Trial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and benchmark a deterministic, stdlib-only NEXUS Traceability Graph V2 with bounded impact, drift/coverage diagnostics and evidence-preserving security controls.

**Architecture:** Add a focused reusable graph engine plus frozen experiment/CLI artifacts. Keep the NEXUS Control Plane authoritative. Also carry forward three validated P1 review fixes inherited from PR #58 without modifying PR #58 itself.

**Tech Stack:** Python 3.12 stdlib (`json`, `hashlib`, `argparse`, `collections`, `time`, `tracemalloc`, `unittest`); GitHub Actions.

**Spec:** `docs/architecture/NEXUS_TRACEABILITY_GRAPH_V2_DESIGN_TRIAL.md`

## Global Constraints

- Base SHA: `f997419541c6611293087a4a840865c7a0e100c0`.
- Branch: `feat/nexus-traceability-graph-v2-design-trial`.
- No merge is authorized.
- Zero new third-party runtime dependencies.
- SpecD runtime remains MONITOR/NOT_TESTED until an upstream reproducible candidate appears.
- Evidence classes remain bounded to the NEXUS taxonomy.
- Five deterministic benchmark repetitions are mandatory.
- Safety limits: 2,000 nodes, 8,000 edges, 256 fan-out, depth 16, metadata strings 2,048 chars.

---

### Task 0: Carry forward PR #58 P1 review fixes

**Files:**
- Modify: `experiments/specd_isolated_v1/trial.py`
- Modify: `.github/workflows/specd-isolated-runtime-trial.yml`
- Modify: `tests/test_specd_isolated_runtime_trial_v1.py`

**Interfaces:**
- Consumes: frozen SpecD trial evaluator/workflow from PR #58.
- Produces: correct precision semantics and phase-specific bounded failure evidence for future SpecD rechecks.

- [ ] Write regression tests proving an unexpected affected file lowers precision.
- [ ] Write static workflow tests requiring explicit setup/install/build/CLI/index/impact blocker classes and MONITOR short-circuit for the unchanged blocked SpecD pin.
- [ ] Run quality workflow and observe RED before changing evaluator/workflow.
- [ ] Implement only the three reviewed fixes.
- [ ] Verify tests GREEN without rerunning blocked SpecD runtime.

### Task 1: Freeze graph protocol and 18-case fixture corpus

**Files:**
- Create: `experiments/traceability_graph_v2/protocol.json`
- Create: `experiments/traceability_graph_v2/fixtures.json`
- Create: `experiments/traceability_graph_v2/fixture-manifest.json`
- Test: `tests/test_traceability_graph_v2.py`

**Interfaces:**
- Produces: versioned graph/benchmark contract and frozen SHA-256 manifest.

- [ ] Write tests requiring protocol version, evidence taxonomy, 5 repetitions, node/edge/safety bounds and exactly 18 required scenario classes.
- [ ] Observe RED while the three artifacts are absent.
- [ ] Create the minimal protocol/fixtures/manifest satisfying tests.
- [ ] Verify GREEN.

### Task 2: Implement deterministic graph core

**Files:**
- Create: `examples/traceability_graph_v2.py`
- Test: `tests/test_traceability_graph_v2.py`

**Interfaces:**
- Produces: `TraceabilityGraph.from_document(document)`, `audit()`, `impact(node_id, direction, depth)`, `fingerprint()`, `to_document()`.

- [ ] Write tests for canonical graph build, node/edge validation, duplicate-edge rejection, safe paths, missing targets, unknown types, fan-out limits, cycle diagnostics, fingerprint determinism and bidirectional impact.
- [ ] Observe RED because module/API does not exist.
- [ ] Implement minimal stdlib graph core.
- [ ] Verify GREEN.
- [ ] Refactor canonicalization/traversal helpers while preserving tests.

### Task 3: Implement coverage, orphan, stale-link and drift diagnostics

**Files:**
- Modify: `examples/traceability_graph_v2.py`
- Test: `tests/test_traceability_graph_v2.py`

**Interfaces:**
- `audit()` returns stable machine-readable diagnostics with bounded codes.

- [ ] Write failing tests for orphan requirement/spec/task/implementation/test/evidence, stale file/symbol, spec/implementation drift and malformed/untrusted metadata.
- [ ] Observe RED.
- [ ] Implement diagnostics and metadata injection flagging without executing metadata.
- [ ] Verify GREEN and deterministic diagnostic ordering.

### Task 4: Build CLI and Execution Receipts

**Files:**
- Create: `experiments/traceability_graph_v2/cli.py`
- Test: `tests/test_traceability_graph_v2.py`

**Interfaces:**
- Commands: `build`, `impact`, `audit`; JSON and text output; optional receipt path.

- [ ] Write subprocess tests for build/impact/audit and bounded invalid input.
- [ ] Observe RED.
- [ ] Implement CLI using graph core.
- [ ] Verify GREEN.

### Task 5: Benchmark 18 frozen cases

**Files:**
- Create: `experiments/traceability_graph_v2/benchmark.py`
- Create: `.github/workflows/traceability-graph-v2.yml`
- Test: `tests/test_traceability_graph_v2.py`

**Interfaces:**
- Produces `result.json`, `execution-receipt.json`, graph sample outputs and raw repetition metrics.

- [ ] Write tests requiring precision/recall/F1, FP/FN, detection rates, timings, tracemalloc peak, node/edge/byte counts, fingerprint equality and 5 repetitions.
- [ ] Observe RED.
- [ ] Implement benchmark with frozen score weights and no SpecD runtime comparison.
- [ ] Add dedicated workflow and evidence artifact upload.
- [ ] Verify GREEN in GitHub Actions.

### Task 6: Reviews, provenance and adoption matrix V4

**Files:**
- Create: `docs/audits/NEXUS_TRACEABILITY_GRAPH_V2_RESULTS.md`
- Create: `docs/audits/NEXUS_TRACEABILITY_GRAPH_V2_REVIEW.md`
- Create: `docs/governance/UPSTREAM_ADOPTION_MATRIX_V4.md`

**Interfaces:**
- Produces bounded conclusions, provenance and next gate.

- [ ] Record raw benchmark metrics and evidence class.
- [ ] Perform architecture, security, adversarial, traceability and reproducibility reviews against executable checks.
- [ ] Record Spec Kit v1.0.1, OpenSpec v1.11.0 and SpecD pin/provenance; distinguish concepts from code reuse.
- [ ] Update decisions without claiming SpecD runtime comparison.
- [ ] Re-run full repository verification and dedicated graph workflow.
- [ ] Open stacked PR over #58 and keep merge blocked for human authorization.
