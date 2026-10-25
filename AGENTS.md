# eis-ds

Design system visual. Nesta fase contém os **primitivos** (cor, tipografia, espaçamento, forma) e os **elementos básicos** (botão, chip, campos, escolhas, tabela, painel, navegação, lista). Componentes compostos e frameworks ficam para uma fase posterior.

Usos previstos: slides, websites, emails, ilustrações e imagens em geral (artigos, peças de design).

## Status

v0.1, rascunho. Só o modo claro está definido. Valores podem mudar; decisões ficam em `docs/visual-guidance/visual-guidance.md` §7.

## Leia antes de mexer

1. `docs/tokens.md` — formato e convenções dos tokens (W3C DTCG 2025.10). **Obrigatório** antes de criar ou editar qualquer token.
2. `docs/visual-guidance/visual-guidance.md` — direção visual, referências e de onde veio cada escolha. **Obrigatório** antes de criar qualquer peça ou propor um valor.
3. `system/foundations.html`, `system/elements.html` e `system/examples.html` — o sistema renderizado. Navegam entre si pelo cabeçalho.

## Estrutura

```
eis-ds/
  AGENTS.md                  este arquivo — regras para qualquer agente
  CLAUDE.md                  aponta para AGENTS.md
  system/                    o design system: documentação, CSS, tokens e templates
    foundations.html         primitivos: cor, contraste, tipo, espaço, forma, motivos
    elements.html            elementos básicos, todos funcionando
    examples.html            índice dos exemplos, com preview
    examples/                páginas e templates feitos COM o sistema
      dashboard/             tasks-work.html
    tokens/                  fonte da verdade, formato DTCG (.tokens.json)
      primitive/             valores crus: color, dimension, font
      semantic/              papéis (light) e estilos de texto, só por referência
      eis-ds.resolver.json   ordem de resolução (Resolver Module)
    css/
      tokens.css             GERADO dos tokens. Nunca editar à mão
      elements.css           base + elementos básicos. Escrito à mão, só usa tokens
      docs.css               layout das páginas do próprio sistema (não usar em peças)
  scripts/
    build-tokens.py          valida system/tokens e gera system/css/tokens.css (stdlib)
  docs/
    tokens.md                formato e convenções dos tokens
    visual-guidance/         só referência: direção visual e de onde ela veio
      visual-guidance.md     direção visual, fontes, decisões
      references/            imagens de referência, uma pasta por fonte
        te/                  Teenage Engineering (âncora)
        pinterest/           moodboard de retrofuturismo
        interface/           referências de UI; main-* são as principais, board/ o resto
        palette/             referências de cor pontuais
```

Toda imagem nova em `docs/visual-guidance/references/` entra na tabela de fontes do `visual-guidance.md`. Exemplo novo vai em `system/examples/<tipo>/` e ganha um card em `system/examples.html`. Uma peça carrega, nesta ordem, `system/css/tokens.css`, `system/css/elements.css` e depois só o CSS de layout dela, por caminho relativo (de `system/examples/<tipo>/`: `../../css/`). Pastas novas entram nesta seção.

## Fluxo

1. Edite o `.tokens.json` (nunca o CSS gerado).
2. `python3 scripts/build-tokens.py` — valida (tipo, descrição, nome, hex × components, referências, ciclos) e regenera `system/css/tokens.css`. Falha = não usar.
3. Elemento novo ou alterado: em `system/css/elements.css` **e** demonstrado em `system/elements.html`.
4. Abra `foundations.html` e `elements.html` e confira nas três larguras.

## Regras

### Idioma e responsividade
- **Interface e nomes de arquivo sempre em inglês.** Todo texto de UI (menus, rótulos, botões, estados, datas, mensagens) e todo nome de arquivo ou pasta. O conteúdo vindo das fontes do usuário (tarefas, notas, nomes de eventos) mantém o idioma original.
- **Tudo sempre responsivo.** Toda peça em HTML funciona de 360px até telas largas, sem rolagem horizontal, texto cortado ou elemento sobreposto. Layout fluido (`grid`, `flex`, `minmax`, `clamp()`), com breakpoints só onde a composição quebra. Em grid automático, o mínimo é sempre `minmax(min(<px>,100%),1fr)`: um `minmax(<px>,1fr)` puro estoura quando o container fica menor que o mínimo. Slides escalam pelo próprio container (`cqw`). Uma peça só está pronta depois de renderizada e conferida em **375px, 768px e 1440px**, e arrastando a janela entre elas.

