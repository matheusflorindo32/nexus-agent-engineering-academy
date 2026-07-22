---
id: governance.learner-pilot
lang: pt-BR
title: Protocolo de piloto com estudantes
status: review
version: 0.1.0
---

# Protocolo de piloto com estudantes

## Objetivo

Validar se a NEXUS permite que pessoas reais aprendam, executem e expliquem os resultados propostos sem depender de orientação oral constante, exposição a risco ou alegações pedagógicas não sustentadas.

## Perguntas de pesquisa

1. Pessoas iniciantes concluem o quickstart e a Trilha Zero?
2. Os pré-requisitos e stop conditions são compreendidos?
3. Os laboratórios produzem evidência reproduzível?
4. A progressão de dificuldade é adequada?
5. Quais barreiras de acessibilidade, linguagem e ambiente aparecem?
6. O estudante distingue demo, piloto, produção e segurança absoluta?
7. Outra pessoa consegue reproduzir a entrega final?

## Desenho inicial

O primeiro piloto deve ser pequeno, controlado e exploratório. Recomenda-se uma coorte de 5 a 12 participantes com diversidade de experiência, dispositivo e familiaridade com programação. A amostra não autoriza generalização estatística ampla.

## Segmentos

- iniciante absoluto em programação;
- pessoa com experiência básica em scripts;
- pessoa de produto ou automação visual;
- pessoa desenvolvedora;
- pessoa que utilize tecnologia assistiva, quando houver participação voluntária e condições adequadas.

## Escopo do piloto

- onboarding e quickstart;
- Trilha Zero;
- Módulos 00 e 01;
- LAB-000 e LAB-101;
- projeto Starter;
- reprodução de uma entrega por colega.

Módulos de alto risco não entram no primeiro piloto sem ambiente isolado, facilitador capacitado e protocolo específico.

## Ética, privacidade e consentimento

- participação voluntária;
- objetivo e uso dos dados explicados antes do início;
- coleta mínima;
- nenhum segredo, dado pessoal operacional ou credencial real;
- possibilidade de desistência sem penalidade;
- publicação somente de resultados agregados ou anonimizados;
- gravação apenas com consentimento específico;
- canal para correção ou exclusão dos dados do participante.

## Baseline

Antes da atividade, registrar:

- experiência declarada;
- sistema operacional e dispositivo;
- familiaridade com terminal, Git e Python;
- necessidade de acessibilidade comunicada voluntariamente;
- expectativa e confiança inicial;
- tempo estimado para concluir a tarefa sem material NEXUS, quando aplicável.

## Métricas

### Resultado

- taxa de conclusão por etapa;
- tempo até primeiro resultado verificável;
- taxa de execução correta dos comandos;
- taxa de cenários críticos aprovados;
- taxa de reprodução por outra pessoa;
- retenção de conceitos em verificação posterior curta.

### Processo

- pedidos de ajuda por etapa;
- pontos de abandono;
- erros recorrentes;
- links ou instruções não encontrados;
- tempo em troubleshooting;
- barreiras de acessibilidade;
- confiança antes e depois.

### Segurança e entendimento

- participantes que identificam limites de autoridade;
- participantes que reconhecem stop conditions;
- tentativas de usar credenciais ou dados reais;
- confusão entre CI verde e prontidão;
- compreensão de risco residual.

Toda métrica deve declarar numerador, denominador, exclusões e tamanho da amostra.

## Cenários obrigatórios

1. localizar o ponto de entrada sem orientação oral;
2. executar o quickstart;
3. explicar o que o exemplo pode e não pode fazer;
4. localizar uma stop condition;
5. concluir o LAB-000;
6. produzir contrato do LAB-101;
7. identificar um caso em que workflow simples é melhor que agente;
8. registrar limitação e risco residual;
9. entregar evidence bundle mínimo;
10. permitir reprodução por colega.

## Intervenção do facilitador

Ajuda deve ser registrada em níveis:

- `0`: nenhuma ajuda;
- `1`: indicação da seção correta;
- `2`: explicação conceitual;
- `3`: passo técnico específico;
- `4`: facilitador executa parte da tarefa.

Conclusão com ajuda 3 ou 4 não pode ser contabilizada como conclusão independente.

## Stop conditions

Interromper atividade quando houver risco de usar sistema real, exposição de dado sensível, sofrimento ou constrangimento, barreira de acessibilidade sem alternativa razoável, efeito externo não previsto, ambiente fora do controle ou pedido de retirada do participante.

## Análise

Separar:

- defeito do conteúdo;
- defeito do portal;
- pré-requisito ausente;
- problema de ambiente;
- barreira de acessibilidade;
- erro do exemplo;
- hipótese pedagógica não confirmada;
- caso isolado ainda inconclusivo.

Não remover resultados desfavoráveis. Mudanças no método depois do início devem ser registradas.

## Critérios para revisão curricular

Abrir correção prioritária quando:

- mais de 20% da coorte encontra o mesmo bloqueio;
- qualquer participante é induzido a ação insegura;
- uma instrução essencial depende de orientação oral;
- reprodução independente falha por conhecimento tácito;
- achado crítico de acessibilidade aparece;
- hard gate não é compreendido ou aplicado.

Os percentuais são sinais operacionais para o piloto, não prova estatística de eficácia.

## Relatório de saída

```yaml
pilot_id: pilot-YYYY-NNN
commit_sha: <sha>
scope: []
participants_enrolled: 0
participants_completed: 0
independent_completions: 0
methods: []
blocking_findings: []
accessibility_findings: []
content_changes: []
residual_risks: []
decision: revise-before-next-pilot
```

## Decisões possíveis

- `stop-and-redesign`;
- `revise-before-next-pilot`;
- `continue-with-constraints`;
- `expand-pilot`.

Nenhuma decisão do piloto equivale automaticamente a `stable`, certificação ou eficácia universal.

## Limitações

O piloto inicial produz evidência contextual, não uma validação científica definitiva. Promoções de status exigem repetição, revisão externa, acessibilidade prática e integração das correções.