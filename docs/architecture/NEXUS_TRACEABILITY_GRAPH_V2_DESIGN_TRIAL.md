---
id: architecture.nexus-traceability-graph-v2-design-trial
content_id: architecture.nexus-traceability-graph-v2-design-trial
version: 2.0.0
title: NEXUS Traceability Graph V2 — Design Trial
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Traceability Graph V2 — Design Trial

## Goal

Implementar um grafo NEXUS-native, stdlib-only e determinístico que estenda o Control Plane sem substituí-lo. A cadeia autoritativa permanece `requirement → spec → task → code → test → evidence`; o V2 adiciona nós de `file` e `symbol`, relações explícitas, diagnósticos de cobertura/drift e análise de impacto bidirecional.

## Base

- Repository: `matheusflorindo32/nexus-agent-engineering-academy`
- Base PR: #58
- Base SHA: `f997419541c6611293087a4a840865c7a0e100c0`
- Branch: `feat/nexus-traceability-graph-v2-design-trial`
- No merge is authorized.

## Evidence taxonomy

Toda alegação deve ser uma de: `REAL_RUNTIME_EVIDENCE`, `DETERMINISTIC_CONTROL_EVIDENCE`, `DOCUMENTED_UPSTREAM_CAPABILITY`, `INFERRED`, `NOT_TESTED` ou `NOT_APPLICABLE`.

O benchmark do grafo NEXUS usa `DETERMINISTIC_CONTROL_EVIDENCE`. Tempos de CI são medições reais daquela execução, mas não são claims de produção. SpecD runtime continua `NOT_TESTED/BLOCKED` até existir candidato upstream reproduzível.

## Architecture

```text
NEXUS Control Plane
        ↓
Traceability Graph V2
        ↓
Impact / Coverage / Drift Analysis
```

O grafo não pode alterar constitution, human approval, release gates ou evidence classes. Não há graph database, parser externo ou dependência third-party no V2.

### Node types

`requirement`, `spec`, `task`, `file`, `symbol`, `test`, `evidence`.

### Edge types

- `REFINED_BY`: requirement → spec
- `PLANNED_BY`: spec → task
- `TOUCHES_FILE`: spec/task → file
- `TOUCHES_SYMBOL`: spec/task → symbol
- `CONTAINS_SYMBOL`: file → symbol
- `DEPENDS_ON`: file/symbol → file/symbol
- `VERIFIED_BY`: task/file/symbol → test
- `PRODUCES_EVIDENCE`: test/task → evidence

Edges são directed, versioned e canonicalizados. Duplicate edges são rejeitados. IDs e paths são tratados como dados, nunca como instruções.

## Safety limits

- maximum nodes: 2,000
- maximum edges: 8,000
- maximum fan-out per node: 256
- maximum traversal depth: 16
- maximum metadata string length: 2,048 characters
- absolute paths, NUL bytes e path traversal (`..`) são rejeitados
- unknown node/edge types são rejeitados
- references to missing nodes são rejeitadas
- metadata com padrões de prompt/tool injection é marcada como untrusted; nunca executada
- cycles são diagnosticados e traversal sempre permanece bounded

## Determinism and fingerprint

Nós e edges são ordenados por representação canônica. O fingerprint é SHA-256 do JSON canônico do grafo validado. Cinco builds iguais devem produzir fingerprint e output iguais, desconsiderando campos explicitamente temporais de receipts.

## Audit semantics

O V2 deve detectar pelo menos:

- orphan requirement;
- orphan spec;
- orphan task;
- orphan implementation (`file`/`symbol` sem upstream spec/task);
- orphan test;
- orphan evidence;
- spec drift e implementation drift via `expected_hash`/`current_hash`;
- stale/broken file link (`exists=false`);
- stale/broken symbol link (`exists=false`);
- cycles;
- duplicate/poisoned relations;
- pathological fan-out.

## Change impact

A API/CLI oferece traversal `downstream`, `upstream` e `both`, com profundidade explícita. Exemplos esperados:

- requirement → specs/tasks/files/symbols/tests/evidence a revisar;
- spec → implementation/tests/evidence a regenerar;
- file/symbol → upstream specs/requirements e downstream dependents;
- evidence impacted por mudanças upstream.

Saídas JSON são machine-readable; saída text é uma representação do mesmo resultado.

## Frozen fixtures

O trial deriva a cadeia TypeScript simples do PR #58 e padrões de governança do PR #57. O dataset contém no mínimo 18 casos: cadeia válida, seis classes de orphan/drift, stale file/symbol, transitive dependency, cycle, missing symbol, renamed file, traversal path attack, malformed metadata, metadata injection, duplicate edge, poisoned relation e pathological fan-out. Todos os artefatos congelados recebem SHA-256 em manifest.

## Benchmark

Métricas executáveis:

- precision, recall, F1;
- false positives / false negatives;
- orphan detection rate;
- stale-link detection rate;
- regression/security detection rate;
- build duration and impact-query latency;
- node/edge counts and canonical graph bytes;
- Python `tracemalloc` peak allocation;
- deterministic rerun equality;
- fingerprint equality;
- dependencies added (must remain zero runtime third-party dependencies).

Token/context use é `NOT_APPLICABLE` neste benchmark sem LLM. Human maintenance hours são `NOT_TESTED`.

O score 0–100 usa apenas métricas realmente executadas e pesos congelados no protocolo. Não existe comparação numérica com SpecD enquanto SpecD graph runtime estiver `NOT_TESTED`.

## PR #58 inherited review findings

Três P1 do review automatizado do #58 são pré-requisitos nesta branch:

1. precision deve contar qualquer affected file inesperado como false positive, não apenas membros do explicit negative universe;
2. graph index/query failures do SpecD workflow devem produzir receipt/result `BLOCKED`, não perder evidence;
3. upstream setup/install/build/CLI failures devem preservar a fase e diagnóstico reais, sem rotular tudo como lockfile mismatch.

A branch #58 não será alterada; as regressões entram somente nesta branch empilhada.

## Upstream provenance boundary

- GitHub Spec Kit `v1.0.1`: lifecycle/existing-project adoption concepts — ADAPT, MIT.
- OpenSpec `v1.11.0`: stable machine-readable diff/status and explicit approval-before-write concepts — ADAPT, license as upstream repository states.
- SpecD `14422dba5c1cc64f04205f3ebfa3d435cd790aa0`: graph/coverage/impact concepts — ADAPT conceptually; runtime dependency remains STUDY/MONITOR; no source code copied.
- Superpowers: TDD/systematic verification discipline — ADOPT/ADAPT.

## Release gate

`PASS` requires: RED evidence, GREEN, REFACTOR, full repository quality gates, dedicated graph workflow, frozen hashes, execution receipt, adversarial/security/architecture/traceability/reproducibility review, and no unresolved critical/high finding in the new Graph V2 scope. Human merge authorization remains mandatory.