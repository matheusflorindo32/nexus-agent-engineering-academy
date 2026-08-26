---
id: audit.provider-adapters-v3-baseline
title: Provider Adapters V3 — baseline e fontes oficiais
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Adapters V3 — baseline e fontes oficiais

## Escopo

Esta rodada parte do SHA `8cf51f8a046d4b7b4fef37b8f80fe163fc50d579`, head do PR #53 Hardening V2. O PR #53 permanece aberto e não foi mesclado. A nova branch `feat/provider-adapters-v3` foi criada diretamente desse SHA para preservar todo o hardening sem alterar `main`.

## Estado real antes da implementação

O NEXUS já possui, no reference layer, bounded waits, propagação de falha terminal, cancelamento, `operation_id`, `ExecutionReceipt`, idempotência de referência, separação `REQUESTED → APPROVED → EXECUTED → VERIFIED`, Trust Model T0–T7, promoção de Skill por staging/hash/rename atômico, testes unitários e benchmark smoke VAR/RSR/DSER/CTVR.

Ainda não havia adapters executáveis reais e equivalentes para OpenAI Agents SDK, Google ADK e MCP. Portanto, nenhum resultado anterior podia ser interpretado como comparação entre esses frameworks/protocolos.

## Fontes oficiais verificadas em 2026-08-26

### OpenAI Agents SDK

- Repositório oficial: `openai/openai-agents-python`.
- Release estável verificada: `v0.22.0`, publicada em 2026-08-19.
- Changelog oficial informa hardening de runtime, redaction de tool output bloqueado por guardrail, erro explícito para Responses `failed`/`incomplete`, isolamento de usage entre checkpoints e expansão de handoffs em grafos.
- `v0.21.1` adicionou model-call timeouts, networking opcionalmente desabilitado em sandbox e correções relacionadas a approval decisions e cleanup após falhas.
- O SDK permanece em série `0.Y.Z`; mudanças minor podem quebrar interfaces públicas e devem passar por upgrade gate.

### Google ADK Python

- Repositório oficial: `google/adk-python`.
- Release 2.x estável verificada: `v2.7.1`, publicada em 2026-08-17.
- `v2.7.1` restaura ceiling de OpenTelemetry 1.42.1 e valida eventos de inicialização de sessão.
- `v2.7.0` é descrita como correctness release e inclui task mode, melhorias de histórico de chamadas paralelas, eval persistence e instrumentação adicional.
- Issue oficial #6721, aberta em 2026-08-14, descreve possível falha de resume em cenário A2A + human input na 2.7.0. É issue upstream aberta, não advisory e não vulnerabilidade NEXUS reproduzida.

### Model Context Protocol

- Repositório oficial: `modelcontextprotocol/modelcontextprotocol`.
- Especificação estável verificada: `2026-07-28`, publicada em 2026-07-28.
- Mudanças oficiais incluem core stateless, remoção do handshake/sessões de protocolo, `_meta` por request, header-based routing, MRTR, list caching, framework de extensões e hardening de autorização.
- SDKs podem exigir opt-in explícito para falar a revisão `2026-07-28`; compatibilidade deve ser negociada e testada, não presumida.

## Advisories

Foram consultadas fontes públicas oficiais disponíveis (releases, changelogs, documentação e issues oficiais). A interface usada nesta rodada não expõe um catálogo completo de GitHub Security Advisories para esses repositórios; por isso, a ausência de advisory citado aqui **não é evidência de ausência de advisory**. O upgrade gate exige nova verificação antes de cada adoção/version bump.

## Classificação dos achados externos

| Achado | Status NEXUS | Justificativa |
|---|---|---|
| OpenAI 0.22.0 runtime hardening | `MONITORING` | Mudanças relevantes para desenho de adapter; nenhum bug local reproduzido. |
| OpenAI model-call timeout / cleanup de falha | `POTENTIALLY_APPLICABLE` | Alinha-se aos controles NEXUS; será testado por contrato, sem claim sobre runtime real sem SDK instalado. |
| Google ADK #6721 A2A/HITL resume | `POTENTIALLY_APPLICABLE` | NEXUS pretende adapter ADK, mas ainda não existe reprodução local com ADK 2.7.x. |
| Google ADK 2.7.x session correctness | `MONITORING` | Relevante para state integrity; não há incidente local demonstrado. |
| MCP 2026-07-28 stateless core | `MONITORING` | É mudança de protocolo/compatibilidade, não vulnerabilidade. |
| MCP external content / tool metadata as untrusted input | `MITIGATED` no reference layer | Trust Model T0–T7 já impede escalada de T6 para T1 em testes determinísticos; provider-level validation ainda falta. |

## Decisão do milestone

Implementar primeiro **adapters de contrato experimentais** e um harness de paridade, sem chamadas pagas e sem credenciais. Eles normalizam capacidades, riscos, versões e invariantes NEXUS, mas não fingem executar os SDKs reais.

A comparação entre frameworks reais ficará bloqueada até existir ambiente versionado, dependências fixadas, credenciais de teste quando necessárias, mesmos modelos/tarefas e repetição suficiente para variabilidade estocástica.

Princípio: `Upstream finding ≠ NEXUS vulnerability`.
