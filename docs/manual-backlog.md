# Manual backlog

Regras de uso de elementos e de HTML/CSS que vão para o **manual do design system**, quando ele for escrito. Ficam aqui para não se perderem e para não pesar o `AGENTS.md`. As regras já valem; só falta o lugar definitivo.

## HTML
- Sidebar é `<aside>` com `aria-label`, mesmo quando no mobile vira barra no topo. `<header>` é só o cabeçalho da página ou de uma seção.
- Use os elementos semânticos: `ul`/`ol` para listas, `dl` para pares rótulo–valor, `time datetime` para datas e horas, `figure`, `details`/`summary` para o que abre e fecha, `h1`–`h6` em ordem.
- Tabela usa `thead`, `tbody`, `th scope`. Se precisa virar cartão no mobile, muda-se o CSS, não o HTML.
- Controles: checkbox é `<input type="checkbox">` + `<label for>`; opções exclusivas são radio dentro de `<fieldset>` + `<legend>`; switch é checkbox com `role="switch"`; seleção é `<select>`; ação é `<button type="button">`; navegação é `<a href>`. Estilizar o nativo com `appearance:none`.
- Acessibilidade: elementos só visuais levam `aria-hidden`; gráficos têm `role="img"` + `aria-label` com o resumo dos dados; campo inválido leva `aria-invalid` + `aria-describedby`; foco visível com `:focus-visible`.

## CSS
- Nomenclatura: componente `eis-panel`, parte `eis-panel__head`, variante `eis-chip--signal`, estado `eis-is-active`. Preferir estilizar o elemento semântico a criar classe.
- Exceções a "nenhum valor cru": medidas de componente (altura de botão, tamanho de ícone) e meio passo de espaço em dado denso (`calc(var(--space-100) / 2)`).
- Variante usa custom properties locais (`--bg`, `--fg`, `--bd`).
- Grid automático usa `minmax(min(<px>,100%),1fr)`; o `minmax(<px>,1fr)` puro estoura quando o container fica menor que o mínimo.
- Slides escalam pelo próprio container (`cqw`).
- Uma peça carrega `tokens.css`, depois `elements.css`, depois só o CSS de layout dela.

## Elementos
- **Botão age, chip descreve.** Botão: retângulo, raio 4px, mono em caixa alta, tem hover. Chip: pílula, caixa normal, cursor padrão, sem hover. Status, categoria e etiqueta são sempre chip.
- Célula de tabela (`th` e `td`) sempre `vertical-align: middle`.
- Toda borda e todo fio usam `--line`. Contorno de controle interativo usa `--ink-muted` (WCAG 3:1). Tinta cheia nunca contorna forma.
- Hover: botão muda o fundo (secundário e ghost vão para o canvas; primário e signal clareiam 20/15% em direção ao painel via `color-mix`, o que mantém o contraste do texto). Checkbox, radio e switch escurecem o contorno e ganham fundo canvas; marcados clareiam. Botão ganha um glow no hover na cor da própria variante (`--glow`: cinza no secundário, preto no primário, laranja no signal; ghost e desabilitado sem glow). Transição de 120ms, linear.
- Chip hachurado marca o que não conta mais: cancelado, bloqueado.
- Uma ação primária por tela; botão `--signal` só para a ação que é o próprio sinal (gravar, publicar).

## Verificação
- Renderizar em 375, 768 e 1440px e arrastar a janela entre elas; sem rolagem horizontal, texto cortado ou sobreposição.
