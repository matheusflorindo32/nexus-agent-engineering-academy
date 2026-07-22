---
id: lab.501.governed-memory
title: LAB-501 — Memória governada, isolamento e esquecimento
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 6h
risk_level: high-controlled
module: course.module.05-memory-engineering
---

# LAB-501 — Memória governada, isolamento e esquecimento

> [!IMPORTANT]
> Memória útil não é memória ilimitada. O laboratório deve provar que o sistema sabe o que pode gravar, para quem, por quanto tempo, com qual fonte e como corrigir ou excluir.

## Hipótese

Uma memória com política de escrita, escopo obrigatório, TTL, proveniência, correção e exclusão verificável melhora tarefas repetidas sem introduzir vazamento, instrução persistente ou autoridade falsa.

## Missão

Construir uma memória local governada e provar que ela:

- grava somente itens autorizados;
- isola sujeito, tenant e projeto;
- preserva proveniência e versão;
- bloqueia instruções e dados inadequados;
- expira, supersede, corrige e exclui;
- limita recuperação por política;
- melhora uma tarefa em relação ao baseline sem memória.

## Resultado observável

Outra pessoa deve conseguir executar a suíte e confirmar zero vazamento, zero instrução maliciosa persistida, zero item expirado recuperado e exclusão verificável.

## Pré-condições

- [Módulo 05](../course/modules/05-memory-engineering/README.md) concluído;
- Python 3.11+;
- execução local, sem rede e com dados sintéticos;
- [gate dos laboratórios](LABS_PREMIUM_ELITE_GATE.md) lido.

## Baseline

Execute a tarefa-alvo sem memória. Registre qualidade, passos, contexto utilizado e erros. Depois compare com a memória governada usando exatamente os mesmos casos.

## Tipos de memória avaliados

| Tipo | Exemplo permitido | Risco principal |
|---|---|---|
| sessão | estado temporário da execução | mistura entre runs |
| episódica | decisão anterior com proveniência | retenção excessiva |
| semântica | preferência explícita e estável | desatualização |
| procedural | regra operacional aprovada | autoridade indevida |
| perfil | configuração declarada pelo sujeito | reidentificação |

Memória não deve transformar conteúdo recuperado em autoridade automática.

## Contrato mínimo

```yaml
memory_id: mem-001
tenant_id: tenant-demo
subject_id: user-123
project_id: nexus-demo
scope: project
memory_type: semantic
content: prefere respostas em pt-BR
source_kind: explicit_user_statement
source_reference: conversation-demo#turn-12
confidence: 1.0
sensitivity: low
created_at: 2026-07-22T00:00:00Z
expires_at: null
status: active
version: 1
content_hash: sha256:...
policy_version: memory-policy.v1
```

## Invariantes

- tenant, sujeito e projeto são obrigatórios;
- política é aplicada antes do ranking;
- instrução incorporada não é gravada como fato;
- segredos e credenciais simuladas são bloqueados;
- item expirado não é recuperado;
- conflito não é resolvido silenciosamente;
- item `deleted` ou `superseded` não retorna como ativo;
- exclusão remove índices ativos e gera trilha de auditoria;
- recuperação relevante não equivale a verdade ou autoridade.

## Cenários obrigatórios

| ID | Condição | Resultado obrigatório |
|---|---|---|
| M1 | preferência explícita de baixa sensibilidade | gravação aceita |
| M2 | instrução em conteúdo recuperado | gravação bloqueada |
| M3 | mesma memória normalizada duas vezes | um registro ativo |
| M4 | nova declaração incompatível e autorizada | anterior `superseded` |
| M5 | consulta por outro sujeito | zero resultados |
| M6 | consulta por outro projeto | zero resultados |
| M7 | item com TTL expirado | não recuperado |
| M8 | exclusão por sujeito e escopo | zero itens ativos |
| M9 | orçamento de 2 itens | no máximo 2 resultados |
| M10 | memória irrelevante | sem degradação frente ao baseline |
| M11 | fonte sem autoridade tenta corrigir | correção recusada |
| M12 | segredo simulado em entrada | gravação bloqueada e evento redigido |
| M13 | consulta com curinga de escopo | recusada |
| M14 | índice secundário após exclusão | nenhum item recuperável |

