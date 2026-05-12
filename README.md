# ai-radar

A continuous intelligence layer on the AI-assisted-coding ecosystem — Claude Code, MCP, sub-agent frameworks, skills/plugins, autonomous coding patterns, and adjacent infra.

A scheduled Claude Code session wakes up daily, sweeps a configured set of sources (GitHub Search, GitHub trending, awesome-* lists, RSS feeds, Hacker News, Reddit, and X via Exa), filters and scores candidates against a private taste profile, commits a markdown entry per surviving item, and writes a daily mini-digest. Once a week it rolls those up into a longer digest.

The whole thing is driven by Claude Code's built-in [`/goal`](https://code.claude.com/docs/en/goal) primitive — each daily run is one `/goal` session that terminates when the day's iteration is committed.

## Layout

```
ai-radar/
  CLAUDE.md          # Behavior contract — auto-loaded by Claude Code
  radar.goal.md      # The /goal condition string used by the scheduled task
  sources.yaml       # All monitored sources
  kb/
    entries/         # One markdown file per ingested item
    INDEX.md         # Regenerated locally — human-readable index
  digests/
    YYYY-WW.md       # Weekly digests (ISO week)
    daily/           # Daily mini-digests
  scripts/           # Small helpers the agent invokes
  state/             # (gitignored) seen-set, star snapshots, run logs, feedback
  .private/          # (gitignored) taste profile, API keys
```

## How a daily run works

1. Scheduled task fires at 07:00 local. Spawns a headless Claude session in this repo.
2. Session reads `CLAUDE.md` (auto-loaded), then `radar.goal.md`, and invokes `/goal <condition>`.
3. Inside the goal loop:
   - Fetch each source listed in `sources.yaml`
   - Dedupe against `state/seen.json` by canonical key
   - Keyword prefilter using terms in `.private/profile.md`
   - Two-pass LLM scoring (cheap triage → full one-paragraph summary for survivors)
   - Write KB entries with YAML front-matter
   - Write `digests/daily/YYYY-MM-DD.md` summarizing score-≥7 items
   - Update `state/runs/YYYY-MM-DD.md` with metrics
   - Commit and push
4. The `/goal` evaluator confirms completion from the transcript, session ends.

## How a weekly digest works

A second scheduled task fires Sunday 20:00 local. Reads the week's entries, rolls them into `digests/YYYY-WW.md`, commits, pushes.

## Manual usage

```bash
cd /home/bkd/Projects/ai-radar
claude
# Then in the session:
/goal $(cat radar.goal.md)
```

Or for the weekly digest:
```bash
claude -p "/goal $(cat radar.weekly-goal.md)"
```

## Setup notes

- Requires `EXA_API_KEY` in `.private/env` (free tier from [exa.ai](https://exa.ai))
- Requires `gh` CLI authenticated for git push
- Bootstrap (90-day backfill) is run manually once via `radar.bootstrap-goal.md`

## License

MIT
