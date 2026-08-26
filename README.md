---
id: nexus.home
title: NEXUS Agent Engineering Academy
lang: pt-BR
status: foundation
aliases:
  - NEXUS Academy
tags:
  - agent-engineering
  - education
  - open-source
---

<p align="center">
  <img src="assets/brand/nexus-hero-animated.svg" width="100%" alt="NEXUS Agent Engineering Academy — sistemas de agentes com contratos, controle e evidência">
</p>

<p align="center">
  <strong>Engenharia de agentes, do primeiro loop ao sistema multiagente em produção.</strong><br>
  Curso · Laboratório · Documentação · Framework · Portfólio
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-6d5dfc.svg"></a>
  <a href="ROADMAP.md"><img alt="Status: Foundation" src="https://img.shields.io/badge/status-foundation-22d3ee.svg"></a>
  <a href="CONTRIBUTING.md"><img alt="Contributions welcome" src="https://img.shields.io/badge/contributions-welcome-10b981.svg"></a>
  <img alt="Docs: pt-BR canonical" src="https://img.shields.io/badge/docs-pt--BR%20canonical-f59e0b.svg">
</p>

<p align="center">
  <img src="assets/architecture/nexus-system-light-3d.png" width="100%" alt="Infográfico claro em estilo 3D que apresenta entradas, plataforma NEXUS, governança, dados, ciclo de melhoria, princípios, fluxo de aprendizagem, impacto e resultados.">
</p>

<p align="center"><em>Mapa visual canônico do ecossistema NEXUS — arquitetura, aprendizagem, governança e impacto.</em></p>

> [!IMPORTANT]
> A NEXUS ensina decisões de engenharia transferíveis entre ferramentas. APIs mudam; invariantes arquiteturais,
> modelos de ameaça, contratos e métodos de avaliação permanecem.

## Por que a NEXUS existe

Agentes não são apenas prompts com ferramentas. São sistemas distribuídos probabilísticos: recebem contexto não
confiável, tomam decisões sob incerteza, causam efeitos externos e precisam ser avaliados, observados e interrompidos.
A NEXUS transforma esse problema em uma trilha prática, rigorosa e independente de fornecedor.

### O método NEXUS

```mermaid
flowchart LR
    C[Conceito] --> A[Arquitetura]
    A --> I[Implementação]
    I --> X[Comparação]
    X --> P[Projeto real]
    P --> E[Avaliação e evidência]
    E --> C
```

Cada módulo parte de um conceito, explicita contratos e riscos, implementa o mesmo padrão em plataformas diferentes,
compara trade-offs e termina em um artefato demonstrável.

## Arquitetura do conhecimento

```mermaid
flowchart TB
    D[docs/\nconceitos e arquitetura] --> C[course/\nsequência pedagógica]
    D --> A[agents/\npadrões de agentes]
    D --> S[skills/\nprocessos auditáveis]
    D --> L[loops/\ncontrole e confiabilidade]
    P[platforms/\nadapters] --> C
    A --> B[labs/\nexperimentos]
    S --> B
    L --> B
    C --> B
    B --> R[projects/\nportfólio real]
    B --> K[benchmarks/\nevidência comparável]
    T[templates/] --> B
    T --> R
    E[examples/] --> B
    Q[tests/ + CI] -. qualidade .-> D
    Q -. qualidade .-> B
    Q -. qualidade .-> K
    Q -. qualidade .-> R
```

Leia a [decisão arquitetural completa](docs/architecture/overview.md), as
[regras editoriais](docs/standards/content-standard.md), o [contrato dos agentes](AGENTS.md), o
[loop mestre de qualidade](loops/master-quality-loop.md) e a
[auditoria Premium Elite](docs/governance/PREMIUM_ELITE_AUDIT.md).

## Hardening V2

A camada de hardening adiciona contratos explícitos para confiabilidade e integridade de ação sem declarar que bugs
upstream são automaticamente vulnerabilidades locais. O ciclo defensivo é **Discover → Verify → Reproduce → Measure
→ Mitigate → Test → Document → Automate**.

Controles em revisão incluem:

- Context Trust Model T0–T7;
- `REQUESTED → APPROVED → EXECUTED → VERIFIED` para ações externas;
- `operation_id`, Execution Receipts e idempotência para side effects;
- timeout, cancelamento e propagação de falha terminal;
- supply-chain de Agent Skills com staging, hash, promoção atômica e rollback;
- Technology Radar e Framework Upgrade Gate;
- benchmark smoke determinístico para VAR, RSR, DSER e CTVR.

Veja o [Threat Model V2](docs/security/THREAT_MODEL_V2.md), o
[Agent Reliability Model](docs/reliability/AGENT_RELIABILITY_MODEL.md), a
[política de supply-chain de Skills](docs/security/SKILL_SUPPLY_CHAIN_SECURITY.md) e o
[Technology Radar](docs/radar/AGENT_TECH_RADAR.md).

## Diferenciais

