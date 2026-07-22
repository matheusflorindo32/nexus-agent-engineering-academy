---
id: course.rubric.transversal
title: Rubrica transversal NEXUS
lang: pt-BR
status: review
version: 0.2.0
---

# Rubrica transversal NEXUS

Use esta rubrica em módulos, laboratórios e projetos. A nota resume desempenho; ela nunca substitui hard gates, evidência ou julgamento humano.

## Escala

| Nível | Significado |
|---|---|
| 0 — Insuficiente | resultado ausente, não verificável ou com bloqueio crítico |
| 1 — Funcional | cumpre o mínimo, mas possui lacunas relevantes registradas |
| 2 — Robusto | reproduzível, governado, testado e bem justificado |
| 3 — Excelente | inclui comparação, validação adversarial, reprodução independente e melhoria mensurável |

## Dimensões

| Dimensão | 0 — Insuficiente | 1 — Funcional | 2 — Robusto | 3 — Excelente |
|---|---|---|---|---|
| Objetivo e escopo | vago ou sem limites | resultado principal identificado | objetivo observável, critérios e non-goals | trade-offs, owner e risco residual explícitos |
| Reprodutibilidade | faltam passos ou versões | procedimento básico | commit, versões, entradas, outputs e seed | terceiro reproduz e confirma resultados críticos |
| Evidência e rastreabilidade | opinião ou artefato isolado | evidência mínima | múltiplas evidências correlacionadas | evidence bundle independente e reconstrução causal |
| Engenharia | solução improvisada | contratos básicos | estados, interfaces, budgets e falhas explícitos | alternativas comparadas com ADR e métricas |
| Avaliação | sem baseline ou critérios | testes felizes | dataset, graders, thresholds e regressão | holdout, variância, trajetória e hard gates auditáveis |
| Segurança e privacidade | segredo, privilégio ou vazamento | riscos reconhecidos | least privilege, isolamento, redaction e stop conditions | threat model, red team, resposta e risco residual revisado |
| Operação e resiliência | sem pause ou recuperação | tratamento básico de erro | rollback, reconciliação, kill switch e runbook | game day, restore e métricas de recuperação |
| Observabilidade | logs soltos ou sensíveis | eventos básicos | correlação, métricas, traces e auditoria | integridade, cobertura, alertas e modo degradado testados |
| Qualidade pedagógica | passivo ou confuso | explicação e exercício | prática ativa, feedback, progressão e acessibilidade | transferência, metacognição e piloto com evidências |
| Referências e proveniência | inexistentes ou inventadas | fonte adequada | fontes primárias, versão e data | triangulação e limites da evidência explícitos |
| Comunicação e acessibilidade | difícil ou dependente de cor | compreensível | clara, estruturada, navegável e com texto alternativo | síntese visual/textual validada por usuário diverso |
| Internacionalização | IDs instáveis | estrutura traduzível | IDs e termos controlados | paridade verificada entre idiomas |
| Reflexão e melhoria | não reconhece limites | lista limitações | prioriza melhorias com owner | mede impacto e define próximo experimento falsificável |

## Hard gates transversais

A entrega é reprovada independentemente da média quando houver:

- nota 0 em segurança, privacidade, evidência/rastreabilidade ou reprodutibilidade;
- segredo ou dado pessoal real em artefato;
- vazamento entre tenants, sujeitos ou projetos;
- efeito proibido, não autorizado ou duplicado;
- hard gate compensado por média;
- evidência adulterada ou não versionada;
- retry cego após efeito desconhecido;
- risco alto ou crítico sem tratamento, owner e decisão;
- imagem sem licença/proveniência ou texto alternativo;
- alegação de segurança, conformidade ou prontidão absoluta.

## Regras de aprovação

- conclusão de módulo: média mínima **1,5**, sem hard gate falho;
- laboratório: média mínima **2,0**, critérios específicos e reprodução quando exigida;
- projeto starter: média mínima **2,0**, segurança e reprodutibilidade ≥ 2;
- selo Premium Elite: média mínima **2,5**, nenhuma dimensão abaixo de 2 e reprodução independente;
- capstone: rubrica específica + transversal, game day e defesa humana;
- nível 3 exige evidência observável, não apenas texto mais detalhado.

## Processo de revisão

1. valide identidade do artefato, commit e versões;
2. verifique hard gates antes da pontuação;
3. avalie cada dimensão citando evidências;
4. registre incertezas e itens não aplicáveis;
5. peça segunda revisão para entregas de alto risco;
6. produza decisão e próxima ação concreta;
7. reavalie apenas após nova evidência versionada.

## Registro recomendado

```yaml
rubric_id: course.rubric.transversal
rubric_version: 0.2.0
artifact_id: <id>
artifact_commit: <sha>
reviewer: <identificador>
reviewer_role: <papel>
reviewed_at: YYYY-MM-DD
scope: <escopo-exato>
evidence_refs: []
scores:
  objective_scope: 0
  reproducibility: 0
  evidence_traceability: 0
  engineering: 0
  evaluation: 0
  security_privacy: 0
  operations_resilience: 0
  observability: 0
  pedagogy: 0
  references_provenance: 0
  communication_accessibility: 0
  i18n: 0
  reflection_improvement: 0
blocking_findings: []
residual_risks: []
decision: blocked | revise | approved_with_constraints | approved
next_action: <ação concreta>
```

## Honestidade

Rubricas reduzem ambiguidade, mas não eliminam viés, desacordo ou lacunas de teste. A pontuação deve ser acompanhada por evidências, limitações e revisão humana adequada ao risco.