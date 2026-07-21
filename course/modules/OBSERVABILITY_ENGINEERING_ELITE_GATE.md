---
id: course.gate.observability-engineering-elite
title: Gate Premium Elite — Observability Engineering
lang: pt-BR
status: review
---

# Gate Premium Elite — Observability Engineering

Este gate define as condições mínimas para promover o Módulo 10 de `review` para `stable`.

## Bloqueios absolutos

A promoção é proibida quando existir qualquer um dos itens abaixo:

- segredo, token, credencial ou PII persistidos indevidamente;
- efeito sensível sem evento de auditoria íntegro;
- evento crítico descartado por sampling;
- correlação incapaz de reconstruir o caminho causal;
- label de alta cardinalidade em métrica de produção;
- collector indisponível sem degradação segura;
- perda de telemetria crítica não detectada;
- alerta crítico sem owner ou runbook;
- retenção indefinida sem justificativa;
- vazamento entre tenants;
- risco crítico ou alto sem mitigação e aprovação humana.

## Evidências técnicas obrigatórias

- [ ] IDs opacos e correlacionados de request a effect.
- [ ] Schema de evento versionado e validado.
- [ ] Redaction ocorre antes da persistência.
- [ ] Labels de alta cardinalidade são recusadas.
- [ ] Eventos críticos são preservados em 100%.
- [ ] Sampling e retenção possuem política versionada.
- [ ] Falhas de collector, fila cheia e schema incompatível são testadas.
- [ ] Efeitos órfãos e spans críticos ausentes são detectados.
- [ ] Alertas incluem impacto, owner, runbook e condição de resolução.
- [ ] Auditoria permite reconstruir decisão, aprovação e efeito.
- [ ] CI está verde no SHA final.

## Evidências pedagógicas obrigatórias

- [ ] Diagnóstico inicial e final aplicados.
- [ ] LAB-1001 executado por pessoa diferente do autor.
- [ ] Prática guiada e independente reproduzidas sem informação tácita.
- [ ] Estudantes diferenciaram logs, traces, métricas e auditoria.
- [ ] Testes negativos foram compreendidos e reproduzidos.
- [ ] Rubrica de quatro níveis aplicada de forma consistente.
- [ ] Dificuldades recorrentes e pedidos de ajuda registrados.

## Validação multiplataforma

- [ ] Windows.
- [ ] Linux.
- [ ] macOS.
- [ ] Python 3.11 ou superior.
- [ ] Execução local sem rede, API ou segredo.

## Acessibilidade

- [ ] Diagramas possuem descrição textual.
- [ ] Dashboards e alertas não dependem apenas de cor.
- [ ] Tabelas possuem cabeçalhos claros.
- [ ] Exemplos estão disponíveis como texto copiável.
- [ ] Estrutura de títulos é navegável por leitor de tela.
- [ ] Conteúdo audiovisual futuro possui legenda e transcrição.

## Segurança, privacidade e governança

- [ ] Revisão humana de segurança concluída.
- [ ] Revisão de privacidade e retenção concluída.
- [ ] Revisão técnica concluída.
- [ ] Revisão pedagógica concluída.
- [ ] Acesso a telemetria sensível é rastreável.
- [ ] Riscos residuais estão documentados.
- [ ] Nenhuma alegação de segurança absoluta foi feita.

## Métricas mínimas

O relatório de validação deve incluir:

- trace completeness rate;
- orphan effect rate;
- audit event missing rate;
- duplicate event rate;
- schema rejection rate;
- telemetry drop rate;
- secret exposure rate;
- cross-tenant leakage rate;
- alert actionability rate;
- custo de observabilidade por execução.

## Regra de promoção

O módulo só pode ser promovido para `stable` quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. as evidências técnicas, pedagógicas e de acessibilidade estiverem anexadas;
3. a suíte negativa e a simulação de falha do collector forem reproduzíveis;
4. revisões humanas estiverem registradas;
5. o CI estiver verde no mesmo SHA aprovado;
6. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.