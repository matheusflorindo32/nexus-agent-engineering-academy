---
id: course.zero-track.z05
title: Z05 — HTTP, APIs, chaves e variáveis de ambiente
lang: pt-BR
status: review
prerequisites: [course.zero-track.z04]
estimated_hours: 5
---

# Z05 — HTTP, APIs, chaves e variáveis de ambiente

> **Estado:** conteúdo em revisão pedagógica. Ainda não foi validado com turma piloto.

## Para quem é

Para pessoas que já conseguem ler Python, JSON e YAML, mas ainda não entendem como programas trocam informações ou como credenciais devem ser protegidas.

## Resultado final

Ao concluir, você deverá conseguir:

- explicar requisição, resposta, método, URL, cabeçalhos e corpo;
- diferenciar API de interface gráfica;
- reconhecer códigos HTTP comuns;
- explicar autenticação sem expor credenciais;
- usar variáveis de ambiente de forma básica;
- recusar exemplos que pedem chave real sem necessidade;
- testar um contrato de API com dados sintéticos e sem internet.

## Por que isso importa

Agentes usam APIs e ferramentas para agir. Uma integração mal compreendida pode vazar credenciais, enviar dados ao destino errado, repetir operações ou interpretar falhas como sucesso.

## Camada 1 — linguagem simples

Uma API é como um balcão de atendimento entre programas. A requisição faz um pedido. A resposta informa o resultado. A chave de API funciona como uma credencial e não deve aparecer no código, em prints ou no Git.

## Camada 2 — explicação profissional

HTTP define semântica de métodos, endereçamento, cabeçalhos, status e payloads. Autenticação identifica ou autoriza o cliente. Variáveis de ambiente separam configuração sensível do código, mas não tornam o segredo automaticamente seguro.

## Camada 3 — implementação

Modelo sintético de requisição:

```json
{
  "method": "POST",
  "path": "/v1/tasks",
  "headers": {
    "content-type": "application/json",
    "authorization": "Bearer example-value"
  },
  "body": {
    "title": "revisar laboratório"
  }
}
```

Neste material, `example-value` é um placeholder curto e falso. Nunca substitua por credencial real.

## Conceitos essenciais

- URL: endereço do recurso;
- método: intenção da operação, como GET ou POST;
- cabeçalho: metadado da requisição;
- corpo: dados enviados;
- status: resultado padronizado;
- timeout: limite de espera;
- retry: nova tentativa controlada;
- autenticação: comprovação de identidade;
- autorização: permissão para agir;
- variável de ambiente: configuração fornecida fora do código.

## Códigos HTTP iniciais

| Código | Significado prático |
|---:|---|
| 200 | operação concluída |
| 201 | recurso criado |
| 400 | entrada inválida |
| 401 | autenticação ausente ou inválida |
| 403 | identidade conhecida, mas sem permissão |
| 404 | recurso não encontrado |
| 409 | conflito, como duplicidade |
| 429 | limite de uso atingido |
| 500 | falha interna do serviço |

## Demonstração local segura

Execute o simulador sem rede:

```bash
python course/zero-track/scripts/simulate_api_contract.py
```

Ele simula requisições e respostas em memória. Não abre conexão, não lê credenciais e não acessa variáveis de ambiente.

## Variáveis de ambiente

Exemplo conceitual em Python:

```python
import os

api_key = os.environ.get("EXAMPLE_API_KEY")
if not api_key:
    raise RuntimeError("EXAMPLE_API_KEY não configurada")
```

Este exemplo mostra leitura, mas você não deve configurar chave real durante a Trilha Zero. O objetivo é entender o contrato e o risco.

## Prática guiada

1. Execute o simulador local.
2. Observe casos 200, 400, 401 e 409.
3. Explique por que 401 e 403 não são iguais.
4. Altere apenas dados sintéticos.
5. Registre a saída em `evidencia-z05.txt`.
6. Identifique onde um retry seria permitido e onde poderia duplicar efeitos.

## Prática independente

Desenhe um contrato de API para criar uma tarefa com:

- método e caminho;
- corpo JSON;
- resposta de sucesso;
- resposta de entrada inválida;
- conflito por idempotency key repetida;
- regra para não registrar o cabeçalho de autorização.

## Erros comuns

- colar chave no código;
- enviar segredo em URL;
- imprimir todos os cabeçalhos;
- confundir 401 com 403;
- repetir POST sem idempotência;
- não definir timeout;
- interpretar qualquer resposta como sucesso;
- colocar `.env` real no Git.

## Stop conditions

Pare imediatamente quando:

- alguém solicitar uma chave real para concluir o exercício;
- o exemplo tenta acessar serviço externo sem explicação;
- o código imprime autorização, cookies ou variáveis de ambiente;
- a operação pode cobrar, excluir ou publicar algo;
- não houver confirmação de endpoint, ambiente ou permissão.

## Teste de segurança

Confirme que:

- somente placeholders falsos são usados;
- nenhum `.env` real foi criado;
- logs não exibem `authorization`;
- a simulação não abre rede;
- operações de escrita usam chave de idempotência no desenho do contrato.

## Evidência mínima

- saída do simulador;
- contrato de API em JSON ou YAML;
- tabela de status esperados;
- explicação sobre autenticação versus autorização;
- checklist de proteção de credenciais.

## Critérios de conclusão

- [ ] Explico requisição e resposta.
- [ ] Reconheço os principais status HTTP.
- [ ] Não armazeno chave no código ou no Git.
- [ ] Sei por que logs devem redigir autorização.
- [ ] Identifico risco de retry em operações de escrita.

## Autoavaliação

Explique por que usar variável de ambiente reduz exposição acidental, mas não elimina a necessidade de controle de acesso, rotação e redaction.

## Próximo passo

Siga para Z06 — segurança básica e proteção de segredos, ainda planejado.
