---
title: "open-webui/mcpo"
canonical_key: "gh:open-webui/mcpo"
url: "https://github.com/open-webui/mcpo"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["mcp", "openapi", "proxy", "bridge"]
score: 8
score_reasoning: "MCP-to-OpenAPI proxy \u2014 turns any MCP server into a REST API and vice versa; novel and useful."
status: "new"
---

open-webui/mcpo is a simple, secure proxy that exposes any MCP server as an OpenAPI / REST endpoint. The leverage is that you can now use MCP tooling from non-MCP clients (curl, Postman, plain HTTP clients, OpenAPI-aware code-gen) without rewriting servers as REST. For the reader specifically: this is the cleanest way to let scheduled non-Claude jobs or CI systems consume MCP servers built primarily for Claude Code.
