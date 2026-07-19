---
id: lab.1101.idempotent-automation
title: LAB-1101 — Automação idempotente e compensável
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 5h
---

# LAB-1101 — Automação idempotente e compensável

## Hipótese

Um workflow orientado a eventos com chave idempotente, ledger de efeitos, controle de concorrência, retry limitado e compensação explícita processa reentregas e falhas parciais sem duplicar efeitos externos.

## Missão

Construir e testar uma automação que recebe eventos repetidos ou concorrentes, usa agente apenas em decisões ambíguas, exige aprovação para efeitos sensíveis e mantém trilha completa entre evento, decisão, aprovação e efeito.

## Cenários obrigatórios

| ID | Condição | Resultado esperado |
|---|---|---|
| A1 | evento único válido | um efeito confirmado |
| A2 | mesma chave reentregue | nenhum efeito duplicado |
| A3 | duas execuções concorrentes | apenas uma obtém o direito de efeito |
| A4 | timeout antes da confirmação | reconciliação determina o estado real |
| A5 | falha após efeito externo | retry consulta ledger antes de repetir |
| A6 | aprovação ausente | efeito sensível bloqueado |
| A7 | dependência indisponível | retry limitado e dead-letter explícita |
| A8 | payload divergente com mesma chave | conflito rejeitado e auditado |
| A9 | compensação possível | estado anterior restaurado uma única vez |
| A10 | compensação impossível | escalonamento manual com evidência |
| A11 | agente indisponível | caminho determinístico ou manual seguro |
| A12 | replay fora da retenção | rejeição ou processo formal de exceção |

## Contratos mínimos

```yaml
workflow_schema: nexus.automation.v1
idempotency:
  key: required
  payload_hash: required
  effect_ledger: append_only
concurrency:
  lock_scope: idempotency_key
  timeout_seconds: bounded
retries:
  attempts: bounded
  backoff: exponential_with_jitter
  dead_letter: required
approval:
  required_for: [sensitive_effect]
observability:
  correlation: [event_id, workflow_id, decision_id, approval_id, effect_id]
```

## Procedimento

1. Defina o estado do workflow e suas transições válidas.
2. Implemente chave idempotente e hash canônico do payload.
3. Registre intenção, tentativa, confirmação e compensação no ledger.
4. Simule reentrega sequencial e execução concorrente.
5. Injete timeout antes e depois do efeito externo.
6. Teste aprovação ausente, negada e expirada.
7. Force indisponibilidade da dependência até a dead-letter queue.
8. Teste payload divergente com a mesma chave.
9. Execute compensação segura e reconciliação.
10. Produza relatório de invariantes, limitações e riscos residuais.

## Evidências

- diagrama de estados;
- ledger antes e depois dos cenários;
- prova de efeito único sob reentrega e concorrência;
- logs correlacionados;
- registro de aprovação;
- conteúdo da dead-letter queue;
- demonstração de reconciliação e compensação;
- relatório de riscos residuais.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| efeitos duplicados | 0 |
| conflitos silenciosos de payload | 0 |
| retries ilimitados | 0 |
| efeitos sensíveis sem aprovação | 0 |
| estados sem correlação | 0 |
| compensações duplicadas | 0 |
| falhas parciais sem reconciliação | 0 |
| cenários corretos | 12/12 |

## Testes adversariais

- variar apenas a ordem das chaves do payload;
- reutilizar chave com payload semanticamente diferente;
- interromper o processo entre efeito e persistência local;
- expirar o lock durante a chamada externa;
- reentregar evento após compensação;
- forjar aprovação sem identidade válida;
- saturar retries simultâneos;
- responder sucesso tardio após timeout.

## Comando

Implemente a suíte na tecnologia escolhida e execute todos os cenários de forma reproduzível. O relatório deve registrar versões, seed, timestamps e resultados.

## Stop conditions

Interrompa se houver efeito duplicado, conflito de payload tratado como sucesso, retry ilimitado, efeito sensível sem aprovação, perda de correlação ou compensação não idempotente.
