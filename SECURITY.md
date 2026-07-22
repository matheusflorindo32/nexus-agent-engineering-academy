---
id: governance.security-policy
title: Política de segurança
lang: pt-BR
status: review
version: 0.2.0
---

# Política de segurança

## Escopo

Esta política cobre código, exemplos, validadores, workflows, documentação executável e configurações mantidas neste repositório.

Conteúdo educacional incorreto, link quebrado ou dúvida pedagógica normalmente deve ser relatado por issue comum. Trate como segurança quando houver possibilidade de:

- exposição de segredo ou dado pessoal;
- execução não autorizada;
- ampliação de privilégio;
- vazamento entre tenants ou projetos;
- efeito externo duplicado ou irreversível;
- bypass de approval, policy gate, hard gate ou kill switch;
- ataque à cadeia de suprimentos;
- instrução maliciosa persistida ou executada;
- manipulação de evidência ou auditoria.

## Versões suportadas

Enquanto o projeto permanecer em `review`, recebem atenção prioritária:

- a branch padrão integrada e validada;
- o release público mais recente, quando existir;
- branches de PR ativas apenas para vulnerabilidades introduzidas por suas próprias mudanças.

A existência de CI verde ou documentação de controle não constitui garantia de segurança.

## Relato responsável

Não abra issue, discussion ou PR público contendo detalhes exploráveis de vulnerabilidade.

Use o recurso **Private vulnerability reporting** do GitHub no repositório oficial. Caso o recurso não esteja habilitado, contate um maintainer por canal privado publicado no perfil oficial, sem enviar segredo real.

Inclua, quando possível:

- componente e commit afetado;
- impacto e cenário de ameaça;
- pré-condições;
- reprodução mínima em ambiente isolado;
- resultado esperado e observado;
- evidência sanitizada;
- mitigação sugerida;
- informação sobre divulgação prévia.

Não execute testes contra contas, tenants, usuários, serviços ou infraestrutura que não sejam seus e explicitamente autorizados.

## Dados proibidos no relato

Não envie:

- tokens, chaves, senhas ou cookies reais;
- dados pessoais reais;
- dumps completos;
- prompts ou logs privados;
- credenciais de terceiros;
- material cuja posse ou redistribuição não seja autorizada.

Use valores sintéticos e remova metadados desnecessários.

## Resposta e coordenação

Meta de resposta inicial: até 72 horas. Essa meta não é SLA contratual.

O processo pode incluir:

1. confirmação de recebimento;
2. triagem e severidade preliminar;
3. pedido de evidência sanitizada;
4. reprodução controlada;
5. mitigação temporária;
6. correção e testes de regressão;
7. divulgação coordenada;
8. postmortem quando proporcional ao impacto.

Prazos de correção dependem de severidade, complexidade, disponibilidade de mantenedores e risco de divulgação. Não há programa de recompensa financeira nesta fase.

## Baseline obrigatório

- Segredos somente em secret managers ou variáveis locais ignoradas pelo Git.
- Dados sintéticos em exemplos, laboratórios e CI.
- Ferramentas e servidores MCP com menor escopo possível, allowlists e autenticação explícita.
- Identidade, tenant, políticas e budgets fora do controle livre do modelo.
- Aprovação humana vinculada a ação, argumentos, escopo, hash, expiração e contexto de risco.
- Logs e traces redigidos antes de persistência, buffer, exportação ou quarentena.
- Limites de custo, tempo, passos, tentativas e efeitos externos.
- Circuit breaker, stop conditions, kill switch e caminho manual.
- Ledger, idempotência e reconciliação antes de retry após efeito desconhecido.
- Rollback e restore ensaiados no escopo proporcional ao risco.
- Hard gates críticos não compensados por médias.

## Severidade orientativa

| Nível | Exemplos |
|---|---|
| Crítica | segredo real exposto, execução remota, vazamento amplo entre tenants, bypass de efeito sensível |
| Alta | ampliação de autoridade, approval reutilizável, efeito duplicado, cadeia de suprimentos comprometida |
| Média | redaction incompleta com dados sintéticos, denial of service limitado, isolamento parcial em demo |
| Baixa | informação excessiva sem dado sensível, hardening, documentação de controle ambígua |

A classificação final depende de impacto, explorabilidade, escopo e precondições.

## Safe harbor limitado

Pesquisas de boa-fé devem:

- respeitar leis e autorizações aplicáveis;
- permanecer em ambiente próprio ou explicitamente autorizado;
- minimizar acesso e coleta;
- parar ao encontrar dado real, segredo ou efeito não previsto;
- não interromper serviços;
- não extorquir, ameaçar ou divulgar prematuramente;
- permitir tempo razoável para correção.

Esta seção expressa intenção de colaboração, não concede autorização sobre sistemas de terceiros nem substitui aconselhamento jurídico.

## Divulgação

A divulgação pública deve ocorrer apenas após coordenação suficiente para reduzir risco, salvo obrigação legal. Créditos ao pesquisador serão considerados mediante consentimento e desde que não prejudiquem usuários ou investigação.

## Referências internas

- [Segurança de sistemas agentes](docs/security/index.md)
- [Gate de Guardrails & Security](course/modules/GUARDRAILS_SECURITY_ENGINEERING_ELITE_GATE.md)
- [LAB-801 — Agent Security Red Team](labs/LAB-801-agent-security-red-team.md)
- [Licenciamento e uso de ativos](LICENSING.md)

## Limitações

Esta política organiza o processo de segurança do projeto. Ela não garante ausência de vulnerabilidades, resposta em prazo fixo, compatibilidade com todas as plataformas ou proteção de sistemas externos não controlados pela NEXUS.