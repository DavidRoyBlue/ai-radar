---
title: "bytedance/deer-flow"
canonical_key: "gh:bytedance/deer-flow"
url: "https://github.com/bytedance/deer-flow"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["agent-harness", "long-horizon", "sub-agents", "bytedance"]
score: 8
score_reasoning: "Bytedance long-horizon agent harness with explicit sub-agents, memory, message gateway, sandboxes."
status: "new"
---

Bytedance's deer-flow is a long-horizon SuperAgent harness that combines sandboxes, persistent memory, tools, skills, sub-agents, and a message gateway. The interesting parts are the explicit architectural separation (memory store, message gateway, skills registry) which most open harnesses elide, and the fact that a real engineering org with operational scale is publishing this rather than yet-another-LangChain wrapper. Worth reading the architecture and copying any of the boundaries (message gateway in particular) that aren't yet in the reader's own design.
