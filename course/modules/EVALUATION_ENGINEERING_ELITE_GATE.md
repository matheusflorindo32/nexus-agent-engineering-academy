---
id: course.gate.evaluation-engineering-elite
title: Gate Premium Elite — Evaluation Engineering
lang: pt-BR
status: review
---

# Gate Premium Elite — Evaluation Engineering

Este gate define as condições mínimas para promover o Módulo 07 de `review` para `stable`.

## Bloqueios absolutos

A promoção é proibida quando existir:

- hard gate compensável por média;
- falha nova em caso crítico;
- holdout contaminado ou usado para ajuste;
- baseline e candidato em condições não equivalentes;
- grader por modelo sem calibração e versão fixada;
- segredo ou dado sensível desnecessário no dataset ou relatório;
- trajetória insegura classificada como sucesso apenas pela resposta final;
- caso flaky removido ou ocultado sem justificativa;
- decisão de release irreproduzível;
- risco crítico ou alto sem tratamento e revisão humana.

## Evidências técnicas obrigatórias

- [ ] Dataset possui versão, schema, proveniência e partições.
- [ ] Todos os casos possuem ID, severidade, tags e objetivo.
- [ ] Development, validation, regression, holdout e adversarial estão separados.
- [ ] Baseline e candidato executam sob condições equivalentes.
- [ ] Graders determinísticos são usados quando aplicáveis.
- [ ] Graders heurísticos e por modelo têm limitações documentadas.
- [ ] Concordância e estabilidade dos graders são medidas.
- [ ] Variância e flakiness são registradas.
- [ ] Trajetória, efeitos e razão terminal são avaliados.
- [ ] Hard gates bloqueiam release corretamente.
- [ ] Relatórios por caso e agregados são reproduzíveis.
- [ ] CI está verde no SHA final.

## Evidências pedagógicas obrigatórias

- [ ] Diagnóstico inicial e final aplicados.
- [ ] LAB-701 executado por pessoa diferente do autor.
- [ ] Estudantes conseguem explicar por que uma média pode enganar.
- [ ] Pelo menos um release é bloqueado corretamente no exercício.
- [ ] Prática guiada e independente foram concluídas.
- [ ] Rubrica de quatro níveis foi aplicada de forma consistente.
- [ ] Dificuldades e pedidos de ajuda foram registrados.

## Validação multiplataforma

- [ ] Windows.
- [ ] Linux.
- [ ] macOS.
- [ ] Python 3.11 ou superior.
- [ ] Execução local sem rede, API ou segredo.

## Acessibilidade

- [ ] Diagramas possuem descrição textual.
- [ ] Tabelas possuem cabeçalhos claros.
- [ ] Gráficos possuem alternativa tabular.
- [ ] Aprovação e falha não dependem apenas de cor.
- [ ] Relatórios são navegáveis por leitor de tela.
- [ ] Exemplos são copiáveis em texto.

## Governança e honestidade

- [ ] Revisão técnica concluída.
- [ ] Revisão pedagógica concluída.
- [ ] Revisão humana de segurança concluída.
- [ ] Integridade e exposição do holdout foram revisadas.
- [ ] Riscos residuais e lacunas de cobertura estão documentados.
- [ ] Nenhuma alegação de segurança absoluta foi feita.
- [ ] Nenhuma conformidade normativa foi alegada sem base licenciada e revisão aplicável.

## Métricas mínimas

O relatório de validação deve incluir:

- case pass rate;
- critical pass rate;
- task success rate;
- groundedness rate;
- policy violation rate;
- regression count;
- flaky case rate;
- grader disagreement rate;
- custo por sucesso;
- p50, p95 e p99 de latência;
- cobertura por dimensão e severidade.

## Regra de promoção

O módulo só pode ser promovido para `stable` quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. as evidências técnicas, pedagógicas e de acessibilidade estiverem anexadas;
3. o holdout estiver protegido e sem contaminação conhecida;
4. hard gates e decisões de release forem reproduzíveis;
5. revisões humanas estiverem registradas;
6. o CI estiver verde no mesmo SHA aprovado;
7. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.