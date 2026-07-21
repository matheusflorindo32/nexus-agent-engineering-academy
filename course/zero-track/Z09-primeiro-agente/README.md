---
id: course.zero-track.z09
title: Z09 — Primeiro agente simples
lang: pt-BR
status: review
prerequisites: [course.zero-track.z08]
estimated_hours: 5
---

# Z09 — Primeiro agente simples

## Para quem é

Para quem concluiu Z00–Z08 e já consegue executar Python, interpretar erros, usar Git, validar dados e explicar um workflow determinístico.

## Resultado demonstrável

Ao concluir, a pessoa consegue executar, explicar e testar um agente local, read-only e determinístico que:

- recebe uma missão limitada;
- usa somente ferramentas permitidas;
- registra decisões;
- respeita orçamento de passos;
- recusa entrada fora de escopo;
- para de forma explícita;
- não usa rede, chave de API ou dado pessoal.

## Por que isso importa

Um agente não é apenas um prompt. É um sistema que observa uma entrada, decide entre ações permitidas, usa ferramentas sob política e termina com evidência. Antes de usar modelos externos, é mais seguro aprender o contrato do agente em um ambiente local e reproduzível.

## Diagnóstico inicial

Explique, com suas palavras:

1. a diferença entre script, workflow e agente;
2. por que um agente precisa de stop conditions;
3. por que uma ferramenta deve ter permissões explícitas;
4. o que acontece quando o orçamento de passos termina.

Caso não consiga responder, revise Z06 e Z08.

## Explicação em três camadas

### Camada 1 — linguagem simples

Um agente é como um assistente que recebe uma missão, escolhe entre poucas ações autorizadas, verifica o resultado e sabe quando parar.

### Camada 2 — explicação profissional

Neste curso, um agente possui objetivo, estado, ferramentas, política de decisão, orçamento, condições de parada, recusas e evidência. Autonomia sem limite não é uma competência; é um risco.

### Camada 3 — implementação

O exemplo `first_agent.py` usa:

- entrada JSON validada;
- allowlist de intenções;
- ferramenta local read-only;
- política determinística;
- limite de passos;
- log estruturado;
- resultado final com status e justificativa.

## Mapa mental

```text
missão
  ↓
validar entrada
  ↓
classificar intenção
  ↓
selecionar ferramenta permitida
  ↓
executar ação read-only
  ↓
registrar evidência
  ↓
finalizar ou recusar
```

## Demonstração

```bash
python course/zero-track/scripts/first_agent.py --demo
python course/zero-track/scripts/first_agent.py --self-test
```

A demonstração não acessa internet, arquivos pessoais, variáveis de ambiente ou serviços externos.

## Prática guiada

1. Execute `--demo`.
2. Identifique a missão recebida.
3. Localize a ferramenta escolhida.
4. Verifique quantos passos foram usados.
5. Explique por que o agente encerrou.
6. Execute `--self-test`.
7. Registre o resultado em `evidence/z09-agent-report.md`.

## Prática independente

Crie uma nova intenção segura, como `list_capabilities`, mantendo:

- ferramenta read-only;
- entrada estritamente validada;
- resposta sem dados pessoais;
- teste positivo;
- teste de recusa;
- orçamento máximo de três passos.

## Erros comuns

- chamar qualquer script com loop de agente;
- permitir ferramenta sem contrato;
- misturar decisão e execução sem log;
- não limitar passos;
- usar entrada livre sem validação;
- esconder falhas com `except Exception: pass`;
- tratar resposta plausível como evidência de correção.

## Stop conditions

Pare a atividade quando:

- o código tentar acessar rede;
- surgir solicitação para ler segredo, `.env` ou arquivo pessoal;
- uma ferramenta puder escrever ou excluir dados sem aprovação;
- o agente entrar em repetição;
- um teste falhar sem causa compreendida.

## Teste de segurança

O agente deve recusar:

- intenção desconhecida;
- campos extras;
- orçamento inválido;
- pedido de leitura de credenciais;
- tentativa de executar comando arbitrário.

## Evidência mínima

Entregue:

- saída do `--self-test`;
- explicação do contrato do agente;
- um diagrama simples do fluxo;
- uma recusa analisada;
- uma limitação real do exemplo.

## Critérios de conclusão

- [ ] Diferencio agente de workflow.
- [ ] Explico objetivo, ferramenta, política, orçamento e parada.
- [ ] Consigo executar e testar o exemplo.
- [ ] Consigo demonstrar uma recusa.
- [ ] Não usei chave real, rede ou dado pessoal.
- [ ] Documentei limitações.

## Autoavaliação

Classifique-se de 0 a 3:

- 0 — apenas li;
- 1 — executei com ajuda;
- 2 — executei e expliquei;
- 3 — alterei com segurança e mantive os testes verdes.

Avance para a avaliação de saída somente com nível 2 ou 3.