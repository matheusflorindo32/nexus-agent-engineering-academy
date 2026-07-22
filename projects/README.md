---
id: projects.index
title: Projetos NEXUS
lang: pt-BR
status: review
version: 0.2.0
---

# Projetos NEXUS

Projetos integram competências e geram portfólio auditável. Nenhum projeto é aprovado apenas por funcionar em uma demonstração feliz: a entrega precisa ser reproduzível, limitada, segura, observável e honesta sobre riscos residuais.

## Projetos disponíveis

| Projeto | Nível | Resultado principal |
|---|---|---|
| [Starter — triagem segura](starter-safe-triage/README.md) | inicial | comparar baseline determinístico e agente read-only |
| [Capstone production-grade](capstone/README.md) | final | defender sistema integrado com evidências, rollback e game day |

## Contrato obrigatório de projeto

Todo projeto deve declarar:

- problema, usuários e owner;
- requisitos e non-goals;
- baseline comparável;
- dados permitidos e proibidos;
- arquitetura e fronteiras de confiança;
- autoridade, tools e efeitos externos;
- critérios de sucesso e hard gates;
- dataset, versões e avaliação;
- segurança, privacidade e risco residual;
- observabilidade e correlação;
- operação, rollback, reconciliação e caminho manual;
- acessibilidade e instruções de reprodução;
- limitações conhecidas e próximo experimento.

## Fases e gates

1. **Discovery:** problema, baseline, dados, usuários e non-goals aprovados.
2. **Design:** contratos, arquitetura, threat model, avaliação e SLOs revisados.
3. **Vertical slice:** fluxo mínimo ponta a ponta executável com dados sintéticos.
4. **Hardening:** testes negativos, least privilege, observabilidade, idempotência e rollback.
5. **Independent reproduction:** outra pessoa reproduz usando somente a documentação.
6. **Defense:** demo, evidências, custos, limites, riscos residuais e decisão `go`, `no-go` ou `go-with-constraints`.

## Evidence bundle mínimo

- commit e versões de artefato, configuração, política, schema e dataset;
- instruções de execução local;
- requisitos e ADRs;
- threat model;
- resultados de avaliação por caso e agregados;
- traces, métricas e eventos redigidos;
- matriz de testes positivos, negativos e adversariais;
- prova de rollback, reconciliação ou limpeza;
- riscos residuais e limitações;
- revisão independente e registro da rubrica.

## Bloqueadores transversais

A entrega é bloqueada quando houver:

- segredo, dado pessoal real ou credencial de produção;
- vazamento entre tenants, sujeitos ou projetos;
- efeito externo não autorizado ou duplicado;
- autoridade definida pelo modelo;
- retry cego após efeito desconhecido;
- hard gate compensado por média;
- evidência não reproduzível;
- risco crítico ou alto sem tratamento e owner;
- ausência de caminho manual para ação sensível;
- alegação de segurança, conformidade ou prontidão absoluta.

## Aprovação

Use a [rubrica transversal](../course/rubrics/transversal-rubric.md) e o [gate Premium Elite de projetos](PROJECTS_PREMIUM_ELITE_GATE.md). O status permanece `review` até piloto real, revisão humana, acessibilidade e reprodução independente.