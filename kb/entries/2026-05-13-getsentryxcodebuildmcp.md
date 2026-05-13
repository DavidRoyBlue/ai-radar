---
title: "getsentry/XcodeBuildMCP"
canonical_key: "gh:getsentry/xcodebuildmcp"
url: "https://github.com/getsentry/XcodeBuildMCP"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["mcp", "ios", "macos", "xcode"]
score: 6
score_reasoning: "Xcode/iOS build MCP from Sentry \u2014 niche but well-built."
status: "new"
---

Sentry's XcodeBuildMCP gives agents structured access to xcodebuild — start simulators, run tests, capture build logs, query targets. Solves the long-running pain of agents shelling out to xcodebuild and trying to parse human-readable output. Relevant only if the reader's stack includes Apple-platform work, but the design (wrap a chatty CLI in an MCP surface that emits structured results) is a transferable pattern.
