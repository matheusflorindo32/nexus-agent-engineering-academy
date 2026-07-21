---
id: adr.002.observability-redaction
title: ADR-002 — Redaction defensiva na telemetria
lang: pt-BR
status: review
---

# ADR-002 — Redaction defensiva na telemetria

## Status

Proposto para revisão humana. A decisão é efetiva apenas após merge explícito.

## Contexto

A implementação inicial removia valores apenas quando o nome da chave continha `token`, `secret` ou `password`. Isso permitia persistir credenciais embutidas em atributos permitidos, por exemplo `tool="catalog.read token=abc123"`. Eventos incompatíveis enviados à quarentena também exigem tratamento explícito para não criar um canal alternativo de persistência de dados sensíveis.

A revisão adversarial do PR #8 identificou ainda dois riscos de confiabilidade operacional:

1. um evento comum removido do buffer para priorizar um evento crítico permanecia registrado como visto, fazendo um reenvio legítimo retornar `duplicate` mesmo sem existir em `persisted`, `buffer` ou `quarantine`;
2. a redaction de um `owner` de alerta poderia produzir um responsável não acionável, como `[REDACTED]`.

## Decisão

Aplicar redaction antes de qualquer persistência, bufferização, quarentena ou emissão operacional. A sanitização deve:

1. identificar chaves sensíveis;
2. identificar credenciais dentro de valores textuais permitidos;
3. percorrer estruturas aninhadas;
4. preservar conteúdo não sensível e o tipo de coleção quando possível;
5. não modificar o objeto de entrada;
6. produzir resultado determinístico;
7. falhar de forma segura diante de formatos desconhecidos;
8. remover o estado de deduplicação de eventos efetivamente evictados do buffer;
9. preservar um identificador operacional acionável para `owner` de alertas;
10. rejeitar owners sensíveis que não possam ser normalizados com segurança.

## Padrões mínimos cobertos

- pares `token`, `secret`, `password`, `api_key`, `apikey`, `access_token`, `refresh_token` e `client_secret`;
- esquemas `Bearer` e `Basic`;
- prefixos conhecidos de credenciais usados em testes sintéticos;
- estruturas `dict`, `list` e `tuple`;
- conteúdo aninhado em atributos permitidos;
- owners operacionais estáveis, incluindo normalização do identificador local de e-mails sintéticos;
- referências de runbook em caminho Markdown ou URL HTTPS sanitizada.

Os testes devem usar somente valores sintéticos e nunca incluir credenciais reais.

## Ordem do pipeline

```text
collect → classify → redact → validate → sample → persist | buffer | quarantine
```

A quarentena não constitui exceção à política de redaction.

## Contrato de eviction

Quando um evento comum é removido do buffer para abrir espaço para um evento crítico, seu `event_key` e fingerprint devem ser esquecidos. Isso permite novo processamento legítimo se o produtor reenviar o evento após a recuperação do collector. Eventos recusados por `buffer_full` ou `critical_buffer_full` também não devem envenenar o estado de deduplicação.

## Contrato de alertas

- `owner` deve permanecer um identificador operacional estável e não sensível;
- e-mails sintéticos podem ser normalizados para o identificador local quando este satisfaz o contrato de owner;
- owners contendo segredos ou sem formato operacional devem ser rejeitados;
- `runbook` deve continuar acionável após sanitização e corresponder a um caminho Markdown ou URL HTTPS válida;
- `name` e `condition` podem ser sanitizados, desde que não exponham o valor sensível.

## Alternativas rejeitadas

### Redigir somente por nome de chave

Rejeitada por não proteger segredos inseridos em valores de campos autorizados.

### Redigir a string inteira

Rejeitada como padrão porque destrói contexto diagnóstico desnecessariamente. Pode ser usada apenas quando não for possível isolar o trecho sensível com segurança.

### Confiar no produtor da telemetria

Rejeitada porque fontes externas e componentes internos podem produzir dados malformados ou hostis.

### Manter deduplicação de evento evicto

Rejeitada porque transforma uma perda de buffer em falso `duplicate`, impedindo retry legítimo sem evidência de persistência.

### Aceitar owner totalmente redigido

Rejeitada porque um alerta sem responsável acionável viola o objetivo operacional do alerta.

## Critérios de aceite

Os itens desta seção são requisitos de aceitação, não declaração de cobertura. O estado comprovado deve ser registrado na matriz de rastreabilidade e no readiness do mesmo SHA.

- nenhum valor sintético sensível aparece em `persisted`, `buffer`, `quarantine`, `metrics`, `alerts` ou mensagens de erro;
- texto seguro permanece disponível;
- objetos de entrada permanecem inalterados;
- testes adversariais passam de forma determinística;
- eventos críticos continuam preservados após sanitização;
- evento comum evicto pode ser reenviado e processado, em vez de retornar falso `duplicate`;
- owner de alerta permanece operacional ou o alerta é rejeitado;
- CI executa a suíte de observabilidade.

## Testes

```bash
python examples/observability_pipeline.py --self-test
python -m unittest discover -s tests -p "test_*.py" -v
python -m compileall -q examples tests
```

## Risco residual

Expressões regulares não provam detecção universal de segredos. Formatos novos, ofuscação, Unicode confusável e segredos fragmentados podem escapar. A normalização do identificador local de e-mail também pode gerar colisões sem uma camada externa de diretório. O risco deve ser reduzido por allowlist, minimização de telemetria, secret scanning, testes adversariais, diretório operacional de owners e revisão periódica.

## Referências

Ver [Referências ABNT e rastreabilidade](../references/REFERENCIAS_ABNT.md).
