---
id: audit.provider-adapters-v3-review-scorecard
title: Provider Adapters V3 — revisão independente e scorecard
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Adapters V3 — revisão independente e scorecard

## Escopo

Revisão adversarial do milestone `Provider Adapters V3 — contract parity`, limitada ao **Contract Trial**. Nenhum SDK/provider/model real foi executado e nenhuma conclusão comparativa entre OpenAI Agents SDK, Google ADK e MCP é permitida neste estágio.

## Perspectivas de revisão

A revisão consolidou perguntas equivalentes às de especialistas em:

- Agent Engineering e sistemas distribuídos;
- OpenAI Agents SDK, Google ADK e MCP;
- segurança de agentes, prompt injection e tool abuse;
- SRE, fault tolerance e observabilidade;
- Python e engenharia de testes;
- DevSecOps e software supply chain;
- desenho experimental, reprodutibilidade e open science.

Os revisores foram instruídos a procurar evidência negativa, claims excessivos, falsa paridade e testes que apenas simulassem sucesso.

## Achados encontrados e corrigidos

### F1 — import do teste de adapters quebrava o CI

**Severidade:** média para o milestone.

O primeiro CI do PR falhou no teste `test_provider_adapter_contracts`. A implementação de import dinâmico não registrava o módulo da forma esperada pelo `dataclass`. O problema foi corrigido usando import normal do módulo após adicionar `examples/` ao `sys.path` do teste.

**Estado:** `MITIGATED`.

**Evidência:** CI posterior executou unit tests e quality gates com sucesso.

### F2 — Recovery Success Rate era assumida, não medida

**Severidade:** alta metodológica / média operacional no Contract Trial.

A primeira versão de `_recovery_scenario()` retornava `1.0` por construção. Isso poderia criar uma falsa aparência de evidência para RSR.

A revisão rejeitou esse desenho. O cenário agora cria `BoundedChannel`, injeta falha terminal sintética e exige `TransportClosed`; timeout ou ausência de erro observável produz falha da métrica.

**Estado:** `MITIGATED`.

**Lição:** uma métrica não pode ser preenchida por expectativa arquitetural; precisa resultar de comportamento executado.

## Achados externos e classificação

| Achado upstream | Classificação NEXUS | Claim permitido |
|---|---|---|
| OpenAI 0.22.0 runtime hardening | `MONITORING` | requisito/insumo para futuro runtime trial |
| OpenAI timeout e cleanup de falha | `POTENTIALLY_APPLICABLE` | testar quando SDK real estiver pinado |
| Google ADK #6721 A2A/HITL resume | `POTENTIALLY_APPLICABLE` | criar regressão; não chamar de vulnerabilidade NEXUS |
| Google ADK 2.7.1 session initialization validation | `MONITORING` | observar state/session semantics |
| MCP 2026-07-28 stateless core | `MONITORING` | requisito de compatibilidade/version negotiation |
| MCP external content T6 → T1 | `MITIGATED` somente no reference layer | non-escalation determinística; runtime real ainda não testado |

## Riscos residuais

1. **Adapters ainda declarativos:** `AdapterSpec` registra capacidades com base em fontes oficiais, mas não prova comportamento do SDK em execução.
2. **Sem provider-level adversarial testing:** prompt injection/tool poisoning ainda não foram executados contra OpenAI/ADK/MCP reais.
3. **ADK A2A/HITL não reproduzido:** o issue upstream segue `POTENTIALLY_APPLICABLE`.
4. **MCP runtime pendente:** version negotiation, MRTR, auth e malicious metadata ainda não foram testados com servidor/cliente real.
5. **Observabilidade real pendente:** não há exporter OpenTelemetry/provider traces neste milestone.
6. **Supply chain de runtime pendente:** não há lock/SBOM dos SDKs porque as dependências de provider ainda não foram instaladas.
7. **Advisory coverage incompleta:** a interface utilizada não expôs catálogo completo de GitHub Security Advisories; ausência de advisory citado não prova ausência de advisory.
8. **Paridade não é equivalência:** os três adapters usam o mesmo control-plane NEXUS; scores iguais não dizem que frameworks têm a mesma confiabilidade ou segurança.

## Scorecard baseado em evidência

| Dimensão | Nota /10 | Evidência / limitação |
|---|---:|---|
| Arquitetura | 9.2 | separa Contract Trial de Runtime Trial por ADR |
| Segurança | 9.1 | trust boundaries e no-escalation formalizados; runtime externo pendente |
| Agent Security | 9.0 | action integrity e T0–T7 testados no reference layer |
| Reliability | 9.2 | recovery agora é comportamento executado, não constante |
| Testing | 9.3 | testes negativos e anti-claim incluídos; providers reais faltam |
| CI/CD | 9.5 | validator, unit tests, benchmark contract, TypeScript e secret scan |
| Observabilidade | 8.2 | boa base existente; provider/OpenTelemetry runtime ainda ausente |
| Supply Chain | 8.6 | upgrade gate/Skill controls fortes; lock/SBOM de providers pendentes |
| Reprodutibilidade | 9.4 | deterministic stdlib Contract Trial ligado a SHA/version baseline |
| Scientific Readiness | 8.6 | desenho mais defensável; comparação pública ainda bloqueada |
| Provider Comparison Readiness | 6.5 | contrato comum pronto, runtimes/model experiments não executados |
| Maintainability | 9.1 | adapters pequenos, sem dependências novas neste estágio |

## Maturity Level

**L3 — Reproducible**, restrito ao **reference/contract layer**.

Não há evidência suficiente para `L4 — Secure-by-Design` em runtime de providers e não existe claim de `production-grade`.

## Decisão independente

**Aprovar o Contract Trial para revisão humana**, condicionado a CI verde no SHA final.

**Não aprovar ainda o Provider Runtime Trial** até existir:

- protocolo versionado/preregistrável;
- dependências pinadas e supply-chain review;
- ambientes reproduzíveis;
- testes reais equivalentes por provider;
- tracing/redaction verificável;
- chaos/adversarial suite;
- métricas executadas e vinculadas a SHA/versões.

## Regra de parada

Não adicionar LangGraph, CrewAI ou outros frameworks neste milestone. O ganho marginal agora está em transformar os três adapters prioritários de `contract only` para runtime mensurável, não em aumentar o número de integrações.
