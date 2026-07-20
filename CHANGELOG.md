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

### Changed

- Trilha curricular normalizada para Modules 00–12.
- Laboratórios normalizados, com LAB-1001 para observabilidade e LAB-1101 para automação idempotente.
- Pipeline de observabilidade passa a sanitizar antes de persistir, bufferizar ou quarentenar.

### Security

- Redaction ampliada para chaves sensíveis e credenciais embutidas em valores permitidos.
- Quarentena deixa de armazenar o objeto de evento bruto.

### Fixed

- Colisões históricas de módulos e laboratórios.
- Falso negativo do validador diante de prefixos duplicados.
- Possível exposição de segredo em atributo permitido ou evento incompatível.
