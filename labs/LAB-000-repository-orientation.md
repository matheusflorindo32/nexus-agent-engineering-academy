---
id: lab.000.repository-orientation
title: LAB-000 — Orientação no repositório
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 45min
risk_level: low
---

# LAB-000 — Orientação no repositório

## Missão

Validar que a arquitetura NEXUS permite rastrear um conceito desde sua definição até uma prática verificável.

## Hipótese

Uma arquitetura com IDs estáveis e links relativos permite encontrar conceito → módulo → laboratório → template → evidência sem depender de conhecimento tácito.

## Materiais

- Git;
- Python 3.11+;
- editor de texto ou Obsidian;
- cópia local do repositório.

## Preparação

```bash
git clone https://github.com/matheusflorindo32/nexus-agent-engineering-academy.git
cd nexus-agent-engineering-academy
git rev-parse HEAD
python --version
```

Registre a saída antes de continuar.

## Procedimento

1. Execute `python tests/validate_repository.py`.
2. Abra `loops/README.md` ou o índice equivalente disponível.
3. Selecione um conceito: loop, tool, MCP, avaliação ou segurança.
4. Localize o módulo de curso correspondente.
5. Localize um template ou artefato relacionado.
6. Encontre uma fonte oficial citada no conteúdo.
7. Desenhe o caminho em Mermaid.
8. Registre o tempo gasto e qualquer navegação ambígua.

## Evidências

```markdown
- Commit: `<sha>`
- Python: `<versão>`
- Validador: aprovado | reprovado
- Conceito escolhido: `<conceito>`
- Tempo de navegação: `<minutos>`
- Caminho: `<arquivo 1> → <arquivo 2> → ...`
- Ambiguidades: `<lista>`
- Proposta de melhoria: `<texto>`
```

## Critérios de aprovação

- validador executado e saída registrada;
- diagrama com ao menos cinco nós;
- todos os caminhos apontam para arquivos ou fontes existentes;
- commit e versões registrados;
- nenhuma credencial ou dado pessoal incluído;
- autoavaliação concluída.

## Teste adversarial

Peça a outra pessoa — ou a outro agente sem contexto prévio — para repetir o caminho usando apenas sua evidência. Registre onde ela hesitou ou falhou.

## Stop conditions

Pare imediatamente quando:

- houver pedido de credencial;
- for necessária instalação privilegiada não prevista;
- o repositório analisado não puder ser confirmado;
- o mesmo erro ocorrer três vezes;
- o limite de 45 minutos for atingido.

Não contorne controles de segurança. Registre o bloqueio e a próxima ação segura.

## Reflexão final

1. Qual parte dependeu de conhecimento tácito?
2. O que poderia ser validado automaticamente?
3. A estrutura funcionaria igualmente no GitHub e no Obsidian?
4. Qual risco apareceu durante o laboratório?
5. Qual melhoria tem maior impacto e menor custo?

## Entrega

Salve o relatório como:

```text
labs/evidence/LAB-000-<seu-identificador>.md
```

Não inclua e-mail, telefone, token, chave ou outro dado sensível no nome ou conteúdo do arquivo.
