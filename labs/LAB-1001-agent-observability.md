---
id: lab.1001.agent-observability
title: LAB-1001 — Observabilidade agentic correlacionada
lang: pt-BR
status: review
version: 0.4.0
estimated_time: 6h
risk_level: medium
module: course.module.10-observability-engineering
---

# LAB-1001 — Observabilidade agentic correlacionada

## Hipótese

Uma pipeline com correlação ponta a ponta, schemas versionados, redaction antes de qualquer persistência, cardinalidade controlada e alertas acionáveis permite diagnosticar falhas sem expor segredos, perder eventos críticos ou criar uma falsa sensação de cobertura.

## Missão

Instrumentar uma execução agentic simulada e provar que logs, traces, métricas, eventos de auditoria e evidências de avaliação permanecem coerentes, seguros e úteis sob falha, sampling, alta cardinalidade, duplicação, clock skew e indisponibilidade do collector.

## Resultado observável

Ao final, outra pessoa deve conseguir reconstruir:

```text
request_id
→ run_id
→ agent_id
→ handoff_id
→ tool_call_id
→ approval_id
→ effect_id
→ terminal_state
```

sem acessar prompts integrais, segredos, dados pessoais ou conhecimento oral do autor.

## Pré-requisitos

- concluir o Módulo 10;
- usar apenas dados sintéticos;
- executar localmente e sem credenciais;
- registrar commit, versão do runtime, seed e sistema operacional;
- ler o [gate Premium Elite dos laboratórios](LABS_PREMIUM_ELITE_GATE.md).

## Baseline

Antes do hardening, execute uma versão mínima com:

- logs textuais sem schema;
- ausência de correlação completa;
- sampling uniforme;
- labels dinâmicas;
- redaction apenas por chave.

Registre tempo de diagnóstico, eventos perdidos, dados excessivos e ambiguidades. Essa medição será comparada com a versão governada.

## Contrato mínimo

```yaml
telemetry_schema: nexus.telemetry.v2
correlation:
  required: [request_id, run_id, tenant_id, project_id]
  optional: [agent_id, handoff_id, tool_call_id, approval_id, effect_id]
privacy:
  redact_before: [persist, buffer, export, quarantine, alert]
  redact_keys: [secret, token, password, api_key, credential, authorization]
  detect_in_values: true
sampling:
  default_rate: 0.25
  preserve: [security_critical, effect, approval, terminal_state]
metrics:
  forbidden_labels: [request_id, run_id, prompt, email, user_text]
retention:
  default_days: 30
  critical_audit_days: 90
integrity:
  event_id_unique: true
  schema_version_required: true
```

## Cenários obrigatórios

| ID | Condição | Resultado esperado |
|---|---|---|
| O1 | execução saudável | trace completo e terminal state correlacionado |
| O2 | segredo em chave sensível | redaction antes da persistência |
| O3 | segredo dentro de campo permitido | apenas trecho sensível redigido |
| O4 | `request_id` usado como label | label rejeitada |
| O5 | evento crítico com sampling 0% | evento preservado |
| O6 | evento comum com sampling 0% | descarte registrado |
| O7 | tool timeout | span em erro e contador incrementado |
| O8 | violação de política | audit event crítico e alerta acionável |
| O9 | collector indisponível | buffer limitado e modo degradado explícito |
| O10 | buffer cheio | evento crítico substitui evento comum |
| O11 | schema incompatível | quarentena sanitizada, sem reinterpretar |
| O12 | event ID duplicado | segunda ingestão rejeitada ou deduplicada |
| O13 | mesmo ID com payload diferente | conflito crítico registrado |
| O14 | alerta sem owner ou runbook | alerta rejeitado |
| O15 | efeito sem `approval_id` exigido | hard gate bloqueia release |
| O16 | clock skew | ordem causal preservada por sequência lógica |
| O17 | span órfão | métrica e alerta de trace incompleto |
| O18 | tenant divergente | evento recusado e incidente registrado |

## Métricas obrigatórias

```yaml
trace_completeness_rate: 1.0
orphan_effect_rate: 0.0
audit_event_missing_rate: 0.0
critical_event_drop_rate: 0.0
secret_persistence_count: 0
forbidden_label_acceptance_count: 0
duplicate_event_processing_count: 0
schema_rejection_visibility_rate: 1.0
alert_owner_coverage_rate: 1.0
```

