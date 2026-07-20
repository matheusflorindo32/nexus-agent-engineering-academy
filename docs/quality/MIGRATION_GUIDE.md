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

| Origem histórica | Destino canônico | Ação |
|---|---|---|
| conteúdos conflitantes de MCP e Skills | especializações e módulos relacionados | preservar no histórico Git e referenciar no índice de especializações |
| módulos legados 05–09 com prefixos concorrentes | Modules 05–09 Premium Elite | consolidar editorialmente e remover colisão ativa |
| `10-automation` | `11-automation` | renumerar e atualizar pré-requisitos e links |
| `11-capstone` | `12-capstone` | renumerar e atualizar pré-requisitos e links |
| reserva histórica `LAB-1001` de idempotência | `LAB-1101` | mover a finalidade para o módulo 11 |
| `LAB-1001-agent-observability` | permanece LAB-1001 | manter como laboratório oficial de observabilidade |

## Compatibilidade

- caminhos antigos não são considerados API estável;
- materiais externos que apontem para caminhos antigos devem ser atualizados manualmente;
- o histórico Git permanece como fonte de recuperação;
- futuras renumerações exigem novo ADR e atualização deste guia.

## Procedimento de migração local

```bash
git fetch origin
git checkout audit/premium-elite-readiness-docs
python tests/validate_repository.py
python -m compileall -q examples tests
python examples/observability_pipeline.py --self-test
```

## Rollback

Antes do merge, o rollback consiste em fechar o PR e remover a branch. Após eventual merge, o rollback deve usar `git revert` do merge commit, preservando histórico e evidência. Não usar force-push na `main`.

## Critérios de aceite

- nenhum prefixo duplicado;
- nenhum laboratório duplicado;
- nenhum link interno quebrado;
- conteúdo legado rastreável pelo histórico;
- documentação de especializações acessível;
- CI verde no SHA auditado.
