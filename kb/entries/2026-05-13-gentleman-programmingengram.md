---
title: "Gentleman-Programming/engram"
canonical_key: "gh:gentleman-programming/engram"
url: "https://github.com/Gentleman-Programming/engram"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["agent-memory", "sqlite", "mcp", "tooling"]
score: 7
score_reasoning: "Agent-agnostic persistent memory: SQLite+FTS5, MCP server, HTTP API, CLI, TUI \u2014 concrete and well-scoped."
status: "new"
---

Gentleman-Programming/engram — a persistent-memory system for coding agents, agent-agnostic, Go binary backed by SQLite + FTS5, exposed via MCP server, HTTP API, CLI, and TUI. The scoping is exactly right: one binary, one storage backend, four interface surfaces, model-agnostic. Worth running locally and comparing the FTS5 retrieval against your current memory recall behavior; even better, this is a good model for how to package any small agent-side service.
