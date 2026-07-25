---
id: governance.portal-security-baseline
title: Baseline de segurança do portal
lang: pt-BR
status: review
version: 0.2.0
---

# Baseline de segurança do portal

## Objetivo

Estabelecer um gate auditável para detectar padrões de segredos e impedir regressões no conjunto de vulnerabilidades npm conhecido, sem representar a linha de base como correção, aceitação de segurança ou certificação.

## Escopo

O workflow executa instalação reproduzível, examina arquivos rastreados por padrões de alto risco, registra `npm audit --json` e compara os resultados com uma linha de base temporária versionada.

## Linha de base temporária

A linha de base fica em `portal/security/npm-audit-baseline.json` e registra:

- contagens máximas conhecidas por severidade;
- identificadores dos advisories observados;
- data de registro;
- prazo obrigatório para nova revisão;
- justificativas e limitações.

Ela existe para impedir piora silenciosa enquanto dependências transitivas sem correção automatizada são investigadas. Não transforma vulnerabilidades conhecidas em achados resolvidos e não autoriza sua aceitação permanente.

## Hard gates

A execução falha quando identifica:

- chave privada em texto;
- token GitHub com padrão conhecido;
- chave OpenAI com padrão conhecido;
- chave de acesso AWS com padrão conhecido;
- atribuição genérica de segredo com valor não reconhecido como exemplo;
- qualquer vulnerabilidade crítica;
- aumento das contagens alta, moderada ou crítica em relação à linha de base;
- advisory novo não registrado na linha de base;
- linha de base com prazo de revisão expirado;
- ausência do evidence bundle.

## Evidências

O bundle retido contém:

- `security-baseline-report.json`;
- `npm-audit.json`;
- `npm-audit-baseline-used.json`;
- quantidade de arquivos rastreados examinados;
- achados sem exposição do valor potencialmente sensível;
- resumo de vulnerabilidades por severidade;
- advisories observados;
- regressões detectadas;
- prazo de revisão e limitações explícitas.

## Interpretação

Um resultado verde sustenta apenas que, nesta execução e segundo as regras implementadas:

1. os padrões bloqueantes definidos não foram encontrados nos arquivos rastreados examinados;
2. nenhuma vulnerabilidade crítica foi reportada;
3. não houve crescimento das contagens conhecidas;
4. nenhum advisory novo foi observado;
5. a linha de base ainda está dentro do prazo de revisão;
6. os relatórios de evidência foram produzidos.

Um resultado verde não significa que as vulnerabilidades conhecidas foram corrigidas.

## Tratamento obrigatório dos achados conhecidos

A equipe deve:

1. investigar atualizações seguras do Docusaurus e dependências transitivas;
2. revisar o impacto real dos advisories no contexto de build, desenvolvimento e runtime;
3. reduzir a linha de base sempre que um achado for removido;
4. nunca aumentar a linha de base sem justificativa, evidência e revisão humana;
5. renovar o prazo apenas após nova análise documentada;
6. priorizar correção sobre aceitação de risco.

## Limitações

Este controle não prova:

- ausência de segredos expostos;
- ausência de vulnerabilidades;
- segurança do código-fonte ou do ambiente de execução;
- cobertura equivalente a CodeQL, Semgrep, Gitleaks, OSV, Trivy, SAST ou DAST;
- segurança de autenticação, autorização, APIs ou agentes de IA;
- conformidade com OWASP, NIST, ISO ou qualquer certificação;
- autorização para merge, release ou produção.

Scanners por padrão e bancos de advisories podem produzir falsos positivos, falsos negativos ou classificações que dependem do contexto. O protocolo permanece em `status: review` até revisão humana e evolução dos controles.
