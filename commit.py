"""
Decides whether to commit at the current trigger time.

Uses an MD5 hash of today's date as a seed so all triggers on the
same day agree on the commit count and chosen time slots.
"""

import hashlib
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timezone


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        return json.load(f)


def get_daily_seed(date_str: str) -> int:
    """Hash the date string to get a deterministic but unpredictable seed."""
    h = hashlib.md5(date_str.encode()).hexdigest()
    return int(h, 16)


def decide_today(config: dict, date_str: str) -> tuple[int, list[str]]:
    """Return (commit_count, chosen_slots) for the given date."""
    seed = get_daily_seed(date_str)
    rng = random.Random(seed)

    min_c = config["min_commits"]
    max_c = config["max_commits"]
    pool = config["time_pool"]

    commit_count = rng.randint(min_c, max_c)

    # Pick which time slots are active today
    if commit_count >= len(pool):
        chosen_slots = list(pool)
    else:
        chosen_slots = rng.sample(pool, commit_count)

    return commit_count, chosen_slots


def pick_message(config: dict, date_str: str, slot: str) -> str:
    """Pick a deterministic-but-random message for this date + slot combo."""
    seed = get_daily_seed(date_str + slot)
    rng = random.Random(seed)
    return rng.choice(config["messages"])


def git_commit(message: str):
    """Stage activity.log and commit with the given message."""
    log_path = os.path.join(os.path.dirname(__file__), "activity.log")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(log_path, "a") as f:
        f.write(f"{timestamp} — {message}\n")

    subprocess.run(["git", "add", "activity.log"], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)


def main():
    config = load_config()

    # Current trigger time in UTC (HH:MM matching cron format)
    now_utc = datetime.now(timezone.utc)
    current_slot = now_utc.strftime("%H:%M")
    date_str = now_utc.strftime("%Y%m%d")

    commit_count, chosen_slots = decide_today(config, date_str)

    print(f"Date: {date_str}")
    print(f"Commits today: {commit_count}")
    print(f"Chosen slots: {chosen_slots}")
    print(f"Current slot: {current_slot}")

    if commit_count == 0:
        print("Today is a rest day. Skipping.")
        sys.exit(0)

    # Check if current trigger is one of today's chosen slots
    if current_slot not in chosen_slots:
        print(f"Slot {current_slot} not chosen today. Skipping.")
        sys.exit(0)

    message = pick_message(config, date_str, current_slot)
    print(f"Committing with message: {message}")
    git_commit(message)
    print("Done!")


if __name__ == "__main__":
    main()
