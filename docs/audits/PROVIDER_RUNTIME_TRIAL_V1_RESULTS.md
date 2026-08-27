---
id: audit.provider-runtime-trial-v1-results
title: Provider Runtime Trial V1 — resultados executados
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Runtime Trial V1 — resultados executados

## Escopo do claim

Estes resultados são de **SDK Runtime Trial offline/controlado**. Eles não são Provider/Model Trial e não autorizam ranking de fornecedores, modelos, custo, tokens ou latência de API.

O primeiro conjunto completo de runtime executado em CI na branch V1 usou:
- OpenAI Agents SDK `0.22.0`;
- Google ADK Python `2.8.0`;
- MCP Python SDK `2.1.1`, negociando `2026-07-28`;
- Python `3.12.14`;
- Ubuntu GitHub-hosted runner.

## Resultado observado

| Adapter | Runtime real | Boundary externo | Task success | VAR | RSR | DSER | CTVR |
|---|---|---|---:|---:|---:|---:|---:|
| OpenAI Agents SDK 0.22.0 | sim | official `ScriptedModel` | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 |
| Google ADK 2.8.0 | sim | custom offline `BaseLlm` | 1.0 | NOT_EXECUTED | 1.0 | NOT_EXECUTED | 0.0 |
| MCP Python SDK 2.1.1 | sim | client/server in-process | 1.0 | NOT_EXECUTED | 1.0 | NOT_EXECUTED | 0.0 |

### OpenAI

A execução passou pelo `Runner` e tool pipeline reais do SDK. O `ScriptedModel` oficial chamou a mesma tool sintética duas vezes com o mesmo `operation_id`. O ledger NEXUS registrou uma única execução do efeito e uma receipt verificável.

Isso demonstra **a integração do controle de idempotência do NEXUS através do runtime OpenAI testado**. Não demonstra que o SDK OpenAI, isoladamente, fornece exactly-once ou Execution Receipts.

### Google ADK

A execução usou `Runner` e `InMemorySessionService` reais com um `BaseLlm` customizado offline. O marcador foi transportado pelo runtime e uma falha determinística do modelo foi propagada de forma bounded.

A2A, HITL pause/resume, tool side effects, VAR e DSER permanecem **NOT_EXECUTED** neste boundary. Issues upstream de A2A/state não foram reproduzidos.

### MCP

A execução usou `MCPServer` e `Client` reais no mesmo processo. A negociação observada foi `2026-07-28`. Uma tool de falha retornou `is_error` dentro do limite temporal.

HTTP, DNS, OAuth, MRTR, server discovery remoto, auth audience/resource e network chaos permanecem **NOT_EXECUTED**.

## Duração observada

Em uma execução de CI de referência:
- OpenAI offline runtime: ~23 ms;
- Google ADK offline runtime: ~172 ms;
- MCP in-process runtime: ~54 ms.

Esses números **não são benchmark comparativo de performance**. Os boundaries fazem trabalhos diferentes, rodam em jobs separados e não incluem provider/network. Eles servem apenas para provar terminação e registrar observabilidade local.

## Métricas deliberadamente ausentes

- provider latency;
- token usage;
- estimated cost;
- model correctness beyond the deterministic marker;
- p95/p99;
- model quality.

Ausência é representada por `null`/NOT_EXECUTED, não zero.

## Supply chain da execução

Cada job:
1. instala um top-level pin exato;
2. executa `pip check`;
3. registra `pip freeze`;
4. gera JSON de evidência;
5. publica artifact separado.

Risco residual: dependências transitivas ainda não são hash-locked. O freeze captura o ambiente resolvido da execução, mas não substitui lockfile com hashes/provenance attestations.

## Classificação de achados externos

| Achado | Resultado V1 |
|---|---|
| OpenAI 0.22.0 hardening de replay/redaction | MONITORING |
| OpenAI timeout/cleanup | POTENTIALLY_APPLICABLE; bounded failure offline passou, provider timeout real não executado |
| Google ADK 2.8.0 mudanças A2A/task/state | MONITORING |
| Google ADK issues A2A/state | POTENTIALLY_APPLICABLE; não reproduzidos neste V1 |
| MCP advisories históricos de 1.x | NOT_APPLICABLE ao pin 2.1.1 por versão |
| MCP 2026-07-28 version negotiation | REPRODUCED como compatibilidade funcional no client/server in-process |
| T6 não escalar para T1 no host NEXUS | MITIGATED no host/reference layer; não é claim de resistência intrínseca do modelo/SDK |

## Conclusão permitida

Os três runtimes oficiais selecionados foram exercitados com sucesso em boundaries offline e controlados. O V1 demonstra integração funcional e bounded failure nos cenários executados.

**Não demonstra superioridade entre OpenAI, Google ou MCP.**
