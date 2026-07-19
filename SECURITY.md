---
id: governance.security-policy
title: Política de segurança
lang: pt-BR
status: stable
---

# Política de segurança

## Versões suportadas

Durante a fase Foundation, apenas a branch padrão e o release mais recente recebem correções de segurança.

## Relato responsável

Não abra uma issue pública para vulnerabilidades. Use o recurso **Private vulnerability reporting** do GitHub no
repositório oficial. Se ainda não estiver habilitado, contate um maintainer por um canal privado publicado no perfil
da organização. Inclua impacto, pré-condições, reprodução mínima e mitigação sugerida. Não inclua segredos reais.

Meta de resposta inicial: 72 horas. A confirmação, correção e divulgação coordenada dependem de severidade e
complexidade. Não oferecemos recompensa financeira nesta fase.

## Baseline obrigatório

- Segredos somente em secret managers ou variáveis locais ignoradas pelo Git.
- Ferramentas e servidores MCP com menor escopo possível, allowlists e autenticação explícita.
- Aprovação humana para ações destrutivas, financeiras, externas ou irreversíveis.
- Logs com correlação, sem prompts sensíveis ou credenciais.
- Limites de custo, tempo, passos e tentativas; circuit breaker e stop conditions.
- Rollback ensaiado e resposta a incidentes documentada.

O modelo de ameaças e os controles estão em [Segurança de sistemas agentes](docs/security/index.md).

