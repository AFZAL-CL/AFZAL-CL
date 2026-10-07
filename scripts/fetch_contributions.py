from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "contributions.json"
USERNAME = "AFZAL-CL"
URL = f"https://github.com/users/{USERNAME}/contributions"


def parse_count(label: str) -> int:
    m = re.search(r"(\d[\d,]*)\s+contribution", label or "", re.I)
    return int(m.group(1).replace(",", "")) if m else 0


def main() -> None:
    r = requests.get(URL, timeout=30, headers={"User-Agent": "AFZAL-CL-profile-bot/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        date = cell.get("data-date")
        if not date:
            continue
        count = parse_count(cell.get("aria-label", ""))
        # GitHub's contribution level is useful for the renderer, but count is canonical.
        cls = cell.get("class", [])
        level = 0
        for c in cls:
            m = re.fullmatch(r"ContributionCalendar-day(\d)", c)
            if m:
                level = int(m.group(1))
        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda x: x["date"])
    if not days:
        raise RuntimeError("GitHub returned no contribution cells")

    counts = [d["count"] for d in days]
    total = sum(counts)
    active = sum(c > 0 for c in counts)

    current = 0
    i = len(days) - 1
    while i >= 0 and days[i]["count"] == 0:
        i -= 1
    while i >= 0 and days[i]["count"] > 0:
        current += 1
        i -= 1

    longest = 0
    run = 0
    for c in counts:
        if c > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    best = max(days, key=lambda d: d["count"])
    monthly = defaultdict(int)
    for d in days:
        monthly[d["date"][:7]] += d["count"]

    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "stats": {
            "total": total,
            "active_days": active,
            "current_streak": current,
            "longest_streak": longest,
            "best_day": {"date": best["date"], "count": best["count"]},
            "average_active_day": round(total / active, 1) if active else 0,
            "monthly": dict(sorted(monthly.items())),
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(days)} days / {total} contributions")


if __name__ == "__main__":
    main()