## Procedimento

1. Execute e registre o baseline sem memória.
2. Implemente armazenamento local.
3. Normalize conteúdo antes do hash.
4. Exija tenant, sujeito, projeto, fonte, sensibilidade e política.
5. Implemente allowlist de tipos graváveis.
6. Bloqueie instruções executáveis e segredos simulados.
7. Deduplicate por identidade, escopo, tipo e hash.
8. Implemente conflito, correção e supersessão.
9. Filtre por política, TTL e escopo antes do ranking.
10. Implemente limite de recuperação.
11. Implemente exclusão e tombstone auditável.
12. Execute os quatorze cenários.
13. Compare baseline e candidato.
14. Solicite reprodução independente de pelo menos cinco cenários.

## Testes adversariais

- inserir instrução disfarçada como preferência;
- alterar apenas caixa e espaços para burlar deduplicação;
- omitir tenant, sujeito ou projeto;
- usar TTL no passado;
- consultar com escopo curinga;
- superseder com fonte sem autoridade;
- excluir registro e manter índice secundário;
- recuperar item `deleted` ou `superseded`;
- forçar limite acima da política;
- inserir token ou senha simulada;
- combinar atributos para reidentificação;
- alterar `policy_version` sem migração.

## Métricas

| Métrica | Meta |
|---|---:|
| cenários corretos | 14/14 |
| vazamentos de escopo | 0 |
| instruções indevidas persistidas | 0 |
| duplicidades ativas | 0 |
| itens expirados recuperados | 0 |
| exclusões incompletas | 0 |
| correções não autorizadas | 0 |
| dados sensíveis em logs | 0 |
| benefício líquido frente ao baseline | demonstrado |
| cenários reproduzidos por outra pessoa | ≥ 5 |

## Comandos

```bash
python examples/governed_memory_store.py --self-test
python tests/validate_repository.py
```

## Evidências

- baseline sem memória;
- contrato e política de escrita;
- saída dos quatorze cenários;
- dump antes e depois de deduplicação e supersessão;
- prova de isolamento;
- prova de expiração;
- trilha de correção e exclusão;
- relatório de itens bloqueados;
- comparação com baseline;
- reprodução independente;
- riscos residuais.

## Critérios de aprovação

- 14/14 cenários corretos;
- nenhum vazamento entre escopos;
- nenhuma instrução ou segredo simulado persistido;
- nenhuma duplicidade ativa;
- nenhum item expirado recuperado;
- exclusão remove acesso por índices ativos;
- conflitos e correções preservam histórico;
- benefício da memória supera custo e risco no caso medido;
- evidências são reproduzíveis.

## Rubrica específica

| Nível | Evidência |
|---|---|
| insuficiente | memória sem escopo, TTL, proveniência ou exclusão confiável |
| funcional | gravação e recuperação básicas respeitam política |
| robusta | isolamento, conflito, expiração, exclusão e testes adversariais são comprovados |
| excelente | benefício líquido, reprodução independente, acessibilidade e riscos estão completos |

## Stop conditions

Pare imediatamente se houver recuperação fora do escopo, persistência de instrução indevida, retorno de item expirado, exclusão incompleta, alteração silenciosa do histórico ou exposição de dado sensível.

## Troubleshooting

| Sintoma | Verificação |
|---|---|
| duplicidade permanece | confira normalização e chave composta |
| item expirado aparece | aplique TTL antes do ranking |
| correção apaga histórico | use supersessão versionada |
| exclusão deixa resultado | revise índices e caches locais |
| contexto piora a resposta | reduza orçamento e compare com baseline |

## Acessibilidade

- explique campos do contrato em texto;
- use tabelas com cabeçalhos claros;
- disponibilize dumps e logs em formato textual;
- não use apenas cor para status de memória.

## Limpeza

Remova o armazenamento local e índices simulados, preserve apenas evidências redigidas e confirme que não restou dado de teste fora da pasta prevista.

## Limitações

O laboratório valida controles locais e cenários sintéticos. Não prova conformidade jurídica, privacidade absoluta nem funcionamento seguro em produção. O status permanece `review` até piloto e revisão humana.