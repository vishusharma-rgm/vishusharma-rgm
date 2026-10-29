"""Render contribution summary cards and a compact monthly bar chart."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/contributions.json")
    parser.add_argument("--output", default="profile-stats.svg")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    days = data.get("days", [])
    total = int(data.get("total", 0))
    active = sum(1 for item in days if int(item.get("count", 0)) > 0)
    best = data.get("best_day") or {"count": 0, "date": "—"}
    average = round(total / active, 1) if active else 0
    months = data.get("months") or {}
    month_items = list(months.items())[-12:]
    max_month = max([int(value) for _, value in month_items] or [1])
    bars = []
    for index, (month, value) in enumerate(month_items):
        x = 25 + index * 36
        height = max(8, round(int(value) / max_month * 105))
        bars.append(f'<rect x="{x}" y="{374 - height}" width="22" height="{height}" rx="4" fill="#39d353"><title>{html.escape(month)}: {int(value)} contributions</title></rect>')
        bars.append(f'<text x="{x + 11}" y="394" text-anchor="middle" class="axis">{html.escape(month[5:])}</text>')
    cards = [
        ("$ current streak", f"{int(data.get('current_streak', 0))}", "days", "#39d353"),
        ("$ longest streak", f"{int(data.get('longest_streak', 0))}", "days", "#f0f6fc"),
        ("$ contributions", f"{total:,}", "last year", "#f0f6fc"),
        ("$ active days", f"{active}", f"/ {len(days)}", "#79c0ff"),
        ("$ best day", f"{int(best.get('count', 0))}", str(best.get("date", "—")), "#ffa657"),
        ("$ avg / active day", f"{average}", "contributions", "#d2a8ff"),
    ]
    card_svg = []
    for index, (label, value, note, color) in enumerate(cards):
        col, row = index % 2, index // 2
        x, y = 18 + col * 235, 42 + row * 62
        card_svg.append(f'<rect x="{x}" y="{y}" width="223" height="52" rx="8" class="card"/><text x="{x + 12}" y="{y + 16}" class="label">{html.escape(label)}</text><text x="{x + 12}" y="{y + 40}" class="value" style="fill:{color}">{html.escape(value)}</text><text x="{x + 105}" y="{y + 40}" class="note">{html.escape(note)}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 494 415" role="img" aria-label="Contribution statistics">
<style>.bg{{fill:#0d1117;stroke:#30363d;stroke-width:2}}.card{{fill:#161b22;stroke:#30363d}}.label,.note,.axis{{fill:#8b949e;font:11px ui-monospace,SFMono-Regular,Menlo,monospace}}.value{{font:700 22px ui-monospace,SFMono-Regular,Menlo,monospace}}.title{{fill:#c9d1d9;font:700 13px ui-monospace,SFMono-Regular,Menlo,monospace}}</style>
<rect class="bg" x="1" y="1" width="492" height="413" rx="12"/><text x="18" y="24" class="title">vishu@github ~ $ stats.sh</text>{''.join(card_svg)}<text x="18" y="236" class="title">$ contributions / month</text>{''.join(bars)}</svg>'''
    Path(args.output).write_text(svg, encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
