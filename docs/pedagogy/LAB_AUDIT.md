---
id: docs.pedagogy.lab-audit
title: Auditoria pedagógica dos laboratórios
lang: pt-BR
status: review
---

# Auditoria pedagógica dos laboratórios

## Escopo

O catálogo atual possui 12 laboratórios canônicos, do LAB-000 ao LAB-1101. O LAB-1201 permanece planejado e não deve ser anunciado como disponível.

## Diagnóstico geral

O catálogo é tecnicamente coerente e cobre a progressão curricular. Porém, o contrato atual de LAB ainda é insuficiente para garantir experiência pedagógica completa: exige objetivo, ambiente, entradas, procedimento, métricas, stop conditions e reflexão, mas não exige starter code, solução comentada, erros comuns, rubrica, acessibilidade ou modelo de relatório.

## Critérios de auditoria

Cada laboratório deve ser classificado em relação a:

- objetivo observável;
- hipótese testável;
- público e pré-requisitos;
- ambiente seguro;
- starter code;
- fixtures sintéticas;
- procedimento reproduzível;
- comandos copiáveis;
- resultado esperado;
- critérios de sucesso;
- stop conditions;
- cleanup;
- testes;
- solução de referência;
- explicação da solução;
- erros comuns;
- extensão avançada;
- rubrica;
- acessibilidade;
- modelo de relatório;
- vínculo com objetivo de aprendizagem.

## Matriz inicial

| LAB | Tema | Estado editorial | Risco pedagógico principal | Ação prioritária |
|---|---|---|---|---|
| LAB-000 | orientação do repositório | implementado | pressupõe terminal e Git | adicionar caminho guiado para iniciante e solução comentada |
| LAB-101 | contrato de agente | implementado | pode virar exercício apenas documental | incluir casos, baseline e revisão de recusas |
| LAB-201 | seleção de contexto | implementado | métricas podem parecer abstratas | incluir corpus pequeno, resultado esperado e análise de erro |
| LAB-301 | fronteira de ferramenta | implementado | risco de copiar código sem compreender permissões | exigir threat scenario, testes negativos e reconciliação |
| LAB-401 | stop conditions | implementado | loops podem ser tratados só conceitualmente | incluir simulação executável de runaway e budget |
| LAB-501 | memória governada | implementado | retenção e exclusão podem não ser observáveis | incluir expiração, correção, deleção e proveniência |
| LAB-601 | coordenação multiagente | implementado | complexidade sem baseline | comparar equipe com agente único usando mesma tarefa |
| LAB-701 | avaliação e regressão | implementado | risco de métricas desconectadas de decisão | exigir versão de dataset e critério de promoção |
| LAB-801 | security red team | implementado | conteúdo adversarial exige containment forte | explicitar ambiente isolado, proibições e cleanup |
| LAB-901 | production readiness | implementado | pode depender de infraestrutura externa | criar modo local simulado e plano de rollback |
| LAB-1001 | observabilidade | implementado | logs podem expor segredo ou não ser acionáveis | validar todos os canais e owner de alerta |
| LAB-1101 | automação idempotente | implementado | duplicidade pode ser demonstrada sem falha realista | incluir retry, crash, reconciliação e compensação |
| LAB-1201 | Capstone | planejado | inexistência pode ser confundida com oferta ativa | manter marcado como planejado até escopo aprovado |

## Gates para considerar um LAB pronto

Um laboratório só pode ser anunciado como pronto quando:

1. funciona em ambiente documentado;
2. usa dados e credenciais sintéticos;
3. possui procedimento e resultado esperado;
4. inclui pelo menos um teste negativo;
5. possui solução de referência comentada;
6. possui rubrica;
7. gera evidência versionada;
8. inclui stop conditions e cleanup;
9. possui alternativa acessível quando depende de elemento visual;
10. foi executado por pessoa que não o escreveu.

## Backlog recomendado

### Prioridade P1 pedagógica

- criar solução comentada e guia de recuperação para LAB-000;
- reforçar containment e proibições no LAB-801;
- garantir modo local sem serviços pagos para LAB-901;
- manter LAB-1201 fora da lista de disponíveis.

### Prioridade P2 pedagógica

- adicionar starter code e fixtures uniformes;
- padronizar resultado esperado e testes negativos;
- criar rubrica e modelo de relatório para todos;
- vincular cada LAB à matriz de resultados de aprendizagem.

### Prioridade P3 pedagógica

- extensões avançadas;
- desafios opcionais;
- vídeos curtos e transcrições;
- exemplos equivalentes para Windows, Linux e macOS.

## Parecer

Os LABs existentes formam uma boa base técnica, mas o conjunto ainda não pode ser tratado como laboratório educacional validado para qualquer público. O estado atual é **implementado tecnicamente, com maturidade pedagógica desigual**.
