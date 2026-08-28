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

> **For agentic workers:** executar tarefa por tarefa com TDD, revisão independente e evidence before assertion.

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

**Files:**
- Create: `tests/test_nexus_control_plane_contracts.py`

**Produces:** testes que exigem constitution, rigor levels, standards registry, schemas, traceability, hooks e release gates.

- [x] Escrever teste antes dos artefatos `.nexus`.
- [ ] Executar CI e confirmar falha por arquivos ausentes, não por erro sintático.
- [ ] Registrar o run como evidência RED.

### Task 2: GREEN — constitution e rigor levels

**Files:**
- Create: `.nexus/constitution.md`
- Create: `.nexus/rigor-levels.json`

**Produces:** invariantes permanentes e cinco níveis de rigor.

- [ ] Criar conteúdo mínimo que satisfaça os testes.
- [ ] Reexecutar testes focados e confirmar progresso.

### Task 3: GREEN — standards registry e traceability

**Files:**
- Create: `.nexus/standards/registry.json`
- Create: `.nexus/traceability/model.json`

**Produces:** seleção contextual de padrões e cadeia requirement→evidence.

- [ ] Criar registros com IDs únicos e decisões válidas.
- [ ] Validar estados e referências estruturais.

### Task 4: GREEN — schemas versionados

**Files:**
- Create: `.nexus/schemas/spec.schema.json`
- Create: `.nexus/schemas/task.schema.json`
- Create: `.nexus/schemas/execution-receipt.schema.json`

**Produces:** contratos estruturados com campos obrigatórios e `additionalProperties` explícito.

- [ ] Criar schemas JSON válidos.
- [ ] Confirmar required fields e version identifiers pelos testes.

### Task 5: GREEN — hooks e release gates

**Files:**
- Create: `.nexus/hooks/hooks.json`
- Create: `.nexus/gates/release-gates.json`

**Produces:** hooks permitidos sem ações destrutivas default e gates PASS/BLOCKED/GO com human merge authority.

- [ ] Implementar policy declarativa.
- [ ] Confirmar que nenhum hook padrão contém merge/deploy/delete/credential rotation.

### Task 6: Verify / adversarial review

**Files:**
- Create: `docs/audits/NEXUS_CONTROL_PLANE_V1_REVIEW_SCORECARD.md`

- [ ] Executar `NEXUS Quality`, docs quality e secret scan no head final.
- [ ] Tentar quebrar enums, IDs, additionalProperties, human authority e forbidden hooks.
- [ ] Registrar riscos residuais e limites de claim.

### Task 7: PR gate

- [ ] Confirmar diff somente na nova branch.
- [ ] Abrir PR com base `feat/provider-runtime-trial-v1`.
- [ ] Não fazer merge.
