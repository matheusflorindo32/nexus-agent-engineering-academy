---
id: portal.readme
title: Portal NEXUS
lang: pt-BR
status: review
version: 0.1.0
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

## Executar localmente

```bash
cd portal
npm ci
npm run start
```

Para validar o build estático:

```bash
npm run build
npm run serve
```

O build deve falhar diante de links quebrados.

## Rotas

| Conteúdo | Rota |
|---|---|
| Curso | `/curso/` |
| Laboratórios | `/laboratorios/` |
| Projetos | `/projetos/` |

## Evidência mínima antes de publicar

- `python tests/validate_repository.py` no repositório;
- `npm ci` com lockfile aprovado;
- `npm run build` sem erro;
- navegação por teclado;
- foco visível;
- zoom a 200%;
- leitura do conteúdo essencial sem JavaScript;
- smoke test das rotas críticas;
- comparação do digest do preview com o artefato publicado;
- rollback ensaiado.

## Hard gates

A publicação permanece bloqueada se houver:

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

Este scaffold ainda não prova acessibilidade, segurança ou eficácia pedagógica. Ele precisa ser instalado, compilado, inspecionado por pessoa revisora, publicado em preview e submetido aos protocolos do repositório antes de qualquer promoção de status.
