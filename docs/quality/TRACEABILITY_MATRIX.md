---
id: docs.quality.traceability-matrix
title: Matriz de rastreabilidade da correção Premium Elite
lang: pt-BR
status: review
---

# Matriz de rastreabilidade da correção Premium Elite

## Escopo

Esta matriz liga os achados confirmados da auditoria às mudanças implementadas, testes, critérios de aceite e fontes. Não inclui recomendações ainda não adjudicadas.

| Achado | Severidade | Arquivo ou área | Mudança confirmada | Teste correspondente | Referência | Critério de aceite | Resultado esperado |
|---|---|---|---|---|---|---|---|
| AUD-P2-001 | P2 | `course/modules` | estabelecer Modules 00–12 sem prefixos duplicados | `python tests/validate_repository.py` e testes negativos do validador | ADR-001 | um diretório canônico por número | corrigido; aprovado no snapshot de CI |
| AUD-P2-002 | P2 | `labs` | reservar LAB-1001 para observabilidade, LAB-1101 para idempotência e catalogar os 12 LABs existentes | validador de LABs e links | ADR-001 | número e ID únicos; catálogo completo | corrigido; aprovado no snapshot de CI |
| AUD-P2-003 | P2 | `examples/observability_pipeline.py` | mascarar segredos embutidos em valores permitidos | self-test O13–O14 e casos adversariais adicionais | ADR-002; REF-003; REF-005 | nenhum segredo sintético persistido | corrigido; aprovado no snapshot de CI |
| AUD-P2-004 | P2 | quarentena de telemetria | aplicar sanitização antes da quarentena sem modificar a entrada | self-test O15 e testes dedicados | ADR-002 | quarentena sem dado sensível e entrada imutável | corrigido; aprovado no snapshot de CI |
| AUD-P2-005 | P2 | frontmatter curricular | validar ID, slug e pré-requisitos contra a árvore conhecida | testes negativos com fixtures temporárias | ADR-001 | pré-requisito inexistente e slug duplicado reprovam | corrigido; aprovado no snapshot de CI |
| AUD-P2-006 | P2 | migração curricular | mapear individualmente os caminhos removidos e registrar redução de MCP/Skills | revisão do diff `main...2100dc7` | ADR-001; MIGRATION_GUIDE | nenhuma equivalência implícita ou perda não registrada | implementado com risco residual explícito |
| AUD-P2-007 | P2 | integração | documentar ordem PR final → PR #7 → PR #6 → `main` e rollback por estágio | revisão humana da base/head e dos SHAs | MIGRATION_GUIDE; RELEASE_READINESS | nenhuma integração fora de ordem | documentado; execução proibida nesta branch |
| AUD-P3-001 | P3 | governança | registrar taxonomia e migração em ADR e guia | validação de links e frontmatter | ADR-001 | documentos rastreáveis | implementado nesta branch |
| AUD-P3-002 | P3 | referências | criar registro ABNT com status de verificação | revisão documental | REFERENCIAS_ABNT | nenhuma norma declarada como integralmente verificada sem acesso oficial | implementado com ressalva explícita |
| AUD-P3-003 | P3 | release | publicar readiness e risco residual | revisão humana | RELEASE_READINESS | parecer limitado às evidências | implementado nesta branch |

## Casos adversariais mínimos para redaction

| Caso | Canal | Resultado obrigatório |
|---|---|---|
| `tool="catalog.read token=valor-sintetico"` | persisted | trecho sensível substituído |
| `outcome="Bearer valor-sintetico"` | persisted | credencial substituída |
| segredo em dicionário aninhado | persisted/buffer | conteúdo sensível ausente |
| segredo em lista e tupla | persisted/buffer | tipo preservado quando possível |
| schema incompatível com segredo | quarantine | evento sanitizado antes de armazenar |
| segredo em mensagem de erro | exceção/log | valor ausente da mensagem |

## Evidências obrigatórias de CI

- `tests/validate_repository.py`;
- `python -m compileall -q examples tests`;
- todos os self-tests Python existentes;
- `examples/observability_pipeline.py --self-test` com 15/15;
- TypeScript 5.8.3 em modo strict;
- validação documental;
- artifact do relatório do validador.
- identificação do SHA, ambiente, comandos, resultados e limitações no artifact final.

## Limitação

A matriz registra cobertura conhecida. Ela não equivale a prova de ausência universal de regressões ou vazamentos. Novos formatos de segredo e dependências externas exigem revisão contínua.
