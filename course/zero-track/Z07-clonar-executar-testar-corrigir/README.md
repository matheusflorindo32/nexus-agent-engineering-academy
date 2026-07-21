---
id: course.zero-track.z07
title: Z07 — Clonar, executar, testar e corrigir um projeto
lang: pt-BR
status: review
prerequisites: [course.zero-track.z06]
estimated_hours: 5
---

# Z07 — Clonar, executar, testar e corrigir um projeto

## Para quem é

Pessoas que já conhecem terminal, Git, Python, arquivos de configuração, APIs e segurança básica.

## Resultados observáveis

Ao concluir, a pessoa consegue:

- clonar um repositório;
- identificar README, dependências, testes e ponto de entrada;
- executar um exemplo em ambiente isolado;
- interpretar exit code e traceback;
- reproduzir uma falha antes de alterá-la;
- aplicar correção pequena em branch própria;
- provar a correção com teste e diff.

## Em linguagem simples

Corrigir sem reproduzir o erro é como trocar peças de um carro sem saber o defeito. Primeiro observe, depois reduza o problema, altere o mínimo e teste novamente.

## Fluxo profissional

```text
clonar → ler → preparar ambiente → executar baseline → reproduzir → formular hipótese → corrigir → testar → documentar
```

## Prática guiada

```bash
git clone https://github.com/matheusflorindo32/nexus-agent-engineering-academy.git
cd nexus-agent-engineering-academy
python tests/validate_repository.py
python -m unittest discover -s tests -p "test_*.py" -v
```

No Windows, use PowerShell. Em Linux e macOS, use o terminal do sistema. Não execute comandos com `sudo` ou como administrador sem necessidade explícita.

## Diagnóstico de falha

Registre:

1. comando exato;
2. diretório de execução;
3. versão do Python;
4. exit code;
5. mensagem principal;
6. menor cenário que reproduz;
7. hipótese;
8. evidência após correção.

## Prática independente

Crie uma branch de laboratório, introduza uma falha segura em um arquivo temporário, confirme que o teste detecta, reverta ou corrija e gere um pequeno relatório.

## Erros comuns

- alterar vários arquivos antes de entender a falha;
- ignorar o primeiro erro e reagir ao último efeito;
- executar no diretório errado;
- instalar dependências globalmente sem necessidade;
- afirmar que corrigiu sem teste de regressão;
- misturar refatoração ampla com correção pequena.

## Stop conditions

Pare quando:

- o comando pedir credencial inesperada;
- houver risco de apagar dados fora da pasta de laboratório;
- a correção exigir desativar teste ou validador;
- o comportamento não for reproduzível;
- você não conseguir explicar o diff.

## Teste de segurança

Diante de um teste vermelho, é proibido remover o teste apenas para deixar a CI verde. Documente a causa ou mantenha o bloqueio.

## Evidência mínima

- URL ou origem do repositório;
- branch de laboratório;
- comando de baseline;
- falha reproduzida ou exercício equivalente;
- diff pequeno;
- testes antes e depois;
- limitações.

## Critérios de conclusão

- [ ] Consigo clonar e localizar o ponto de entrada.
- [ ] Sei distinguir erro de ambiente e erro do código.
- [ ] Não enfraqueci testes.
- [ ] A correção é explicável e reproduzível.

## Autoavaliação

Outra pessoa consegue repetir meu diagnóstico apenas com o relatório e os comandos registrados?