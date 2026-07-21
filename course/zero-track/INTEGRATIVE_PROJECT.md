---
id: course.zero-track.integrative-project
title: Projeto integrador da Trilha Zero
lang: pt-BR
status: review
---

# Projeto integrador da Trilha Zero

## Missão

Construir e documentar um pequeno sistema local que recebe uma solicitação estruturada, valida a entrada, executa somente ações read-only permitidas, registra evidências e recusa operações fora do escopo.

O projeto deve funcionar sem internet, sem chave de API e sem serviço pago.

## Entregáveis

- `README.md` do projeto;
- código Python 3.11+;
- dados sintéticos;
- testes positivos e negativos;
- exemplo de recusa;
- relatório de limitações;
- histórico Git com branches e commits compreensíveis;
- evidência sanitizada de execução.

## Escopo mínimo

O sistema deve possuir:

- objetivo explícito;
- entrada JSON validada;
- allowlist de intenções;
- pelo menos duas ferramentas read-only;
- orçamento máximo de passos;
- condição de parada;
- log estruturado;
- tratamento de erro;
- `--demo`;
- `--self-test`.

## Sugestões seguras

- explicar capacidades do próprio projeto;
- consultar catálogo sintético de módulos;
- verificar checklist de prontidão;
- resumir dados fictícios fornecidos no próprio código;
- validar estrutura de configuração sintética.

## Proibições

- acesso a conta real;
- leitura de `.env` ou arquivos pessoais;
- execução de comandos arbitrários;
- envio de mensagem;
- escrita, exclusão ou alteração fora da pasta do laboratório;
- rede;
- credencial real;
- coleta de dado pessoal.

## Procedimento sugerido

1. Escreva o contrato do sistema.
2. Defina não objetivos.
3. Liste ferramentas e permissões.
4. Defina entradas aceitas.
5. Crie testes antes ou junto da implementação.
6. Implemente o caminho mínimo.
7. Teste recusas e orçamento.
8. Registre limitações.
9. Execute em clone ou pasta limpa.
10. Revise a evidência antes de publicar.

## Testes obrigatórios

- missão permitida concluída;
- missão desconhecida recusada;
- campo extra rejeitado;
- orçamento inválido rejeitado;
- repetição segura ou resultado determinístico;
- ausência de rede e segredo;
- falha compreensível diante de entrada inválida.

## Rubrica

| Dimensão | Peso |
|---|---:|
| Contrato e escopo | 20% |
| Implementação e clareza | 20% |
| Testes e evidência | 20% |
| Segurança e recusas | 25% |
| Git e documentação | 15% |

## Gate de aprovação

O projeto não é aprovado quando:

- há segredo real;
- há acesso desnecessário;
- testes foram enfraquecidos;
- não existe recusa;
- o sistema pode executar ação destrutiva;
- a evidência não permite reprodução;
- a pessoa não consegue explicar o próprio código.

## Defesa curta

A pessoa deve explicar em até dez minutos:

- o problema resolvido;
- por que escolheu um agente ou workflow;
- quais ações foram negadas;
- como o sistema termina;
- qual risco permaneceu;
- o que seria necessário para uso real.

## Honestidade pedagógica

Concluir este projeto demonstra prontidão inicial para estudar engenharia de agentes. Não equivale a domínio profissional, produção ou senioridade.