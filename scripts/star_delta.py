#!/usr/bin/env python3
"""Append a star snapshot and compute the 7-day star delta for a GitHub repo.

Snapshots live in state/star-snapshots.jsonl, one line per observation:
    {"repo": "owner/name", "stars": 1234, "ts": "2026-05-12T07:00:00"}

Usage:
    python3 scripts/star_delta.py <owner/repo> <current_stars> [--state-file PATH]

Prints JSON:
    {"repo": "owner/repo", "current": 1234, "prior": 1100, "prior_ts": "...",
     "delta_7d": 134, "snapshots_seen": 5}

`prior` is the most recent snapshot >= 7 days old; if none, the oldest available.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def load_snapshots(path: Path, repo: str) -> list[dict]:
    if not path.exists():
        return []
    out = []
    repo_lc = repo.lower()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("repo", "").lower() == repo_lc:
                out.append(rec)
    out.sort(key=lambda r: r.get("ts", ""))
    return out


def pick_prior(snapshots: list[dict], now: datetime) -> dict | None:
    if not snapshots:
        return None
    cutoff = (now - timedelta(days=7)).isoformat()
    older = [s for s in snapshots if s.get("ts", "") <= cutoff]
    return older[-1] if older else snapshots[0]


def append_snapshot(path: Path, repo: str, stars: int, ts: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"repo": repo, "stars": stars, "ts": ts}) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="owner/name")
    ap.add_argument("current", type=int)
    ap.add_argument(
        "--state-file",
        default="state/star-snapshots.jsonl",
        help="path to snapshots jsonl",
    )
    ap.add_argument(
        "--no-append",
        action="store_true",
        help="compute delta but don't append a new snapshot",
    )
    args = ap.parse_args()

    state_file = Path(args.state_file)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    now_iso = now.isoformat()

    snapshots = load_snapshots(state_file, args.repo)
    prior = pick_prior(snapshots, now)

    result = {
        "repo": args.repo,
        "current": args.current,
        "prior": prior["stars"] if prior else None,
        "prior_ts": prior["ts"] if prior else None,
        "delta_7d": (args.current - prior["stars"]) if prior else None,
        "snapshots_seen": len(snapshots),
    }

    if not args.no_append:
        append_snapshot(state_file, args.repo, args.current, now_iso)

    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
