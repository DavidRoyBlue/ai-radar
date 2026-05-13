---
title: "ChromeDevTools/chrome-devtools-mcp"
canonical_key: "gh:chromedevtools/chrome-devtools-mcp"
url: "https://github.com/ChromeDevTools/chrome-devtools-mcp"
seen_via: ["github_search"]
source: "github_search"
date_seen: "2026-05-13"
tags: ["mcp", "chrome", "browser", "devtools", "official"]
score: 7
score_reasoning: "Official Chrome DevTools MCP \u2014 bridges browser tooling to coding agents."
status: "new"
---

Chrome DevTools team's official MCP server exposing devtools primitives (network, console, DOM, performance) to coding agents. Until now, browser-tooling MCPs were third-party with varying quality; an official Chromium-team implementation raises the floor for any agent that needs to inspect or interact with a running web app. If the reader's stack includes UI work, switching from ad-hoc Puppeteer scripts to this MCP eliminates a maintenance surface.
