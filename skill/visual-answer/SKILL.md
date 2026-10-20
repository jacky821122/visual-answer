---
name: visual-answer
description: >-
  Turn an answer into a well-designed page — a claude.ai Artifact, or a standalone HTML file
  where Artifacts aren't available — instead of a long terminal reply:
  deep explanations, technical principles, long write-ups, data visualisation, ops diagnosis,
  option comparisons, and recaps of what an agent just did. Use ONLY when the user explicitly
  asks for it: invokes /visual-answer, or says things like "做成頁面", "用 HTML 回答", "畫圖說明",
  "視覺化", "做成 artifact 給我看", "給我 html 檔", "看不懂，畫出來", "make it a page", "visualize this",
  "recap what you did as a page". Never use it on your own initiative for a normal reply.
argument-hint: "[topic or what to recap]"
---

# visual-answer: answer with one page

The user decided a page is wanted. The hard part is not the HTML; it is **deciding what this
reader should see**. A page that shows everything you know is a failed page. A page that shows
the few things the reader cares about, interpreted, with a clear so-what, is a good one.

Arguments: `$ARGUMENTS`

## 1. Workflow

1. **Reader and purpose first.** Read `${CLAUDE_SKILL_DIR}/references/reader.local.md`
   (the user's own profile; fall back to `references/reader.md` if it does not exist). Then write down
   for yourself, in 3 lines: what the reader wants to learn or decide from this page; the
   so-what (what it means for them / what to do); what they will NOT care about. Everything
   after this step serves those lines. If `reader.local.md` does not exist yet, follow
   `references/setup.md` first (one question; a light pass, then back to the request).
2. **Pick the page type** (table below) and read its reference. Types are starting points, not
   forms: the reference gives principles and examples, never a list of sections you must fill.
3. **Gather real material** — files, command output, data, this session. Never invent facts.
4. **Find the story.** Before outlining, ask: what is the interesting pattern, the surprise, the
   judgement worth making? Group things into meaningful categories and say what each means.
   The reader's own remarks and context are the richest material — weave them into the story
   next to the items they explain, not into a separate corrections section.
5. **Outline** — only sections that serve step 1. For each, ask "would the reader miss this?"
   Content you're unsure about goes to a closing 「可能有興趣」 `<details>`, or becomes a one-line
   question in the terminal reply.
6. **Build and deliver** — pick the delivery first:
   - **Artifact** (the Artifact tool exists and the user didn't ask for a file): run its
     `quickstart` first (`intent: "other"`) and use the design guidance it returns — it stands in
     for `artifact-design`, so don't load that skill as well. Always build a plain HTML page,
     even if quickstart offers a Docs or Slides type. Load `dataviz` only if there is a chart.
     Publish with the Artifact tool; title = a short name for the subject.
   - **HTML file** (no Artifact tool, or the user asked for a file): read
     `references/standalone.md` and follow it for delivery and the design baseline.
   Either way, apply section 4 of this file on top.
7. **Terminal reply**: 1–3 lines — the core takeaway and the link or file path, plus at most one
   question about content you left out. Don't paste page content.

| Type | Use when | Reference |
|---|---|---|
| explain | How something works; a principle; a long explanation | `references/explain.md` |
| recap | Reporting what an agent/session did | `references/recap.md` |
| diagnose | Something broken or odd | `references/diagnose.md` |
| compare | Choosing between options | `references/compare.md` |
| report | Data, numbers, specs, inventories | `references/report.md` |

## 2. Content principles

- **Lead with insight, not inventory.** The first screen says what the material means for the
  reader ("週末午餐撐起一半營收，但平日晚餐才是毛利來源"), not summary statistics or a table of contents.
- **End with the so-what.** A recommendation, a next action, or what to watch.
- **Translate.** Write in the reader's words. Never expose source vocabulary: API field names,
  raw column names, match scores, error codes — unless the reader must type them.
- **Judge.** Second person, interpretive, willing to call it ("這個方案省錢，但半年後會卡在維護").
  Hedging belongs only where real uncertainty would change the reader's action.
- **Method and data quality get a footer budget**: a few muted lines at the end. A caveat moves
  up only if it would flip a conclusion, and then it sits next to the item it affects.
- **Full lookup tables are folded** (`<details>`) unless looking things up is the page's job.
- **Cut** what the reader profile lists as unwanted, even if it took effort to find.
- **Except the subject itself.** A cut rule yields when the item is what the question is about:
  the error code the user is asking about can be the headline; a rejected option they asked
  "why not" about is the topic, not a footnote.

## 3. Layout

Default is **one reading column** (max ~860px), a narrative top to bottom, each section with a
visual anchor (a coloured name line, a key number, a chip row). Use a multi-panel **board**
only for a page meant to be scanned at a glance (a status dashboard); never split a story into
a grid of small panels. Inside a section, side-by-side blocks are fine when they compare.

Diagrams: Mermaid in `<pre class="mermaid">…</pre>` (an Artifact renders it natively — never load
a Mermaid library there; an HTML file loads it as `references/standalone.md` shows). Never
hand-draw diagram SVG. Draw one only when a relationship is the point and a
sentence can't carry it; ≤ ~15 nodes; labels short. In an Artifact, leave Mermaid on its default
theme (it follows light/dark); in an HTML file, the snippet in `references/standalone.md` picks
the theme. Add `classDef` colours only if they read on both backgrounds.

## 4. Design emphasis (applies on top of the base design guidance: quickstart, or standalone.md)

The default design guidance leans utilitarian for reports and docs. These pages are read for pleasure and
insight, so push further:

- **Semantic colour.** Define 3–5 colour tokens that mean something in this subject (categories,
  good/warn/bad, tiers) and apply each one consistently everywhere it appears: bars, numbers,
  chips, section markers, legend. A single accent plus grey is not enough.
- **One focal point.** The first screen has one dramatic element: a large key number or fact in
  an accent colour, sized well above the body text.
- **Chips and states.** Status and flags are filled chips with text (✓ 已完成, ! 注意) on a tinted
  background. Values past a meaningful limit change colour.
- **Callouts that stand out.** Tinted background + coloured edge or icon-free label; one style per
  meaning (insight, warning, action). Use as many as the content genuinely has.
- **A subject-specific voice in type.** A display face or eyebrow line that fits the subject's
  world; body text stays highly readable.
- **Charts use the same semantic colours.** A category has one colour in its chart, chips and
  headings. Take chart mechanics (scales, ticks, labels) from `dataviz`, not its palette; if it
  has a palette/contrast check, run it on your own colours and adjust any that fail.
- Still: no decoration without meaning, and both light and dark themes designed.

## 5. Writing

- Answer first; no preamble, no closing summary, no "希望有幫助".
- Each fact once; if a chart or table shows it, the prose interprets it instead of repeating it.
- Plain, warm, direct Taiwan Traditional Chinese (or the user's language). Code, commands and
  product names stay as they are; give titles, products and places their common local names.
- Steps (only in procedures): one action each, condition first.
- No 賦能、綜上所述、值得注意的是、進行優化.

## 6. Honesty

- No invented numbers. No real data → no chart. Illustrative values are labelled 示意.
- Inferences are marked once, lightly (a small 推定 chip), not with a disclaimer per line.
- When the headline or focal point is itself your inference (your own grouping or reading of the
  data), no chip on it; put one small muted line right under it saying what it rests on
  ("依過去 12 週的訂單歸類").
- Data source and date: one footer line.
- If part of the request couldn't be done, say so in one sentence where it matters — not as the
  opening of the page.

## 7. Updating

Revise by editing the same local file and publishing the same path (same URL); for an earlier
session's page use the Artifact tool's `url` flow. An HTML file is revised in place at its path.

When the user asks for more or less of something, revise this page first. If the feedback looks
like a lasting preference rather than a one-off for this page, ask in one line whether to record
it in `references/reader.local.md` ("要記進讀者偏好嗎？"), and update that file only if they
agree — create it as a copy of `references/reader.md` first if it does not exist. Never write
personal preferences into `reader.md` itself; it is the shared template.
