---
id: governance.contributing
title: Guia de contribuição
lang: pt-BR
status: stable
---

# Contribuindo com a NEXUS

Obrigado por elevar o padrão da educação em Agent Engineering. Leia também o
[Código de Conduta](CODE_OF_CONDUCT.md) e a [Política de Segurança](SECURITY.md).

## Fluxo

1. Abra uma issue descrevendo problema, evidência e resultado esperado.
2. Crie uma branch curta: `docs/...`, `feat/...`, `fix/...` ou `lab/...`.
3. Faça mudanças coesas e testes proporcionais ao risco.
4. Execute `python tests/validate_repository.py`.
5. Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
6. Abra um pull request preenchendo todo o template.

## Padrão editorial

Todo conteúdo educacional deve seguir: **conceito → arquitetura → implementação → comparação → projeto real**.
Arquivos Markdown precisam de frontmatter com `id`, `title`, `lang` e `status`. O `id` é permanente e igual em todas
as traduções. Links internos são relativos; não use sintaxe proprietária do Obsidian como única forma de navegação.

## Evidência e referências

- Priorize fontes primárias: documentação oficial, RFC, norma, artigo científico ou livro reconhecido.
- Registre autor institucional, título, versão/data, URL e data de acesso.
- Separe afirmação documentada de opinião pedagógica.
- Não copie exemplos de terceiros; prefira implementações mínimas originais.

## Definition of Done

- [ ] Escopo e decisão arquitetural estão claros.
- [ ] Exemplos não contêm segredos nem permissões excessivas.
- [ ] IDs, links relativos e navegação foram validados.
- [ ] Referências existem e sustentam as afirmações.
- [ ] Conteúdo canônico em português foi atualizado antes das traduções.
- [ ] Mudança possui teste, laboratório ou justificativa de não aplicabilidade.

