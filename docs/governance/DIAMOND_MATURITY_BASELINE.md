---
id: governance.diamond-maturity-baseline
title: Baseline de maturidade Diamante Premium Elite
lang: pt-BR
status: review
version: 0.1.0
---

# Baseline de maturidade Diamante Premium Elite

## Resumo executivo

Este documento registra a primeira linha de base auditável para a evolução do Nexus Agent Engineering Academy. Ele não certifica o projeto, não substitui auditoria independente e não autoriza merge, release ou produção.

A avaliação usa uma escala provisória de 0 a 5:

- 0 — inexistente;
- 1 — inicial;
- 2 — parcialmente definido;
- 3 — implementado;
- 4 — medido e controlado;
- 5 — otimizado, validado e auditável.

Nenhum domínio recebe nível 5 nesta versão. Os níveis abaixo refletem apenas evidências observadas no repositório e nos workflows até o commit-base deste documento.

## Regras de governança

1. `main` não pode ser alterada diretamente.
2. Nenhum merge pode ser automático.
3. Todo novo Pull Request permanece em Draft até decisão humana explícita.
4. CI verde é evidência técnica, não aprovação humana.
5. Validadores e testes existentes não podem ser enfraquecidos.
6. Conteúdo pedagógico permanece `status: review` até validação real com aprendizes.
7. O status `pilot` não deve ser utilizado.
8. Nenhuma alegação absoluta de segurança, conformidade, acessibilidade ou eficácia é permitida.

## Evidências atualmente confirmadas

- instalação reprodutível do portal;
- preview verificável;
- ensaio de rollback;
- integridade de artefato com controle positivo e negativo;
- SBOM CycloneDX 1.5 derivado do lockfile;
- digest SHA-256 do SBOM;
- controle de determinismo por geração repetida;
- declaração de proveniência gerada pelo workflow;
- documentação de governança em `status: review`;
- workflows de qualidade técnica ativos.

Evidências principais no repositório:

- `.github/workflows/portal-artifact-integrity.yml`;
- `.github/workflows/portal-rollback-rehearsal.yml`;
- `.github/workflows/portal-preview-quality.yml`;
- `.github/workflows/portal-sbom-provenance.yml`;
- `portal/scripts/verify-artifact-integrity.mjs`;
- `portal/scripts/generate-sbom.mjs`;
- `docs/governance/PORTAL_ARTIFACT_INTEGRITY.md`;
- `docs/governance/PORTAL_SBOM_PROVENANCE.md`.

## Mapa provisório de maturidade

| Domínio | Nível | Evidência observada | Lacuna principal | Confiança |
|---|---:|---|---|---|
| Arquitetura | 2 | Estrutura funcional e documentação parcial | Falta mapa arquitetural consolidado e ADRs | ★★★☆☆ |
| Código | 3 | Gates de qualidade e build ativos | Falta baseline formal de cobertura e dívida técnica | ★★★★☆ |
| Testes | 2 | Smoke tests e gates técnicos | Falta suíte E2E abrangente e regressão visual | ★★★★☆ |
| CI | 4 | Workflows independentes e reproduzíveis | Falta gate consolidado de release readiness | ★★★★★ |
| Segurança | 1 | Controles de integridade e permissões mínimas | Falta SAST, secrets, OSV, Trivy e threat model | ★★★★☆ |
| Supply chain | 3 | Lockfile, SBOM, digest e proveniência limitada | Falta assinatura/atestação externa e política de licenças | ★★★★★ |
| Acessibilidade | 1 | Intenção registrada | Faltam axe, WCAG, teclado e validação humana | ★★★☆☆ |
| UX | 1 | Portal funcional | Faltam pesquisa com usuários e métricas de usabilidade | ★★★☆☆ |
| Documentação | 3 | Contratos documentais e governança | Falta índice mestre, arquitetura e guias operacionais | ★★★★☆ |
| Ciência | 1 | Diretriz de ciência baseada em evidências | Falta protocolo editorial e registro de fontes | ★★★☆☆ |
| Didática | 1 | Status de revisão e intenção pedagógica | Faltam rubricas, objetivos, avaliação e validação | ★★★☆☆ |
| Avaliação educacional | 0 | Sem evidência suficiente | Definir instrumentos e protocolo com aprendizes | ★★★★★ |
| Governança | 3 | Regras explícitas, Draft e aprovação humana | Faltam RACI, ADRs e política de exceções | ★★★★☆ |
| Privacidade | 0 | Sem evidência suficiente | Inventário de dados, base legal e minimização | ★★★★☆ |
| Operação | 2 | Preview, rollback e artefatos | Faltam SLOs, runbooks e incident response | ★★★★☆ |
| Observabilidade | 0 | Sem evidência suficiente | Logs, métricas, tracing e health checks | ★★★★★ |
| Resiliência | 2 | Ensaio de rollback | Faltam DR, RTO, RPO e chaos controlado | ★★★★☆ |
| Release | 2 | Gates individuais | Falta decisão consolidada e checklist de readiness | ★★★★☆ |
| Auditoria | 2 | Evidências por workflow | Falta relatório consolidado e revisão independente | ★★★★☆ |
| Internacionalização | 1 | Parte da documentação em inglês | Falta estratégia de idiomas e consistência editorial | ★★★☆☆ |

## Riscos prioritários

