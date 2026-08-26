---
id: research.readiness-v3
title: Research Readiness V3 — comparação de providers
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Research Readiness V3 — comparação de providers

## Pergunta

O NEXUS já pode afirmar que OpenAI Agents SDK, Google ADK ou MCP é superior em confiabilidade, segurança, custo ou desempenho?

**Não.** O milestone V3 estabelece paridade de contrato e proveniência/versionamento, mas ainda não executa os runtimes reais.

## O que já pode ser medido

No Contract Trial, todos os adapters declarados passam pelo mesmo oracle NEXUS para:

- Verified Action Rate (VAR);
- Recovery Success Rate (RSR);
- Duplicate Side Effect Rate (DSER);
- Context Trust Violation Rate (CTVR).

Essas métricas validam o wrapper/control-plane NEXUS. Não medem o framework real.

## O que ainda exige Runtime Trial

- task success rate;
- correctness com modelo real;
- latency e p95/p99;
- token usage e custo;
- tool-call count;
- retry/error rate reais;
- interruption/resume do SDK;
- state/session integrity real;
- prompt injection/tool poisoning contra runtime;
- tracing/OpenTelemetry real;
- A2A/HITL real no ADK;
- MCP 2026-07-28 real com version negotiation/MRTR.

## Desenho do próximo experimento

Para cada adapter real:

1. fixar versão e lockfile;
2. registrar provider/model/configuração;
3. usar exatamente o mesmo dataset/tarefas;
4. separar control-plane determinístico de comportamento estocástico do modelo;
5. repetir runs e reportar distribuição, não somente média;
6. pré-definir critérios de sucesso/falha e exclusão;
7. registrar falhas e retries sem descarte seletivo;
8. incluir cenário benigno, falha de transporte, indirect injection e side effect idempotente;
9. emitir JSON/CSV com SHA, timestamp, versão, seed quando aplicável e limitações;
10. não inferir causalidade se modelos/configurações não forem equivalentes.

## Classificação de maturidade

- Contratos comuns: **alto**.
- Proveniência/version baseline: **alto para a data verificada**.
- Contract Trial reproduzível: **implementado, aguardando CI do SHA final**.
- Runtime Trial OpenAI: **não implementado**.
- Runtime Trial Google ADK: **não implementado**.
- Runtime Trial MCP: **não implementado**.
- Comparação científica pública: **não pronta**.

## Próximo gate científico

Criar protocolo versionado `PROTOCOL_PROVIDER_RUNTIME_COMPARISON_V1.md` antes de executar qualquer comparação paga ou dependente de modelo.
