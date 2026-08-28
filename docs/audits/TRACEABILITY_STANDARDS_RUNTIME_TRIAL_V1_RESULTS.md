---
id: audits.traceability-standards-runtime-trial-v1-results
content_id: audits.traceability-standards-runtime-trial-v1-results
version: 1.0.0
title: Traceability & Standards Runtime Trial V1 — Results
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Traceability & Standards Runtime Trial V1 — Results

## Evidence boundary

The only executable comparison in V1 is `baseline_ungoverned` versus `nexus_control_plane_v1` using the identical 11-case fixture set. Evidence class: `DETERMINISTIC_CONTROL_EVIDENCE`.

Spec Kit, OpenSpec, SpecD, Agent OS, Superpowers, Open GSD Core and SpecDD are recorded as `DOCUMENTED_UPSTREAM_CAPABILITY`; their runtime evidence in this trial is `NOT_TESTED`.

## RED evidence

Commit `05e001b10371a06a5f00dd20efef169b20ee7ffc`:

- NEXUS Quality run `33193009546`: failure;
- 70 tests executed;
- new trial tests: 1 failure + 6 errors because `fixtures.json`, `upstream_capabilities.json` and `trial.py` did not yet exist;
- repository validator additionally found an unsupported `status: experiment`, later corrected to `status: review`;
- validation artifact: `9694541073`;
- artifact digest: `sha256:a021afab03ddcf7495a51aa383c8bfe5c6051ca3ca1b15b0500b57b733fe590d`.

## GREEN evidence

Commit `136e89fdb834017e21db583c745968874c2ef993`:

- NEXUS Quality run `33193171836`: success;
- Documentation quality run `33193171728`: success;
- Security - Secret Scan run `33193171786`: success;
- Provider Runtime Trial inherited run `33193171720`: executed separately;
- identical fixtures applied to both local conditions.

Dedicated workflow at commit `afb9b669e0f6a2ef77c9e1db8e499f07ffa974bf`:

- workflow: `Traceability Standards Runtime Trial V1`;
- run: `33193233042`;
- conclusion: success;
- artifact: `9694631257`;
- artifact digest: `sha256:7727642ce0c31f807e971bb15e2721c9e2627416e26a56f063f76faf6eaff2a8`.

## Deterministic metrics

| Metric | Baseline | NEXUS V1 | Direction |
|---|---:|---:|---|
| Traceability coverage | 0.8182 | 1.0000 | higher better |
| Orphan requirement rate | 0.0909 | 0.0000 | lower better |
| Orphan implementation rate | 0.0909 | 0.0000 | lower better |
| Spec drift detection | 0.5000 | 1.0000 | higher better |
| Change-impact detection | 0.0000 | 1.0000 | higher better |
| Standards selection precision | 0.9091 | 1.0000 | higher better |
| Provenance completeness | 0.9091 | 1.0000 | higher better |
| Receipt completeness | 0.0000 | 1.0000 | higher better |
| Task success | 0.1818 | 1.0000 | higher better |
| Correctness | 0.1818 | 1.0000 | higher better |
| Regression detection | 1.0000 | 1.0000 | higher better |
| Hostile input rejection | 0.0000 | 1.0000 | higher better |
| Duplicate side-effect rate | 1.0000 | 0.0000 | lower better |
| Context units proxy | 11 | 7 | lower better |
| Maintenance complexity proxy | 1 | 9 | lower better |

The maintenance proxy deliberately penalizes NEXUS for the extra governance machinery. This prevents the benchmark from treating controls as free.

## Composite control score 0–100

A transparent equal-weight transformation is used only for the two executed deterministic conditions. Positive metrics remain as-is; orphan and duplicate rates are inverted; context is normalized against 11 units; maintenance proxy is inverted against a 10-unit ceiling.

- `baseline_ungoverned`: **48.1 / 100**
- `nexus_control_plane_v1`: **89.8 / 100**

Classification: `DETERMINISTIC_CONTROL_EVIDENCE`. This score is not a provider, model or external-framework benchmark.

## Upstream documentary-fit score 0–100

These are architecture-fit judgements derived from verified upstream documentation and are classified `INFERRED`, not runtime evidence.

| Project | Verified state | Fit score | Runtime in V1 | Decision |
|---|---|---:|---|---|
| GitHub Spec Kit | v1.0.1, 2026-08-21 | 95 | NOT_TESTED | ADAPT |
| OpenSpec | v1.11.0, 2026-08-26 | 92 | NOT_TESTED | ADAPT |
| Superpowers | v6.1.1 observed | 89 | NOT_TESTED | ADOPT/ADAPT |
| SpecD | active main observed | 86 | NOT_TESTED | STUDY/ADAPT |
| Open GSD Core | active main observed | 81 | NOT_TESTED | STUDY/ADAPT |
| Agent OS | 3.0 | 79 | NOT_TESTED | ADAPT |
| SpecDD | active main observed | 70 | NOT_TESTED | STUDY |

The fit score considers traceability relevance, specification lifecycle, verification discipline, context/standards handling, portability, maturity and integration cost. It must not be interpreted as measured product performance.

## Fresh upstream findings

- Spec Kit latest verified release is `v1.0.1` and includes existing-project adoption guidance plus fixes around workflows, manifests and presets.
- OpenSpec latest verified release is `v1.11.0`; `show --diff`, batch status, stricter validation and explicit approval before Explore writes materially improve its relevance to NEXUS.
- SpecD documents compiled context, deterministic validation and spec/code graph impact analysis; actual runtime remains untested here.
- Agent OS 3.0 explicitly refocuses on standards establishment/injection.
- Superpowers remains strongest as a development-discipline layer rather than the canonical spec store.

## Measurements not made

- actual LLM tokens: `NOT_TESTED`;
- wall-clock human engineering effort: `NOT_TESTED`;
- real third-party framework latency: `NOT_TESTED`;
- external framework correctness on the fixture set: `NOT_TESTED`;
- real code-graph quality versus SpecD: `NOT_TESTED`;
- monetary maintenance cost: `NOT_TESTED`.

## Gate

`PASS` for the deterministic-control experiment and claim boundaries.

`GO` for a later isolated external-runtime trial only if dependencies are pinned, licenses rechecked, execution environments isolated and the same fixtures are adapted without changing semantics.
