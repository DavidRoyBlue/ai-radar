#!/usr/bin/env python3
"""Regenerate kb/INDEX.md from the front-matter of every entry.

Scans kb/entries/*.md, parses YAML front-matter (the part between the leading
`---` lines), and writes a human-readable index grouped by score band and
sorted by date desc.

Usage:
    python3 scripts/regenerate_index.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    m = FM_RE.search(text)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        # Try to interpret list/number/string. Front-matter is JSON-y by design.
        if v.startswith("[") and v.endswith("]"):
            try:
                out[k] = json.loads(v)
                continue
            except Exception:
                pass
        if v.startswith('"') and v.endswith('"'):
            try:
                out[k] = json.loads(v)
                continue
            except Exception:
                pass
        # bare number?
        try:
            out[k] = int(v)
            continue
        except ValueError:
            pass
        try:
            out[k] = float(v)
            continue
        except ValueError:
            pass
        out[k] = v
    return out


def band(score: int) -> str:
    if score >= 8:
        return "Must-look (8–10)"
    if score >= 6:
        return "Worth a skim (6–7)"
    if score >= 4:
        return "FYI (4–5)"
    return "Archive (<4)"


def main() -> int:
    root = Path("kb/entries")
    if not root.exists():
        print("kb/entries does not exist; nothing to index", file=sys.stderr)
        return 1

    entries = []
    for p in sorted(root.glob("*.md")):
        fm = parse_front_matter(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        fm["_path"] = str(p)
        entries.append(fm)

    entries.sort(key=lambda e: e.get("date_seen", ""), reverse=True)

    by_band: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        try:
            sc = int(e.get("score", 0))
        except Exception:
            sc = 0
        if e.get("status") == "archived":
            continue
        by_band[band(sc)].append(e)

    lines = ["# ai-radar — KB Index", "",
             f"_{len(entries)} entries indexed_  ", ""]
    for b in [
        "Must-look (8–10)",
        "Worth a skim (6–7)",
        "FYI (4–5)",
    ]:
        items = by_band.get(b, [])
        lines.append(f"## {b} — {len(items)}")
        lines.append("")
        if not items:
            lines.append("_none_\n")
            continue
        for e in items:
            tags = e.get("tags") or []
            if isinstance(tags, list):
                tag_str = ", ".join(str(t) for t in tags)
            else:
                tag_str = str(tags)
            title = e.get("title", "(untitled)")
            score = e.get("score", "?")
            date = e.get("date_seen", "?")
            path = e.get("_path", "")
            rel = path.replace("kb/", "", 1) if path.startswith("kb/") else path
            lines.append(
                f"- [{score}] [{title}]({rel}) — {date} — `{tag_str}`"
            )
        lines.append("")

    out_path = Path("kb/INDEX.md")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
