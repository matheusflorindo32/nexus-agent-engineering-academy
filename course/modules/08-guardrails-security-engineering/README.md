---
id: course.module.08-guardrails-security-engineering
title: 08 — Guardrails & Security Engineering
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 14h
prerequisites: [course.module.07-evaluation-engineering]
learning_outcomes:
  - modelar ameaças para sistemas agentic
  - aplicar least privilege e aprovação humana
  - mitigar prompt injection e exfiltração
  - proteger segredos, memória, ferramentas e handoffs
  - executar red teaming reproduzível com critérios de release
---

# 08 — Guardrails & Security Engineering

> [!IMPORTANT]
> Segurança em agentes não é um filtro adicionado ao final. É uma propriedade arquitetural composta por fronteiras, autoridade mínima, validação, isolamento, observabilidade e capacidade de interrupção.

## Objetivos

- Construir threat models específicos para agentes, ferramentas, memória, MCP e multiagentes.
- Separar conteúdo não confiável de instruções autorizadas.
- Aplicar least privilege, deny-by-default e aprovação humana vinculada ao artefato exato.
- Evitar exfiltração, confusão de autoridade, tool abuse, persistência maliciosa e cross-tenant leakage.
- Criar testes de segurança locais, reproduzíveis e executáveis em CI.

## Pré-requisitos

[Módulo 07](../07-evaluation-engineering/README.md); threat modeling, testes automatizados e contratos de ferramentas.

## Superfícies de ataque

| Superfície | Exemplos |
|---|---|
| Entrada | prompt injection, conteúdo adversarial, encoding enganoso |
| Contexto | documentos contaminados, instruções ocultas, proveniência ausente |
| Ferramentas | argumentos fora do schema, path traversal, SSRF, mutação indevida |
| Memória | persistência de instruções maliciosas, vazamento, dados obsoletos |
| Multiagentes | confused deputy, ampliação de autoridade, handoff adulterado |
| Segredos | logs, exceções, prompts, artefatos e commits |
| Saída | PII, credenciais, conteúdo proibido, falsa autorização |
| Operação | ausência de kill switch, alertas incompletos, rollback impossível |

## Threat modeling NEXUS

Use o fluxo:

```text
ativos → atores → fronteiras de confiança → capacidades → abuso → controles → evidências
```

Para cada ameaça, registre:

```yaml
threat_id: THR-001
asset: customer_records
trust_boundary: untrusted_retrieved_document
abuse_case: document attempts to instruct export of records
preconditions:
  - retriever accepts external content
  - tool can access customer data
controls:
  - content/instruction separation
  - least privilege
  - approval gate
  - output DLP
verification:
  - adversarial test case
  - structured security event
residual_risk: low
owner: security
```

## Princípios obrigatórios

1. **Deny by default** — capacidades precisam ser explicitamente concedidas.
2. **Least privilege** — cada agente recebe somente ferramentas, escopos e dados necessários.
3. **Assume breach** — conteúdo recuperado e outputs de outros agentes permanecem não confiáveis.
4. **Complete mediation** — toda chamada sensível atravessa o policy enforcement point.
5. **Fail closed** — erro de política, schema ou aprovação bloqueia a ação.
6. **Separation of duties** — planejar, executar, revisar e aprovar não devem compartilhar autoridade irrestrita.
7. **Evidence before release** — ausência de teste adversarial é bloqueador de release.

## Prompt injection

Conteúdo externo pode conter texto semelhante a instruções, mas não ganha autoridade por estar no contexto. A arquitetura deve preservar classes explícitas:

```json
{
  "trusted_instructions": ["system policy", "approved task contract"],
  "untrusted_content": ["retrieved page", "email body", "tool output"],
  "allowed_actions": ["summarize", "extract"],
  "forbidden_actions": ["reveal secrets", "change policy", "expand scope"]
}
```

Controles mínimos:

- proveniência por item;
- delimitação e rotulagem do conteúdo;
- política fora do conteúdo recuperado;
- allowlist de ações e ferramentas;
- validação de argumentos após o modelo;
- bloqueio de tentativas de alterar instruções, permissões ou destino;
- redaction antes de persistência e logs.

## Tool security

Toda ferramenta sensível precisa de:

- schema estrito;
- validação semântica;
- escopo de recursos;
- limites de volume;
- idempotência;
- timeout;
- classificação de efeito;
- preview;
- aprovação quando aplicável;
- reconciliação pós-efeito;
- evento de auditoria.

Exemplo de política:

```yaml
tool: customer.export
allowed_roles: [compliance_exporter]
tenant_scope: required
max_records: 100
requires_preview: true
requires_human_approval: true
approval_binds:
  - actor
  - tenant
  - arguments_hash
  - preview_hash
expires_in_seconds: 300
```

## Aprovação humana segura

Aprovação não deve ser um booleano genérico. Ela precisa estar vinculada a:

- identidade do aprovador;
- ação;
- tenant e projeto;
- argumentos canônicos;
- hash do preview;
- política vigente;
- prazo de expiração.

Qualquer alteração invalida a aprovação.

## Segredos e dados sensíveis

Regras:

- nunca incluir segredo em prompt quando um token opaco resolve;
- não registrar headers, credenciais ou payloads sensíveis;
- usar secrets manager em produção;
- rotacionar credenciais de curta duração;
- separar credenciais por ambiente, tenant e função;
- impedir commits de segredos;
- aplicar redaction em erros, traces e artefatos.

## Memória segura

Antes de persistir:

