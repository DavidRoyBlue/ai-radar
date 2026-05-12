One-time backfill of the ai-radar KB.

cd to /home/bkd/Projects/ai-radar. Treat the lookback window as the last 90 days. Run the full daily pipeline described in CLAUDE.md, but with these adjustments:

- For `github_search`: include `created:>YYYY-MM-DD` (90 days ago) and `pushed:>YYYY-MM-DD` (90 days ago) variants of each query.
- For `github_releases`: fetch the last 90 days of releases per repo (not just the most recent 5).
- For `rss`/`hn`/`reddit`: walk back as far as the feed exposes (most expose 30–90 days).
- For `exa_twitter`: cap at 15 searches for this one-time run (not 5).
- For LLM scoring: do NOT batch any larger than 10; this run will produce a large number of entries, that is expected.

Triage is allowed to be more aggressive — keep only score ≥ 5 for the bootstrap (vs. the daily default of ≥ 4) to avoid burying signal under 90 days of noise.

Skip writing a daily digest for backfilled items. Instead, write `digests/bootstrap-YYYY-MM-DD.md` with the top-20 score-≥7 entries from the backfill.

Commit progress every ~25 entries so we don't lose work if the session caps out. Commit messages: `radar: bootstrap batch <n> — <m> entries`.

Cap at 60 turns. The iteration is complete when:
1. `RADAR_BOOTSTRAP_COMPLETE` printed.
2. The bootstrap digest path printed.
3. `state/runs/bootstrap-YYYY-MM-DD.md` written and cat'd to transcript with totals.
4. Final commit SHA via `git rev-parse HEAD`.
5. `git push` succeeded.
