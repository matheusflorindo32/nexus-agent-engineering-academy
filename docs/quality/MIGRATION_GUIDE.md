---
id: docs.quality.migration-guide
title: Guia de migração da taxonomia curricular
lang: pt-BR
status: review
---

# Guia de migração da taxonomia curricular

## Objetivo

Orientar a transição da árvore curricular histórica para a trilha canônica 00–12 sem perder rastreabilidade.

## Mapeamento

O mapeamento abaixo foi derivado do diff entre `main` e a head inicial do PR #6 (`2100dc77b836c9d08baf539c3c853417d912e6c7`). “Histórico Git” significa recuperável por commit; não significa conteúdo publicado na árvore atual.

| Caminho e ID históricos | Destino canônico | Estado e ação de migração |
|---|---|---|
| `course/modules/05-mcp-skills/README.md` — `course.module.05-mcp-skills` | conceitos de ferramentas em `course/modules/03-tool-engineering/`; segurança MCP em `docs/security/index.md` | conteúdo reduzido, sem equivalência integral na árvore atual; preservar no histórico e decidir em revisão humana se deve voltar como especialização sem número curricular |
| `course/modules/06-evaluation/README.md` — `course.module.06-evaluation` | `course/modules/07-evaluation-engineering/README.md` — `course.module.07-evaluation-engineering` | consolidado no módulo canônico de avaliação |
| `course/modules/07-observability-sre/README.md` — `course.module.07-observability-sre` | `course/modules/09-production-architecture/README.md` e `course/modules/10-observability-engineering/README.md` | responsabilidades de SRE e observabilidade separadas entre produção e telemetria |
| `course/modules/08-security/README.md` — `course.module.08-security` | `course/modules/08-guardrails-security-engineering/README.md` — `course.module.08-guardrails-security-engineering` | consolidado no módulo canônico de segurança |
| `course/modules/09-multi-agent-systems/README.md` — `course.module.09-multi-agent-systems` | `course/modules/06-multi-agent-systems/README.md` — `course.module.06-multi-agent-systems` | consolidado e renumerado para preservar a progressão |
| `course/modules/10-automation/README.md` — `course.module.10-automation` | `course/modules/11-automation/README.md` — `course.module.11-automation` | renumerado; pré-requisito, links e LAB atualizados |
| `course/modules/11-capstone/README.md` — `course.module.11-capstone` | `course/modules/12-capstone/README.md` — `course.module.12-capstone` | renumerado; pré-requisito e links atualizados |
| `labs/LAB-801-prompt-injection.md` — `lab.801.prompt-injection` | `labs/LAB-801-agent-security-red-team.md` — `lab.801.agent-security-red-team` | cenário de prompt injection incorporado a um red team mais amplo; caminho antigo deixa de existir |
| reserva histórica do `LAB-1001` para idempotência | `labs/LAB-1101-idempotent-automation.md` | finalidade transferida ao módulo 11; não havia segundo arquivo canônico a preservar |
| `labs/LAB-1001-agent-observability.md` | mesmo caminho e ID | permanece laboratório oficial de observabilidade |

## Compatibilidade

- caminhos antigos não são considerados API estável;
- materiais externos que apontem para caminhos antigos devem ser atualizados manualmente;
- o histórico Git permanece como fonte de recuperação;
- não há redirects ou aliases para os caminhos removidos;
- MCP e Skills permanecem como risco curricular documentado porque a consolidação não preservou equivalência integral;
- futuras renumerações exigem novo ADR e atualização deste guia.

## Procedimento de migração local

```bash
git fetch origin
git checkout fix/final-security-readiness
python tests/validate_repository.py
python -m compileall -q examples tests
python examples/observability_pipeline.py --self-test
```

## Ordem de integração da pilha

1. revisar o PR final, cuja base deve ser `audit/premium-elite-readiness-docs`;
2. integrar o PR final na branch do PR #7;
3. confirmar a CI do PR #7 no novo SHA;
4. integrar o PR #7 na branch do PR #6, `fix/curriculum-observability-contracts`;
5. confirmar a CI do PR #6 no novo SHA;
6. somente então avaliar o merge do PR #6 na `main`;
7. confirmar a CI pós-merge na `main`;
8. criar tag ou release apenas após a validação da `main`.

Nenhuma dessas integrações é automática. PRs devem permanecer Draft até decisão humana explícita.

## Rollback por estágio

- **Antes de qualquer merge:** interromper a integração e manter PR e branch para preservar discussão e evidência; não é necessário remover a branch.
- **PR final já integrado no PR #7:** reverter na branch do PR #7 o commit ou merge commit correspondente e executar novamente sua CI.
- **PR #7 já integrado no PR #6:** reverter primeiro a integração do PR #7 na branch do PR #6; depois validar o estado do PR #6.
- **PR #6 já integrado na `main`:** identificar a estratégia usada. Para merge commit, usar `git revert -m 1 <merge-sha>`; para squash/rebase, reverter os commits efetivamente introduzidos em ordem inversa. Abrir PR de rollback e exigir CI antes de integrá-lo.
- **Após release:** reverter o código antes de mover tags ou publicar uma correção; nunca reescrever tag pública silenciosamente.

Não usar force-push na `main`, não apagar histórico e não executar comandos de rollback sem confirmar os SHAs e o impacto sobre commits posteriores.

## Critérios de aceite

- nenhum prefixo duplicado;
- nenhum laboratório duplicado;
- nenhum link interno quebrado;
- conteúdo legado rastreável pelo histórico;
- documentação de especializações acessível;
- redução de MCP/Skills explicitamente aceita ou corrigida por revisão humana;
- ordem de integração e rollback da stack revisados;
- CI verde no SHA auditado.
