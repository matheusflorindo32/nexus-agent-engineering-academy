---
id: projects.premium-elite-gate
title: Gate Premium Elite de projetos
lang: pt-BR
status: review
version: 0.1.0
---

# Gate Premium Elite de projetos

Este gate define a promoção de projetos NEXUS. Ele complementa requisitos específicos e a rubrica transversal.

## Evidências obrigatórias

- brief aprovado;
- baseline comparável;
- matriz de rastreabilidade;
- arquitetura, ADRs e threat model;
- contratos de autoridade, tools, estado e efeitos;
- dataset e graders versionados;
- testes positivos, negativos, adversariais e de regressão;
- observabilidade correlacionada e redigida;
- rollback, reconciliação e caminho manual;
- evidence bundle;
- reprodução independente;
- registro de rubrica e decisão humana.

## Hard gates

Bloqueie imediatamente diante de:

- segredo, credencial real ou dado pessoal não autorizado;
- cross-tenant, cross-subject ou cross-project leakage;
- efeito proibido, duplicado ou sem aprovação válida;
- autoridade ampliada pelo modelo ou conteúdo recuperado;
- retry cego após `effect_unknown`;
- hard gate ignorado por média;
- kill switch inoperante quando aplicável;
- rollback ou restore não demonstrado quando exigido;
- evento crítico perdido ou efeito sem correlação;
- evidência adulterada, incompatível ou não versionada;
- risco alto ou crítico sem tratamento, owner e decisão;
- ausência de reprodução independente;
- alegação de segurança ou conformidade absoluta.

## Revisões mínimas

- revisão técnica;
- revisão pedagógica;
- revisão de segurança e privacidade proporcional ao risco;
- revisão de acessibilidade;
- revisão por pessoa diferente do autor;
- CI verde no mesmo SHA da decisão.

## Critérios de promoção

### Starter concluído

- todos os cenários obrigatórios aprovados;
- hard gates verdes;
- média transversal ≥ 2,0;
- segurança e reprodutibilidade ≥ 2;
- execução local reproduzida.

### Premium Elite

- todas as dimensões ≥ 2;
- média transversal ≥ 2,5;
- pelo menos três dimensões no nível 3;
- comparação com alternativa simples;
- testes adversariais e regressão;
- reprodução independente;
- limitações e risco residual explícitos.

### Capstone apto para piloto

- gates Discovery–Defense concluídos;
- LAB-1201 executado;
- zero bloqueio crítico;
- rollout, abort, rollback, restore e caminho manual demonstrados;
- decisão humana `go-with-constraints` para escopo limitado;
- plano de monitoramento e encerramento do piloto.

## Condições para `stable`

O status `stable` permanece bloqueado até existir:

- piloto real com consentimento e escopo controlado;
- correções baseadas em dados do piloto;
- acessibilidade validada;
- execução multiplataforma;
- revisão humana documentada;
- integração ordenada dos PRs;
- CI verde na versão final;
- aprovação humana explícita.

## Registro de decisão

```yaml
project_id: <id>
project_commit: <sha>
gate_version: 0.1.0
reviewers: []
evidence_bundle: <path-ou-id>
hard_gates: pass | fail
rubric_average: 0.0
blocking_findings: []
residual_risks: []
decision: blocked | revise | approved_with_constraints | approved
scope_constraints: []
next_review: YYYY-MM-DD
```

CI verde não implica aprovação, merge ou prontidão para produção.