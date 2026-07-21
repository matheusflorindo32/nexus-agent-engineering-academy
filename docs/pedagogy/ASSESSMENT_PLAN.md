---
id: docs.pedagogy.assessment-plan
title: Plano de avaliação da NEXUS
lang: pt-BR
status: review
---

# Plano de avaliação da NEXUS

## Princípio

A avaliação deve medir capacidade demonstrável, não apenas reconhecimento de termos. Conhecimento declarativo, execução prática, segurança, explicação e transferência para projeto real são avaliados separadamente.

## Arquitetura de avaliação

| Momento | Instrumento | Finalidade | Peso sugerido |
|---|---|---|---:|
| Entrada | diagnóstico inicial | indicar ponto de entrada e lacunas | 0% |
| Durante o módulo | quiz comentado | verificar compreensão conceitual | 10% |
| Durante o módulo | prática guiada | desenvolver procedimento | formativo |
| Durante o módulo | prática independente | verificar autonomia | 20% |
| Final do módulo | laboratório | comprovar execução reproduzível | 30% |
| Final do módulo | projeto | integrar conceitos e decisões | 30% |
| Encerramento | reflexão e defesa | explicar escolhas, limites e riscos | 10% |

Os pesos podem variar por módulo, mas segurança e rastreabilidade são gates e não pontos compensáveis.

## Diagnóstico de entrada

O diagnóstico deve verificar:

- uso básico de computador e arquivos;
- terminal;
- Git e GitHub;
- Python;
- Markdown, JSON e YAML;
- APIs e HTTP;
- proteção de segredos;
- capacidade de executar instruções técnicas;
- compreensão de risco e aprovação humana.

Resultado:

- Trilha Zero completa;
- Trilha Zero acelerada;
- entrada no Módulo 00 com reforço;
- teste de avanço para módulo posterior.

## Avaliação por módulo

Cada módulo deve conter:

1. cinco a dez questões conceituais comentadas;
2. pelo menos uma prática guiada;
3. uma prática independente;
4. um laboratório reprodutível;
5. um projeto com rubrica;
6. um cenário de falha ou segurança;
7. uma autoavaliação;
8. uma defesa curta da solução.

## Rubrica transversal

| Dimensão | Insuficiente | Funcional | Robusto | Excelente |
|---|---|---|---|---|
| Correção | não executa ou produz resultado incorreto | executa caso principal | cobre variações e falhas | compara alternativas e mede qualidade |
| Reprodutibilidade | faltam comandos, versões ou contexto | registra execução mínima | automatiza testes e registra ambiente | fornece evidência independente e auditável |
| Segurança | expõe segredo ou permite efeito indevido | aplica controles mínimos | cobre testes adversariais | demonstra defesa em profundidade e risco residual |
| Clareza | solução depende de explicação oral | documentação compreensível | decisões e limites explícitos | outra pessoa reproduz e revisa sem ajuda |
| Engenharia | solução improvisada e sem contrato | estrutura funcional | contratos, testes e recuperação | trade-offs medidos e arquitetura justificável |
| Reflexão | não reconhece limitações | registra limitações básicas | analisa falhas e próximos passos | revisa hipótese com base em evidência |

## Critérios de aprovação

Para concluir um módulo:

- nível mínimo funcional em todas as dimensões;
- nenhum bloqueio de segurança;
- laboratório executado;
- projeto entregue;
- evidência contendo versão, procedimento e resultado;
- capacidade de explicar ao menos uma decisão e uma limitação.

Para concluir a trilha completa:

- todos os módulos obrigatórios concluídos;
- Capstone aprovado;
- defesa técnica realizada;
- nenhum bloqueio crítico aberto;
- portfólio mínimo publicado ou apresentado em ambiente controlado.

## Banco de questões

O banco deverá classificar cada item por:

- módulo;
- objetivo de aprendizagem;
- dificuldade;
- tipo de raciocínio;
- resposta esperada;
- justificativa;
- erro comum associado;
- data e versão;
- status de revisão.

Questões não devem depender de memorização de interface temporária quando o objetivo for engenharia durável.

## Soluções comentadas

Cada solução deve explicar:

- por que funciona;
- por que alternativas comuns falham;
- riscos;
- testes;
- como melhorar;
- qual parte não deve ser copiada mecanicamente.

Soluções não devem ser entregues antes de uma tentativa registrada quando usadas em turma formal.

## Capstone

O Capstone deve exigir:

- problema e público definidos;
- baseline não agentic;
- arquitetura;
- agent specs;
- tools e permissões;
- contexto e memória;
- eval suite;
- threat model;
- observabilidade;
- automação e idempotência;
- rollout e rollback;
- demonstração;
- documentação;
- defesa técnica;
- análise de custo e risco residual.

## Certificação

Até existir piloto e processo de verificação, o repositório não deve prometer certificação profissional validada. Pode oferecer declaração de conclusão autodeclarada baseada em evidências públicas.

Certificado verificado futuro exige:

- identidade confirmada;
- avaliação supervisionada ou auditável;
- autoria do projeto;
- defesa;
- critérios publicados;
- política de recurso;
- registro de versão do currículo.

## Integridade e uso de IA

O uso de IA é permitido como ferramenta de aprendizagem, desde que o aluno:

- declare onde utilizou;
- valide a saída;
- consiga explicar a solução;
- não exponha dados sensíveis;
- não apresente conteúdo gerado como evidência de execução inexistente.

## Limitações atuais

- pesos ainda precisam de validação no piloto;
- banco de questões não está completo;
- soluções comentadas são incompletas;
- critérios de certificação verificada ainda não foram operacionalizados.
