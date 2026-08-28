---
id: governance.upstream-adoption-matrix-v1
content_id: governance.upstream-adoption-matrix-v1
version: 1.0.0
title: Matriz de adoção e provenance upstream V1
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Matriz de adoção e provenance upstream V1

## Regra

`Upstream pattern ≠ NEXUS dependency ≠ NEXUS security claim.` Ideias podem ser reimplementadas; código/texto somente com licença/provenance compatíveis. Nenhum código upstream é copiado nesta versão.

| Fonte oficial | Capacidade | Licença observada | Decisão | Adaptação local | Risco/limite |
|---|---|---|---|---|---|
| `github/spec-kit` | constitution, SDD lifecycle, converge, workflow composition | MIT | ADAPT | lifecycle e constitution vendor-neutral | não instalar CLI por padrão |
| `Fission-AI/OpenSpec` | lightweight/living specs, change workflow | MIT | ADAPT | specs incrementais e revisão antes do código | não duplicar fonte da verdade |
| `aws-samples/sample-specship` | RECON, TDD, adversarial validation, recover/ship | MIT; experimental | ADAPT | RECON e adversarial review | upstream declara ausência de revisão externa de segurança |
| `obra/superpowers` | brainstorming, approval gate, TDD, debugging, plans, verification | MIT | ADOPT/ADAPT | disciplina operacional NEXUS | skill text não é copiado; princípios são reimplementados |
| `kirodotdev/Kiro` | Specs, Hooks, Steering, MCP, Powers | não confirmada como licença OSS reutilizável nesta auditoria | STUDY/ADAPT concepts | hook policy e steering contextual | não copiar código/templates até licença específica ser validada |
| `bmad-code-org/BMAD-METHOD` | role separation, orchestration, handoffs | MIT + trademark notice | ADAPT | papéis Planner/Builder/Verifier/Security/Release | evitar uso de marca como produto derivado |
| `specd-sdd/SpecD` | compiled context, deterministic verification, graph/impact, hooks | MIT | STUDY/ADAPT | traceability model e futuro trial | upstream jovem; evitar dependência core no V1 |
| `buildermethods/agent-os` | standards discovery/injection | MIT | ADAPT | standards registry contextual | V3 deliberadamente não compete com planning moderno |
| `open-gsd/gsd-core` | fresh-context subagents, persistent state, verify/fix loop | MIT | STUDY/ADAPT | context isolation em trabalhos longos | predecessor `gsd-build/get-shit-done` arquivado |
| `specdd/specdd` | local/source-adjacent specs | Apache-2.0 + trademark notice | STUDY | avaliar em trial isolado | não introduzir `.sdd` no V1 |

## Decisões transversais

### ADOPT
- evidence before assertion;
- approval antes de implementação arquitetural;
- TDD quando comportamento é testável;
- systematic debugging;
- independent verification;
- human merge authority;
- provenance obrigatória.

### ADAPT
- constitution/lifecycle;
- RECON;
- standards registry/injection;
- role separation;
- hooks declarativos;
- traceability/drift model;
- context isolation;
- convergence.

### STUDY
- SpecD CLI/MCP como dependência real;
- SpecDD `.sdd`;
- Open GSD Core como runtime de orquestração;
- qualquer integração executável com Kiro.

### REJECT
- framework soup;
- múltiplas fontes canônicas concorrentes;
- dependência obrigatória de IDE/vendor;
- auto-merge;
- execução de código upstream não auditado;
- claims de segurança derivados apenas de documentação upstream.

## Provenance snapshot

Data da observação: `2026-08-28`.

Fontes consultadas: repositórios oficiais, README/SECURITY/LICENSE/release history disponíveis publicamente. A versão V1 registra conceitos e licenças observadas, não blobs copiados. Quando código upstream vier a ser incorporado, registrar tag/commit exato, arquivo, licença e modificação em registro específico antes do merge.
