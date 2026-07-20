---
id: docs.references.abnt
 title: Referências ABNT e matriz de verificação
lang: pt-BR
status: review
---

# Referências ABNT e matriz de verificação

## Escopo

Este documento registra as fontes usadas nas decisões curriculares, de segurança, observabilidade, qualidade e governança do NEXUS Agent Engineering Academy. A apresentação segue os elementos essenciais da ABNT NBR 6023 quando os metadados estão disponíveis.

## Limitação normativa

A edição vigente e o texto integral das normas ABNT devem ser confirmados no catálogo oficial ou por acesso institucional licenciado antes de declarar conformidade formal. Este repositório não reproduz conteúdo protegido das normas e não afirma auditoria normativa completa sem essa consulta.

## Critérios de inclusão

- fonte primária ou documentação oficial;
- autoria ou instituição identificável;
- versão, data ou DOI verificável;
- relação explícita com um requisito do repositório;
- acesso registrado em 19 jul. 2026.

## Critérios de exclusão

- referência sem autoria ou origem verificável;
- DOI ou URL não confirmado;
- blog secundário quando existe especificação oficial;
- fonte que não sustenta a afirmação associada;
- norma citada apenas por memória, sem confirmação de catálogo.

## Referências verificadas

### Inteligência artificial e gestão de riscos

TABASSI, Elham. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. Gaithersburg: National Institute of Standards and Technology, 2023. NIST AI 100-1. DOI: https://doi.org/10.6028/NIST.AI.100-1. Disponível em: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10. Acesso em: 19 jul. 2026.

AUTIO, Chloe et al. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. Gaithersburg: National Institute of Standards and Technology, 2024. NIST AI 600-1. DOI: https://doi.org/10.6028/NIST.AI.600-1. Disponível em: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence. Acesso em: 19 jul. 2026.

### Segurança de agentes

OPEN WORLDWIDE APPLICATION SECURITY PROJECT. *AI Agent Security Cheat Sheet*. [S. l.]: OWASP Cheat Sheet Series, [2026]. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html. Acesso em: 19 jul. 2026.

### Observabilidade

CLOUD NATIVE COMPUTING FOUNDATION. *OpenTelemetry Specification*. [S. l.]: OpenTelemetry Authors, [s. d.]. Disponível em: https://opentelemetry.io/docs/specs/. Acesso em: 19 jul. 2026.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *Guide to Computer Security Log Management*. Gaithersburg: NIST, 2006. NIST Special Publication 800-92. DOI: https://doi.org/10.6028/NIST.SP.800-92. Acesso em: 19 jul. 2026.

### Desenvolvimento seguro

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. *Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities*. Gaithersburg: NIST, 2022. NIST Special Publication 800-218. DOI: https://doi.org/10.6028/NIST.SP.800-218. Acesso em: 19 jul. 2026.

### Confiabilidade

BEYER, Betsy et al. *Site Reliability Engineering: how Google runs production systems*. Sebastopol: O'Reilly Media, 2016.

### Arquitetura e integração

HOHPE, Gregor; WOOLF, Bobby. *Enterprise Integration Patterns: designing, building, and deploying messaging solutions*. Boston: Addison-Wesley, 2003.

FORD, Neal et al. *Software Architecture: the hard parts*. Sebastopol: O'Reilly Media, 2021.

### Versionamento e changelog

KEEP A CHANGELOG. *Keep a Changelog 1.1.0*. [S. l.], 2023. Disponível em: https://keepachangelog.com/en/1.1.0/. Acesso em: 19 jul. 2026.

SEMANTIC VERSIONING. *Semantic Versioning 2.0.0*. [S. l.], [s. d.]. Disponível em: https://semver.org/spec/v2.0.0.html. Acesso em: 19 jul. 2026.

## Normas ABNT a confirmar por acesso oficial

As normas abaixo são requisitos editoriais declarados pelo projeto, mas sua edição vigente e metadados completos não foram confirmados nesta execução por acesso ao texto oficial licenciado:

- ABNT NBR 6023 — referências;
- ABNT NBR 10520 — citações;
- ABNT NBR 14724 — apresentação de trabalhos acadêmicos;
- ABNT NBR 6024 — numeração progressiva;
- ABNT NBR 6027 — sumário;
- ABNT NBR 6028 — resumo.

Status: **PARCIALMENTE VERIFICADAS — confirmar no catálogo ABNT antes de declaração formal de conformidade**.

## Matriz de rastreabilidade das fontes

| ID | Tema | Afirmação apoiada | Fonte primária | Status | Data |
|---|---|---|---|---|---|
| REF-001 | gestão de risco de IA | riscos devem ser governados, mapeados, medidos e geridos ao longo do ciclo de vida | NIST AI RMF 1.0 | VERIFICADA | 19 jul. 2026 |
| REF-002 | IA generativa | riscos específicos de IA generativa exigem perfil complementar ao AI RMF | NIST AI 600-1 | VERIFICADA | 19 jul. 2026 |
| REF-003 | segurança agentic | ferramentas exigem mínimo privilégio, validação, monitoramento e testes adversariais | OWASP AI Agent Security Cheat Sheet | VERIFICADA | 19 jul. 2026 |
| REF-004 | observabilidade | traces, métricas e logs requerem contratos e semântica consistente | OpenTelemetry Specification | VERIFICADA | 19 jul. 2026 |
| REF-005 | logging seguro | gestão de logs deve considerar segurança, retenção e proteção de dados | NIST SP 800-92 | VERIFICADA | 19 jul. 2026 |
| REF-006 | desenvolvimento seguro | práticas de segurança devem integrar o ciclo de desenvolvimento | NIST SP 800-218 | VERIFICADA | 19 jul. 2026 |
| REF-007 | confiabilidade | SLOs, alertas e runbooks sustentam operação confiável | Google SRE | VERIFICADA POR OBRA PUBLICADA | 19 jul. 2026 |
| REF-008 | integração | idempotência, mensageria e compensação exigem padrões explícitos | Enterprise Integration Patterns | VERIFICADA POR OBRA PUBLICADA | 19 jul. 2026 |
| REF-009 | referências | forma e elementos de referências acadêmicas | ABNT NBR 6023 | PARCIALMENTE VERIFICADA | 19 jul. 2026 |
| REF-010 | citações | apresentação de citações em documentos | ABNT NBR 10520 | PARCIALMENTE VERIFICADA | 19 jul. 2026 |

## Regra editorial

Nenhuma fonte marcada como `NÃO VERIFICADA` pode sustentar requisito bloqueante. Referências parcialmente verificadas devem permanecer acompanhadas de limitação explícita até conferência institucional.
