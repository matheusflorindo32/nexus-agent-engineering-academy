---
id: platforms.capability-matrix
title: Matriz comparativa de capacidades e verificação
lang: pt-BR
status: review
version: 0.1.0
reviewed_at: 2026-07-19
---

# Matriz comparativa de capacidades e verificação

## Propósito

Comparar plataformas sem confundir categoria de produto, interface, modelo, SDK, CLI ou agente de software. Esta matriz é um instrumento de verificação, não uma declaração permanente de paridade.

## Escopo inicial

- ChatGPT;
- Codex;
- Claude Code;
- Gemini CLI.

## Legenda

- `S`: suportado e verificado;
- `P`: suporte parcial ou condicionado;
- `N`: não suportado no escopo verificado;
- `U`: desconhecido ou ainda não verificado;
- `A`: não aplicável à categoria.

Toda célula diferente de `U` deve apontar para uma ficha de adapter com fonte oficial, versão e data.

## Diferença de categoria

| Plataforma | Categoria NEXUS | Uso principal no curso |
|---|---|---|
| ChatGPT | produto conversacional e ambiente de ferramentas | interação, pesquisa, análise e orquestração assistida |
| Codex | agente de engenharia de software | trabalho sobre repositórios, código, testes e mudanças versionadas |
| Claude Code | agente/CLI de engenharia de software | leitura e modificação de bases de código com fluxo terminal |
| Gemini CLI | agente/CLI para desenvolvimento | tarefas de terminal, código, arquivos e integrações compatíveis |

As categorias acima orientam o currículo e ainda exigem fichas oficiais atualizadas antes de alegar capacidades específicas.

## Matriz operacional inicial

| Capacidade | ChatGPT | Codex | Claude Code | Gemini CLI | Critério de verificação |
|---|:---:|:---:|:---:|:---:|---|
| conversa geral | U | U | U | U | sessão reproduzível e documentação oficial |
| leitura de repositório | U | U | U | U | projeto de teste fixo |
| edição de múltiplos arquivos | U | U | U | U | diff auditável |
| execução de comandos | U | U | U | U | sandbox e log de comandos |
| execução de testes | U | U | U | U | suíte fixa com resultado esperado |
| criação de commits/PRs | U | U | U | U | permissões e trilha de auditoria |
| aprovação humana antes de efeitos | U | U | U | U | cenário com ação sensível |
| integração MCP | U | U | U | U | servidor MCP de teste e fonte oficial |
| uso de skills/instruções locais | U | U | U | U | contrato local versionado |
| memória persistente | U | U | U | U | definição, escopo e expiração |
| isolamento/sandbox | U | U | U | U | documentação e teste de fronteira |
| telemetria e logs | U | U | U | U | eventos observáveis e exportáveis |
| operação offline | U | U | U | U | execução sem rede |
| suporte multimodal | U | U | U | U | entrada fixa de imagem/PDF |
| automação agendada | U | U | U | U | execução futura verificável |

## Protocolo de preenchimento

Para alterar qualquer `U`:

1. identificar a categoria e o produto exato;
2. registrar versão, plano e ambiente;
3. consultar documentação oficial atual;
4. criar caso mínimo reproduzível;
5. executar teste benigno e adversarial;
6. registrar resultado, limitação e evidência;
7. revisar por segunda pessoa ou agente revisor;
8. definir `verified_at` e data de expiração.

## Dimensões de comparação

### Engenharia

- leitura e escrita de arquivos;
- compreensão de repositório;
- execução de testes;
- qualidade do diff;
- rollback;
- trabalho em branch;
- rastreabilidade.

### Controle

- budgets;
- stop conditions;
- aprovação humana;
- permissões por ferramenta;
- isolamento;
- recuperação de falhas.

### Contexto

- tamanho e seleção;
- arquivos e fontes;
- proveniência;
- memória;
- compressão;
- defesa contra instrução incorporada.

### Operação

- instalação;
- autenticação;
- custo;
- limites de uso;
- logs;
- integrações;
- disponibilidade por plano ou região.

### Segurança

- gerenciamento de segredos;
- acesso ao sistema de arquivos;
- execução de shell;
- rede;
- MCP e ferramentas externas;
- políticas empresariais;
- retenção de dados.

## Ficha mínima de evidência

```yaml
platform: codex
capability: run-tests
status: U
verified_version: null
verified_at: null
expires_at: null
official_sources: []
test_case: null
result: null
limitations: []
reviewer: null
```

## Regras editoriais

- não usar “melhor” sem cenário, métrica e evidência;
- não comparar plano gratuito com plano empresarial sem declarar a diferença;
- não tratar modelo e produto como sinônimos;
- não extrapolar uma demonstração para disponibilidade geral;
- não assumir que uma capacidade de interface existe na API ou CLI;
- marcar rapidamente como `stale` quando houver mudança material.

## Próximas verificações

1. criar ficha oficial do ChatGPT;
2. criar ficha oficial do Codex;
3. criar ficha oficial do Claude Code;
4. criar ficha oficial do Gemini CLI;
5. executar o mesmo repositório-laboratório nas quatro plataformas;
6. publicar resultados e divergências conforme a [política de fontes](../docs/standards/source-evidence-policy.md).
