#!/usr/bin/env python3
"""Read-only Gemini local request-budget check; makes no network requests."""
import argparse
import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.limit < 1:
        raise SystemExit("INVALID_LIMIT")
    root = Path(__file__).resolve().parents[1]
    ledger = root / "evaluation/.gemini_review_request_ledger.json"
    data = json.loads(ledger.read_text(encoding="utf-8")) if ledger.exists() else {}
    now = dt.datetime.now(dt.timezone.utc)
    day_pt = now.astimezone(ZoneInfo("America/Los_Angeles")).date().isoformat()
    used = max(int(data.get(now.date().isoformat(), 0)), int(data.get("PT:" + day_pt, 0)))
    print(json.dumps({"status": "ESEGUITO", "day_pacific": day_pt,
        "local_used": used, "local_limit": args.limit,
        "local_remaining": max(0, args.limit - used),
        "google_remaining": None, "api_requests": 0}))

if __name__ == "__main__":
    main()
