---
id: governance.roadmap
title: Roadmap
lang: pt-BR
status: active
---

# Roadmap

## Princípios de priorização

Impacto educacional, evidência, segurança e manutenção vêm antes da quantidade de integrações.

### Foundation — v0.1

- [x] Arquitetura modular e taxonomia com IDs estáveis.
- [x] Currículo progressivo e contrato de módulo.
- [x] Baseline de segurança, governança e CI.
- [x] Estrutura de adapters de plataforma e tradução.

### Hardening V2 — reliability, action integrity e Skill supply chain

- [x] Auditar o estado real e separar implementação de documentação aspiracional.
- [x] Formalizar Context Trust Model T0–T7.
- [x] Criar reference runtime para bounded transport failure, action receipts e idempotência.
- [x] Criar referência de staging/hash/promoção atômica de Skills.
- [x] Adicionar primeira Skill compatível com o formato Agent Skills (`skill-supply-chain-auditor`).
- [x] Adicionar testes unitários de hardening e benchmark smoke determinístico.
- [x] Criar technology radar e framework upgrade policy.
- [x] Obter CI verde no SHA final do PR #53.
- [x] Executar auditoria independente no reference layer.
- [x] Abrir PR #53 sem auto-merge.

### Provider Adapters V3 — contract parity

- [x] Verificar fontes oficiais atuais de OpenAI Agents SDK, Google ADK e MCP.
- [x] Registrar versões verificadas: OpenAI Agents SDK 0.22.0, Google ADK Python 2.7.1, MCP 2026-07-28.
- [x] Classificar achados upstream antes de qualquer claim local.
- [x] Criar adapters experimentais de contrato com o mesmo oracle NEXUS.
- [x] Adicionar testes de paridade VAR/RSR/DSER/CTVR sem chamadas de provider.
- [x] Atualizar Technology Radar, Threat Model e Research Readiness.
- [x] Obter CI verde após correções do Contract Trial; o SHA final deste milestone ainda deve ser revalidado após mudanças documentais finais.
- [x] Executar revisão independente V3 e corrigir achados metodológicos encontrados.
- [x] Abrir PR #54 como stacked PR, sem auto-merge.

### Provider Runtime Trial V1 — offline controlled runtimes

- [x] Criar protocolo versionado antes da execução do Runtime Trial.
- [x] Isolar jobs e fixar versões top-level por adapter; registrar pip freeze.
- [x] Executar OpenAI Agents SDK 0.22.0 real com ScriptedModel oficial, tool pipeline e falha determinística.
- [x] Executar Google ADK 2.8.0 real com Runner/session e BaseLlm offline.
- [x] Executar MCP Python SDK 2.1.1 real in-process com negotiation 2026-07-28.
- [x] Registrar task success, bounded failure/RSR e métricas aplicáveis sem inventar valores ausentes.
- [x] Registrar Microsoft Agent Framework como MONITORING até Contract Trial paritário.
- [ ] Adicionar lock/constraints transitivos com hashes/provenance.
- [ ] Executar ADK A2A/HITL pause-resume, parallel side effects e state integrity.
- [ ] Executar MCP remoto com HTTP/auth/MRTR/cancellation e casos adversariais.
- [ ] Executar tracing/OpenTelemetry/redaction por runtime.
- [ ] Criar Provider/Model Trial somente com autorização explícita, orçamento e protocolo estatístico.

### Core Curriculum — v0.2

- [ ] Publicar conteúdo completo dos módulos 00–04.
- [ ] Criar rubricas e soluções verificáveis para laboratórios básicos.
- [ ] Implementar exemplos equivalentes em OpenAI Agents SDK, LangGraph e n8n.

### Production Engineering — v0.3

- [ ] Completar observabilidade, avaliação, segurança e confiabilidade.
- [ ] Adicionar ambientes reproduzíveis e suíte de ataques controlados.
- [ ] Publicar projetos capstone com rubricas de arquitetura.
- [ ] Evoluir Execution Receipts do exemplo in-memory para adapters com evidência externa verificável.
- [ ] Criar chaos/failure lab para transport, MCP, storage, state e approval workflows.

### Ecosystem — v0.4

- [ ] Expandir adapters conforme [matriz de plataformas](platforms/README.md).
- [ ] Entregar traduções inglês e espanhol com paridade mensurável.
- [ ] Publicar trilhas para livros, vídeo e formação corporativa.

### Stable — v1.0

- [ ] Validar o currículo com turmas reais e revisão externa.
- [ ] Garantir compatibilidade, acessibilidade e política de releases.
- [ ] Formar equipe sustentável de maintainers.
