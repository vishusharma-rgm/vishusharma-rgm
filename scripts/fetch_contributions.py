"""Scrape the public contribution calendar (no token needed)."""
import json, re, sys, datetime as dt
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USER = "vishusharma-rgm"
URL = f"https://github.com/users/{USER}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # tooltips hold the real count: "3 contributions on ..." / "No contributions on ..."
    tips = {}
    for t in soup.find_all("tool-tip"):
        m = re.match(r"\s*(\d+|No)\s+contribution", t.get_text())
        if m and t.get("for"):
            tips[t["for"]] = 0 if m.group(1) == "No" else int(m.group(1))

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        if not td.get("data-date"):
            continue
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": tips.get(td.get("id"), 0),
        })
    days.sort(key=lambda d: d["date"])
    total = sum(d["count"] for d in days)
    return days, total


def stats(days):
    today = dt.date.today().isoformat()
    past = [d for d in days if d["date"] <= today]
    longest = run = 0
    for d in past:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    cur = 0
    for d in reversed(past):
        if d["count"] > 0:
            cur += 1
        elif d["date"] == today:
            continue  # today may not have commits yet
        else:
            break
    best = max(days, key=lambda d: d["count"]) if days else None
    months = {}
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]
    return {"current_streak": cur, "longest_streak": longest,
            "best_day": best, "months": months}


if __name__ == "__main__":
    days, total = fetch()
    if not days:
        sys.exit("no days parsed - GitHub HTML may have changed")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"user": USER, "total": total, "days": days,
                               **stats(days)}, indent=1))
    print(f"{len(days)} days, {total} contributions -> {OUT}")
