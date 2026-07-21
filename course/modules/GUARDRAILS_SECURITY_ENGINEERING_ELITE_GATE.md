---
id: course.gate.guardrails-security-elite
title: Gate Premium Elite — Guardrails & Security Engineering
lang: pt-BR
status: review
---

# Gate Premium Elite — Guardrails & Security Engineering

Este gate define as condições mínimas para promover o Módulo 08 de `review` para `stable`.

## Bloqueios absolutos

A promoção é proibida quando existir qualquer um dos itens abaixo:

- exfiltração de segredo;
- vazamento entre tenants;
- efeito sensível sem aprovação válida;
- aprovação aceita com hash divergente ou expirada;
- ampliação de autoridade ou confused deputy;
- chamada fora da allowlist;
- kill switch inoperante;
- efeito ambíguo sem reconciliação;
- evento de auditoria insuficiente para reconstruir o incidente;
- risco crítico ou alto sem tratamento e aprovação humana;
- teste crítico ausente, ignorado ou não executado.

## Evidências técnicas obrigatórias

- [ ] Threat model versionado com responsáveis.
- [ ] Fronteiras de confiança e ativos identificados.
- [ ] Deny-by-default e least privilege demonstrados.
- [ ] Policy enforcement ocorre fora do modelo.
- [ ] Schemas, identidade, tenant e escopo são validados.
- [ ] Aprovações vinculam identidade, ação, argumentos, preview, política e prazo.
- [ ] Segredos são bloqueados em prompts, outputs, logs e artefatos.
- [ ] Prompt injection direta, indireta e obfuscada é testada.
- [ ] Cross-tenant leakage rate é zero na suíte local.
- [ ] Confused deputy e handoff adulterado são bloqueados.
- [ ] Kill switch, contenção, rollback ou compensação são testados.
- [ ] Eventos de segurança são estruturados e redigidos.
- [ ] Hard gates bloqueiam release em violações críticas.
- [ ] CI está verde no SHA final.

## Evidências pedagógicas obrigatórias

- [ ] Diagnóstico inicial e final foram aplicados.
- [ ] LAB-801 foi executado por pessoa diferente do autor.
- [ ] O estudante consegue explicar por que prompt injection não é resolvida só com prompt.
- [ ] Prática guiada e independente foram concluídas.
- [ ] Simulação de incidente foi reproduzida.
- [ ] Rubrica específica foi aplicada de forma consistente.
- [ ] Dificuldades, falsos positivos e pedidos de ajuda foram registrados.

## Validação multiplataforma

- [ ] Windows.
- [ ] Linux.
- [ ] macOS.
- [ ] Python 3.11 ou superior.
- [ ] Execução local sem rede, API ou segredo.

## Acessibilidade

- [ ] Diagramas possuem descrição textual.
- [ ] Tabelas possuem cabeçalhos claros.
- [ ] Severidade não depende apenas de cor.
- [ ] Exemplos estão disponíveis como texto copiável.
- [ ] Estrutura de títulos é navegável por leitor de tela.
- [ ] Conteúdo audiovisual futuro possui legenda e transcrição.

## Revisões humanas

- [ ] Revisão técnica concluída.
- [ ] Revisão pedagógica concluída.
- [ ] Revisão humana de segurança concluída.
- [ ] Revisão de privacidade concluída.
- [ ] Revisão de acessibilidade concluída.
- [ ] Riscos residuais foram registrados.
- [ ] Nenhuma alegação de segurança absoluta ou conformidade não comprovada foi feita.

## Métricas mínimas

O relatório de validação deve incluir:

- attack success rate;
- blocked-before-tool rate;
- secret exposure rate;
- cross-tenant leakage rate;
- false positive rate;
- approval integrity rate;
- mean time to detect;
- mean time to contain;
- audit completeness;
- regression recurrence.

## Regra de promoção

O módulo só pode ser promovido para `stable` quando:

1. todos os bloqueios absolutos estiverem ausentes;
2. as evidências técnicas, pedagógicas e de acessibilidade estiverem anexadas;
3. o LAB-801 e a suíte adversarial forem reproduzidos;
4. revisões humanas estiverem registradas;
5. o CI estiver verde no mesmo SHA aprovado;
6. a integração receber aprovação humana explícita.

Até lá, o status correto permanece `review`.