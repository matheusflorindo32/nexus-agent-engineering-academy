---
id: plan.specd-isolated-runtime-trial-v1
content_id: plan.specd-isolated-runtime-trial-v1
version: 1.0.0
title: SpecD Isolated Runtime Trial V1 Implementation Plan
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# SpecD Isolated Runtime Trial V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute the real SpecD code graph from pinned upstream source against a frozen TypeScript fixture and compare only the semantically equivalent impact-analysis subset with NEXUS.

**Architecture:** Keep SpecD outside NEXUS runtime. GitHub Actions clones `specd-sdd/SpecD` at the frozen commit, installs with its own pnpm lockfile, builds the CLI, creates an isolated temporary git repository from committed fixtures, indexes it through `specd graph index --path`, runs impact queries, and feeds raw JSON to a NEXUS-owned evaluator. Metrics lacking equivalent runtime semantics are never scored.

**Tech Stack:** Python 3.12 stdlib for orchestration/scoring; Node.js 22; pnpm 10.6.5; upstream SpecD TypeScript CLI; GitHub Actions.

**Spec:** `docs/architecture/SPECD_ISOLATED_RUNTIME_TRIAL_V1_SPEC.md`

## Global Constraints

- Base SHA is `d712c03dc5a97e3e349f884d6bb79e5900341208`.
- Upstream SpecD commit is `14422dba5c1cc64f04205f3ebfa3d435cd790aa0`.
- No PR merge is authorized.
- Five repetitions are mandatory for the comparable subset.
- Third-party runtime claims require actual upstream execution.
- Non-equivalent metrics must be `NOT_TESTED` or `NOT_APPLICABLE`.

---

### Task 1: Freeze contracts and observe RED

**Files:**
- Create: `tests/test_specd_isolated_runtime_trial_v1.py`
- Create later: `experiments/specd_isolated_v1/protocol.json`
- Create later: `experiments/specd_isolated_v1/fixture_manifest.json`
- Create later: `experiments/specd_isolated_v1/trial.py`
- Create later: `.github/workflows/specd-isolated-runtime-trial.yml`

**Interfaces:**
- Consumes: project root and committed trial paths.
- Produces: structural tests proving upstream pin, five repetitions, evidence classes, fixture/oracle existence, and no fabricated global runtime score.

- [x] **Step 1: Write failing structural tests** requiring the frozen protocol, fixture manifest, evaluator and workflow before those implementation files exist.
- [x] **Step 2: Open a draft stacked PR on `feat/traceability-standards-runtime-trial-v1` and observe GitHub Actions RED caused by the missing implementation files.**
- [x] **Step 3: Preserve run IDs/artifact evidence in the final review document; do not rewrite history.**

### Task 2: Build the frozen fixture and NEXUS oracle

**Files:**
- Create: `experiments/specd_isolated_v1/protocol.json`
- Create: `experiments/specd_isolated_v1/fixture_manifest.json`
- Create: `experiments/specd_isolated_v1/fixture/src/core.ts`
- Create: `experiments/specd_isolated_v1/fixture/src/service.ts`
- Create: `experiments/specd_isolated_v1/fixture/src/controller.ts`
- Create: `experiments/specd_isolated_v1/fixture/src/unrelated.ts`
- Create: `experiments/specd_isolated_v1/fixture/oracle.json`

**Interfaces:**
- Consumes: upstream graph semantics documented by SpecD `graph index` and `graph impact`.
- Produces: deterministic import/call chain and an oracle for expected affected files from `core.ts`.

- [ ] **Step 1: Commit a minimal TypeScript dependency chain** where `controller.ts → service.ts → core.ts` and `unrelated.ts` has no dependency path to the target.
- [ ] **Step 2: Freeze expected affected files and repetitions in JSON.**
- [ ] **Step 3: Record SHA-256 values in `fixture_manifest.json`, calculated over committed UTF-8 bytes.**

### Task 3: Execute real SpecD from pinned source

**Files:**
- Create: `.github/workflows/specd-isolated-runtime-trial.yml`
- Create: `experiments/specd_isolated_v1/trial.py`

**Interfaces:**
- Consumes: raw SpecD `graph index` and `graph impact --format json` outputs written by the workflow.
- Produces: `result.json`, `execution-receipt.json`, raw upstream outputs and a comparable-subset score.

- [ ] **Step 1: Clone `https://github.com/specd-sdd/SpecD.git` and checkout exactly `14422dba5c1cc64f04205f3ebfa3d435cd790aa0`.**
- [ ] **Step 2: Enable corepack, activate pnpm `10.6.5`, run `pnpm install --frozen-lockfile`, and build `@specd/cli`.**
- [ ] **Step 3: Copy fixture files to `$RUNNER_TEMP/specd-fixture`, initialize a git repository, and run the pinned CLI `graph index --path ... --force --format json`.**
- [ ] **Step 4: Run `graph impact --file src/core.ts --path ... --direction dependents --depth 3 --format json` five times, preserving each raw output.**
- [ ] **Step 5: Run `trial.py` to compute precision, recall, false-positive rate, false-negative rate, repeatability and duration from actual raw outputs.**
- [ ] **Step 6: If upstream build/index/query fails, exit non-zero and classify runtime comparison as BLOCKED; never synthesize values.**

### Task 4: Review and close the gate

**Files:**
- Create: `docs/audits/SPECD_ISOLATED_RUNTIME_TRIAL_V1_RESULTS.md`
- Create: `docs/audits/SPECD_ISOLATED_RUNTIME_TRIAL_V1_REVIEW.md`
- Create: `docs/governance/UPSTREAM_ADOPTION_MATRIX_V3.md`

**Interfaces:**
- Consumes: final GitHub Actions evidence and upstream audit facts.
- Produces: bounded decision `ADOPT/ADAPT/STUDY/MONITOR/REJECT/NOT_APPLICABLE` and next gate recommendation.

- [ ] **Step 1: Record raw metrics and separate `REAL_RUNTIME_EVIDENCE` from deterministic NEXUS control evidence.**
- [ ] **Step 2: Adversarially inspect false positives/negatives, fixture bias, upstream open issues, unsigned commit, unprotected branch and dependency/build exposure.**
- [ ] **Step 3: Run the complete repository CI and dedicated SpecD trial on the final head.**
- [ ] **Step 4: Mark the PR Ready for Review only after all final workflows required by the spec are green.**
- [ ] **Step 5: Keep merge blocked pending explicit human authorization.**

## Self-review

- Spec coverage: executable SpecD, exact pinning, five repetitions, comparable-only scoring, provenance, TDD, security/adversarial review and final PR gate are all mapped to tasks.
- Placeholder scan: no deferred implementation placeholder is used as an execution instruction.
- Type/contract consistency: workflow raw JSON → `trial.py` → result/receipt → audit documents is the only evidence path.
