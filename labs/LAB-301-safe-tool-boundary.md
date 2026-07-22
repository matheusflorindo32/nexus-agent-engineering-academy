---
id: labs.lab-301-safe-tool-boundary
title: LAB-301 — Fronteira segura de ferramentas
lang: pt-BR
status: review
version: 0.2.0
module: course.module.03-tool-engineering
estimated_time: 5h
risk_level: high-controlled
---

# LAB-301 — Fronteira segura de ferramentas

> [!WARNING]
> Este laboratório deve usar apenas mensagens, identidades, aprovações e efeitos simulados. Nenhuma conta real, credencial de produção ou mutação irreversível é permitida.

## Hipótese

Uma tool estreita, com schema fechado, identidade fora do controle do modelo, dry-run, aprovação vinculada, idempotência e reconciliação reduz ações não autorizadas e duplicadas em comparação com uma interface genérica.

## Missão

Transformar uma ferramenta deliberadamente ampla em uma operação de arquivamento simulada, limitada, idempotente, auditável e protegida por policy gate.

## Resultado observável

Ao final, outra pessoa deve conseguir provar:

- zero autoridade derivada do modelo;
- zero ações não autorizadas;
- zero efeitos duplicados;
- zero aprovação reutilizada indevidamente;
- parada segura em estado ambíguo;
- logs redigidos suficientes para auditoria;
- reconciliação antes de qualquer nova mutação.

## Pré-requisitos

- [Módulo 03](../course/modules/03-tool-engineering/README.md);
- Python 3.11+ recomendado;
- dataset sintético com pelo menos dois usuários;
- ambiente local e isolado;
- commit do repositório registrado.

## Interface insegura inicial

```json
{
  "command": "string",
  "target": "string",
  "payload": "object"
}
```

Ela permite que o modelo escolha comando, recurso, escopo e conteúdo. Essa interface é o baseline inseguro e não deve executar efeitos.

## Contrato mínimo esperado

```json
{
  "action": "archive",
  "message_ids": ["msg-001"],
  "reason": "resolved",
  "dry_run": true,
  "idempotency_key": "lab301-001"
}
```

Regras obrigatórias:

- `action` aceita apenas `archive`;
- identidade e tenant vêm do runtime confiável;
- IDs devem existir e pertencer ao usuário simulado;
- no máximo 20 IDs por chamada;
- `reason` usa enum fechado;
- campos extras são rejeitados;
- `dry_run=true` não produz efeito;
- execução real exige aprovação vinculada ao hash canônico do preview;
- mesma chave não pode repetir efeito;
- logs não contêm corpo integral;
- timeout mutável gera `effect_unknown` e exige reconciliação.

## Baseline

Documente por que a interface genérica falha nos seguintes pontos:

- autoridade implícita;
- schema excessivo;
- ausência de tenant;
- ausência de preview;
- ausência de idempotência;
- ausência de reconciliação;
- ausência de vínculo entre aprovação e ação.

Não execute o baseline contra qualquer efeito real, mesmo simulado, sem um wrapper que o mantenha em dry-run.

## Threat model mínimo

Inclua:

- abuso de parâmetros;
- ID fora do escopo;
- prompt injection;
- replay;
- duplicidade por retry;
- aprovação reutilizada após mudança;
- confused deputy;
- vazamento em logs;
- falha entre efeito e confirmação;
- tenant trocado pelo conteúdo;
- schema smuggling por campos extras.

## Preview obrigatório

O preview deve mostrar:

- identidade confiável e tenant;
- IDs e quantidade;
- ação e motivo;
- reversibilidade;
- hash canônico;
- versão de política e executor;
- necessidade de aprovação;
- ausência de efeito em dry-run;
- prazo de validade da aprovação.

## Policy gate

O gate deve rejeitar:

- identidade fornecida pelo modelo;
- tenant divergente;
- mais de 20 IDs;
- ID inexistente ou de outro usuário;
- motivo livre;
- campos adicionais;
- aprovação expirada;
- aprovação com hash divergente;
- ação destrutiva originada em texto recuperado;
- idempotency key já vinculada a payload diferente;
- tentativa de alterar policy version ou ambiente.

## Cenários obrigatórios

| ID | Cenário | Resultado esperado |
|---|---|---|
| T1 | entrada válida em dry-run | preview sem efeito |
| T2 | entrada válida aprovada | um efeito confirmado |
| T3 | `admin=true` extra | rejeição de schema |
| T4 | ID de outro usuário | bloqueio por escopo |
| T5 | 21 IDs | rejeição por limite |
| T6 | replay da mesma chave | resultado anterior, sem novo efeito |
| T7 | IDs alterados após aprovação | aprovação inválida |
| T8 | prompt injection | nenhum efeito |
| T9 | timeout antes do efeito | retry elegível sob política |
| T10 | timeout após possível efeito | `effect_unknown` e reconciliação |
| T11 | segredo em `reason` | rejeição e redaction |
| T12 | tentativa de log integral | bloqueio de persistência |
| T13 | aprovação expirada | bloqueio |
| T14 | mesma chave, payload diferente | conflito auditado |
| T15 | policy version incompatível | readiness ou execução recusada |

