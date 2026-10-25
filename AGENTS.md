# eis-ds

Design system visual: primitivos (cor, tipografia, espaço, forma) e elementos básicos, em HTML e CSS puros. Usos previstos: slides, websites, emails, ilustrações e imagens.

v0.1, rascunho. Só o modo claro está definido.

## Leia antes de mexer

1. `docs/tokens.md` — formato e convenções dos tokens (W3C DTCG 2025.10). Obrigatório antes de mexer em token.
2. `docs/visual-guidance/visual-guidance.md` — direção visual, referências e decisões. Obrigatório antes de criar peça ou propor valor.
3. `system/foundations.html`, `elements.html`, `examples.html` — o sistema renderizado.
4. `docs/manual-backlog.md` — regras de uso dos elementos, até o manual existir.

## Estrutura

```
system/                  design system: páginas, tokens, CSS e exemplos
  tokens/                fonte da verdade (.tokens.json)
  css/tokens.css         GERADO. Nunca editar à mão
  css/elements.css       base + elementos básicos
  css/docs.css           layout só das páginas do sistema
  examples/<tipo>/       páginas feitas com o sistema
scripts/build-tokens.py  valida os tokens e gera tokens.css
docs/                    tokens.md, manual-backlog.md
  visual-guidance/       só referência: guidance + imagens
```

## Fluxo

1. Token: edite o `.tokens.json` e rode `python3 scripts/build-tokens.py`. Falhou, não usa.
2. Elemento: muda em `elements.css` e aparece em `elements.html`.
3. Exemplo novo: `system/examples/<tipo>/` + card em `examples.html`.
4. Imagem de referência nova: entra na tabela de fontes do `visual-guidance.md`.

## Regras

- Interface e nomes de arquivo em inglês.
- Tudo responsivo, de 360px a telas largas, sem rolagem horizontal.
- HTML semântico e controles nativos funcionando. Nada de emular tabela ou controle com `div`/`span`.
- Toda classe com prefixo `eis-`.
- Nenhum valor cru no CSS: tudo vem dos tokens.
- Peça não redefine elemento básico; se precisa diferente, muda no sistema.
- Variante muda só cor.
- Exemplos usam só dados fictícios.
- Sem framework (React, Tailwind etc.).
- Decisão visual é proposta e mostrada em HTML antes de virar token.
- Contraste é medido, nunca estimado.
- Arquivos temporários começam com `_` e são apagados depois.
