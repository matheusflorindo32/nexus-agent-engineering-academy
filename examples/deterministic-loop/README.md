---
id: example.deterministic-loop
title: Exemplo — Loop determinístico
lang: pt-BR
status: stable
---

# Loop determinístico

Este exemplo usa apenas a biblioteca padrão do Python e demonstra budget, no-progress e resultado tipado.

```bash
python examples/deterministic-loop/loop.py success
python examples/deterministic-loop/loop.py stalled
```

O “modelo” é uma fixture determinística. Isso torna testes reproduzíveis antes de introduzir um SDK.

