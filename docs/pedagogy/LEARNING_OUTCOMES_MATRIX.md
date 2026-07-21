---
id: docs.pedagogy.learning-outcomes-matrix
title: Matriz de resultados de aprendizagem
lang: pt-BR
status: review
---

# Matriz de resultados de aprendizagem

## Finalidade

Esta matriz conecta cada resultado de aprendizagem a conteúdo, prática, laboratório, avaliação e evidência. Ela impede que objetivos existam apenas como intenção editorial.

## Regra de alinhamento

Todo resultado deve:

1. usar verbo observável;
2. declarar condições de execução;
3. possuir padrão mínimo de qualidade;
4. gerar evidência verificável;
5. ser avaliado por instrumento compatível;
6. declarar riscos e limites quando houver efeito externo.

## Matriz curricular principal

| Módulo | Resultado observável | Aula ou seção | Prática | LAB | Avaliação | Evidência mínima |
|---|---|---|---|---|---|---|
| 00 | navegar a arquitetura NEXUS e registrar decisão reproduzível | arquitetura, ciclo NEXUS e ADR | localizar conceito, exemplo e template | LAB-000 | diagnóstico + ADR | comando executado, SHA, saída e ADR |
| 01 | diferenciar modelo, assistente, workflow e agente por critérios testáveis | taxonomia e contrato de agente | especificar agente read-only | LAB-101 | quiz + projeto | agent spec, casos e baseline |
| 02 | construir pipeline de contexto com seleção, limites e avaliação | contexto, recuperação e relevância | comparar estratégias de seleção | LAB-201 | experimento comparativo | dataset, métricas e análise de erro |
| 03 | implementar ferramenta com validação, menor privilégio e tratamento de falhas | tool contract e boundary | criar tool segura | LAB-301 | teste prático | schema, testes, recusas e logs |
| 04 | implementar loop com budgets, retries e stop conditions | loop controlável | comparar políticas de retry | LAB-401 | simulação de falha | estados, limites, recovery e evidência |
| 05 | projetar memória com retenção, correção e proteção de dados | memória governada | armazenar, recuperar e excluir | LAB-501 | estudo de caso | política, testes e trilha de auditoria |
| 06 | coordenar agentes com papéis, supervisão e medição de ganho real | coordenação multiagente | comparar agente único e equipe | LAB-601 | experimento A/B | métricas, conflitos e decisão arquitetural |
| 07 | criar suíte de avaliação reproduzível e útil para decisão | datasets, métricas e regressão | construir casos positivos e negativos | LAB-701 | eval suite | dataset versionado, resultados e limites |
| 08 | elaborar threat model e testar guardrails adversarialmente | ameaças, privilégios e aprovação | red team sintético | LAB-801 | revisão de segurança | ameaças, testes, mitigação e risco residual |
| 09 | desenhar arquitetura operável com rollout, rollback e degradação segura | runtime de produção | simular falha de dependência | LAB-901 | revisão arquitetural | diagrama, runbook e plano de rollback |
| 10 | construir telemetria segura, correlacionada e acionável | logs, métricas, alertas e redaction | validar canais de telemetria | LAB-1001 | self-test + análise | evidência, alertas, runbook e limitações |
| 11 | implementar automação idempotente e compensável | idempotência e orquestração | simular retry e duplicidade | LAB-1101 | teste de recuperação | chave, estado, compensação e logs |
| 12 | integrar arquitetura, segurança, avaliação e operação em sistema completo | capstone | projeto incremental | LAB-1201 planejado | defesa técnica | repositório, relatório, demonstração e defesa |

## Trilha Zero

| Unidade | Resultado observável | Prática | Avaliação | Evidência |
|---|---|---|---|---|
| Z00 | identificar arquivos, pastas, programas e ambiente de desenvolvimento | organizar projeto local | checklist prático | estrutura criada e explicada |
| Z01 | executar comandos básicos sem privilégios desnecessários | navegar, criar e remover arquivos seguros | desafio guiado | histórico de comandos comentado |
| Z02 | clonar, criar branch, commit e abrir PR simples | contribuição simulada | tarefa prática | branch, commit e PR |
| Z03 | ler e alterar script Python básico | executar e corrigir programa | exercício com testes | código e saída |
| Z04 | editar Markdown, JSON e YAML válidos | corrigir arquivos malformados | validação automática | arquivos aprovados |
| Z05 | explicar requisição HTTP, API e variável de ambiente | chamada local simulada | quiz + prática | request/response sintética |
| Z06 | proteger segredo e reconhecer risco básico | remover credencial sintética | cenário adversarial | correção e justificativa |
| Z07 | clonar, executar, testar e diagnosticar projeto | reproduzir quickstart | prova prática | relatório de execução |
| Z08 | construir workflow determinístico simples | fluxo com decisões fixas | comparação | diagrama e testes |
| Z09 | construir agente mínimo com limite e recusa | agente local read-only | projeto curto | spec, execução e logs |

## Níveis de desempenho

| Nível | Descrição |
|---|---|
| Insuficiente | não produz evidência reproduzível ou viola gate de segurança |
| Funcional | executa o caso principal e documenta condições mínimas |
| Robusto | cobre falhas, testes negativos, limites e recuperação |
| Excelente | compara alternativas, mede resultados e explicita risco residual |

## Gates

- nenhum resultado é considerado atingido apenas por leitura;
- quiz isolado não comprova competência prática;
- projeto inseguro não pode ser aprovado por sofisticação técnica;
- evidência sem versão, contexto ou procedimento é insuficiente;
- objetivos do Capstone devem rastrear competências dos módulos anteriores.

## Lacunas atuais

- vários módulos ainda precisam mapear seções e exercícios concretos para esta matriz;
- o LAB-1201 permanece planejado;
- soluções comentadas não estão completas em toda a trilha;
- a validade pedagógica depende de piloto com alunos reais.
