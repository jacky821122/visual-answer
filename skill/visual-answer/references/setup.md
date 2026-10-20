# setup — bootstrap the reader profile

Run this when `reader.local.md` does not exist (first use, or right after install). It is a
light, surface-level pass: a minute of reading, not an investigation. The profile only has to
be good enough to frame pages from the reader's seat; it improves later through feedback.

## Steps
1. **Ask once**, in one line: 「要先花一分鐘從記憶和目前目錄建立讀者側寫嗎？」
   - No → copy `reader.md` to `reader.local.md` unchanged (so this is never asked again), then
     continue with the original request.
2. **Read only what exists, at the top level.** Budget: at most 5 source files (this skill's
   own files don't count), no subagents, no recursive search, no session transcripts, no
   source code.
   - `~/.claude/CLAUDE.md` — the user's global instructions.
   - This project's memory index `MEMORY.md` — the index lines only, not the memory files.
   - The working directory's `CLAUDE.md` and `README*` — the first ~40 lines each.
3. **Extract only**:
   - what they do and own (roles, projects, domains), as plain descriptions;
   - the language they read in and the tone they like;
   - preferences they have explicitly stated about answers or pages.
   Describe the person, not their infrastructure: a home lab or service stack is one short
   phrase, never an inventory. Never copy IP addresses, hostnames, emails, file paths,
   credentials or money figures. If a source says little, write little — don't infer a persona.
4. **Draft** `reader.local.md` from `reader.md`: fill "Who they are" with at most 5 bullets
   (tone and answer-style preferences belong in its language/tone bullet). Preferences about
   page content go under "What they want" or "What they do not want". Leave the rest as is.
5. **Show the sections you filled** in the terminal and write the file only after the user
   agrees (edits welcome). Then resume the original request, if there was one.
