---
id: lab.000.repository-orientation
title: LAB-000 — Orientação no repositório
lang: pt-BR
status: review
version: 0.3.0
estimated_time: 60min
risk_level: low
---

# LAB-000 — Orientação no repositório

> [!IMPORTANT]
> Este laboratório valida se uma pessoa sem conhecimento tácito consegue navegar, executar o validador e reconstruir a relação entre conceito, módulo, laboratório, template e evidência.

## Hipótese

Uma arquitetura com IDs estáveis, índices claros e links relativos permite que uma pessoa encontre conceito → módulo → laboratório → template → evidência em até 60 minutos, sem orientação oral do autor.

## Missão

Validar a navegabilidade e a reprodutibilidade básica do repositório NEXUS, identificando ambiguidades reais e propondo melhorias baseadas em evidência.

## Resultado observável

Ao final, você deverá entregar:

- saída do validador;
- commit analisado;
- mapa de navegação com pelo menos seis nós;
- tempo gasto por etapa;
- lista de ambiguidades;
- reprodução por outra pessoa;
- proposta de melhoria priorizada.

## Pré-requisitos

- Git instalado;
- Python 3.11 ou superior;
- editor de texto;
- acesso de leitura ao repositório;
- nenhuma credencial de produção.

## Materiais

- cópia local do repositório;
- terminal;
- navegador ou editor Markdown;
- cronômetro;
- formulário de evidências deste laboratório.

## Preparação

```bash
git clone https://github.com/matheusflorindo32/nexus-agent-engineering-academy.git
cd nexus-agent-engineering-academy
git rev-parse HEAD
python --version
```

Registre a saída antes de continuar.

## Baseline

Antes de abrir os índices, registre:

1. quanto você já sabe sobre a estrutura do repositório;
2. quanto tempo estima que levará para encontrar um módulo e seu laboratório;
3. quais nomes de diretório espera encontrar;
4. qual dificuldade prevê.

## Procedimento

1. Execute `python tests/validate_repository.py`.
2. Registre sucesso, falha e mensagem principal.
3. Abra o README raiz.
4. Localize o currículo.
5. Selecione um conceito entre contexto, tools, loops, memória, avaliação ou segurança.
6. Localize o módulo correspondente.
7. Localize o laboratório vinculado.
8. Localize um template ou rubrica aplicável.
9. Localize uma referência oficial citada.
10. Encontre o gate Premium Elite correspondente.
11. Desenhe o caminho em Mermaid ou texto estruturado.
12. Registre tempo, hesitações, links quebrados e ambiguidades.

## Cenários obrigatórios

| ID | Cenário | Resultado esperado |
|---|---|---|
| O1 | navegação pelo README raiz | currículo encontrado sem busca externa |
| O2 | navegação pelo índice do curso | módulo correto localizado |
| O3 | navegação pelo índice de labs | laboratório correspondente localizado |
| O4 | execução do validador | resultado e ambiente registrados |
| O5 | busca por gate | regra de promoção localizada |
| O6 | reprodução independente | outra pessoa repete o caminho sem ajuda oral |

## Testes negativos

- link relativo inexistente;
- conceito sem laboratório claro;
- arquivo sem frontmatter reconhecível;
- referência citada sem contexto suficiente;
- caminho que exige conhecimento tácito;
- instrução que depende de interface específica;
- arquivo com nome ambíguo ou duplicado.

Não invente o destino correto. Registre a falha exatamente como ocorreu.

## Evidências

```markdown
- Lab: LAB-000
- Commit: `<sha>`
- Sistema operacional: `<sistema>`
- Python: `<versão>`
- Validador: aprovado | reprovado
- Conceito escolhido: `<conceito>`
- Tempo total: `<minutos>`
- Caminho: `<arquivo 1> → <arquivo 2> → ...`
- Links quebrados: `<lista>`
- Ambiguidades: `<lista>`
- Reprodutor independente: `<identificador não sensível>`
- Resultado da reprodução: sucesso | parcial | falha
- Melhoria prioritária: `<texto>`
- Risco residual: `<texto>`
```

