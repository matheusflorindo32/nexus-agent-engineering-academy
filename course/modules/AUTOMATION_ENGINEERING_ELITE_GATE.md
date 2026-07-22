---
id: course.gate.automation-engineering-elite
title: Gate Premium Elite — Automação Agentic
lang: pt-BR
status: review
---

# Gate Premium Elite — Automação Agentic

Este gate define as condições mínimas para promover o Módulo 11 de `review` para `stable`.

## Bloqueios absolutos

A promoção é proibida quando existir qualquer um dos itens abaixo:

- reentrega ou concorrência capaz de duplicar efeito externo;
- retry após timeout sem reconciliação do estado real;
- agente capaz de alterar identidade, tenant, destino, permissão ou política;
- aprovação reutilizável em payload diferente;
- efeito sensível sem ledger ou trilha de auditoria íntegra;
- DLQ sem owner e política de tratamento;
- compensação não idempotente;
- segredo em evento, prompt, log ou artefato;
- ausência de caminho manual seguro;
- risco crítico ou alto sem mitigação e aprovação humana.

## Evidências técnicas obrigatórias

- [ ] Eventos possuem ID, versão, origem, tenant e correlação.
- [ ] Reentrega retorna resultado existente sem novo efeito.
- [ ] Execução concorrente produz um único efeito lógico.
- [ ] Idempotency keys são duráveis e semanticamente estáveis.
- [ ] Timeouts mutáveis entram em estado `effect_unknown`.
- [ ] Reconciliação ocorre antes de retry de efeito ambíguo.
- [ ] Retry budget, backoff e jitter são testados.
- [ ] DLQ, poison messages e backpressure são demonstrados.
- [ ] Compensações possuem chave própria e resultado terminal.
- [ ] Aprovações estão vinculadas ao artefato exato.
- [ ] Agente é usado somente em decisão ambígua.
- [ ] Trace e ledger permitem reconstrução completa.
- [ ] CI está verde no SHA final.

## Evidências pedagógicas obrigatórias

- [ ] Diagnóstico inicial e final foram aplicados.
- [ ] LAB-1101 foi executado por pessoa diferente do autor.
- [ ] Pelo menos um estudante explicou a diferença entre retry, compensação e reconciliação.
- [ ] Prática guiada e independente foram reproduzidas sem informação tácita.
- [ ] Testes negativos foram compreendidos e executados.
- [ ] Comparação entre código e plataforma visual usou critérios equivalentes.
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

## Segurança e operação

- [ ] Revisão humana de segurança concluída.
- [ ] Revisão de privacidade e isolamento concluída.
- [ ] Revisão técnica concluída.
- [ ] Revisão pedagógica concluída.
- [ ] Owners, SLA, alertas e runbooks estão definidos.
- [ ] Kill switch e caminho manual foram testados.
- [ ] Riscos residuais estão documentados.
- [ ] Nenhuma alegação de segurança absoluta ou conformidade jurídica foi feita.

## Métricas mínimas

O relatório de validação deve incluir:

- duplicate effect rate;
- redelivery rate;
- idempotency hit rate;
- retry success rate;
- unknown effect rate;
- compensation rate;
- DLQ rate;
- manual intervention rate;
- workflow success rate;
- time to reconcile.

## Regra de promoção

O módulo só pode ser promovido para `stable` quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. as evidências técnicas, pedagógicas e de acessibilidade estiverem anexadas;
3. reentrega, concorrência, timeout e compensação forem reproduzíveis;
4. revisões humanas estiverem registradas;
5. o CI estiver verde no mesmo SHA aprovado;
6. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.