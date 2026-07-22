---
id: lab.601.governed-multi-agent-coordination
title: LAB-601 — Coordenação multiagente governada
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 6h
risk_level: high-controlled
module: course.module.06-multi-agent-systems
---

# LAB-601 — Coordenação multiagente governada

> [!IMPORTANT]
> O laboratório não premia quantidade de agentes. Ele exige evidência de que a decomposição melhora especialização, isolamento ou revisão sem criar ciclos, vazamento, autoridade indevida ou custo de coordenação desproporcional.

## Hipótese

Contratos explícitos de papel, autoridade, contexto, integridade e terminação permitem obter benefícios de especialização sem aceitar ciclos, vazamento ou ampliação de privilégios.

## Missão

Construir um sistema supervisor–workers local, sem API externa, provar sua governança sob falhas injetadas e comparar o resultado com uma solução de agente único ou workflow determinístico.

## Resultado observável

Outra pessoa deve conseguir executar os cenários e confirmar:

- zero ampliação de autoridade;
- zero vazamento entre escopos;
- zero ciclo não detectado;
- zero efeito sensível sem aprovação;
- handoffs íntegros;
- preservação de artefatos válidos;
- recomendação arquitetural baseada em evidência.

## Pré-condições

- [Módulo 06](../course/modules/06-multi-agent-systems/README.md) concluído;
- Python 3.11+;
- dados e ferramentas exclusivamente locais;
- efeitos externos simulados;
- [gate dos laboratórios](LABS_PREMIUM_ELITE_GATE.md) lido.

## Baseline

Execute a mesma tarefa com um agente único ou workflow determinístico. Registre qualidade, passos, latência abstrata, custo, falhas e necessidade de revisão. A arquitetura multiagente só é recomendada quando demonstrar benefício líquido.

## Arquitetura mínima

- `supervisor`: recebe, decompõe, valida e encerra;
- `researcher`: produz fatos com proveniência local;
- `writer`: produz artefato com fatos autorizados;
- `reviewer`: verifica schema, cobertura e políticas;
- `approver`: papel humano simulado para efeitos sensíveis.

Cada papel declara capacidades, entradas, saídas, tenant, projeto, budgets, ferramentas, proibições e stop conditions.

## Contrato mínimo

```yaml
agent_id: reviewer
contract_version: 1
allowed_inputs: [draft.v1, evidence.v1]
allowed_outputs: [review_report.v1]
allowed_tools: []
permissions:
  read: [authorized_artifacts]
  write: [review_report]
forbidden:
  - executar efeito externo
  - alterar registro de agentes
  - ampliar budget
  - acessar outro tenant
budgets:
  max_steps: 4
  max_handoffs: 0
termination:
  success: review_complete
  stop: [schema_invalid, policy_violation, budget_exhausted]
```

## Invariantes

- somente agentes registrados podem executar;
- autoridade não pode ser ampliada pelo agente;
- tenant, projeto, run e delegation são obrigatórios;
- handoff transfere somente contexto necessário;
- payload alterado invalida integridade;
- grafo de delegação possui limite e detecção de ciclos;
- reviewer não executa o efeito que revisa;
- aprovação humana está vinculada ao artefato exato;
- falha parcial não apaga artefato confirmado;
- consensus não substitui evidência independente.

## Cenários obrigatórios

| ID | Condição injetada | Resultado obrigatório |
|---|---|---|
| A1 | tarefa válida com papéis registrados | `complete` com trace íntegro |
| A2 | destino não registrado | rejeição antes da execução |
| A3 | worker solicita tool não autorizada | `authority_violation` |
| A4 | agente delega de volta ao remetente | `cycle_detected` |
| A5 | máximo de handoffs atingido | `budget_exhausted` |
| A6 | contexto de outro tenant | `scope_violation` |
| A7 | saída viola schema | revisão falha sem efeito |
| A8 | worker falha após artefato válido | artefato preservado |
| A9 | reviewer aprova sem evidência | decisão recusada |
| A10 | efeito sensível sem aprovação | `approval_required` |
| A11 | handoff alterado após hash | `integrity_failure` |
| A12 | multiagente custa mais sem ganho | recomendar arquitetura simples |
| A13 | dois agentes escrevem o mesmo recurso | conflito detectado e arbitrado |
| A14 | aprovação forjada ou expirada | efeito bloqueado |
| A15 | agentes correlacionados concordam sem fonte | consenso insuficiente |

