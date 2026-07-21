---
id: docs.pedagogy.pedagogical-audit
title: Auditoria pedagógica inicial da NEXUS
lang: pt-BR
status: draft
---

# Auditoria pedagógica inicial da NEXUS

## Parecer executivo

A NEXUS possui arquitetura técnica forte, progressão curricular coerente e preocupação incomum com segurança, avaliação, rastreabilidade e produção. Porém, no estado atual, ela deve ser classificada como **B — currículo técnico utilizável**, não como curso validado para qualquer pessoa.

A base atual atende melhor:

- pessoas com noções de terminal, Git e Python;
- estudantes de programação em nível introdutório ou intermediário;
- profissionais de software, automação, dados e IA;
- instrutores capazes de mediar conceitos complexos.

Ainda não atende de forma autônoma e confiável:

- iniciantes absolutos em computação;
- pessoas sem experiência com terminal;
- estudantes que nunca executaram código localmente;
- públicos que dependem de vídeo, legenda, transcrição ou instrução passo a passo;
- alunos que precisam de feedback automático ou solução comentada em todos os exercícios.

## Evidências positivas

1. A trilha principal possui progressão explícita do Módulo 00 ao 12.
2. Os módulos usam objetivos observáveis, projetos, laboratórios, checklists e critérios de excelência.
3. Segurança e rastreabilidade funcionam como critérios de bloqueio.
4. Há exemplos locais que evitam contas pagas e credenciais reais em etapas iniciais.
5. O currículo ensina engenharia de sistemas agentic, e não apenas uso superficial de prompts.

## Lacunas críticas

### P2-PED-001 — promessa de entrada sem pré-requisitos não corresponde à tarefa real

O Módulo 00 declara ausência de pré-requisitos, mas exige clonagem de repositório, navegação por terminal e execução de Python. Para iniciante absoluto, isso constitui pré-requisito implícito.

### P2-PED-002 — ausência de Trilha Zero implementada

Não há uma preparação completa cobrindo terminal, Git, Python, Markdown, JSON, YAML, HTTP, APIs, variáveis de ambiente e segurança básica.

### P2-PED-003 — conteúdo ainda se comporta parcialmente como documentação técnica

Existem boas explicações e exercícios, mas ainda falta padronização obrigatória de:

- analogia inicial;
- prática guiada;
- prática independente;
- solução comentada;
- erros comuns;
- feedback;
- diagnóstico inicial;
- glossário por módulo.

### P2-PED-004 — ausência de validação com alunos reais

CI verde comprova integridade técnica, não aprendizagem. Ainda não há piloto documentado com tempos, dúvidas, abandono, pré-teste, pós-teste e qualidade das entregas.

### P2-PED-005 — acessibilidade incompleta

Ainda não existe evidência consolidada de:

- instruções equivalentes para Windows, Linux e macOS;
- materiais de baixo consumo de dados;
- transcrições de vídeo;
- legendas;
- validação de contraste;
- navegação por teclado;
- diagramas sempre acompanhados de descrição textual.

## Classificação por público

| Público | Estado atual | Motivo |
|---|---|---|
| Iniciante absoluto | não recomendado sem mediação | faltam Trilha Zero e orientação operacional básica |
| Iniciante em programação | possível com esforço | exige autonomia para terminal, Git e Python |
| Intermediário técnico | recomendado | estrutura, exemplos e critérios já geram evolução real |
| Profissional avançado | recomendado como trilha e referência | forte em arquitetura, segurança, avaliação e produção |
| Empresa | útil para formação interna, ainda não pronto como pacote completo | faltam versão instrutor, piloto e critérios formais de certificação |

## Auditoria inicial dos módulos

| Módulo | Iniciante absoluto | Iniciante técnico | Intermediário | Avançado | Lacuna principal | Ação prioritária |
|---|---:|---:|---:|---:|---|---|
| 00 — Orientação | baixo | médio | alto | médio | terminal e Git implícitos | ligar à Trilha Zero e criar diagnóstico |
| 01 — Fundamentos | baixo | médio | alto | médio | alta densidade conceitual | adicionar analogias, glossário e prática guiada |
| 02 — Context Engineering | baixo | médio | alto | alto | conceitos abstratos | exemplos progressivos com corpus pequeno |
| 03 — Tool Engineering | baixo | médio | alto | alto | contratos e validação | starter code e erros comuns |
| 04 — Loop Engineering | baixo | médio | alto | alto | budgets, recovery e stop conditions | simulador visual e exercícios graduais |
| 05 — Memory Engineering | baixo | médio | alto | alto | governança e retenção | analogias, casos e solução comentada |
| 06 — Multi-Agent Systems | muito baixo | médio | alto | alto | coordenação e variância | baseline obrigatório e visualização de mensagens |
| 07 — Evaluation Engineering | muito baixo | médio | alto | alto | métricas e datasets | introdução estatística mínima e exemplos anotados |
| 08 — Guardrails e Security | baixo | médio | alto | alto | threat modeling | checklist guiado e laboratório seguro |
| 09 — Production Architecture | muito baixo | baixo | alto | alto | infraestrutura e rollback | trilha intermediária obrigatória |
| 10 — Observability Engineering | muito baixo | baixo | alto | alto | telemetria, métricas e incidentes | dashboard simples e interpretação guiada |
| 11 — Automação | baixo | médio | alto | alto | idempotência e compensação | laboratório visual com retries |
| 12 — Capstone | muito baixo | baixo | médio | alto | grande carga integradora | milestones, starter kit e banca simulada |

## Prioridades recomendadas

1. Criar a Trilha Zero.
2. Atualizar o contrato de módulo com estrutura pedagógica obrigatória.
3. Criar diagnóstico de entrada.
4. Definir matriz objetivo–atividade–avaliação–evidência.
5. Auditar todos os LABs e remover qualquer status indevido de disponibilidade.
6. Criar soluções comentadas e feedback mínimo.
7. Planejar e executar piloto com públicos diferentes.
8. Só então declarar prontidão para iniciantes absolutos.

## Gate de comunicação pública

Até que as lacunas P2-PED-001 a P2-PED-005 sejam tratadas, a apresentação pública recomendada é:

> Formação open source em engenharia de agentes de IA para pessoas com conhecimentos introdutórios de programação, Git e terminal.

Não usar ainda:

> Curso para qualquer pessoa, do zero absoluto ao avançado.

## Conclusão

A NEXUS já possui potencial para se tornar uma referência em português. O risco principal não é falta de conteúdo técnico. É tentar ampliar a promessa antes de transformar documentação e currículo em experiência pedagógica comprovada.
