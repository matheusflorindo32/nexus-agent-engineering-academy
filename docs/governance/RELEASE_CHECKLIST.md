---
id: governance.release-checklist
title: Checklist de release NEXUS
lang: pt-BR
status: review
version: 0.1.0
---

# Checklist de release NEXUS

## Regra de decisão

Uma release só pode ser proposta quando o escopo, o SHA, as evidências e os riscos residuais estiverem explícitos. CI verde não cria autorização automática para merge, tag, publicação ou promoção de conteúdo para `stable`.

Decisão permitida:

- `no-go` — existe bloqueador ou evidência insuficiente;
- `go-with-constraints` — piloto ou publicação limitada com restrições documentadas;
- `go` — somente para o escopo exato validado.

## 1. Escopo e identidade

- [ ] Release ID e versão foram definidos.
- [ ] SHA exato, branch e base integrada foram registrados.
- [ ] Mudanças incluídas e excluídas estão listadas.
- [ ] Dependências, PRs e migrações estão identificados.
- [ ] A versão não promete estabilidade, certificação ou eficácia além da evidência.

## 2. Integração

- [ ] PRs empilhados foram integrados na ordem correta.
- [ ] Cada retarget/rebase foi revalidado.
- [ ] Não há PR crítico ainda baseado em SHA obsoleto.
- [ ] Aprovações humanas correspondem ao SHA final.
- [ ] Nenhum merge automático foi usado para contornar revisão.

## 3. Qualidade técnica

- [ ] `python tests/validate_repository.py` passa no SHA final.
- [ ] Workflows obrigatórios estão verdes no mesmo SHA.
- [ ] Exemplos e laboratórios afetados foram executados.
- [ ] Schemas, IDs, links e contratos permanecem válidos.
- [ ] Baseline e candidato foram comparados quando aplicável.
- [ ] Regressões estão classificadas e tratadas.

## 4. Segurança e privacidade

- [ ] Threat model foi atualizado para mudanças relevantes.
- [ ] Segredos e dados pessoais não aparecem em código, logs, traces, artefatos ou mídia.
- [ ] Tenant, identidade, políticas, budgets e autoridade permanecem fora do controle livre do modelo.
- [ ] Prompt injection, tool abuse, memória, handoffs e egress foram avaliados quando aplicável.
- [ ] Aprovações estão vinculadas a identidade, ação, argumentos, tenant, versão e expiração.
- [ ] Timeout mutável usa `effect_unknown` e reconciliação, nunca retry cego.
- [ ] Hard gates críticos possuem resultado zero para violações.
- [ ] Riscos altos ou críticos possuem tratamento, owner e evidência.

## 5. Operação e recuperação

- [ ] Readiness, liveness e deep health foram verificados quando aplicável.
- [ ] Canary, janela de observação e abort criteria estão definidos.
- [ ] Rollback restaura artefato, configuração, política, schema, flags e estado compatível.
- [ ] Kill switch foi testado.
- [ ] Backups e restore foram testados dentro do RTO/RPO declarado.
- [ ] Filas, DLQ, idempotência, backpressure e reconciliação foram verificadas.
- [ ] Existe caminho manual seguro.

## 6. Conteúdo e pedagogia

- [ ] Objetivos, pré-requisitos, exercícios, avaliação e critérios de aprovação estão coerentes.
- [ ] Módulos, laboratórios, projetos e rubricas possuem navegação válida.
- [ ] Conteúdo não foi promovido para `stable` sem revisão humana e piloto aplicável.
- [ ] Alegações pedagógicas são proporcionais aos dados disponíveis.
- [ ] Limitações e risco residual estão explícitos.
- [ ] Feedback de estudantes foi registrado ou a ausência foi declarada.

## 7. Acessibilidade e internacionalização

- [ ] Imagens possuem texto alternativo e licença/proveniência.
- [ ] Diagramas possuem explicação textual equivalente.
- [ ] Headings, tabelas, links e ordem de leitura foram revisados.
- [ ] Conteúdo pode ser usado sem depender apenas de cor, animação ou interação visual.
- [ ] IDs canônicos foram preservados.
- [ ] Manifesto i18n foi atualizado quando aplicável.

## 8. Open source, licença e marca

- [ ] `LICENSE` e `LICENSING.md` cobrem os ativos publicados.
- [ ] Conteúdo de terceiros possui atribuição e termos compatíveis.
- [ ] Marca e identidade visual não são apresentadas como licença aberta irrestrita.
- [ ] README, QUICKSTART, CONTRIBUTING, SECURITY e Código de Conduta estão consistentes.
- [ ] Templates de issue e PR apontam para os canais corretos.

## 9. Evidence bundle

- [ ] Manifesto da release.
- [ ] SHA e relatórios de CI.
- [ ] Matriz de testes e regressões.
- [ ] Relatório de segurança e riscos residuais.
- [ ] Evidência de rollback/restore quando aplicável.
- [ ] Resultado de reprodução independente.
- [ ] Decisões e ADRs relevantes.
- [ ] Lista de limitações conhecidas.

## 10. Aprovações humanas

- [ ] Revisão técnica.
- [ ] Revisão pedagógica.
- [ ] Revisão de segurança e privacidade.
- [ ] Revisão de acessibilidade.
- [ ] Revisão de licença/marca.
- [ ] Aprovação do responsável pela release.

Registre nomes, datas e escopo aprovado. Aprovação genérica ou de SHA anterior não é válida para uma release alterada.

## Bloqueadores absolutos

A decisão deve ser `no-go` quando houver:

- segredo ou dado pessoal exposto;
- vazamento entre tenants ou escopos;
- efeito proibido ou duplicado;
- aprovação inválida aceita;
- retry cego após mutação ambígua;
- hard gate crítico ignorado;
- kill switch inoperante;
- rollback ou restore incompleto;
- evidência adulterada ou não reproduzível;
- risco alto ou crítico sem owner e tratamento;
- alegação de segurança, conformidade ou eficácia não sustentada.

## Registro final

```yaml
release_id: <id>
version: <semver-ou-identificador>
commit_sha: <sha-completo>
decision: no-go | go-with-constraints | go
scope: <escopo-exato>
constraints: []
blocking_findings: []
residual_risks: []
approvals:
  technical: null
  pedagogical: null
  security_privacy: null
  accessibility: null
  licensing_brand: null
  release_owner: null
reviewed_at: YYYY-MM-DD
```

## Limitações

Este checklist reduz omissões conhecidas, mas não substitui auditoria independente, revisão jurídica, pentest, operação real controlada ou validação pedagógica com estudantes.
