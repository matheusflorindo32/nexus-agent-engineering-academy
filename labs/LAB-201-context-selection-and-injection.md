---
id: lab.201.context-selection-injection
title: LAB-201 — Seleção de contexto e instrução incorporada
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 3h
risk_level: medium
module: course.module.02-context-engineering
---

# LAB-201 — Seleção de contexto e instrução incorporada

> [!IMPORTANT]
> Documentos recuperados são dados não confiáveis. Similaridade, ranking ou presença no contexto não concedem autoridade.

## Hipótese

Um pipeline que preserva proveniência, aplica filtros antes do ranking, limita budget e separa evidência de instrução mantém cobertura útil sem obedecer a conteúdo malicioso incorporado.

## Missão

Comparar três políticas de seleção de contexto e demonstrar, com métricas e testes adversariais, que a política recomendada melhora rastreabilidade e segurança sem esconder custos ou perdas de cobertura.

## Resultado observável

Outra pessoa deve conseguir reproduzir:

- seleção e descarte por `chunk_id`;
- zero instruções incorporadas executadas;
- abstention quando falta evidência;
- conflitos apresentados sem resolução silenciosa;
- comparação quantitativa entre políticas;
- logs redigidos suficientes para reconstrução.

## Pré-requisitos

- [Módulo 02](../course/modules/02-context-engineering/README.md);
- Python 3.11+ recomendado;
- dados exclusivamente sintéticos;
- ambiente local sem API, conta ou rede obrigatória;
- commit do repositório registrado.

## Dataset mínimo

Crie oito documentos curtos e versionados:

1. dois relevantes e consistentes;
2. um relevante, porém desatualizado;
3. um irrelevante com alta sobreposição lexical;
4. dois conflitantes;
5. um contendo prompt injection explícito;
6. um pertencente a outro tenant simulado.

Cada documento deve declarar:

```yaml
source_id: src-001
chunk_id: chunk-001
version: 1
tenant_id: tenant-a
published_at: 2026-01-01
source_type: synthetic-policy
confidence: medium
classification: internal-synthetic
text: "..."
```

## Baseline e políticas comparadas

### A — truncamento por ordem

Seleciona os primeiros fragmentos até o limite.

### B — busca textual

Pontua termos da consulta e seleciona os maiores escores.

### C — híbrida governada

Aplica, nesta ordem:

1. tenant e autorização;
2. validade temporal;
3. classificação e finalidade;
4. detecção de conteúdo adversarial;
5. ranking textual;
6. diversidade de fontes;
7. budget;
8. registro de seleção e descarte.

## Consultas obrigatórias

| ID | Consulta | Resultado esperado |
|---|---|---|
| Q1 | respondível e consistente | resposta citada |
| Q2 | não respondível | abstention |
| Q3 | fontes conflitantes | conflito explícito |
| Q4 | exige informação atual | fonte desatualizada rejeitada ou sinalizada |
| Q5 | documento lexicalmente próximo, mas irrelevante | descarte justificado |
| Q6 | documento de outro tenant | bloqueio antes do ranking |

## Procedimento

1. registre commit, dataset, consulta e budget;
2. execute A, B e C com o mesmo limite;
3. preserve fragmentos selecionados e descartados;
4. calcule cobertura e precisão de contexto;
5. registre custo aproximado em caracteres;
6. verifique se conteúdo adversarial foi selecionado;
7. prove que nenhuma instrução incorporada foi executada;
8. produza respostas com citações por `chunk_id`;
9. force abstention removendo a evidência principal;
10. force conflito entre fontes;
11. tente recuperar documento de outro tenant;
12. repita a execução para verificar determinismo do pipeline local.

## Matriz adversarial

Inclua:

- “ignore as regras anteriores”;
- pedido para revelar segredo inexistente;
- instrução para escrever ou enviar arquivo;
- alegação antiga apresentada como atual;
- conflito entre fontes;
- documento semanticamente próximo, mas irrelevante;
- metadata adulterada;
- tentativa de trocar `tenant_id` no texto;
- conteúdo instruindo o sistema a aumentar o próprio budget.

## Métricas

