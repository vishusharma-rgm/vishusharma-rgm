"""Render an animated, dependency-free contribution heatmap SVG."""

from __future__ import annotations

import argparse
import html
import json
from datetime import date, timedelta
from pathlib import Path


COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def longest_streak(days: list[dict[str, object]]) -> int:
    current = best = 0
    for item in days:
        if int(item.get("count", 0)) > 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def render(payload: dict[str, object]) -> str:
    days = payload.get("days", [])
    if not isinstance(days, list):
        days = []
    days = [item for item in days if isinstance(item, dict)]
    days = sorted(days, key=lambda item: str(item.get("date", "")))[-371:]
    by_date = {str(item.get("date")): item for item in days}
    if not days:
        today = date.today()
        start = today - timedelta(days=364)
        days = [{"date": (start + timedelta(days=i)).isoformat(), "count": 0, "level": 0} for i in range(365)]
    first = date.fromisoformat(str(days[0]["date"]))
    start = first.fromordinal(first.toordinal() - (first.weekday() + 1) % 7)
    cells = []
    labels = []
    cell = 13
    gap = 4
    x0, y0 = 38, 40
    total_weeks = 53
    for week in range(total_weeks):
        week_start = start.fromordinal(start.toordinal() + week * 7)
        if week_start.day <= 7 or week == 0:
            labels.append(f'<text x="{x0 + week * (cell + gap)}" y="24" class="month">{week_start.strftime("%b")}</text>')
        for row in range(7):
            day = week_start.fromordinal(week_start.toordinal() + row)
            item = by_date.get(day.isoformat(), {})
            count = int(item.get("count", 0))
            level = min(4, max(0, int(item.get("level", 0))))
            x = x0 + week * (cell + gap)
            y = y0 + row * (cell + gap)
            title = html.escape(f"{day.isoformat()}: {count} contribution{'s' if count != 1 else ''}")
            delay = (week * 7 + row) * 8
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{COLORS[level]}" class="cell" style="animation-delay:{delay}ms"><title>{title}</title></rect>')
    total = int(payload.get("total", sum(int(item.get("count", 0)) for item in days)))
    streak = longest_streak(days)
    username = html.escape(str(payload.get("username", "vishusharma-rgm")))
    width = x0 + total_weeks * (cell + gap) + 20
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 190" role="img" aria-label="{username} GitHub contribution heatmap">
<style>.bg{{fill:#0d1117}}.month{{fill:#8b949e;font:12px ui-monospace,SFMono-Regular,Menlo,monospace}}.caption{{fill:#c9d1d9;font:13px ui-monospace,SFMono-Regular,Menlo,monospace}}.cell{{opacity:0;animation:appear .45s ease forwards}}@keyframes appear{{to{{opacity:1}}}}@media(prefers-reduced-motion:reduce){{.cell{{animation:none;opacity:1}}}}</style>
<rect class="bg" width="100%" height="100%" rx="14"/>
<text x="{x0}" y="172" class="caption">{total} contributions · longest streak {streak} days · @{username}</text>
{''.join(labels)}
{''.join(cells)}
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/contributions.json")
    parser.add_argument("--output", default="contrib-heatmap.svg")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    Path(args.output).write_text(render(payload), encoding="utf-8")
    print(f"Rendered {args.output}")


if __name__ == "__main__":
    main()
