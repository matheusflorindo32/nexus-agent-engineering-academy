---
id: audit.current-state-v2
title: Auditoria do estado atual — Hardening V2
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Auditoria do estado atual — Hardening V2

## Escopo

Esta auditoria registra o estado observado do repositório antes das mudanças de hardening. A regra é separar documentação aspiracional de implementação comprovada.

## Baseline observado

- Branch base: `main` no commit `48b4040c06693abd3e06cb02cfdb4b507f6f13e9`.
- Branch de trabalho criada: `feat/agent-hardening-v2`.
- O repositório se declara em fase `foundation` e adota Apache-2.0.
- O README posiciona o NEXUS como curso, laboratório, documentação, framework e portfólio para Agent Engineering.
- O contrato de agentes já exige fontes primárias, branch própria, PR, segurança, reversibilidade e critérios de parada.
- A política de segurança já cobre least privilege, MCP, aprovação humana, circuit breaker, rollback e segredos.
- A arquitetura já modela estados `Receive → Plan → Act → Observe`, com `AwaitApproval`, `Recover`, `Stopped`, `Cancelled` e `Complete`.
- Há CI em `.github/workflows/`, Dependabot, CODEOWNERS e pre-commit.
- Há validação estrutural própria em `tests/validate_repository.py` e testes adicionais em `tests/`.
- Há pelo menos um agent spec em `agents/specs/minimal-readonly-agent.yaml`.

## Evidência de CI

O último workflow de documentação observado em `main`, associado ao commit `security: add pre-commit secret scanning`, terminou com `conclusion=success` em 2026-08-25. Isso comprova apenas aquele workflow, não toda a suíte.

## Limitação de execução local desta auditoria

A tentativa de clonar o repositório no ambiente local de auditoria falhou por indisponibilidade de resolução de rede para `github.com`. Portanto, nesta etapa não se afirma que `python tests/validate_repository.py` ou `python tests/run_quality_gates.py` tenham sido executados localmente. A execução deverá ser comprovada pelo CI da branch ou por ambiente com checkout disponível.

## Matriz de maturidade observada

| Componente | Estado | Evidência / observação |
|---|---|---|
| Governança do agente | IMPLEMENTED + DOCUMENTED | `AGENTS.md` define papéis, loop, stop conditions e DoD. |
| Segurança base | IMPLEMENTED + DOCUMENTED | `SECURITY.md` e `docs/security/index.md`. |
| Threat model | IMPLEMENTED, requer V2 | Existe modelo inicial, ainda sem taxonomia T0–T7 e sem matriz completa de ativos/atores. |
| CI | IMPLEMENTED | Workflows presentes; um workflow recente observado como bem-sucedido. |
| Secret scanning local | IMPLEMENTED | `.pre-commit-config.yaml` existe e commit recente registra inclusão. |
| Testes estruturais | IMPLEMENTED | `tests/validate_repository.py` valida estrutura, frontmatter, links, agent specs, executáveis e padrões básicos de secrets. |
| Observabilidade | IMPLEMENTED/EXPERIMENTAL | Existem exemplo e testes específicos; precisa ser reavaliada contra modelo de eventos V2. |
| Skills formais (`SKILL.md`) | NOT_IMPLEMENTED/NOT_OBSERVED | A busca pública do repositório não retornou `SKILL.md`; a árvore atual não expõe diretório `skills/` na raiz. |
| Skill registry | NOT_IMPLEMENTED | Não observado. |
| Atomic Skill Updates | NOT_IMPLEMENTED | Não observado. |
| Skill supply-chain auditor | NOT_IMPLEMENTED | Não observado. |
| MCP security lab dedicado | PLANNED/PARTIAL | Segurança MCP está documentada, mas não foi comprovada uma suíte dedicada de regressão nesta auditoria. |
| Execution Receipts | NOT_IMPLEMENTED/NOT_OBSERVED | Conceito não comprovado no código atual. |
| Side-effect idempotency framework | PARTIAL/DOCUMENTED | Idempotência aparece como princípio de segurança; mecanismo formal não comprovado. |
| HITL/A2A integrity lab | NOT_IMPLEMENTED | Não observado. |
| Chaos/failure testing | PLANNED | Roadmap prevê produção/reliability; suíte dedicada não observada. |
| Framework upgrade gate | NOT_IMPLEMENTED | Não observado. |
| Technology radar | NOT_IMPLEMENTED | Não observado. |

## Pontos fortes

1. A fundação conceitual é significativamente melhor que um repositório típico de exemplos de agentes: contratos, segurança, stop conditions, observabilidade e evidência já aparecem como invariantes.
2. A arquitetura separa Knowledge Core, Platform Adapters, Practice e Governance, reduzindo lock-in de fornecedor.
3. O validador estrutural próprio reduz regressões editoriais e de organização.
4. O projeto já diferencia conteúdo externo de instrução confiável no guia de segurança.

## Lacunas prioritárias

### P0 — integridade de ação e confiança

- Falta um modelo formal `REQUESTED → APPROVED → EXECUTED → VERIFIED`.
- Falta `Execution Receipt` independente da narrativa do LLM.
- Falta idempotência verificável para side effects.
- Falta taxonomia formal de confiança de contexto T0–T7.

### P0 — supply chain de Skills

- O NEXUS ainda não possui uma camada formal de Agent Skills observada nesta auditoria.
- Antes de adotar Skills externas, deve existir staging, validação, proveniência, licença, hashes, promoção atômica e rollback.

### P1 — reliability

- Timeout, cancelamento, retry, backoff, circuit breaker e recovery existem como princípios, mas precisam de contratos executáveis e testes de falha.
- A suíte deve distinguir falha de modelo, transporte, ferramenta, MCP, armazenamento e estado.

### P1 — upgrade safety

- Frameworks agentic não devem ser atualizados apenas por release cadence. É necessário um gate com release review, sandbox, regressão, benchmark e aprovação.

## Maturity level provisório

**L2 — Tested (provisório, com evidência parcial).**

Justificativa: há testes, CI, contratos e documentação substantiva. Ainda não há evidência suficiente para L3/L4 porque faltam mecanismos formais de reproducibilidade/upgrade gate, supply-chain de Skills, receipts de execução, trust model completo e suíte de reliability/chaos exigida pelo Hardening V2.

A classificação deverá ser recalculada após CI da branch e auditoria independente.