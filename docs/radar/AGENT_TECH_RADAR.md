---
id: radar.agent-tech
title: NEXUS Agent Technology Radar
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# NEXUS Agent Technology Radar

## Objetivo

Registrar tecnologias relevantes sem converter descoberta em dependência automática.

## Estados de adoção

- **ADOPT** — estável, usado e testado no NEXUS.
- **TRIAL** — benchmark/integração ativa em ambiente controlado.
- **ASSESS** — estudo e triagem.
- **HOLD** — não adotar até resolução de riscos/lacunas.

## Radar atual

| Tecnologia | Versão verificada | Estado | Prioridade | Justificativa |
|---|---|---:|---:|---|
| Python stdlib validation core | Python 3.12 CI | ADOPT | 10/10 | Base simples, reproduzível e de baixo bootstrap. |
| OpenAI Agents SDK | 0.22.0 | TRIAL — runtime offline | 9.7/10 | Runner/tool pipeline real executado com ScriptedModel oficial; provider/model externo não testado. |
| Google ADK Python | 2.8.0 | TRIAL — runtime offline | 9.7/10 | Runner/session real executado com BaseLlm offline; A2A/HITL real continua gated. |
| MCP | Python SDK 2.1.1 / spec 2026-07-28 | TRIAL — runtime in-process | 10/10 | Client/server real executado in-process com negociação 2026-07-28; HTTP/auth/MRTR remoto pendente. |
| Google ADK Go | — | ASSESS | 9.3/10 | Relevante para concorrência e serviços; não criar integração só por paridade. |
| Agent Skills specification/patterns | current upstream | ASSESS/TRIAL parcial | 10/10 | Supply-chain auditor e lifecycle seguro já existem no reference layer. |
| LangGraph | — | ASSESS | 8.5/10 | Útil para stateful graphs/checkpointing; entra depois dos três adapters prioritários. |
| Microsoft Agent Framework | Python 1.15.0 / .NET 1.19.0 | ASSESS/MONITORING | 8.8/10 | Relevante e atual, mas V1 bloqueia runtime até Contract Trial paritário. |
| CrewAI | — | ASSESS | 8/10 | Bom para papéis/flows; não priorizar sobre contratos e reliability. |
| AutoGen | — | HOLD for new core work | 6/10 | Estudar padrões, não usar como default sem evidência atual. |
| OpenTelemetry | múltiplas integrações | TRIAL/partial | 9.5/10 | Adequado para tracing distribuído; redaction e schema NEXUS são obrigatórios. |

## O que `TRIAL — contract only` significa

Existe código executável NEXUS aplicando exatamente os mesmos invariantes a cada adapter declarado, com versões oficiais registradas e CI. Isso **não** significa que o SDK/protocolo real foi executado, benchmarkado ou considerado equivalente.

Nenhuma métrica de latência, custo, tokens, task success ou segurança comparativa pode ser publicada até o estágio `TRIAL — runtime`.

## Achados upstream em monitoramento

### OpenAI Agents SDK

- 0.22.0: runtime/data-isolation hardening — `MONITORING`;
- 0.21.1: model-call timeout/cleanup — `POTENTIALLY_APPLICABLE` ao adapter real.

### Google ADK

- issue #6721 — cenário A2A/human-input resume na 2.7.0 — `POTENTIALLY_APPLICABLE`;
- 2.7.1 — session initialization validation — `MONITORING`.

Nenhum item acima é alegado como vulnerabilidade local reproduzida.

### MCP

- spec 2026-07-28 stateless core e authorization hardening — `MONITORING`;
- conteúdo MCP externo permanece T6; non-escalation T6→T1 está `MITIGATED` no reference layer, não validada ainda contra SDK/servidor real.

## Fluxo de adoção

```text
DISCOVERED → TRIAGED → AUDITED → CONTRACT_TRIAL → RUNTIME_TRIAL → APPROVED → ADOPTED
                                      ↘ REJECTED / HOLD
```

## Regra

Nenhuma tecnologia muda para `RUNTIME_TRIAL` ou `ADOPT` sem dependência/version pin, fonte oficial, threat review, testes equivalentes, rollback e evidência do SHA executado.

## Provider Runtime Trial V1

O V1 promoveu OpenAI Agents SDK, Google ADK e MCP do estágio de contrato para runtime controlado/offline. Isso **não** promove nenhum deles a ADOPT e não cria ranking de providers. O próximo gate exige fechar A2A/HITL, MCP remoto/auth/MRTR, observabilidade runtime e supply-chain locking.
