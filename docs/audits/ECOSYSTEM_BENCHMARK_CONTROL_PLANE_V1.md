---
id: audit.ecosystem-benchmark-control-plane-v1
content_id: audit.ecosystem-benchmark-control-plane-v1
version: 1.0.0
title: Benchmark do ecossistema — NEXUS Control Plane V1
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Benchmark do ecossistema — NEXUS Control Plane V1

## Método

Benchmark documental e arquitetural executado em 2026-08-28 com fontes oficiais/primárias disponíveis. Não é benchmark de runtime. Nota total (0–100): Engenharia 15, Maturidade 15, Segurança 15, Agentic Engineering 15, Specification 15, Qualidade/Verification 10, Integração/Portabilidade 10, Governança/Licença 5. Ausência de evidência recebe nota menor; popularidade não é critério direto.

## Resultado global

| Projeto | Eng | Mat | Seg | Agentic | Spec | QA | Int | Gov | Total | Decisão NEXUS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| GitHub Spec Kit | 14 | 15 | 13 | 13 | 15 | 8 | 10 | 5 | **93** | ADAPT |
| Superpowers | 13 | 14 | 10 | 14 | 11 | 10 | 9 | 5 | **86** | ADOPT/ADAPT |
| OpenSpec | 13 | 14 | 12 | 11 | 14 | 8 | 9 | 5 | **86** | ADAPT |
| Agent OS 3 | 12 | 12 | 9 | 11 | 10 | 7 | 9 | 5 | **75** | ADAPT |
| Open GSD Core | 12 | 11 | 10 | 14 | 11 | 8 | 8 | 5 | **79** | STUDY/ADAPT |
| AWS SpecShip | 11 | 5 | 10 | 12 | 12 | 10 | 7 | 5 | **72** | ADAPT concepts |
| Kiro | 13 | 13 | 13 | 14 | 13 | 8 | 7 | 2 | **83** | ADAPT concepts |
| BMAD-METHOD | 12 | 14 | 9 | 15 | 12 | 8 | 9 | 4 | **83** | ADAPT roles |
| SpecD | 14 | 5 | 11 | 13 | 15 | 9 | 9 | 5 | **81** | STUDY/ADAPT |
| SpecDD | 11 | 4 | 9 | 9 | 14 | 7 | 7 | 5 | **66** | STUDY |

## Observações que afetam a nota

- Spec Kit lançou 1.0.0 em 2026-08-21 e consolidou integrations, extensions, presets, workflows e workflow steps; MIT.
- OpenSpec é MIT, possui fluxo leve de specs e política de segurança publicada; sua versão de package observada durante a auditoria foi 1.6.0.
- SpecShip declara explicitamente ser experimental/unofficial, sem revisão externa de segurança, apesar de ter RECON/TDD/validação adversarial muito úteis; o repositório observado tinha histórico público mínimo.
- Superpowers possui disciplina forte de TDD, debugging, planning, work isolation e independent verification; MIT.
- Agent OS 3 deliberadamente reduziu escopo para standards establishment/injection, evitando reinventar planning moderno; MIT.
- O repositório antigo `gsd-build/get-shit-done` está arquivado; o upstream ativo considerado é `open-gsd/gsd-core`, MIT.
- SpecD possui arquitetura tecnicamente forte (compiled context, deterministic verification, code graph, hooks, approvals), mas comunidade/maturidade pública ainda pequena; MIT.
- SpecDD usa specs locais source-adjacent e Apache-2.0; ainda é novo e não deve ser dependência obrigatória.
- Kiro oferece Specs/Hooks/Steering/MCP/Powers e política de segurança, mas o benchmark não confirmou licença open-source equivalente para reutilização ampla do código do produto; portanto apenas padrões conceituais entram automaticamente.

## Vencedor por capacidade

| Capacidade | Vencedor | Uso no NEXUS |
|---|---|---|
| Framework-base de SDD | GitHub Spec Kit | modelo de lifecycle/composição, não instalação obrigatória |
| Specs incrementais | OpenSpec | change model leve |
| Constitution/governança | Spec Kit + NEXUS existente | constitution canônica |
| Brownfield RECON | SpecShip | fase RECON adaptada |
| TDD | Superpowers | disciplina obrigatória quando aplicável |
| Debugging sistemático | Superpowers | ADOPT |
| Context isolation | Open GSD Core | fresh-context como padrão para trabalhos longos |
| Standards injection | Agent OS 3 | registry + seleção contextual |
| Multi-agent role separation | BMAD | papéis/handoffs, sem framework lock-in |
| Hooks | Kiro / SpecD | policy declarativa + gates |
| Traceability/impact | SpecD | modelo conceitual e futuro trial técnico |
| Local source-adjacent specs | SpecDD | STUDY |
| Adversarial validation | SpecShip + NEXUS | ADAPT |
| Verification-before-completion | Superpowers + SpecD | ADOPT/ADAPT |

## Matriz feature-level (0–5)

| Capacidade | Spec Kit | OpenSpec | SpecShip | BMAD | Kiro | SpecD | Superpowers | GSD Core | Agent OS | SpecDD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Requirements/spec | 5 | 5 | 4 | 4 | 5 | 5 | 3 | 4 | 3 | 5 |
| Brownfield recon | 3 | 4 | 5 | 3 | 4 | 4 | 3 | 4 | 4 | 4 |
| TDD | 3 | 3 | 5 | 4 | 3 | 4 | 5 | 4 | 2 | 3 |
| Planning | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 2 | 3 |
| Hooks | 4 | 3 | 4 | 3 | 5 | 5 | 3 | 4 | 3 | 2 |
| Traceability/drift | 4 | 4 | 3 | 3 | 3 | 5 | 3 | 4 | 3 | 4 |
| Multi-agent | 4 | 3 | 5 | 5 | 4 | 4 | 5 | 5 | 3 | 2 |
| Debugging | 4 | 3 | 4 | 3 | 3 | 4 | 5 | 4 | 2 | 2 |
| Verification | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 5 | 3 | 4 |
| Security governance | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 4 | 3 | 3 |

## Decisão

Nenhum projeto vence todas as categorias. O NEXUS deve permanecer control plane próprio. Instalação simultânea dos frameworks é `REJECT`; incorporação seletiva de padrões é `ADOPT/ADAPT` conforme a matriz de provenance.

## Limites

As notas representam adequação ao objetivo específico NEXUS e evidência pública observada em 2026-08-28. Não equivalem a qualidade absoluta, certificação de segurança, benchmark de performance ou avaliação de modelos.
