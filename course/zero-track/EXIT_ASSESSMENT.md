---
id: course.zero-track.exit-assessment
title: Avaliação de saída da Trilha Zero
lang: pt-BR
status: review
---

# Avaliação de saída da Trilha Zero

## Objetivo

Verificar se a pessoa possui autonomia mínima para iniciar o Módulo 00 sem depender de instruções passo a passo em todas as ações.

Esta avaliação não é certificação profissional e não comprova domínio de engenharia de agentes.

## Formato

A avaliação contém quatro blocos:

1. fundamentos e ambiente;
2. execução e depuração;
3. segurança e evidência;
4. primeiro agente.

Tempo sugerido: 90 a 150 minutos.

## Bloco A — fundamentos e ambiente

A pessoa deve demonstrar que consegue:

- identificar sistema operacional, Python e Git;
- navegar em uma pasta de laboratório;
- criar, mover e remover arquivo de teste;
- explicar Git versus GitHub;
- criar branch e commit com mensagem compreensível.

## Bloco B — execução e depuração

A pessoa recebe um script pequeno com uma falha sintética e deve:

- reproduzir a falha;
- interpretar o traceback;
- formular uma hipótese;
- corrigir o mínimo necessário;
- executar os testes;
- registrar o que mudou.

Não é permitido remover testes, suprimir exceções ou alterar o resultado esperado para fabricar sucesso.

## Bloco C — segurança e evidência

A pessoa deve:

- identificar pelo menos quatro locais onde segredos podem vazar;
- preparar um `.env.example` sem segredo real;
- demonstrar uma recusa diante de pedido perigoso;
- produzir evidência sem username, home path, token ou conteúdo pessoal;
- explicar quando revogar ou rotacionar uma credencial.

## Bloco D — primeiro agente

Execute:

```bash
python course/zero-track/scripts/first_agent.py --self-test
python course/zero-track/scripts/first_agent.py --demo
```

Depois responda:

1. Qual é o objetivo do agente?
2. Quais ferramentas ele pode usar?
3. Qual é o orçamento máximo?
4. O que acontece com uma missão fora da allowlist?
5. Qual limitação impede que esse exemplo seja chamado de agente inteligente completo?

## Rubrica

| Critério | Insuficiente | Funcional | Robusto |
|---|---|---|---|
| Ambiente | não executa sem ajuda total | executa com pequenas consultas | executa e explica versões e caminhos |
| Git | não cria histórico válido | cria branch e commit | explica histórico e riscos |
| Python | não reproduz a falha | corrige e testa | explica causa e impacto |
| Segurança | expõe ou ignora segredos | evita segredo real | demonstra prevenção e resposta |
| Agente | executa sem compreender | explica contrato básico | modifica com segurança e mantém testes |
| Evidência | incompleta ou sensível | suficiente | reproduzível e sanitizada |

## Critérios de aprovação

A pessoa é considerada pronta para o Módulo 00 quando:

- não possui nenhum critério em nível insuficiente;
- alcança pelo menos nível funcional em todos os critérios;
- passa o self-test do agente;
- documenta uma recusa e uma limitação;
- não expõe dados sensíveis;
- conclui o projeto integrador.

Segurança e integridade da evidência são critérios de bloqueio.

## Resultado possível

- `REVISAR`: existem lacunas que exigem retorno às unidades indicadas;
- `PRONTO_COM_APOIO`: pode avançar com checklist e acompanhamento;
- `PRONTO`: demonstra autonomia mínima consistente.

A classificação final deve registrar evidências, não apenas uma nota.