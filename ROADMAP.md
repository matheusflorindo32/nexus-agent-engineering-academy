---
id: governance.roadmap
title: Roadmap
lang: pt-BR
status: active
version: 0.2.0
---

# Roadmap

## Princípios de priorização

Impacto educacional, evidência, segurança, acessibilidade e manutenção vêm antes da quantidade de integrações. CI verde não implica merge, release, eficácia pedagógica ou prontidão para produção.

## Estados

- `review`: conteúdo ou sistema ainda depende de integração, revisão humana ou piloto;
- `pilot`: não é um valor editorial permitido no frontmatter; pilotos são registrados como evidência externa ao status;
- `stable`: somente após critérios técnicos, pedagógicos, operacionais e humanos.

## Foundation — v0.1

- [x] Arquitetura modular e taxonomia com IDs estáveis.
- [x] Currículo progressivo e contrato de módulo.
- [x] Baseline de segurança, governança e CI.
- [x] Estrutura de adapters de plataforma e tradução.

## Premium Elite curriculum — candidato a v0.2

- [x] Trilha Zero para iniciantes.
- [x] Redesign dos módulos 00–12.
- [x] Governança e redesign dos laboratórios LAB-000 a LAB-1201.
- [x] Projetos Starter e Capstone com rubricas e hard gates.
- [x] Quickstart local sem chave.
- [x] Governança open source, segurança, licenciamento e release.
- [ ] Integrar a pilha de PRs em ordem, com aprovação humana e CI verde em cada SHA final.
- [ ] Executar revisão técnica, de segurança, privacidade, acessibilidade e pedagogia.

## Portal público — candidato a v0.3

- [x] Definir arquitetura do portal com Markdown canônico.
- [x] Definir protocolo de acessibilidade.
- [x] Definir runbook de deploy e rollback.
- [ ] Registrar ADR do gerador estático.
- [ ] Implementar portal mínimo sem autenticação.
- [ ] Gerar previews imutáveis por PR.
- [ ] Automatizar build, rotas, links e verificações acessíveis.
- [ ] Ensaiar rollback do artefato completo.
- [ ] Publicar somente após aprovação humana.

## Validação com estudantes — candidato a v0.4

- [x] Definir protocolo de piloto.
- [ ] Recrutar primeira coorte voluntária e diversificada.
- [ ] Executar quickstart, Trilha Zero, módulos 00–01, LAB-000, LAB-101 e Starter.
- [ ] Registrar ajuda, abandono, erros, acessibilidade e reprodução independente.
- [ ] Corrigir bloqueios e adicionar regressões.
- [ ] Repetir piloto com novo SHA.
- [ ] Obter revisão externa independente.

## Ecosystem — futuro

- [ ] Expandir adapters apenas com contrato, versão verificada e teste comparável.
- [ ] Entregar traduções inglês e espanhol com paridade mensurável.
- [ ] Publicar trilhas para livros, vídeo e formação corporativa.
- [ ] Formar equipe sustentável de maintainers.

## Stable — v1.0

A promoção para `stable` exige cumulativamente:

- currículo integrado e versionado;
- CI verde no mesmo SHA publicado;
- zero bloqueador crítico aberto;
- acessibilidade prática no escopo declarado;
- piloto real repetido e correções incorporadas;
- reprodução independente;
- revisão externa;
- política de release e rollback ensaiados;
- licenciamento e proveniência auditados;
- aprovação humana explícita.

## Bloqueadores absolutos

Não publicar ou promover diante de segredo, vazamento entre escopos, efeito proibido ou duplicado, hard gate ignorado, evidência adulterada, acessibilidade crítica não tratada, rollback incompleto, risco alto ou crítico sem owner ou alegação absoluta sem suporte.