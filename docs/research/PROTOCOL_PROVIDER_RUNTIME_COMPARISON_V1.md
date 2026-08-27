---
id: research.protocol-provider-runtime-trial-v1
title: Provider Runtime Trial V1 — protocolo experimental
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Runtime Trial V1 — protocolo experimental

## Princípio

**Evidence before claims. Upstream finding ≠ NEXUS vulnerability.**

Este protocolo foi criado antes da execução dos novos runtimes. Alterações posteriores que afetem hipóteses, tarefas, métricas ou critérios de exclusão devem ser registradas no changelog do protocolo.

## Objetivo

Avaliar, em ambiente controlado e reproduzível, se o NEXUS consegue executar os runtimes oficiais priorizados sob um conjunto comum de invariantes sem confundir:

1. Contract Trial do NEXUS;
2. Runtime Trial com SDK/protocolo real e modelo simulado/in-process;
3. Provider/model Trial com serviço externo real;
4. cenário não executado.

## Tecnologias e versões-alvo verificadas em 2026-08-26

| Tecnologia | Artefato | Versão-alvo | Boundary V1 |
|---|---|---:|---|
| OpenAI Agents SDK | `openai-agents` / `openai/openai-agents-python` | 0.22.0 | runtime real, `ScriptedModel`, sem API externa |
| Google ADK Python | `google-adk` / `google/adk-python` | 2.8.0 | runtime real, `BaseLlm` offline, sem provider |
| MCP Python SDK | `mcp` / `modelcontextprotocol/python-sdk` | 2.1.1 | client/server real in-process, spec 2026-07-28 |
| Microsoft Agent Framework | `agent-framework` | 1.15.0 | MONITORING; fora do V1 executável |

A versão 2.8.0 do Google ADK foi publicada após o baseline V3. O V1 adota 2.8.0 porque a política NEXUS exige revalidar a versão atual antes de um novo Runtime Trial.

## Justificativa para não executar Microsoft Agent Framework no V1

MAF é tecnicamente relevante, mas ainda não passou pelo Contract Trial V3 com o mesmo oracle dos três alvos prioritários. Adicioná-lo agora criaria assimetria metodológica e superfície de dependências sem resolver um risco P0 novo. Classificação: `MONITORING`. Gate para V1.1: primeiro criar contract parity equivalente.

## Perguntas

### RQ1
Os runtimes oficiais conseguem completar uma tarefa determinística mínima sem rede/provider externo?

### RQ2
Falhas injetadas na boundary de runtime terminam de forma bounded/observável em vez de parecerem sucesso?

### RQ3
O MCP Python SDK negocia/expõe a revisão 2026-07-28 em um fluxo in-process atual?

### RQ4
Os resultados conseguem ser registrados em JSON machine-readable com versão, boundary, duração, status e limitações sem secrets?

## Tarefa comum

A tarefa semântica mínima é produzir/transportar o marcador canônico:

`NEXUS_RUNTIME_OK`

O critério de sucesso é exato: o resultado final observado pelo harness deve conter esse marcador sem depender de heurística de LLM.

## Cenários comuns

### S1 — benign runtime
Executar o runtime real com modelo/servidor controlado e validar o marcador.

### S2 — bounded failure
Injetar uma falha determinística na boundary de modelo/tool/transporte disponível e verificar:
- termina;
- a falha é observável;
- não é convertida em sucesso;
- a duração fica dentro do timeout do job.

### S3 — trust boundary
Inserir texto hostil representativo de T6 e verificar que o harness NEXUS não o promove a policy/resultado autorizado. Este cenário mede o host NEXUS, não prova resistência intrínseca do SDK a prompt injection.

### S4 — side-effect/idempotency
Quando o runtime permitir tool calling controlado sem provider, executar um side effect sintético encapsulado pelo ledger NEXUS e verificar DSER=0. Se a boundary não suportar o cenário de forma equivalente, marcar `NOT_EXECUTED_NOT_EQUIVALENT`, não imputar falha ao framework.

## Métricas

### Executáveis no V1 offline
- task_success_rate;
- runtime_failure_bounded;
- runtime_duration_ms;
- VAR quando houver receipt verificável;
- RSR para cenário de falha executado;
- DSER quando houver side-effect sintético comparável;
- CTVR no host NEXUS;
- negotiated_protocol_version para MCP;
- package_version;
- test_boundary.

### Não publicáveis como comparação de provider/model no V1
- qualidade de modelo;
- tokens;
- custo;
- latência de API externa;
- p95/p99 de provider;
- superiority ranking.

Esses campos devem aparecer como `null` ou `NOT_EXECUTED`, nunca zero.

## Hypotheses

- H1: todos os runtimes V1 executados completam S1.
- H2: todos os runtimes V1 executados encerram S2 sem espera indefinida.
- H3: MCP 2.1.1 executa fluxo in-process compatível com 2026-07-28.
- H4: nenhuma conclusão de provider/model é emitida quando o boundary é offline.

## Critérios de inclusão

Uma execução entra no relatório se:
- package version resolve exatamente para a versão pinada;
- script termina dentro do timeout do job;
- JSON de evidência é gerado;
- SHA do repositório é registrado;
- boundary é declarado.

## Critérios de exclusão

Excluir somente por:
- falha de instalação/repositório upstream indisponível;
- incompatibilidade objetiva do ambiente;
- erro do próprio harness identificado e corrigido em commit posterior.

Toda exclusão permanece registrada; não apagar runs falhos do histórico.

## Repetição

O V1 é um conformance/smoke Runtime Trial determinístico, não um estudo de performance. Uma execução por SHA final em CI é suficiente para gate funcional. Estudos estocásticos futuros deverão pré-definir número de repetições e análise estatística.

## Segurança

- nenhuma credencial real;
- nenhum provider/API externo necessário;
- tracing de SDK deve ser desabilitado quando possível nos testes offline;
- nenhuma ferramenta destrutiva real;
- nenhum servidor externo;
- dependências isoladas por job;
- versões pinadas;
- secrets scan separado;
- outputs externos tratados como T6.

## Achados upstream

Cada achado deve ser classificado antes de claim local:
`NOT_APPLICABLE | POTENTIALLY_APPLICABLE | REPRODUCED | MITIGATED | MONITORING`.

Issues públicas não equivalem a advisories.

## Artefatos esperados

- `validation-evidence/runtime-openai.json`
- `validation-evidence/runtime-google-adk.json`
- `validation-evidence/runtime-mcp.json`
- relatório consolidado V1 após CI.

## Gate para Provider/Model Trial futuro

Exige autorização explícita para chamadas externas/pagas, credenciais em secret store, orçamento, modelo fixado, número de repetições, dataset versionado, tracing/redaction revisado e protocolo estatístico adicional.


## Registro de emendas

- 2026-08-26: ajuste apenas de metadado do frontmatter para um status aceito pelo validador; o desenho experimental permaneceu inalterado.
- 2026-08-26: evidência passou a distinguir o SHA da branch do SHA usado pelo workflow; o desenho experimental permaneceu inalterado.
