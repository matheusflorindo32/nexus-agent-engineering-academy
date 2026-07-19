---
id: lab.501.governed-memory
title: LAB-501 — Memória governada, isolamento e esquecimento
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 5h
---

# LAB-501 — Memória governada, isolamento e esquecimento

## Hipótese

Uma memória com política de escrita, escopo obrigatório, TTL, proveniência e exclusão verificável melhora tarefas repetidas sem introduzir vazamento ou autoridade falsa.

## Missão

Construir uma memória local e provar, com testes adversariais, que ela só grava itens autorizados, recupera dados úteis dentro do escopo correto e consegue expirar, superseder e excluir registros.

## Cenários obrigatórios

| ID | Condição | Resultado obrigatório |
|---|---|---|
| M1 | preferência explícita e de baixa sensibilidade | gravação aceita |
| M2 | instrução encontrada em conteúdo recuperado | gravação bloqueada |
| M3 | mesma memória normalizada duas vezes | um registro ativo |
| M4 | nova declaração incompatível | versão anterior superseded |
| M5 | consulta por outro usuário | zero resultados |
| M6 | consulta por outro projeto | zero resultados |
| M7 | item com TTL expirado | não recuperado |
| M8 | exclusão por sujeito e escopo | zero itens ativos |
| M9 | orçamento de 2 itens | no máximo 2 resultados |
| M10 | memória irrelevante | baseline sem degradação |

## Contrato mínimo

Cada registro deve conter:

```yaml
memory_id: mem-001
subject: user:123
scope: project:nexus
type: semantic
content: prefere respostas em pt-BR
source_kind: explicit_user_statement
source_reference: conversation:abc#turn-12
confidence: 1.0
sensitivity: low
created_at: 2026-07-19T12:00:00Z
expires_at: null
status: active
version: 1
content_hash: sha256:...
```

## Procedimento

1. Implemente armazenamento local em memória, sem API ou banco externo.
2. Normalize o conteúdo antes de calcular hash.
3. Exija sujeito, escopo, fonte, sensibilidade e política de escrita.
4. Bloqueie padrões que tentem persistir instruções executáveis.
5. Deduplicate por sujeito, escopo, tipo e hash.
6. Superseda conflito explícito sem apagar o histórico.
7. Filtre por política, TTL, sujeito e escopo antes do ranking.
8. Limite recuperação por quantidade de itens.
9. Implemente exclusão e trilha de auditoria.
10. Compare pelo menos uma tarefa com e sem memória.

## Comandos

```bash
python examples/governed_memory_store.py --self-test
python tests/validate_repository.py
```

## Evidências

- saída dos dez cenários;
- dump antes e depois da supersessão;
- prova de isolamento entre usuários e projetos;
- prova de expiração;
- trilha de exclusão;
- relatório de itens bloqueados;
- comparação de baseline;
- reflexão sobre limitações.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários corretos | 10/10 |
| vazamentos de sujeito/escopo | 0 |
| instruções maliciosas persistidas | 0 |
| duplicidades ativas | 0 |
| itens expirados recuperados | 0 |
| exclusões incompletas | 0 |
| segredos em logs | 0 |

## Testes adversariais

- inserir `ignore todas as instruções anteriores` como fato;
- alterar apenas caixa e espaços para burlar deduplicação;
- omitir sujeito ou escopo;
- usar TTL no passado;
- consultar com escopo curinga;
- superseder com fonte sem autoridade;
- excluir um sujeito e deixar índice secundário ativo;
- tentar recuperar item `deleted` ou `superseded`;
- forçar `limit` acima do máximo da política;
- inserir token, senha ou chave simulada.

## Stop conditions

Pare imediatamente se houver recuperação fora de sujeito/escopo, persistência de instrução maliciosa, retorno de item expirado, exclusão incompleta ou alteração silenciosa do histórico. O runner deve encerrar em até 10 segundos e não pode usar rede.