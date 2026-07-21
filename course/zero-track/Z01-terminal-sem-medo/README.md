---
id: course.zero-track.z01
title: Z01 — Terminal sem medo
lang: pt-BR
status: pilot
prerequisites: [course.zero-track.z00]
estimated_hours: 3
---

# Z01 — Terminal sem medo

## Para quem é

Para quem nunca trabalhou com terminal ou ainda executa comandos sem entender diretório atual, caminho relativo e efeito da operação.

## O que você vai aprender

Ao concluir, você consegue:

- descobrir em qual pasta está;
- listar arquivos e pastas;
- criar, entrar, copiar, mover e remover itens de laboratório;
- ler mensagens de erro;
- interromper uma operação insegura;
- registrar um transcript reproduzível.

## Explicação simples

O terminal é uma conversa com o computador. Cada comando possui:

```text
verbo + alvo + opções
```

Exemplo:

```text
criar + pasta laboratório
```

O computador não adivinha intenção. Ele executa o comando no diretório atual e com as permissões disponíveis.

## Conceito profissional

Operações de terminal dependem de working directory, shell, PATH, permissões e quoting. Um comando reproduzível declara esses elementos e possui condição explícita de parada antes de qualquer efeito destrutivo.

## Comandos essenciais

| Objetivo | PowerShell | Linux/macOS |
|---|---|---|
| mostrar pasta atual | `Get-Location` | `pwd` |
| listar itens | `Get-ChildItem` | `ls -la` |
| criar pasta | `New-Item -ItemType Directory nome` | `mkdir nome` |
| entrar na pasta | `Set-Location nome` | `cd nome` |
| voltar | `Set-Location ..` | `cd ..` |
| criar arquivo | `New-Item arquivo.txt` | `touch arquivo.txt` |
| ler arquivo | `Get-Content arquivo.txt` | `cat arquivo.txt` |
| copiar arquivo | `Copy-Item a.txt b.txt` | `cp a.txt b.txt` |
| mover arquivo | `Move-Item a.txt pasta/` | `mv a.txt pasta/` |
| remover arquivo | `Remove-Item a.txt` | `rm a.txt` |

## Regra de segurança

Nunca execute remoção recursiva fora de uma pasta de laboratório.

Evite, até compreender completamente:

```text
rm -rf
Remove-Item -Recurse -Force
```

## Prática guiada

Crie uma pasta exclusiva chamada `nexus-terminal-lab`.

Dentro dela:

1. crie as pastas `entrada`, `saida` e `arquivo`;
2. crie `entrada/mensagem.txt`;
3. escreva uma frase segura no arquivo;
4. copie o arquivo para `saida`;
5. mova a cópia para `arquivo`;
6. confirme o conteúdo;
7. remova somente a cópia movida;
8. liste a estrutura final.

### Exemplo PowerShell

```powershell
New-Item -ItemType Directory nexus-terminal-lab
Set-Location nexus-terminal-lab
New-Item -ItemType Directory entrada, saida, arquivo
"NEXUS terminal lab" | Set-Content entrada/mensagem.txt
Copy-Item entrada/mensagem.txt saida/mensagem.txt
Move-Item saida/mensagem.txt arquivo/mensagem.txt
Get-Content arquivo/mensagem.txt
Remove-Item arquivo/mensagem.txt
Get-ChildItem -Recurse
```

### Exemplo Linux/macOS

```bash
mkdir nexus-terminal-lab
cd nexus-terminal-lab
mkdir entrada saida arquivo
printf 'NEXUS terminal lab\n' > entrada/mensagem.txt
cp entrada/mensagem.txt saida/mensagem.txt
mv saida/mensagem.txt arquivo/mensagem.txt
cat arquivo/mensagem.txt
rm arquivo/mensagem.txt
find . -maxdepth 2 -print
```

## Prática independente

Sem copiar a sequência acima, crie uma nova estrutura com:

- uma pasta `dados`;
- dois arquivos de texto;
- uma pasta `backup`;
- uma cópia de cada arquivo em `backup`;
- uma evidência final da estrutura.

## Erros comuns

- esquecer em qual pasta está;
- usar caminho de Windows no Linux ou vice-versa;
- remover o arquivo original em vez da cópia;
- não colocar caminhos com espaços entre aspas;
- executar comando como administrador sem necessidade;
- ocultar mensagens de erro na entrega.

## Stop conditions

Pare imediatamente quando:

- o diretório atual não for a pasta de laboratório;
- o comando incluir curingas que você não entende;
- houver solicitação de privilégio administrativo inesperada;
- o alvo da remoção não estiver explicitamente confirmado;
- o resultado divergir da etapa anterior.

## Evidência mínima

Entregue:

- comandos executados;
- saída final da estrutura;
- um erro real encontrado;
- explicação de como confirmou o diretório antes de remover algo;
- nenhuma informação sensível.

## Miniavaliação

1. Qual é a diferença entre caminho absoluto e relativo?
2. Por que o diretório atual importa?
3. O que deve ser verificado antes de remover um arquivo?
4. Quando uma pessoa deve parar e pedir ajuda?

## Critérios de conclusão

- **funcional:** navega, cria e lê arquivos;
- **robusta:** copia, move e remove apenas alvos confirmados;
- **excelente:** produz transcript que outra pessoa consegue seguir com segurança.

## Próximo passo

Siga para [Z02 — Git e GitHub essenciais](../Z02-git-e-github-essenciais/README.md).
