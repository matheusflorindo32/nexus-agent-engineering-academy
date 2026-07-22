---
id: nexus.quickstart
title: Quickstart local sem chave
lang: pt-BR
status: review
version: 0.1.0
---

# Quickstart local sem chave

## Objetivo

Em até 10 minutos, validar o repositório e executar um agente mínimo read-only sem conta externa, chave de API, pagamento ou acesso a dados reais.

## Pré-requisitos

- Git;
- Python 3.11 ou superior;
- terminal com permissão para criar arquivos na pasta escolhida;
- conexão apenas para clonar o repositório. A execução principal é local.

## 1. Clonar e entrar no projeto

```bash
git clone https://github.com/matheusflorindo32/nexus-agent-engineering-academy.git
cd nexus-agent-engineering-academy
```

Registre o commit usado:

```bash
git rev-parse HEAD
```

## 2. Confirmar a versão do Python

Linux/macOS:

```bash
python3 --version
```

Windows:

```powershell
python --version
```

Use o comando que retornar Python 3.11 ou superior nos passos seguintes.

## 3. Validar o repositório

```bash
python tests/validate_repository.py
```

Resultado esperado:

- frontmatter válido;
- links internos existentes;
- IDs sem conflito;
- módulos, labs e projetos com seções obrigatórias;
- nenhum erro bloqueador.

CI ou validador verde prova somente os contratos automatizados implementados. Não prova correção total, segurança absoluta ou qualidade pedagógica com estudantes reais.

## 4. Executar o exemplo read-only

```bash
python examples/minimal_readonly_agent.py --demo
```

O exemplo deve:

- usar dados sintéticos;
- não acessar e-mail, calendário, nuvem ou conta real;
- não produzir efeito externo;
- demonstrar classificação, recusa ou abstention;
- encerrar de forma determinística.

## 5. Registrar evidência mínima

Crie um relatório local fora do repositório ou em uma branch própria:

```markdown
- Commit: `<git rev-parse HEAD>`
- Sistema operacional: `<nome e versão>`
- Python: `<versão>`
- Validador: aprovado | reprovado
- Demo: aprovada | reprovada
- Tempo total: `<minutos>`
- Bloqueios: `<lista>`
- Próxima ação: `<ação concreta>`
```

Não registre nome completo, e-mail, token, caminho pessoal, IP ou credencial.

## Próxima etapa

- iniciante absoluto: [Trilha Zero](course/zero-track/README.md);
- já usa terminal e Git: [Módulo 00](course/modules/00-orientation/README.md);
- quer construir o primeiro contrato: [Módulo 01](course/modules/01-agent-foundations/README.md);
- quer validar navegação e evidência: [LAB-000](labs/LAB-000-repository-orientation.md).

## Troubleshooting

### `python` não encontrado

Tente `python3`. No Windows, confirme se o Python foi adicionado ao `PATH` durante a instalação.

### Versão inferior a 3.11

Instale uma versão suportada sem remover ambientes exigidos por outros projetos. Não use privilégios administrativos além do necessário.

### Erro de link ou frontmatter

Confirme o commit e execute novamente sem modificar arquivos. Persistindo, abra uma issue com:

- commit;
- sistema operacional;
- versão do Python;
- comando executado;
- mensagem de erro sanitizada.

### Demo tenta acessar rede ou credencial

Pare imediatamente. O quickstart canônico não deve exigir rede depois do clone, conta externa ou segredo.

### Resultado diferente entre execuções

Registre as duas saídas, versão do Python e commit. Não esconda flakiness nem selecione apenas a execução favorável.

## Stop conditions

Interrompa quando:

- houver pedido de chave, senha ou login;
- dados reais forem solicitados;
- for necessário executar ação externa;
- o repositório ou commit não puder ser confirmado;
- o mesmo erro ocorrer três vezes sem nova evidência;
- qualquer comando parecer incompatível com o escopo local e read-only.

## Critérios de conclusão

- [ ] Commit registrado.
- [ ] Python suportado confirmado.
- [ ] Validador executado.
- [ ] Demo read-only executada.
- [ ] Nenhuma credencial ou dado pessoal utilizado.
- [ ] Evidência mínima registrada.
- [ ] Próxima etapa escolhida.

## Limitações

Este quickstart valida apenas a entrada local no projeto. Ele não substitui revisão de segurança, testes dos módulos, validação multiplataforma, acessibilidade prática ou piloto com estudantes.