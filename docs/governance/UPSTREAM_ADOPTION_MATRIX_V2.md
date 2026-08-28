---
id: governance.upstream-adoption-matrix-v2
content_id: governance.upstream-adoption-matrix-v2
version: 2.0.0
title: Upstream Adoption Matrix V2
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Upstream Adoption Matrix V2

| Capability | Source | Decision | Evidence | Local action |
|---|---|---|---|---|
| Canonical governance / constitution | Spec Kit + NEXUS | ADOPT | DOCUMENTED_UPSTREAM_CAPABILITY + DETERMINISTIC_CONTROL_EVIDENCE | Keep `.nexus/constitution.md` canonical |
| Spec lifecycle / convergence | GitHub Spec Kit v1.0.1 | ADAPT | DOCUMENTED_UPSTREAM_CAPABILITY | Map lifecycle into NEXUS without installing the full framework |
| Incremental spec diffs / batch status | OpenSpec v1.11.0 | ADAPT | DOCUMENTED_UPSTREAM_CAPABILITY | Prototype diff/status semantics in a future isolated trial |
| Explore write approval | OpenSpec v1.11.0 | ADOPT | DOCUMENTED_UPSTREAM_CAPABILITY | Preserve explicit human authorization before agent writes where risk warrants |
| TDD / systematic debugging / verification | Superpowers | ADOPT | DOCUMENTED_UPSTREAM_CAPABILITY + local process evidence | Keep as engineering discipline |
| Compiled context / spec-code graph | SpecD | STUDY | DOCUMENTED_UPSTREAM_CAPABILITY | Highest-priority external runtime candidate; do not claim parity yet |
| Deterministic impact analysis | SpecD | STUDY/ADAPT | DOCUMENTED_UPSTREAM_CAPABILITY | Design comparable fixture adapter before adoption |
| Standards discovery/injection | Agent OS 3.0 | ADAPT | DOCUMENTED_UPSTREAM_CAPABILITY | Keep NEXUS standards registry and improve contextual selection |
| Fresh-context orchestration | Open GSD Core | STUDY/ADAPT | DOCUMENTED_UPSTREAM_CAPABILITY | Evaluate only for long multi-step agent tasks |
| Colocated local specifications | SpecDD | STUDY | DOCUMENTED_UPSTREAM_CAPABILITY | Consider for large monorepos; avoid new spec format in V1 |
| Framework soup | Multiple | REJECT | DETERMINISTIC_CONTROL_EVIDENCE + complexity analysis | One NEXUS source of truth; integrate ideas selectively |
| Third-party runtime superiority claims | All upstreams | NOT_APPLICABLE | NOT_TESTED | Forbidden until actual equivalent runtime execution |

## Changes from V1

1. OpenSpec rises in relevance because v1.11.0 adds spec diffs, batch status, stronger validation and explicit approval before Explore writes.
2. SpecD remains the highest-priority runtime comparison for traceability because its documented code graph directly targets the largest remaining NEXUS gap.
3. The deterministic trial supports retaining the NEXUS control plane: governance coverage improved under the frozen fixtures, although maintenance complexity increased.
4. No upstream project is promoted on the basis of popularity or documentary fit alone.

## Next external-runtime order

1. SpecD isolated traceability/code-graph trial.
2. OpenSpec isolated spec-diff/change-management trial.
3. Agent OS standards injection trial.
4. Spec Kit harness trial only if the first three expose a gap that cannot be reproduced more minimally.

Every external trial must preserve the V1 evidence taxonomy and frozen semantic cases.
