---
id: docs.pedagogy.pilot-plan
title: Plano de piloto pedagógico
lang: pt-BR
status: review
---

# Plano de piloto pedagógico

## Objetivo

Validar se a NEXUS ensina de fato os públicos definidos, em vez de inferir aprendizagem a partir de documentação existente ou CI verde.

## Amostra mínima

| Perfil | Quantidade mínima | Critério de entrada |
|---|---:|---|
| Iniciante absoluto | 2 | sem experiência prática em programação, Git ou terminal |
| Iniciante em programação | 2 | conhece lógica e executa scripts simples |
| Intermediário | 2 | desenvolve aplicações e usa Git regularmente |
| Avançado | 2 | experiência com arquitetura, IA aplicada ou sistemas distribuídos |

A amostra mínima serve para detectar problemas graves, não para provar validade estatística ampla.

## Fases

### Fase 1 — teste de entrada

- consentimento informado;
- perfil e experiência;
- diagnóstico inicial;
- expectativas;
- disponibilidade;
- necessidades de acessibilidade.

### Fase 2 — observação da Trilha Zero

Aplicável aos dois grupos iniciantes.

Observar:

- compreensão das instruções;
- dependência de ajuda;
- erros de ambiente;
- tempo por unidade;
- ansiedade e confiança;
- capacidade de repetir o procedimento sem roteiro.

### Fase 3 — teste dos módulos 00–02

Todos os participantes devem executar:

- Módulo 00;
- Módulo 01;
- Módulo 02;
- práticas e LABs correspondentes.

### Fase 4 — amostragem dos módulos avançados

Intermediários e avançados devem testar ao menos:

- um módulo de arquitetura ou loops;
- um módulo de segurança ou avaliação;
- um módulo de produção ou observabilidade.

### Fase 5 — avaliação pós

- pós-teste equivalente ao diagnóstico;
- execução prática sem roteiro;
- entrevista semiestruturada;
- escala de dificuldade;
- confiança percebida;
- intenção de continuar;
- revisão dos artefatos produzidos.

## Métricas obrigatórias

| Métrica | Como medir | Sinal de atenção |
|---|---|---|
| Tempo por unidade | cronômetro e registro | acima de 150% da estimativa recorrente |
| Taxa de conclusão | etapas concluídas/iniciadas | abandono acima de 25% em unidade inicial |
| Pedidos de ajuda | contagem por tarefa | mais de 3 intervenções críticas por atividade |
| Erros de ambiente | classificação | erro recorrente em mais de 2 participantes |
| Ganho de aprendizagem | pré versus pós | ausência de melhoria prática |
| Autonomia | tarefa sem roteiro | incapacidade de repetir procedimento principal |
| Segurança | cenários adversariais | exposição de segredo ou ação indevida |
| Clareza | entrevista e rubrica | explicação depende do instrutor |
| Satisfação | escala e comentário | nota baixa sem causa identificada |
| Acessibilidade | checklist e relato | barreira impeditiva sem alternativa |

## Instrumentos

- formulário de perfil;
- teste diagnóstico;
- roteiro de observação;
- log de intervenções;
- ficha de tempo;
- rubrica transversal;
- questionário pós;
- entrevista final;
- registro de bugs pedagógicos.

## Categorias de problema

- P0 pedagógico: risco de segurança, dano ou instrução perigosa;
- P1 pedagógico: bloqueia a maioria dos alunos do público-alvo;
- P2 pedagógico: objetivo central não é atingido de forma confiável;
- P3 pedagógico: causa confusão ou atrito relevante;
- P4 pedagógico: melhoria editorial ou estética.

## Critérios para avançar de estágio

A classificação pode passar de **B — currículo técnico utilizável** para **C — curso técnico em piloto** quando:

- Trilha Zero mínima estiver implementada;
- instrumentos do piloto existirem;
- primeiro grupo iniciar formalmente;
- problemas forem registrados de forma rastreável.

Pode passar para **D — curso validado para público definido** somente quando:

- objetivos prioritários forem atingidos pelos públicos declarados;
- nenhum P0 ou P1 pedagógico permanecer aberto;
- P2s tiverem plano e prazo;
- tempos reais forem incorporados;
- acessibilidade tiver alternativas documentadas;
- resultados e limitações do piloto forem publicados.

## Ética e privacidade

- coletar apenas dados necessários;
- obter consentimento;
- não publicar nome ou desempenho individual sem autorização;
- não usar credenciais ou contas reais nos exercícios;
- permitir abandono sem penalidade;
- registrar conflitos de interesse;
- não prometer certificação ou emprego.

## Relatório final do piloto

Deve incluir:

1. perfil agregado da amostra;
2. versão e SHA do currículo;
3. ambiente utilizado;
4. resultados quantitativos;
5. achados qualitativos;
6. incidentes e bloqueios;
7. mudanças propostas;
8. limitações;
9. decisão de avanço ou repetição;
10. backlog priorizado.

## Limitação

Um piloto pequeno identifica falhas evidentes, mas não comprova eficácia para toda a população. Novas turmas e públicos exigem ciclos adicionais.
