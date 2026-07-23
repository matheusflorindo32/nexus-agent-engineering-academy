---
id: governance.portal-artifact-integrity
title: Integridade criptográfica do artefato do portal
lang: pt-BR
status: review
version: 0.1.0
---

# Integridade criptográfica do artefato do portal

## Objetivo

Detectar qualquer alteração no artefato estático entre o término do build e sua validação, mantendo evidência reproduzível e vinculada ao SHA candidato.

Este protocolo não equivale a assinatura digital por identidade humana, não substitui proveniência externa e não prova integridade após upload em uma plataforma de hospedagem.

## Modelo de ameaça

O gate considera como falha:

- arquivo adicionado após o selo;
- arquivo removido;
- conteúdo alterado;
- tamanho alterado;
- ordem ou lista do manifesto adulterada;
- digest do manifesto inconsistente;
- evidence bundle incompleto.

## Manifesto

O manifesto contém, para cada arquivo do diretório `build`:

- caminho relativo normalizado;
- tamanho em bytes;
- SHA-256 do conteúdo.

Também contém:

- versão do esquema;
- algoritmo declarado;
- número total de arquivos;
- tamanho total;
- digest SHA-256 da lista canônica de registros.

## Controles positivos e negativos

O workflow executa três verificações obrigatórias:

1. **controle positivo inicial**: o artefato recém-selado deve passar;
2. **controle negativo**: uma alteração deliberada em `build/index.html` deve ser rejeitada;
3. **controle positivo após restauração**: o arquivo original é restaurado e o artefato deve voltar a passar.

O gate falha quando o controle negativo não é detectado.

## Hard gates

A execução é reprovada diante de:

- instalação, typecheck ou build com erro;
- manifesto vazio;
- digest malformado;
- divergência entre manifesto e artefato;
- adulteração aceita pelo verificador;
- restauração que não recompõe a integridade;
- evidência ausente;
- alteração dos manifestos de dependência durante a execução.

## Evidência mínima

O bundle deve conter:

- SHA candidato e versões das ferramentas;
- logs de instalação, typecheck e build;
- manifesto completo;
- digest externo do manifesto;
- relatório de geração;
- relatório de verificação inicial;
- relatório do controle negativo;
- relatório de verificação após restauração.

## Limitações

Este gate não prova:

- identidade criptográfica do autor;
- assinatura Sigstore ou chave privada;
- segurança do runner do GitHub Actions;
- integridade em CDN, DNS ou navegador do usuário;
- ausência de código malicioso já presente antes do selo;
- prontidão irrestrita para produção.

O conteúdo e a governança permanecem em `status: review` até aprovação humana e validação real.
