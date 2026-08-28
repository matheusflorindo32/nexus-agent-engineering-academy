---
id: audit.nexus-control-plane-v1-review-scorecard
content_id: audit.nexus-control-plane-v1-review-scorecard
version: 1.0.0
title: Revisão adversarial — NEXUS Control Plane V1
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# Revisão adversarial — NEXUS Control Plane V1

## Escopo

Revisão separada da implementação declarativa do Control Plane V1. Esta revisão não é auditoria humana independente nem certificação externa; é uma passada de verificação com papel adversarial, complementada por CI real.

## Evidência TDD

### RED 1 — contratos ausentes

- commit: `b1fcb9664b67e14ec4bb7486043350ebf32696d5`;
- NEXUS Quality run: `33192038733` — failure;
- `unittest`: 62 testes, 1 failure + 9 errors;
- causa observada: nove artefatos `.nexus` ausentes, com `FileNotFoundError` e lista explícita de arquivos faltantes;
- repository validator passou antes da falha;
- Secret Scan passou;
- evidence artifact: `9694146965`, SHA-256 do ZIP `7adfc0186bb5b1113e37c8c3c6991ecf95fc8ffe45e85648a8033bd5976953cf`.

### GREEN 1 — contratos declarativos

- commit: `a5296f6713c0243a7583d4dc9af8aba8d7c85226`;
- NEXUS Quality run `33192249700` — success;
- Documentation quality run `33192249776` — success;
- Security - Secret Scan run `33192249694` — success.

### RED 2 — entrypoint não roteava para o Control Plane

- commit: `e3e3538dd98962c1b759dc46e6c7f33ef9521255`;
- Documentation quality run `33192394335` — failure;
- 63 testes, exatamente 1 failure;
- causa observada: `AGENTS.md` não continha `NEXUS Spec-Driven Control Plane` nem referências `.nexus` exigidas pelo novo contrato;
- todos os demais contratos do Control Plane passaram.

## Revisão adversarial por requisito

| Controle | Ataque/pergunta | Resultado |
|---|---|---|
| Constitution | um framework upstream pode sobrescrever autoridade humana? | BLOQUEADO por Human Authority e precedence explícita no entrypoint |
| Rigor | um projeto pode declarar L0 para escapar de política crítica? | BLOQUEADO: política de domínio pode elevar, nunca reduzir rigor |
| Standards registry | IDs duplicados ou decisão fora da taxonomia passam? | BLOQUEADO por teste automatizado |
| Schemas | contratos aceitam campos arbitrários silenciosamente? | BLOQUEADO no schema: `additionalProperties=false` |
| Traceability | estados ilimitados/ambíguos podem aparecer? | BLOQUEADO por conjunto fechado testado |
| Hooks | hook default pode fazer merge/deploy/delete/rotate credential? | BLOQUEADO por teste + lista de autorização humana explícita |
| Release gate | `PASS` autoriza merge? | NÃO; `human_merge_authority=true`, `auto_merge_allowed=false` |
| Upstream | projeto popular vira dependência automaticamente? | NÃO; decisões e provenance são explícitas |

## Security review

### Pontos positivos

- nenhuma nova dependência externa;
- nenhum código upstream copiado;
- hooks V1 são política declarativa, não executor privilegiado;
- merge/deploy/delete/credential rotation permanecem fora de autoridade automática;
- schemas e receipts não incluem requisito de armazenar secrets;
- Secret Scan foi executado nos ciclos observados.

### Riscos residuais

1. `main` continuava sem branch protection na auditoria de base; esta branch não altera configuração administrativa do GitHub.
2. Os JSON Schemas são contratos versionados, mas o V1 não adiciona uma biblioteca JSON Schema completa; os testes stdlib validam invariantes centrais, não toda a semântica Draft 2020-12.
3. Hooks são declarativos; não existe ainda um hook engine NEXUS que prove execução consistente em diferentes agentes/IDEs.
4. Traceability V1 define o modelo, mas não constrói code graph/symbol graph automático como SpecD.
5. O benchmark 0–100 é documental/arquitetural e específico ao NEXUS; não mede runtime, velocidade ou qualidade de modelo.
6. Kiro entra apenas como influência conceitual até licença específica de qualquer artefato reutilizado ser confirmada.
7. Revisão verdadeiramente independente por outro humano/modelo não foi comprovada nesta rodada; o PR deve permanecer sujeito a revisão humana antes de merge.

## Avaliação

- arquitetura: 9.4/10;
- minimização de lock-in: 9.7/10;
- testabilidade V1: 9.4/10;
- segurança do escopo declarativo: 9.3/10;
- provenance/governança: 9.5/10;
- automação de traceability: 7.0/10 (intencionalmente futura);
- confiança global no escopo V1: **9.3/10**.

## Gate proposto

`PASS` para os contratos declarativos somente se o head final mantiver NEXUS Quality, Documentation quality, Secret Scan e Provider Runtime Trial herdado verdes.

`GO` posterior: Runtime Security Convergence V1.1 e trials isolados de traceability/context standards, sem promover frameworks inteiros automaticamente.

Merge permanece decisão humana.
