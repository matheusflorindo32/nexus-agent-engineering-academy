---
id: governance.portal-rollback-rehearsal
title: Ensaio de rollback do portal
lang: pt-BR
status: review
version: 0.1.0
---

# Ensaio de rollback do portal

## Objetivo

Demonstrar, em ambiente controlado, que um artefato candidato pode ser substituído por um alvo anterior conhecido, mantendo identidade verificável, rotas críticas e evidência vinculada aos dois SHAs.

O ensaio não promove automaticamente uma release e não prova rollback externo na plataforma de hospedagem.

## Hipótese falsificável

Se o portal candidato precisar ser retirado, então o artefato correspondente ao SHA-base poderá ser reconstruído, servido e validado sem depender do estado do candidato.

A hipótese é rejeitada quando qualquer uma destas condições ocorrer:

- o alvo de rollback não puder ser reconstruído pelo lockfile versionado;
- a identidade publicada não corresponder ao SHA-base;
- uma rota crítica falhar após a troca;
- o manifesto do alvo estiver ausente ou incompleto;
- o processo candidato permanecer ativo e mascarar a troca;
- a evidência não permitir distinguir candidato e rollback.

## Escopo do ensaio

O workflow compara dois estados:

1. **candidato**: SHA de head do pull request;
2. **alvo de rollback**: SHA de base do pull request.

Cada estado é:

- obtido por checkout separado;
- instalado com `npm ci`;
- verificado por typecheck;
- compilado independentemente;
- identificado por `/.well-known/nexus-build.json`;
- servido por processo separado;
- submetido à mesma suíte de smoke tests.

## Sequência operacional

```text
checkout candidato
→ build candidato
→ manifesto candidato
→ preview candidato
→ smoke candidato
→ parada confirmada
→ preview alvo-base
→ smoke alvo-base
→ identidade do rollback confirmada
→ evidence bundle
```

## Hard gates

O ensaio deve falhar diante de:

- instalação não reproduzível;
- typecheck ou build com erro;
- identidade ausente;
- SHA de identidade divergente;
- rota crítica indisponível;
- processo anterior não encerrado;
- manifesto ou digest ausente;
- evidence bundle incompleto.

## Evidência mínima

O bundle precisa conter:

- SHAs candidato e alvo;
- versões de Node e npm;
- manifestos SHA-256 separados;
- digests dos manifestos;
- resultados de smoke separados;
- identidades publicadas separadas;
- logs dos dois servidores.

## Critério de aprovação

O ensaio é tecnicamente aprovado quando:

- ambos os builds são reproduzíveis;
- ambos os previews passam nas rotas críticas;
- a identidade do candidato corresponde ao head SHA;
- a identidade após rollback corresponde ao base SHA;
- os processos são encerrados de forma controlada;
- a evidência é gerada no mesmo run.

## Limitações e risco residual

Este ensaio não prova:

- rollback de domínio, DNS, CDN ou TLS;
- propagação real de cache;
- restauração de configuração externa;
- disponibilidade da plataforma;
- acessibilidade prática;
- ausência de regressões não cobertas pelos smoke tests;
- prontidão irrestrita para produção.

O rollback externo continua bloqueado até existir um projeto de hospedagem explicitamente associado ao NEXUS e um preview imutável aprovado.
