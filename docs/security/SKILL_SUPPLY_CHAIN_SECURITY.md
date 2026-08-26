---
id: security.skill-supply-chain
title: Skill Supply-Chain Security
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Skill Supply-Chain Security

## Objetivo

Definir um processo seguro para descoberta, auditoria, instalação, atualização e rollback de Agent Skills no NEXUS.

## Princípio

Nenhuma Skill externa é confiável por ser popular, oficial ou compatível com um runtime. Toda Skill entra como `UNTRUSTED` até passar por auditoria proporcional ao risco.

## Pipeline de adoção

```text
DISCOVERED
→ STAGED
→ PROVENANCE_VERIFIED
→ LICENSE_REVIEWED
→ CONTENT_AUDITED
→ DEPENDENCIES_AUDITED
→ TESTED
→ HASHED_VERSION
→ APPROVED
→ ATOMIC_PROMOTION
→ RUNTIME_DISCOVERY
→ MONITORED
```

Falhas podem levar a `QUARANTINED` ou `REJECTED`.

## Controles obrigatórios

### Proveniência

Registrar autor/organização, repositório oficial, commit/tag/release, data de acesso e assinatura quando disponível.

### Licença

Registrar licença e compatibilidade com Apache-2.0 e com uso educacional/comercial do repositório. Material source-available não deve ser tratado automaticamente como open source.

### Conteúdo

Auditar `SKILL.md`, scripts, references, assets, hooks, executáveis e instruções para downloads/runtime.

### Permissões

A Skill deve declarar necessidade de filesystem, network, shell, tools, credentials e side effects. Ausência de declaração é falha de revisão, não permissão implícita.

### Dependências

Verificar typosquatting, dependency confusion, pacote abandonado, post-install scripts, versões vulneráveis e origem de artefatos.

### Prompt injection

Tratar texto da própria Skill como código/instrução privilegiada. Buscar instruções ocultas, escalada de confiança, tentativa de desativar políticas, exfiltração e carregamento dinâmico não auditado.

## Atualização atômica

Nunca sobrescrever uma Skill ativa in-place.

Estratégia preferida:

```text
skills/.staging/<name>/<version>/
→ validate
→ audit
→ test
→ compute hash
→ move/rename atomically to immutable version path
→ update registry pointer
```

Se o filesystem não garantir atomicidade, usar lock/transaction equivalente e documentar risco residual.

## Manifest mínimo proposto

Campos adicionais só serão promovidos após ADR e revisão de compatibilidade com a especificação oficial adotada.

```yaml
name: example
version: 0.1.0
source:
  repository: https://example.invalid/repo
  commit: abc123
license: Apache-2.0
permissions:
  network: none
  filesystem: read-only
  shell: false
risk: low
status: experimental
content_hash: sha256:...
```

## Classificação

- `APPROVED`
- `APPROVED_WITH_RESTRICTIONS`
- `EXPERIMENTAL`
- `QUARANTINED`
- `REJECTED`

## Loader requirements

O loader futuro deve distinguir:

- conteúdo inválido;
- arquivo ausente transitório;
- I/O/resource exhaustion;
- hash mismatch;
- versão incompatível;
- Skill revogada.

Erro transitório não deve ser reportado como “Skill inválida” sem evidência de parsing/schema.

## Rollback

O registry deve preservar a versão anterior aprovada até que a nova versão tenha sido carregada e validada pelo runtime. Rollback não pode depender de baixar novamente a versão antiga.

## Critério de adoção

Nenhuma Skill externa deve ser usada em projeto real até existir pelo menos: provenance record, licença, hash, permissões, teste mínimo e decisão explícita de status.