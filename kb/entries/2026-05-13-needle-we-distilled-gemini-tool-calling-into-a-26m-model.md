---
title: "Needle: We Distilled Gemini Tool Calling Into a 26M Model"
canonical_key: "reddit:1tb9b0r"
url: "https://www.reddit.com/r/LocalLLaMA/comments/1tb9b0r/needle_we_distilled_gemini_tool_calling_into_a/"
seen_via: ["reddit"]
source: "reddit"
date_seen: "2026-05-13"
tags: ["local-llm", "tool-use", "small-model", "reddit"]
score: 6
score_reasoning: "26M parameter tool-calling model \u2014 points at where local-first agents are headed."
status: "new"
---

Needle: a 26M-parameter function-calling model distilled from Gemini's tool-calling behavior, running at 6000 tok/s prefill / 1200 tok/s decode on consumer hardware. Even if you don't deploy small models locally, this matters for the agentic-coding space: it suggests that a non-trivial slice of tool-use can be offloaded from frontier models, which changes the cost structure of agent architectures. Worth watching for whether anyone uses this in an MCP-style coordinator pattern.
