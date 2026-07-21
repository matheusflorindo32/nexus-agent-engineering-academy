---
id: course.gate.production-architecture-elite
title: Gate Premium Elite — Production Architecture
lang: pt-BR
status: review
---

# Gate Premium Elite — Production Architecture

Este gate define as condições mínimas para promover o Módulo 09 de `review` para `stable`.

## Bloqueios absolutos

A promoção é proibida quando existir qualquer um dos itens abaixo:

- readiness aprova serviço com política, schema ou configuração incompatível;
- rollout sem abort criteria;
- rollback restaura apenas código;
- migração pode corromper estado sem plano de recuperação;
- fila pode duplicar efeito externo;
- degradação amplia privilégio;
- restore de backup não foi testado;
- kill switch não funciona;
- efeito ambíguo não é reconciliado;
- incidente não possui owner, contenção ou evidência;
- risco crítico ou alto sem mitigação e aprovação humana.

## Evidências técnicas obrigatórias

- [ ] Control, data, state e observability plane estão separados.
- [ ] Artefato, configuração, política e schema são versionados.
- [ ] Liveness, readiness, startup e deep health foram testados.
- [ ] SLI, SLO e error budget estão definidos e medidos.
- [ ] Hard gates prevalecem sobre error budget.
- [ ] Canary executa expansão e abort automático.
- [ ] Rollback completo foi reproduzido.
- [ ] Migração de estado possui compatibilidade e validação.
- [ ] Filas usam idempotência, DLQ, retries limitados e backpressure.
- [ ] Degradação segura não amplia autoridade.
- [ ] Restore foi concluído dentro do RTO declarado.
- [ ] Telemetria correlaciona rollout, execução e efeitos.
- [ ] CI está verde no SHA final.

## Evidências pedagógicas obrigatórias

- [ ] Diagnóstico inicial e final foram aplicados.
- [ ] LAB-901 foi executado por pessoa diferente do autor.
- [ ] O estudante diferenciou corretamente liveness e readiness.
- [ ] O estudante executou canary, abort e rollback.
- [ ] O estudante demonstrou restore e reconciliação.
- [ ] Testes negativos foram compreendidos e reproduzidos.
- [ ] Rubrica específica foi aplicada consistentemente.
- [ ] Dificuldades recorrentes foram registradas.

## Validação multiplataforma

- [ ] Windows.
- [ ] Linux.
- [ ] macOS.
- [ ] Python 3.11 ou superior.
- [ ] Execução local sem rede, API ou segredo.

## Acessibilidade

- [ ] Diagramas possuem descrição textual.
- [ ] Tabelas possuem cabeçalhos claros.
- [ ] Estados não dependem apenas de cor.
- [ ] Exemplos estão disponíveis como texto copiável.
- [ ] Estrutura de títulos é navegável.
- [ ] Conteúdo audiovisual futuro possui legenda e transcrição.

## Segurança e governança

- [ ] Revisão humana de segurança concluída.
- [ ] Revisão de privacidade concluída.
- [ ] Revisão técnica concluída.
- [ ] Revisão pedagógica concluída.
- [ ] Riscos residuais estão documentados.
- [ ] Nenhuma alegação de segurança absoluta ou conformidade jurídica foi feita.
- [ ] Incidentes simulados geraram casos de regressão.

## Métricas mínimas

O relatório de validação deve incluir:

- disponibilidade;
- task success rate;
- p50, p95 e p99 de latência;
- custo por execução e por sucesso;
- rollback time;
- restore time;
- checkpoint recovery success;
- duplicate effect rate;
- queue retry rate;
- canary abort rate;
- incident detection e containment time.

## Regra de promoção

O módulo só pode ser promovido para `stable` quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. as evidências técnicas, pedagógicas e de acessibilidade estiverem anexadas;
3. rollback e restore estiverem demonstrados;
4. revisões humanas estiverem registradas;
5. o CI estiver verde no mesmo SHA aprovado;
6. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.