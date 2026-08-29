---
id: governance.upstream-adoption-matrix-v5
content_id: governance.upstream-adoption-matrix-v5
version: 5.0.0
title: NEXUS Upstream Adoption Matrix V5
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Upstream Adoption Matrix V5

| Capability | Source | Decision | Local implementation / rationale |
|---|---|---|---|
| Repository discovery + Python symbols | NEXUS native / Python stdlib | ADOPT | Read-only `os.walk` + `ast`; zero runtime dependencies. |
| Incremental content-hash reuse | NEXUS native | ADOPT | SHA-256 record reuse with changed/reused/removed accounting. |
| File/symbol graph + impact concepts | SpecD `14422dba5c1cc64f04205f3ebfa3d435cd790aa0` | ADAPT | Concepts only; no source copied and no runtime dependency. Upstream `main` rechecked 2026-08-28 and remains at the known blocked pin. |
| SpecD runtime dependency | SpecD | MONITOR | Do not rerun until a new reproducible commit/tag candidate exists. |
| Constitution/spec lifecycle | GitHub Spec Kit v1.0.1 | ADAPT | Remains governance inspiration; not installed into indexer. |
| Incremental change/approval model | OpenSpec v1.11.0 | ADAPT | Conceptual fit; no dependency needed for indexing. |
| TDD/systematic verification | Superpowers | ADOPT / ADAPT | RED→GREEN and verification-before-completion applied to this trial. |
| Heavy graph database | generic graph DBs | REJECT | No demonstrated need at current scale; worsens supply-chain/operational complexity. |
| Third-party Python parser | parser ecosystems | REJECT for V1 | Python stdlib AST is sufficient for the bounded Python-only scope. Reconsider only for multi-language trial. |
| TypeScript/JavaScript parser | NOT SELECTED | STUDY | Multi-language indexer is a later gate; no runtime claim in V1. |
| Git rename inference | Git history strategies | STUDY | Valuable, but explicitly `NOT_TESTED` in V1. |

## Provenance boundary

No upstream code or templates are copied into the indexer implementation. Architectural ideas are reimplemented independently under the NEXUS contracts. License/provenance records from earlier Control Plane trials remain authoritative for Spec Kit, OpenSpec, SpecD and Superpowers.
