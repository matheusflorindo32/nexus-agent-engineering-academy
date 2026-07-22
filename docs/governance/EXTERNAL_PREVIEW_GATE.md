---
id: governance.external-preview-gate
title: Gate de Preview Externo
lang: pt-BR
status: review
version: 0.1.0
---

# Gate de Preview Externo

Este gate verifica um preview HTTPS já publicado sem promover automaticamente o conteúdo, alterar domínio ou executar deploy de produção.

## Pré-condições

- SHA completo aprovado para teste;
- URL imutável do preview;
- build gerado com `portal/package-lock.json` versionado;
- endpoint `/.well-known/nexus-build.json` presente;
- headers definidos em `portal/vercel.json` aplicados pela plataforma;
- nenhum segredo inserido como parâmetro.

## Execução

Acione manualmente `Portal External Preview Gate` e informe:

- `preview_url`: URL HTTPS do artefato;
- `expected_sha`: SHA completo que deve aparecer na identidade publicada.

O workflow verifica rotas críticas, marcadores de conteúdo, ausência de redirecionamento inesperado, identidade do build, SHA, status editorial e headers reais.

## Hard gates

A decisão é `fail` diante de:

- URL sem HTTPS;
- SHA inválido ou divergente;
- rota crítica diferente de HTTP 200;
- conteúdo esperado ausente;
- identidade indisponível;
- header obrigatório ausente ou divergente;
- CSP sem `default-src 'self'`, `object-src 'none'` ou `frame-ancestors 'none'`;
- evidência não gerada.

## Evidência

O artefato contém o resultado JSON e seu SHA-256. A evidência vale somente para a URL e o SHA testados.

## Limitações

Um gate verde não prova acessibilidade prática, eficácia pedagógica, segurança absoluta, estabilidade futura da plataforma ou autorização para produção. Deploy, rollback e promoção continuam sujeitos a aprovação humana.
