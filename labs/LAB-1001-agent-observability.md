---
id: lab.1001.agent-observability
title: LAB-1001 — Observabilidade agentic correlacionada
lang: pt-BR
status: review
version: 0.3.0
estimated_time: 5h
---

# LAB-1001 — Observabilidade agentic correlacionada

## Hipótese

Uma pipeline com correlação, schema versionado, redaction por chave e conteúdo, cardinalidade controlada e alertas acionáveis permite diagnosticar falhas sem expor segredos nem perder eventos críticos.

## Missão

Instrumentar uma execução agentic simulada e provar que logs, traces, métricas, quarentena e eventos de auditoria permanecem coerentes, seguros e úteis sob falha, sampling, alta cardinalidade e tentativas de ocultar credenciais dentro de campos permitidos.

## Cenários obrigatórios

| ID | Condição | Resultado esperado |
|---|---|---|
| O1 | execução saudável | trace completo e métricas atualizadas |
| O2 | segredo em chave sensível | valor redigido antes da persistência |
| O3 | `request_id` usado como label | label rejeitada |
| O4 | evento crítico com sampling 0% | evento preservado |
| O5 | evento comum com sampling 0% | evento descartado |
| O6 | tool timeout | span em erro e contador incrementado |
| O7 | violação de política | audit event crítico e alerta |
| O8 | collector indisponível | buffer limitado e degradação explícita |
| O9 | buffer cheio | evento crítico substitui evento comum |
| O10 | schema incompatível | evento quarentenado |
| O11 | duplicação de event ID | segunda ingestão ignorada |
| O12 | alerta sem owner/runbook | alerta rejeitado |
| O13 | segredo embutido em atributo permitido | apenas o trecho sensível é redigido |
| O14 | credencial de autorização em texto | credencial redigida antes da persistência |
| O15 | schema incompatível com segredo | quarentena recebe somente representação sanitizada e a entrada permanece imutável |

## Contratos mínimos

```yaml
telemetry_schema: nexus.telemetry.v1
correlation:
  request_id: required
  run_id: required
sampling:
  default_rate: 0.25
  preserve_severities: [critical]
privacy:
  allowed_attributes: [tool, outcome, duration_ms, policy_version]
  redact_keys: [secret, token, password, api_key, credential]
  redact_values: [key_value_credentials, authorization_credentials, known_token_prefixes]
  order: redact_before_persist_buffer_or_quarantine
metrics:
  forbidden_labels: [request_id, run_id, prompt, email]
retention_days: 30
```

## Procedimento

1. Execute a implementação de referência.
2. Gere uma execução saudável com dois spans e um efeito externo.
3. Injete os quinze cenários obrigatórios.
4. Verifique IDs e relações parent-child.
5. Inspecione a saída persistida e confirme ausência de segredos.
6. Injete credenciais dentro de `tool` e `outcome`, embora sejam campos permitidos.
7. Injete um evento de schema incompatível contendo credencial sintética.
8. Confirme que a quarentena recebe apenas a representação sanitizada.
9. Confirme que o evento original não foi modificado.
10. Valide métricas e ausência de labels proibidas.
11. Simule indisponibilidade do collector e saturação do buffer.
12. Gere alertas de latência e segurança.
13. Confirme owner, runbook e condição de resolução.
14. Produza relatório com limitações, falsos positivos, falsos negativos e riscos residuais.

## Evidências

- saída do autoteste 15/15;
- amostra de trace correlacionado;
- snapshot das métricas;
- prova de redaction por chave;
- prova de redaction dentro de valores permitidos;
- prova de sanitização da quarentena;
- prova de imutabilidade do evento de entrada;
- lista de eventos preservados e descartados;
- alerta aceito e alerta rejeitado;
- demonstração de buffer e prioridade;
- reflexão sobre privacidade, custo e lacunas.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários corretos | 15/15 |
| segredos persistidos | 0 |
| segredos enviados à quarentena | 0 |
| eventos de entrada modificados | 0 |
| eventos críticos perdidos | 0 |
| labels proibidas aceitas | 0 |
| eventos duplicados processados | 0 |
| schemas incompatíveis reinterpretados | 0 |
| alertas sem owner/runbook aceitos | 0 |
| efeitos sem correlação | 0 |

## Testes adversariais

- inserir token em campo aninhado;
- inserir `token=valor` dentro de atributo permitido;
- inserir credencial de autorização dentro de `outcome`;
- inserir segredo em evento enviado à quarentena;
- confirmar que a entrada original continua intacta;
- variar maiúsculas, espaços e delimitadores;
- usar email como nome de métrica;
- criar milhares de labels dinâmicas;
- tentar reduzir severidade de evento crítico;
- remover `policy_version` do audit event;
- duplicar event ID com payload diferente;
- encher o buffer com eventos comuns antes de uma violação crítica;
- gerar alerta sem ação operacional.

## Comando

```bash
python examples/observability_pipeline.py --self-test
```

## Stop conditions

Interrompa se um segredo for persistido, armazenado no buffer ou enviado à quarentena; se o evento de entrada for modificado; se um evento crítico for descartado; se uma label de alta cardinalidade for aceita; se um efeito externo não puder ser correlacionado; se um schema incompatível for reinterpretado silenciosamente; ou se um alerta sem owner e runbook for emitido.
