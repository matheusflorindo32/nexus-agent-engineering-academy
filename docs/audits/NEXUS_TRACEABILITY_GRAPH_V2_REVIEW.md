---
id: audit.nexus-traceability-graph-v2-review
content_id: audit.nexus-traceability-graph-v2-review
version: 1.0.0
title: NEXUS Traceability Graph V2 — Review
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Traceability Graph V2 — Review

## Review scope

Separate review pass over the Graph V2 architecture, security boundary, traceability semantics and reproducibility contract. This is **not** an independent human audit. Independent machine verification is provided by separate repository and dedicated CI workflows; human review remains the merge gate.

## Architecture review

**Decision: PASS for Design Trial scope.**

- NEXUS Control Plane remains authoritative.
- Graph V2 is an extension, not a replacement framework.
- persistent schema lives at `.nexus/traceability/graph-v2.schema.json`;
- `.nexus/traceability/model.json` routes to that schema;
- graph runtime is Python stdlib-only;
- no graph database, vendor SDK, code parser or framework runtime was introduced;
- human merge/release authority remains outside the graph.

## Adversarial review

### Finding A1 — semantic graph poisoning

**Severity: High within graph integrity scope; fixed via TDD.**

A known edge name could initially connect semantically incompatible node types. Example: `requirement --DEPENDS_ON--> evidence`.

The adversarial test was committed first and produced a real RED. The implementation now enforces endpoint constraints for every edge type, including:

- `REFINED_BY`: requirement → spec;
- `PLANNED_BY`: spec → task;
- `TOUCHES_FILE`: spec/task → file;
- `TOUCHES_SYMBOL`: spec/task → symbol;
- `CONTAINS_SYMBOL`: file → symbol;
- `DEPENDS_ON`: file/symbol → file/symbol;
- `VERIFIED_BY`: task/file/symbol → test;
- `PRODUCES_EVIDENCE`: test/task → evidence.

### Finding A2 — Control Plane schema routing

**Severity: Medium; fixed via TDD.**

The V1 traceability model did not explicitly route to the Graph V2 schema. The failing contract was observed before updating `model.json` to `nexus.traceability.v2` with `graph_schema`.

### Finding A3 — prior SpecD evidence weaknesses

Three unresolved P1 findings inherited from PR #58 were independently validated before Graph V2 implementation and fixed only in this stacked branch:

- precision now counts unexpected affected files;
- upstream/runtime failure phase is preserved;
- graph index/query failure paths preserve bounded evidence;
- known blocked SpecD pin is not repeatedly executed without a new candidate.

## Security review

**PASS for frozen parser-free graph-document boundary; broader repository indexing remains NOT_TESTED.**

Executable controls cover:

- absolute/path-traversal/NUL path rejection;
- bounded node, edge, fan-out and traversal sizes;
- duplicate edge rejection;
- missing-node references rejected;
- unknown node/edge types rejected;
- semantically incompatible edge endpoint types rejected;
- malformed metadata rejected;
- metadata string/depth limits;
- injection-like metadata flagged as `UNTRUSTED_METADATA` and never executed;
- bounded traversal despite cycles;
- deterministic canonicalization/fingerprints.

Not demonstrated in V2 Design Trial:

- parsing hostile source-language ASTs;
- symlink/filesystem race handling;
- untrusted external graph database input;
- network/MCP ingestion into graph;
- actual tool execution from graph metadata;
- distributed graph concurrency;
- cryptographic signing of graph provenance.

Those remain `NOT_TESTED` or `NOT_APPLICABLE` rather than implicit PASS.

## Traceability audit

The canonical chain is machine traversable:

`requirement → spec → task → file/symbol → test → evidence`.

The graph supports reverse traversal so code/symbol change-impact can recover upstream specs and requirements. Orphan diagnostics cover requirement, spec, task, implementation, test and evidence classes. Drift/staleness diagnostics are explicit and stable.

Limit: Graph V2 currently consumes an explicit graph document. Automatic source-code symbol discovery and Git-based rename inference are not implemented.

## Reproducibility audit

**PASS for frozen Design Trial.**

- protocol versioned;
- fixtures versioned;
- fixture SHA-256 manifest committed;
- CI verifies hashes before benchmark;
- five repetitions mandatory;
- graph canonicalization deterministic;
- fingerprint equality required;
- runtime dependencies added = 0;
- Execution Receipt binds benchmark result, fixture manifest and branch head.

## Performance interpretation

Timing uses a seven-node/seven-edge synthetic graph on a GitHub-hosted runner. `tracemalloc` measures Python allocations, not process RSS. No scaling claim is justified from these values.

Before production use, benchmark at minimum sparse, dense and pathological graphs near configured limits, plus real repositories.

## Supply-chain review

Graph V2 itself adds zero third-party runtime dependencies. This intentionally avoids adding a graph database/parser dependency before there is empirical need. GitHub Actions remain upstream dependencies governed by existing repository CI policy.

## Provenance review

No SpecD source implementation was copied. Concepts adapted after upstream study include:

- explicit file/symbol nodes;
- dependency relations;
- bounded change-impact traversal;
- graph fingerprinting;
- coverage/stale-link concepts;
- machine-readable impact output.

NEXUS adds requirement/task/test/evidence authority, release gates, Evidence Classes and Execution Receipts around those concepts.

## Technical debt / next engineering work

1. automatic repository indexer from files/symbols;
2. parser adapters for selected languages under sandboxed limits;
3. Git rename/move reconciliation;
4. incremental graph update and invalidation;
5. larger real-repository benchmark;
6. trusted provenance/signing for externally produced graph fragments;
7. stronger policy for cycles allowed only in dependency subgraphs if needed;
8. schema-validator tooling if complexity justifies a dependency.

## Review gate

- architecture: PASS for Design Trial;
- adversarial review: PASS after A1/A2 fixes;
- security: PASS for explicit bounded graph-document boundary;
- traceability: PASS for canonical synthetic chain;
- reproducibility: PASS for frozen trial;
- real-repository indexer: NOT_TESTED;
- SpecD runtime comparison: NOT_TESTED;
- independent human review: PENDING;
- merge: BLOCKED pending explicit human authorization.