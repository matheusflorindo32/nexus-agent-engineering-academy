---
id: lab.1101.idempotent-automation
title: LAB-1101 — Automação idempotente e compensável
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 6h
risk_level: high-controlled
module: course.module.11-automation
---

# LAB-1101 — Automação idempotente e compensável

## Hipótese

Um workflow orientado a eventos com estado explícito, chave idempotente, ledger de efeitos, controle de concorrência, retry limitado, reconciliação e compensação auditável processa reentregas e falhas parciais sem duplicar efeitos nem ampliar autoridade.

## Missão

Construir uma automação local que recebe eventos repetidos ou concorrentes, usa agente somente em decisão ambígua, exige aprovação vinculada ao artefato exato e mantém trilha completa entre evento, decisão, aprovação, tentativa, efeito, reconciliação e compensação.

## Resultado observável

A entrega deve provar:

```text
múltiplas entregas
→ uma decisão lógica
→ no máximo um efeito externo simulado
→ estado terminal tipado
→ reconciliação verificável
```

## Pré-requisitos

- concluir o Módulo 11;
- executar apenas com dados e efeitos simulados;
- não usar conta, webhook ou credencial real;
- registrar commit, runtime, seed e sistema operacional;
- ler o [gate Premium Elite dos laboratórios](LABS_PREMIUM_ELITE_GATE.md).

## Baseline

Implemente primeiro uma versão ingênua:

- sem ledger;
- retry imediato após timeout;
- chave baseada apenas no ID da tentativa;
- sem lock ou compare-and-set;
- aprovação genérica;
- ausência de reconciliação.

Execute reentrega e concorrência e registre efeitos duplicados, estados ambíguos e lacunas de auditoria. Depois compare com a versão governada.

## Contrato mínimo

```yaml
workflow_schema: nexus.automation.v2
identity:
  tenant_id: trusted_context
  actor_id: trusted_context
idempotency:
  key: required
  payload_hash: canonical
  effect_ledger: append_only
  conflicting_payload: reject
concurrency:
  lock_scope: tenant_and_idempotency_key
  lease: bounded
retries:
  attempts: bounded
  backoff: exponential_with_jitter
  retryable_errors: explicit
  dead_letter: required
approval:
  bind: [tenant_id, action, canonical_payload_hash, policy_version, expires_at]
reconciliation:
  required_for: [effect_unknown, late_success, crash_after_effect]
compensation:
  idempotency_key: required
  preconditions: required
observability:
  correlation: [event_id, workflow_id, decision_id, approval_id, attempt_id, effect_id]
```

## Máquina de estados

Use estados tipados:

```text
received
→ validated
→ planned
→ awaiting_approval
→ executing
→ effect_unknown
→ reconciling
→ confirmed | compensated | dead_lettered | stopped
```

Transições inválidas devem ser recusadas e auditadas.

## Cenários obrigatórios

| ID | Condição | Resultado esperado |
|---|---|---|
| A1 | evento único válido | um efeito confirmado |
| A2 | mesma chave reentregue | resultado anterior reutilizado |
| A3 | duas execuções concorrentes | apenas uma adquire direito ao efeito |
| A4 | payload divergente com mesma chave | conflito rejeitado |
| A5 | timeout antes do efeito | retry permitido conforme política |
| A6 | timeout após possível efeito | `effect_unknown` e reconciliação antes de retry |
| A7 | sucesso tardio após timeout | ledger reconciliado sem duplicação |
| A8 | crash após efeito antes do commit local | retomada consulta destino e ledger |
| A9 | aprovação ausente | efeito bloqueado |
| A10 | aprovação expirada | efeito bloqueado |
| A11 | payload alterado após aprovação | hash divergente e bloqueio |
| A12 | dependência indisponível | retries limitados e DLQ |
| A13 | mensagem venenosa | quarentena ou DLQ com owner |
| A14 | compensação possível | reversão executada uma única vez |
| A15 | compensação impossível | escalonamento manual com evidência |
| A16 | agente indisponível | caminho determinístico ou manual seguro |
| A17 | agente tenta mudar tenant ou destino | tentativa recusada |
| A18 | replay fora da retenção | rejeição ou exceção formal aprovada |

## Procedimento

