---
id: governance.control-register
title: Registro de controle operacional
lang: pt-BR
status: review
version: 0.2.0
updated_at: 2026-07-19
---

# Registro de controle operacional

## Finalidade

Manter a evolução da NEXUS dentro de limites explícitos, auditáveis e reversíveis. Este arquivo registra os bloqueios da branch `fix/final-security-readiness`, baseada na head `a48fa0d1952c147d232424ea4323ec91407a4b83` do PR #7.

## Regras invariantes

1. A PR permanece em rascunho até todos os portões obrigatórios estarem comprovados.
2. Nenhum merge, auto-merge, release ou promoção para revisão ocorre automaticamente.
3. Nenhuma credencial, dado real ou acesso privilegiado entra em exemplos, datasets ou logs.
4. A branch não é sincronizada com `main` sem inventário dos commits exclusivos e avaliação de conflitos.
5. Uma ausência de status de CI é tratada como bloqueio, nunca como aprovação.
6. Documentação, código, testes e métricas precisam declarar o mesmo escopo.
7. Toda mudança deve ser reversível por commit e possuir mensagem descritiva.

## Registro de riscos

| ID | Risco | Severidade | Estado | Evidência atual | Ação obrigatória |
|---|---|---:|---|---|---|
| CTRL-001 | CI final ainda não executada no SHA definitivo | crítica | aberto | PR final ainda não criado | criar PR Draft contra a branch do PR #7 e obter todos os workflows verdes no mesmo SHA |
| CTRL-002 | integração fora de ordem da pilha | alta | controlado | PR #7 depende do PR #6; branch final depende do PR #7 | seguir a ordem e os gates do guia de migração; não apontar o PR final para `main` |
| CTRL-003 | dependência TypeScript obtida pela rede no CI | média | aberto | `npx` com versão fixada, sem lockfile | criar lockfile ou runner hermético antes de release |
| CTRL-004 | ações GitHub referenciadas por tag | média | aberto | `actions/*@vN` | avaliar pin por SHA após verificação oficial |
| CTRL-005 | LAB-401 prometia oito cenários e testava sete | alta | mitigado | autoteste atualizado para oito cenários | confirmar em CI visível |
| CTRL-006 | revisão externa ainda ausente | média | aberto | nenhum relatório externo | executar ao menos um laboratório com terceiro |
| CTRL-007 | capacidades de plataformas podem ficar obsoletas | média | controlado | matriz usa `U` e datas de verificação | preencher somente com fonte e teste reproduzível |
| CTRL-008 | imagens sem derivados responsivos | baixa | aberto | PNG canônico publicado | gerar WebP e versão mobile após auditoria tipográfica |
| CTRL-009 | conteúdo MCP/Skills reduzido na consolidação | média | aberto | objetivos históricos não possuem equivalência integral na árvore atual | revisão humana decide restauração como especialização ou aceita formalmente a redução |
| CTRL-010 | LAB-1201 ainda não implementado | baixa | controlado | módulo 12 o marca como planejado | não contar como evidência ou requisito disponível |

## Portões de liberação

| Portão | Critério | Estado |
|---|---|---|
| G1 — CI | execução visível e verde no SHA final | bloqueado até criação do PR final |
| G2 — Integridade | validador, links, IDs, slugs, pré-requisitos e secret scan aprovados | aguardando CI final |
| G3 — Testes | todos os autotestes Python, testes do validador e TypeScript aprovados | aguardando CI final |
| G4 — Integração | base/head e ordem da pilha preservadas | controlado; execução depende de revisão humana |
| G5 — Evidência | fontes e capacidades atuais verificadas | parcial |
| G6 — Revisão externa | pelo menos um laboratório executado por terceiro | bloqueado |
| G7 — Revisão humana | conteúdo, design e escopo aprovados | bloqueado |

## Protocolo de mudança

Antes de qualquer alteração estrutural:

1. identificar o risco reduzido ou a capacidade adicionada;
2. limitar o menor conjunto de arquivos possível;
3. registrar teste ou critério de aceitação;
4. manter a PR em draft;
5. verificar se o novo código amplia permissões, rede, shell ou acesso a dados;
6. atualizar este registro quando o estado de um risco mudar.

## Ações proibidas sem autorização explícita

- merge, squash ou rebase destrutivo;
- force push;
- exclusão de histórico;
- alteração da branch padrão;
- publicação de pacote ou release;
- conexão com sistemas reais;
- inclusão de tokens, chaves, cookies ou credenciais;
- habilitação de auto-merge;
- declaração de CI aprovado sem execução verificável.

## Definition of Controlled

Uma entrega está **sob controle** quando:

- possui escopo e limites explícitos;
- tem teste e evidência rastreáveis;
- não amplia autoridade silenciosamente;
- pode ser revertida por commit;
- mantém documentação e implementação alinhadas;
- não ultrapassa nenhum portão bloqueado.
