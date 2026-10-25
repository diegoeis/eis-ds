# Tokens — formato e convenções

Os tokens do eis-ds seguem o **Design Tokens Format Module 2025.10** do W3C Design Tokens Community Group (DTCG), junto com os módulos irmãos de Cor e Resolver da mesma versão.

- Format: https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/
- Color: https://www.w3.org/community/reports/design-tokens/CG-FINAL-color-20251028/
- Resolver: https://www.w3.org/community/reports/design-tokens/CG-FINAL-resolver-20251028/

> É um relatório final de Community Group, não um W3C Standard. O próprio documento se declara estável e pronto para implementação. Quando a spec usa MUST/SHOULD, aqui vale o mesmo peso.

Este documento diz **como** escrever tokens. **Quais** tokens existem e por quê fica em `docs/` à medida que a linha visual é definida.

---

## 1. Fonte da verdade

- Os arquivos `.tokens.json` são a única fonte da verdade. Todo o resto (CSS, prompts, documentação visual) é derivado deles.
- Nunca edite um valor direto no CSS derivado. Mude o token e regenere.
- Extensão: `.tokens.json` (a spec recomenda `.tokens` ou `.tokens.json`; usamos a segunda para os editores abrirem como JSON).
- Media type, se algum dia for servido: `application/design-tokens+json`.
- JSON puro (RFC 8259). Sem comentários, sem vírgula sobrando. Explicações vão em `$description`.

## 2. Anatomia de um token

Um objeto com `$value` é um token. Um objeto sem `$value` é um grupo.

```json
{
  "color": {
    "$type": "color",
    "$description": "Cores primitivas. Não usar direto em peças; usar os papéis semânticos.",
    "neutral": {
      "900": {
        "$value": { "colorSpace": "srgb", "components": [0.067, 0.067, 0.067], "hex": "#111111" },
        "$description": "Tinta principal."
      }
    }
  }
}
```

Propriedades reservadas (prefixo `$`):

| Propriedade | Onde | Uso no eis-ds |
|---|---|---|
| `$value` | token | **Obrigatório.** |
| `$type` | token ou grupo | **Obrigatório**, declarado no grupo de nível mais alto possível e herdado pelos filhos. Ferramentas não podem adivinhar o tipo pelo valor. |
| `$description` | token ou grupo | **Obrigatório em todo token.** Diz o papel e quando usar, não repete o valor. |
| `$deprecated` | token ou grupo | `true` ou uma string apontando o substituto. Token não é apagado sem passar por aqui primeiro. |
| `$extensions` | token ou grupo | Dados próprios, sempre sob a chave `com.diegoeis.eis-ds`. Ex.: proveniência da decisão. |
| `$extends` | grupo | Herda outro grupo (deep merge). Evitar, exceto se um modo realmente for uma variação de outro. |
| `$root` | dentro de grupo | Token "padrão" de um grupo que também tem variações (`color.accent.$root`, `color.accent.strong`). |

## 3. Nomes

**Regras da spec (MUST):**
- Nomes não começam com `$`.
- Nomes não contêm `{`, `}` ou `.`.
- Nomes diferenciam maiúsculas de minúsculas.

**Convenções do eis-ds:**
- Tudo em minúsculas, `kebab-case`, sem espaços nem acentos: `line-height`, não `Line Height`.
- Nunca dois nomes que diferem só na caixa.
- Caminho = categoria › propriedade › variante, do geral para o específico: `color.neutral.900`, `space.200`, `font.size.300`.
- Escalas numéricas usam passos de 100 (`100`, `200`, `300`…) para deixar espaço de inserção sem renomear.
- O nome do primitivo descreve **o que é** (`neutral.900`). O nome semântico descreve **para que serve** (`surface.base`, `ink.primary`). Nunca misturar.

**Do caminho para o CSS:** troque `.` por `-` e prefixe com `--`.
`color.neutral.900` → `--color-neutral-900`. Para `$root`, o segmento some: `color.accent.$root` → `--color-accent`.

## 4. Camadas

| Camada | Pasta | Conteúdo | Quem consome |
|---|---|---|---|
| Primitivos | `system/tokens/primitive/` | Valores crus: a paleta, a escala de espaço, as fontes. | Peças, para tudo que não tem papel semântico. |
| Semânticos | `system/tokens/semantic/` | Papéis de cor que carregam significado (`surface`, `ink`, `line`, `signal`) e estilos de texto. Apontam para primitivos por referência. | Peças, sempre que o papel existir. |

- **Semântico só quando acrescenta significado.** Um papel existe se diz *para que serve* uma cor (fundo, texto, linha, sinal) ou se vai mudar entre modos. Um alias que só renomeia um primitivo é complexidade sem ganho e não entra.
- **Usar o primitivo direto é o normal** para espaço, raio, borda, tamanho e peso de fonte, e para a escala de cinza de gráficos (`--color-neutral-200 · 400 · 600 · 900`).
- **Cor de superfície, texto, linha e sinal sempre pelo papel** (`--surface-panel`, `--ink-muted`, `--signal`), nunca pelo primitivo, porque é isso que troca quando um modo novo entrar.
- Ao criar o modo escuro, reavaliar a escala de gráficos: se ela precisar se inverter, aí sim ganha papéis semânticos.

## 5. Referências (aliases)

- Sintaxe padrão: chaves com o caminho completo, `"$value": "{color.neutral.900}"`.
- Uma referência aponta para um **token**, nunca para um grupo. Para o padrão de um grupo, use `{color.accent.$root}`.
- Referências encadeadas são permitidas (`a → b → c`). Referência circular é erro.
- Tipo não precisa ser repetido num alias; ele herda o tipo do token referenciado.
- JSON Pointer (`{ "$ref": "#/color/neutral/900/$value/components/0" }`) só quando for preciso pegar uma parte de um valor composto. No eis-ds isso deve ser raro.

