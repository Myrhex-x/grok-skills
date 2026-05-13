#!/usr/bin/env python3
"""
Helper script for Hantavirus News Tracker skill.
Manages persistent last-run timestamp for incremental news fetching.
"""

import datetime
import os
import sys

SKILL_DIR = "/home/workdir/.grok/skills/hantavirus-news-tracker"
LAST_RUN_FILE = os.path.join(SKILL_DIR, "last_run.txt")
DEFAULT_LOOKBACK_DAYS = 7


def get_last_run() -> datetime.datetime:
    """Return the last run datetime (UTC). Creates default if missing."""
    if os.path.exists(LAST_RUN_FILE):
        try:
            with open(LAST_RUN_FILE, "r", encoding="utf-8") as f:
                ts_str = f.read().strip()
                if ts_str:
                    # Handle both with and without timezone info
                    if ts_str.endswith("Z"):
                        ts_str = ts_str[:-1] + "+00:00"
                    return datetime.datetime.fromisoformat(ts_str).replace(tzinfo=datetime.timezone.utc)
        except (ValueError, OSError) as e:
            print(f"[WARN] Could not read last_run.txt: {e}", file=sys.stderr)
    
    # Default: 7 days ago (first-time use or corrupted file)
    default_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DEFAULT_LOOKBACK_DAYS)
    return default_dt


def save_last_run(dt: datetime.datetime) -> None:
    """Save current datetime as last run (UTC, ISO format)."""
    try:
        os.makedirs(SKILL_DIR, exist_ok=True)
        with open(LAST_RUN_FILE, "w", encoding="utf-8") as f:
            f.write(dt.isoformat())
        print(f"[OK] Updated last run time to {dt.isoformat()}")
    except OSError as e:
        print(f"[ERROR] Failed to save last_run.txt: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python hantavirus_news_helper.py [get-since | update-last | show-last]")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "get-since":
        last_dt = get_last_run()
        print(last_dt.isoformat())
    elif cmd == "update-last":
        now = datetime.datetime.now(datetime.timezone.utc)
        save_last_run(now)
    elif cmd == "show-last":
        last_dt = get_last_run()
        print(f"Last run: {last_dt.isoformat()}")
        print(f"Human: {last_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
