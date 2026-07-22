---
id: lab.901.production-readiness
title: LAB-901 — Production readiness, rollout e rollback
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 6h
risk_level: high-controlled
module: course.module.09-production-architecture
---

# LAB-901 — Production readiness, rollout e rollback

## Hipótese

Arquitetura com artefato imutável, configuração e política versionadas, health checks úteis, SLOs, canary e rollback completo reduz impacto de regressões e torna a operação agentic auditável e recuperável.

## Missão

Provar que um candidato só é promovido quando cumpre gates de qualidade, segurança, custo, latência e recuperação; e que o sistema retorna a um estado conhecido quando um gate falha.

## Resultado final observável

A entrega deverá demonstrar:

- release manifest completo;
- matriz de compatibilidade;
- health checks separados;
- baseline estável;
- rollout em estágios;
- abort criteria objetivos;
- rollback de código, configuração, política e estado;
- reconciliação de filas e efeitos;
- kill switch;
- restore testado;
- relatório de release e incidente reproduzíveis.

## Ambiente controlado

- execução local ou sandbox isolada;
- tráfego, filas, dependências e efeitos simulados;
- nenhuma credencial de produção;
- dados sintéticos;
- owner e operador identificados;
- janela máxima de 6 horas;
- kill switch testável antes do rollout.

## Release manifest mínimo

```yaml
release_id: rel-009
candidate_digest: sha256:candidate
previous_digest: sha256:stable
config_version: 17
policy_version: 12
schema_version: 5
model_route_version: 4
feature_flag_version: 8
migration_version: 3
rollout_percent: 5
slo:
  min_success_rate: 0.97
  max_p95_latency_ms: 2500
  max_cost_per_success: 0.08
  max_critical_policy_violations: 0
abort:
  max_error_budget_burn_rate: 2.0
  max_duplicate_effects: 0
  max_cross_scope_leaks: 0
```

## Health checks

Implemente e diferencie:

- `startup`: processo iniciou e carregou dependências mínimas;
- `liveness`: processo não está travado;
- `readiness`: versão, política, configuração e dependências permitem receber tráfego;
- `deep_health`: executa fluxo sintético sem efeito real e valida estado, policy e observabilidade.

Liveness verde não implica readiness.

## Baseline operacional

Registre para a versão estável:

- success rate;
- critical policy violations;
- p50 e p95 de latência;
- custo por sucesso;
- duplicate effect rate;
- queue depth;
- error budget burn;
- restore time;
- versões do release manifest.

## Cenários obrigatórios

| ID | Condição | Resultado esperado |
|---|---|---|
| P1 | artefato, política e configuração compatíveis | readiness `ready` |
| P2 | schema incompatível | readiness `blocked` |
| P3 | canary saudável em 5% | avanço para 25% |
| P4 | violação crítica de política | abort imediato e rollback |
| P5 | queda de sucesso acima do limite | abort e rollback |
| P6 | p95 acima do limite | rollout pausado ou revertido |
| P7 | custo por sucesso excessivo | candidato rejeitado |
| P8 | dependência indisponível | modo degradado read-only |
| P9 | rollback restaura apenas código | teste falha |
| P10 | rollback completo | estado anterior íntegro |
| P11 | backup não restaurável | readiness bloqueada |
| P12 | kill switch acionado | novos efeitos bloqueados |
| P13 | configuração muda durante execução | release invalidado |
| P14 | migração incompatível | promoção bloqueada |
| P15 | timeout após possível efeito | `effect_unknown` e reconciliação |
| P16 | mensagem duplicada na fila | um único efeito lógico |
| P17 | DLQ sem owner | readiness bloqueada |
| P18 | collector indisponível | telemetria degradada e mutações sensíveis suspensas |

## Procedimento

1. fixe versões de artefato, configuração, política, schema, flags e migração;
2. valide digest e matriz de compatibilidade;
3. execute startup, liveness, readiness e deep health;
4. registre baseline estável;
5. teste kill switch e restore antes do rollout;
6. inicie canary em 5%;
7. mantenha janela mínima de observação;
8. injete os dezoito cenários;
9. aplique abort criteria antes de ampliar tráfego;
10. execute rollback completo em falha;
11. reconcilie estado, filas e efeitos;
12. valide o estado anterior com deep health;
13. gere relatório de release e incidente;
14. solicite reprodução independente dos cenários críticos.

## Rollback completo

O rollback precisa coordenar:

```text
artefato
+ configuração
+ política
+ model route
+ feature flags
+ schema compatível
+ migração ou forward-fix
+ consumidores de fila
+ estado e checkpoints
```

