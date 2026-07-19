---
id: i18n.policy
title: Política de internacionalização
lang: pt-BR
status: stable
---

# Internacionalização

Português brasileiro é a fonte canônica. Inglês e espanhol são traduções, não forks editoriais.

## Regras

1. Preserve `id`, blocos de código, nomes de arquivos referenciados e âncoras explícitas.
2. Traduza `title`, corpo, texto alternativo e rótulos do Mermaid quando viável.
3. Mantenha `translation_of` apontando para o ID canônico e `source_revision` para o commit traduzido.
4. Atualize [manifest.yml](manifest.yml) com `missing`, `outdated`, `review` ou `current`.
5. Links relativos apontam preferencialmente para o mesmo idioma; fallback explícito pode apontar para `pt-BR`.
6. Revisão humana é obrigatória para objetivos, rubricas, segurança e referências.

## Layout

O conteúdo canônico permanece nos diretórios de domínio. Traduções residirão em `docs/i18n/en/` e `docs/i18n/es/`,
espelhando o caminho relativo quando publicadas. Arquivos `.gitkeep` mantêm a estrutura inicial sem simular tradução.

