Execute the daily ai-radar iteration in /home/bkd/Projects/ai-radar.

First, cd to /home/bkd/Projects/ai-radar and confirm CLAUDE.md is loaded (it documents the full pipeline). Then run the daily pipeline end-to-end as described in CLAUDE.md: fetch every source in sources.yaml, dedupe, keyword-prefilter, star-delta enrich, LLM-triage in batches of 10, full-score survivors, write KB entries with proper YAML front-matter for every score-≥4 item, write the daily mini-digest at digests/daily/YYYY-MM-DD.md, write the run summary at state/runs/YYYY-MM-DD.md, then commit with message `radar: YYYY-MM-DD — N new entries (X high-score)` and push to origin/main.

The iteration is complete when the conversation transcript shows ALL of the following:

1. The literal string `RADAR_RUN_COMPLETE` printed at the end (echo it).
2. The git commit SHA printed via `git rev-parse HEAD` (or a clear log line saying "no new items, nothing to commit").
3. The contents of `state/runs/YYYY-MM-DD.md` cat'd into the transcript so the evaluator can see the metrics block.
4. Confirmation that `git push` succeeded (or a clear log of why it was skipped — e.g., no commit made).

If any single source fails, log it in the run summary and continue — that is success, not failure. Do NOT retry forever. Cap total turns at 30; if you hit turn 28, write a partial run summary explaining what's done and what's left, commit what you have, and finish.

Honor the constraints in CLAUDE.md strictly:
- Never commit anything under `.private/` or `state/` (gitignored)
- Cap Exa searches at 5 for this run; track in state/exa-budget.json
- Idempotency: rely on state/seen.json so re-running the same day doesn't duplicate

Stop after the four transcript signals above are present.
