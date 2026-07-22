---
id: governance.deployment-runbook
lang: pt-BR
title: Runbook de deploy e rollback do portal
status: review
version: 0.1.0
---

# Runbook de deploy e rollback do portal

## Objetivo

Publicar o portal educacional de forma reproduzível, auditável e reversível, garantindo que o artefato aprovado seja exatamente o artefato entregue.

## Pré-condições

- PR integrado por aprovação humana;
- CI verde no SHA candidato;
- build local ou em runner limpo;
- inventário de dependências atualizado;
- validação de links, rotas e frontmatter;
- protocolo de acessibilidade executado no escopo definido;
- owner de deploy e owner de rollback identificados;
- digest anterior conhecido;
- nenhuma credencial em arquivo, log ou artefato.

## Manifesto de release

```yaml
release_id: portal-YYYY.N
commit_sha: <sha>
artifact_digest: sha256:<digest>
previous_digest: sha256:<digest>
build_environment: <identificador>
content_status: review
accessibility_report: <referência>
security_review: <referência>
rollback_owner: <responsável>
decision: no-go
```

## Fluxo

1. congelar o SHA candidato;
2. construir em ambiente limpo;
3. gerar digest do artefato;
4. executar testes de links, rotas, conteúdo e acessibilidade;
5. publicar preview imutável;
6. realizar revisão humana do preview;
7. registrar decisão `no-go`, `go-with-constraints` ou `go`;
8. publicar o mesmo digest aprovado;
9. executar smoke tests;
10. monitorar janela inicial;
11. reconciliar divergências;
12. encerrar ou executar rollback.

## Smoke tests

- página inicial retorna sucesso;
- quickstart abre e comandos são legíveis;
- Trilha Zero e módulos 00–12 são alcançáveis;
- laboratório e projeto representativos abrem;
- busca estática retorna resultado conhecido;
- navegação por teclado permanece funcional;
- assets críticos carregam;
- links internos amostrados resolvem;
- página de segurança e licenciamento está disponível;
- cabeçalho ou rodapé informa status editorial.

## Monitoramento inicial

Durante a janela definida, observar:

- erros 4xx e 5xx;
- rotas não encontradas;
- falhas de assets;
- tempo de resposta e tamanho de páginas;
- regressões de acessibilidade automatizáveis;
- divergência entre digest aprovado e publicado;
- relatos de usuário;
- indisponibilidade do provedor.

Nenhuma telemetria deve registrar busca, conteúdo lido ou identificadores pessoais sem decisão explícita e documentação de privacidade.

## Critérios de abort

Executar rollback imediatamente diante de:

- digest publicado diferente do aprovado;
- segredo ou dado privado exposto;
- rota crítica indisponível;
- navegação principal quebrada;
- barreira crítica de acessibilidade introduzida;
- conteúdo incorreto com risco operacional;
- alteração não autorizada de domínio, DNS ou configuração;
- impossibilidade de identificar o artefato em execução.

## Rollback

1. bloquear novos deploys;
2. registrar razão tipada;
3. selecionar o digest anterior aprovado;
4. restaurar configuração compatível;
5. publicar o artefato anterior;
6. executar smoke tests completos;
7. confirmar rotas e assets;
8. registrar tempo de detecção, contenção e recuperação;
9. abrir incidente e regressão;
10. só retomar deploy após revisão humana.

Rollback de código sem restaurar configuração, redirects, headers, índice de busca e assets compatíveis é incompleto.

## Falhas do provedor

Quando o provedor estiver indisponível:

- não alterar DNS de forma improvisada;
- preservar o último artefato íntegro;
- publicar aviso por canal independente quando possível;
- evitar ampliar permissões para recuperar serviço;
- registrar impacto e decisão;
- testar estratégia alternativa antes de usá-la em incidente real.

## Evidence bundle

- manifesto de release;
- logs sanitizados do build;
- digest do artefato;
- relatórios de testes;
- URL do preview;
- aprovação humana;
- resultado do smoke test;
- evidência do rollback ensaiado;
- riscos residuais;
- decisão final.

## Hard gates

A publicação é `no-go` com CI em outro SHA, artefato sem digest, preview não revisado, rollback não ensaiado, rota crítica quebrada, achado crítico aberto, segredo no build ou ausência de owner.

## Limitações

Este runbook reduz risco de publicação, mas não garante disponibilidade contínua, segurança absoluta ou ausência de falhas do provedor.