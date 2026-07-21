---
id: course.zero-track.z04
title: Z04 — Markdown, JSON e YAML
lang: pt-BR
status: review
prerequisites: [course.zero-track.z03]
estimated_hours: 4
---

# Z04 — Markdown, JSON e YAML

> **Estado:** conteúdo em revisão pedagógica. Ainda não foi validado com turma piloto.

## Para quem é

Para quem já consegue executar scripts simples em Python, mas ainda confunde texto de documentação com dados estruturados e arquivos de configuração.

## Resultado final

Ao concluir, você deverá conseguir:

- escrever documentação básica em Markdown;
- criar e validar JSON;
- ler e editar YAML simples;
- diferenciar documentação, dados e configuração;
- detectar erros comuns de sintaxe;
- evitar inserir segredos em arquivos versionados.

## Por que isso importa

Projetos agentic usam Markdown para documentação, JSON para troca de dados e YAML para contratos e configuração. Pequenos erros nesses formatos podem quebrar automações, testes e agentes.

## Camada 1 — linguagem simples

- Markdown organiza texto.
- JSON organiza dados com regras rígidas.
- YAML organiza configurações com menos símbolos, mas exige cuidado com indentação.

## Camada 2 — explicação profissional

Markdown é linguagem de marcação leve. JSON representa estruturas de dados interoperáveis. YAML é uma linguagem de serialização frequentemente usada em configuração e contratos legíveis por humanos.

## Camada 3 — implementação

### Markdown

```markdown
# Título

## Objetivo

- item 1
- item 2

```bash
python app.py
```
```

### JSON

```json
{
  "agent": "triage-readonly",
  "max_steps": 5,
  "requires_approval": true
}
```

### YAML

```yaml
agent: triage-readonly
max_steps: 5
requires_approval: true
```

## Conceitos essenciais

- chave e valor;
- lista;
- objeto ou mapa;
- string, número, booleano e nulo;
- indentação;
- aspas;
- escaping;
- schema;
- validação.

## Prática guiada

1. Crie `README.md` com título, objetivo, comandos e checklist.
2. Crie `config.json` com nome, versão, limite de passos e aprovação humana.
3. Crie `config.yaml` com os mesmos dados.
4. Valide o JSON usando Python:

```bash
python -m json.tool config.json
```

5. Compare as diferenças entre os três formatos.

## Prática independente

Crie uma especificação mínima de agente em YAML com:

- objetivo;
- não objetivos;
- entradas;
- saídas;
- ferramentas;
- permissões;
- budgets;
- stop conditions.

Depois, explique em Markdown por que cada campo existe.

## Erros comuns

- vírgula final inválida em JSON;
- usar aspas simples como se JSON fosse Python;
- misturar tabs e espaços em YAML;
- alterar indentação sem perceber;
- usar YAML complexo demais para iniciantes;
- salvar segredo em arquivo de configuração;
- tratar um arquivo legível como prova de validade.

## Stop conditions

Pare quando:

- o arquivo contém token, senha ou chave real;
- a validação falha e você não consegue localizar a linha;
- um exemplo depende de recurso externo não explicado;
- o YAML usa recursos avançados que você ainda não entende.

## Teste de segurança

Procure manualmente por termos como:

```text
password
token
secret
api_key
```

Use apenas placeholders curtos e claramente falsos, como `example-value`.

## Evidência mínima

- `README.md` bem estruturado;
- `config.json` validado;
- `config.yaml` equivalente;
- explicação das diferenças;
- commit sem segredo.

## Critérios de conclusão

- [ ] Sei quando usar Markdown, JSON e YAML.
- [ ] Consigo validar JSON.
- [ ] Reconheço erro de indentação em YAML.
- [ ] Consigo representar listas e objetos.
- [ ] Não armazeno credenciais no repositório.

## Autoavaliação

Explique por que “parece correto” não é suficiente para validar um arquivo estruturado.

## Próximo passo

Siga para [Z05 — HTTP, APIs, chaves e variáveis de ambiente](../Z05-http-apis-chaves/README.md).
