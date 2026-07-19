---
id: platforms.capability-matrix
title: Matriz comparativa de capacidades e verificação
lang: pt-BR
status: review
version: 0.2.0
reviewed_at: 2026-07-19
---

# Matriz comparativa de capacidades e verificação

## Propósito

Comparar plataformas sem confundir categoria de produto, interface, modelo, SDK, CLI ou agente de software. Esta matriz é um instrumento de verificação, não uma declaração permanente de paridade.

## Escopo inicial

- ChatGPT;
- Codex;
- Claude Code;
- Gemini CLI;
- Kimi K3;
- Kimi K3 Swarm;
- Kimi Agent;
- Kimi Code;
- Kimi API.

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
| Kimi K3 | modelo de fronteira multimodal | raciocínio, conhecimento, contexto longo e tarefas agentic |
| Kimi K3 Swarm | modo agentic de busca e processamento em lote | pesquisa em larga escala, decomposição e execução paralela |
| Kimi Agent | produto agentic autônomo | execução ponta a ponta com ferramentas e produção de artefatos |
| Kimi Code | agente de engenharia de software | trabalho sobre código, arquivos e tarefas de desenvolvimento |
| Kimi API | interface programática | integração de capacidades Kimi em sistemas e agentes próprios |

As categorias acima orientam o currículo e ainda exigem fichas oficiais atualizadas antes de alegar capacidades específicas.

## Matriz operacional inicial

| Capacidade | ChatGPT | Codex | Claude Code | Gemini CLI | Kimi K3 | Kimi Agent | Kimi Code | Critério de verificação |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| conversa geral | U | U | U | U | U | U | U | sessão reproduzível e documentação oficial |
| leitura de repositório | U | U | U | U | U | U | U | projeto de teste fixo |
| edição de múltiplos arquivos | U | U | U | U | U | U | U | diff auditável |
| execução de comandos | U | U | U | U | U | U | U | sandbox e log de comandos |
| execução de testes | U | U | U | U | U | U | U | suíte fixa com resultado esperado |
| criação de commits/PRs | U | U | U | U | U | U | U | permissões e trilha de auditoria |
| aprovação humana antes de efeitos | U | U | U | U | U | U | U | cenário com ação sensível |
| integração MCP | U | U | U | U | U | U | U | servidor MCP de teste e fonte oficial |
| uso de skills/instruções locais | U | U | U | U | U | U | U | contrato local versionado |
| memória persistente | U | U | U | U | U | U | U | definição, escopo e expiração |
| isolamento/sandbox | U | U | U | U | U | U | U | documentação e teste de fronteira |
| telemetria e logs | U | U | U | U | U | U | U | eventos observáveis e exportáveis |
| operação offline | U | U | U | U | U | U | U | execução sem rede |
| suporte multimodal | U | U | U | U | U | U | U | entrada fixa de imagem/PDF |
| automação agendada | U | U | U | U | U | U | U | execução futura verificável |
| contexto ultralongo | U | U | U | U | U | U | U | teste padronizado e documentação oficial |
| execução em lote/swarm | U | U | U | U | U | U | U | conjunto fixo de tarefas e logs |

## Taxonomia oficial inicial do ecossistema Kimi

A documentação oficial consultada em 19 jul. 2026 distingue:

- `Kimi K3`: modelo principal para chat e tarefas agentic;
- `Kimi K3 Swarm`: modo voltado a busca em larga escala e processamento em lote;
- `Kimi Agent`: produto autônomo com múltiplas ferramentas;
- `Kimi Code`: ambiente/agente de desenvolvimento;
- `Kimi API`: acesso programático;
- `Kimi App` e `kimi.com`: superfícies de produto.

Esses componentes não devem ser agrupados em uma única coluna chamada apenas “Kimi”, pois modelo, produto, agente e API possuem contratos e capacidades diferentes.

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
platform: kimi-k3
capability: long-context
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

## Fontes oficiais iniciais do ecossistema Kimi

- Moonshot AI — página oficial do Kimi K3, consultada em 19 jul. 2026;
- Kimi Help Center — visão geral de modelos, consultada em 19 jul. 2026;
- Kimi Help Center — visão geral do Kimi Agent, consultada em 19 jul. 2026.

## Próximas verificações

1. criar ficha oficial do ChatGPT;
2. criar ficha oficial do Codex;
3. criar ficha oficial do Claude Code;
4. criar ficha oficial do Gemini CLI;
5. criar fichas separadas para Kimi K3, K3 Swarm, Kimi Agent, Kimi Code e Kimi API;
6. executar o mesmo repositório-laboratório nas plataformas compatíveis;
7. publicar resultados e divergências conforme a [política de fontes](../docs/standards/source-evidence-policy.md).
