---
id: governance.changelog
title: Changelog
lang: pt-BR
status: stable
---

# Changelog

Todas as mudanças relevantes serão registradas aqui. O formato segue
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) e o versionamento seguirá
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) quando houver artefatos versionados.

## [Unreleased]

### Added

- Fundação editorial, curricular, arquitetural, multilíngue e de segurança.
- Automação de qualidade e governança do GitHub.
- ADRs para taxonomia curricular e redaction defensiva.
- Referências em formato ABNT com status de verificação e limitações explícitas.
- Matriz de rastreabilidade, revisão por pares, guia de migração e parecer de readiness.
- Cenário O15 para provar sanitização da quarentena sem mutação do evento de entrada.
- Mapeamento individual da migração curricular e procedimento seguro para integrar a pilha de PRs.
- Catálogo completo dos 12 laboratórios implementados e marcação explícita do LAB-1201 como planejado.
- Hardening V2 com Context Trust Model T0–T7, Execution Receipts, idempotência e reliability model.
- Auditoria de aplicabilidade para achados upstream sem promovê-los automaticamente a vulnerabilidades locais.
- Referência de lifecycle seguro de Agent Skills com staging, hash, promoção atômica e rollback.
- Primeira Agent Skill formal: `skill-supply-chain-auditor`.
- Testes de timeout, cancelamento, resume, integridade HITL, efeitos duplicados, Skill integrity e conteúdo MCP não confiável.
- Benchmark smoke determinístico para VAR, RSR, DSER e CTVR.
- Technology Radar e Framework Upgrade Gate para adoção controlada de SDKs/frameworks agentic.
- Provider Adapters V3 com baseline oficial verificado para OpenAI Agents SDK 0.22.0, Google ADK Python 2.7.1 e MCP 2026-07-28.
- Contract Trial comum para os três adapters prioritários, com VAR, RSR, DSER e CTVR e escopo de claim explícito.
- Threat Model V3 para fronteiras de providers/protocolo e ADR de paridade de contrato antes de Runtime Trial.
- Research Readiness V3 e revisão independente/scorecard específicos para comparação futura de providers.

### Changed

- Trilha curricular normalizada para Modules 00–12.
- Laboratórios normalizados, com LAB-1001 para observabilidade e LAB-1101 para automação idempotente.
- Pipeline de observabilidade passa a sanitizar antes de persistir, bufferizar ou quarentenar.
- Readiness, registro de controles, auditoria e referências passam a distinguir evidência histórica do estado da branch final.
- Pré-requisito do Módulo 09 corrigido para o ID canônico do Módulo 08.
- Quality gates passam a executar o reference runtime, benchmark smoke do Hardening V2 e Contract Trial dos adapters V3.
- Technology Radar distingue `TRIAL — contract only` de execução de runtime real.

### Security

- Redaction ampliada para chaves sensíveis e credenciais embutidas em valores permitidos.
- Quarentena deixa de armazenar o objeto de evento bruto.
- Skills externas passam a ser tratadas como supply-chain não confiável até auditoria e aprovação.
- Aprovação, execução e verificação de ações são modeladas como estados independentes.
- Conteúdo externo/MCP não pode elevar seu próprio nível de confiança por instrução textual.
- Findings upstream de OpenAI/Google/MCP passam por classificação explícita antes de qualquer claim local.

### Fixed

- Colisões históricas de módulos e laboratórios.
- Falso negativo do validador diante de prefixos duplicados.
- Possível exposição de segredo em atributo permitido ou evento incompatível.
- Reference runtime passa a persistir o `retry_count` de tentativas idempotentes sem repetir o side effect.
- Teste dos Provider Adapters V3 deixa de usar import dinâmico incompatível com `dataclass`.
- Recovery Success Rate do Contract Trial deixa de ser assumida e passa a exigir uma falha terminal sintética observável e bounded.
