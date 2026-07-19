---
id: standards.content
title: Padrão editorial e pedagógico
lang: pt-BR
status: stable
---

# Padrão editorial e pedagógico

## Frontmatter mínimo

```yaml
---
id: domain.unique-stable-id
title: Título humano
lang: pt-BR
status: draft
---
```

IDs usam letras minúsculas, números, ponto e hífen; não incluem idioma, versão ou caminho. `status` aceita `draft`,
`foundation`, `active`, `accepted`, `stable`, `deprecated` ou `archived`.

## Estrutura de ensino

Todo módulo deve tornar visível esta sequência:

1. **Conceito:** definições, invariantes e limites.
2. **Arquitetura:** componentes, contratos, dados, estados e ameaças.
3. **Implementação:** pelo menos um adapter verificável.
4. **Comparação:** equivalências, lacunas, custos e lock-in.
5. **Projeto real:** resultado observável e rubrica.

## Linguagem

- Defina termos antes de abreviar.
- Diferencie fato, inferência, recomendação e opinião.
- Use exemplos pequenos, originais e seguros por padrão.
- Não use antropomorfismo para esconder mecanismos.
- Marque conteúdo instável com data de verificação.

## Referências

Fontes primárias precedem blogs e agregadores. Toda referência web inclui data de acesso; APIs incluem versão quando
publicada. Use o [catálogo e os modelos de citação](../references/README.md).

## Diagramas e acessibilidade

Mermaid deve ter explicação textual adjacente. Imagens possuem `alt`. Tabelas são usadas apenas para comparação de
campos repetidos. Emojis e callouts são discretos e nunca a única pista semântica.

## Review loop

Antes do merge, execute até dez ciclos conforme necessário: precisão → clareza → consistência → links → estrutura →
ortografia → arquitetura → duplicação → segurança → refinamento. Registre exceções na PR.

