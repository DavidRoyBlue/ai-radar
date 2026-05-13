---
title: "Using Claude Code: The Unreasonable Effectiveness of HTML"
canonical_key: "url:simonwillison.net/2026/may/8/unreasonable-effectiveness-of-html"
url: "https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything"
seen_via: ["rss"]
source: "rss"
date_seen: "2026-05-13"
tags: ["claude-code", "simon-willison", "patterns", "html"]
score: 9
score_reasoning: "Simon Willison on a counterintuitive Claude-Code pattern \u2014 exactly the reader's interest area."
status: "new"
---

Simon Willison's post on the "unreasonable effectiveness of HTML" when working with Claude Code — argues that prompting agents to emit raw HTML rather than React/components is more reliable, easier to debug, and faster than the framework-heavy default. The concrete suggestion the reader can steal today: change skill outputs and tool-emitted artifacts to lean on plain HTML wherever the final consumer is a browser, and treat "framework-free" as a quality criterion in agent code review.
