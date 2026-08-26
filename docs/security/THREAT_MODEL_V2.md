---
id: security.threat-model-v2
title: Threat Model V2 — NEXUS Agent Engineering Academy
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Threat Model V2

## Objetivo

Modelar ameaças em todas as fronteiras relevantes do NEXUS, assumindo que modelos, tools, Skills, MCP, memória e conteúdo externo podem falhar ou ser adversariais.

## Ativos críticos

- integridade de instruções de sistema e repositório;
- identidade e intenção do usuário;
- credenciais e tokens;
- integridade de Skills e dependências;
- estado/memória do agente;
- dados e documentos externos;
- ferramentas e servidores MCP;
- execução de side effects;
- logs/traces;
- CI/CD e artefatos;
- datasets e resultados de benchmark.

## Trust model de contexto

| Nível | Origem | Regra |
|---|---|---|
| T0 | System / immutable policy | Autoridade máxima; não pode ser alterada por conteúdo inferior. |
| T1 | Instruções controladas pelo repositório | Confiáveis após review/merge; sujeitas a versionamento. |
| T2 | Skills aprovadas | Confiáveis apenas dentro das permissões declaradas e versão auditada. |
| T3 | Tools confiáveis | Saída ainda deve ser validada; tool confiável não implica dado verdadeiro. |
| T4 | Dados do usuário | Autorizados como input, não como política global. |
| T5 | Documentos externos | Dados não confiáveis. |
| T6 | Web/MCP/third-party | Dados e metadados não confiáveis; risco elevado de indirect injection. |
| T7 | Desconhecido/adversarial | Isolar, minimizar, rejeitar ações derivadas sem validação adicional. |

Regra de não escalada: conteúdo de nível inferior não pode ampliar permissões, reclassificar sua própria confiança ou substituir política de nível superior.

## Fronteiras principais

### Conteúdo externo → modelo

- **Ameaça:** prompt injection direta/indireta, instruções codificadas, conteúdo oculto.
- **Impacto:** desvio de objetivo, exfiltração, tool abuse.
- **Controles:** provenance labels, minimização, parsing estruturado, policy gate externo ao modelo, allowlists e testes adversariais.
- **Risco residual:** médio; classificadores não são autoridade final.

### Modelo → tool

- **Ameaça:** parâmetros incorretos, ação não autorizada, hallucinated target, abuso de side effects.
- **Impacto:** alteração/exclusão/publicação indevida.
- **Controles:** schemas estritos, autorização determinística, dry-run, approval scoped, idempotency, execution receipts.
- **Risco residual:** médio até receipts/idempotência estarem implementados.

### Agent/Orchestrator → A2A peer

- **Ameaça:** confused deputy, forged approval, state contamination, semantic loss on resume.
- **Impacto:** bypass de approval, ação não executada porém declarada concluída, handoff inconsistente.
- **Controles:** identity-bound approval, operation IDs, typed resume contracts, state isolation, verified receipts.
- **Risco residual:** alto em adapters experimentais até testes específicos passarem.

### Host → MCP server

- **Ameaça:** tool poisoning, malicious descriptions, server discovery injection, credential forwarding, excessive scope.
- **Impacto:** exfiltração, abuso de filesystem/network, privilege escalation.
- **Controles:** registry/provenance, schema pinning, OAuth audience/resource validation, no token passthrough, egress restrictions, sandboxing.
- **Risco residual:** médio/alto para MCP externo não auditado.

### Skill registry → runtime

- **Ameaça:** race condition, partial write, malicious Skill, dependency confusion, post-install scripts.
- **Impacto:** instruções/código comprometidos, loader inconsistente, supply-chain compromise.
- **Controles:** staging, audit, immutable versions, hash, atomic promotion, rollback, no auto-execution of scripts.
- **Risco residual:** alto enquanto o registry não estiver implementado.

### Memory/vector DB → model

- **Ameaça:** memory poisoning, stale context, provenance loss.
- **Impacto:** instrução hostil persistente, decisão baseada em estado obsoleto.
- **Controles:** provenance, TTL, namespace isolation, mutation audit, trust labels, invalidation.
- **Risco residual:** médio.

### CI/dependency registry → release

- **Ameaça:** compromised dependency, secret leakage, malicious action, unreviewed major upgrade.
- **Impacto:** código comprometido ou comportamento agentic alterado silenciosamente.
- **Controles:** pinned actions/dependencies quando apropriado, lockfiles, secret scan, dependency review, framework upgrade gate.
- **Risco residual:** médio até upgrade gate completo.

## Side-effect lifecycle

Toda ação externa relevante deve obedecer:

```text
REQUESTED
  → AUTHORIZED
  → APPROVED (quando exigido)
  → EXECUTED
  → VERIFIED
  → RECONCILED
```

Um estado não prova o seguinte. Especialmente, `APPROVED ≠ EXECUTED` e texto do LLM `≠ VERIFIED`.

## Execution Receipt mínimo

- `operation_id`
- `tool_name`
- `requested_at`
- `principal`
- `approval_id` quando aplicável
- `executed_at`
- `status`
- `resource_id`/target verificável
- `result_hash` quando aplicável
- `retry_count`

## Cenários prioritários de teste

1. indirect prompt injection via MCP/tool output;
2. forged HITL response from remote peer;
3. duplicate retry after ambiguous transport failure;
4. partial success with parallel tool calls;
5. corrupted/stale memory;
6. Skill updated while runtime is loading it;
7. server/tool metadata altered between approval and execution;
8. secret present in log/trace payload;
9. context trust violation T6/T7 → T1/T0 behavior;
10. dependency/framework upgrade changing action semantics.

## Critério de aceite V2

O threat model só poderá ser marcado `accepted` quando os controles P0 tiverem pelo menos um teste regressivo executado em CI e os riscos residuais estiverem registrados.