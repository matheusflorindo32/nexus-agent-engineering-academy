---
id: lab.601.governed-multi-agent-coordination
title: LAB-601 — Coordenação multiagente governada
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 5h
---

# LAB-601 — Coordenação multiagente governada

## Hipótese

Contratos explícitos de papel, autoridade, contexto e terminação permitem obter os benefícios de especialização sem aceitar ciclos, vazamento ou ampliação de privilégios.

## Missão

Construir um sistema supervisor–workers local, reproduzível e sem API externa, provar sua governança sob falhas injetadas e comparar o resultado com uma solução de agente único.

## Arquitetura mínima

- `supervisor`: recebe a tarefa, decompõe e delega;
- `researcher`: produz fatos com proveniência local;
- `writer`: produz o artefato usando apenas fatos autorizados;
- `reviewer`: valida schema, cobertura e políticas;
- `approver`: papel humano simulado para efeitos sensíveis.

Cada papel deve declarar capacidades, entradas, saídas, escopo, budgets, ferramentas e proibições.

## Cenários obrigatórios

| ID | Condição injetada | Resultado obrigatório |
|---|---|---|
| M1 | tarefa válida com três papéis | `complete` com trace íntegro |
| M2 | destino de delegação não registrado | rejeição antes da execução |
| M3 | worker solicita ferramenta não autorizada | `authority_violation` |
| M4 | agente tenta delegar de volta ao remetente | `cycle_detected` |
| M5 | número máximo de handoffs atingido | `budget_exhausted` |
| M6 | contexto de outro tenant é anexado | `scope_violation` |
| M7 | saída do writer viola schema | revisão falha sem efeito externo |
| M8 | researcher falha após produzir um artefato válido | recuperação preserva o artefato |
| M9 | reviewer aprova sem evidência suficiente | decisão rejeitada pelo supervisor |
| M10 | efeito sensível sem aprovação humana | `approval_required` |
| M11 | payload do handoff muda após assinatura | `integrity_failure` |
| M12 | multiagente custa mais sem ganho de qualidade | recomendação de arquitetura simples |

## Contratos mínimos

```yaml
supervisor:
  may_delegate: [researcher, writer, reviewer]
  may_execute_external_effects: false
  max_handoffs: 6
researcher:
  may_delegate: []
  allowed_tools: [local_reference_index]
writer:
  may_delegate: [reviewer]
  allowed_tools: []
reviewer:
  may_delegate: []
  may_approve_external_effects: false
```

## Procedimento

1. Registre os agentes em um catálogo imutável.
2. Modele `Task`, `AgentContract`, `Delegation`, `Handoff`, `Artifact` e `RunReport`.
3. Restrinja toda mensagem por `tenant_id`, `project_id`, `run_id` e `delegation_id`.
4. Assine o payload do handoff com SHA-256.
5. Valide destino, capacidade, autoridade e schema antes da execução.
6. Mantenha o grafo de delegações e rejeite ciclos.
7. Persista artefatos válidos separadamente do estado transitório.
8. Injete os doze cenários obrigatórios.
9. Execute a mesma tarefa em modo agente único.
10. Compare qualidade, custo abstrato, latência em passos, handoffs e falhas.

## Métricas

| Métrica | Meta |
|---|---:|
| cenários com resultado correto | 12/12 |
| ampliações de privilégio aceitas | 0 |
| vazamentos de escopo | 0 |
| ciclos não detectados | 0 |
| efeitos sem aprovação | 0 |
| handoffs sem integridade verificável | 0 |
| artefatos válidos perdidos após falha parcial | 0 |
| relatórios com grafo e razão terminal | 100% |

## Comandos

```bash
python examples/governed_multi_agent_orchestrator.py --self-test
python tests/validate_repository.py
```

## Evidências

- catálogo de contratos;
- grafo de delegação por cenário;
- logs estruturados;
- hashes dos handoffs;
- artefatos válidos antes e depois de falhas;
- relatório terminal dos doze cenários;
- comparação agente único versus multiagente;
- reflexão sobre custo de coordenação.

## Testes adversariais

- inserir instrução maliciosa em um artefato do researcher;
- trocar `tenant_id` durante o handoff;
- solicitar ampliação de `max_handoffs` dentro da tarefa;
- registrar dois agentes com o mesmo `agent_id`;
- reutilizar `delegation_id` com payload diferente;
- forjar aprovação humana;
- criar cadeia `A → B → C → A`;
- provocar timeout após artefato válido;
- fazer dois agentes escreverem o mesmo recurso;
- induzir consenso sem evidência independente.

## Critérios de aprovação

O laboratório é aprovado somente quando:

- todos os cenários terminam de modo determinístico;
- nenhum agente atua fora do contrato;
- nenhuma mensagem cruza escopo;
- ciclos e budgets são observáveis;
- falhas parciais não apagam trabalho válido;
- efeitos sensíveis permanecem bloqueados sem aprovação;
- a comparação arquitetural não assume que multiagente é sempre superior.

## Stop conditions

Interrompa imediatamente se houver vazamento entre tenants, execução de ferramenta não concedida, efeito externo sem aprovação, alteração não detectada de handoff, ciclo além do limite ou perda de artefato já confirmado.