---
id: standards.source-evidence
content_id: standards.source-evidence
version: 1.0.0
title: Política de fontes, evidências e divergências
lang: pt-BR
status: active
reviewed_at: 2026-07-19
---

# Política de fontes, evidências e divergências

## Objetivo

Garantir que afirmações técnicas, comparações de plataformas e recomendações da NEXUS possam ser verificadas, atualizadas e contestadas sem depender de autoridade informal.

## Hierarquia de fontes

1. especificação, documentação ou repositório oficial versionado;
2. artigo científico, padrão técnico ou publicação institucional primária;
3. documentação oficial não versionada;
4. implementação reproduzível e teste registrado pela NEXUS;
5. fonte secundária reconhecida, usada apenas para contexto;
6. comunidade, fórum ou relato individual, sempre rotulado como evidência anedótica.

Fontes promocionais não sustentam alegações de segurança, desempenho, equivalência ou confiabilidade sem verificação independente.

## Campos obrigatórios

Toda referência operacional deve registrar, quando aplicável:

- título;
- autor ou organização;
- URL ou identificador persistente;
- versão, release ou commit;
- data de publicação;
- data de acesso;
- trecho ou capacidade sustentada;
- limitações conhecidas;
- idioma;
- responsável pela verificação.

## Classes de afirmação

| Classe | Exemplo | Evidência mínima |
|---|---|---|
| conceitual | definição de agente | fonte primária ou bibliografia consolidada |
| capacidade atual | ferramenta suporta aprovação humana | documentação oficial atual e data de acesso |
| desempenho | abordagem A supera B | benchmark reproduzível com dataset e métricas |
| segurança | controle reduz risco | threat model, teste adversarial e limitação explícita |
| recomendação | usar workflow em vez de agente | critérios, trade-offs e contexto de aplicação |

## Tratamento de divergências

Quando fontes confiáveis discordarem:

1. não escolher silenciosamente uma versão;
2. registrar as duas interpretações;
3. comparar escopo, versão, data e definição usada;
4. executar teste reproduzível quando possível;
5. marcar a conclusão como `resolved`, `provisional` ou `unresolved`;
6. definir condição para reavaliação.

## Atualidade

Capacidades de plataformas devem ter `verified_at` e `verified_version`. Uma comparação fica `stale` quando:

- a fonte oficial muda materialmente;
- ocorre nova release principal;
- passam 90 dias sem revisão para produtos de evolução rápida;
- um teste deixa de ser reproduzível.

## Citações e formatos

- ABNT: documentos educacionais e institucionais em português;
- Vancouver: conteúdos biomédicos ou científicos que exijam numeração;
- links inline: documentação técnica operacional;
- DOI, ISBN, RFC, commit ou release devem ser preservados quando existirem.

## Conteúdo gerado por IA

Texto gerado por IA nunca é fonte. Ele pode:

- resumir uma fonte já verificada;
- propor hipóteses;
- ajudar a estruturar testes;
- sugerir lacunas.

Ele não pode substituir consulta, versionamento, teste ou atribuição.

## Definition of Done de evidência

Uma entrega está pronta apenas quando:

- cada alegação importante possui fonte ou teste;
- datas e versões estão registradas;
- inferências estão identificadas como inferências;
- limitações e divergências aparecem junto à conclusão;
- nenhuma fonte foi inventada;
- links e identificadores foram verificados;
- há critério explícito para atualização futura.
