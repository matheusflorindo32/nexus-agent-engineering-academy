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

### Changed

- Trilha curricular normalizada para Modules 00–12.
- Laboratórios normalizados, com LAB-1001 para observabilidade e LAB-1101 para automação idempotente.
- Pipeline de observabilidade passa a sanitizar antes de persistir, bufferizar ou quarentenar.
- Readiness, registro de controles, auditoria e referências passam a distinguir evidência histórica do estado da branch final.
- Pré-requisito do Módulo 09 corrigido para o ID canônico do Módulo 08.

### Security

- Redaction ampliada para chaves sensíveis e credenciais embutidas em valores permitidos.
- Quarentena deixa de armazenar o objeto de evento bruto.

### Fixed

- Colisões históricas de módulos e laboratórios.
- Falso negativo do validador diante de prefixos duplicados.
- Possível exposição de segredo em atributo permitido ou evento incompatível.