| ID | Risco | Probabilidade | Impacto | Criticidade | Controle atual | Tratamento recomendado |
|---|---|---|---|---|---|---|
| R-001 | Cobertura funcional insuficiente | Alta | Alto | Crítica | Smoke tests | Implementar Playwright E2E por fluxos críticos |
| R-002 | Vulnerabilidades e segredos não detectados | Média | Muito alto | Crítica | Integridade e lockfile | Adicionar CodeQL, Gitleaks, OSV e Trivy |
| R-003 | Barreiras de acessibilidade | Alta | Alto | Crítica | Nenhum gate confirmado | Axe, Lighthouse, teclado e testes humanos |
| R-004 | Conteúdo pedagógico sem validação real | Alta | Alto | Crítica | `status: review` | Protocolo com aprendizes e rubricas |
| R-005 | Decisão de release fragmentada | Média | Alto | Alta | Gates isolados | Criar Release Readiness consolidado |
| R-006 | Ausência de observabilidade operacional | Média | Alto | Alta | Logs de CI | Definir SLOs, métricas, runbooks e alertas |
| R-007 | Privacidade não mapeada | Média | Muito alto | Crítica | Nenhuma evidência suficiente | Inventário de dados e avaliação LGPD |
| R-008 | Complexidade crescente dos workflows | Média | Médio | Média | Workflows especializados | Catálogo, ownership e redução de redundância |

## Visão do padrão Diamante

O padrão interno Diamante somente poderá ser considerado após evidências convergentes nos seguintes pilares:

1. engenharia reproduzível;
2. segurança contínua e modelagem de ameaças;
3. testes funcionais e não funcionais;
4. acessibilidade técnica e humana;
5. ciência e referências verificáveis;
6. didática validada com aprendizes;
7. governança com decisões rastreáveis;
8. observabilidade e resposta a incidentes;
9. recuperação testada;
10. auditoria externa ou revisão independente.

O termo “Diamante” é uma classificação interna de maturidade. Não representa certificação ISO, NIST, OWASP, SLSA ou qualquer acreditação externa.

## Roadmap por ondas

### Onda 0 — Estabilização

- manter todos os gates atuais verdes;
- registrar causas-raiz e correções;
- impedir regressão dos contratos documentais;
- concluir revisão humana dos PRs empilhados.

### Onda 1 — Fundação

- ADRs;
- mapa arquitetural;
- catálogo de workflows;
- RACI e owners;
- baseline de cobertura e dívida técnica.

### Onda 2 — Qualidade

- E2E com Playwright;
- segurança estática e de dependências;
- acessibilidade automatizada;
- performance budget;
- regressão visual controlada.

### Onda 3 — Ciência e didática

- política editorial baseada em evidências;
- registro verificável de fontes;
- objetivos de aprendizagem;
- rubricas;
- avaliações formativas e somativas;
- protocolo de validação humana.

### Onda 4 — Governança

- release readiness;
- política de exceções;
- matriz de riscos viva;
- indicadores e revisões periódicas;
- trilha de auditoria.

### Onda 5 — Resiliência

- observabilidade;
- incident response;
- disaster recovery;
- RTO e RPO;
- chaos testing apenas em ambiente isolado.

### Onda 6 — Internacionalização

- estratégia pt-BR/en;
- guia editorial;
- metadados consistentes;
- glossário técnico;
- acessibilidade linguística.

### Onda 7 — Validação humana

- aprendizes iniciantes, intermediários e avançados;
- professores e especialistas;
- pessoas com deficiência;
- revisores técnicos, científicos e linguísticos.

### Onda 8 — Auditoria Diamante

- relatório consolidado;
- evidências por domínio;
- riscos residuais;
- pareceres independentes;
- decisão humana formal.

## Sequência proposta de Pull Requests

| Ordem | Entrega | Prioridade | Dependência |
|---:|---|---|---|
| 46 | Testes E2E e fluxos críticos | P0 | PR 45 |
| 47 | Segurança de código, segredos e dependências | P0 | PR 46 |
| 48 | Acessibilidade automatizada | P0 | PR 47 |
| 49 | Performance budget e Core Web Vitals | P1 | PR 48 |
| 50 | Release Readiness consolidado | P0 | PR 49 |
| 51 | ADRs e mapa arquitetural | P1 | PR 50 |
| 52 | Política científica e registro de fontes | P1 | PR 51 |
| 53 | Framework pedagógico e rubricas | P1 | PR 52 |
| 54 | Protocolo de validação humana | P0 | PR 53 |
| 55 | Observabilidade e runbooks | P1 | PR 54 |
| 56 | Disaster Recovery e continuidade | P1 | PR 55 |
| 57 | Chaos testing isolado | P2 | PR 56 |
| 58 | Internacionalização editorial | P2 | PR 57 |
| 59 | Auditoria consolidada Diamante | P0 | PR 58 |

## Critérios de aceite desta baseline

- documento compatível com o contrato documental do repositório;
- todas as notas acompanhadas por evidência e lacuna;
- nenhuma alegação de certificação;
- riscos prioritários registrados;
- roadmap e sequência de PRs definidos;
- limitações explícitas;
- `status: review` preservado;
- decisão humana obrigatória antes de qualquer merge.

## Limitações

- a avaliação não inclui auditoria independente;
- não houve entrevista com mantenedores ou usuários;
- não houve teste humano de acessibilidade;
- não houve validação pedagógica com aprendizes;
- não houve inventário jurídico completo;
- não houve inspeção manual de cada arquivo do repositório nesta etapa;
- as notas devem ser atualizadas quando novas evidências forem produzidas.

## Próximo passo recomendado

Implementar o PR de testes E2E como primeira capacidade distinta da Fase 2, sem remover ou substituir os gates existentes.

## Nível de confiança global

**★★★★☆ — alto.**

A avaliação possui evidência direta para CI, integridade, rollback e supply chain. A confiança é menor nos domínios pedagógico, científico, jurídico, UX e acessibilidade porque ainda faltam validação humana e inventários específicos.
