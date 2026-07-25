---
id: governance.portal-security-baseline
title: Baseline de segurança do portal
lang: pt-BR
status: review
version: 0.1.0
---

# Baseline de segurança do portal

## Objetivo

Estabelecer um primeiro gate auditável para detectar padrões de segredos em arquivos rastreados e vulnerabilidades npm classificadas como altas ou críticas.

## Escopo

O workflow executa instalação reproduzível, examina arquivos rastreados por padrões de alto risco e registra o resultado de `npm audit --json`.

## Hard gates

A execução falha quando identifica:

- chave privada em texto;
- token GitHub com padrão conhecido;
- chave OpenAI com padrão conhecido;
- chave de acesso AWS com padrão conhecido;
- atribuição genérica de segredo com valor não reconhecido como exemplo;
- vulnerabilidade npm de severidade alta ou crítica;
- ausência do evidence bundle.

## Evidências

O bundle retido contém:

- `security-baseline-report.json`;
- `npm-audit.json`;
- quantidade de arquivos rastreados examinados;
- achados sem exposição do valor potencialmente sensível;
- resumo de vulnerabilidades por severidade;
- limitações explícitas.

## Interpretação

Um resultado verde sustenta apenas que, nesta execução e segundo as regras implementadas:

1. os padrões bloqueantes definidos não foram encontrados nos arquivos rastreados examinados;
2. o banco consultado pelo npm não reportou vulnerabilidades altas ou críticas nas dependências instaladas;
3. os relatórios de evidência foram produzidos.

## Limitações

Este controle não prova:

- ausência de segredos expostos;
- ausência de vulnerabilidades;
- segurança do código-fonte ou do ambiente de execução;
- cobertura equivalente a CodeQL, Semgrep, Gitleaks, OSV, Trivy, SAST ou DAST;
- segurança de autenticação, autorização, APIs ou agentes de IA;
- conformidade com OWASP, NIST, ISO ou qualquer certificação;
- autorização para merge, release ou produção.

Scanners por padrão podem produzir falsos positivos e falsos negativos. O protocolo permanece em `status: review` até revisão humana e evolução dos controles.
