"""Fetch a public GitHub contribution calendar for the profile README.

The GitHub Actions token is used only for the GraphQL read. If the request
cannot be made (for example, during local preview), an existing JSON file is
kept so the renderer remains usable offline.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path


QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount contributionLevel }
        }
      }
    }
  }
}
"""

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fallback_days() -> list[dict[str, object]]:
    today = date.today()
    start = today - timedelta(days=364)
    return [{"date": (start + timedelta(days=i)).isoformat(), "count": 0, "level": 0} for i in range(365)]


def fetch(login: str, token: str) -> dict[str, object]:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-art-workflow"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise RuntimeError(json.dumps(payload.get("errors", payload)))
    calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [
        {"date": item["date"], "count": int(item["contributionCount"]), "level": LEVELS.get(item["contributionLevel"], 0)}
        for week in calendar["weeks"]
        for item in week["contributionDays"]
    ]
    return {"username": login, "total": int(calendar["totalContributions"]), "days": days}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default="vishusharma-rgm")
    parser.add_argument("--output", default="data/contributions.json")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            raise RuntimeError("GITHUB_TOKEN is not available")
        result = fetch(args.user, token)
    except (OSError, urllib.error.URLError, RuntimeError, json.JSONDecodeError) as error:
        if output.exists():
            print(f"Contribution fetch skipped: {error}; keeping {output}")
            return
        print(f"Contribution fetch skipped: {error}; creating an empty preview")
        days = fallback_days()
        result = {"username": args.user, "total": 0, "days": days}
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {result['total']} contributions to {output}")


if __name__ == "__main__":
    main()
