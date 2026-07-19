---
id: lab.901.production-readiness
title: LAB-901 — Production readiness, rollout e rollback
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 5h
---

# LAB-901 — Production readiness, rollout e rollback

## Hipótese

Arquitetura com configuração versionada, health checks úteis, SLOs, canary e rollback completo reduz o impacto de regressões e torna a operação agentic auditável.

## Missão

Provar que um candidato só é promovido quando cumpre gates de qualidade, segurança, custo e latência; e que o sistema retorna ao estado anterior quando um gate falha.

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
| P8 | dependência externa indisponível | modo degradado read-only |
| P9 | rollback restaura apenas código | teste deve falhar |
| P10 | rollback completo | estado anterior íntegro |
| P11 | backup não restaurável | readiness operacional bloqueada |
| P12 | kill switch acionado | novos efeitos externos bloqueados |

## Contratos mínimos

```yaml
release_id: rel-009
candidate_digest: sha256:candidate
previous_digest: sha256:stable
config_version: 17
policy_version: 12
schema_version: 5
rollout_percent: 5
slo:
  min_success_rate: 0.97
  max_p95_latency_ms: 2500
  max_cost_per_success: 0.08
  max_critical_policy_violations: 0
```

## Procedimento

1. Valide artefato, configuração, política e schema.
2. Execute startup, liveness, readiness e deep health.
3. Registre baseline estável.
4. Inicie canary em 5%.
5. Injete os doze cenários.
6. Aplique abort criteria antes de ampliar tráfego.
7. Execute rollback completo em falha.
8. Reconcile estado, filas e efeitos.
9. Gere relatório de release.
10. Gere relatório de incidente quando aplicável.

## Evidências

- configuração e política versionadas;
- matriz de compatibilidade;
- resultados dos health checks;
- métricas por estágio do rollout;
- razão tipada de promoção, pausa ou rollback;
- snapshot antes e depois do rollback;
- prova de modo degradado;
- saída do autoteste;
- reflexão sobre limites.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários corretos | 12/12 |
| promoção com violação crítica | 0 |
| rollback incompleto aceito | 0 |
| efeitos após kill switch | 0 |
| restauração dentro do RTO simulado | 100% |
| relatórios com versões completas | 100% |
| segredos em logs | 0 |

## Testes adversariais

- alterar configuração no meio da execução;
- tentar promover candidato com média boa e uma violação crítica;
- omitir versão da política no relatório;
- restaurar artefato antigo com schema novo incompatível;
- marcar readiness como saudável sem deep health;
- aumentar rollout sem janela mínima;
- degradar ampliando permissão;
- executar efeito externo após kill switch.

## Comando

```bash
python examples/production_runtime.py --self-test
```

## Stop conditions

Interrompa imediatamente se houver violação crítica, efeito após kill switch, ampliação de privilégio durante degradação, configuração mutável dentro da execução, rollback não reconciliado ou relatório sem versões de artefato, política, configuração e schema.