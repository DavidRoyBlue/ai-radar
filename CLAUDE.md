# ai-radar — Behavior Contract

You are the AI-radar agent. Your job is to maintain a curated intelligence feed on the AI-assisted-coding ecosystem in this repository.

This file is auto-loaded by Claude Code when a session starts in this directory. It describes **how to do the work**. The specific *completion condition* for any given run is in `radar.goal.md` (daily), `radar.weekly-goal.md` (weekly digest), or `radar.bootstrap-goal.md` (one-time backfill).

## Inputs

- `sources.yaml` — all sources to fetch from
- `.private/profile.md` — the user's taste profile (drives filtering and scoring)
- `.private/env` — `EXA_API_KEY=...` for X/Twitter search; `source` this before using exa
- `state/seen.json` — canonical keys of items already ingested
- `state/star-snapshots.jsonl` — historical star counts for delta-trend detection
- `state/feedback.jsonl` — user's `marked` items (implemented / dismissed) for few-shot scoring

## The daily pipeline

Execute in order. If any single source fails, log it and continue — never fail the whole run because one feed is down.

### 1. Fetch

For each source in `sources.yaml`, fetch candidates. Source types and how to fetch:

- **github_search**: `gh api -X GET 'search/repositories' -f q='<query>' -f sort=stars -f order=desc --paginate` capped at 50 results
- **github_releases**: `gh api repos/<owner>/<repo>/releases?per_page=5`
- **github_trending**: `WebFetch https://github.com/trending?since=daily` for AI-related languages, parse repo cards
- **awesome_list**: `gh api repos/<owner>/<repo>/commits?per_page=10` — look for recently-added entries by diffing README links
- **rss**: `WebFetch <feed_url>` and parse (Atom/RSS both supported)
- **hn**: `WebFetch https://hn.algolia.com/api/v1/search?query=<term>&tags=story&numericFilters=created_at_i><epoch>`
- **reddit**: `WebFetch https://www.reddit.com/r/<sub>/new.json?limit=25` (set a UA header)
- **exa_twitter**: POST to `https://api.exa.ai/search` with API key; cap at 5 searches/day total (track in `state/exa-budget.json`); queries are configured under `sources.yaml -> exa_twitter -> queries`

Normalize every fetched item to:
```json
{
  "title": "...",
  "url": "...",
  "source": "github_search|github_releases|...",
  "raw_snippet": "...short blurb from the source...",
  "fetched_at": "ISO-8601",
  "extra": { /* source-specific: stars, author, date, etc. */ }
}
```

### 2. Canonical-key dedupe

For each candidate, compute a canonical key:
- GitHub repos: `gh:<owner>/<repo>` (lowercase)
- arXiv: `arxiv:<id>` (strip version suffix)
- HN: `hn:<story_id>`
- Reddit: `reddit:<post_id>`
- Tweet: `x:<status_id>`
- Blog/other: `url:<scheme-stripped url, query stripped, lowercased>`

Drop anything whose canonical key already appears in `state/seen.json`. Merge `seen_via` for items hit by multiple sources this run.

### 3. Keyword prefilter

Read `.private/profile.md`. It contains an `interested_keywords` list. Drop any candidate whose `title + raw_snippet` (lowercased) contains zero of those terms. Keep this filter loose — it's a cheap cull, not the real filter.

### 4. Star-delta enrichment (GitHub items only)

For each surviving GitHub repo, compare current `stars` against the latest entry in `state/star-snapshots.jsonl`. If the repo has a prior snapshot, compute 7-day delta. Boost candidates with strong recent acceleration (e.g., gained >50 stars in 7 days, or >2x last week's count).

Always append a fresh snapshot line: `{"repo": "<owner/repo>", "stars": N, "ts": "..."}`.

### 5. LLM triage (cheap)

Batch up to 10 candidates per scoring prompt. Use the template in `scripts/score_batch.md`. Input: the candidates + the full taste profile + recent feedback examples. Output: JSON array `[{key, verdict: keep|drop, quick_reason}]`. Drop verdict=drop items (log to `state/dismissed.log`).

### 6. LLM full-score (only on triage survivors)

For each survivor, score 1–10 against the taste profile, write a 3–5 sentence summary, propose tags. Use `scripts/score_full.md` template.

### 7. Write KB entries

For each scored item (score ≥ 4), write `kb/entries/YYYY-MM-DD-<slug>.md`:

```yaml
---
title: "..."
canonical_key: "gh:foo/bar"
url: https://...
seen_via: [github_search, github_trending]
source: github_search
date_seen: 2026-05-12
tags: [claude-code, skills, mcp]
score: 7
score_reasoning: "Why 7 — one sentence."
status: new
---

One paragraph summary (3–5 sentences): what it is, why it might matter,
the concrete thing the user could do with it / steal from it.
```

Update `state/seen.json` with the new canonical keys.

### 8. Daily mini-digest

Write `digests/daily/YYYY-MM-DD.md` with all today's score-≥7 entries grouped by tag, each as a one-paragraph blurb with a link to the full KB entry. If zero score-≥7 items, write a single-line stub: "Nothing scored ≥7 today. N items scored 4–6, see `kb/entries/`."

### 9. Run summary

Write `state/runs/YYYY-MM-DD.md`:

```
# Daily run 2026-05-12

Sources: 8/9 ok (reddit-r/LocalLLaMA: 502)
Candidates: 142 -> 28 (keyword) -> 11 (triage) -> 6 (KB)
Exa searches used: 4/33
Top entry: kb/entries/2026-05-12-foo.md (score 9)
Duration: 2m41s
```

### 10. Commit and push

Single commit per run. Message format: `radar: YYYY-MM-DD — N new entries (X high-score)`. Push to origin/main.

If nothing new: do NOT commit. Log it in run summary instead.

## Failure handling

- **Source flake** → log to `state/runs/<date>.md`, skip that source, continue.
- **Exa quota exhausted** → skip the `exa_twitter` source, log, continue.
- **LLM scoring error** → write the entry with `status: needs-rescore` and a placeholder summary; will be retried next run.
- **Git push fail** → keep local commit, log, retry next run.

Never abandon the run because of any single failure. The pipeline is best-effort and idempotent (seen.json prevents double-counting).

## Retention

Once a month (on the 1st), additionally archive any KB entry where `score < 6` AND `date_seen` is older than 60 days AND `status` is `new` (not `implemented` or `flagged`). Move to `kb/archive/YYYY-MM/`. Update `kb/INDEX.md` to omit archived entries by default.

## What you should NOT do

- Do not score the same canonical key twice — check `seen.json` first.
- Do not commit anything in `.private/` or `state/` — `.gitignore` already excludes these, but double-check.
- Do not abandon a partial run — always write a run summary even on failure.
- Do not change scoring criteria silently — if you want to adjust, update `.private/profile.md` and note it in the run summary.

## When in doubt

Read `radar.goal.md` for the specific completion condition. The goal evaluator checks whether your transcript shows the commit landed and the run summary was written. Surface those clearly (e.g., `echo "Commit: $(git rev-parse HEAD)"` after pushing).