1. execute e meça o baseline;
2. modele máquina de estados e invariantes;
3. normalize o payload antes do hash;
4. implemente ledger append-only;
5. controle concorrência por tenant e chave idempotente;
6. vincule aprovação ao payload, ação, tenant, política e expiração;
7. injete os dezoito cenários;
8. trate timeout mutável como estado desconhecido;
9. reconcilie por `effect_id` ou chave idempotente;
10. implemente DLQ com owner, razão e política de reprocessamento;
11. implemente compensação idempotente;
12. compare baseline e versão governada;
13. produza relatório de invariantes e risco residual.

## Métricas obrigatórias

```yaml
duplicate_effect_count: 0
conflicting_payload_success_count: 0
blind_retry_count: 0
unapproved_sensitive_effect_count: 0
unreconciled_unknown_effect_count: 0
duplicate_compensation_count: 0
dlq_without_owner_count: 0
terminal_state_coverage_rate: 1.0
```

Toda taxa deve declarar numerador, denominador e população avaliada.

## Testes negativos e adversariais

- variar ordem de chaves sem alterar semântica;
- reutilizar chave com payload diferente;
- expirar lock durante chamada externa;
- interromper entre efeito e persistência;
- falsificar aprovação;
- reutilizar aprovação em outro tenant;
- saturar retries concorrentes;
- enviar sucesso tardio após compensação;
- alterar policy version no meio da execução;
- pedir ao agente para ampliar retries ou mudar destino;
- reprocessar item da DLQ sem owner;
- compensar duas vezes.

## Evidências obrigatórias

- diagrama de estados;
- manifesto de versões;
- baseline e comparação final;
- ledger antes e depois dos cenários;
- prova de efeito único sob concorrência;
- logs correlacionados e redigidos;
- registro de aprovação válida e inválida;
- conteúdo sanitizado da DLQ;
- reconciliação de `effect_unknown`;
- compensação bem-sucedida e impossível;
- relatório de riscos residuais.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários corretos | 18/18 |
| efeitos duplicados | 0 |
| conflitos silenciosos | 0 |
| retries cegos | 0 |
| efeitos sensíveis sem aprovação válida | 0 |
| estados desconhecidos sem reconciliação | 0 |
| compensações duplicadas | 0 |
| itens de DLQ sem owner | 0 |
| reprodução independente | aprovada |

Hard gates prevalecem sobre qualquer média ou taxa agregada.

## Troubleshooting

| Sintoma | Verificação segura |
|---|---|
| efeito duplicado | confira escopo da chave e atomicidade do ledger |
| lock expirando cedo | revise lease e duração máxima da chamada |
| timeout ambíguo | consulte destino antes de repetir |
| DLQ crescendo | classifique causas, owner e política de reprocessamento |
| compensação falha | confirme precondições e idempotência própria |
| aprovação rejeitada | recalcule hash canônico e validade |

Nunca resolva uma falha desativando idempotência, aprovação ou reconciliação.

## Acessibilidade

- diagramas devem possuir descrição textual;
- estados e severidades não podem depender apenas de cor;
- logs e relatórios precisam ser navegáveis por teclado;
- comandos devem ser copiáveis;
- decisões e razões terminais devem aparecer em texto simples.

## Reprodução independente

Outra pessoa deve reproduzir A2, A3, A6, A8, A11 e A14 usando somente documentação e artefatos. Divergências devem virar correções ou limitações registradas.

## Limpeza e rollback

- encerre workers e locks;
- esvazie filas temporárias;
- preserve somente evidências sanitizadas;
- confirme ausência de efeitos pendentes;
- restaure o estado simulado inicial;
- registre itens não reconciliados, caso existam.

## Rubrica específica

| Nível | Evidência |
|---|---|
| insuficiente | reentrega ou concorrência pode duplicar efeito |
| funcional | fluxo normal e retries limitados funcionam |
| robusto | concorrência, timeout, DLQ, reconciliação e compensação são demonstrados |
| excelente | reprodução independente, acessibilidade e comparação com baseline comprovam governança completa |

## Stop conditions

Interrompa imediatamente se houver efeito duplicado, conflito de payload tratado como sucesso, retry cego, efeito sensível sem aprovação válida, perda de correlação, compensação não idempotente, vazamento entre tenants ou DLQ sem owner.

## Limitações

O laboratório usa efeitos simulados e não prova comportamento idêntico em fornecedores externos. Semânticas de timeout, idempotência e compensação precisam ser revalidadas em cada integração real antes de produção.