## Procedimento

1. Execute e registre o baseline simples.
2. Registre os agentes em catálogo imutável.
3. Modele `Task`, `AgentContract`, `Delegation`, `Handoff`, `Artifact` e `RunReport`.
4. Restrinja mensagens por tenant, projeto, run e delegation.
5. Calcule hash canônico dos handoffs.
6. Valide destino, capability, autoridade e schema antes da execução.
7. Mantenha grafo de delegações e detecte ciclos.
8. Separe artefatos confirmados de estado transitório.
9. Implemente arbitragem de conflito.
10. Execute os quinze cenários.
11. Compare baseline e multiagente.
12. Solicite reprodução independente de cinco cenários críticos.

## Testes adversariais

- inserir instrução indevida em artefato do researcher;
- trocar tenant durante handoff;
- solicitar ampliação de handoffs na própria tarefa;
- registrar agentes com o mesmo ID;
- reutilizar delegation ID com payload diferente;
- apresentar aprovação inválida;
- criar cadeia A → B → C → A;
- provocar timeout após artefato válido;
- fazer dois agentes escreverem o mesmo recurso;
- induzir consenso entre agentes não independentes;
- anexar contexto excessivo ao handoff;
- remover evidência desfavorável do trace.

## Métricas

| Métrica | Meta |
|---|---:|
| cenários corretos | 15/15 |
| ampliações aceitas | 0 |
| vazamentos de escopo | 0 |
| ciclos não detectados | 0 |
| efeitos sem aprovação | 0 |
| handoffs sem integridade | 0 |
| artefatos válidos perdidos | 0 |
| relatórios com grafo e razão terminal | 100% |
| coordination overhead | medido |
| benefício frente ao baseline | demonstrado ou arquitetura simples recomendada |
| cenários reproduzidos por outra pessoa | ≥ 5 |

## Comandos

```bash
python examples/governed_multi_agent_orchestrator.py --self-test
python tests/validate_repository.py
```

## Evidências

- baseline simples;
- catálogo versionado de contratos;
- grafo de delegação por cenário;
- logs estruturados;
- hashes dos handoffs;
- artefatos antes e depois de falhas;
- relatório terminal dos quinze cenários;
- matriz adversarial;
- comparação arquitetural;
- reprodução independente;
- risco residual.

## Critérios de aprovação

- 15/15 cenários terminam corretamente;
- nenhum agente atua fora do contrato;
- nenhuma mensagem cruza escopo;
- ciclos e budgets são observáveis;
- falhas parciais preservam trabalho válido;
- efeitos sensíveis ficam bloqueados sem aprovação válida;
- integridade de handoffs é verificada;
- conflitos possuem arbitragem explícita;
- comparação não presume superioridade multiagente;
- evidências permitem reconstrução causal.

## Rubrica específica

| Nível | Evidência |
|---|---|
| insuficiente | papéis vagos, ciclos, vazamento ou autoridade implícita |
| funcional | contratos e handoffs básicos funcionam |
| robusta | isolamento, integridade, falha parcial, arbitragem e budgets são comprovados |
| excelente | benefício líquido, reprodução independente, acessibilidade e riscos estão completos |

## Stop conditions

Interrompa imediatamente se houver vazamento entre tenants, tool não concedida, efeito sem aprovação, alteração não detectada de handoff, ciclo além do limite, perda de artefato confirmado ou agente capaz de ampliar a própria autoridade.

## Troubleshooting

| Sintoma | Verificação |
|---|---|
| tarefa circula entre agentes | inspecione grafo e max handoffs |
| worker recebe contexto excessivo | revise contrato de handoff |
| artefato desaparece após falha | separe armazenamento confirmado do estado transitório |
| consensus parece forte demais | avalie independência de modelos, dados e prompts |
| multiagente é mais lento | compare coordination overhead com baseline |

## Acessibilidade

- forneça descrição textual do grafo;
- não diferencie papéis apenas por cor;
- disponibilize contratos e traces em texto;
- use tabelas com cabeçalhos claros.

## Limpeza

Remova artefatos e traces simulados não necessários, preserve somente evidências redigidas e confirme que nenhuma execução permanece ativa.

## Limitações

O laboratório valida uma arquitetura local e cenários controlados. Não prova segurança absoluta, independência real entre modelos nem prontidão irrestrita para produção. O status permanece `review` até piloto e revisão humana.