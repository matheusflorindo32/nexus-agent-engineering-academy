---
id: course.zero-track.index
title: Trilha Zero — Fundamentos para começar
lang: pt-BR
status: review
---

# Trilha Zero — Fundamentos para começar

A Trilha Zero prepara pessoas sem experiência prévia em programação para entrar no currículo NEXUS com menos dependência de ajuda externa.

> **Estado:** piloto. A existência destes materiais não significa validação pedagógica concluída.

## Para quem é

- pessoas que nunca usaram terminal;
- estudantes que ainda confundem arquivo, pasta, programa e processo;
- iniciantes que nunca trabalharam com Git ou GitHub;
- pessoas que desejam revisar fundamentos antes do Módulo 00.

## Como estudar

Cada unidade segue o ciclo:

```text
explicação simples → demonstração → prática guiada → prática independente → evidência → reflexão
```

Não avance apenas porque leu. Avance quando conseguir produzir a evidência solicitada.

## Unidades implementadas

| Unidade | Tema | Evidência mínima |
|---|---|---|
| [Z00](Z00-computador-e-ambiente/README.md) | computador, arquivos, programas e ambiente | relatório do verificador de ambiente |
| [Z01](Z01-terminal-sem-medo/README.md) | navegação e operações seguras no terminal | transcript com criação, leitura e remoção controlada |
| [Z02](Z02-git-e-github-essenciais/README.md) | Git, commit, branch e GitHub | repositório local com histórico compreensível |
| [Z03](Z03-python-essencial/README.md) | Python essencial | script, testes e falha explicada |
| [Z04](Z04-markdown-json-yaml/README.md) | Markdown, JSON e YAML | documentação e configurações validadas |
| [Z05](Z05-http-apis-chaves/README.md) | HTTP, APIs e proteção de credenciais | contrato de API e simulação local segura |
| [Z06](Z06-seguranca-e-segredos/README.md) | segurança básica e proteção de segredos | política curta, `.gitignore` e varredura sintética |
| [Z07](Z07-clonar-executar-testar-corrigir/README.md) | clonar, executar, testar e corrigir | baseline, diff pequeno e evidência antes/depois |
| [Z08](Z08-primeiro-workflow/README.md) | primeiro workflow determinístico | execução, falha, retry idempotente e testes |

## Unidade planejada

- Z09 — primeiro agente simples.

## Gate de saída desta etapa

A pessoa pode avançar quando consegue:

- identificar sistema operacional e versão do Python;
- navegar por pastas sem interface gráfica;
- criar, ler, mover e excluir arquivos de teste;
- explicar a diferença entre Git e GitHub;
- criar um repositório local, registrar um commit e abrir uma branch;
- executar um script Python e interpretar um traceback;
- diferenciar Markdown, JSON e YAML;
- explicar requisição, resposta, autenticação e autorização;
- proteger credenciais em código, configuração e logs;
- clonar, testar e corrigir um projeto sem enfraquecer os testes;
- modelar um workflow com stop conditions e idempotência;
- mostrar evidências do que executou.

## Segurança

- nunca cole credenciais reais;
- não execute comandos destrutivos que não entende;
- use somente pastas de laboratório;
- registre erros e dúvidas em vez de ocultá-los;
- pare quando houver risco de perda de dados ou exposição de segredo.
