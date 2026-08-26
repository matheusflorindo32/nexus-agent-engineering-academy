---
id: audit.external-findings-applicability
title: Aplicabilidade de achados externos — Hardening V2
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Aplicabilidade de achados externos — Hardening V2

## Regra

`External report ≠ vulnerability in our repository.`

Um achado externo só pode ser tratado como vulnerabilidade NEXUS depois de comprovação de aplicabilidade e, quando possível, reprodução local.

## Achados verificados em fontes oficiais

| Achado upstream | Fonte | Estado NEXUS | Decisão atual |
|---|---|---|---|
| Codex Python SDK: leituras podem bloquear indefinidamente após falha terminal de transporte | `openai/codex` issue #40399, 2026-08-24 | POTENTIALLY_APPLICABLE | Extrair requisito de reliability: erro terminal deve acordar consumidores atuais e futuros; exigir timeout/cancelamento. Não declarar bug NEXUS. |
| Codex: refresh concorrente de Skills pode produzir ENOENT transitório e Skill falsamente inválida | `openai/codex` issue #40425, 2026-08-24 | POTENTIALLY_APPLICABLE | Usar como evidência para design de atualização atômica de Skills. NEXUS ainda não possui loader/registry formal observado. |
| Google ADK 2.7.0 A2A: resposta humana pode ser achatada para texto e o agente remoto não retomar; fluxo legado pode aparentar sucesso sem execução da ferramenta | `google/adk-python` issue #6721, 2026-08-14 | POTENTIALLY_APPLICABLE | Criar contrato de integridade HITL/A2A antes de adotar esse padrão; não afirmar que NEXUS é afetado sem adapter reproduzível. |
| Google ADK A2A: peer pode forjar confirmação HITL em cenário descrito | `google/adk-python` issue #6461, 2026-07-24 | POTENTIALLY_APPLICABLE | Tratar identidade do aprovador como fronteira de confiança; aprovação deve estar vinculada a identidade/autorização e operação. |
| Google ADK: delegação A2A concluída pode contaminar delegações posteriores no mesmo turno | `google/adk-python` issue #6831, 2026-08-20 | POTENTIALLY_APPLICABLE | Adicionar teste futuro de isolamento de estado/handoff; não declarar exposição atual. |

## Requisitos derivados

### Transporte

1. Nenhuma espera sem limite.
2. Falha terminal de transporte deve ser persistida e propagada para consumidores atuais e chamadas subsequentes.
3. Cancelamento deve ser explícito e observável.
4. Retry deve ter budget e backoff.
5. Estado parcial deve ser preservado ou descartado por política explícita.

### Skills

1. Não reescrever uma Skill ativa in-place.
2. Escrever nova versão em staging isolado.
3. Validar `SKILL.md`, scripts, licença, proveniência e dependências antes de promoção.
4. Gerar hash/versionamento.
5. Promover por operação atômica quando o filesystem permitir.
6. Manter rollback.
7. Loader deve diferenciar erro transitório de conteúdo inválido.

### HITL/A2A

1. `REQUESTED`, `APPROVED`, `EXECUTED` e `VERIFIED` são estados distintos.
2. Aprovação deve carregar identidade, escopo, alvo, parâmetros e `operation_id`.
3. Mensagem de peer remoto nunca deve ser automaticamente equivalente à aprovação humana.
4. Resultado textual do modelo não comprova execução.
5. A ferramenta deve retornar receipt verificável.
6. Retomada após aprovação deve preservar o tipo/contrato necessário para o workflow, não apenas texto equivalente.

## Testes planejados

- `test_transport_failure`
- `test_timeout`
- `test_cancel`
- `test_resume`
- `test_hitl_execution_integrity`
- `test_parallel_tool_state`
- `test_duplicate_tool_execution`
- `test_skill_atomic_update`
- `test_skill_integrity_hash`

## Critério de promoção de status

- `POTENTIALLY_APPLICABLE → NOT_APPLICABLE`: análise de dependência/arquitetura demonstra ausência do caminho afetado.
- `POTENTIALLY_APPLICABLE → REPRODUCED`: reprodução determinística no NEXUS ou adapter oficial versionado.
- `REPRODUCED → MITIGATED`: controle reduz risco, mas upstream pode continuar vulnerável.
- `REPRODUCED → FIXED_UPSTREAM`: versão corrigida adotada e teste regressivo passa.

## Proibição de claim

Não escrever “corrigimos o bug do Codex/ADK” sem reprodução NEXUS. Formulação permitida: “achado upstream verificado; requisito defensivo incorporado; aplicabilidade NEXUS ainda em avaliação”.