---
id: governance.portal-http-e2e
title: Contrato HTTP E2E do portal
lang: pt-BR
status: review
version: 0.1.0
---

# Contrato HTTP E2E do portal

## Objetivo

Validar o artefato estático do portal por meio de uma jornada HTTP executada contra o servidor candidato construído no próprio workflow.

## Escopo

O gate verifica:

- resposta HTTP 200 da página inicial;
- presença de HTML e conteúdo principal;
- amostragem determinística de até oito links internos expostos pela página inicial;
- resposta HTTP 200 e contrato HTML nas rotas amostradas;
- resposta HTTP 404 para uma rota deliberadamente inexistente;
- geração de relatório estruturado e retenção de evidências.

## Hard gates

A execução falha quando:

- a instalação reproduzível falha;
- typecheck ou build falham;
- o servidor candidato não fica disponível;
- uma rota esperada retorna status divergente;
- uma página esperada não apresenta contrato HTML mínimo;
- a página inicial não expõe links internos amostráveis;
- a rota negativa não retorna 404.

## Evidências

O bundle contém:

- `report.json` com rotas, status, duração, tipo de conteúdo e tamanho;
- log do servidor candidato;
- SHA do PR incorporado ao nome do artefato.

## Interpretação

Um resultado verde sustenta apenas que o artefato candidato respondeu corretamente ao contrato HTTP testado no ambiente do workflow.

## Limitações

Este controle:

- não usa navegador real;
- não substitui Playwright, Cypress ou testes equivalentes de interação;
- não verifica leitores de tela, navegação por teclado ou acessibilidade humana;
- não detecta regressões visuais;
- não comprova comportamento da infraestrutura de produção;
- não autoriza merge, release ou deploy.

O protocolo permanece em `status: review` até revisão humana e expansão futura para testes reais de navegador.
