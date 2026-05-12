Generate this week's ai-radar digest in /home/bkd/Projects/ai-radar.

cd to /home/bkd/Projects/ai-radar. Compute the current ISO week (YYYY-WW). Read every KB entry under `kb/entries/` whose front-matter `date_seen` falls inside the Monday–Sunday window of the current ISO week.

Write `digests/YYYY-WW.md` with this structure:

```
# Week WW (Mon DD – Sun DD, YYYY)

## Must-look (score 8–10)

For each entry in this band, render:
### [Title](url) — score N — [tags]
The entry's one-paragraph summary verbatim. Link to the full KB file with a relative path.

## Worth a skim (score 6–7)

Same format, terser is fine.

## FYI (score 4–5)

Bullet list, one line each: [Title](url) — score N — tags

## Numbers

- Total entries this week: N
- Score distribution: ...
- Top tags: ...
- Sources hit: ...
```

If there are no entries this week, write a single-line digest noting that and still commit. Then commit with message `radar: weekly digest YYYY-WW` and push to origin/main.

The iteration is complete when the transcript shows:
1. The literal `RADAR_WEEKLY_COMPLETE` printed at the end.
2. The path of the digest file written (e.g., `digests/2026-W19.md`).
3. The git commit SHA via `git rev-parse HEAD`.
4. Confirmation that `git push` succeeded.

Cap at 15 turns. If anything fails, write what you can and commit a partial digest with a note.
