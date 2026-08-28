---
id: governance.upstream-adoption-matrix-v4
content_id: governance.upstream-adoption-matrix-v4
version: 4.0.0
title: Upstream Adoption Matrix V4 — Traceability Graph
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Upstream Adoption Matrix V4 — Traceability Graph

## Decision rule

`ADOPT`, `ADAPT`, `STUDY`, `MONITOR`, `REJECT` and `NOT_APPLICABLE` are capability-level decisions. They are not blanket endorsements of an upstream project.

| Upstream / capability | Version or pin audited | License / reuse boundary | Decision | NEXUS use | Deliberately not incorporated |
|---|---|---|---|---|---|
| NEXUS Traceability Graph V2 native core | this PR | NEXUS repository | ADOPT for Design Trial | requirement/spec/task/file/symbol/test/evidence graph, bounded impact, diagnostics, fingerprint, receipt | production source indexer not yet promoted |
| GitHub Spec Kit — lifecycle/governance | v1.0.1 (2026-08-21) | MIT; concepts adapted, no runtime dependency | ADAPT | lifecycle discipline, existing-project/spec governance concepts | no `.specify` runtime or parallel source of truth |
| OpenSpec — incremental artifacts/approval | v1.11.0 (2026-08-26) | MIT; concepts adapted | ADAPT | incremental change thinking, machine-readable status/diff, explicit approval before writes | no OpenSpec runtime/source-of-truth duplication |
| SpecD — graph/index/impact concepts | `14422dba5c1cc64f04205f3ebfa3d435cd790aa0` | MIT package/repository; concepts only, no source copied | ADAPT concepts | file/symbol nodes, dependency edges, bounded impact, fingerprint/coverage/stale-link concepts | runtime dependency; current pin remains non-reproducible with frozen lockfile |
| SpecD runtime dependency | same pin | MIT but operational reproducibility blocked | STUDY / MONITOR | recheck only after a new reproducible commit/tag exists | no `--no-frozen-lockfile`, no `latest`, no synthetic runtime score |
| Superpowers — TDD/verification/debugging discipline | installed skill baseline audited 2026-08-28 | MIT | ADOPT / ADAPT | RED→GREEN→REFACTOR, systematic review, verification-before-completion | not a competing NEXUS source of truth |
| AWS SpecShip patterns — RECON/adversarial validation | upstream patterns from Control Plane audit | concept-level only in this PR; license must be rechecked before code reuse | ADAPT | brownfield RECON and adversarial gate philosophy | no SpecShip runtime dependency |
| Kiro patterns — hooks/steering | upstream patterns from Control Plane audit | concept-level; no code copied | ADAPT | event-driven hook/steering design influence | no IDE/runtime lock-in |
| BMAD-METHOD — role separation | upstream patterns from Control Plane audit | concept-level; no code copied | ADAPT | planner/builder/verifier/security role separation | no persona framework dependency |
| Agent OS — standards discovery/injection | upstream patterns from Control Plane audit | concept-level; no code copied in Graph V2 | ADAPT | standards registry/context selection direction | no duplicate standards authority |
| Open GSD — context isolation | upstream patterns from Control Plane audit | concept-level | STUDY / ADAPT | fresh-context/isolation ideas | no GSD runtime dependency |
| SpecDD local `.sdd` format | upstream patterns from Control Plane audit | no code copied | STUDY | possible future local-spec ergonomics research | no additional spec format in V2 |

## Current provenance facts checked for this trial

- `github/spec-kit` license is MIT; v1.0.1 is the current release used by this audit baseline.
- `Fission-AI/OpenSpec` license is MIT; v1.11.0 is the current release used by this audit baseline.
- `specd-sdd/SpecD` source pin used for architectural study is `14422dba...`; the package declares MIT. Its frozen source installation remained blocked in PR #58 and `main` had not advanced at the start of this trial.
- `obra/superpowers` license is MIT.

## Promotion rules

A capability moves from `STUDY/MONITOR` to `ADAPT/ADOPT` only with a documented need, compatible licensing, bounded security review and evidence appropriate to the claim. A documentation claim never becomes runtime evidence merely because an upstream README describes a feature.

## SpecD decision after Graph V2

The isolated failure to reproduce the pinned SpecD source did **not** justify rejecting its architecture. Graph V2 therefore adapts concepts independently while rejecting runtime lock-in. The NEXUS graph has now produced deterministic control evidence; the SpecD side of any runtime comparison remains `NOT_TESTED`.

## No-framework-soup gate

Graph V2 introduces zero third-party runtime dependencies. NEXUS remains the single authority for constitution, traceability semantics, release gates, evidence classes, provenance and human approval.