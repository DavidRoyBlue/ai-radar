# Full-scoring prompt (used on triage survivors)

Substitute:

- `{{PROFILE}}` — `.private/profile.md`
- `{{FEEDBACK_EXAMPLES}}` — last 10 marked items from `state/feedback.jsonl`
- `{{CANDIDATE}}` — single candidate JSON dict (you score ONE at a time at this stage; batched scoring sacrifices summary quality)
- `{{ENRICHMENT}}` — any extra context fetched specifically for this item (e.g., star delta, full README snippet, full thread text from a tweet)

---

Score one candidate for the AI-assisted-coding intelligence feed.

Reader's taste profile:

{{PROFILE}}

Recent feedback:

{{FEEDBACK_EXAMPLES}}

Candidate:

{{CANDIDATE}}

Enrichment context:

{{ENRICHMENT}}

Score on a 1–10 scale: how likely is this to help the reader's day-to-day work in the AI-assisted-coding space? Use the whole range:

- 1–3: noise, off-target, generic chatbot/tutorial/wrapper
- 4–5: tangentially relevant, FYI at most
- 6–7: worth a skim, has at least one interesting idea
- 8–9: worth deep reading; concrete pattern or tool the reader would likely use or steal from
- 10: must-read; directly competitive or directly useful for what they're building

Output a single JSON object. No prose outside it.

```json
{
  "canonical_key": "...",
  "score": <int 1-10>,
  "score_reasoning": "<one sentence>",
  "tags": ["<3-6 short tags>"],
  "summary": "<3-5 sentences: what it is, why it matters here, the concrete thing the reader could do with it or steal from it. Plain prose, no marketing tone.>",
  "status": "new"
}
```
