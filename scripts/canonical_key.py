#!/usr/bin/env python3
"""Compute a canonical key for an ingested item, used for cross-source dedupe.

Usage:
    python3 scripts/canonical_key.py <source> <url> [--title TITLE]

Prints the canonical key to stdout. Examples:

    canonical_key.py github_search https://github.com/Foo/Bar     -> gh:foo/bar
    canonical_key.py rss https://arxiv.org/abs/2401.12345v2       -> arxiv:2401.12345
    canonical_key.py hn https://news.ycombinator.com/item?id=999  -> hn:999
    canonical_key.py reddit https://reddit.com/r/x/comments/abc/  -> reddit:abc
    canonical_key.py exa_twitter https://x.com/foo/status/12345   -> x:12345
    canonical_key.py rss https://example.com/post/?utm=...        -> url:example.com/post
"""

from __future__ import annotations

import argparse
import re
import sys
from urllib.parse import urlparse


ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
GH_REPO_RE = re.compile(r"^/([^/]+)/([^/]+)(?:/|$)")
HN_RE = re.compile(r"(?:^|[?&])id=(\d+)")
REDDIT_RE = re.compile(r"/comments/([a-z0-9]+)")
TWEET_RE = re.compile(r"/status(?:es)?/(\d+)")


def canonical_key(source: str, url: str) -> str:
    if not url:
        raise ValueError("url is required")
    p = urlparse(url)
    host = (p.netloc or "").lower().removeprefix("www.")
    path = p.path or ""

    # GitHub repos
    if host == "github.com":
        m = GH_REPO_RE.match(path)
        if m:
            return f"gh:{m.group(1).lower()}/{m.group(2).lower()}"

    # arXiv
    if "arxiv.org" in host:
        m = ARXIV_ID_RE.search(path)
        if m:
            return f"arxiv:{m.group(1)}"

    # Hacker News
    if host.endswith("ycombinator.com") or host.endswith("algolia.com"):
        m = HN_RE.search(p.query) or HN_RE.search(path)
        if m:
            return f"hn:{m.group(1)}"

    # Reddit
    if host.endswith("reddit.com"):
        m = REDDIT_RE.search(path)
        if m:
            return f"reddit:{m.group(1)}"

    # X / Twitter
    if host in {"x.com", "twitter.com", "mobile.twitter.com"}:
        m = TWEET_RE.search(path)
        if m:
            return f"x:{m.group(1)}"

    # Fallback: normalized URL (strip scheme + query + fragment + trailing slash)
    stem = f"{host}{path}".rstrip("/").lower()
    return f"url:{stem}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="source-type from sources.yaml")
    ap.add_argument("url")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()
    print(canonical_key(args.source, args.url))
    return 0


if __name__ == "__main__":
    sys.exit(main())
