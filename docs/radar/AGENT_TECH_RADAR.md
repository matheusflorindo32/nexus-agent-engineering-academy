---
id: radar.agent-tech
title: NEXUS Agent Technology Radar
lang: pt-BR
status: review
reviewed_at: 2026-08-25
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

| Tecnologia | Categoria | Estado | Prioridade | Justificativa |
|---|---|---:|---:|---|
| Python stdlib validation core | Foundation | ADOPT | 10/10 | Base atual simples, reproduzível e de baixo bootstrap. |
| OpenAI Agents SDK | Agent framework | ASSESS/TRIAL planned | 9.5/10 | Forte em tools, handoffs, guardrails e tracing; exige benchmark e upgrade gate. |
| Google ADK Python | Agent framework | ASSESS | 9.5/10 | Arquitetura rica, A2A/HITL e workflows; achados recentes exigem testes de integridade antes de adoção crítica. |
| Google ADK Go | Agent framework/runtime | ASSESS | 9.3/10 | Relevante para concorrência e serviços; não criar integração só por paridade. |
| Agent Skills specification/patterns | Skills | ASSESS | 10/10 | Prioridade alta para portabilidade e codificação de processos; supply chain deve preceder adoção. |
| MCP | Protocol/tools | ASSESS/TRIAL planned | 10/10 | Camada central de interoperabilidade; tratar conteúdo e metadata como não confiáveis. |
| LangGraph | Orchestration | ASSESS | 8.5/10 | Útil para stateful graphs/checkpointing; só entra após tarefa comparável. |
| Microsoft Agent Framework | Agent framework | ASSESS | 8.5/10 | Relevante para enterprise, workflows e observabilidade; acompanhar maturidade. |
| CrewAI | Multi-agent | ASSESS | 8/10 | Bom para papéis/flows; não priorizar sobre contratos e reliability. |
| AutoGen | Historical/legacy patterns | HOLD for new core work | 6/10 | Estudar padrões, mas não usar como default para nova arquitetura sem evidência atual. |
| OpenTelemetry | Observability | TRIAL/partial | 9.5/10 | Adequado para tracing distribuído; precisa de contrato de eventos NEXUS e redaction. |

## Achados upstream em monitoramento

### OpenAI Codex

- issue #40399 — transporte terminal pode deixar leituras futuras bloqueadas;
- issue #40425 — refresh concorrente de Skills pode gerar ENOENT transitório.

**Uso no NEXUS:** fonte de requisitos e testes, não evidência de vulnerabilidade local.

### Google ADK

- issue #6461 — risco de confirmação HITL forjada por peer A2A no cenário descrito;
- issue #6721 — regression 2.7.0 em resume de human-input/A2A;
- issue #6831 — possível contaminação de delegações posteriores por state/event shape.

**Uso no NEXUS:** gate obrigatório para adapters A2A/HITL e state integrity.

## Fluxo de adoção

```text
DISCOVERED → TRIAGED → AUDITED → TESTED → APPROVED → ADOPTED
                             ↘ REJECTED / HOLD
```

## Regra

Nenhuma tecnologia muda de `ASSESS` para `TRIAL/ADOPT` sem versão registrada, fontes oficiais, threat review, testes equivalentes e plano de rollback.