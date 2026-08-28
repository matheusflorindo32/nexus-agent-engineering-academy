---
id: audit.specd-isolated-runtime-trial-v1-results
content_id: audit.specd-isolated-runtime-trial-v1-results
version: 1.0.0
title: SpecD Isolated Runtime Trial V1 — Results
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# SpecD Isolated Runtime Trial V1 — Results

## Decision summary

- Methodological execution gate: **PASS** — the protocol detected and preserved a real upstream reproducibility blocker without fabricating runtime results.
- SpecD graph runtime comparison: **BLOCKED / NOT_TESTED**.
- Global NEXUS × SpecD runtime winner: **BLOCKED**.
- Merge: **BLOCKED — explicit human authorization required**.

## Frozen inputs

| Item | Value |
|---|---|
| NEXUS base PR | #57 |
| NEXUS base SHA | `d712c03dc5a97e3e349f884d6bb79e5900341208` |
| Trial branch | `feat/specd-isolated-runtime-trial-v1` |
| SpecD repository | `specd-sdd/SpecD` |
| SpecD source commit | `14422dba5c1cc64f04205f3ebfa3d435cd790aa0` |
| License | MIT |
| Package manager declared by upstream | `pnpm@10.6.5` |
| Repetitions planned | 5 |
| Fixture language | TypeScript |

## Fixture hashes

| File | SHA-256 |
|---|---|
| `fixture/src/core.ts` | `1f2e11ab1a1935007062d97b9032fa2b8d489583f20fcd1d9c97586553356393` |
| `fixture/src/service.ts` | `b1b1311bdb7abbb504821d120470dfba8801ba24f025a28d38849fba9bce3196` |
| `fixture/src/controller.ts` | `a482e543386e585f671b4e5b725bf81fe43a2436b094bcd0219f44fd0a2d1297` |
| `fixture/src/unrelated.ts` | `5c34484584d68dd5b15dcb9f767a8ccd4423c746ff9858b52f4ad9446bea2dca` |
| `fixture/oracle.json` | `59c3a86a6f99761ce9c4b55fc03576bf7193871364264e5daaf73def3374b8db` |

The dedicated workflow verified these hashes before touching upstream code.

## TDD RED

Head `a14f176d303e4b4ceb68ba35651f9ee37152aa58` intentionally contained the specification, plan and contract tests without the executable trial artifacts.

Real GitHub Actions evidence:

- NEXUS Quality run `33196018114`: **failure**;
- Python suite: 77 tests, with **1 failure + 5 errors** caused by the intentionally absent protocol, fixture/oracle, evaluator and workflow;
- an additional repository-validator failure identified missing NEXUS frontmatter in the new plan and was corrected rather than suppressed;
- RED evidence artifact: `9695760495`;
- artifact digest: `sha256:4fc55bb89b36b8870b1730d42dcc231d0c502f6f07ddc0cd9ecfc03901e8c7b3`.

## Real upstream execution attempt

The workflow then:

1. verified the frozen fixture hashes;
2. cloned `https://github.com/specd-sdd/SpecD.git`;
3. checked out exactly `14422dba5c1cc64f04205f3ebfa3d435cd790aa0` in detached mode;
4. activated pnpm `10.6.5`;
5. executed the upstream-preserving command `pnpm install --frozen-lockfile`.

The install failed with upstream `ERR_PNPM_OUTDATED_LOCKFILE` before the CLI could be built. The reported mismatch is between `pnpm-lock.yaml` and `packages/cli/package.json`; the lockfile still contains an `@specd/code-graph` CLI dependency specifier that is not present in the pinned package manifest.

This is `REAL_RUNTIME_EVIDENCE` about upstream reproducibility/buildability. It is **not** evidence about graph accuracy or performance.

## No fallback rule

The trial explicitly refused to use `pnpm install --no-frozen-lockfile` because that would resolve dependencies differently from the committed upstream lockfile and invalidate the frozen-source reproducibility condition.

No mock CLI, synthetic graph output, npm `latest`, alternate SpecD commit or locally repaired lockfile was substituted.

## Runtime metrics

| Metric | SpecD V1 result | Evidence class |
|---|---:|---|
| source commit checkout | PASS | REAL_RUNTIME_EVIDENCE |
| frozen fixture hash verification | PASS | REAL_RUNTIME_EVIDENCE |
| frozen-lockfile install | FAIL | REAL_RUNTIME_EVIDENCE |
| CLI build | NOT_TESTED | NOT_TESTED |
| graph index | NOT_TESTED | NOT_TESTED |
| 5 impact queries | NOT_TESTED | NOT_TESTED |
| affected-file precision | NOT_TESTED | NOT_TESTED |
| affected-file recall | NOT_TESTED | NOT_TESTED |
| false-positive rate | NOT_TESTED | NOT_TESTED |
| false-negative rate | NOT_TESTED | NOT_TESTED |
| repeatability | NOT_TESTED | NOT_TESTED |
| median query duration | NOT_TESTED | NOT_TESTED |
| tokens/context | NOT_TESTED | NOT_TESTED |
| prompt injection / tool poisoning | NOT_APPLICABLE to this pre-build graph attempt | NOT_APPLICABLE |

## 0–100 benchmark boundary

**SpecD runtime comparable-subset score: `NOT_TESTED` — no valid 0–100 runtime score exists.** Assigning `0/100` would falsely treat an upstream dependency-lock reproducibility failure as measured graph quality; assigning a positive number would fabricate graph execution. Both are rejected.

The previously recorded architecture/documentation fit for SpecD (86/100) remains an `INFERRED` design-fit score, not runtime evidence, and must not be compared numerically with runtime metrics.

## Final bounded workflow evidence before documentation closeout

Head `4fac3e9ae3433f8566d1730c79695e0303a8293f`:

- SpecD Isolated Runtime Trial V1 run `33196484438`: **success** as a methodological gate that recorded the blocker;
- NEXUS Quality run `33196484297`: **success**;
- Documentation quality run `33196484287`: **success**;
- Security - Secret Scan run `33196484265`: **success**;
- Provider Runtime Trial V1 run `33196484312`: **success**;
- blocker evidence artifact: `9695953825`;
- artifact digest: `sha256:c89ccc02e66289459fd3e0df6cd6de213ef17785d3131ee280b8dd7f5fce8fb0`.

A fresh final-head verification is still required after adding this results/review documentation.
