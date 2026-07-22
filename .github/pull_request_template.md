## Objetivo e escopo

Explique o problema, o resultado esperado, o que mudou e o que ficou explicitamente fora do escopo.

- Issue relacionada:
- Tipo: `docs` | `feat` | `fix` | `lab` | `security` | `release`
- Risco: `baixo` | `médio` | `alto controlado`
- Base e dependências da pilha:

## Evidência reproduzível

- [ ] Registrei commit/SHA, versões, ambiente, entradas e saídas relevantes.
- [ ] Executei `python tests/validate_repository.py` no SHA final.
- [ ] Executei os testes, exemplos e laboratórios afetados.
- [ ] Comparei com baseline ou justifiquei formalmente a não aplicabilidade.
- [ ] Anexei evidência suficiente para outra pessoa reproduzir a mudança.
- [ ] CI verde pertence ao mesmo SHA informado neste PR.

## Qualidade pedagógica

- [ ] Mantive objetivos observáveis, prática ativa, avaliação e critérios de aprovação.
- [ ] Conteúdo educacional permanece `review` até validação humana e piloto aplicável.
- [ ] Não transformei ausência de evidência em alegação de eficácia pedagógica.
- [ ] Incluí troubleshooting, limitações e próxima ação do estudante quando aplicável.

## Segurança, privacidade e autoridade

- [ ] Não adicionei segredos, dados pessoais reais, credenciais ou permissões excessivas.
- [ ] Tenant, identidade, budgets, políticas e autoridade não ficam sob controle livre do modelo.
- [ ] Avaliei prompt injection, tools/MCP, memória, handoffs, egress, aprovação, idempotência e rollback quando aplicável.
- [ ] Timeout mutável não autoriza retry cego; estados ambíguos exigem reconciliação.
- [ ] Logs, traces, artefatos e quarentena foram verificados contra vazamento.
- [ ] Riscos altos ou críticos possuem tratamento, owner e evidência de fechamento.

## Compatibilidade e operação

- [ ] IDs, links, schemas e contratos permanecem compatíveis ou possuem migração documentada.
- [ ] Stop conditions, kill switch, rollback e caminho manual foram considerados.
- [ ] Mudanças de produção incluem readiness, canary, abort criteria e restauração quando aplicável.
- [ ] Nenhum hard gate foi compensado por média ou ignorado para obter CI verde.

## Conteúdo, referências e acessibilidade

- [ ] Priorizei fontes primárias e registrei versão/data quando necessário.
- [ ] Não inventei referências, resultados, certificações ou conformidade.
- [ ] Diagramas possuem alternativa textual; imagens possuem texto alternativo e licença/proveniência.
- [ ] Linguagem, headings, tabelas, links e ordem de leitura são acessíveis.
- [ ] Atualizei o manifesto i18n quando aplicável e preservei IDs canônicos.

## Declarações finais

- [ ] A mudança é coesa, pequena e usa Conventional Commits.
- [ ] Declarei conteúdo gerado ou substancialmente assistido por IA e realizei revisão humana.
- [ ] Limitações, riscos residuais e decisões `go/no-go` estão explícitos.
- [ ] Este PR permanece Draft enquanto houver bloqueador, dependência não integrada ou revisão pendente.
- [ ] Entendo que CI verde não implica merge, release, segurança absoluta ou prontidão pedagógica.

## Revisões humanas requeridas

Marque as revisões necessárias e indique responsáveis quando conhecidos.

- [ ] Técnica
- [ ] Pedagógica
- [ ] Segurança
- [ ] Privacidade
- [ ] Acessibilidade
- [ ] Licenciamento/marca
- [ ] Operação/release

## Decisão recomendada

`blocked` | `manual_review` | `ready_for_human_review`

Justificativa: