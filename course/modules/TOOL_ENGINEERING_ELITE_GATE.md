---
id: course.modules.tool-engineering-elite-gate
title: Gate Premium Elite — Tool Engineering
lang: pt-BR
status: review
---

# Gate Premium Elite — Tool Engineering

Este gate controla a promoção do Módulo 03 e do LAB-301 para `stable`.

## Bloqueios obrigatórios

A promoção é proibida enquanto qualquer item permanecer aberto:

- [ ] piloto com estudantes de perfis distintos;
- [ ] execução validada em Windows, Linux e macOS;
- [ ] LAB-301 revisado sob o contrato pedagógico atual;
- [ ] demonstração executável reproduzida por pessoa diferente do autor;
- [ ] revisão humana de segurança;
- [ ] revisão de acessibilidade;
- [ ] revisão das referências e datas de acesso;
- [ ] ausência de risco crítico ou alto sem tratamento;
- [ ] CI integralmente verde no SHA final.

## Evidências técnicas mínimas

- schema rejeita campos extras e valores fora do domínio;
- identidade, tenant, credencial e ambiente vêm do runtime confiável;
- preview apresenta efeito, escopo, custo, irreversibilidade e rollback;
- aprovação está vinculada ao hash do preview;
- idempotência evita efeitos duplicados;
- timeout ambíguo leva à reconciliação, não a retry cego;
- logs redigem segredos e dados sensíveis;
- testes incluem parâmetros hostis e falhas ambíguas;
- stop conditions são observáveis;
- risco residual está documentado.

## Evidências pedagógicas mínimas

- diagnóstico inicial aplicado;
- tempo real comparado à estimativa;
- pontos recorrentes de bloqueio registrados;
- prática guiada e independente concluídas;
- rubrica aplicada por pelo menos dois avaliadores em amostra;
- aluno consegue explicar validação, autorização, aprovação, idempotência e reconciliação sem copiar definições;
- alternativa textual disponível para diagramas e demonstrações.

## Critérios de reprovação imediata

- autoridade escolhida pelo modelo ou pelo texto recuperado;
- segredo real em código, fixture, log ou screenshot;
- escrita externa não idempotente repetida após efeito desconhecido;
- aprovação desvinculada dos parâmetros executados;
- teste ou validador enfraquecido apenas para obter CI verde;
- alegação de segurança absoluta;
- material anunciado como validado antes do piloto.

## Decisão de promoção

A mudança para `stable` exige registro com:

- SHA avaliado;
- ambientes testados;
- participantes do piloto de forma anonimizada;
- métricas observadas;
- riscos residuais;
- revisores responsáveis;
- decisão final e data de revisão futura.
