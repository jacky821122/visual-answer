# visual-answer

A Claude Code skill that turns an answer into a well-designed claude.ai Artifact page —
explanations, recaps, diagnoses, comparisons and data reports — only when explicitly asked.

It is a content layer: it decides page type, structure and which components (prose, Mermaid
diagram, table, chart, callout) earn their place. Visual design is left to the built-in
`artifact-design` / `dataviz` skills.

## Install

```bash
ln -s ~/visual-answer/skill/visual-answer ~/.claude/skills/visual-answer
```

Optional: personalise the reader profile (git-ignored, read in preference to the template):

```bash
cp ~/visual-answer/skill/visual-answer/references/reader{,.local}.md
```

Use: `/visual-answer <topic>` or ask "做成頁面 / 畫圖說明 / recap 成頁面".

## Layout

- `skill/visual-answer/SKILL.md` — workflow, layouts, component rules, writing & honesty rules
- `skill/visual-answer/references/` — page types: explain, recap, diagnose, compare, report,
  plus `reader.md` (reader-profile template; your own copy lives in `reader.local.md`)

Acceptance testing used blind re-creations of real pages; those cases contain private data and
are not published.

## Credits

Ideas adapted (no code copied) from
[answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) (MIT),
[visual-explainer](https://github.com/nicobailon/visual-explainer),
[html-artifacts](https://github.com/dogum/html-artifacts) and
[archify](https://github.com/tt-a1i/archify).

## License

MIT — see [LICENSE](LICENSE).
