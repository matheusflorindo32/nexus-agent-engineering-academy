---
id: portal.readme
title: Portal NEXUS
lang: pt-BR
status: review
version: 0.2.0
---

# Portal NEXUS

Portal estático para publicar o conteúdo canônico do repositório sem duplicar módulos, laboratórios ou projetos.

## Decisão

- gerador: Docusaurus 3.10.2;
- runtime de build: Node.js 20 ou superior;
- conteúdo: `../course`, `../labs` e `../projects`;
- autenticação: nenhuma na primeira versão;
- busca remota, analytics e cookies: desabilitados até decisão arquitetural específica;
- deploy: somente por preview imutável, digest e aprovação humana.

A versão foi fixada para reduzir deriva entre preview e produção. Todos os pacotes `@docusaurus/*` usam a mesma versão.

## Estado atual da instalação

O repositório ainda não contém `portal/package-lock.json`. Enquanto esse artefato não for gerado, revisado e versionado:

- o workflow usa `npm install` apenas para provar que o scaffold pode ser resolvido, tipado e compilado;
- a execução não é considerada totalmente reproduzível;
- cache de dependências permanece desabilitado;
- publicação e release continuam bloqueadas;
- o próximo gate é substituir `npm install` por `npm ci` no mesmo SHA que contiver o lockfile aprovado.

Esse modo transitório não deve ser interpretado como exceção permanente ao requisito de lockfile.

## Executar localmente antes do lockfile

```bash
cd portal
npm install --no-audit --no-fund --ignore-scripts
npm run typecheck
npm run build
npm run serve
```

Após a aprovação do lockfile, o procedimento obrigatório será:

```bash
cd portal
npm ci --ignore-scripts
npm run typecheck
npm run build
npm run serve
```

O build deve falhar diante de links quebrados.

## Quality gate automatizado

O workflow `.github/workflows/portal-quality.yml` executa no SHA exato do pull request:

1. checkout do commit;
2. Node.js fixado;
3. registro das versões de Node e npm;
4. instalação transitória das dependências declaradas;
5. typecheck;
6. build estático;
7. verificação das rotas críticas;
8. manifesto ordenado dos arquivos gerados;
9. evidence bundle retido por sete dias.

Um workflow verde prova somente que esse SHA foi resolvido e compilado naquele ambiente. Ele não prova reprodutibilidade completa, acessibilidade, segurança, eficácia pedagógica, aprovação para merge ou prontidão para deploy.

## Rotas

| Conteúdo | Rota |
|---|---|
| Curso | `/curso/` |
| Laboratórios | `/laboratorios/` |
| Projetos | `/projetos/` |

## Evidência mínima antes de publicar

- `python tests/validate_repository.py` no repositório;
- `npm ci` com lockfile aprovado;
- `npm run typecheck` sem erro;
- `npm run build` sem erro;
- evidence bundle vinculado ao SHA;
- navegação por teclado;
- foco visível;
- zoom a 200%;
- leitura do conteúdo essencial sem JavaScript;
- smoke test das rotas críticas;
- comparação do digest do preview com o artefato publicado;
- rollback ensaiado.

## Hard gates

A publicação permanece bloqueada se houver:

- ausência de lockfile aprovado;
- rota crítica indisponível;
- link interno quebrado;
- segredo no bundle;
- conteúdo essencial dependente exclusivamente de JavaScript;
- navegação impossível por teclado;
- foco invisível;
- imagem instrucional sem alternativa textual;
- digest diferente do preview aprovado;
- rollback não demonstrado.

## Limitações

Este scaffold e seu build automatizado ainda não provam acessibilidade, segurança ou eficácia pedagógica. O portal precisa de lockfile aprovado, revisão humana, preview imutável, validação prática de acessibilidade, smoke test e ensaio de rollback antes de qualquer promoção de status ou publicação.