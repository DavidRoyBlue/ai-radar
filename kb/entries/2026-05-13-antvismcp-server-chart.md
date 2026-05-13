---
title: "antvis/mcp-server-chart"
canonical_key: "gh:antvis/mcp-server-chart"
url: "https://github.com/antvis/mcp-server-chart"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["mcp", "visualization", "charts"]
score: 6
score_reasoning: "MCP server for chart generation \u2014 niche but well-built example of skill+server bundle."
status: "new"
---

AntV's MCP server that exposes 25+ visualization chart types to agents, bundled with skills for chart generation and data analysis. The implementation pattern is worth a look: it pairs an MCP server (the tool surface) with a skill (the model-side instructions for using it well). That bundle pattern — server + matching skill — is increasingly the right unit of distribution and is something to copy when shipping radar's own MCP servers.
