---
id: adr.008.runtime-trial-boundaries
title: ADR-008 — separar SDK Runtime Trial de Provider/Model Trial
lang: pt-BR
status: review
---

# ADR-008 — separar SDK Runtime Trial de Provider/Model Trial

## Contexto

O NEXUS precisa avançar além de adapters de contrato sem transformar um teste offline em alegação de desempenho de provider/model. OpenAI Agents SDK oferece `ScriptedModel`; Google ADK permite `BaseLlm` customizado; MCP permite client/server in-process. Essas boundaries executam runtime real com comportamento externo controlado.

## Decisão

Adotar três níveis explícitos:

1. **Contract Trial** — NEXUS stdlib, sem SDK.
2. **SDK Runtime Trial** — SDK/protocolo real, modelo/servidor controlado e sem provider externo.
3. **Provider/Model Trial** — serviço/modelo externo real, somente após autorização, orçamento e protocolo estatístico.

O V1 promove OpenAI Agents SDK, Google ADK e MCP ao segundo nível apenas se o CI do runtime real passar.

## Isolamento

Cada SDK é instalado em job separado para reduzir conflitos de dependência e permitir `pip freeze` por adapter.

Top-level pins são exatos. Dependências transitivas ainda não são hash-locked; o `pip freeze` da execução registra o ambiente resolvido. Hash locking completo fica como hardening futuro e risco residual de supply chain.

## Microsoft Agent Framework

Permanece `MONITORING` no V1 porque não passou pelo Contract Trial V3. Entrar diretamente no Runtime Trial quebraria o gate metodológico.

## Consequências

### Positivas
- prova execução de runtime oficial sem custo/API;
- mantém claims proporcionais à evidência;
- evidencia incompatibilidades reais de instalação/API;
- permite evolução posterior para provider real.

### Limitações
- não mede qualidade de modelo;
- não mede rede externa;
- não testa credenciais/OAuth;
- não produz custo/tokens de provider;
- não prova segurança contra prompt injection do modelo.

## Gate de promoção

Nenhum adapter recebe status `TRIAL — runtime` até seu job pinado passar e a evidência JSON registrar boundary e versão.
