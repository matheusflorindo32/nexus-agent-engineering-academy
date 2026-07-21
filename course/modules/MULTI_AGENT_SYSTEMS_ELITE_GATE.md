---
id: course.gate.multi-agent-systems-elite
title: Gate Premium Elite — Multi-Agent Systems
lang: pt-BR
status: review
---

# Gate Premium Elite — Multi-Agent Systems

Este gate define as condições mínimas para promover o Módulo 06 de `review` para `stable`.

## Bloqueios absolutos

A promoção é proibida quando existir qualquer um dos itens abaixo:

- ciclo de delegação sem interrupção determinística;
- auto-delegação não bloqueada;
- agente capaz de ampliar a própria autoridade;
- vazamento entre tenant, projeto, agente ou execução;
- handoff sem origem, destino, versão, classificação ou hash;
- efeito externo sem responsável identificável;
- falha parcial que duplique efeitos ou apague estado válido;
- trace incapaz de reconstruir decisões e acessos;
- alegação de vantagem multiagente sem comparação com baseline;
- risco crítico ou alto sem mitigação e aprovação humana.

## Evidências técnicas obrigatórias

- [ ] Todos os agentes possuem contratos versionados.
- [ ] O registro de capacidades é validado pelo orquestrador.
- [ ] Agentes não registrados são recusados.
- [ ] Budgets globais e locais são testados.
- [ ] Ciclos A → B → A e auto-delegação são detectados.
- [ ] Handoffs transferem somente contexto necessário.
- [ ] Isolamento por tenant e projeto apresenta leakage rate igual a zero na suíte local.
- [ ] Separação entre propor, executar, revisar e aprovar é demonstrada.
- [ ] Falha parcial preserva artefatos válidos.
- [ ] Efeito ambíguo exige reconciliação antes de nova mutação.
- [ ] Trace e relatório terminal são reproduzíveis.
- [ ] CI está verde no SHA final.

## Evidências pedagógicas obrigatórias

- [ ] Diagnóstico inicial e final foram aplicados.
- [ ] LAB-601 foi executado por pessoa diferente do autor.
- [ ] Pelo menos um estudante identificou corretamente quando não usar multiagentes.
- [ ] Prática guiada e independente foram concluídas sem dependência de informação tácita.
- [ ] Testes negativos foram compreendidos e reproduzidos.
- [ ] Rubrica de quatro níveis foi aplicada de forma consistente.
- [ ] Dificuldades recorrentes e pedidos de ajuda foram registrados.

## Validação multiplataforma

- [ ] Windows.
- [ ] Linux.
- [ ] macOS.
- [ ] Python 3.11 ou superior.
- [ ] Execução local sem rede, API ou segredo.

## Acessibilidade

- [ ] Diagramas possuem descrição textual.
- [ ] Tabelas possuem cabeçalhos claros.
- [ ] Informação não depende apenas de cor.
- [ ] Exemplos estão disponíveis como texto copiável.
- [ ] Estrutura de títulos é navegável por leitor de tela.
- [ ] Conteúdo audiovisual futuro possui legenda e transcrição.

## Segurança, privacidade e governança

- [ ] Revisão humana de segurança concluída.
- [ ] Revisão de privacidade e isolamento concluída.
- [ ] Revisão pedagógica concluída.
- [ ] Revisão técnica concluída.
- [ ] Riscos residuais estão documentados.
- [ ] Nenhuma alegação de conformidade jurídica ou segurança absoluta foi feita.
- [ ] Incidentes simulados possuem responsável, contenção e evidência.

## Métricas mínimas

O relatório de validação deve incluir:

- task success rate;
- handoff efficiency;
- coordination overhead;
- rework rate;
- authority violations;
- context leakage rate;
- cycle rate;
- arbitration rate;
- custo e latência comparados ao baseline simples.

## Regra de promoção

O módulo só pode ser promovido para `stable` quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. as evidências técnicas, pedagógicas e de acessibilidade estiverem anexadas;
3. a comparação com agente único ou workflow demonstrar benefício líquido;
4. revisões humanas estiverem registradas;
5. o CI estiver verde no mesmo SHA aprovado;
6. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.