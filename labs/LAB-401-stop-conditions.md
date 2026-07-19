---
id: lab.401.stop-conditions
title: LAB-401 — Stop conditions
lang: pt-BR
status: foundation
---

# LAB-401 — Stop conditions

## Hipótese

Stop conditions determinísticas limitam dano mesmo quando a decisão do modelo é imprevisível.

## Procedimento

Execute o [loop determinístico](../examples/deterministic-loop/README.md) para: sucesso, budget zero, três observações
sem progresso, dependência falha e ação ambígua. Registre estado final, motivo, passos e efeitos.

## Evidência e critério

Todos os cenários terminam no estado esperado; nenhum excede o budget; efeito ambíguo não sofre retry.

## Stop conditions

O próprio runner termina após 20 passos e 10 segundos, independentemente do cenário.