Rollback somente de código é falha.

## Migrações

Toda migração deve declarar:

- origem e destino;
- compatibilidade backward/forward;
- estratégia expand/contract;
- backfill idempotente;
- validação antes e depois;
- rollback ou forward-fix;
- impacto em filas, memória e checkpoints.

Migração irreversível exige aprovação humana e contingência explícita.

## Filas e efeitos

Comprove:

- idempotency key;
- deduplicação;
- retry budget;
- visibility timeout;
- DLQ;
- owner de poison message;
- backpressure;
- reconciliação após timeout;
- efeito único sob reentrega concorrente.

## Métricas

| Métrica | Meta |
|---|---:|
| cenários corretos | 18/18 |
| promoção com violação crítica | 0 |
| rollback incompleto aceito | 0 |
| efeitos após kill switch | 0 |
| duplicate effect rate | 0 |
| cross-scope leak rate | 0 |
| restauração dentro do RTO simulado | 100% |
| relatórios com versões completas | 100% |
| segredos em logs | 0 |

## Evidências

- release manifest e hashes;
- matriz de compatibilidade;
- resultados dos quatro health checks;
- baseline e métricas por estágio;
- abort criteria e decisões;
- snapshots antes e depois;
- prova de rollback completo;
- prova de restore;
- ledger de efeitos e filas;
- prova de modo degradado;
- prova do kill switch;
- relatório de incidente;
- limitações e risco residual;
- reprodução independente.

## Critérios de aprovação

O laboratório só é aprovado quando:

- todos os cenários possuem terminal correto;
- hard gates críticos prevalecem sobre médias;
- rollout não avança sem janela e evidência;
- rollback restaura versões e estado compatíveis;
- timeout mutável não causa retry cego;
- efeitos permanecem idempotentes;
- restore ocorre dentro do RTO simulado;
- degradação não amplia privilégios;
- kill switch bloqueia mutações;
- outra pessoa reproduz rollback, kill switch e restore.

## Testes adversariais

- promover candidato com média boa e falha crítica;
- omitir versão da política;
- restaurar artefato antigo com schema incompatível;
- marcar readiness saudável sem deep health;
- ampliar rollout sem janela mínima;
- degradar ampliando permissão;
- executar efeito após kill switch;
- alterar feature flag fora do manifest;
- consumir fila com versão incompatível;
- ocultar retries no custo;
- aceitar backup sem restore;
- modificar abort criteria após observar falha.

## Troubleshooting

| Sintoma | Ação segura |
|---|---|
| readiness oscila | inspecione dependências, versões e deep health; não amplie rollout |
| rollback não estabiliza | suspenda tráfego, reconcilie estado e avalie forward-fix |
| fila cresce | aplique backpressure, limite retries e inspecione poison messages |
| telemetria falha | entre em modo degradado e suspenda mutações sensíveis |
| restore excede RTO | bloqueie readiness e revise backup, volume e procedimento |

## Stop conditions

Interrompa imediatamente se houver:

- violação crítica;
- efeito após kill switch;
- ampliação de privilégio durante degradação;
- configuração mutável durante execução;
- rollback não reconciliado;
- relatório sem versões completas;
- migração incompatível;
- retry cego após efeito desconhecido;
- backup não restaurável;
- uso de ambiente ou credencial real.

## Acessibilidade

- estados devem ter rótulos textuais;
- gráficos precisam de tabela equivalente;
- não use apenas cor em rollout ou incidentes;
- runbooks devem ser navegáveis por títulos;
- comandos e resultados devem ser copiáveis;
- diagramas precisam de descrição textual.

## Limpeza

Restaure o ambiente ao snapshot inicial, esvazie filas simuladas, invalide approval tokens e remova artefatos temporários. Preserve somente evidências redigidas e hashes.

## Rubrica

| Nível | Evidência |
|---|---|
| insuficiente | deploy manual sem gates ou rollback apenas de código |
| funcional | canary, abort e rollback básico funcionam |
| robusta | estado, migração, filas, restore e degradação são testados |
| excelente | reprodução independente e recuperação completa dentro dos objetivos |

## Limitações

O laboratório não equivale a certificação de produção. Ele produz evidência local sob cenários simulados e requer revisão humana, testes no ambiente-alvo e piloto controlado.

## Entrega Premium Elite

A entrega deve atender ao [gate transversal dos laboratórios](LABS_PREMIUM_ELITE_GATE.md) e permitir reconstruir toda decisão de promoção, pausa, rollback e recuperação.