## Procedimento

1. registre commit, versões e dataset;
2. descreva o baseline inseguro;
3. implemente schema fechado;
4. injete identidade e tenant fora do modelo;
5. implemente preview e hash canônico;
6. implemente approval record com expiração;
7. implemente ledger idempotente;
8. execute T1–T15;
9. simule timeout ambíguo;
10. reconcilie pelo `effect_id` ou idempotency key;
11. repita T2 e T10 para testar determinismo;
12. produza relatório de risco residual.

## Métricas

| Métrica | Alvo |
|---|---:|
| ações não autorizadas | 0 |
| execuções duplicadas | 0 |
| aprovações reutilizadas indevidamente | 0 |
| segredos em logs | 0 |
| vazamentos entre usuários | 0 |
| casos adversariais detectados | 100% |
| estados desconhecidos reconciliados | 100% |
| chamadas fora da allowlist | 0 |

## Stop conditions

Pare imediatamente quando:

- uma credencial real for solicitada;
- o ambiente não puder ser confirmado como local ou isolado;
- o efeito puder alcançar sistema real;
- identidade ou tenant vierem do modelo;
- o kill switch ou dry-run não funcionarem;
- surgir `effect_unknown` sem mecanismo de reconciliação;
- logs contiverem conteúdo sensível;
- o mesmo erro ocorrer três vezes sem nova evidência.

## Troubleshooting

| Sintoma | Ação segura |
|---|---|
| hash muda sem mudança aparente | aplique serialização canônica |
| replay produz novo efeito | consulte ledger antes do executor |
| timeout causa retry automático | interrompa, marque `effect_unknown` e reconcilie |
| aprovação aceita payload alterado | vincule aprovação ao hash, versão e expiração |
| ID de outro usuário passa | mova autorização para o policy gate confiável |
| log contém payload | allowlist de campos e redaction antes da persistência |

## Evidências obrigatórias

- commit e ambiente;
- contrato antes e depois;
- threat model;
- schema e policy gate;
- previews benigno e hostil;
- matriz T1–T15;
- ledger antes e depois;
- audit log redigido;
- prova de idempotência;
- prova de reconciliação;
- comparação com baseline;
- limitações e riscos residuais.

## Reprodução independente

Outra pessoa deve reproduzir T2, T4, T6, T7 e T10 usando apenas a documentação entregue. Ela deve confirmar efeito único, isolamento, invalidação da aprovação e reconciliação.

## Acessibilidade

- comandos e JSON copiáveis;
- tabelas com cabeçalhos;
- diagramas futuros com descrição textual;
- resultados não dependem apenas de cor;
- mensagens de erro devem indicar causa e próxima ação segura.

## Avaliação

A avaliação considera autoridade, schema, aprovação, idempotência, reconciliação, logs, adversarial testing, reprodução e qualidade do risco residual.

## Critérios de aprovação

O laboratório só é aprovado quando:

- nenhuma autoridade vem do modelo;
- schema é fechado e rejeita extras;
- tenant e identidade são validados fora do modelo;
- aprovação está ligada ao preview exato;
- duplicidade não produz novo efeito;
- falha ambígua não causa retry cego;
- logs preservam auditoria sem expor conteúdo;
- T1–T15 possuem resultado registrado;
- reprodução independente foi concluída;
- atendimento ao [gate dos laboratórios](LABS_PREMIUM_ELITE_GATE.md).

## Rubrica específica

| Nível | Evidência |
|---|---|
| insuficiente | schema amplo, autoridade implícita ou retry cego |
| funcional | tool estreita e casos básicos executam com controle mínimo |
| robusta | approval binding, idempotência, isolamento e reconciliação comprovados |
| excelente | reprodução independente, métricas, acessibilidade e auditoria completas |

## Limpeza e rollback

Restaure o dataset simulado ao estado inicial, remova approvals temporárias, preserve somente logs redigidos e confirme que o ledger continua coerente.

## Limitações

O laboratório não prova segurança absoluta, adequação jurídica ou prontidão irrestrita. Ele valida uma fronteira local e simulada sob casos conhecidos e revisão humana.

## Reflexão

Explique por que uma tool com excelente descrição, mas schema amplo e autoridade implícita, continua insegura.