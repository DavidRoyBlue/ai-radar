#!/usr/bin/env python3
"""Filter a stream of candidates against state/seen.json by canonical key.

Reads JSON-lines from stdin, each line a candidate dict with at minimum
`url` and `source`. Computes canonical_key (via canonical_key.py logic) and
keeps only candidates not already in `state/seen.json`.

Outputs the surviving candidates as JSON-lines on stdout, each augmented with
a `canonical_key` field.

Side-effects: NONE by default. Pass --commit to write surviving keys back to
seen.json (with date_seen). Run without --commit during prefilter; with --commit
only AFTER scoring is done and entries are written.

Usage:
    cat fetched.jsonl | python3 scripts/dedupe.py
    cat scored.jsonl  | python3 scripts/dedupe.py --commit
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Local import: same dir
sys.path.insert(0, str(Path(__file__).resolve().parent))
from canonical_key import canonical_key  # noqa: E402


def load_seen(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_seen(path: Path, seen: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(seen, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--seen-file", default="state/seen.json", help="path to seen.json"
    )
    ap.add_argument(
        "--commit",
        action="store_true",
        help="persist surviving canonical_keys back to seen.json",
    )
    args = ap.parse_args()

    seen_path = Path(args.seen_file)
    seen = load_seen(seen_path)
    today = datetime.now(timezone.utc).date().isoformat()

    # Within this batch, also dedupe by canonical_key. Merge seen_via.
    batch: dict[str, dict] = {}

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        url = item.get("url")
        source = item.get("source", "unknown")
        if not url:
            continue
        key = canonical_key(source, url)
        item["canonical_key"] = key

        if key in seen:
            # Already persisted — record extra `seen_via` if new
            existing = seen[key]
            if isinstance(existing, dict):
                seen_via = set(existing.get("seen_via", []))
                seen_via.add(source)
                existing["seen_via"] = sorted(seen_via)
            continue

        if key in batch:
            # Already in this batch from another source — merge seen_via
            prior = batch[key]
            via = set(prior.get("seen_via", [prior.get("source")]))
            via.add(source)
            prior["seen_via"] = sorted(via)
            continue

        item["seen_via"] = [source]
        batch[key] = item

    for item in batch.values():
        print(json.dumps(item))

    survivors_keys = [(k, v.get("seen_via", [v.get("source")])) for k, v in batch.items()]

    if args.commit and survivors_keys:
        for key, via in survivors_keys:
            seen[key] = {
                "first_seen": today,
                "seen_via": list(via) if isinstance(via, list) else [via],
            }
        save_seen(seen_path, seen)

    return 0


if __name__ == "__main__":
    sys.exit(main())