## Critérios de aprovação

- validador executado e saída registrada;
- commit, sistema operacional e runtime registrados;
- mapa com pelo menos seis nós válidos;
- todos os caminhos apontam para arquivos ou fontes existentes;
- ao menos um teste negativo foi tentado;
- outra pessoa reproduziu o caminho usando somente a evidência;
- ambiguidades foram classificadas por impacto;
- nenhuma credencial ou dado pessoal foi incluído;
- autoavaliação concluída.

## Rubrica

| Nível | Evidência |
|---|---|
| insuficiente | validador ou mapa ausente; navegação não reproduzível |
| funcional | caminho principal encontrado e evidência básica registrada |
| robusta | testes negativos, tempos e reprodução independente documentados |
| excelente | ambiguidades priorizadas, correções propostas e evidência totalmente reproduzível |

## Teste adversarial

Peça a outra pessoa, ou a um agente sem contexto prévio, para repetir o caminho usando apenas seu relatório.

Ela não pode receber:

- explicação oral adicional;
- caminho pronto por mensagem externa;
- indicação visual do arquivo correto;
- credencial ou acesso especial.

Registre onde ela hesitou, desviou ou falhou.

## Stop conditions

Pare imediatamente quando:

- houver pedido de credencial;
- for necessária instalação privilegiada não prevista;
- o repositório analisado não puder ser confirmado;
- o mesmo erro ocorrer três vezes;
- o limite de 60 minutos for atingido;
- houver risco de expor dado sensível;
- a instrução exigir mutação não prevista no repositório.

Não contorne controles de segurança. Registre o bloqueio e a próxima ação segura.

## Troubleshooting

| Problema | Ação segura |
|---|---|
| `python` não encontrado | testar `python3 --version` e registrar a diferença |
| clone falha | confirmar URL e conectividade; não inserir token no comando |
| validador falha | preservar a saída e localizar o arquivo citado |
| Mermaid não renderiza | entregar descrição textual equivalente |
| link abre página errada | registrar origem, destino e commit |
| tempo esgotado | encerrar e registrar o ponto exato de bloqueio |

## Acessibilidade

- O mapa Mermaid deve possuir descrição textual equivalente.
- Não use somente cor para indicar sucesso ou falha.
- Registre comandos e resultados em texto copiável.
- Não dependa apenas de posição visual da interface.
- Use títulos hierárquicos e listas curtas.
- Evite screenshots como única evidência.

## Limpeza

Este laboratório não realiza mutações externas. Ao concluir:

- remova arquivos temporários que contenham caminhos locais sensíveis;
- confirme que nenhum token foi incluído no histórico do terminal ou relatório;
- preserve somente evidências necessárias.

## Reflexão final

1. Qual parte dependeu de conhecimento tácito?
2. O que poderia ser validado automaticamente?
3. A estrutura funcionaria igualmente no GitHub e em um editor local?
4. Qual ambiguidade teve maior impacto?
5. Qual melhoria oferece maior benefício com menor custo?
6. A reprodução independente confirmou sua hipótese?

## Autoavaliação

Consigo demonstrar:

- qual commit analisei;
- como executei o validador;
- como naveguei do conceito até a evidência;
- onde a estrutura foi ambígua;
- como outra pessoa reproduziu o caminho;
- qual melhoria proponho e por quê.

## Entrega

Salve o relatório como:

```text
labs/evidence/LAB-000-<identificador-nao-sensivel>.md
```

Não inclua e-mail, telefone, token, chave ou outro dado sensível no nome ou conteúdo do arquivo.

## Limitações

Este laboratório valida navegabilidade em um ambiente e perfil específicos. Ele não prova acessibilidade universal, ausência total de links quebrados ou adequação para todos os públicos. O status permanece `review` até reprodução independente, revisão humana e atendimento ao [gate Premium Elite dos laboratórios](LABS_PREMIUM_ELITE_GATE.md).