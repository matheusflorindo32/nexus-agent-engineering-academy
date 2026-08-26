---
id: audit.hardening-v2-report
title: Hardening V2 — Relatório de implementação
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Hardening V2 — Relatório de implementação

## Objetivo

Elevar o NEXUS em quatro dimensões que não estavam formalizadas na fundação: reliability de transporte, integridade HITL/side effects, supply chain de Skills e governança de upgrades.

## Implementado nesta branch

### Governança e auditoria

- `docs/audits/CURRENT_STATE_AUDIT.md`
- `docs/audits/EXTERNAL_FINDINGS_APPLICABILITY.md`
- `docs/audits/INDEPENDENT_REVIEW_SCORECARD.md`
- `docs/security/THREAT_MODEL_V2.md`
- `docs/security/SKILL_SUPPLY_CHAIN_SECURITY.md`
- `docs/reliability/AGENT_RELIABILITY_MODEL.md`
- `docs/radar/AGENT_TECH_RADAR.md`
- `docs/governance/FRAMEWORK_UPGRADE_POLICY.md`
- `docs/research/RESEARCH_READINESS_V2.md`
- `docs/governance/NEXT_MILESTONE.md`

### Código de referência

`examples/agent_reliability_runtime.py` adiciona, sem rede e sem side effects reais:

- canal com espera limitada;
- persistência de falha terminal para leitores futuros;
- cancelamento explícito;
- `ActionLedger` com `operation_id`;
- approval scoped por principal/operação;
- `ExecutionReceipt`;
- execução idempotente de referência com retry contabilizado sem repetição de efeito;
- verificação distinta de execução;
- Skill staging + SHA-256 + promoção por rename atômico;
- modelo T0–T7 para não escalada de confiança.

### Skills

Foi adicionada a primeira Agent Skill formal do Hardening V2:

`skills/skill-supply-chain-auditor/SKILL.md`

Ela trata Skills como supply-chain não confiável até revisão de proveniência, licença, conteúdo, scripts, dependências, permissões, prompt injection e testes.

### Testes e benchmark

`tests/test_agent_hardening_v2.py` cobre:

- transport failure;
- timeout;
- cancel;
- resume;
- duplicate tool execution;
- idempotency;
- HITL execution integrity;
- parallel tool state;
- Skill atomic update;
- Skill integrity hash;
- hostile Skill text tratado como input em staging, sem claim de detector perfeito;
- untrusted MCP instruction;
- execution receipt.

`tests/test_skill_contract.py` valida o contrato mínimo das Skills.

`benchmarks/hardening_v2_smoke.py` produz métricas machine-readable de referência para VAR, RSR, DSER e CTVR sem usar LLM/provider/network e sem alegar comparação entre frameworks.

`tests/run_quality_gates.py` executa o reference runtime e benchmark smoke juntamente com os gates existentes.

## Evidência de CI

No SHA `92b3458ba13c98800a86106ed4b0a545b8124e63`, disparado pelo draft PR #53:

- `NEXUS Quality` — **success**;
- `Documentation quality` — **success**;
- `Security - Secret Scan` — **success**.

Dentro de `NEXUS Quality`:

- `Contracts and Python self-tests` — **success**;
- `TypeScript boundary contract` — **success**.

Isso comprova a suíte configurada nesse SHA. Commits posteriores de documentação/review ainda devem passar novamente no SHA final antes do merge.

## Auditoria independente

A revisão consolidada está em `docs/audits/INDEPENDENT_REVIEW_SCORECARD.md`.

Resultado atual:

- críticos: 0 identificados;
- altos: 0 identificados no escopo do reference layer;
- médios: identity binding real, durable receipts, atomicidade distribuída de Skills, MCP adversarial lab, provider-level prompt-injection evaluation e supply-chain automation mais completa.

Maturidade proposta: **L3 — Reproducible**, restrita ao escopo do laboratório/reference layer. `L4 — Secure-by-Design` ainda não é alegado.

## O que NÃO está sendo alegado

- Não se afirma que issues upstream do Codex ou Google ADK são vulnerabilidades do NEXUS.
- Não se afirma que o exemplo de ledger substitui banco transacional/distributed exactly-once.
- Não se afirma que SHA-256 resolve proveniência/autenticidade por si só.
- Não se afirma que o teste de conteúdo hostil detecta prompt injection; a arquitetura exige um gate de revisão separado.
- Não se afirma que o benchmark smoke compara frameworks/modelos.
- Não se afirma `production grade` sem adapters reais e controles distribuídos correspondentes.

## Riscos residuais

1. `ActionLedger` é in-memory e pedagógico; produção exige armazenamento durável/consistente.
2. `os.replace` é atômico sob condições do filesystem local; ambientes distribuídos precisam de contrato diferente.
3. Aprovação é modelada por identidade declarada, não por sistema real de autenticação/assinatura.
4. Não existe ainda adapter A2A/ADK reproduzindo os achados upstream.
5. Não existe registry de Skills completo nem scanner/SBOM/provenance automation dedicado.
6. Não existe ainda chaos runner integrado aos providers reais.

## Próximos gates

1. Confirmar CI verde no SHA final do PR.
2. Implementar adapters controlados para OpenAI Agents SDK, Google ADK e MCP.
3. Criar chaos/failure lab real.
4. Evoluir receipts para evidência externa/durável quando houver side effects reais.
5. Criar protocolo experimental antes de qualquer comparação pública entre frameworks.

## Status

**IMPLEMENTED:** sim, para os controles/documentação/reference runtime descritos.

**TESTED:** sim no SHA de evidência acima; exigir rerun verde no SHA final antes do merge.

**VERIFIED:** revisão independente simulada concluída, com limitações registradas; CI final ainda é gate de merge.

**PRODUCTION GRADE:** não alegado.