---
id: audit.provider-runtime-trial-v1-review
title: Provider Runtime Trial V1 — revisão adversarial e scorecard
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Runtime Trial V1 — revisão adversarial e scorecard

## Método

Revisão independente por perspectivas de Agent Engineering, distributed systems, OpenAI Agents SDK, Google ADK, MCP, AI security/red team, SRE, observability, Python, TypeScript/Go boundary awareness, DevSecOps, supply chain e metodologia/reprodutibilidade.

Os revisores foram instruídos a procurar razões para **rejeitar claims**, não para maximizar nota.

## Achados reais durante a rodada

### F1 — frontmatter inválido do protocolo
**Severidade:** baixa/quality gate.

O protocolo foi criado com um valor de `status` não aceito pelo validador do repositório. A primeira CI bloqueou a mudança.

**Correção:** usar estado suportado `review`. Nenhum conteúdo de hipótese/tarefa/métrica foi modificado.

### F2 — teste estático acoplado a frase literal
**Severidade:** baixa/test robustness.

Um teste buscava uma frase que não correspondia literalmente ao protocolo, embora a regra semântica estivesse presente.

**Correção:** alinhar o assertion ao texto canônico do protocolo. O teste continua impedindo promoção indevida de offline trial para provider claim.

### F3 — SHA de PR merge versus branch head na evidência
**Severidade:** média/reprodutibilidade.

GitHub Actions em `pull_request` usa `GITHUB_SHA` do merge ref. Isso é um SHA válido do workflow, mas não é o head commit da branch.

**Correção:** evidence schema passa a registrar separadamente `commit_sha` usando o head do PR e `workflow_sha` usando o merge ref.

### F4 — top-level pin não é lockfile transitivo
**Severidade:** média/supply chain.

`package==version` fixa o SDK principal, mas o resolver ainda pode selecionar dependências transitivas diferentes no futuro.

**Tratamento V1:** `pip freeze` preservado como artifact por execução.  
**Risco residual:** hash-lock/constraints completos e attestations ainda faltam.

### F5 — CTVR não mede prompt-injection resistance do framework
**Severidade:** média/metodologia.

CTVR=0 no V1 vem do policy gate NEXUS T6→T1. Isso não testa se um modelo real obedeceria a conteúdo hostil.

**Tratamento:** claim explicitamente limitado ao host. Provider/model adversarial trial permanece futuro.

### F6 — assimetria VAR/DSER
**Severidade:** média/comparabilidade.

OpenAI tem tool-pipeline side-effect sintético no V1; ADK e MCP não possuem cenário equivalente ainda.

**Tratamento:** métricas ausentes são NOT_EXECUTED, não imputadas como zero/falha. Nenhum ranking é permitido.

### F7 — Google A2A/HITL e MCP network/auth ainda fora do boundary
**Severidade:** média/risk coverage.

As fronteiras de maior interesse de segurança não foram exercitadas neste smoke V1.

**Tratamento:** permanecem POTENTIALLY_APPLICABLE/MONITORING e são P0 do próximo laboratório adversarial.

### F8 — runtime source fora do compileall central
**Severidade:** média/test coverage.

Uma alteração no helper de evidence introduziu sintaxe inválida. O workflow específico de runtime detectou a falha, mas o NEXUS Quality permaneceu verde porque o gate `compileall` não incluía `runtime_trials/`.

**Correção:** incluir `runtime_trials` no compileall central. Isso converteu a falha encontrada em regressão bloqueável por dois caminhos independentes.

## Divergências dos revisores

- **SRE:** aceita o V1 como runtime smoke porque há timeouts, failure injection e artifacts; não aceita chamar de chaos engineering completo.
- **AI Security:** considera CTVR útil como host invariant, mas rejeita qualquer interpretação como prompt-injection benchmark do SDK/modelo.
- **Distributed Systems:** aceita MCP in-process para version negotiation básica, mas rejeita inferências sobre HTTP/OAuth/retry/network partitions.
- **Methodology:** considera a separação `NOT_EXECUTED` correta e prefere dados ausentes a equivalência forçada.
- **Supply Chain:** considera top-level pin insuficiente para L4; exige lock transitivo/hash/attestation antes de produção.

## Scorecard V1

| Dimensão | Nota | Evidência/limite |
|---|---:|---|
| Architecture | 9.3 | boundaries explícitos e stacked PR |
| Agent Engineering | 9.2 | três runtimes reais; provider real ainda fora |
| Reliability | 9.1 | bounded failure executado; network chaos pendente |
| Security | 8.9 | host trust model forte; adversarial provider/MCP remoto pendente |
| Supply Chain | 8.1 | pins + freeze; falta hash lock/attestation |
| Testing | 9.3 | CI isolada + falhas reais de harness corrigidas |
| Observability | 8.8 | JSON/SHA/env; OTel runtime profundo ainda parcial |
| Reproducibility | 9.1 | protocolo prévio, versões, freeze, artifacts |
| Methodological Integrity | 9.5 | claim boundary e NOT_EXECUTED preservados |
| Provider Comparison Readiness | 7.2 | runtime foundation pronta; modelos/providers reais não comparados |
| Scientific Readiness | 8.9 | protocolo executável; plano estatístico para provider real ainda falta |
| Maintainability | 9.0 | adapters pequenos e jobs isolados |

## Maturity

**L3 — Reproducible**, agora incluindo **SDK Runtime Trial offline**.

Não promover para L4 enquanto faltarem:
- dependency locks com hashes/provenance;
- remote MCP security lab;
- ADK A2A/HITL integrity lab;
- real identity binding;
- durable receipts;
- provider/model adversarial testing;
- OTel/redaction runtime verification mais completa.

## Decisão

**APROVAR o Provider Runtime Trial V1 offline para revisão humana.**

**NÃO APROVAR claims de superioridade de provider/model ou production-grade.**
