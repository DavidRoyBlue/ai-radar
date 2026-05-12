#!/usr/bin/env python3
"""Render a scored item into a KB entry markdown file.

Reads a single JSON object from stdin (the full-scored candidate) plus the
canonical-key/url/source/seen_via from the fetched item (merged), and writes
kb/entries/YYYY-MM-DD-<slug>.md.

Usage:
    echo '<merged json>' | python3 scripts/render_entry.py [--kb-dir kb/entries]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


SLUG_STRIP = re.compile(r"[^a-z0-9-]+")


def slugify(title: str, fallback: str = "entry") -> str:
    s = title.lower().strip()
    s = re.sub(r"\s+", "-", s)
    s = SLUG_STRIP.sub("", s)
    s = s.strip("-")
    return (s or fallback)[:70]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb-dir", default="kb/entries")
    args = ap.parse_args()

    data = json.loads(sys.stdin.read())
    title = data.get("title", "(untitled)")
    today = datetime.now(timezone.utc).date().isoformat()
    slug = slugify(title)
    out_path = Path(args.kb_dir) / f"{today}-{slug}.md"
    # If already exists (rare: same title same day), append -2, -3, ...
    if out_path.exists():
        i = 2
        while (Path(args.kb_dir) / f"{today}-{slug}-{i}.md").exists():
            i += 1
        out_path = Path(args.kb_dir) / f"{today}-{slug}-{i}.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    front = {
        "title": title,
        "canonical_key": data.get("canonical_key", ""),
        "url": data.get("url", ""),
        "seen_via": data.get("seen_via", [data.get("source", "unknown")]),
        "source": data.get("source", "unknown"),
        "date_seen": today,
        "tags": data.get("tags", []),
        "score": data.get("score", 0),
        "score_reasoning": data.get("score_reasoning", ""),
        "status": data.get("status", "new"),
    }

    # Render YAML by hand to keep deps zero
    lines = ["---"]
    for k, v in front.items():
        if isinstance(v, list):
            inner = ", ".join(json.dumps(x) for x in v)
            lines.append(f"{k}: [{inner}]")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    lines.append("---")
    lines.append("")
    lines.append(data.get("summary", "").strip() or "(no summary)")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