## 6. Tipos permitidos

Todo token usa um tipo da spec. Estes são os que o eis-ds usa:

| Tipo | Valor | Uso no eis-ds |
|---|---|---|
| `color` | objeto `{ colorSpace, components, alpha?, hex? }` | Paleta. |
| `dimension` | `{ "value": 16, "unit": "px" }`, unidade só `px` ou `rem` | Espaço, raio, espessura de linha, tamanho de fonte. `unit` obrigatório até para 0. |
| `fontFamily` | string ou array, do mais preferido ao fallback | Famílias tipográficas. |
| `fontWeight` | número 1–1000 ou alias (`regular`, `bold`…) | Pesos. Preferimos **número**. |
| `number` | número JSON | Entrelinha (multiplicador do tamanho), proporções. |
| `typography` | composto: `fontFamily`, `fontSize`, `fontWeight`, `letterSpacing`, `lineHeight` | Estilos de texto, montados por referência aos primitivos. |
| `border` | composto: `color`, `width`, `style` | Se o sistema tiver bordas. |
| `shadow` | composto: `color`, `offsetX`, `offsetY`, `blur`, `spread`, `inset?` | Somente se o sistema decidir ter sombra. |

Fora de escopo por enquanto: `duration`, `cubicBezier`, `transition`, `gradient`, `strokeStyle`. Entram se e quando forem decididos.

### 6.1 Cor

- `colorSpace`: **`srgb`**. Emails, imagens geradas e a maioria das ferramentas só entendem sRGB. Outro espaço de cor (`oklch`, `display-p3`) só com decisão registrada.
- `components`: `[r, g, b]` de 0 a 1, até 3 casas decimais.
- `hex`: **sempre preenchido** no eis-ds (na spec é opcional). Seis dígitos, minúsculas: `#f05627`. É o valor usado em email, prompts de imagem e conferência humana.
- `components` e `hex` têm de representar a mesma cor. Na dúvida, o `hex` é o que vale e os `components` são recalculados a partir dele.
- `alpha`: só quando for diferente de 1. A transparência fica no `alpha`; o `hex` continua com seis dígitos.

### 6.2 Dimensão

- Unidade canônica: **`px`**. Slides, imagens e email trabalham em pixel, e a conversão para `rem` (÷16) pode ser feita na saída para web.
- Valores inteiros sempre que possível.

## 7. Modos

Modos (claro, escuro, papel…) seguem o **Resolver Module 2025.10**:

- Um arquivo `system/tokens/eis-ds.resolver.json` declara os conjuntos (`sets`) fixos, isto é, os primitivos, e um modificador `mode` com um contexto por modo, cada um apontando para seu arquivo semântico.
- Primitivos são únicos para todos os modos. Só a camada semântica muda.
- Todo modo define **o mesmo conjunto de nomes**. Um papel que existe em um modo existe em todos.
- O modo padrão é declarado em `default`.
- **Hoje só existe o modo claro.** Como um modificador com um único contexto é erro pela spec, o resolver tem apenas dois `sets` (`primitive`, `semantic`). O modificador `mode` entra junto com o segundo modo.
- Observação: a spec do Resolver se contradiz sobre o `version` obrigatório (`2025-10-01` na tabela, `2025-11-01` no texto). Usamos `2025-10-01` até haver errata.

## 8. Do token para o CSS

Cada token vira uma CSS custom property nativa. Regras de conversão:

| Tipo | Saída CSS |
|---|---|
| `color` | o `hex`. Com `alpha` < 1: `rgb(r g b / a)` |
| `dimension` | `16px` |
| `fontFamily` | lista separada por vírgula, nomes com espaço entre aspas, genérico (`sans-serif`, `serif`, `monospace`) sempre por último |
| `fontWeight` | número |
| `number` | número |
| alias | `var(--caminho-do-referenciado)`, para a cadeia continuar viva no CSS |
| `typography` | não existe variável composta em CSS: vira uma variável por propriedade (`--type-body-font-size`, `--type-body-line-height`…) **e** uma classe `.eis-type-<nome>` que aplica todas (`text-transform: uppercase` no `label`) |
| `border`, `shadow` | a forma abreviada do CSS (`1px solid var(--…)`, `0 2px 8px 0 rgb(…)`) |

Modos no CSS: o modo padrão fica em `:root`, os outros em `[data-mode="<nome>"]`, redefinindo **apenas** variáveis semânticas.

A conversão é feita por `scripts/build-tokens.py` (Python, só stdlib), que também roda o checklist do §10 antes de escrever `system/css/tokens.css`. `letterSpacing` fica em `px` porque a spec não aceita `em`; o valor é calculado para o tamanho em que o estilo é usado (ex.: `0.88px` = 0.08em a 11px).

## 9. Fora do CSS

Prompts para geradores de imagem e ferramentas que não leem CSS recebem os valores resolvidos em texto simples: hex, px, nome da fonte. O `$description` de cada token é escrito pensando nesse uso, explicando o papel em linguagem comum.

## 10. Checklist antes de dar um token como pronto

- [ ] `$type` presente (no token ou herdado do grupo)
- [ ] `$description` explica o papel
- [ ] nome em minúsculas e kebab-case, sem `{`, `}`, `.` ou `$`
- [ ] cor com `colorSpace: srgb`, `components` e `hex` coerentes entre si
- [ ] dimensão com `unit`
- [ ] referências resolvem e não formam ciclo
- [ ] se for semântico, existe em todos os modos
- [ ] contraste medido, se for par de texto e fundo
- [ ] proveniência registrada em `$extensions["com.diegoeis.eis-ds"].source`, quando vier de uma referência
