---
id: platform.openai-agents-sdk
title: Adapter OpenAI Agents SDK
lang: pt-BR
status: foundation
verified: 2026-07-19
---

# OpenAI Agents SDK

Fonte primária: [documentação oficial Python](https://openai.github.io/openai-agents-python/), verificada em 2026-07-19.

| Conceito NEXUS | Suporte | Observação |
|---|---|---|
| Agent + instructions | suportado | instruções não substituem policy gates |
| Tools | suportado | validar schema, identidade e efeitos |
| Handoffs | suportado | medir custo e qualidade do roteamento |
| Guardrails | suportado | usar como camada, não autoridade única |
| Tracing | suportado | aplicar redaction e política de retenção |

O adapter executável será introduzido no marco v0.2 com versão fixada e testes de equivalência. Até lá, este documento
delimita o mapeamento sem publicar código possivelmente desatualizado.

