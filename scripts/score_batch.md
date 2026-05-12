# Triage scoring prompt (cheap pass)

This template is used during step 5 (LLM triage) of the daily pipeline. You (the agent) construct a single prompt by substituting:

- `{{PROFILE}}` — full contents of `.private/profile.md`
- `{{FEEDBACK_EXAMPLES}}` — last 6 marked items from `state/feedback.jsonl` if any (format: `- <title> | mark: <implemented|dismissed> | reason: <one-liner>`); empty string if file missing
- `{{CANDIDATES}}` — JSON array of up to 10 candidate dicts: `{canonical_key, title, url, source, raw_snippet, extra}` (compact, one per line)

---

You are filtering candidate items for an AI-assisted-coding intelligence feed.

The reader's taste profile:

{{PROFILE}}

Recent feedback (what they kept vs dismissed):

{{FEEDBACK_EXAMPLES}}

Below are up to 10 candidates. For each, decide `keep` or `drop` based on whether it plausibly matches the profile. Be ruthless — when in doubt, drop. The goal is to reduce noise before a more expensive scoring pass.

Candidates:

{{CANDIDATES}}

Respond with a single JSON array, one object per candidate, in the same order:

```json
[
  {"canonical_key": "...", "verdict": "keep" | "drop", "quick_reason": "<≤12 words>"},
  ...
]
```

No prose outside the JSON array.
