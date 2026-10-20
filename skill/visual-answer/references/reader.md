# Reader profile — who these pages are for

> Template. Copy to `reader.local.md` (git-ignored) and personalise it there; the skill reads
> `reader.local.md` when it exists and falls back to this file. The preferences below are
> sensible defaults, not a description of you.

The default reader is the user. This file describes what they tend to care about. It is a
living profile: when their feedback on a page ("這個我不需要", "這個好") looks like a lasting
preference, ask whether to record it in `reader.local.md` and update that file only if they agree.
Use it to decide what goes up front, what goes in a fold, and what is cut. It is guidance for
judgement, not a checklist to fill.

## Who they are
- (Fill in: what the reader does and owns — work, projects, machines — so pages are framed from
  their seat. Example: "runs a small business and a home lab; reads as the owner, not an auditor".)
- (Fill in: reading language and tone preferences. Example: "reads Traditional Chinese; likes
  direct, opinionated answers; dislikes padding".)

## What they want from a page
- **The so-what.** What this means for them, what they should do or decide, what is surprising.
- **Insight over report.** Patterns, interpretation, judgement — said plainly, in second person.
- **Decisions and their reasons**, trade-offs, turning points (when and why direction changed).
- **Scale at a glance** — a few numbers that size the thing (how many, how big, which language),
  touched lightly.
- **Open risks** — wanted, but the lowest priority of the above; short.

## What they do not want (cut, or at most a footer line)
- Process narration: which files were read, which tools ran, line counts, timelines of the session.
- Raw source vocabulary: API field names, match scores, internal class names, exit codes.
- Data-quality and methodology detail that does not change the conclusion.
- In recaps and explanations: rejected alternatives and why (the agent can remember them;
  mention one only if they will ask). Compare pages are exempt — there the options are the topic.
- Token/time spent, dead ends hit along the way.
- Comparison with how others do it — only when the page's topic is a comparison.
- Per-criterion verification evidence. One line of "verified how" is enough unless asked.

## When unsure
If you can't tell whether they'd care about something, don't put it in the main flow. Either
put it in a closing `<details>` titled 「可能有興趣」, or ask in one line in the terminal reply
("要不要我把 X 也加進頁面？"). If an answer reveals a lasting preference, offer to record it in `reader.local.md`.
