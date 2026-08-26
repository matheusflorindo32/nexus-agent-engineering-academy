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
- [ ] Obter CI verde no SHA final da branch `feat/agent-hardening-v2`.
- [ ] Executar auditoria independente e fechar achados críticos/altos.
- [ ] Abrir PR sem auto-merge.

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
