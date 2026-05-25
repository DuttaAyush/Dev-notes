# 🌱 Green Graph

An automated GitHub contribution tracker that keeps your profile graph active with natural-looking commit patterns — powered by GitHub Actions.

No local machine, no cron jobs on your PC, no manual effort. Set it up once and forget it.

---

## ✨ Features

- **Randomised commit count** — 0 to 9 commits per day, never the same pattern
- **Randomised timing** — commits land at different hours each day from a pool of 14 time slots
- **Deterministic daily plan** — all triggers on the same day agree on the plan using a date-based hash seed
- **Natural rest days** — occasionally produces zero-commit days so the graph doesn't look artificial
- **One-file configuration** — adjust commit range, time slots, and messages without touching the workflow
- **Zero maintenance** — runs entirely on GitHub Actions with no external dependencies

---

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── auto-commit.yml   # GitHub Actions workflow with 14 cron triggers
├── commit.py                  # Core logic — decides whether to commit or skip
├── config.json                # User-configurable settings
├── activity.log               # Append-only log updated by each commit
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- A GitHub account (free tier is sufficient)
- Git installed locally (for initial setup only)

### Step 1 — Create a Repository

1. Go to [github.com/new](https://github.com/new)
2. Name it something like `daily-tracker` or `activity-log`
3. Set visibility to **Public** (required for commits to appear on your profile graph)
4. **Do not** initialise with a README (we'll push our own)

### Step 2 — Push the Project

```bash
git init
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git add .
git commit -m "feat: initialise automated contribution tracker"
git branch -M main
git push -u origin main
```

### Step 3 — Enable Workflow Permissions

1. Navigate to your repository on GitHub
2. Go to **Settings → Actions → General**
3. Under **Workflow permissions**, select **Read and write permissions**
4. Click **Save**

### Step 4 — Verify

1. Go to the **Actions** tab in your repository
2. Select **🌱 Keep Graph Green**
3. Click **Run workflow → Run workflow** to trigger a manual test
4. Check the run logs to confirm the script executed successfully

The automated schedule will take over from here. No further action required.

---

## ⚙️ Configuration

All settings live in [`config.json`](config.json):

```json
{
  "min_commits": 0,
  "max_commits": 9,
  "time_pool": ["03:53", "05:17", "06:08", ...],
  "messages": ["chore: update dependencies", "fix: minor bug fix", ...]
}
```

| Key | Type | Description |
|---|---|---|
| `min_commits` | `int` | Minimum commits per day. Set to `0` for occasional rest days, `1` for always-green. |
| `max_commits` | `int` | Maximum commits per day. |
| `time_pool` | `string[]` | UTC times (HH:MM) that match the cron triggers in the workflow file. |
| `messages` | `string[]` | Pool of commit messages. One is randomly selected per commit. |

> **Note:** If you modify `time_pool`, you must also update the corresponding `cron` entries in `.github/workflows/auto-commit.yml` to match.

---

## 🧠 How It Works

1. **14 cron triggers** are defined in the workflow, spread across the day (9:23 AM – 1:51 AM IST).
2. Each trigger invokes `commit.py`, which:
   - Computes an MD5 hash of today's date to generate a deterministic seed.
   - Uses the seed to decide how many commits to make today (between `min_commits` and `max_commits`).
   - Uses the same seed to randomly select that many time slots from the pool.
   - Checks whether the current trigger's time slot was selected.
   - If selected → appends a timestamped entry to `activity.log`, commits with a random message, and pushes.
   - If not selected → exits silently with no changes.

Because every trigger on the same day hashes the same date string, they all independently arrive at the same commit plan — no shared state or coordination needed.

---

## 📊 Resource Usage

| Metric | Value |
|---|---|
| Runs per day | 14 (one per time slot) |
| Average commits per day | ~4.5 |
| Average run duration | ~10–30 seconds |
| Estimated monthly usage | ~100 minutes |
| GitHub Actions free tier (public repos) | **Unlimited** |

---

## 📝 License

This project is provided as-is for personal use. Use responsibly.
