---
id: labs.gate.premium-elite
title: Gate Premium Elite — Laboratórios
lang: pt-BR
status: review
---

# Gate Premium Elite — Laboratórios

Este gate define as condições mínimas para declarar um laboratório NEXUS validado além do estado `review`.

## Bloqueios absolutos

A promoção é proibida quando existir qualquer um dos seguintes itens:

- uso de segredo, credencial de produção ou dado pessoal real;
- efeito irreversível sem ambiente isolado e aprovação humana;
- evidência que apenas afirma sucesso sem demonstrá-lo;
- teste negativo crítico ausente;
- stop condition inexistente ou inoperante;
- timeout mutável seguido de retry cego;
- vazamento entre tenant, projeto ou execução;
- log ou artefato contendo segredo;
- procedimento que depende de conhecimento tácito não documentado;
- laboratório não reproduzido por pessoa diferente do autor;
- risco alto ou crítico sem mitigação e owner;
- CI falho ou executado em SHA diferente do avaliado.

## Contrato documental obrigatório

- [ ] Frontmatter válido.
- [ ] Status `review` enquanto o gate não estiver concluído.
- [ ] Hipótese falsificável.
- [ ] Missão com resultado observável.
- [ ] Pré-requisitos e materiais.
- [ ] Preparação reproduzível.
- [ ] Procedimento numerado.
- [ ] Cenários obrigatórios.
- [ ] Testes negativos ou adversariais.
- [ ] Stop conditions.
- [ ] Evidências esperadas.
- [ ] Critérios de aprovação.
- [ ] Rubrica de quatro níveis.
- [ ] Acessibilidade.
- [ ] Limitações e risco residual.
- [ ] Limpeza, rollback ou reconciliação quando aplicável.

## Evidências técnicas

- [ ] Commit SHA registrado.
- [ ] Sistema operacional e runtime registrados.
- [ ] Comandos executados documentados.
- [ ] Configuração relevante versionada.
- [ ] Baseline registrado.
- [ ] Cenário positivo executado.
- [ ] Cenário negativo executado.
- [ ] Cenário adversarial executado quando aplicável.
- [ ] Falhas e bloqueios preservados.
- [ ] Evidências redigidas sem segredos.
- [ ] Resultado reproduzido por outra pessoa.
- [ ] CI verde no SHA final.

## Segurança e privacidade

- [ ] Dados são sintéticos ou devidamente anonimizados e autorizados.
- [ ] Credenciais são fake, temporárias ou sem privilégio.
- [ ] Ambiente é local, simulado ou isolado.
- [ ] Tenant e projeto permanecem segregados.
- [ ] Efeitos mutáveis usam idempotência.
- [ ] Timeout ambíguo exige reconciliação.
- [ ] Logs passam por redaction antes da persistência.
- [ ] Retenção e descarte de evidências estão definidos.
- [ ] Risco residual possui owner e tratamento explícito.

## Validação pedagógica

- [ ] Objetivo do laboratório é compreensível sem explicação oral do autor.
- [ ] Tempo estimado foi confrontado com execução real.
- [ ] Instruções foram testadas por pessoa com perfil compatível ao público-alvo.
- [ ] Erros comuns e troubleshooting foram registrados.
- [ ] Rubrica foi aplicada de forma consistente.
- [ ] Feedback do reprodutor independente foi incorporado ou justificado.
- [ ] O laboratório mede aprendizagem, não apenas cumprimento mecânico de passos.

## Acessibilidade

- [ ] Estrutura de títulos é navegável.
- [ ] Diagramas possuem descrição textual.
- [ ] Informação não depende apenas de cor.
- [ ] Comandos e resultados estão disponíveis em texto.
- [ ] Siglas são expandidas na primeira ocorrência.
- [ ] Instruções não dependem somente de posição visual.
- [ ] Conteúdo audiovisual futuro possui legenda e transcrição.

## Validação por risco

### Risco baixo

Exige revisão técnica, pedagógica, acessibilidade e reprodução independente.

### Risco médio

Além dos itens anteriores, exige teste adversarial, rollback ou limpeza e revisão de segurança.

### Risco alto controlado

Além dos itens anteriores, exige:

- ambiente isolado;
- plano de contenção;
- kill switch quando aplicável;
- owner explícito;
- revisão humana de segurança;
- evidência de não duplicação ou não vazamento;
- postmortem quando houver game day ou incidente simulado.

## Regra de promoção

Um laboratório somente pode sair de `review` quando:

1. nenhum bloqueio absoluto estiver presente;
2. todos os itens proporcionais ao risco estiverem comprovados;
3. a reprodução independente estiver registrada;
4. revisões técnica, pedagógica, acessibilidade e segurança aplicável estiverem concluídas;
5. o CI estiver verde no mesmo SHA;
6. houver aprovação humana explícita.

Até lá, o status correto permanece `review`.