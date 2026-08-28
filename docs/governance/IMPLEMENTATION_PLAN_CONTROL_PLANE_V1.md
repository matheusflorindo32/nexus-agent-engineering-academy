---
id: governance.implementation-plan-control-plane-v1
content_id: governance.implementation-plan-control-plane-v1
version: 1.0.0
title: Plano de implementação — NEXUS Control Plane V1
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Spec-Driven Control Plane V1 Implementation Plan

> **For agentic workers:** executar tarefa por tarefa com TDD, revisão separada e evidence before assertion.

**Goal:** adicionar uma camada declarativa, stdlib-only e vendor-neutral para governar rigor, standards, schemas, traceability, hooks e release gates sem substituir os mecanismos runtime existentes.

**Architecture:** `.nexus/` é a fonte canônica de control-plane contracts; `AGENTS.md` continua porta de entrada portátil. Os contratos são JSON/Markdown estáticos validados por `unittest`, e o quality gate existente os executa automaticamente por discovery.

**Tech Stack:** Markdown, JSON, Python stdlib `unittest`/`json`/`pathlib`.

**Spec:** `docs/architecture/NEXUS_SPEC_DRIVEN_CONTROL_PLANE_V1.md`

## Global Constraints

- Base SHA: `0c64f066f8eff96f724e688f505ab93cee766779`.
- Não alterar nem mesclar PRs #53, #54 ou #55.
- Nenhuma dependência externa nova no V1.
- Nenhum auto-merge/deploy.
- Nenhum resultado alegado sem CI/evidência.
- Nenhum código upstream copiado no V1.

---

### Task 1: RED — contrato mínimo do control plane

- [x] Escrever `tests/test_nexus_control_plane_contracts.py` antes dos artefatos `.nexus`.
- [x] Confirmar CI RED por arquivos ausentes, não por erro sintático.
- [x] Registrar run `33192038733` e artifact `9694146965` como evidência RED.

### Task 2: GREEN — constitution e rigor levels

- [x] Criar `.nexus/constitution.md`.
- [x] Criar `.nexus/rigor-levels.json` com L0–L4.
- [x] Confirmar contratos em CI GREEN.

### Task 3: GREEN — standards registry e traceability

- [x] Criar `.nexus/standards/registry.json` com IDs únicos e decisões válidas.
- [x] Criar `.nexus/traceability/model.json` com requirement→evidence e estados fechados.

### Task 4: GREEN — schemas versionados

- [x] Criar schemas de spec, task e execution receipt.
- [x] Exigir campos centrais, `$id`, versionamento e `additionalProperties=false`.

### Task 5: GREEN — hooks, gates e entrypoint

- [x] Criar hook policy sem ações destrutivas default.
- [x] Criar release gates PASS/BLOCKED/GO com human merge authority.
- [x] Executar segundo ciclo RED para exigir roteamento em `AGENTS.md`: run `33192394335`, 63 testes e exatamente 1 failure.
- [x] Atualizar `AGENTS.md` como entrypoint portátil para `.nexus`.

### Task 6: Verify / adversarial review

- [x] Registrar `docs/audits/NEXUS_CONTROL_PLANE_V1_REVIEW_SCORECARD.md`.
- [x] Tentar quebrar enums, IDs, `additionalProperties`, human authority e forbidden hooks por contratos automatizados.
- [x] Registrar riscos residuais e limites de claim.
- [ ] Confirmar todos os workflows obrigatórios verdes no **head final**.

### Task 7: PR gate

- [x] Branch isolada criada sobre o SHA exato do PR #55.
- [x] PR #56 aberto com base `feat/provider-runtime-trial-v1`.
- [x] Nenhum merge executado.
- [ ] Após CI final verde, promover o draft apenas para revisão humana.