| Dimensão | Compromisso NEXUS |
|---|---|
| Engenharia | Contratos, estados, falhas, budgets, telemetria e testes antes do framework. |
| Multiplataforma | Um conceito, adapters independentes e uma matriz explícita de equivalência. |
| Segurança | Prompt injection, MCP, least privilege, aprovação humana, rollback e incidentes desde o início. |
| Evidência | Fontes primárias verificáveis, versões/datas e formatos ABNT/Vancouver. |
| Aprendizagem | Objetivos observáveis, laboratórios, rubricas, checklists e projetos de portfólio. |
| Longevidade | Markdown puro, Obsidian, IDs estáveis, links relativos e tradução desacoplada. |

## Currículo

| Fase | Módulos | Resultado |
|---|---|---|
| I — Fundamentos | 00–02 | Modelar agentes e contexto com contratos explícitos. |
| II — Tools, loops, memória e coordenação | 03–06 | Projetar ferramentas seguras, loops controláveis, memória governada e sistemas multiagente. |
| III — Avaliação, segurança e produção | 07–09 | Avaliar, proteger e operar agentes com readiness, rollout e rollback. |
| IV — Observabilidade, automação e capstone | 10–12 | Consolidar telemetria, automação confiável e projeto final. |

Comece pelo [mapa curricular](course/README.md). Cada módulo segue o
[contrato pedagógico](course/module-template.md) e inclui objetivos, pré-requisitos, projeto, checklist, laboratórios,
bibliografia e referências.

## Plataformas

Adapters planejados: ChatGPT, OpenAI Agents SDK, Codex, Claude, Claude Code, Gemini, Gemini CLI, Kimi, OpenClaw,
Hermes, CrewAI, LangGraph, AutoGen, n8n e Make. Inclusão na matriz não significa paridade nem endosso: cada adapter
declara status, recursos, limitações, versão verificada e fonte oficial.

Consulte a [matriz e o contrato de adapter](platforms/README.md).

## Estrutura

```text
.
├── agents/       # padrões, papéis, memória, handoffs e coordenação
├── benchmarks/   # métricas e experimentos comparáveis/machine-readable
├── course/       # sequência pedagógica e módulos
├── docs/         # conceitos, arquitetura, segurança, padrões e referências
├── examples/     # implementações mínimas comparáveis
├── labs/         # experimentos guiados e mensuráveis
├── loops/        # máquinas de estado, budgets e stop conditions
├── platforms/    # adapters e matriz de capacidades
├── projects/     # projetos integradores e capstone
├── skills/       # Agent Skills pequenas, versionáveis e auditáveis
├── templates/    # contratos, ADRs, ameaças e avaliações reutilizáveis
├── tests/        # validação estrutural, segurança e regressão
└── .github/      # CI, templates, ownership e dependências
```

## Tecnologias e formatos

- Markdown + YAML frontmatter, compatíveis com Obsidian.
- Mermaid para diagramas versionáveis.
- Python padrão para validadores e reference controls de baixo bootstrap.
- GitHub Actions, Dependabot, CODEOWNERS e Conventional Commits.
- Agent Skills em diretórios com `SKILL.md` e metadados mínimos compatíveis com o formato adotado.
- Adapters podem usar Python, Go, TypeScript ou automação visual quando o experimento exigir.

## Começar

```bash
git clone https://github.com/matheusflorindo32/nexus-agent-engineering-academy.git
cd nexus-agent-engineering-academy
python tests/validate_repository.py
python tests/run_quality_gates.py
```

Depois, siga o [Módulo 00](course/modules/00-orientation/README.md) e registre decisões relevantes com o
[template de ADR](templates/adr.md).

## Roadmap

Foundation → Hardening V2 → Core Curriculum → Production Engineering → Ecosystem → Stable. Veja marcos, critérios e
entregas no [ROADMAP](ROADMAP.md).

## Contribuir

Contribuições de conteúdo, revisão científica, segurança, adapters, acessibilidade e tradução são bem-vindas.
Antes de começar, leia [CONTRIBUTING.md](CONTRIBUTING.md), o [Código de Conduta](CODE_OF_CONDUCT.md),
[SECURITY.md](SECURITY.md) e [AGENTS.md](AGENTS.md).

## Idiomas

- **Português (`pt-BR`)** — fonte canônica.
- **English (`en`)** — estrutura preparada; tradução rastreada pelo [manifesto](docs/i18n/manifest.yml).
- **Español (`es`)** — estrutura preparada; tradução rastreada pelo [manifesto](docs/i18n/manifest.yml).

IDs nunca são traduzidos. Veja a [política de internacionalização](docs/i18n/README.md).

## Licença

Código e documentação são licenciados sob [Apache License 2.0](LICENSE). Marcas e identidade visual não recebem
automaticamente direitos de uso além do necessário para atribuição e referência ao projeto.

---

<p align="center"><strong>NEXUS</strong> — aprenda a construir agentes que você consegue explicar, avaliar e parar.</p>
