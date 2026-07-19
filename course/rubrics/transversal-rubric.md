---
id: course.rubric.transversal
title: Rubrica transversal NEXUS
lang: pt-BR
status: review
version: 0.1.0
---

# Rubrica transversal NEXUS

Use esta rubrica em módulos, laboratórios e projetos. Segurança e rastreabilidade são critérios de bloqueio.

## Níveis

| Nível | Significado |
|---|---|
| 0 — Insuficiente | não demonstra o resultado ou contém risco crítico |
| 1 — Funcional | cumpre o mínimo com limitações registradas |
| 2 — Robusto | é reproduzível, seguro e bem justificado |
| 3 — Excelente | adiciona validação adversarial, comparação e melhoria mensurável |

## Dimensões

| Dimensão | 0 — Insuficiente | 1 — Funcional | 2 — Robusto | 3 — Excelente |
|---|---|---|---|---|
| Objetivo | vago ou ausente | resultado principal identificado | objetivo observável e critérios claros | objetivo, limites e trade-offs explícitos |
| Reprodutibilidade | faltam passos ou contexto | procedimento básico registrado | versões, commit, entradas e saídas registrados | outra pessoa reproduz e confirma o resultado |
| Evidência | opinião sem suporte | artefato mínimo | múltiplas evidências coerentes | evidência independente ou teste adversarial |
| Engenharia | solução improvisada | contratos básicos | estados, falhas e interfaces explícitos | alternativas comparadas e decisão registrada |
| Segurança | segredo, privilégio ou ação perigosa | riscos básicos reconhecidos | least privilege e stop conditions aplicados | threat model, rollback e teste adversarial |
| Qualidade pedagógica | passivo ou confuso | explicação e exercício simples | prática ativa, feedback e progressão | engajamento, transferência e metacognição |
| Referências | inexistentes ou inventadas | ao menos uma fonte adequada | fontes primárias, links e data de acesso | triangulação, versão e limites da evidência |
| Comunicação | difícil de entender | compreensível | clara, acessível e estruturada | excelente síntese visual e textual |
| Internacionalização | texto rígido ou IDs instáveis | estrutura traduzível | IDs estáveis e termos controlados | paridade verificada entre idiomas |
| Reflexão | não reconhece limites | lista limitações | prioriza melhorias | mede impacto e propõe próximo experimento |

## Regras de aprovação

- Média mínima para conclusão de módulo: **1,5**.
- Média mínima para selo Premium Elite: **2,5**.
- Nota zero em segurança ou rastreabilidade reprova a entrega, independentemente da média.
- Alegações sem fonte não podem receber nível 3 em evidência.
- Imagens sem licença/proveniência e texto alternativo bloqueiam publicação.

## Registro recomendado

```yaml
rubric_id: course.rubric.transversal
artifact_id: <id>
reviewer: <humano-ou-agente>
reviewed_at: YYYY-MM-DD
scores:
  objective: 0
  reproducibility: 0
  evidence: 0
  engineering: 0
  security: 0
  pedagogy: 0
  references: 0
  communication: 0
  i18n: 0
  reflection: 0
blocking_findings: []
next_action: <ação concreta>
```