### HTML
- **HTML semântico, sempre.** Use o elemento que já carrega o significado: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `h1`–`h6` em ordem, `ul`/`ol` para listas, `dl` para pares rótulo–valor, `time datetime` para datas e horas, `figure`, `details`/`summary` para o que abre e fecha. Sidebar é `<aside>` (com `aria-label`), mesmo quando no mobile vira barra no topo; `<header>` é só o cabeçalho da página ou de uma seção.
- **Dado tabular é `<table>`**, com `thead`, `tbody`, `th scope`. Nunca emular tabela, lista ou formulário com `div`. Se a tabela precisa virar cartão no mobile, muda-se o CSS, não o HTML.
- **Controles são nativos e funcionam.** Checkbox é `<input type="checkbox">` com `<label for>`; opções exclusivas são `<input type="radio">` dentro de `<fieldset>` + `<legend>`; switch é checkbox com `role="switch"`; seleção é `<select>`; ação é `<button type="button">`; navegação é `<a href>`; formulário é `<form>`. Estilize o nativo (`appearance:none`), nunca o substitua por `span`. Foco visível sempre (`:focus-visible`).
- **Acessível por padrão.** Todo controle tem rótulo; elementos só visuais levam `aria-hidden`; gráficos têm `role="img"` + `aria-label` com o resumo dos dados; campo inválido leva `aria-invalid` + `aria-describedby` apontando a mensagem.

### CSS
- **Toda classe começa com `eis-`.** Componentes `eis-panel`, partes `eis-panel__head`, variantes `eis-chip--signal`, estados `eis-is-active`. Estilizar por elemento semântico é preferível a criar classe.
- **Nenhum valor cru.** Cor, tamanho de fonte, peso, espaçamento, raio e borda vêm de `var(--…)` do `tokens.css`. Se falta um valor, crie o token, não o número. Medidas de componente (altura de botão, tamanho de ícone) e meio passo de espaço em dado denso (`calc(var(--space-100) / 2)`) são as exceções.
- **Não redefina elemento básico na peça.** Botão, chip, campo, tabela e painel vêm de `elements.css`. Se a peça precisa de algo diferente, o elemento muda no sistema.
- **Variante muda só cor**, via custom properties locais (`--bg`, `--fg`, `--bd`). Nunca estrutura, tamanho, raio ou comportamento.
- **Botão age, chip descreve.** Botão: retângulo, raio 4px, mono em caixa alta, tem hover. Chip: pílula, caixa normal, sem hover, nunca clicável. Status, categoria e etiqueta são sempre chip.
- **Célula de tabela é sempre `vertical-align: middle`** (`th` e `td`).
- **Toda borda e todo fio usam `--line`.** Contorno de controle interativo usa `--ink-muted` (WCAG 3:1). Tinta cheia nunca contorna forma.
- **Tokens no padrão W3C DTCG 2025.10.** Os `.tokens.json` são a única fonte da verdade; CSS e prompts são derivados. Detalhes em `docs/tokens.md`.
- **Sem framework.** Nada de React, Tailwind ou bibliotecas. O consumo é por CSS custom properties nativas.

### Processo
- **HTML standalone.** Abre direto no navegador; as únicas dependências são os CSS de `system/css/` e as fontes.
- **Agnóstico de plataforma.** Nada aqui deve depender de um agente, editor ou ferramenta específica.
- **Conceito antes de arquivo.** Decisões visuais são propostas e aprovadas antes de virarem token.
- **Escolhas visuais são mostradas, não descritas.** Opções em HTML lado a lado, variando um único eixo.
- **Proveniência.** Cada decisão registra de qual referência veio.
- **Regra dita para um caso vale para o sistema.** Registrar aqui ou em `docs/`, não só no arquivo em edição.
- **Contraste é medido, nunca estimado.**
- Arquivos temporários de amostra começam com `_` e são apagados após a decisão.
