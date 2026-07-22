---
id: governance.contributing
title: Guia de contribuição
lang: pt-BR
status: review
version: 0.2.0
---

# Contribuindo com a NEXUS

Obrigado por ajudar a construir educação aberta e rigorosa em Agent Engineering. Leia também o [Código de Conduta](CODE_OF_CONDUCT.md), a [Política de Segurança](SECURITY.md), as [regras de licenciamento](LICENSING.md) e o contrato operacional em [AGENTS.md](AGENTS.md).

## Antes de começar

Escolha uma mudança pequena, verificável e proporcional ao risco. Prefira uma issue por problema e um PR por objetivo principal.

Não use a primeira contribuição para:

- reestruturar todo o currículo;
- trocar validadores sem evidência;
- promover conteúdo para `stable`;
- adicionar dependência ampla;
- inserir integração com conta real;
- alterar licença, marca ou governança sem discussão explícita.

## Tipos de contribuição

| Tipo | Exemplos | Evidência mínima |
|---|---|---|
| Correção editorial | link, termo, clareza | validador e justificativa |
| Conteúdo pedagógico | módulo, explicação, exercício | objetivo, prática, avaliação e fonte |
| Laboratório | cenário, teste negativo, métrica | hipótese, baseline, evidência e stop conditions |
| Código ou exemplo | demo, validador, adapter | teste, versões, limitações e segurança |
| Segurança | hardening, teste adversarial | threat model e relato privado quando houver vulnerabilidade |
| Acessibilidade | alt text, navegação, linguagem | reprodução por pessoa ou ferramenta adequada |
| Tradução | pt-BR para outro idioma | IDs preservados e paridade verificada |

## Fluxo recomendado

1. Procure issue ou PR existente.
2. Abra uma issue descrevendo problema, evidência, escopo e resultado esperado.
3. Crie branch curta: `docs/...`, `feat/...`, `fix/...`, `lab/...` ou `test/...`.
4. Faça mudanças coesas.
5. Adicione teste ou justifique claramente a não aplicabilidade.
6. Execute:

```bash
python tests/validate_repository.py
```

7. Use Conventional Commits.
8. Abra um Draft PR enquanto houver trabalho ou revisão pendente.
9. Preencha riscos, evidências, limitações e plano de rollback.
10. Aguarde revisão humana. CI verde não autoriza merge.

## Padrão editorial

Conteúdo educacional deve demonstrar, quando aplicável:

```text
problema e baseline
→ conceito
→ contratos e arquitetura
→ implementação mínima
→ testes positivos e negativos
→ comparação
→ evidência
→ limitações e próxima ação
```

Arquivos Markdown precisam de frontmatter com `id`, `title`, `lang` e `status`. O `id` é permanente e igual em todas as traduções. Links internos são relativos. Não use sintaxe proprietária como única forma de navegação.

Conteúdo novo permanece em `review` até possuir evidência humana suficiente. Não use `stable` como sinônimo de “parece pronto”.

## Evidência e referências

- Priorize documentação oficial, RFC, norma, artigo científico ou livro reconhecido.
- Registre autor institucional, título, versão ou data, URL e data de acesso quando o padrão editorial exigir.
- Separe fato documentado, inferência e decisão pedagógica.
- Não invente DOI, benchmark, compatibilidade ou suporte de plataforma.
- Não copie exemplos, imagens ou datasets sem licença compatível.
- Declare versões e limitações de qualquer integração externa.

## Segurança e privacidade

Toda contribuição deve adotar:

- dados sintéticos por padrão;
- nenhuma credencial real;
- nenhuma conta ou infraestrutura de produção;
- least privilege;
- deny by default para efeitos sensíveis;
- redaction antes de persistência;
- stop conditions;
- reconciliação antes de retry após efeito ambíguo;
- revisão humana para autoridade, merge, release e promoção.

Vulnerabilidades não devem ser descritas em issue pública. Siga [SECURITY.md](SECURITY.md).

## Testes proporcionais ao risco

| Risco | Exigência mínima |
|---|---|
| Baixo | validador estrutural e revisão editorial |
| Médio | teste positivo, negativo e limitação explícita |
| Alto controlado | threat model, cenários adversariais, hard gates e revisão independente |
| Crítico ou ambiente real | fora do escopo sem aprovação formal e ambiente isolado |

Nunca enfraqueça um validador apenas para fazer a CI passar. Corrija o conteúdo ou demonstre, em discussão separada, por que o contrato precisa mudar.

## Acessibilidade

- use títulos hierárquicos;
- descreva diagramas também em texto;
- forneça alt text útil;
- não dependa apenas de cor;
- mantenha comandos copiáveis;
- explique siglas na primeira ocorrência;
- registre limitações de acessibilidade conhecidas.

## Licenciamento

Confirme a origem e a licença de código, texto, imagem, dataset, fonte e mídia. Contribuir implica possuir direito de licenciar o material. Consulte [LICENSING.md](LICENSING.md).

## Definition of Done

- [ ] Escopo e resultado observável estão claros.
- [ ] Baseline ou justificativa de não aplicabilidade foi registrado.
- [ ] Exemplos não contêm segredos, dados pessoais ou autoridade excessiva.
- [ ] IDs, frontmatter, links e navegação foram validados.
- [ ] Referências sustentam as afirmações relevantes.
- [ ] Testes positivos e negativos foram executados quando aplicáveis.
- [ ] Hard gates não foram substituídos por média.
- [ ] Acessibilidade e internacionalização foram consideradas.
- [ ] Limitações e riscos residuais são explícitos.
- [ ] O conteúdo permanece em `review` quando não houve piloto humano.
- [ ] O PR está pequeno, auditável e sem merge automático.

## Revisão e decisão

Mantenedores podem solicitar mudanças, dividir o PR, bloquear escopo perigoso ou recusar material sem proveniência. Aprovação técnica não substitui revisão pedagógica, segurança, privacidade, acessibilidade ou licenciamento quando essas dimensões forem relevantes.