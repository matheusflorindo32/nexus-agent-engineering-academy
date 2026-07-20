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
| AUD-P2-001 | P2 | `course/modules` | estabelecer Modules 00–12 sem prefixos duplicados | `python tests/validate_repository.py` | ADR-001 | um diretório canônico por número | aprovado pela CI |
| AUD-P2-002 | P2 | `labs` | reservar LAB-1001 para observabilidade e LAB-1101 para idempotência | validador de LABs e links | ADR-001 | número e ID únicos | aprovado pela CI |
| AUD-P2-003 | P2 | `examples/observability_pipeline.py` | redigir segredos embutidos em valores permitidos | self-test O13–O14 | ADR-002; REF-003; REF-005 | nenhum segredo sintético persistido | aprovado se a CI executar 15/15 |
| AUD-P2-004 | P2 | quarentena de telemetria | aplicar sanitização antes da quarentena sem modificar a entrada | self-test O15 | ADR-002 | quarentena sem dado sensível e entrada imutável | aprovado se a CI executar 15/15 |
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

## Limitação

A matriz registra cobertura conhecida. Ela não equivale a prova de ausência universal de regressões ou vazamentos. Novos formatos de segredo e dependências externas exigem revisão contínua.
