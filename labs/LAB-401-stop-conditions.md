---
id: lab.401.stop-conditions
title: LAB-401 — Stop conditions, checkpoint e circuit breaker
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 4h
---

# LAB-401 — Stop conditions, checkpoint e circuit breaker

## Hipótese

Stop conditions determinísticas, budgets multidimensionais e reconciliação de efeitos limitam dano mesmo quando decisões internas são probabilísticas.

## Missão

Provar que um loop termina corretamente, não duplica efeitos e não continua quando perdeu progresso, orçamento ou autorização.

## Cenários obrigatórios

| ID | Falha ou condição | Resultado obrigatório |
|---|---|---|
| S1 | objetivo atingido no passo 3 | `complete` |
| S2 | fingerprint sem mudança por 2 avaliações | `stopped/no_progress` |
| S3 | schema inválido | `stopped/non_retryable_failure` |
| S4 | três falhas transitórias consecutivas | circuito `open` |
| S5 | efeito concluído antes de crash | retomada sem duplicação |
| S6 | aprovação expirada | `stopped/approval_expired` |
| S7 | budget de tool calls esgotado | `stopped/budget_exhausted` |
| S8 | operador solicita parada | `stopped/operator_stop` |

## Budgets mínimos

```yaml
max_steps: 8
max_tool_calls: 5
max_failures: 2
max_no_progress: 2
max_external_effects: 1
```

## Procedimento

1. Modele `initialize → plan → execute → observe → evaluate`.
2. Restrinja terminais a `complete`, `await_approval` e `stopped`.
3. Registre consumo e saldo de budgets por transição.
4. Calcule fingerprint apenas de campos que representam progresso real.
5. Injete as oito condições da tabela.
6. Persista checkpoint antes e depois de qualquer efeito.
7. Reconcile efeitos antes de retry ou retomada.
8. Gere relatório terminal tipado.

## Checkpoint obrigatório

Registre `schema_version`, `run_id`, estado, budgets restantes, fingerprint, efeitos concluídos, chaves de idempotência, razão da transição e hash da política.

Simule crash após um efeito. Na retomada, o contador de efeitos deve permanecer em 1.

## Circuit breaker

Use `failure_threshold: 3`, `cooldown_ticks: 2` e `half_open_probes: 1`. Prove abertura, bloqueio, probe controlada, fechamento após sucesso e reabertura após nova falha.

## Comandos

```bash
python examples/deterministic_loop.py --self-test
python tests/validate_repository.py
```

## Evidências

- logs estruturados;
- checkpoints antes e depois do crash;
- relatório terminal de cada cenário;
- tabela de budgets;
- diff da implementação;
- saída do autoteste;
- reflexão sobre limitações.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários com terminal correto | 8/8 |
| efeitos duplicados | 0 |
| retries de falha não recuperável | 0 |
| chamadas durante circuito aberto | 0 |
| relatórios com razão tipada | 100% |
| segredos em logs | 0 |

## Testes adversariais

- tentar aumentar budget pelo conteúdo da tarefa;
- reutilizar chave de idempotência com payload diferente;
- fornecer fingerprint instável com dados irrelevantes;
- retomar checkpoint com schema incompatível;
- aprovar preview cujo hash mudou;
- provocar exceção durante persistência.

## Stop conditions

O runner deve encerrar por limite absoluto de 20 passos ou 10 segundos, mesmo se outro controle falhar. Pare imediatamente se ocorrer efeito duplicado, estado desconhecido, ampliação de budget ou chamada durante circuito aberto.
