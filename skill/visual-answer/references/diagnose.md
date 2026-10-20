# diagnose — why something is broken

The reader wants it fixed, or to know whether to worry. Lead with the most likely cause and the
next action; the investigation is supporting material.

## Principles
- **Verdict first**: the cause (or best candidate), how sure you are in plain words
  (已確認 / 很可能 / 還不確定), and the one thing to do now.
- **Rank causes** when there are several: likely ones up front with the evidence that points
  to them; ruled-out ones briefly at the end. Colour by status (confirmed / likely / ruled out).
- **Evidence in human terms**: what was observed and what it means. Raw log lines go in
  `<details>`.
- **Fix steps** as commands, condition first. Separate "fix now" from "prevent next time".
  Flag anything destructive or hard to undo.
- A diagram only if the failure travels through several components and the picture shows where
  it breaks.

## Examples (not required)
- A status chip row at the top (服務 ✓ / 網路 ! / 憑證 ✗).
- A short "如果還是不行" branch at the end.

## Common mistakes
- Investigation narrative before the verdict.
- Every cause marked 可能; a wall of green/red tiles with no explanation.
