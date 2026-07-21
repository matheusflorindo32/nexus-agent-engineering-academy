---
id: course.zero-track.z03
title: Z03 — Python essencial
lang: pt-BR
status: review
prerequisites: [course.zero-track.z02]
estimated_hours: 6
---

# Z03 — Python essencial

> **Estado:** conteúdo em revisão pedagógica. Ainda não foi validado com turma piloto.

## Para quem é

Para pessoas que já conseguem usar o terminal, criar arquivos e registrar alterações com Git, mas ainda não conseguem ler ou escrever um programa simples em Python.

## Resultado final

Ao concluir, você deverá conseguir:

- executar um arquivo Python pelo terminal;
- usar variáveis, tipos básicos, condições, repetições e funções;
- ler mensagens de erro sem apagar evidências;
- transformar uma entrada simples em saída estruturada;
- escrever e executar testes básicos com `unittest`;
- reconhecer código inseguro ou que tenta acessar dados desnecessários.

## Por que isso importa

Agentes, ferramentas, avaliações e automações são implementados como programas. Sem entender o fluxo básico de um programa, a pessoa fica dependente de copiar código sem conseguir verificar o que ele faz.

## Diagnóstico inicial

Tente responder sem pesquisar:

1. Qual a diferença entre texto, número inteiro e valor verdadeiro/falso?
2. O que acontece quando uma condição é verdadeira?
3. Por que uma função recebe parâmetros?
4. O que uma mensagem de erro informa?

Não saber ainda é esperado.

## Camada 1 — linguagem simples

Um programa é uma receita escrita para o computador. Variáveis guardam valores, condições escolhem caminhos, laços repetem tarefas e funções organizam passos reutilizáveis.

## Camada 2 — explicação profissional

Python executa instruções em ordem, mantendo estado em memória. Tipos definem operações válidas. Funções criam contratos entre entrada e saída. Exceções representam falhas que precisam ser tratadas ou registradas.

## Camada 3 — implementação

Crie `primeiro_programa.py`:

```python
from __future__ import annotations


def classificar_tarefa(nome: str, urgente: bool) -> dict[str, object]:
    prioridade = "alta" if urgente else "normal"
    return {"nome": nome.strip(), "prioridade": prioridade}


if __name__ == "__main__":
    resultado = classificar_tarefa("revisar laboratório", True)
    print(resultado)
```

Execute:

```bash
python primeiro_programa.py
```

## Conceitos essenciais

- variável: nome que referencia um valor;
- tipo: regras associadas ao valor;
- condição: decisão baseada em expressão booleana;
- repetição: execução controlada de um bloco;
- função: contrato reutilizável;
- exceção: falha detectada durante a execução;
- teste: exemplo automatizado que verifica comportamento esperado.

## Exemplo mínimo

```python
nome = "NEXUS"
print(nome)
```

## Exemplo intermediário

```python
tarefas = ["ler", "testar", "documentar"]
for tarefa in tarefas:
    print(tarefa.upper())
```

## Exemplo realista

```python
def validar_limite(passos: int, limite: int = 5) -> bool:
    if passos < 0:
        raise ValueError("passos não pode ser negativo")
    return passos <= limite
```

Esse padrão aparece em budgets e stop conditions de agentes.

## Prática guiada

1. Crie uma pasta `z03-lab`.
2. Crie `tarefas.py`.
3. Escreva uma função que recebe nome e duração estimada.
4. Rejeite duração negativa com `ValueError`.
5. Retorne um dicionário.
6. Execute três casos válidos e um inválido.
7. Registre a saída em `evidencia-z03.txt`.

## Prática independente

Implemente uma função que classifica uma tarefa como `curta`, `media` ou `longa` e escreva três testes com `unittest`.

## Erros comuns

- misturar texto e número sem conversão;
- ignorar indentação;
- capturar qualquer exceção sem explicar a causa;
- executar código copiado sem ler;
- colocar segredo diretamente no arquivo;
- apagar a mensagem de erro em vez de registrá-la.

## Stop conditions

Pare e peça revisão quando:

- o script solicita senha, token ou chave real;
- o código tenta excluir arquivos fora da pasta de laboratório;
- você não entende uma dependência solicitada;
- o erro sugere acesso a rede, sistema ou credenciais sem necessidade.

## Teste de segurança

Verifique que o programa:

- não lê variáveis de ambiente;
- não acessa internet;
- não abre arquivos fora da pasta de laboratório;
- usa apenas dados sintéticos;
- não imprime informações pessoais.

## Evidência mínima

- arquivo Python executável;
- três testes automatizados;
- uma falha proposital registrada;
- explicação curta sobre a causa e a correção;
- commit com mensagem compreensível.

## Critérios de conclusão

- [ ] Consigo explicar variável, condição, laço e função.
- [ ] Executo um script pelo terminal.
- [ ] Leio o traceback antes de alterar o código.
- [ ] Escrevo pelo menos três testes.
- [ ] Não uso credenciais reais.

## Autoavaliação

Explique, com suas palavras, por que um teste deve verificar comportamento e não apenas confirmar que o programa “rodou”.

## Próximo passo

Siga para [Z04 — Markdown, JSON e YAML](../Z04-markdown-json-yaml/README.md).
