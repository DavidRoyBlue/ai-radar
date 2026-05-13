---
title: "Behind the Scenes Hardening Firefox with Claude Mythos Preview"
canonical_key: "url:simonwillison.net/2026/may/7/firefox-claude-mythos"
url: "https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything"
seen_via: ["rss"]
source: "rss"
date_seen: "2026-05-13"
tags: ["claude-code", "production", "security", "case-study"]
score: 7
score_reasoning: "Mozilla using Claude in production to harden Firefox is a high-signal case study."
status: "new"
---

Simon Willison's notes on Mozilla's "Claude Mythos" effort to harden Firefox — what they prompted, which agents they used, the failure modes they hit, and what discipline they layered on top. Production deployments of Claude into a real C++ codebase at Mozilla scale are rare publicly-documented data points; the operational lessons (sandboxing prompts, audit trails, reviewer involvement) are directly transferable to anyone shipping AI-assisted code at a serious org.
