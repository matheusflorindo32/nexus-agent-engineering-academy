---
id: standards.visual-evidence
title: Política de imagens e evidências visuais
lang: pt-BR
status: review
version: 0.1.0
---

# Política de imagens e evidências visuais

## Objetivo

Garantir que diagramas, capturas de tela, fotografias, infográficos e vídeos sejam claros, acessíveis, rastreáveis, legalmente reutilizáveis e tecnicamente corretos.

## Princípios

1. **A imagem precisa ensinar.** Elementos apenas decorativos não substituem explicação.
2. **A fonte precisa ser rastreável.** Toda imagem externa deve registrar autor, origem, licença e data de acesso.
3. **Acessibilidade é obrigatória.** Toda imagem informativa deve possuir texto alternativo e, quando complexa, descrição longa.
4. **O conteúdo visual deve ser versionável.** Prefira Mermaid, SVG editável ou arquivo-fonte junto ao exportado.
5. **Dados sensíveis devem ser removidos.** Capturas não podem expor nomes, e-mails, chaves, tokens, caminhos pessoais ou dados institucionais restritos.
6. **IA generativa deve ser declarada.** Imagens sintéticas devem registrar ferramenta, finalidade, data e revisão humana.

## Hierarquia de preferência

1. diagramas próprios em Mermaid ou SVG;
2. capturas próprias sanitizadas;
3. imagens oficiais com autorização/licença clara;
4. imagens Creative Commons compatíveis;
5. imagens geradas por IA, quando não representarem evidência factual.

## Metadados mínimos

```yaml
asset_id: visual.<identificador>
title: <título>
type: diagram | screenshot | photo | infographic | video
creator: <autor ou organização>
source_url: <URL ou caminho interno>
license: <licença>
created_at: YYYY-MM-DD
accessed_at: YYYY-MM-DD
ai_generated: false
reviewed_by: <responsável>
alt_text: <descrição objetiva>
```

## Capturas de tela

Antes de publicar:

- recorte áreas irrelevantes;
- oculte dados pessoais e segredos;
- destaque apenas o passo ensinado;
- registre plataforma e versão;
- evite interface desatualizada sem aviso;
- inclua legenda indicando o objetivo da captura.

## Diagramas

- use fluxo de leitura consistente;
- evite mais de 9 nós sem agrupamento;
- não dependa apenas de cores;
- mantenha contraste adequado;
- explique siglas na primeira ocorrência;
- forneça equivalente textual para diagramas críticos.

## Imagens geradas por IA

Podem ser usadas para:

- capas;
- metáforas visuais;
- cenários fictícios;
- elementos de identidade;
- ilustrações conceituais revisadas.

Não devem ser usadas como prova de:

- funcionamento de uma interface;
- resultado experimental;
- existência de uma pessoa, produto ou evento;
- dado científico;
- procedimento oficial.

## Critérios de bloqueio

A publicação deve parar quando:

- a licença for desconhecida;
- houver dado pessoal ou segredo;
- a imagem induzir interpretação técnica incorreta;
- faltar texto alternativo;
- a fonte não puder ser verificada;
- uma imagem sintética estiver apresentada como evidência real.

## Checklist de revisão

- [ ] A imagem tem função pedagógica clara.
- [ ] Fonte, licença e versão foram registradas.
- [ ] Não há PII, credenciais ou informações restritas.
- [ ] Há texto alternativo adequado.
- [ ] Cores não são o único meio de comunicação.
- [ ] O arquivo-fonte está preservado quando aplicável.
- [ ] Conteúdo gerado por IA está identificado.
- [ ] A imagem foi revisada por uma pessoa.

## Referências de consulta

- Web Content Accessibility Guidelines (WCAG): https://www.w3.org/WAI/standards-guidelines/wcag/
- Creative Commons Licenses: https://creativecommons.org/share-your-work/cclicenses/
- GitHub documentation — Rendering diagrams: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- Mermaid documentation: https://mermaid.js.org/
