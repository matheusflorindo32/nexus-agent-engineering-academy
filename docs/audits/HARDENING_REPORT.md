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
- `docs/security/THREAT_MODEL_V2.md`
- `docs/security/SKILL_SUPPLY_CHAIN_SECURITY.md`
- `docs/reliability/AGENT_RELIABILITY_MODEL.md`
- `docs/radar/AGENT_TECH_RADAR.md`
- `docs/governance/FRAMEWORK_UPGRADE_POLICY.md`

### Código de referência

`examples/agent_reliability_runtime.py` adiciona, sem rede e sem side effects reais:

- canal com espera limitada;
- persistência de falha terminal para leitores futuros;
- cancelamento explícito;
- `ActionLedger` com `operation_id`;
- approval scoped por principal/operação;
- `ExecutionReceipt`;
- execução idempotente de referência;
- verificação distinta de execução;
- Skill staging + SHA-256 + promoção por rename atômico;
- modelo T0–T7 para não escalada de confiança.

### Testes

`tests/test_agent_hardening_v2.py` cobre os nomes mínimos definidos para a rodada:

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

`tests/run_quality_gates.py` passou a incluir o self-test `agent-hardening-v2`.

## O que NÃO está sendo alegado

- Não se afirma que issues upstream do Codex ou Google ADK são vulnerabilidades do NEXUS.
- Não se afirma que o exemplo de ledger substitui banco transacional/distributed exactly-once.
- Não se afirma que SHA-256 resolve proveniência/autenticidade por si só.
- Não se afirma que o teste de conteúdo hostil detecta prompt injection; a arquitetura exige um gate de revisão separado.
- Não se afirma produção-ready enquanto CI, adapters reais e auditoria independente não forem concluídos.

## Riscos residuais

1. `ActionLedger` é in-memory e pedagógico; produção exige armazenamento durável/consistente.
2. `os.replace` é atômico sob condições do filesystem local; ambientes distribuídos precisam de contrato diferente.
3. Aprovação é modelada por identidade declarada, não por sistema real de autenticação/assinatura.
4. Não existe ainda adapter A2A/ADK reproduzindo os bugs upstream.
5. Não existe registry de Skills completo nem scanner de dependência dedicado.
6. Não existe ainda chaos runner integrado aos providers reais.

## Próximos gates

1. CI da branch deve executar validator, unittest, compileall e self-tests.
2. Corrigir qualquer regressão antes de adicionar adapters reais.
3. Adicionar ADRs de trust model, receipts e Skill updates.
4. Criar benchmark machine-readable para VAR/RSR/DSER/CTVR.
5. Somente depois implementar adapters experimentais para OpenAI/ADK/MCP.

## Status

**IMPLEMENTED:** documentação e runtime/testes de referência descritos acima.

**TESTED:** pendente de evidência de CI da branch no momento da criação deste relatório.

**VERIFIED:** pendente de auditoria independente e execução de CI.

**PRODUCTION GRADE:** não alegado.