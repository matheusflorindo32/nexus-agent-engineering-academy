---
id: audit.nexus-repository-indexer-v1-results
content_id: audit.nexus-repository-indexer-v1-results
version: 1.0.1
title: NEXUS Repository Indexer V1 — Results
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Repository Indexer V1 — Results

## Frozen inputs

- `protocol.json` SHA-256: `ad9384481fbc89f21457dbc500cf90d39840896f1fac3f60fa970939501a3ff3`
- `fixtures.json` SHA-256: `eeb51a4ffa9918ba2147e984871f5dc676d34958dc09552fc886e10aefefd1d7`
- repetitions: 5
- runtime dependencies added: 0

## Fixture evidence

Class: `DETERMINISTIC_CONTROL_EVIDENCE`.

Após revisão adversarial, todos os oito fixtures passaram a declarar explicitamente o oracle completo de files, symbols, dependencies, parse errors e limite mínimo de texto não confiável. O fallback que poderia usar o próprio observado como expectativa deixou de influenciar o corpus congelado.

O capture com oracle completo produziu 100/100 dentro do corpus: precision, recall, F1, fixture pass rate e deterministic rerun equality = 1.0, com zero false positives e zero false negatives. Esse resultado é restrito ao corpus sintético congelado e não constitui claim de produção ou multi-language.

## Real repository evidence

Class: `REAL_RUNTIME_EVIDENCE` para observações feitas pelo workflow ao indexar este repositório em modo read-only. O artifact do head final é a fonte autoritativa para contagens de files/symbols, fingerprint, elapsed time, memória e incremental reuse porque esses valores dependem do conteúdo exato do PR.

O real-repository correctness score é deliberadamente `NOT_APPLICABLE`: não existe oracle completo independente para todos os symbols/dependencies do próprio repositório. TypeScript, JavaScript e rename inference permanecem `NOT_TESTED`.

## Security evidence

O workflow exige zero repository writes. O indexador registra zero network calls e zero repository instructions executadas. Strings semelhantes a prompt injection são contadas somente como texto não confiável.

## Score boundary

`100/100` pode ser reportado apenas para o benchmark de fixtures quando o check final do manifest `FROZEN` passar. Não pode ser apresentado como qualidade geral do NEXUS, segurança de produção, correctness do repositório real ou superioridade sobre SpecD.
