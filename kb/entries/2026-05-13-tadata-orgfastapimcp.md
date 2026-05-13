---
title: "tadata-org/fastapi_mcp"
canonical_key: "gh:tadata-org/fastapi_mcp"
url: "https://github.com/tadata-org/fastapi_mcp"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["mcp", "fastapi", "auth", "python"]
score: 7
score_reasoning: "FastAPI to MCP exposure with auth \u2014 useful pattern for retro-fitting existing APIs."
status: "new"
---

tadata-org/fastapi_mcp converts an existing FastAPI application's endpoints into MCP tools automatically, with authentication preserved. This is exactly the integration pain point any team faces when they already have a Python service and want to plug it into agentic workflows — instead of writing an MCP server by hand, decorate the existing FastAPI app. Useful in any internal stack where Python services dominate and rewriting them as MCP servers would be wasted work.
