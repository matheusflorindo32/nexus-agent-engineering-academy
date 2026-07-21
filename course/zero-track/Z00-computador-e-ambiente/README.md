---
id: course.zero-track.z00
title: Z00 — Computador e ambiente de desenvolvimento
lang: pt-BR
status: pilot
prerequisites: []
estimated_hours: 2
---

# Z00 — Computador e ambiente de desenvolvimento

## Para quem é

Para quem usa computador no dia a dia, mas ainda não entende claramente arquivos, pastas, programas, processos, terminal e versões de ferramentas.

## O que você vai aprender

Ao concluir, você consegue:

- diferenciar hardware, sistema operacional, programa, processo, arquivo e pasta;
- localizar uma pasta de trabalho;
- identificar versões do sistema, Python e Git;
- executar um verificador seguro;
- registrar evidência do ambiente sem expor dados sensíveis.

## Por que isso importa

Grande parte dos erros de iniciantes não é erro de programação. É confusão sobre onde o arquivo está, qual programa está sendo executado ou qual versão está instalada.

## Explicação em linguagem simples

Pense no computador como uma oficina:

- **hardware** é o espaço físico e as máquinas;
- **sistema operacional** é a administração da oficina;
- **programa** é uma ferramenta disponível;
- **processo** é a ferramenta em uso;
- **arquivo** é um documento ou peça armazenada;
- **pasta** é uma forma de organizar esses itens;
- **terminal** é um balcão onde você dá instruções por texto.

## Conceito profissional

Um ambiente reproduzível registra sistema operacional, arquitetura, versões de runtime, dependências, diretório de trabalho e commit. Sem isso, resultados iguais não podem ser esperados de forma confiável.

## Demonstração guiada

### Windows PowerShell

```powershell
Get-Location
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
python --version
git --version
```

### Linux ou macOS

```bash
pwd
uname -a
python3 --version
git --version
```

Não se preocupe se algum comando falhar. Registrar a falha faz parte da atividade.

## Verificador seguro

Na raiz do repositório, execute:

### Windows

```powershell
python course/zero-track/scripts/check_environment.py
```

### Linux ou macOS

```bash
python3 course/zero-track/scripts/check_environment.py
```

O script não envia dados para a internet e não lê credenciais.

## Prática guiada

1. Crie uma pasta chamada `nexus-zero-lab` em um local conhecido.
2. Entre nela.
3. Crie um arquivo chamado `evidencia-z00.txt`.
4. Registre:
   - sistema operacional;
   - versão do Python;
   - versão do Git;
   - diretório de trabalho;
   - comandos que falharam.

## Prática independente

Explique, com suas palavras:

1. a diferença entre programa e processo;
2. por que duas pessoas podem obter resultados diferentes com o mesmo código;
3. quais informações são úteis para reproduzir um erro;
4. quais informações não devem ser publicadas.

## Erros comuns

- executar comandos em uma pasta diferente da esperada;
- usar `python` quando o sistema possui apenas `python3`;
- copiar caminhos sem aspas quando possuem espaços;
- publicar nome de usuário, tokens, chaves ou caminhos sensíveis;
- acreditar que uma falha de instalação significa incapacidade para programar.

## Teste de segurança

O relatório não pode conter:

- senhas;
- tokens;
- chaves de API;
- conteúdo de arquivos pessoais;
- variáveis de ambiente sensíveis;
- endereço residencial ou outros dados desnecessários.

## Evidência mínima

Entregue:

- saída do verificador;
- arquivo `evidencia-z00.txt`;
- uma explicação curta do ambiente;
- ao menos uma dificuldade encontrada e como foi investigada.

## Critérios de conclusão

- **insuficiente:** apenas leu o material;
- **funcional:** executou os comandos e registrou versões;
- **robusta:** explicou falhas e protegeu dados sensíveis;
- **excelente:** outra pessoa consegue reproduzir o ambiente usando o relatório.

## Autoavaliação

- [ ] Sei dizer onde estou no sistema de arquivos.
- [ ] Sei identificar a versão do Python e do Git.
- [ ] Entendo a diferença entre arquivo, programa e processo.
- [ ] Registrei evidência sem expor segredos.

## Próximo passo

Siga para [Z01 — Terminal sem medo](../Z01-terminal-sem-medo/README.md).
