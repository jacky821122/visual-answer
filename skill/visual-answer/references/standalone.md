# standalone — deliver a self-contained HTML file

Use when there is no Artifact tool in this session, or the user asks for a file. It replaces the
design guidance quickstart would give; SKILL.md sections 2–6 still apply on top.

## Delivery
- One self-contained `.html` file named `YYYY-MM-DD-<slug>.html`. Folder, first match wins:
  a location the user names; the "HTML files go to" line in `reader.local.md`;
  `~/visual-answer-pages/`. Create the folder if needed.
- Revisions overwrite the same path.
- Terminal reply: the core takeaway and the absolute path. Don't try to open a browser.

## Baseline
- `<!doctype html>`, `<meta charset="utf-8">`, viewport meta, a `<title>` that is a short name
  for the subject.
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

## Diagrams
Mermaid from a pinned ESM build, theme following the system:

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';
  const dark = matchMedia('(prefers-color-scheme: dark)').matches;
  mermaid.initialize({ startOnLoad: true, theme: dark ? 'dark' : 'default' });
</script>
```

The theme is chosen once at load; that is enough. Offline, the diagram source shows as plain
text — keep node labels short and readable.

## Charts
- Simple bars, meters and sparklines: inline SVG or CSS, coloured with the page's semantic tokens.
- Chart.js only when interaction or many series earn it (`chart.js@4.4.1` from jsDelivr).
- Use the `dataviz` skill if this environment has it; otherwise follow SKILL.md section 4.

## Before replying
- Every resource the page loads follows the rules above (scripts pinned and from the allowed
  CDNs; Google Fonts is the only stylesheet host).
- Run `python3 ${CLAUDE_SKILL_DIR}/scripts/check-page.py <file>` once. It renders desktop and
  phone widths in light and dark and lists overflow, console errors, failed loads, unrendered
  Mermaid, an inert dark theme and low-contrast text. Fix what it lists in one pass; don't loop
  on re-checks. Exit 2 means Playwright isn't installed — skip, and say so in one line.
- Screenshots (`--shots <dir>`) only when the user asks or for evals; have a subagent look at
  them rather than reading images into the main conversation.
- Size is reasonable (no large embedded data URIs without a reason).
