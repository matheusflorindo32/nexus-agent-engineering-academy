---
id: architecture.specd-isolated-runtime-trial-v1
content_id: architecture.specd-isolated-runtime-trial-v1
version: 1.0.0
title: SpecD Isolated Runtime Trial V1
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# SpecD Isolated Runtime Trial V1

## Goal

Execute the real upstream SpecD code graph in an isolated, source-pinned environment and compare only the capabilities that can be made semantically equivalent to NEXUS Traceability & Standards Runtime Trial V1. Any non-equivalent metric remains `NOT_TESTED` or `NOT_APPLICABLE`; no global superiority claim is allowed.

## Base

- Repository: `matheusflorindo32/nexus-agent-engineering-academy`
- Base PR: #57
- Base SHA: `d712c03dc5a97e3e349f884d6bb79e5900341208`
- Branch: `feat/specd-isolated-runtime-trial-v1`
- No merge is authorized.

## Upstream pin

- Repository: `specd-sdd/SpecD`
- Commit: `14422dba5c1cc64f04205f3ebfa3d435cd790aa0`
- License: MIT
- Root package manager: `pnpm@10.6.5`
- Runtime under test: SpecD CLI built from the pinned source commit, not an inferred npm-latest alias.

## Evidence taxonomy

Every claim MUST be classified as one of:

- `REAL_RUNTIME_EVIDENCE`
- `DETERMINISTIC_CONTROL_EVIDENCE`
- `DOCUMENTED_UPSTREAM_CAPABILITY`
- `INFERRED`
- `NOT_TESTED`
- `NOT_APPLICABLE`

## Comparable runtime subset

The V1 executable comparison is intentionally restricted to code-graph semantics that both systems can represent without inventing equivalence:

1. deterministic TypeScript fixture discovery;
2. file/symbol dependency graph indexing;
3. downstream/upstream change-impact detection;
4. affected-file precision and recall against a frozen oracle;
5. false-positive and false-negative rates;
6. deterministic repeatability across five runs;
7. duplicate-effect absence for the read-only graph trial;
8. runtime duration when directly measured by the workflow.

## Non-equivalent metrics

The following MUST NOT receive a comparative runtime score unless the executed SpecD condition exposes equivalent semantics under this frozen protocol:

- requirement → spec → task → code → test → evidence completeness;
- orphan requirements/tasks;
- Execution Receipt semantics native to SpecD;
- standards registry selection;
- token/context consumption;
- human engineering effort;
- prompt-injection/tool-poisoning resistance of an LLM agent;
- approval identity/non-repudiation;
- full lifecycle drift detection beyond the graph fixture.

## Upstream risk facts to preserve

The audit must record, without converting upstream issues into NEXUS vulnerabilities:

- repository has no GitHub release at audit time;
- pinned main commit is unsigned and branch protection is disabled upstream;
- open issue #52 documents incomplete dependency detection across TypeScript/Python/Go;
- open issue #58 documents unstable/incomplete member identities for implementation links;
- open issue #26 documents unsigned/self-declared approval identity;
- upstream README marks MCP as in progress.

## TDD gate

1. protocol/spec and tests are committed before the executable harness/workflow;
2. RED is observed on GitHub Actions for missing trial implementation;
3. GREEN is accepted only after the pinned SpecD source is cloned/built and its CLI is actually invoked;
4. a failed upstream build or incompatible CLI produces `BLOCKED`, never a synthetic score.

## Acceptance criteria

The trial gate can be `PASS` only if:

1. PR #57 remains unchanged and unmerged;
2. SpecD source commit is pinned exactly;
3. fixture and oracle are versioned and hashed;
4. the workflow clones the pinned upstream commit and uses its lockfile;
5. five equivalent runs are executed for the comparable subset;
6. raw SpecD outputs are preserved as artifacts;
7. NEXUS and SpecD scores are computed only on the comparable subset;
8. all non-equivalent metrics are explicitly bounded;
9. NEXUS Quality, docs, secret scan, inherited provider/runtime trial and this dedicated trial are green at final head;
10. adversarial/security review records residual risks.

## Non-goals

- installing SpecD into the NEXUS runtime;
- replacing `.nexus` with SpecD;
- benchmarking models/providers;
- claiming framework-wide superiority;
- merging any PR.
