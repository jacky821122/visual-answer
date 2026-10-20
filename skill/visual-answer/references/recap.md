# recap — what was done

The reader was away. They want to know, at a high level, what happened and what it means —
not to audit the work. Think "briefing from a trusted colleague", not "acceptance report".

## Principles
- **Outcome first**: done / partly done / blocked, and what they now have, in one or two sentences.
- **Decisions are the core.** What was decided, why, and what it trades off. Turning points —
  where direction changed and why — are often the most interesting part.
- **The analysis behind it**, briefly: what was found that shaped the decisions.
- **How it was built, in outline** — this is wanted, not optional: the main parts and how they
  fit together, what each part is responsible for, and which tools or frameworks it leans on.
  A few sentences, or one small diagram if the structure matters. Scale touched lightly
  (e.g. "3 commits, Python, ~400 lines") — a chip row works well; use only numbers that exist
  (no commits yet → say files and language instead).
- **Open risks and what's left for the user**: short, near the end. If nothing was verified for
  real, say so in one line; otherwise one line on how it was verified is enough.
- Use reader.md: process narration, file lists, line counts, tool calls, rejected alternatives,
  dead ends and token cost don't belong here.

## Examples of things that may fit (not required, not exhaustive)
- A "decisions" section where each decision is a short heading + one-paragraph why.
- A before/after of the thing changed, when the change is structural.
- A next-step callout with the one action the user should take.

## Common mistakes
- A changelog of files.
- Proof per acceptance criterion on the main page.
- A session timeline.
