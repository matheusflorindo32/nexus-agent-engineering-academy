---
id: audit.specd-isolated-runtime-trial-v1-review
content_id: audit.specd-isolated-runtime-trial-v1-review
version: 1.0.0
title: SpecD Isolated Runtime Trial V1 — Adversarial and Security Review
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# SpecD Isolated Runtime Trial V1 — Adversarial and Security Review

## Review stance

This review attempts to disprove the claim that SpecD can currently be compared fairly with the NEXUS Control Plane under a reproducible source-pinned runtime protocol. It does not treat an upstream failure as a negative graph-quality score.

## Upstream audit findings

### Repository and release posture

- Official repository audited: `specd-sdd/SpecD`.
- License at the pinned source: MIT.
- GitHub Releases endpoint contained no published release at audit time.
- Root workspace declares `pnpm@10.6.5`.
- CLI package declares version `0.2.0` and MIT, while current `main` is substantially ahead of the public package history.
- Pinned source commit: `14422dba5c1cc64f04205f3ebfa3d435cd790aa0`, commit message `fix(all): repair code graph coverage indexing`.
- The audited commit is unsigned and the upstream `main` branch was observed without branch protection.
- No repository-root `SECURITY.md` was found at the pinned commit.

### Architecture verified from source

The pinned CLI contains real operator surfaces for:

- `graph index --path/--config` with isolated indexing, coverage diagnostics, graph fingerprint, workspaces and timing;
- `graph impact` over file, symbol, spec and public export targets;
- impact direction/depth selection;
- affected files/symbols and risk output;
- spec-side `implementation` links persisted in `spec-lock.json`;
- `COVERS_FILE` / `COVERS_SYMBOL` graph relations for spec→implementation traceability.

The implementation-file-tracking design explicitly states that requirement-level traceability is a non-goal of that layer: its scope stops at spec→file and spec→symbol. Therefore this trial must not equate SpecD implementation links with NEXUS's complete Requirement→Spec→Task→Code→Test→Evidence contract.

### Open upstream risk/debt surfaces

The audit observed open issues relevant to this trial:

- #52 documents incomplete dependency detection across TypeScript, Python and Go, including dynamic imports, member calls and project-layout resolution gaps;
- #58 documents member-identity limitations that can create stale or ambiguous symbol implementation links;
- #26 documents that approval identities are not cryptographically proven and can be self-declared through git identity;
- #39 tracks missing execution-flow/process modeling for richer functional blast-radius analysis;
- #9 proposes semantic workflow compliance gates that are not part of the proven runtime in this trial.

The changelog contains a 0.2.0 entry claiming work on multi-language call resolution, while #52 remains open in the current repository. This is treated as a signal to trust current executable evidence/open debt over historical release prose when they conflict.

## Reproducibility finding — critical

The exact pinned source was cloned successfully and the commit hash was verified. The frozen fixture was also hash-verified. The next required command was:

`pnpm install --frozen-lockfile`

It failed with `ERR_PNPM_OUTDATED_LOCKFILE` because the committed lockfile and `packages/cli/package.json` do not agree. The diagnostic specifically shows `@specd/code-graph` present in the lockfile's CLI specifier set but absent from the pinned package manifest specifier set.

### Why no fallback was permitted

Using `pnpm install --no-frozen-lockfile` would:

1. alter dependency resolution from the committed upstream state;
2. make the run dependent on registry state at execution time;
3. weaken provenance and exact reproducibility;
4. violate the pre-registered protocol.

Therefore the correct trial outcome is `BLOCKED`, not a repaired unofficial SpecD build.

## Security review

### Supply chain

**Risk: HIGH for this trial's reproducibility goal.** The source/lockfile mismatch prevents an exact lockfile build. This is not evidence of malicious behavior, but it blocks deterministic dependency provenance for the chosen upstream head.

### Commit authenticity

**Risk: MEDIUM.** The pinned commit is unsigned. Commit identity therefore has no cryptographic verification through GitHub's commit verification field.

### Branch governance

**Risk: MEDIUM.** Upstream `main` was observed without branch protection. This is a governance risk signal, not a vulnerability in SpecD code.

### Security policy discoverability

**Risk: MEDIUM/LOW.** No root `SECURITY.md` was found. This reduces clarity for vulnerability disclosure but does not prove absence of a private or external security process.

### Parser / graph attack surface

**NOT_TESTED.** The CLI could not be built under the frozen protocol, so malformed AST/parser inputs, graph-store robustness, path traversal, resource exhaustion and hostile source-file cases were not executed.

### Prompt injection / tool poisoning

**NOT_APPLICABLE to the blocked graph-runtime attempt.** No LLM agent or MCP tool execution occurred.

## Adversarial conclusions

1. **Do not score SpecD graph accuracy as zero.** Build reproducibility failure is not a false-negative graph result.
2. **Do not score SpecD graph accuracy positively.** No graph query executed.
3. **Do not promote SpecD from STUDY/ADAPT to ADOPT as a runtime dependency yet.** The exact source head did not satisfy the frozen-lockfile gate.
4. **Do preserve/adapt the architectural concepts.** Source review confirms valuable code-graph primitives, spec→file/symbol coverage, impact traversal, graph fingerprints and coverage diagnostics.
5. **Do not copy its approval model into NEXUS.** The upstream open issue on signed approvals reinforces NEXUS's stronger human-authority/evidence requirements.
6. **Do not claim NEXUS runtime superiority.** The NEXUS side still lacks an equivalent real code-graph runtime, so a fair runtime winner remains unknowable.

## Recommended next gate

`SpecD Reproducibility Recheck V1` should be **MONITOR**, not immediately implemented by weakening the pin. Re-run only when one of these conditions is true:

- upstream fixes `pnpm-lock.yaml` for the audited head or publishes a reproducibly buildable release/tag;
- a new upstream commit can be independently frozen before the next trial with an internally consistent lockfile;
- an upstream maintainer documents an official reproducible source-build procedure that preserves dependency provenance.

Meanwhile, the next NEXUS engineering gate can proceed independently as `NEXUS Traceability Graph V2 — Design Trial`, adapting graph concepts without importing SpecD as a runtime dependency.

## Gate

- methodology: **PASS**;
- SpecD source-pinned runtime: **BLOCKED**;
- SpecD graph metrics: **NOT_TESTED**;
- global NEXUS × SpecD runtime comparison: **BLOCKED**;
- merge: **BLOCKED — human authorization required**.
