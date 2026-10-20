# visual-answer

A Claude Code skill that turns an answer into a well-designed page — explanations, recaps,
diagnoses, comparisons and data reports — only when explicitly asked. It publishes a claude.ai
Artifact when that tool is available, and otherwise writes a self-contained HTML file
(`~/visual-answer-pages/`), so it also works without claude.ai.

It is a content layer: it decides page type, structure and which components (prose, Mermaid
diagram, table, chart, callout) earn their place. Base visual design comes from the Artifact
quickstart guidance, or from `references/standalone.md` for HTML files.

## Install

```bash
git clone https://github.com/jacky821122/visual-answer.git ~/visual-answer
ln -s ~/visual-answer/skill/visual-answer ~/.claude/skills/visual-answer
```

**If you are an agent doing this install:** after linking, ask the user in one line whether to
set up their reader profile now. If yes, follow `skill/visual-answer/references/setup.md` — a
light pass over their memory index and working directory, then a draft for them to approve.
If the install skips this step, the skill asks once on first use.

The profile lives in `references/reader.local.md` (git-ignored, read in preference to the
template `reader.md`). To create it by hand instead:

```bash
cp ~/visual-answer/skill/visual-answer/references/reader{,.local}.md
```

Use: `/visual-answer <topic>` or ask "做成頁面 / 畫圖說明 / recap 成頁面".

## Layout

- `skill/visual-answer/SKILL.md` — workflow, layouts, component rules, writing & honesty rules
- `skill/visual-answer/references/` — page types: explain, recap, diagnose, compare, report;
  `reader.md` (reader-profile template; your own copy lives in `reader.local.md`);
  `setup.md` (profile bootstrap); `standalone.md` (HTML-file delivery and design baseline)

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