- classificar sensibilidade;
- remover segredos e PII desnecessária;
- verificar autoridade de escrita;
- aplicar tenant/project scope;
- bloquear instruções persistentes originadas de conteúdo não confiável;
- registrar proveniência, TTL e base legal quando aplicável.

## Multiagentes e confused deputy

Um agente não pode usar a autoridade de outro para realizar ação que ele próprio não poderia executar. Handoffs devem carregar intenção, escopo e capacidades delegadas, nunca autoridade implícita.

Bloqueie:

- delegação para agente não registrado;
- aumento de capabilities no handoff;
- troca de tenant;
- reuso de aprovação entre payloads;
- cadeia circular;
- execução por reviewer ou planner sem capacidade explícita.

## Output security

Antes da resposta ou efeito:

- verificar schema;
- detectar segredo, PII e dados de outro tenant;
- validar citações e proveniência;
- rejeitar conteúdo que afirma ter executado ação não comprovada;
- aplicar política de conteúdo e disclosure mínimo.

## Segurança operacional

Todo sistema de produção deve possuir:

- kill switch;
- budgets por execução e por tenant;
- rate limits;
- circuit breaker;
- eventos de segurança estruturados;
- alertas acionáveis;
- rollback ou compensação;
- runbook de incidente;
- retenção e acesso de logs governados.

## Red teaming

O conjunto adversarial deve incluir:

- injeção direta e indireta;
- encoding e obfuscação;
- exfiltração de segredo;
- path traversal e argumentos maliciosos;
- SSRF simulada;
- aprovação adulterada ou expirada;
- confused deputy;
- cross-tenant leakage;
- memory poisoning;
- adulteração de handoff;
- abuso de custo e loops;
- evasão de logging.

## Métricas

| Métrica | Interpretação |
|---|---|
| attack success rate | ataques que alcançam efeito proibido |
| blocked-before-tool rate | ataques interrompidos antes da chamada |
| secret exposure rate | outputs/logs contendo segredo |
| cross-tenant leakage rate | dados retornados fora do escopo |
| false positive rate | ações legítimas bloqueadas |
| approval integrity rate | aprovações válidas e corretamente vinculadas |
| mean time to detect | tempo até gerar evento/alerta |
| mean time to contain | tempo até bloquear ou revogar capacidade |

## Hard gates de release

Release deve falhar quando houver:

- qualquer exfiltração de segredo;
- qualquer efeito sensível sem aprovação válida;
- qualquer vazamento entre tenants;
- qualquer ampliação de autoridade;
- qualquer chamada fora da allowlist;
- qualquer aprovação aceita com hash divergente;
- ausência de trilha de auditoria para efeito externo;
- teste crítico ausente ou não executado.

## Implementação de referência

```bash
python examples/security_guardrails.py --self-test
```

A implementação local deve provar controles de política sem API, rede ou credenciais.

## Laboratório

- [LAB-801](../../../labs/LAB-801-agent-security-red-team.md) — red team reproduzível com hard gates.

## Projeto

Construa um gateway de segurança que:

1. rotule instruções e conteúdo;
2. aplique allowlist por papel;
3. valide tenant e argumentos;
4. detecte prompt injection e segredo;
5. exija aprovação vinculada por hash;
6. redija logs;
7. gere eventos de segurança;
8. execute suíte adversarial;
9. produza relatório de release.

## Quiz

1. Por que prompt injection não é resolvida apenas com outro prompt?
2. Qual a diferença entre validação de schema e validação semântica?
3. Por que aprovação precisa ser vinculada ao hash do preview?
4. Como ocorre o confused deputy em multiagentes?
5. Quando um sistema deve falhar fechado?

<details>
<summary>Gabarito comentado</summary>

1. Porque o problema envolve autoridade, dados e efeitos fora do modelo; são necessários controles arquiteturais.
2. Schema valida forma; validação semântica verifica escopo, intenção, limites e política.
3. Para impedir que uma aprovação seja reutilizada após alteração do conteúdo ou dos argumentos.
4. Quando um componente usa a autoridade de outro para realizar ação que não poderia executar diretamente.
5. Em erro de política, aprovação, identidade, escopo, schema ou integridade.

</details>

## Checklist

- [ ] Threat model versionado e com proprietários.
- [ ] Toda entrada externa é tratada como não confiável.
- [ ] Ferramentas usam deny-by-default e least privilege.
- [ ] Aprovações são vinculadas a ação, argumentos, preview e prazo.
- [ ] Segredos não aparecem em prompts, logs ou artefatos.
- [ ] Memória possui classificação, escopo e política de persistência.
- [ ] Cross-tenant e confused deputy estão cobertos por testes.
- [ ] Eventos de segurança são estruturados e redigidos.
- [ ] Hard gates bloqueiam release em violações críticas.
- [ ] Existe kill switch e runbook de incidente.

## Critérios de excelência

| Dimensão | Padrão Premium Elite |
|---|---|
| Autoridade | zero ampliação implícita ou confused deputy |
| Dados | zero segredo ou cross-tenant leakage |
| Efeitos | 100% dos efeitos sensíveis com aprovação íntegra |
| Testes | suíte adversarial reproduzível e versionada |
| Operação | detecção, contenção, rollback e auditoria comprovados |
| Release | hard gates prevalecem sobre médias agregadas |

## Referências

- OWASP — Top 10 for LLM Applications.
- NIST — AI Risk Management Framework.
- MITRE ATLAS — Adversarial Threat Landscape for AI Systems.
- Saltzer e Schroeder — The Protection of Information in Computer Systems.
- Google — Secure AI Framework (SAIF).

## Próximo passo

Conclua o LAB-801 e obtenha zero violações críticas antes de avançar para arquitetura de produção.
