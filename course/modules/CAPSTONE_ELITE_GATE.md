---
id: course.gate.capstone-elite
title: Gate Premium Elite — Capstone production-grade
lang: pt-BR
status: review
---

# Gate Premium Elite — Capstone production-grade

Este gate define as condições mínimas para concluir o capstone e promover o Módulo 12 de `review` para `stable`.

## Bloqueios absolutos

A conclusão é proibida quando existir qualquer um dos itens abaixo:

- violação crítica de segurança;
- vazamento entre tenants ou projetos;
- segredo persistido em prompt, log, trace ou artefato;
- efeito externo duplicado;
- retry cego após timeout mutável;
- autoridade ampliada pelo modelo;
- efeito sensível sem aprovação vinculada;
- hard gate ignorado ou compensado por média;
- ausência de kill switch funcional;
- rollback incompleto ou não testado;
- trace incapaz de reconstruir decisão, aprovação e efeito;
- demo dependente de informação tácita ou segredo compartilhado;
- risco crítico ou alto sem tratamento e owner;
- alegação de conformidade, segurança absoluta ou prontidão irrestrita sem evidência.

## Evidências de escopo e produto

- [ ] Problema, usuário e valor observável estão definidos.
- [ ] Requisitos e non-goals são rastreáveis.
- [ ] Critérios de aceitação são testáveis.
- [ ] Baseline mais simples foi implementado ou analisado.
- [ ] A opção agentic demonstra benefício líquido.
- [ ] Vertical slice executável está disponível.

## Evidências arquiteturais

- [ ] Diagramas de contexto e componentes estão atualizados.
- [ ] Fronteiras de confiança estão identificadas.
- [ ] Control, data, state e observability plane estão separados.
- [ ] Contratos de contexto, tool, loop, memória e automação estão versionados.
- [ ] ADRs registram decisões e alternativas rejeitadas.
- [ ] Estratégia de degradação segura está documentada.

## Evidências de segurança e privacidade

- [ ] Threat model possui ativos, atores, abuse cases, controles e owners.
- [ ] Deny-by-default e least privilege são demonstrados.
- [ ] Prompt injection direta e indireta são testadas.
- [ ] Tenant, projeto e finalidade são validados.
- [ ] Aprovações estão vinculadas ao artefato exato.
- [ ] Redaction ocorre antes da persistência.
- [ ] Riscos residuais estão explícitos.
- [ ] Revisão humana de segurança e privacidade foi concluída.

## Evidências de avaliação

- [ ] Dataset e graders estão versionados.
- [ ] Baseline e candidato foram comparados em condições equivalentes.
- [ ] Casos críticos, adversariais e de regressão foram executados.
- [ ] Hard gates bloquearam release em cenários negativos.
- [ ] Variância e flakiness foram registradas quando relevantes.
- [ ] Relatório de avaliação contém decisão e justificativa.

## Evidências operacionais

- [ ] SLI, SLO e error budget estão definidos.
- [ ] Canary possui abort criteria.
- [ ] Rollback restaura artefato, configuração, política, schema e estado compatível.
- [ ] Kill switch foi testado.
- [ ] Runbooks possuem owner e condição de resolução.
- [ ] Backup e restore foram testados quando aplicáveis.
- [ ] Piloto controlado possui escopo, janela, rollback e owner.

## Evidências de automação

- [ ] Reentrega e concorrência não duplicam efeitos.
- [ ] Idempotency keys e ledger são demonstrados.
- [ ] Retry budget, backoff e timeout são limitados.
- [ ] `effect_unknown` exige reconciliação.
- [ ] DLQ possui owner e política.
- [ ] Compensação é explícita, idempotente e auditável.
- [ ] Existe caminho manual.

## Evidências de observabilidade

- [ ] Correlação ponta a ponta está completa.
- [ ] Logs, traces, métricas e eventos de auditoria possuem schemas versionados.
- [ ] Eventos críticos não são descartados por sampling.
- [ ] Cardinalidade e retenção são governadas.
- [ ] Alertas possuem impacto, owner, runbook e resolução.
- [ ] Falha do collector possui degradação segura.
- [ ] Efeitos órfãos, eventos ausentes e duplicações são detectáveis.

## Game day

- [ ] Dependência indisponível foi simulada.
- [ ] Prompt injection indireta foi simulada.
- [ ] Budget anormal foi consumido.
- [ ] Timeout com efeito desconhecido foi simulado.
- [ ] Falha do collector foi simulada.
- [ ] Reentrega concorrente foi simulada.
- [ ] Invariantes de segurança e idempotência foram preservadas.
- [ ] Evidências e ações do operador foram registradas.
- [ ] Postmortem e casos de regressão foram produzidos.

## Reprodutibilidade e acessibilidade

- [ ] Outra pessoa executou a demo sem segredo compartilhado.
- [ ] Instruções funcionam em Windows, Linux e macOS, ou limitações estão explícitas.
- [ ] Diagramas possuem descrição textual.
- [ ] Conteúdo não depende apenas de cor, áudio ou animação.
- [ ] Vídeos futuros possuem legenda e transcrição.
- [ ] Documentação é navegável por teclado e leitor de tela no futuro portal.
- [ ] Dificuldades de reprodução foram registradas e corrigidas.

## Defesa técnica

- [ ] O estudante justificou por que o problema exige ou não exige agente.
- [ ] Explicou onde reside a autoridade real.
- [ ] Demonstrou falha fechada.
- [ ] Explicou prevenção de efeitos duplicados.
- [ ] Defendeu a decisão de release com evidência.
- [ ] Demonstrou contenção e recuperação.
- [ ] Declarou limitações e riscos residuais.
- [ ] Identificou simplificações futuras.

## CI e integração

- [ ] Documentation quality está verde.
- [ ] NEXUS Quality está verde.
- [ ] O SHA aprovado é o mesmo validado pelo CI.
- [ ] A pilha de PRs foi integrada na ordem correta.
- [ ] Nenhum merge automático foi utilizado.
- [ ] A integração recebeu aprovação humana explícita.

## Regra de conclusão

O capstone só pode ser concluído quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. todas as evidências aplicáveis estiverem anexadas;
3. o projeto atingir nível funcional ou superior em todas as dimensões bloqueantes;
4. o game day preservar invariantes e produzir evidência;
5. a reprodução independente for bem-sucedida;
6. revisões humanas estiverem registradas;
7. o CI estiver verde no mesmo SHA aprovado;
8. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.