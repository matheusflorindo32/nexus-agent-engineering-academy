---
id: docs.pedagogy.accessibility-checklist
title: Checklist de acessibilidade educacional
lang: pt-BR
status: review
---

# Checklist de acessibilidade educacional

## Objetivo

Garantir que a NEXUS não dependa de um único modo de percepção, interação ou ambiente técnico. Este checklist é um gate editorial e técnico, não uma alegação automática de conformidade formal.

## Linguagem e compreensão

- [ ] Frases curtas e diretas quando o conceito permitir.
- [ ] Termos técnicos definidos antes do uso.
- [ ] Glossário por módulo.
- [ ] Siglas expandidas na primeira ocorrência.
- [ ] Exemplos simples antes dos avançados.
- [ ] Instruções numeradas para procedimentos.
- [ ] Resultado esperado mostrado após cada comando.
- [ ] Erros comuns e recuperação documentados.
- [ ] Alternativa em linguagem simples para conceitos críticos.

## Estrutura e navegação

- [ ] Hierarquia de títulos lógica e sem saltos desnecessários.
- [ ] Links com texto descritivo.
- [ ] Índice em documentos longos.
- [ ] Próximo passo explícito.
- [ ] Caminho de retorno ao currículo.
- [ ] IDs estáveis para módulos e LABs.
- [ ] Navegação possível sem depender exclusivamente de imagem ou cor.

## Imagens, diagramas e vídeo

- [ ] Toda imagem informativa possui texto alternativo útil.
- [ ] Diagramas são acompanhados de descrição textual equivalente.
- [ ] Cor não é o único meio de comunicar estado.
- [ ] Contraste é revisado.
- [ ] GIFs possuem alternativa estática ou textual.
- [ ] Vídeos possuem legendas.
- [ ] Vídeos possuem transcrição.
- [ ] Demonstrações visuais descrevem comandos e resultados em texto.
- [ ] Animações evitam piscar ou oferecem controle.

## Código e comandos

- [ ] Blocos de código indicam linguagem.
- [ ] Comandos são copiáveis.
- [ ] Linhas longas têm alternativa legível.
- [ ] Saídas importantes são explicadas em texto.
- [ ] Não se usa apenas cor para indicar sucesso ou falha.
- [ ] Exemplos evitam fontes minúsculas em imagens.
- [ ] Cada comando destrutivo possui aviso e alternativa segura.
- [ ] Existe explicação para PowerShell, Linux e macOS quando necessário.

## Teclado e interfaces

- [ ] Conteúdo principal pode ser consumido por teclado.
- [ ] Interfaces demonstrativas possuem foco visível.
- [ ] Ordem de foco é lógica.
- [ ] Controles têm rótulos claros.
- [ ] Não há interação obrigatória baseada apenas em hover.
- [ ] Atalhos não conflitam com tecnologias assistivas sem alternativa.

## Compatibilidade e acesso

- [ ] Quickstart funciona sem conta paga.
- [ ] Primeiro contato não exige chave de API.
- [ ] Há alternativa local ou simulada para serviços externos.
- [ ] Dependências e versões estão explícitas.
- [ ] Existe versão de baixo consumo de dados.
- [ ] Materiais essenciais podem ser baixados ou impressos.
- [ ] Requisitos mínimos de hardware são honestos.
- [ ] Há alternativa quando uma plataforma não é suportada.

## Avaliação inclusiva

- [ ] Tempo sugerido não é usado como único indicador de competência.
- [ ] Há mais de uma forma de demonstrar entendimento quando possível.
- [ ] Critérios são publicados antes da atividade.
- [ ] Rubrica avalia resultado, segurança e explicação, não estilo pessoal.
- [ ] Necessidades de adaptação podem ser registradas no piloto.
- [ ] A defesa pode ter formato acessível equivalente.
- [ ] Erros de digitação não anulam competência técnica quando não são o objeto avaliado.

## Segurança e privacidade

- [ ] Nenhuma adaptação exige exposição de diagnóstico médico.
- [ ] Dados de acessibilidade são minimizados e protegidos.
- [ ] Exercícios usam dados e credenciais sintéticos.
- [ ] O aluno pode executar atividades sem compartilhar conta pessoal.
- [ ] Há canal para relatar barreira de acessibilidade com privacidade.

## Plataformas mínimas de teste

| Ambiente | Teste mínimo |
|---|---|
| Windows PowerShell | clone, validação, exemplo e teste |
| Linux | clone, validação, exemplo e teste |
| macOS | clone, validação, exemplo e teste |
| Leitor de tela | navegação por títulos, links, código e texto alternativo |
| Apenas teclado | navegação e uso da demonstração principal |
| Tela pequena | leitura do README, currículo e instruções |
| Baixa conexão | acesso aos textos e exemplos essenciais |

## Evidência obrigatória

Uma revisão de acessibilidade deve registrar:

- versão e SHA;
- páginas ou módulos testados;
- ambiente;
- ferramentas utilizadas;
- barreiras encontradas;
- severidade;
- correção ou alternativa;
- risco residual;
- responsável pela revisão.

## Severidade de barreiras

- A0: risco ou impossibilidade total de uso seguro;
- A1: bloqueia público declarado sem alternativa;
- A2: objetivo importante fica significativamente prejudicado;
- A3: atrito relevante, mas contornável;
- A4: melhoria editorial.

## Gate de lançamento

A campanha principal não deve afirmar acessibilidade ampla enquanto:

- imagens essenciais não tiverem alternativa textual;
- vídeos essenciais não tiverem legenda e transcrição;
- Quickstart depender de plataforma única;
- navegação principal falhar por teclado;
- barreiras A0 ou A1 permanecerem abertas.

## Limitação

Este checklist orienta revisão, mas não substitui auditoria especializada nem prova conformidade jurídica com normas específicas.