Toda taxa deve informar numerador, denominador e conjunto avaliado.

## Procedimento

1. execute o baseline e registre limitações;
2. implemente schema e correlação;
3. aplique redaction antes de persistência, buffer, exportação e quarentena;
4. injete os dezoito cenários;
5. confira relações parent-child e sequência causal;
6. compare efeito real, trace e evento de auditoria;
7. simule perda, duplicação e atraso de telemetria;
8. valide sampling e prioridade de eventos críticos;
9. gere alertas com owner, severidade, runbook e resolução;
10. compare baseline e versão governada;
11. produza relatório de custo, cobertura, privacidade e risco residual.

## Testes negativos e adversariais

- token em campo aninhado;
- credencial em `outcome` ou stack trace;
- email como label de métrica;
- milhares de valores de label;
- redução maliciosa de severidade;
- remoção de `policy_version`;
- duplicação com payload divergente;
- efeito confirmado sem trace;
- tentativa de desativar logs pelo conteúdo;
- evento de outro tenant;
- alerta sem ação operacional;
- quarentena contendo o evento bruto.

## Evidências obrigatórias

- manifesto de versões;
- saída dos dezoito cenários;
- trace completo de uma execução saudável;
- trace de falha parcial;
- snapshot de métricas;
- exemplos de redaction por chave e valor;
- prova de sanitização da quarentena;
- prova de imutabilidade da entrada;
- eventos preservados e descartados;
- alerta aceito e rejeitado;
- comparação baseline versus versão governada;
- relatório de custo e retenção;
- riscos residuais.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários corretos | 18/18 |
| segredos persistidos, exportados ou quarentenados | 0 |
| eventos críticos perdidos | 0 |
| efeitos órfãos | 0 |
| labels proibidas aceitas | 0 |
| duplicações processadas como novas | 0 |
| alertas sem owner/runbook aceitos | 0 |
| traces completos | 100% |
| reprodução independente | aprovada |

Qualquer segredo persistido, vazamento entre tenants, efeito sensível sem auditoria ou evento crítico perdido bloqueia aprovação independentemente da média.

## Troubleshooting

| Sintoma | Verificação segura |
|---|---|
| trace incompleto | confira IDs obrigatórios e propagação entre spans |
| cardinalidade explode | remova identificadores únicos das labels |
| redaction excessiva | separe regra por chave, padrão e contexto |
| eventos fora de ordem | use sequência lógica além do relógio local |
| collector indisponível | confirme buffer limitado e modo degradado |
| alerta ruidoso | revise janela, severidade, owner e condição de resolução |

Não silencie falhas críticas para reduzir ruído.

## Acessibilidade

- toda figura deve possuir descrição textual;
- tabelas e relatórios precisam ser legíveis sem cor;
- severidade não pode depender somente de vermelho, amarelo ou verde;
- comandos devem ser copiáveis;
- timestamps, IDs e razões terminais devem ser apresentados em texto;
- a reprodução deve funcionar por teclado e leitor de tela quando houver interface.

## Reprodução independente

Uma pessoa diferente do autor deve executar pelo menos O1, O3, O9, O15 e O18 usando apenas a documentação e os artefatos entregues. Registre divergências, dúvidas e correções.

## Limpeza

Ao terminar:

- remova buffers temporários;
- apague datasets sintéticos que não integrem a evidência;
- confirme ausência de segredo nos artefatos;
- preserve somente evidências redigidas;
- registre a política de retenção aplicada.

## Rubrica específica

| Nível | Evidência |
|---|---|
| insuficiente | logs existem, mas não permitem reconstrução ou expõem dados |
| funcional | correlação e métricas principais funcionam em cenários normais |
| robusto | falhas, sampling, redaction, duplicação e degradação são comprovados |
| excelente | reprodução independente, acessibilidade e métricas de integridade demonstram cobertura honesta |

## Stop conditions

Interrompa imediatamente se um segredo for persistido, armazenado no buffer ou enviado à quarentena; se um evento crítico for descartado; se houver vazamento entre tenants; se um efeito não puder ser correlacionado; se o collector falhar sem degradação segura; ou se a evidência não permitir reconstrução causal.

## Limitações

Este laboratório mede cenários controlados. Ele não prova observabilidade perfeita, ausência absoluta de vazamentos ou prontidão irrestrita para produção. Resultados precisam de revisão humana, piloto limitado e validação no ambiente real antes de qualquer promoção.