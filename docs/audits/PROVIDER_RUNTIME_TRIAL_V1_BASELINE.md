---
id: audit.provider-runtime-trial-v1-baseline
title: Provider Runtime Trial V1 — baseline e triagem oficial
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Runtime Trial V1 — baseline e triagem oficial

## Estado de partida

Branch criada diretamente do head auditado do PR #54: `9b39879050b291cb8b641294f3338d64cca23bb3`.

PR #53 e PR #54 permanecem abertos e sem merge.

O estado herdado já contém:
- Hardening V2;
- Contract Trial V3;
- VAR/RSR/DSER/CTVR no control-plane;
- Trust Model T0–T7;
- Execution Receipts e idempotência de referência;
- Technology Radar;
- Framework Upgrade Gate.

Ainda não havia execução de SDK/protocolo real.

## Fontes oficiais revalidadas

### OpenAI Agents SDK
- upstream: `openai/openai-agents-python`;
- versão estável verificada: `0.22.0`;
- testing oficial oferece `agents.testing` com `ScriptedModel` e falhas determinísticas sem requests de provider;
- model-call timeout é configurável;
- página de segurança do repositório não lista advisory publicado na data da auditoria.

### Google ADK Python
- upstream: `google/adk-python`;
- versão estável atual verificada: `2.8.0`, publicada em 2026-08-26;
- 2.8.0 adiciona, entre outros itens, task mode A2A, Model Armor plugin, métricas experimentais, melhorias MCP/telemetry e correções de segurança/correctness;
- repositório oficial não lista advisory publicado na data da auditoria;
- issues upstream de state/A2A permanecem evidência para testes, não vulnerabilidade NEXUS.

### MCP
- spec estável: `2026-07-28`;
- Python SDK atual selecionado: `2.1.1`;
- v2 implementa 2026-07-28 e negocia versões anteriores;
- security policy diz que somente a release mais nova de cada linha suportada recebe fixes;
- advisories históricos High existem para versões 1.x antigas; eles não são automaticamente aplicáveis ao 2.1.1.

### Microsoft Agent Framework
- upstream: `microsoft/agent-framework`;
- Python release verificada: `1.15.0`;
- .NET 1.19.0 inclui migração de long-running MCP tasks para a extensão 2026-07-28;
- V1 classifica MAF como `MONITORING` por ausência de Contract Trial paritário prévio.

## Matriz de aplicabilidade

| Achado | Classificação NEXUS V1 | Motivo |
|---|---|---|
| OpenAI 0.22.0 blocked-tool-output redaction | MONITORING | relevante para replay/state; V1 offline não reproduz o fluxo completo |
| OpenAI model-call timeout | POTENTIALLY_APPLICABLE | boundary de timeout/retry será testada em etapa futura com provider real; V1 testa bounded failure offline |
| Google ADK 2.8.0 new A2A/task behavior | MONITORING | mudança atual; exige regressão específica antes de side effects reais |
| Google ADK issue #6644 state_delta on resume | POTENTIALLY_APPLICABLE | runtime/state é alvo do laboratório; não declarar reproduzido até teste específico |
| MCP advisories 1.x históricos | NOT_APPLICABLE ao pin 2.1.1 por versão | registrar como precedente de threat model, não como bug local |
| MCP 2026-07-28 stateless/version negotiation | POTENTIALLY_APPLICABLE | V1 executará client/server real in-process |
| Microsoft Agent Framework runtime | MONITORING | fora do V1 por gate metodológico |

## Claim boundary

O V1 pode afirmar apenas o que a CI realmente executar.

`real SDK runtime + simulated model/in-process server != real provider/model trial`.
