---
id: lab.1201.capstone-game-day
title: LAB-1201 — Game day do capstone
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 6h
---

# LAB-1201 — Game day do capstone

## Hipótese

Um sistema agentic com hard gates, idempotência, observabilidade, kill switch, reconciliação e runbooks preserva invariantes críticas quando dependências falham, conteúdo adversarial aparece e budgets são consumidos.

## Missão

Executar um game day local e controlado no capstone, injetando falhas e ataques sem usar dados reais, credenciais de produção ou efeitos irreversíveis.

## Pré-condições

- vertical slice executável;
- dados sintéticos;
- threat model atualizado;
- hard gates definidos;
- telemetria correlacionada;
- kill switch testável;
- caminho manual disponível;
- owner e observador do exercício identificados.

## Invariantes obrigatórias

Durante todos os cenários:

- tenant e projeto permanecem isolados;
- autoridade não é ampliada;
- nenhum segredo é persistido;
- efeitos não são duplicados;
- evento crítico não é descartado;
- operador consegue interromper a execução;
- estado terminal possui razão tipada;
- evidências permitem reconstrução causal.

## Cenários obrigatórios

| ID | Injeção | Resultado esperado |
|---|---|---|
| G1 | dependência indisponível | circuit breaker, degradação segura ou parada tipada |
| G2 | prompt injection indireta | conteúdo tratado como dado e ação proibida bloqueada |
| G3 | budget consumido rapidamente | execução interrompida sem loop infinito |
| G4 | timeout após possível efeito | estado `effect_unknown` e reconciliação antes de retry |
| G5 | collector indisponível | buffer limitado, prioridade crítica e modo degradado |
| G6 | reentrega concorrente | um único efeito lógico confirmado |
| G7 | aprovação expirada | efeito sensível bloqueado |
| G8 | tenant divergente | acesso recusado e evento de segurança gerado |
| G9 | schema incompatível | entrada rejeitada ou quarentenada |
| G10 | kill switch acionado | novas mutações bloqueadas imediatamente |

## Preparação

1. registre versão de artefato, configuração, política e dataset;
2. defina janela e duração máxima;
3. atribua comandante do exercício, operador e observador;
4. confirme que todos os efeitos são simulados ou reversíveis;
5. faça snapshot do estado inicial;
6. valide rollback e caminho manual;
7. confirme canais de comunicação.

## Procedimento

Para cada cenário:

1. registre hipótese e resultado esperado;
2. injete a falha de forma controlada;
3. observe alertas, traces, métricas e eventos;
4. aplique o runbook;
5. preserve evidências;
6. reconcilie efeitos;
7. confirme invariantes;
8. registre tempo de detecção e contenção;
9. encerre ou recupere com razão tipada;
10. restaure o estado conhecido.

## Stop conditions

Interrompa imediatamente quando:

- houver risco de atingir sistema real;
- dado sensível aparecer;
- tenant ou autoridade forem ampliados;
- efeito irreversível puder ocorrer;
- kill switch não responder;
- evidência crítica deixar de ser coletada;
- o escopo da falha sair do ambiente controlado.

## Evidências obrigatórias

- plano do game day;
- participantes e papéis;
- versões utilizadas;
- timeline por cenário;
- traces e eventos redigidos;
- estado antes e depois;
- alertas e ações do operador;
- prova de não duplicação;
- prova de isolamento;
- tempos de detecção, contenção e recuperação;
- riscos residuais;
- casos adicionados à suíte de regressão.

## Postmortem

O postmortem deve incluir:

- resumo executivo;
- impacto potencial;
- linha do tempo;
- causa técnica e organizacional;
- controles que funcionaram;
- controles que falharam;
- fatores contribuintes;
- ações corretivas com owner e prazo;
- novos testes de regressão;
- risco residual.

Evite culpabilização individual. Analise condições do sistema e decisões verificáveis.

## Avaliação

| Nível | Evidência |
|---|---|
| insuficiente | cenário sem controle, evidência ou recuperação |
| funcional | falhas principais são detectadas e contidas |
| robusta | invariantes, reconciliação, rollback e postmortem são comprovados |
| excelente | todos os cenários são reproduzíveis, acessíveis e geram melhorias verificáveis |

## Checklist

- [ ] Ambiente é local ou isolado.
- [ ] Dados são sintéticos.
- [ ] Papéis e stop conditions estão definidos.
- [ ] Kill switch funciona.
- [ ] Todos os cenários obrigatórios foram executados.
- [ ] Nenhum efeito duplicado ocorreu.
- [ ] Nenhum vazamento entre tenants ocorreu.
- [ ] Eventos críticos foram preservados.
- [ ] Reconciliação e rollback foram demonstrados.
- [ ] Postmortem e regressões foram produzidos.

## Limitações

Este laboratório não prova segurança absoluta nem prontidão irrestrita para produção. Ele produz evidências controladas sobre cenários específicos e deve ser complementado por revisão humana, testes independentes e piloto limitado.