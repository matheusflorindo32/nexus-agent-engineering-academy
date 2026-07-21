---
id: course.zero-track.z06
title: Z06 — Segurança básica e proteção de segredos
lang: pt-BR
status: review
prerequisites: [course.zero-track.z05]
estimated_hours: 4
---

# Z06 — Segurança básica e proteção de segredos

## Para quem é

Pessoas que já entendem arquivos, Git, Python, HTTP e APIs, mas ainda não dominam práticas mínimas de segurança.

## Resultados observáveis

Ao concluir, a pessoa consegue:

- distinguir dado público, interno, confidencial e segredo;
- usar `.env.example` sem expor valores reais;
- explicar menor privilégio, rotação e revogação;
- reconhecer vazamentos em logs, commits e screenshots;
- executar uma varredura local com dados sintéticos;
- registrar incidente sem reproduzir o segredo.

## Em linguagem simples

Um segredo é como a chave da sua casa: não deve aparecer em foto, histórico, conversa pública ou arquivo versionado. Apagar depois não garante que desapareceu do histórico.

## Explicação profissional

Segredos incluem tokens, senhas, chaves privadas, cookies de sessão e credenciais de nuvem. O controle mínimo envolve armazenamento fora do código, escopo limitado, expiração, rotação, revogação e auditoria.

## Demonstração

```bash
python course/zero-track/scripts/scan_synthetic_secrets.py
```

O script usa somente fixtures sintéticas e não lê seu ambiente, home ou credenciais reais.

## Prática guiada

1. Crie uma pasta de laboratório.
2. Adicione `.env.example` com `API_KEY=example-placeholder`.
3. Adicione `.env` ao `.gitignore`.
4. Execute a varredura sintética.
5. Registre o resultado sem copiar nenhum valor sensível.

## Prática independente

Escreva uma política curta contendo: onde segredos podem ficar, quem pode acessar, como revogar e o que fazer em caso de exposição.

## Erros comuns

- confiar apenas no `.gitignore` depois do commit;
- colocar token em screenshot;
- imprimir headers de autorização;
- reutilizar a mesma chave em vários ambientes;
- chamar placeholder realista demais de “exemplo”.

## Stop conditions

Pare imediatamente quando houver suspeita de segredo real. Não abra issue pública. Revogue primeiro, preserve evidências mínimas e use o canal de segurança do projeto.

## Teste de segurança

Explique a resposta correta para: “um token foi commitado e removido no commit seguinte”. A resposta deve incluir revogação, análise do histórico, rotação e comunicação segura.

## Evidência mínima

- `.gitignore` de laboratório;
- `.env.example` sem segredo;
- relatório da varredura sintética;
- política curta de resposta a incidente.

## Critérios de conclusão

- [ ] Não versionei segredo real.
- [ ] Sei por que apagar não basta.
- [ ] Sei revogar antes de investigar longamente.
- [ ] Consigo registrar incidente sem republicar o valor.

## Autoavaliação

Consigo explicar para outra pessoa a diferença entre esconder, remover, rotacionar e revogar uma credencial?