---
id: docs.pedagogy.beginner-zero-track
title: Plano de implementação da Trilha Zero
lang: pt-BR
status: draft
---

# Plano de implementação da Trilha Zero

## Objetivo

Preparar uma pessoa sem experiência prévia para entrar no Módulo 00 com autonomia mínima, sem depender de conta paga, chave de API ou serviço externo.

## Estrutura

| Unidade | Tema | Evidência mínima |
|---|---|---|
| Z00 | computador e ambiente de desenvolvimento | identificar arquivos, pastas, programas e sistema operacional |
| Z01 | terminal sem medo | navegar, listar, criar pasta e executar comando |
| Z02 | Git e GitHub essenciais | clonar, verificar status e entender commit |
| Z03 | Python essencial | executar script, alterar variável, função e condição simples |
| Z04 | Markdown, JSON e YAML | criar e validar arquivos básicos |
| Z05 | HTTP, APIs, chaves e ambiente | explicar request/response e proteger segredo |
| Z06 | segurança básica | reconhecer exposição de credencial e aplicar prevenção |
| Z07 | clonar, executar, testar e corrigir | reproduzir ambiente e interpretar erro simples |
| Z08 | primeiro workflow | executar fluxo determinístico com entrada e saída |
| Z09 | primeiro agente simples | comparar workflow e agente read-only |

## Contrato pedagógico por unidade

Cada unidade deve conter:

1. explicação em linguagem popular;
2. analogia;
3. mapa visual;
4. demonstração;
5. prática guiada;
6. prática independente;
7. erros comuns;
8. solução comentada;
9. miniavaliação;
10. checklist;
11. projeto curto;
12. instruções para Windows, Linux e macOS.

## Projeto integrador

A pessoa deverá:

- clonar a NEXUS;
- executar o validador;
- executar um agente read-only local;
- modificar uma entrada sintética;
- interpretar a decisão;
- executar teste;
- registrar ambiente, comando e resultado;
- explicar por que nenhuma credencial foi necessária.

## Critério de aprovação

A entrada no Módulo 00 exige:

- pelo menos 80% da avaliação objetiva;
- conclusão do projeto integrador;
- ausência de segredo em arquivos ou histórico;
- capacidade de reproduzir os comandos sem ajuda direta;
- capacidade de apresentar erro com contexto suficiente.

## Ordem de produção

1. implementar Z01, Z02, Z03 e Z07 como núcleo operacional;
2. implementar Z04, Z05 e Z06;
3. implementar Z08 e Z09;
4. finalizar Z00 como orientação visual;
5. executar teste interno;
6. pilotar com iniciantes absolutos;
7. revisar linguagem e tempo;
8. declarar versão inicial somente após o piloto.

## Gate

Este documento é um plano. A Trilha Zero não pode ser anunciada como disponível enquanto as unidades, exercícios, soluções e testes não existirem na árvore ativa.
