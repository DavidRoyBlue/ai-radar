---
title: "mrexodia/ida-pro-mcp"
canonical_key: "gh:mrexodia/ida-pro-mcp"
url: "https://github.com/mrexodia/ida-pro-mcp"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["mcp", "reverse-engineering", "security", "novel"]
score: 7
score_reasoning: "IDA Pro reverse-engineering bridged into agents \u2014 genuinely novel non-obvious MCP."
status: "new"
---

An MCP server that bridges IDA Pro with language models — the agent can decompile, navigate, name functions, and propose hypotheses about binary behavior interactively. This is the kind of "non-obvious MCP for a non-obvious tool" the radar specifically wants to find: it concretely changes what a Claude Code session can be used for (security/reverse-engineering work without a human in the disassembler). Inspiring pattern even for readers who don't reverse engineer — the server design (small, focused, model-friendly nomenclature) is generalizable.
