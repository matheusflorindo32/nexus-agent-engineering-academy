---
id: course.module.06-multi-agent-systems
title: 06 — Multi-Agent Systems
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 14h
prerequisites: [course.module.05-memory-engineering]
learning_outcomes:
  - decidir quando um sistema multiagente é justificável
  - modelar papéis, autoridade, handoffs e contratos de contexto
  - prevenir ciclos, escalada indevida e vazamento entre agentes
  - avaliar coordenação por qualidade, custo, latência e segurança
---

# 06 — Multi-Agent Systems

> [!IMPORTANT]
> Mais agentes não significam mais inteligência. Um sistema multiagente só é justificável quando a decomposição melhora verificavelmente especialização, controle, paralelismo ou isolamento.

## Objetivos

- Diferenciar agente único com ferramentas, workflow determinístico e sistema multiagente.
- Definir papéis, capacidades, limites de autoridade e critérios de seleção.
- Projetar delegação, handoff, escalonamento e encerramento com contratos auditáveis.
- Isolar contexto e memória para reduzir vazamento, contaminação e ampliação de privilégios.
- Medir coordenação por resultado, custo, latência, conflitos, retrabalho e segurança.

## Pré-requisitos

[Módulo 05](../05-memory-engineering/README.md); contratos de agente, ferramentas seguras e memória governada.

## Quando usar múltiplos agentes

Use múltiplos agentes somente quando pelo menos uma condição puder ser demonstrada:

1. **especialização real** — papéis exigem políticas, ferramentas ou critérios distintos;
2. **isolamento** — dados ou permissões não podem coexistir no mesmo contexto;
3. **paralelismo útil** — tarefas independentes reduzem tempo total sem aumentar reconciliação de forma desproporcional;
4. **separação de funções** — quem propõe não deve aprovar ou executar;
5. **redução mensurável de complexidade** — o controlador fica mais simples e verificável.

Evite multiagentes quando um workflow, função ou máquina de estados resolver o problema com menos custo e menor superfície de falha.

## Padrões arquiteturais

| Padrão | Uso apropriado | Risco dominante |
|---|---|---|
| supervisor–workers | decomposição e controle central | supervisor como gargalo |
| pipeline especializado | sequência estável entre papéis | erro propagado entre etapas |
| debate/revisor | crítica e verificação independente | consenso falso e custo |
| router–specialists | seleção por tipo de tarefa | roteamento incorreto |
| blackboard | colaboração por estado compartilhado | contaminação e concorrência |
| swarm restrito | exploração paralela limitada | explosão de custo e ciclos |

## Contrato mínimo de agente

```yaml
agent_id: evidence_reviewer
role: revisar suporte e proveniência
inputs:
  schema: review_request.v1
outputs:
  schema: review_report.v1
allowed_tools:
  - local_reference_index
permissions:
  read: [task_context, cited_sources]
  write: [review_report]
forbidden:
  - alterar artefato final
  - delegar para agente não registrado
  - acessar memória de outro tenant
budgets:
  max_steps: 6
  max_handoffs: 2
  max_tool_calls: 4
termination:
  success: report_valid
  stop: [budget_exhausted, unsafe_request, cycle_detected]
```

O contrato deve tornar explícito o que o agente pode ler, produzir, delegar e executar. Descrições vagas de personalidade não substituem autoridade formal.

## Delegação

Uma delegação válida contém:

- identificador único;
- objetivo limitado;
- schema de entrada e saída;
- contexto mínimo necessário;
- prazo ou budget;
- autoridade concedida;
- critérios de sucesso;
- política de falha;
- cadeia de responsabilidade.

```json
{
  "delegation_id": "del-104",
  "from": "supervisor",
  "to": "evidence_reviewer",
  "objective": "verificar cinco afirmações",
  "context_refs": ["claim-set-7", "source-index-2"],
  "authority": ["read_sources", "write_review"],
  "max_handoffs": 1,
  "return_schema": "review_report.v1"
}
```

O agente delegado não pode ampliar seu próprio escopo, budget, ferramentas ou autoridade.

## Handoff seguro

Handoff não é copiar toda a conversa. Deve transferir um pacote mínimo e tipado:

- resumo factual;
- decisões confirmadas;
- incertezas;
- referências para artefatos;
- restrições e políticas;
- efeitos já realizados;
- próximo resultado esperado.

Todo handoff precisa de hash, versão e origem. Instruções presentes em conteúdo recuperado permanecem dados, não autoridade.

## Autoridade e separação de funções

A NEXUS recomenda separar:

- **planner** — propõe plano;
- **executor** — realiza ações autorizadas;
- **reviewer** — verifica resultado e políticas;
- **approver humano** — decide efeitos sensíveis.

Um agente não deve aprovar a própria ampliação de privilégio nem validar sozinho um efeito irreversível que ele mesmo propôs.

## Isolamento de contexto e memória

Cada mensagem deve declarar:

```text
tenant_id
project_id
run_id
agent_id
delegation_id
classification
provenance
```

O receptor deve receber somente o contexto necessário à sua função. Memória compartilhada precisa de namespace, política de escrita, TTL e trilha de auditoria. Estado privado de um agente não deve ser exportado automaticamente.

## Prevenção de ciclos

Ciclos surgem quando agentes delegam entre si sem redução mensurável do trabalho. Controles mínimos:

- `max_handoffs` global e por agente;
- grafo de delegação acíclico por padrão;
- detecção de aresta repetida;
- fingerprint do objetivo e do estado;
- budget de custo e tempo;
- stop condition `cycle_detected`;
- supervisor sem auto-delegação.

