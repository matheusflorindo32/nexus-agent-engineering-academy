---
id: platforms.index
title: Matriz de plataformas
lang: pt-BR
status: foundation
---

# Plataformas e adapters

Esta matriz é um backlog verificável, não uma alegação de equivalência. `planned` significa apenas que a estrutura
aceita um adapter futuro. Capacidades mudam; confirme a documentação oficial e registre a data antes de ensinar.

| Plataforma | Tipo | Adapter | Status inicial |
|---|---|---|---|
| ChatGPT | produto | `chatgpt/` | planned |
| OpenAI Agents SDK | SDK | `openai-agents-sdk/` | foundation |
| Codex | agente de software | `codex/` | planned |
| Claude / Claude Code | produto/agente | `anthropic/` | planned |
| Gemini / Gemini CLI | produto/agente | `google/` | planned |
| Kimi | produto/modelo | `kimi/` | research-required |
| OpenClaw | projeto | `openclaw/` | research-required |
| Hermes | projeto | `hermes/` | research-required |
| CrewAI | framework | `crewai/` | planned |
| LangGraph | framework | `langgraph/` | foundation |
| AutoGen | framework | `autogen/` | planned |
| n8n | automação | `n8n/` | planned |
| Make | automação | `make/` | planned |

`research-required` evita atribuir identidade ou capacidade a nomes ambíguos sem fonte oficial confirmada.

## Contrato de adapter

Cada diretório deve conter um `README.md` com:

- fonte oficial, data e versão verificada;
- capacidades mapeadas para conceitos NEXUS;
- instalação/reprodução e requisitos;
- segurança, telemetria e limitações;
- exemplo mínimo original e teste;
- tabela “suportado / parcial / ausente / desconhecido”.

Use [adapter-template.md](adapter-template.md). Nunca condicione o currículo core à disponibilidade de um fornecedor.

