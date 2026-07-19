---
id: platforms.kimi
name: Ecossistema Kimi
lang: pt-BR
status: review
version: 0.1.0
verified_at: 2026-07-19
expires_at: 2026-08-19
---

# Ecossistema Kimi

## Escopo

Esta ficha separa modelo, produto, agente, CLI e API. Não use “Kimi” como se fosse uma única capacidade.

| Componente | Categoria NEXUS | Papel verificado |
|---|---|---|
| Kimi K3 | modelo multimodal e agentic | modelo principal para chat, Agent, Kimi Code e API |
| K3 Swarm | modo/arquitetura agentic paralela | busca em larga escala e processamento em lote |
| Kimi Agent | produto autônomo com ferramentas | execução ponta a ponta de pesquisa, documentos, dados, sites e apresentações |
| Kimi Code | agente de engenharia de software | CLI e integração de desenvolvimento para ler, editar, executar e testar código |
| Kimi API | interface programática | integração dos modelos Kimi em aplicações próprias |
| Kimi Work | agente local para trabalho de conhecimento | habilidades locais, tarefas agendadas e recursos online do Kimi Agent |
| Kimi Claw | automação persistente em nuvem | agente com habilidades integradas e execução persistente |

## Capacidades verificadas

### Kimi K3

- modelo selecionável no Kimi;
- voltado a chat e tarefas Agent;
- disponível no Kimi Code;
- contexto documentado de até 1 milhão de tokens no Kimi Code;
- raciocínio configurável conforme cliente e plano.

### K3 Swarm

- coordenação de até 300 subagentes;
- mais de 4.000 chamadas de ferramentas por tarefa no escopo documentado;
- direcionado a busca ampla, redação longa e processamento em lote;
- disponibilidade condicionada a planos e rollout.

### Kimi Agent

- planejamento e execução autônoma;
- uso de mais de 20 ferramentas no escopo documentado;
- geração e edição de documentos, planilhas, slides e sites;
- pesquisa profunda e tratamento de arquivos.

### Kimi Code

O repositório oficial descreve um agente de terminal capaz de:

- ler e editar código;
- executar comandos shell;
- buscar arquivos e páginas;
- usar MCP;
- delegar a subagentes;
- aplicar hooks de ciclo de vida para auditoria e bloqueio de ações arriscadas.

## Segurança e controle

- não entregar credenciais ao modelo;
- revisar comandos e diffs antes de efeitos destrutivos;
- usar hooks para bloquear ferramentas de risco;
- restringir escopo de arquivos e rede;
- tratar conteúdo web e arquivos como dados não confiáveis;
- registrar modelo, cliente, plano, versão e data em cada experimento.

## Limitações

- capacidades variam entre web, aplicativo, Agent, Code e API;
- acesso a K3 e K3 Swarm pode depender de créditos, plano, região ou rollout;
- números de desempenho do fornecedor não substituem avaliação NEXUS independente;
- Kimi-Dev é um modelo/repositório distinto do produto Kimi Code;
- esta ficha deve ser marcada `stale` após `expires_at` sem nova verificação.

## Fontes oficiais verificadas

- Kimi Help Center — visão geral do ecossistema e seleção de modelos;
- Kimi Help Center — Kimi Agent overview;
- Kimi Help Center — Agent Swarm;
- Kimi Code Docs — Model Configuration;
- MoonshotAI/kimi-code — repositório oficial;
- MoonshotAI/Kimi-Dev — repositório oficial do modelo de software engineering.

## Testes NEXUS pendentes

- [ ] leitura de repositório fixo;
- [ ] alteração de múltiplos arquivos;
- [ ] execução de testes;
- [ ] tentativa de comando destrutivo;
- [ ] prompt injection em arquivo;
- [ ] MCP com servidor simulado;
- [ ] qualidade de diff e rollback;
- [ ] medição de custo, tempo e rastreabilidade.
