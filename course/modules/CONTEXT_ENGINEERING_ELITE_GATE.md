---
id: course.gate.context-engineering-elite
title: Gate Premium Elite — Context Engineering
lang: pt-BR
status: review
---

# Gate Premium Elite — Context Engineering

Este gate define as condições mínimas para promover o Módulo 02 de `review` para `stable`.

## Conteúdo

- [ ] Público, pré-requisitos e resultado final estão explícitos.
- [ ] Explicação simples, profissional e implementável foi revisada.
- [ ] Glossário, mapa visual, exemplo mínimo e demonstração estão presentes.
- [ ] Prática guiada e independente usam o mesmo contrato de avaliação.
- [ ] Projeto e rubrica específica estão completos.

## Execução

- [ ] `examples/context_retriever.py --demo` executa em clone limpo.
- [ ] O LAB-201 executa com fixtures versionadas.
- [ ] Nenhuma chave de API ou conta paga é obrigatória.
- [ ] Comandos foram testados em Windows, Linux e macOS.
- [ ] Links internos e frontmatter passam no validador.

## Segurança

- [ ] Instruções incorporadas não ampliam autoridade.
- [ ] Há teste negativo com conteúdo adversarial.
- [ ] Logs não expõem segredos ou dados pessoais.
- [ ] Ausência de evidência produz abstention.
- [ ] Conflitos entre fontes permanecem visíveis.
- [ ] Retenção e expiração estão definidas.
- [ ] Risco residual está documentado.

## Pedagogia

- [ ] O diagnóstico inicial foi testado com alunos.
- [ ] Tempo mediano real foi comparado à estimativa de 10 horas.
- [ ] Pedidos de ajuda e pontos de abandono foram analisados.
- [ ] Pelo menos um iniciante técnico e um intermediário concluíram o projeto.
- [ ] Feedback do piloto gerou revisão documentada.

## Acessibilidade

- [ ] Diagramas possuem descrição textual equivalente.
- [ ] Tabelas não dependem de cor.
- [ ] Comandos têm saída esperada e interpretação de erro.
- [ ] A navegação é possível por teclado.
- [ ] Evidências visuais possuem alternativa textual.

## Gate de comunicação

Antes da validação real, é permitido afirmar:

> “Módulo implementado em padrão Premium Elite e em revisão pedagógica.”

Não é permitido afirmar:

- “validado para qualquer iniciante”;
- “à prova de prompt injection”;
- “segurança garantida”;
- “adequado a produção sem revisão”.

## Aprovação

A promoção para `stable` exige:

1. CI integralmente verde;
2. piloto documentado;
3. revisão humana pedagógica;
4. revisão humana de segurança;
5. ausência de bloqueios críticos ou altos sem mitigação.