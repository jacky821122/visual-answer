#!/usr/bin/env python3
"""Pre-render a page's Mermaid diagrams into inline SVG, in place.

Usage: render-mermaid.py PAGE.html

Each <pre class="mermaid"> block becomes a <figure class="va-diagram"> holding a light
and a dark SVG (CSS shows the one matching the system theme) plus the source in an inert
<script type="text/x-mermaid">, so the script can be run again after edits. The Mermaid
loader script is removed: the page then needs no JavaScript or network to show diagrams
(iOS file previews, offline viewing). Diagram colours and font come from the page
itself (background, text, --accent or the heading colour) for each theme. On narrow screens a wide diagram scrolls
sideways rather than shrinking its labels below ~12px.
Exit 0 = done (or nothing to do), 1 = a diagram failed, 2 = Playwright not available.
"""
import html
import pathlib
import re
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("SKIP: Playwright not installed — diagrams stay client-rendered")
    sys.exit(2)

MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs"
PRE = re.compile(r'<pre class="mermaid"[^>]*>(.*?)</pre>', re.S)
FIG = re.compile(r'<figure class="va-diagram">.*?<script type="text/x-mermaid">(.*?)</script>\s*</figure>', re.S)
LOADER = re.compile(r'<script type="module">[^<]*mermaid[^<]*</script>\s*', re.S)
STYLE = ('<style id="va-diagram-style">.va-diagram{margin:1.5rem 0;overflow-x:auto}'
         '.va-diagram svg{height:auto}.va-diagram .va-dark{display:none}'
         '@media (prefers-color-scheme: dark){.va-diagram .va-light{display:none}'
         '.va-diagram .va-dark{display:block}}</style>')

# Reads the page's own colours and font so diagrams look like part of the page rather
# than Mermaid's stock lavender. Accent = --accent if defined, else the first heading colour.
PALETTE = """
() => {
  const toRgb = c => { const m = (c || '').match(/[\\d.]+/g); return m ? m.slice(0, 3).map(Number) : null; };
  const probe = document.createElement('i');
  document.body.appendChild(probe);
  const resolve = c => { probe.style.color = ''; probe.style.color = c; return toRgb(getComputedStyle(probe).color); };
  const root = getComputedStyle(document.documentElement), body = getComputedStyle(document.body);
  let bg = toRgb(body.backgroundColor);
  if (!bg || /rgba\\(.*, 0\\)/.test(body.backgroundColor)) bg = toRgb(root.backgroundColor) || [255, 255, 255];
  const fg = toRgb(body.color) || [0, 0, 0];
  const v = root.getPropertyValue('--accent').trim();
  const h = document.querySelector('h2, h1');
  const accent = (v && resolve(v)) || (h && toRgb(getComputedStyle(h).color)) || fg;
  probe.remove();
  const mix = (a, b, t) => a.map((x, i) => Math.round(x * t + b[i] * (1 - t)));
  const hex = c => '#' + c.map(x => x.toString(16).padStart(2, '0')).join('');
  return {
    background: hex(bg), mainBkg: hex(mix(accent, bg, 0.12)), primaryColor: hex(mix(accent, bg, 0.12)),
    primaryBorderColor: hex(mix(accent, bg, 0.7)), primaryTextColor: hex(fg), textColor: hex(fg),
    nodeTextColor: hex(fg), lineColor: hex(mix(fg, bg, 0.55)), clusterBkg: hex(mix(fg, bg, 0.04)),
    clusterBorder: hex(mix(fg, bg, 0.2)), titleColor: hex(fg), edgeLabelBackground: hex(bg),
    fontFamily: body.fontFamily, fontSize: '15px',
  };
}
"""

RENDER = """
async ([src, vars, id]) => {
  const { default: mermaid } = await import('%s');
  mermaid.initialize({ startOnLoad: false, theme: 'base', themeVariables: vars,
                       htmlLabels: false, flowchart: { htmlLabels: false } });
  const { svg } = await mermaid.render(id, src);
  return svg;
}
""" % MERMAID


def legible(svg):
    """Let the diagram shrink to fit, but not below 75% of its natural width (labels stay
    ~12px); past that the figure scrolls sideways instead."""
    m = re.search(r'viewBox="[\d.-]+ [\d.-]+ ([\d.]+)', svg)
    if not m:
        return svg
    w = float(m.group(1))
    style = f'width:100%;max-width:{w:.0f}px;min-width:{w * 0.75:.0f}px'
    head, rest = svg.split(">", 1)
    head = re.sub(r'\sstyle="[^"]*"', "", head)
    return f'{head} style="{style}">{rest}'


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    path = pathlib.Path(sys.argv[1]).resolve()
    text = path.read_text(encoding="utf-8")

    # Sources in page order: fresh <pre> blocks and previously rendered figures.
    blocks = [(m.span(), html.unescape(m.group(1)).strip()) for m in PRE.finditer(text)]
    blocks += [(m.span(), m.group(1).strip()) for m in FIG.finditer(text)]
    blocks.sort()
    if not blocks:
        print("nothing to do: no Mermaid blocks")
        return 0

    out, pos, failed = [], 0, 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        palette = {}
        for scheme in ("light", "dark"):
            ctx = browser.new_context(color_scheme=scheme)
            probe = ctx.new_page()
            probe.goto(path.as_uri())
            palette[scheme] = probe.evaluate(PALETTE)
            ctx.close()
        page = browser.new_page()
        page.set_content("<!doctype html><html><body></body></html>")
        for i, ((start, end), src) in enumerate(blocks):
            try:
                light = legible(page.evaluate(RENDER, [src, palette["light"], f"va-m{i}-light"]))
                dark = legible(page.evaluate(RENDER, [src, palette["dark"], f"va-m{i}-dark"]))
            except Exception as e:  # keep the original block so nothing is lost
                failed += 1
                print(f"diagram {i + 1}: render failed: {str(e).splitlines()[0][:160]}")
                out.append(text[pos:end])
                pos = end
                continue
            out.append(text[pos:start])
            out.append(f'<figure class="va-diagram"><div class="va-light">{light}</div>'
                       f'<div class="va-dark">{dark}</div>'
                       f'<script type="text/x-mermaid">{src}</script></figure>')
            pos = end
        browser.close()
    out.append(text[pos:])
    result = "".join(out)

    if not PRE.search(result):
        result = LOADER.sub("", result)
    if 'id="va-diagram-style"' not in result:
        result = result.replace("</head>", STYLE + "</head>", 1)
    path.write_text(result, encoding="utf-8")
    print(f"rendered {len(blocks) - failed}/{len(blocks)} diagrams into inline SVG")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
