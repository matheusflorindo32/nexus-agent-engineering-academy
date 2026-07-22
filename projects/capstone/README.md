---
id: project.capstone
title: Capstone production-grade
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 30–60h
---

# Capstone production-grade

## Missão

Resolver um processo real delimitado, com owner e usuários identificados, usando IA apenas onde a incerteza justificar. O piloto deve operar em sandbox, com dados permitidos, efeitos simulados ou reversíveis e caminho manual.

## Resultado final observável

A equipe deve entregar e defender um sistema que:

- possui requisitos, non-goals e baseline rastreáveis;
- executa um vertical slice local sem segredo obrigatório;
- separa control, data, state e observability plane;
- restringe autoridade e tools por contrato;
- avalia resposta, trajetória, custo, latência e segurança;
- bloqueia release diante de hard gates;
- observa, pausa, reconcilia, reverte e encerra;
- sobrevive ao LAB-1201 com invariantes preservadas;
- pode ser reproduzido por pessoa diferente do autor.

## Gates

1. **Discovery:** problema, owner, usuários, baseline, dados, critérios e non-goals aprovados.
2. **Architecture:** ADRs, diagramas, threat model, contratos, SLOs e fronteiras revisados.
3. **Vertical slice:** caminho ponta a ponta executável com fake tools, estado e avaliação.
4. **Hardening:** least privilege, approval binding, isolamento, idempotência, observabilidade e testes adversariais.
5. **Operational readiness:** canary, abort criteria, kill switch, rollback, restore e runbooks demonstrados.
6. **Game day:** LAB-1201 executado com postmortem e regressões.
7. **Independent reproduction:** terceiro reproduz demo e casos críticos.
8. **Defense:** evidências, custos, limites, risco residual e decisão final defendidos.

## Entregáveis obrigatórios

- brief e matriz de rastreabilidade;
- código ou workflow reproduzível;
- arquitetura e ADRs;
- threat model e inventário de capabilities;
- dataset permitido, versionado e protegido;
- evaluation report baseline/candidato;
- contratos de contexto, tools, loops, memória e automação;
- logs, traces, métricas e eventos redigidos;
- SLI, SLO, alertas e runbooks;
- release manifest, rollout e rollback;
- evidência do game day;
- postmortem e casos de regressão;
- inventário de dependências e SBOM quando aplicável;
- custos, limitações, riscos residuais e roadmap;
- apresentação e evidence bundle.

## Hard gates

```yaml
critical_policy_violations: 0
cross_tenant_leaks: 0
secrets_persisted: 0
unauthorized_effects: 0
duplicate_effects: 0
blind_retries_after_unknown_effect: 0
critical_events_lost: 0
kill_switch_failures: 0
incomplete_rollbacks: 0
untreated_high_or_critical_risks: 0
```

Qualquer hard gate falho resulta em `no-go`, independentemente da média.

## Rubrica específica

| Dimensão | Peso | Gate crítico |
|---|---:|---|
| Problema e evidência | 10% | baseline comparável e critérios rastreáveis |
| Arquitetura e engenharia | 20% | contratos, ADRs e estados explícitos |
| Qualidade e avaliação | 15% | regressões críticas bloqueiam release |
| Segurança e privacidade | 20% | zero autoridade indevida, vazamento ou segredo |
| Operação e resiliência | 15% | pause, reconcile, rollback e restore demonstrados |
| Observabilidade e auditoria | 10% | efeitos e decisões reconstruíveis |
| Comunicação e reprodução | 10% | terceiro reproduz sem orientação oral |

Use também a [rubrica transversal](../../course/rubrics/transversal-rubric.md). Segurança, privacidade, rastreabilidade e recuperação são bloqueadores.

## Decisão final

A defesa termina com uma decisão explícita:

- `no-go`: bloqueio crítico ou evidência insuficiente;
- `go-with-constraints`: piloto limitado, reversível e monitorado;
- `go`: somente para o escopo exato testado, sem alegação de prontidão irrestrita.

## Stop conditions

Interrompa imediatamente diante de sistema real fora do escopo, dado sensível, efeito irreversível não aprovado, isolamento rompido, kill switch inoperante, evidência crítica perdida ou risco além do blast radius autorizado.

## Limitações

A conclusão do capstone não constitui certificação profissional, conformidade jurídica ou garantia de segurança absoluta. Promoção para `stable` exige piloto real, revisão humana independente, acessibilidade, validação multiplataforma e aprovação explícita.