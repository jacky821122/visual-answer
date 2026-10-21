#!/usr/bin/env python3
# /// script
# dependencies = ["playwright"]
# ///
"""Render a standalone page and report layout/theme problems as text.

Usage: check-page.py PAGE.html [--shots DIR] [--artifact]

Renders desktop (1280px) and phone (375px) widths in light and dark, then lists:
horizontal overflow, console/page errors, failed loads, Mermaid blocks that did
not render, a dark theme that changes nothing, low-contrast text, and loads that
break the standalone loading rules (allowed hosts, exact versions).
--artifact: the page is an Artifact source file; the host renders its Mermaid,
so unrendered Mermaid and standalone loading rules are not reported.
Exit 0 = clean, 1 = issues found, 2 = Playwright not available.
PLAYWRIGHT_CHROMIUM=<browser binary> uses that browser instead of Playwright's own build.
"""
import argparse
import os
import pathlib
import re
import sys
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("SKIP: Playwright not installed (pip install playwright && playwright install chromium)")
    sys.exit(2)

VIEWPORTS = {"desktop": (1280, 900), "phone": (375, 800)}
SCRIPT_HOSTS = {"cdn.jsdelivr.net", "cdnjs.cloudflare.com"}
FONT_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}


def load_rule_problem(url):
    """Why a loaded URL breaks standalone.md's loading rules, or None."""
    u = urlparse(url)
    if u.scheme in ("file", "data", "blob", "about"):
        return None
    if u.hostname in FONT_HOSTS:
        return None
    if u.hostname not in SCRIPT_HOSTS:
        return "host not allowed"
    if not re.search(r"@\d+\.\d+\.\d+|/\d+\.\d+\.\d+/", u.path):
        return "no exact version"
    return None

# Runs in the page: overflow offenders, Mermaid state, body colours, low-contrast text.
PROBE = """
() => {
  const vw = document.documentElement.clientWidth;
  const overflow = [];
  if (document.documentElement.scrollWidth > vw + 1) {
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 && r.width > 0) {
        let p = el.parentElement, scrolls = false;
        while (p && p !== document.body) {
          const o = getComputedStyle(p).overflowX;
          if (o === 'auto' || o === 'scroll' || o === 'hidden') { scrolls = true; break; }
          p = p.parentElement;
        }
        if (!scrolls) overflow.push(el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '') + ` (${Math.round(r.right)}px)`);
      }
      if (overflow.length >= 3) break;
    }
  }
  const mermaid = [...document.querySelectorAll('.mermaid')].map(b =>
    !b.querySelector('svg') ? 'not rendered' : (/syntax error/i.test(b.textContent) ? 'syntax error' : 'ok'));

  const parse = c => { const m = c.match(/[\\d.]+/g); return m ? m.map(Number) : [0, 0, 0, 0]; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) {
      const c = parse(getComputedStyle(e).backgroundColor); if (c.length < 4 || c[3] > 0.5) return c; }
    return [255, 255, 255]; };
  const low = [];
  let checked = 0;
  for (const el of document.body.querySelectorAll('*')) {
    if (checked >= 400) break;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own || el.closest('.mermaid, svg')) continue;
    const st = getComputedStyle(el);
    if (st.visibility === 'hidden' || st.display === 'none' || el.getClientRects().length === 0) continue;
    checked++;
    const a = lum(parse(st.color)), b = lum(bgOf(el));
    const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    const large = parseFloat(st.fontSize) >= 24 || (parseFloat(st.fontSize) >= 18.66 && +st.fontWeight >= 700);
    if (ratio < (large ? 3 : 4.5)) low.push(`${el.tagName.toLowerCase()} "${el.textContent.trim().slice(0, 30)}" ${ratio.toFixed(2)}:1`);
  }
  return { overflow, mermaid, bodyBg: getComputedStyle(document.body).backgroundColor,
           bodyFg: getComputedStyle(document.body).color, low: low.slice(0, 5), lowCount: low.length };
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--shots", help="write full-page screenshots to this folder")
    ap.add_argument("--artifact", action="store_true", help="skip the Mermaid check (host renders it)")
    args = ap.parse_args()
    page_path = pathlib.Path(args.page).resolve()
    if not page_path.exists():
        print(f"ERROR: {page_path} not found")
        return 1
    shots = pathlib.Path(args.shots) if args.shots else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)

    found, colours = {}, {}  # message -> renders it appeared in
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM") or None)
        for scheme in ("light", "dark"):
            for name, (w, h) in VIEWPORTS.items():
                tag = f"{name}/{scheme}"
                issues = []
                ctx = browser.new_context(viewport={"width": w, "height": h}, color_scheme=scheme)
                page = ctx.new_page()
                errors, failed = [], []
                page.on("console", lambda m: m.type == "error" and errors.append(m.text))
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("requestfailed", lambda r: failed.append(r.url))
                page.on("request", lambda r: not args.artifact and load_rule_problem(r.url) and errors.append(
                    f"LOADRULE {load_rule_problem(r.url)}: {r.url}"))
                page.goto(page_path.as_uri(), wait_until="networkidle", timeout=20000)
                page.wait_for_timeout(800)  # let Mermaid finish
                r = page.evaluate(PROBE)
                colours[scheme] = (r["bodyBg"], r["bodyFg"])
                if r["overflow"]:
                    issues.append(f"horizontal overflow from " + ", ".join(r["overflow"]))
                bad = [s for s in r["mermaid"] if s != "ok"]
                if bad and not args.artifact:
                    issues.append(f"{len(bad)}/{len(r['mermaid'])} Mermaid blocks {bad[0]}")
                if r["lowCount"]:
                    issues.append(f"{r['lowCount']} low-contrast text elements, e.g. " + "; ".join(r["low"]))
                for e in [e for e in errors if e.startswith("LOADRULE ")]:
                    issues.append("load rule: " + e[9:160])
                for e in [e for e in errors if not e.startswith("LOADRULE ")][:3]:
                    issues.append(f"console error: {e[:160]}")
                for u in failed[:3]:
                    issues.append(f"failed to load {u}")
                for i in issues:
                    found.setdefault(i, []).append(tag)
                if shots:
                    page.screenshot(path=str(shots / f"{name}-{scheme}.png"), full_page=True)
                ctx.close()
        browser.close()

    # The same issue usually repeats across renders; print it once with where it appeared.
    issues = [f"[{'all' if len(t) == 4 else ', '.join(t)}] {m}" for m, t in found.items()]
    if colours.get("light") == colours.get("dark"):
        issues.append("dark theme: body colours identical to light — prefers-color-scheme not handled")
    if issues:
        print(f"ISSUES ({len(issues)}):")
        print("\n".join(f"- {i}" for i in issues))
    else:
        print("CLEAN: desktop+phone x light+dark — no overflow, errors, failed loads, Mermaid or contrast problems")
    if shots:
        print(f"screenshots: {shots}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
