---
id: governance.maintainers-guide
title: Guia de mantenedores NEXUS
lang: pt-BR
status: review
version: 0.1.0
---

# Guia de mantenedores NEXUS

## Propósito

Este guia organiza decisões técnicas, pedagógicas, editoriais, de segurança e de release sem transformar autoridade de manutenção em aprovação automática. O papel do maintainer é preservar invariantes, exigir evidência proporcional ao risco e tornar decisões revisáveis.

## Princípios obrigatórios

1. **Nenhum merge por inércia:** CI verde é condição necessária, não suficiente.
2. **Hard gates prevalecem:** segurança, privacidade, rastreabilidade e efeitos externos não são compensados por média.
3. **Menor privilégio:** identidade, tenant, budgets, políticas e aprovação ficam fora do controle livre do modelo.
4. **Evidência antes de status:** material educacional permanece `review` até revisão humana e piloto aplicável.
5. **Pilha pequena:** PRs devem ser coesos, ordenados e revisáveis.
6. **Sem alegações absolutas:** não declarar segurança, conformidade, eficácia ou prontidão além do escopo comprovado.
7. **Correção sem culpabilização:** falhas geram melhoria de sistema, documentação e regressão.

## Papéis de revisão

Uma pessoa pode exercer mais de um papel em mudanças de baixo risco, mas mudanças de risco alto controlado exigem separação mínima entre autor e aprovador.

| Papel | Responsabilidade |
|---|---|
| triage | confirmar escopo, duplicidade, risco e rota correta |
| técnico | contratos, implementação, testes, compatibilidade e falhas |
| pedagógico | objetivos, progressão, prática, avaliação e feedback |
| segurança/privacidade | threat model, autoridade, dados, logs e efeitos |
| acessibilidade | navegação, linguagem, alternativas textuais e mídia |
| release | versões, migrações, rollout, rollback e evidências |

## Classificação de risco

### Baixo

Documentação, navegação, texto alternativo, correção de link ou melhoria editorial sem alterar contrato, autoridade, validação ou execução.

### Médio

Exemplo, laboratório, schema ou validador isolado sem infraestrutura real, segredo ou efeito externo.

### Alto controlado

Segurança, autenticação, tenant, memória persistente, tools mutáveis, automação, migração, release, rollback ou qualquer mudança capaz de produzir efeito externo.

Mudança de risco alto controlado exige:

- threat model atualizado;
- testes negativos e adversariais;
- owner e stop conditions;
- evidência de rollback ou reconciliação;
- revisão humana independente;
- decisão explícita de `blocked`, `manual_review` ou `ready_for_human_review`.

## Fluxo de triagem

1. Verifique se a issue usa o canal correto.
2. Remova ou solicite remoção de dados sensíveis.
3. Confirme reprodução, versão e resultado esperado.
4. Classifique área e risco.
5. Identifique hard gates aplicáveis.
6. Divida escopos grandes antes da implementação.
7. Atribua owner ou marque como aguardando responsável.
8. Registre decisão e próxima ação.

## Revisão de pull request

### Antes de ler o diff

- confirme base, head e dependências;
- verifique se o PR permanece Draft quando apropriado;
- confirme risco e revisores necessários;
- valide que o SHA relatado corresponde à CI.

### Durante a revisão

- teste o caminho legítimo e os casos hostis;
- procure autoridade implícita, retry cego e estado ambíguo;
- verifique redaction antes de persistência;
- confirme que métricas possuem denominador e interpretação;
- valide links, IDs, referências e acessibilidade;
- rejeite mudanças que enfraqueçam validadores para obter sucesso.

### Antes da aprovação

- todos os bloqueadores estão fechados;
- a decisão é apoiada por evidence bundle;
- riscos residuais possuem owner e tratamento;
- migração, rollback e caminho manual existem quando aplicável;
- outra pessoa consegue reproduzir a evidência crítica;
- o merge foi explicitamente aprovado por humano autorizado.

## Integração de PRs empilhados

1. Integre na ordem da base para o topo.
2. Após cada integração, retarget/rebase apenas de forma controlada.
3. Reexecute a CI no novo SHA.
4. Não reutilize aprovação de SHA anterior sem revalidação.
5. Interrompa a pilha diante de conflito semântico, regressão ou hard gate.

## Segurança e incidentes

Vulnerabilidades não devem ser discutidas em issue pública. Siga `SECURITY.md`. Durante incidente:

1. contenha efeitos e preserve evidência;
2. acione kill switch quando necessário;
3. não faça retry cego de mutação ambígua;
4. reconcilie o estado real;
5. documente timeline e decisões;
6. produza regressão e ação corretiva com owner.

## Status e releases

- `review`: conteúdo ou controle ainda depende de validação humana, integração ou piloto;
- `stable`: exige critérios documentados, revisão humana e release aprovado;
- CI verde, badge ou merge isolado não autorizam mudança de status.

## Conflitos de interesse

Mantenedores devem declarar vínculo financeiro, autoria relevante, disputa acadêmica ou benefício direto que possa afetar a decisão. Quando houver conflito material, outra pessoa deve assumir a aprovação.

## Limitações

Este guia não substitui revisão especializada, política jurídica, auditoria de segurança ou teste com estudantes reais. Ele define governança mínima verificável para o estágio atual do projeto.
