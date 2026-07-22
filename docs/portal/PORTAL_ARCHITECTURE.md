---
id: portal.architecture
lang: pt-BR
title: Arquitetura do portal educacional NEXUS
status: review
version: 0.1.0
---

# Arquitetura do portal educacional NEXUS

## Objetivo

Publicar o currículo NEXUS como portal navegável, acessível e auditável sem transformar o conteúdo canônico em uma cópia difícil de manter. O Markdown versionado no repositório permanece a fonte de verdade.

## Não objetivos

O primeiro portal não é um LMS completo, não promete certificação, não coleta dados sensíveis e não exige autenticação. Progresso, contas, pagamentos, provas supervisionadas e credenciais verificáveis ficam fora do escopo inicial.

## Invariantes

- conteúdo canônico permanece em `pt-BR` no repositório;
- IDs, links e frontmatter não são reescritos silenciosamente;
- nenhuma página depende de chave de API para ser lida;
- navegação principal funciona por teclado e leitor de tela;
- diagramas possuem alternativa textual;
- build falha diante de link interno quebrado, rota órfã ou frontmatter inválido;
- analytics, quando adotados, devem ser opcionais, minimizados e documentados;
- deploy nunca altera conteúdo sem commit identificável.

## Arquitetura recomendada

```text
Markdown canônico
→ validação estrutural
→ transformação controlada
→ geração estática
→ testes de links, rotas e acessibilidade
→ preview imutável por commit
→ aprovação humana
→ publicação
```

### Camadas

1. **Conteúdo:** `course/`, `labs/`, `projects/`, `docs/`, `templates/`.
2. **Catálogo:** índices derivados de frontmatter e manifesto de navegação.
3. **Apresentação:** gerador estático com componentes progressivos e fallback sem JavaScript.
4. **Qualidade:** validadores do repositório, testes de build, links, rotas e acessibilidade.
5. **Entrega:** preview por PR e produção somente após integração aprovada.

## Navegação mínima

- página inicial;
- quickstart;
- Trilha Zero;
- módulos 00–12;
- laboratórios;
- projetos;
- glossário;
- referências;
- contribuição;
- segurança;
- licenciamento;
- estado do projeto.

Toda página deve informar título, objetivo, pré-requisitos, tempo estimado quando aplicável, status editorial e próxima ação recomendada.

## Busca

A primeira versão deve usar índice estático gerado no build. O índice não pode incluir segredos, artefatos privados, conteúdo excluído ou campos não permitidos. Consultas não devem ser enviadas a terceiros por padrão.

## Segurança

- política de segurança de conteúdo estrita;
- dependências fixadas e auditáveis;
- nenhuma execução de código do usuário no navegador;
- HTML bruto limitado e revisado;
- links externos identificáveis;
- formulários externos não são requisito para aprendizagem;
- previews de PR não devem expor variáveis ou conteúdo privado.

## Privacidade

O portal inicial deve funcionar sem conta e sem cookies não essenciais. Qualquer telemetria futura precisa declarar finalidade, campos, retenção, base de decisão, opt-out e owner.

## Performance

Metas iniciais, verificadas em páginas representativas:

- conteúdo principal utilizável sem JavaScript;
- nenhuma imagem maior que o necessário para o viewport;
- fontes com fallback local do sistema;
- navegação e conteúdo prioritário não bloqueados por mídia decorativa;
- budget de página e exceções registrados no relatório de release.

## Estratégia de deploy

1. gerar preview imutável para cada PR elegível;
2. executar validação de conteúdo, build, rotas e acessibilidade;
3. registrar digest do artefato;
4. obter aprovação humana;
5. publicar exatamente o artefato aprovado;
6. executar smoke test pós-deploy;
7. manter rollback para o digest anterior.

## Evidências obrigatórias

- mapa de rotas;
- relatório de links;
- relatório de acessibilidade;
- inventário de dependências;
- digest do build;
- teste de navegação por teclado;
- teste em viewport móvel e desktop;
- smoke test pós-deploy;
- procedimento de rollback;
- limitações e riscos residuais.

## Hard gates

A publicação é bloqueada se houver rota crítica inacessível, link interno quebrado, conteúdo sem status, imagem instrucional sem alternativa textual, foco invisível, navegação impossível por teclado, segredo no build, preview divergente do artefato publicado ou rollback não demonstrado.

## Decisão arquitetural

A escolha do gerador estático deve ser registrada em ADR comparando, no mínimo, manutenção, acessibilidade, busca, i18n, compatibilidade com Markdown, previews, segurança, custo e reversibilidade. Popularidade não substitui evidência.

## Limitações

Este documento define arquitetura e gates. Ele não prova conformidade com WCAG, segurança absoluta, eficácia pedagógica ou prontidão para escala. Essas afirmações exigem testes independentes, revisão humana e piloto real.