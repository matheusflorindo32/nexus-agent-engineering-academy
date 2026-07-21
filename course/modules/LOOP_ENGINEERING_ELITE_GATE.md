---
id: course.gate.loop-engineering-elite
title: Gate Premium Elite — Loop Engineering
lang: pt-BR
status: review
---

# Gate Premium Elite — Loop Engineering

Este gate define as condições mínimas para promover o Módulo 04 de `review` para `stable`.

## Conteúdo e didática

- [ ] público-alvo e pré-requisitos foram confirmados em piloto;
- [ ] diagnóstico inicial diferencia estudantes preparados e não preparados;
- [ ] explicação em três camadas foi compreendida sem mediação excessiva;
- [ ] prática guiada e independente foram concluídas por perfis diferentes;
- [ ] quiz e rubrica discriminam níveis de domínio;
- [ ] exemplos de sucesso, falha, estagnação e retomada são reproduzíveis.

## Execução

- [ ] `examples/deterministic_loop.py --self-test` executa conforme documentado;
- [ ] execução validada em Windows, Linux e macOS;
- [ ] estados e transições inválidas são rejeitados;
- [ ] todos os cenários alcançam estado terminal permitido;
- [ ] checkpoint incompatível falha de forma segura;
- [ ] retomada não duplica efeitos;
- [ ] circuit breaker possui teste de `closed`, `open` e `half_open`.

## Segurança e confiabilidade

- [ ] nenhum retry automático ocorre após efeito ambíguo;
- [ ] operações não idempotentes exigem reconciliação;
- [ ] budgets são multidimensionais e persistidos;
- [ ] estagnação é detectada por critério mensurável;
- [ ] checkpoints e logs não contêm segredos;
- [ ] operador consegue interromper a execução;
- [ ] risco residual está documentado;
- [ ] nenhum risco crítico ou alto permanece sem tratamento.

## Laboratório e avaliação

- [ ] LAB-401 está alinhado ao contrato Premium Elite;
- [ ] casos negativos incluem budget zero, no-progress, timeout e replay;
- [ ] solução comentada não elimina raciocínio do estudante;
- [ ] evidências mínimas são objetivas e verificáveis;
- [ ] outra pessoa reproduziu a entrega sem conhecimento tácito.

## Acessibilidade

- [ ] diagramas possuem descrição textual;
- [ ] estados não dependem apenas de cor;
- [ ] comandos podem ser copiados e executados por teclado;
- [ ] tabelas possuem cabeçalhos claros;
- [ ] conteúdo foi testado com zoom e navegação por teclado;
- [ ] qualquer vídeo possui legenda e transcrição.

## Evidência pedagógica

- [ ] piloto inclui perfis técnico-iniciante, intermediário e avançado;
- [ ] tempo mediano não excede duas vezes a estimativa sem justificativa;
- [ ] menos de 25% bloqueiam no mesmo ponto sem solução prevista;
- [ ] pedidos de ajuda recorrentes foram analisados;
- [ ] falhas de segurança observadas foram corrigidas;
- [ ] feedback do piloto foi incorporado e registrado.

## Aprovações obrigatórias

- [ ] revisão pedagógica humana;
- [ ] revisão técnica humana;
- [ ] revisão de segurança humana;
- [ ] revisão de acessibilidade;
- [ ] CI integralmente verde no SHA final;
- [ ] integração ordenada da pilha de PRs.

## Comunicação honesta

Enquanto qualquer item obrigatório estiver pendente:

- o módulo permanece em `review`;
- não deve ser anunciado como validado para todos os iniciantes;
- não deve receber alegação de garantia de segurança ou ausência de falhas;
- resultados de piloto não devem ser generalizados além da amostra observada.
