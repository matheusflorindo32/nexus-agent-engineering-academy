---
id: audit.nexus-repository-indexer-v1-results
content_id: audit.nexus-repository-indexer-v1-results
version: 1.0.0
title: NEXUS Repository Indexer V1 — Results
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Repository Indexer V1 — Results

## Frozen inputs

- `protocol.json` SHA-256: `ad9384481fbc89f21457dbc500cf90d39840896f1fac3f60fa970939501a3ff3`
- `fixtures.json` SHA-256: `123946a63f217c667d048a629583ecdb0d4faa18ad4bf84539b1b98594ad0a15`
- repetitions: 5
- runtime dependencies added: 0

## Fixture evidence

Class: `DETERMINISTIC_CONTROL_EVIDENCE`.

The initial GREEN capture produced a 100/100 score inside the frozen fixture corpus with precision, recall, F1, fixture pass rate and deterministic rerun equality equal to 1.0 and zero observed false positives/false negatives. This is a bounded synthetic-corpus result, not a production-quality or multi-language claim.

## Real repository evidence

Class: `REAL_RUNTIME_EVIDENCE` for observations made by the workflow while indexing this repository read-only. The final workflow artifact is authoritative for file/symbol counts, fingerprint, elapsed time, memory and incremental reuse because those values depend on the exact PR head.

The real-repository correctness score is deliberately `NOT_APPLICABLE`: no independent full oracle exists for every symbol/dependency in the repository. TypeScript, JavaScript and rename inference remain `NOT_TESTED`.

## Security evidence

The workflow asserts zero repository writes. The indexer reports zero network calls and zero executed repository instructions. Prompt-injection-like strings are counted as untrusted text only.

## Score boundary

`100/100` may be reported only for the frozen fixture benchmark when the final FROZEN hash check passes. It must not be presented as NEXUS overall quality, production security, real-repository correctness, or superiority over SpecD.
