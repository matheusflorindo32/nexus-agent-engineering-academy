---
id: governance.accessibility-validation
lang: pt-BR
title: Protocolo de validação de acessibilidade
status: review
version: 0.1.0
---

# Protocolo de validação de acessibilidade

## Objetivo

Produzir evidências verificáveis de que o conteúdo e o futuro portal podem ser usados por pessoas com diferentes necessidades, tecnologias assistivas, dispositivos e condições de conectividade.

## Escopo inicial

- README e quickstart;
- Trilha Zero;
- um módulo de cada fase;
- um laboratório de cada nível de risco;
- projeto starter e capstone;
- navegação, busca, código, tabelas, imagens, diagramas e formulários.

## Princípios

- automação ajuda, mas não substitui revisão humana;
- conformidade declarada sem evidência é proibida;
- ausência de erro automático não significa acessibilidade;
- conteúdo visual deve possuir equivalente textual útil;
- a pessoa usuária não deve depender de cor, movimento, áudio ou precisão motora;
- bloqueios críticos prevalecem sobre média ou pontuação agregada.

## Matriz de testes

| Dimensão | Método mínimo | Evidência |
|---|---|---|
| teclado | percurso completo sem mouse | vídeo curto ou sequência documentada |
| foco | ordem, visibilidade e retorno após diálogo | checklist por rota |
| leitor de tela | títulos, landmarks, links, tabelas e formulários | roteiro e achados |
| zoom/reflow | 200% e viewport estreito | capturas e problemas registrados |
| contraste | análise automática e inspeção contextual | relatório |
| movimento | redução de movimento e pausa | comportamento observado |
| imagens | texto alternativo e descrição longa quando necessária | inventário |
| diagramas | explicação textual equivalente | revisão por amostra |
| código | leitura, cópia, wrapping e identificação de linguagem | teste manual |
| linguagem | clareza, glossário e expansão de siglas | revisão editorial |
| formulários | labels, erros, instruções e recuperação | roteiro |
| baixo desempenho | conteúdo essencial sem JavaScript e rede lenta | teste controlado |

## Cenários obrigatórios

1. navegar do README ao primeiro laboratório apenas por teclado;
2. localizar o objetivo e os pré-requisitos com leitor de tela;
3. compreender um diagrama sem acessar a imagem;
4. executar o quickstart em viewport estreito e zoom de 200%;
5. identificar erro de formulário sem depender de cor;
6. interromper animação ou respeitar preferência de movimento reduzido;
7. copiar comando sem perder caracteres;
8. encontrar estado editorial e limitações de uma página;
9. retornar ao ponto anterior após abrir e fechar navegação móvel;
10. acessar conteúdo essencial com JavaScript desativado.

## Severidade

- **crítica:** impede acesso a conteúdo, ação essencial ou segurança;
- **alta:** exige contorno difícil ou exclui grupo relevante;
- **média:** prejudica compreensão, eficiência ou conforto;
- **baixa:** melhoria sem bloqueio imediato.

## Hard gates

Bloqueiam publicação:

- navegação principal impossível por teclado;
- foco invisível ou aprisionado;
- conteúdo essencial ausente para leitor de tela;
- imagem instrucional sem equivalente textual;
- formulário sem label ou recuperação de erro;
- contraste insuficiente em texto ou controle essencial;
- movimento obrigatório sem alternativa;
- conteúdo crítico inacessível com zoom ou reflow;
- achado crítico ou alto sem owner, tratamento ou decisão formal.

## Revisão humana

A validação deve incluir pelo menos uma pessoa diferente do autor. Para promoção futura a `stable`, o projeto deve buscar participação de usuários com tecnologias assistivas e registrar consentimento, escopo, método, compensação quando aplicável e limitações da amostra.

## Relatório

```yaml
accessibility_review_id: a11y-YYYY-NNN
commit_sha: <sha>
routes_tested: []
methods: []
reviewers: []
findings:
  - id: A11Y-001
    severity: high
    route: <rota>
    evidence: <referência>
    owner: <responsável>
    due: YYYY-MM-DD
    status: open
blocking_findings: []
residual_risks: []
decision: no-go
```

## Critérios de saída

- 100% dos cenários obrigatórios executados;
- zero achado crítico aberto;
- zero achado alto sem tratamento aprovado;
- evidências vinculadas ao mesmo SHA;
- regressões adicionadas quando automatizáveis;
- limitações e cobertura declaradas;
- aprovação humana explícita.

## Limitações

O protocolo não garante conformidade legal ou acessibilidade universal. Ele estabelece um processo verificável de redução de barreiras que deve evoluir com testes reais e revisão especializada.