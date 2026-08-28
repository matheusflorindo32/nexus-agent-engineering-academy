---
id: governance.upstream-adoption-matrix-v3
content_id: governance.upstream-adoption-matrix-v3
version: 3.0.0
title: Upstream Adoption Matrix V3
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Upstream Adoption Matrix V3

## Evidence rule

`ADOPT` means a capability is ready to become a NEXUS baseline pattern. `ADAPT` means retain the concept but implement it under NEXUS contracts. `STUDY` means architecture is promising but runtime or maintenance evidence is insufficient. `MONITOR` means wait for an upstream change. No project receives a runtime score without real execution.

| Upstream / capability | Evidence | Decision | Reason |
|---|---|---|---|
| GitHub Spec Kit — constitution/lifecycle/converge | DOCUMENTED_UPSTREAM_CAPABILITY + prior architectural audit | ADAPT | Strong lifecycle primitives; NEXUS remains the control plane. |
| OpenSpec — incremental change/diff/approval-first explore | DOCUMENTED_UPSTREAM_CAPABILITY + prior architectural audit | ADAPT | Useful change model without requiring framework replacement. |
| Superpowers — TDD/debugging/planning/verification | EXECUTED_PROCESS_EVIDENCE within NEXUS workflow + documented upstream capability | ADOPT/ADAPT | Practices repeatedly improved NEXUS trial quality and caught protocol drift. |
| SpecD — code graph architecture | DOCUMENTED_UPSTREAM_CAPABILITY from pinned source | ADAPT | Real graph index/impact implementation, spec→file/symbol coverage and diagnostics are valuable design inputs. |
| SpecD — runtime dependency | REAL_RUNTIME_EVIDENCE of frozen install attempt | STUDY / MONITOR | Exact pinned head failed `pnpm install --frozen-lockfile`; graph runtime remained NOT_TESTED. |
| SpecD — requirement-level traceability | DOCUMENTED_UPSTREAM_CAPABILITY / explicit non-goal in implementation-tracking design | NOT_APPLICABLE as replacement | SpecD implementation tracking stops at spec→file/symbol; NEXUS requires Requirement→Spec→Task→Code→Test→Evidence. |
| SpecD — signed approval identity | DOCUMENTED_UPSTREAM_CAPABILITY from open issue #26 | REJECT as current NEXUS authority model | Current upstream approval identity lacks cryptographic proof/non-repudiation. |
| Agent OS — standards discovery/injection | DOCUMENTED_UPSTREAM_CAPABILITY | ADAPT | Strong fit for selective context injection. |
| Open GSD Core — fresh-context isolation | DOCUMENTED_UPSTREAM_CAPABILITY | STUDY/ADAPT | Useful context-rot mitigation; avoid adopting full runtime without a separate trial. |
| BMAD — role separation | DOCUMENTED_UPSTREAM_CAPABILITY | ADAPT | Planner/architect/builder/reviewer separation aligns with NEXUS independent verification. |
| Kiro — hooks/steering | DOCUMENTED_UPSTREAM_CAPABILITY | ADAPT conceptually | Event-driven checks are useful; preserve vendor independence. |
| SpecDD — colocated `.sdd` specs | DOCUMENTED_UPSTREAM_CAPABILITY | STUDY | Additional source of truth can increase drift; requires a specific trial before adoption. |

## SpecD V1 update

Prior design-fit estimate for SpecD: **86/100 (`INFERRED`)**.

Runtime comparable-subset score after this trial: **`NOT_TESTED`**.

Reason: the exact frozen source commit `14422dba5c1cc64f04205f3ebfa3d435cd790aa0` could not pass `pnpm install --frozen-lockfile` because upstream package metadata and lockfile disagree. Assigning `0/100` would mislabel reproducibility as graph correctness; assigning any positive runtime score would fabricate execution.

## Capabilities worth adapting into NEXUS Traceability Graph V2

- first-class file and symbol graph nodes;
- explicit dependency relations rather than prose-only links;
- impact traversal with bounded direction/depth;
- graph fingerprinting;
- coverage diagnostics (`indexed`, `unsupported`, `parse-failed`, `partial`);
- explicit spec→file / spec→symbol edges;
- stale-link metadata;
- machine-readable impact results;
- isolated indexing worker pattern.

## Capabilities not to import unchanged

- SpecD as an unconditional runtime dependency while source/lockfile reproducibility is unresolved;
- current unsigned approval identity model;
- any claim that spec→file/symbol coverage replaces requirement-level traceability;
- dependency detection assumptions beyond tested language/static forms;
- automatic trust in risk scores before execution-flow and parser coverage limitations are independently measured.

## Next decisions

- `ADAPT`: graph concepts into an internal NEXUS Traceability Graph V2 design trial.
- `MONITOR`: SpecD reproducible source build / published release state.
- `STUDY`: repeat the isolated runtime trial only after a new frozen upstream candidate passes lockfile consistency before graph measurement.
- `REJECT`: weakening reproducibility with an unpinned `latest` or `--no-frozen-lockfile` fallback for benchmark purposes.
