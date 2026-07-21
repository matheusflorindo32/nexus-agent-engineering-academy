---
id: course.zero-track.z02
title: Z02 — Git e GitHub essenciais
lang: pt-BR
status: review
prerequisites: [course.zero-track.z01]
estimated_hours: 4
---

# Z02 — Git e GitHub essenciais

## Para quem é

Para quem nunca criou um repositório ou ainda confunde Git, GitHub, commit, branch, push e pull request.

## O que você vai aprender

Ao concluir, você consegue:

- explicar a diferença entre Git e GitHub;
- iniciar um repositório local;
- identificar mudanças;
- criar commits pequenos e compreensíveis;
- criar e trocar de branch;
- ler um histórico;
- reconhecer situações em que não deve publicar conteúdo.

## Explicação simples

Pense em um trabalho escolar:

- **Git** é o sistema que registra versões no seu computador;
- **GitHub** é um serviço online que armazena e compartilha repositórios;
- **commit** é um ponto de versão com uma explicação;
- **branch** é uma linha paralela de trabalho;
- **pull request** é um pedido para revisar e integrar mudanças.

## Conceito profissional

Git é um sistema distribuído de controle de versão. Cada commit referencia uma árvore de arquivos e um ou mais commits anteriores. Branches são referências móveis para commits. GitHub adiciona colaboração, revisão, permissões, automações e rastreabilidade ao fluxo Git.

## Preparação segura

Use uma pasta de laboratório sem dados pessoais.

Configure identidade local apenas se necessário:

```bash
git config user.name "Aluno NEXUS"
git config user.email "aluno@example.invalid"
```

O domínio `.invalid` é reservado para exemplos e não representa e-mail real.

## Prática guiada

### 1. Criar o laboratório

```bash
mkdir nexus-git-lab
cd nexus-git-lab
git init
```

### 2. Criar o primeiro arquivo

Crie `README.md` com:

```markdown
# Meu laboratório Git

Objetivo: aprender versionamento sem publicar segredos.
```

### 3. Inspecionar e registrar

```bash
git status
git add README.md
git commit -m "docs: iniciar laboratório Git"
```

### 4. Criar uma branch

```bash
git switch -c feat/adicionar-anotacoes
```

Crie `anotacoes.md`, registre uma explicação sobre Git e faça novo commit:

```bash
git add anotacoes.md
git commit -m "docs: adicionar anotações sobre Git"
```

### 5. Ler o histórico

```bash
git log --oneline --decorate --graph --all
```

## Prática independente

Crie uma segunda branch chamada `fix/melhorar-readme`.

Nela:

1. melhore o README;
2. confira o diff;
3. faça commit com mensagem clara;
4. volte para a branch inicial;
5. explique por que a mudança ainda não aparece nela.

Comandos úteis:

```bash
git branch
git switch nome-da-branch
git diff
git log --oneline --graph --all
```

## Quando usar GitHub

Publique somente depois de confirmar que o repositório não contém:

- tokens;
- senhas;
- chaves de API;
- arquivos `.env`;
- documentos pessoais;
- dumps de banco;
- dados de terceiros;
- caminhos ou logs sensíveis desnecessários.

## Arquivo `.gitignore`

Crie um `.gitignore` com pelo menos:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

O `.gitignore` não remove segredos já commitados. Ele apenas evita novos arquivos não rastreados que correspondam às regras.

## Erros comuns

- confundir `git add` com publicação na internet;
- criar commits enormes e sem contexto;
- trabalhar diretamente na branch principal;
- publicar `.env`;
- copiar comandos de remoção de histórico sem compreender;
- usar `git push --force` sem necessidade;
- acreditar que apagar um arquivo remove o segredo do histórico.

## Stop conditions

Pare quando:

- `git status` mostrar arquivo sensível;
- o comando incluir `--force`;
- houver conflito não compreendido;
- você estiver prestes a publicar dados de terceiros;
- a branch de destino não estiver clara.

## Miniavaliação

1. Git e GitHub são a mesma coisa?
2. O que um commit representa?
3. Para que serve uma branch?
4. `git add` envia arquivos ao GitHub?
5. Por que `.gitignore` não resolve um segredo já commitado?

## Evidência mínima

Entregue:

- saída de `git status` limpa;
- saída de `git log --oneline --graph --all`;
- pelo menos duas branches;
- pelo menos três commits pequenos;
- `.gitignore` presente;
- explicação de um risco de segurança evitado.

## Critérios de conclusão

- **funcional:** cria repositório, commit e branch;
- **robusta:** usa histórico e status para explicar o estado;
- **excelente:** mantém commits pequenos, mensagens claras e nenhum dado sensível.

## Próximo passo

A próxima unidade planejada é Z03 — Python essencial. Enquanto ela não estiver implementada, não anuncie a Trilha Zero como concluída.
