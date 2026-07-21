---
id: course.zero-track.z08
title: Z08 — Primeiro workflow
lang: pt-BR
status: review
prerequisites: [course.zero-track.z07]
estimated_hours: 5
---

# Z08 — Primeiro workflow

## Para quem é

Pessoas que já conseguem executar e testar um projeto local e precisam aprender a encadear etapas com critérios explícitos.

## Resultados observáveis

Ao concluir, a pessoa consegue:

- diferenciar script, workflow e agente;
- modelar entrada, etapas, saída e falhas;
- definir pré-condições, stop conditions e critérios de sucesso;
- criar um workflow determinístico local;
- registrar evidências por etapa;
- evitar efeitos duplicados em retries;
- explicar quando um workflow não deve virar agente.

## Em linguagem simples

Um workflow é uma sequência combinada antes da execução. Cada etapa sabe o que recebe, o que entrega e quando deve parar.

## Explicação profissional

Workflow é uma orquestração explícita de estados e transições. Ele favorece previsibilidade, testes e auditoria. Um agente só é necessário quando a decisão dinâmica traz benefício mensurável superior ao fluxo determinístico.

## Modelo

```text
entrada validada
→ preparar
→ executar
→ verificar
→ registrar evidência
→ concluir ou parar
```

## Demonstração

```bash
python course/zero-track/scripts/first_workflow.py --self-test
python course/zero-track/scripts/first_workflow.py --demo
```

O workflow é local, sem rede, sem credenciais e com dados sintéticos.

## Prática guiada

1. Leia as etapas do script.
2. Execute o self-test.
3. Execute a demonstração.
4. Identifique entrada, estados, stop conditions e saída.
5. Repita a mesma operação e observe a proteção contra duplicidade.

## Prática independente

Adicione uma etapa opcional de revisão que não altere o efeito final. Inclua teste para sucesso, falha e repetição.

## Erros comuns

- chamar qualquer sequência de agente;
- omitir estado e critérios de parada;
- executar efeito antes de validar entrada;
- não distinguir retry de nova operação;
- esconder falhas em logs vagos;
- depender de serviço externo em exercício introdutório.

## Stop conditions

Pare quando a entrada for inválida, uma etapa obrigatória falhar, o orçamento de passos terminar ou houver tentativa de repetir efeito com conteúdo conflitante.

## Teste de segurança

O workflow deve rejeitar campos desconhecidos e nunca executar strings como comandos do sistema.

## Evidência mínima

- diagrama do fluxo;
- execução de sucesso;
- execução bloqueada por entrada inválida;
- repetição idempotente;
- teste automatizado;
- limitações documentadas.

## Critérios de conclusão

- [ ] Sei explicar por que o fluxo é determinístico.
- [ ] Cada etapa tem entrada e saída explícitas.
- [ ] Existe pelo menos uma falha testada.
- [ ] Retry não duplica o efeito.
- [ ] Consigo justificar por que ainda não preciso de um agente.

## Autoavaliação

Consigo transformar uma tarefa real simples em etapas testáveis sem delegar decisões desnecessárias a um modelo?