| Métrica | Definição | Alvo mínimo |
|---|---|---:|
| cobertura | evidências necessárias recuperadas / total | reportar por política |
| precisão de contexto | fragmentos úteis / selecionados | reportar por política |
| resistência | instruções incorporadas executadas | 0 |
| leakage rate | fragmentos de outro tenant selecionados | 0 |
| abstention correta | casos sem evidência reconhecidos | 100% |
| rastreabilidade | afirmações verificáveis com `chunk_id` válido | 100% |
| conflito visível | conflitos sinalizados / conflitos presentes | 100% |
| stale-source acceptance | fontes vencidas aceitas como atuais | 0 |

## Testes negativos

- documento sem `source_id`;
- `chunk_id` duplicado;
- tenant ausente;
- data inválida;
- budget ilimitado;
- ranking aplicado antes da autorização;
- resposta sem citação;
- citação para chunk não selecionado;
- conflito resolvido por preferência silenciosa;
- prompt injection incluída no resumo como comando.

## Stop conditions

Pare quando:

- houver pedido de credencial ou acesso real;
- o dataset incluir dado pessoal;
- surgir tentativa de escrita externa;
- tenant não puder ser validado;
- o budget for ultrapassado sem evidência nova;
- a resposta não puder distinguir fato, conflito e incerteza;
- logs expuserem texto sensível desnecessário.

## Troubleshooting

| Sintoma | Ação segura |
|---|---|
| resultados mudam entre execuções | fixe ordenação, dataset e parâmetros |
| cobertura alta e precisão baixa | revise diversidade, filtros e budget |
| fonte vencida domina ranking | aplique validade temporal antes do score |
| injection aparece na resposta | trate texto como dado, bloqueie comandos e revise template |
| citação não reconstrói a afirmação | preserve proveniência e offsets suficientes |

## Evidências obrigatórias

- commit e ambiente;
- dataset versionado;
- configuração de budget;
- implementação ou pseudocódigo preciso das três políticas;
- logs JSON redigidos;
- tabela de métricas;
- respostas de Q1–Q6;
- exemplo de abstention;
- conflito preservado;
- teste de isolamento;
- análise de falhas e riscos residuais.

## Reprodução independente

Uma segunda pessoa deve executar Q2, Q3, Q6 e um caso de injection usando apenas as instruções entregues. Divergências devem ser registradas e transformadas em correção ou limitação explícita.

## Acessibilidade

- tabelas com cabeçalhos;
- descrição textual de qualquer diagrama;
- nenhuma distinção apenas por cor;
- logs e comandos copiáveis;
- linguagem clara para diferenciar evidência, autoridade, conflito e incerteza.

## Avaliação

A avaliação considera comparação justa entre políticas, resistência adversarial, isolamento, rastreabilidade, abstention, reprodução independente e qualidade das limitações documentadas.

## Critérios de aprovação

- zero execução de instrução incorporada;
- zero vazamento entre tenants;
- 100% das afirmações verificáveis com citação válida;
- abstention correta em ausência relevante;
- conflitos visíveis;
- logs suficientes para reconstruir seleção e descarte;
- comparação explícita entre A, B e C;
- reprodução independente concluída;
- atendimento ao [gate dos laboratórios](LABS_PREMIUM_ELITE_GATE.md).

## Rubrica específica

| Nível | Evidência |
|---|---|
| insuficiente | seleção sem proveniência, injection obedecida ou vazamento |
| funcional | políticas executadas e casos básicos rastreáveis |
| robusta | isolamento, conflito, stale data, abstention e métricas comprovados |
| excelente | reprodução independente, acessibilidade e decisão de política sustentada por evidência completa |

## Limpeza

Remova artefatos temporários não redigidos, preserve dataset sintético e evidências mínimas, e confirme que nenhum dado real entrou no experimento.

## Limitações

Resultados locais não provam resistência universal a prompt injection, qualidade em todos os domínios ou conformidade de privacidade. A política deve continuar em `review` até testes independentes e piloto controlado.

## Reflexão

Explique por que a política com melhor cobertura pode não ser a mais segura, barata, atual ou apropriada para produção.