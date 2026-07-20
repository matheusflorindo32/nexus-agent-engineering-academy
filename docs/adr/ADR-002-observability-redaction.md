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

## Decisão

Aplicar redaction antes de qualquer persistência, bufferização, quarentena ou emissão operacional. A sanitização deve:

1. identificar chaves sensíveis;
2. identificar credenciais dentro de valores textuais permitidos;
3. percorrer estruturas aninhadas;
4. preservar conteúdo não sensível e o tipo de coleção quando possível;
5. não modificar o objeto de entrada;
6. produzir resultado determinístico;
7. falhar de forma segura diante de formatos desconhecidos.

## Padrões mínimos cobertos

- pares `token`, `secret`, `password`, `api_key`, `apikey`, `access_token`, `refresh_token` e `client_secret`;
- esquemas `Bearer` e `Basic`;
- prefixos conhecidos de credenciais usados em testes sintéticos;
- estruturas `dict`, `list` e `tuple`;
- conteúdo aninhado em atributos permitidos.

Os testes devem usar somente valores sintéticos e nunca incluir credenciais reais.

## Ordem do pipeline

```text
collect → classify → redact → validate → sample → persist | buffer | quarantine
```

A quarentena não constitui exceção à política de redaction.

## Alternativas rejeitadas

### Redigir somente por nome de chave

Rejeitada por não proteger segredos inseridos em valores de campos autorizados.

### Redigir a string inteira

Rejeitada como padrão porque destrói contexto diagnóstico desnecessariamente. Pode ser usada apenas quando não for possível isolar o trecho sensível com segurança.

### Confiar no produtor da telemetria

Rejeitada porque fontes externas e componentes internos podem produzir dados malformados ou hostis.

## Critérios de aceite

- nenhum valor sintético sensível aparece em `persisted`, `buffer`, `quarantine`, `metrics`, `alerts` ou mensagens de erro;
- texto seguro permanece disponível;
- objetos de entrada permanecem inalterados;
- testes adversariais passam de forma determinística;
- eventos críticos continuam preservados após sanitização;
- CI executa a suíte de observabilidade.

## Testes

```bash
python examples/observability_pipeline.py --self-test
python -m compileall -q examples tests
```

## Risco residual

Expressões regulares não provam detecção universal de segredos. Formatos novos, ofuscação, Unicode confusável e segredos fragmentados podem escapar. O risco deve ser reduzido por allowlist, minimização de telemetria, secret scanning, testes adversariais e revisão periódica.

## Referências

Ver [Referências ABNT e rastreabilidade](../references/REFERENCIAS_ABNT.md).
