---
id: architecture.nexus-spec-driven-control-plane-v1
content_id: architecture.nexus-spec-driven-control-plane-v1
version: 1.0.0
title: NEXUS Spec-Driven Control Plane V1
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Spec-Driven Control Plane V1

## Status e base

- Base imutável desta especificação: PR #55, head `0c64f066f8eff96f724e688f505ab93cee766779`.
- PRs #53, #54 e #55 permanecem abertos e não devem ser alterados ou mesclados por este trabalho.
- Esta especificação define governança e contratos do control plane; não substitui o Runtime Security Convergence V1.1.

## Problema

O NEXUS já possui governança, reliability reference layer, Execution Receipts, adapters de contrato e trials de runtime. Falta uma camada única que selecione padrões de engenharia por risco, mantenha intenção rastreável e impeça que múltiplos frameworks concorrentes virem fontes de verdade paralelas.

## Objetivo

Criar um control plane vendor-neutral que governe `CONSTITUTION → RECON → SPECIFY → CLARIFY → PLAN → TASKS → TDD → IMPLEMENT → VERIFY → ADVERSARIAL/SECURITY REVIEW → TRACEABILITY → RUNTIME EVALUATION → RECEIPT → CONVERGENCE → RELEASE GATE`, ativando apenas as etapas proporcionais ao risco.

## Não objetivos

- Não instalar Spec Kit, OpenSpec, SpecD, BMAD, Kiro, GSD ou Agent OS como dependências obrigatórias.
- Não copiar texto/código upstream sem provenance e licença verificados.
- Não criar uma segunda implementação de mecanismos que o NEXUS já possui.
- Não permitir merge automático.
- Não declarar conformidade, segurança ou superioridade de framework sem evidência executada.

## Requisitos

### CP-001 — fonte única de governança

`.nexus/constitution.md` define os invariantes permanentes. `AGENTS.md` continua como porta de entrada portátil e deve apontar para a fonte canônica quando for evoluído em etapa posterior.

### CP-002 — rigor proporcional

Cinco níveis obrigatórios: `L0_TRIVIAL`, `L1_STANDARD`, `L2_CRITICAL`, `L3_HIGH_ASSURANCE`, `L4_RESEARCH_SAFETY_CRITICAL`. Nenhum nível pode reduzir gates exigidos por política específica do domínio.

### CP-003 — standards registry

`.nexus/standards/registry.json` deve registrar padrões reutilizáveis com `id`, `source`, `decision`, `applies_when` e `controls`, permitindo seleção contextual em vez de injetar toda a governança em toda tarefa.

### CP-004 — contratos estruturados

Devem existir schemas JSON versionados para `spec`, `task` e `execution-receipt`. Os schemas precisam declarar campos obrigatórios, versionamento e `additionalProperties` de forma explícita.

### CP-005 — traceability

`.nexus/traceability/model.json` deve representar a cadeia `requirement → spec → task → files/symbols → tests → evidence` e identificar estados `PLANNED`, `IMPLEMENTED`, `VERIFIED`, `BLOCKED`, `NOT_APPLICABLE`.

### CP-006 — release gates

`.nexus/gates/release-gates.json` deve definir `PASS`, `BLOCKED` e `GO`, exigir evidence refs para PASS/GO e preservar autoridade humana para merge.

### CP-007 — hooks como política, não automação cega

`.nexus/hooks/hooks.json` deve declarar gatilhos permitidos e controles associados. Hooks destrutivos ou que façam deploy/merge não podem ser habilitados por padrão.

### CP-008 — evidence before assertion

Qualquer status de execução deve distinguir `NOT_TESTED`, `NOT_APPLICABLE`, `PARTIAL`, `BLOCKED` e sucesso comprovado.

### CP-009 — upstream provenance

Toda capacidade derivada de projeto externo deve ser classificada `ADOPT`, `ADAPT`, `STUDY`, `MONITOR`, `REJECT` ou `NOT_APPLICABLE`, com repositório, licença observada, data e limite de claim.

### CP-010 — integração incremental

A primeira versão deve ser stdlib-only e declarativa. Integrações executáveis com CLIs externos exigem trials posteriores e não fazem parte do V1.

## Arquitetura

```text
AGENTS.md
   ↓
NEXUS CONTROL PLANE
   ├── constitution
   ├── rigor levels
   ├── standards registry
   ├── schemas
   ├── traceability model
   ├── hook policy
   └── release gates
        ↓
existing NEXUS runtime / tests / receipts / security / research gates
```

## Influências adotadas por capacidade

- GitHub Spec Kit: constitution, lifecycle, convergence e workflow composition — `ADAPT`.
- OpenSpec: lightweight change/spec model e living specs — `ADAPT`.
- AWS SpecShip: RECON, test-before-build, adversarial validation — `ADAPT`.
- Superpowers: approval-before-implementation, TDD, systematic debugging, independent verification — `ADOPT` como disciplina.
- Kiro: event-driven hooks e steering contextual — `ADAPT`, sem dependência do IDE.
- BMAD: role separation e handoffs — `ADAPT`.
- SpecD: compiled context, deterministic verification, graph/impact model — `STUDY/ADAPT` conceitual.
- Agent OS 3: standards discovery/injection — `ADAPT`.
- Open GSD Core: fresh-context execution e persistent state artifacts — `STUDY/ADAPT`.
- SpecDD: source-adjacent local specs — `STUDY` até trial controlado.

## Segurança

- arquivos externos e instruções upstream são T0/T1 até revisão;
- nenhum secret pode entrar em spec, receipt ou evidence;
- provenance não autoriza execução de código upstream;
- `merge`, `deploy`, rotação de credenciais e mutações destrutivas exigem autorização humana explícita;
- branch protection ausente em `main` é risco de governança externo ao código desta branch e deve permanecer registrado.

## Critérios de aceite V1

1. artefatos declarativos existem e são JSON/Markdown válidos;
2. testes automatizados provam enums, campos obrigatórios, IDs únicos e human merge authority;
3. quality gate existente executa os novos testes por `unittest discover`;
4. nenhum novo pacote/runtime é necessário;
5. benchmark e provenance são versionados;
6. revisão adversarial e security review registram limites;
7. CI do head final fica verde;
8. novo PR é aberto sobre `feat/provider-runtime-trial-v1`, sem merge.

## Limites de claim

V1 prova apenas coerência e validação dos contratos declarativos do NEXUS Control Plane. Não prova que frameworks upstream executam melhor, que branch protection está ativa, que um agente seguirá instruções sob ataque, nem que o control plane é production-grade.