## Conflitos e reconciliação

Quando agentes discordam, o sistema deve preservar:

- propostas separadas;
- evidências de cada posição;
- critérios de decisão;
- agente ou humano responsável pela arbitragem;
- decisão final e justificativa.

Não use votação simples quando os agentes compartilham o mesmo modelo, dados ou viés. Diversidade aparente não equivale a independência.

## Falhas parciais

O orquestrador deve distinguir:

- agente indisponível;
- saída inválida;
- tarefa não suportada;
- política violada;
- timeout;
- conflito de estado;
- efeito ambíguo;
- resultado insuficiente.

Falha de um worker não implica reiniciar toda a execução. Reuse artefatos válidos, preserve idempotência e gere um plano de recuperação explícito.

## Observabilidade

Registre, no mínimo:

- grafo real de delegações;
- latência por agente;
- tokens ou custo por agente;
- número de handoffs;
- falhas e retries;
- mudanças de autoridade;
- acesso a contexto e memória;
- conflitos e decisões;
- razão terminal.

Métricas essenciais:

| Métrica | Interpretação |
|---|---|
| task success rate | resultado correto por execução |
| handoff efficiency | handoffs úteis / handoffs totais |
| coordination overhead | custo de coordenação / custo total |
| rework rate | tarefas repetidas por falha de contrato |
| authority violations | tentativas de exceder privilégios |
| context leakage rate | dados indevidos entregues a outro agente |
| cycle rate | execuções interrompidas por ciclo |

## Implementação de referência

Execute:

```bash
python examples/governed_multi_agent_orchestrator.py --self-test
```

A implementação local deve provar:

- roteamento apenas para agentes registrados;
- isolamento por tenant e projeto;
- delegação com autoridade limitada;
- rejeição de ampliação de privilégio;
- detecção de ciclo;
- limite de handoffs;
- validação de schema;
- falha parcial sem perda do estado válido;
- revisão independente antes de conclusão;
- relatório terminal auditável.

## Laboratório

- [LAB-601](../../../labs/LAB-601-governed-multi-agent-coordination.md) — construir e atacar uma coordenação multiagente governada.

## Projeto

Construa um sistema supervisor–workers que:

1. registre agentes por contrato;
2. roteie tarefas por capacidade declarada;
3. aplique escopo e least privilege;
4. transfira contexto mínimo por handoff;
5. limite ciclos, custo e delegações;
6. separe produção, revisão e aprovação;
7. tolere falha parcial;
8. gere trace completo e relatório terminal;
9. compare o resultado com uma solução de agente único.

## Quiz

1. Qual evidência justifica adotar múltiplos agentes?
2. Por que handoff não deve copiar toda a conversa?
3. Como impedir que um worker amplie autoridade?
4. Por que votação entre agentes pode produzir falsa confiança?
5. Qual métrica revela excesso de coordenação?

<details>
<summary>Gabarito comentado</summary>

1. Melhoria mensurável de especialização, isolamento, paralelismo, separação de funções ou complexidade.
2. Porque aumenta custo, vazamento, prompt injection e ambiguidade de autoridade.
3. Autoridade imutável no contrato, validação no orquestrador e rejeição de capacidades não concedidas.
4. Porque agentes semelhantes podem compartilhar modelo, dados e vieses, tornando votos correlacionados.
5. `coordination overhead`, complementada por handoffs, latência e retrabalho.

</details>

## Checklist

- [ ] Multiagentes demonstram vantagem sobre alternativa mais simples.
- [ ] Todo agente possui contrato, schema, budgets e permissões.
- [ ] Delegações têm objetivo, autoridade e retorno tipado.
- [ ] Handoffs transferem somente contexto necessário.
- [ ] Grafo de delegação possui controle de ciclos.
- [ ] Papéis de propor, executar, revisar e aprovar estão separados.
- [ ] Falhas parciais preservam artefatos válidos.
- [ ] Contexto e memória são isolados por tenant e projeto.
- [ ] Telemetria permite reconstruir decisões e acessos.
- [ ] Testes adversariais cobrem autoridade, ciclo, vazamento e schema.

## Critérios de excelência

| Dimensão | Padrão Premium Elite |
|---|---|
| Justificativa | ganho demonstrado frente a agente único/workflow |
| Governança | 100% dos agentes e delegações possuem contrato válido |
| Segurança | zero ampliação de privilégio e zero vazamento entre escopos |
| Terminação | ciclos e budgets encerram de forma determinística |
| Resiliência | falha parcial não duplica efeitos nem perde estado válido |
| Evidência | trace, métricas e relatório permitem auditoria completa |

## Bibliografia

WOOLDRIDGE, Michael. *An Introduction to MultiAgent Systems*. 2. ed. Wiley, 2009.

HUEBSCHER, Markus C.; MCCANN, Julie A. A survey of autonomic computing. *ACM Computing Surveys*, v. 40, n. 3, 2008.

## Referências

- NIST — AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- OWASP — Agentic AI Threats and Mitigations: https://genai.owasp.org/
- Microsoft — Multi-agent reference architecture: https://learn.microsoft.com/azure/architecture/ai-ml/guide/multi-agent-system

> [!WARNING]
> Frameworks podem facilitar mensagens e roteamento, mas não substituem contratos de autoridade, isolamento, terminação, avaliação e resposta a incidentes.

## Próximo passo

Conclua o LAB-601, compare contra uma arquitetura de agente único e registre evidências antes de avançar para Evaluation Engineering.
