# standalone — deliver a self-contained HTML file

Use when there is no Artifact tool in this session, or the user asks for a file. It replaces the
design guidance quickstart would give; SKILL.md sections 2–6 still apply on top.

## Delivery
- One self-contained `.html` file named `YYYY-MM-DD-<slug>.html`. Folder, first match wins: a
  location (folder or full file path) the user names; the "HTML files go to" line in
  `reader.local.md`; `~/visual-answer-pages/`. Create the folder if needed.
- Revisions overwrite the same path.
- Terminal reply: the core takeaway and the absolute path. Don't try to open a browser.

## Baseline
- `<!doctype html>`, `<meta charset="utf-8">`,
  `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`, and
  a `<title>` that is a short name for the subject.
- A small reset, since no host injects one: `:root{color-scheme:light}` (`dark` in the dark
  block) with `padding-block: env(safe-area-inset-top,0px) env(safe-area-inset-bottom,0px)`;
  `body{margin:0}` at 16px/1.6; `img,video{max-width:100%;height:auto}`, `svg{max-width:100%}`;
  `[hidden]{display:none!important}`. Sticky or fixed bars add the safe-area insets themselves.
- Colour tokens on `:root`; a dark set under `@media (prefers-color-scheme: dark)`; `body` gets
  an explicit background and text colour from the tokens. Design both themes.
- System font stack for body text; one Google Font for display type is optional (a
  `fonts.googleapis.com` stylesheet link — it has no version to pin, and that is fine).
- One reading column, max ~860px, 16px side gutter; no horizontal scroll at phone width (wide
  tables scroll inside their own wrapper).
- Everything inline (CSS, SVG, data). External scripts only from `cdn.jsdelivr.net/npm/` or
  `cdnjs.cloudflare.com`, always with an exact version, never `@latest` or a bare major.
  These rules cover what the page loads (`<script src>`, `import`, `<link href>`), not URLs
  shown to the reader as text.

## Design

If this environment has the `artifact-design` skill, load it and skip this section; it is the
fuller source these rules are distilled from.

Treat every page as a small identity job: decide palette, type and rhythm for *this* subject.

**Plan as tokens first.** Open the `<style>` with the plan itself: a one-line comment naming the
layout idea, then 4–6 base colour tokens (ground, text, muted, line, accent) plus the semantic
ones from SKILL.md section 4, and 2–3 font tokens on `:root`. Every later rule reads from
them; a literal hex in a component rule is a bug. Tint the neutrals slightly toward the accent
(a flat #888 grey reads as unchosen). The dark block redefines the same token names (plus
`color-scheme`) and nothing else; tune it on its own (lift the accent, soften pure white text)
instead of inverting the light set.

**Type.** Pick a display face from the subject's world and use it sparingly (title, key numbers,
section heads); body stays a calm, legible face. Fix a scale of 4–5 steps (e.g. 0.85 / 1 / 1.25 /
1.6 / 2.4rem) and never invent sizes in between. Body line-height ~1.6, measure ~65ch;
headings get `text-wrap: balance`; small uppercase labels get ~0.06em tracking. Digits that line
up in tables or stats use `font-variant-numeric: tabular-nums`. Always give a fallback stack.

**Spacing.** One spacing scale (e.g. 4/8/12/16/24/32/48px) as tokens. Siblings are spaced by
`gap` on a flex/grid parent, not margins on children. Keep selectors flat so a section rule and
a component rule don't fight over the same padding.

**Components.** Borders, fills, radius and shadow say "this is a separate object"; give them to
the few blocks that are, not to every section. Repeated items (cards, rows, chips) share edges,
padding and element order. Let content set heights; size grids so every row ends up full.
Clipped text is a defect: long strings wrap or scroll in their own box. Interactive things look
clickable and have a visible `:focus-visible` state.

**Structure means something.** Numbers like 01/02/03, eyebrows and dividers only when they encode
real order or grouping. Reserve a row of big-stat tiles for pages whose answer is those numbers.

**Avoid the stock AI look** unless the user asks for it: beige paper + serif + rust accent;
black page with one neon accent; newspaper hairlines; purple-blue gradient hero; Inter/Space
Grotesk by default; emoji as section icons; everything centred; one large radius on every box;
a coloured stripe down the side of each rounded card.

**Copy.** Name things the way the reader knows them, not by internals. Active verbs on controls.
Plain, short sentences; no em-dash asides, "not X but Y" turns, colon reveals, or filler phrases.

**At rest.** Everything readable is visible on load; animations start from a visible state and
honour `prefers-reduced-motion`. Size the opener to its content, never `100vh`.

**Common mistakes.** Colour defined only inside the dark block; transparent `body`; a padding
shorthand that wipes the side gutter; a flex child with long text missing `min-width: 0`; chart
labels that don't sit on the chart's own scale or use colours that vanish in one theme.

## Diagrams
Write Mermaid as `<pre class="mermaid">` blocks with this loader (pinned ESM build, theme
following the system):

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';
  const dark = matchMedia('(prefers-color-scheme: dark)').matches;
  mermaid.initialize({ startOnLoad: true, theme: dark ? 'dark' : 'default' });
</script>
```

Then run `python3 ${CLAUDE_SKILL_DIR}/scripts/render-mermaid.py <file>`. It replaces each block
with inline SVG (a light and a dark copy, switched by CSS, coloured from the page's body
background, body text colour, `--accent` — or the first heading's colour — and body font), keeps
the source inside the figure, and drops the loader — so diagrams show with no JavaScript or
network, including iOS file previews. After editing a diagram's source, run it again. Exit 2 (no
Playwright) leaves the loader in place: diagrams then render in a browser but not in previews or
offline, so keep node labels short and readable as plain text.
Prefer top-down layouts (`flowchart TD`): a wide left-to-right chart has to scroll sideways on a
phone.

## Charts
- Simple bars, meters and sparklines: inline SVG or CSS, coloured with the page's semantic tokens.
- Chart.js only when interaction or many series earn it (`chart.js@4.4.1` from jsDelivr).
- Use the `dataviz` skill if this environment has it; otherwise follow SKILL.md section 4.

## Before replying
- After `render-mermaid.py`, run `python3 ${CLAUDE_SKILL_DIR}/scripts/check-page.py <file>`
  once. It renders desktop and phone widths in light and dark and lists overflow, console
  errors, failed loads, unrendered Mermaid, an inert dark theme, low-contrast text and loads
  that break the rules above. Fix what it lists in one pass; don't loop on re-checks — whatever
  remains after that pass stays, mentioned in the reply only if it hurts reading. Exit 2 means
  Playwright isn't installed — skip, and say so in one line.
- Screenshots (`--shots <dir>`) only when the user asks or for evals; have a subagent look at
  them rather than reading images into the main conversation.
- Size is reasonable (no large embedded data URIs without a reason).
