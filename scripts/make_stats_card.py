"""Render the animated terminal-style contribution statistics card."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def value(data: dict, key: str) -> int:
    raw = data.get(key, 0)
    return int(raw.get("length", 0) if isinstance(raw, dict) else raw)


def format_metric(metric: int | float) -> str:
    if isinstance(metric, float):
        return f"{metric:,.1f}"
    return f"{int(metric):,}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/contributions.json")
    parser.add_argument("--output", default="profile-stats-animated.svg")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    days = data.get("days", [])
    total = int(data.get("total", data.get("total_contributions", 0)))
    active = int(data.get("active_days", sum(int(d.get("count", 0)) > 0 for d in days)))
    best = data.get("best_day") or {"count": 0, "date": "—"}
    average = float(data.get("avg_per_active_day", round(total / active, 1) if active else 0))
    months = data.get("months") or {}
    if isinstance(months, list):
        months = {item["month"]: item["total"] for item in months}
    month_items = list(months.items())[-12:]
    max_month = max([int(v) for _, v in month_items] or [1])

    cards = [
        ("$ current streak", value(data, "current_streak"), "days", "#39d353"),
        ("$ longest streak", value(data, "longest_streak"), "days", "#f0f6fc"),
        ("$ contributions", total, "last year", "#f0f6fc"),
        ("$ active days", active, f"/ {len(days)}", "#79c0ff"),
        ("$ best day", int(best.get("count", 0)), str(best.get("date", "—")), "#ffa657"),
        ("$ avg / active day", average, "contributions", "#d2a8ff"),
    ]

    card_parts = []
    for index, (label, metric, note, color) in enumerate(cards):
        col, row = index % 2, index // 2
        x, y = 18 + col * 235, 42 + row * 62
        delay = 0.22 + index * 0.12
        count_start = delay + 0.32
        frames = []
        for frame in range(1, 17):
            progress = frame / 16
            shown = metric * (1 - (1 - progress) ** 3)
            if isinstance(metric, float):
                shown = round(shown, 1)
            else:
                shown = int(round(shown))
            start = count_start + 1.1 * (frame - 1) / 16
            end = count_start + 1.1 * frame / 16
            events = f'<set attributeName="opacity" to="1" begin="{start:.3f}s"/>'
            if frame < 16:
                events += f'<set attributeName="opacity" to="0" begin="{end:.3f}s"/>'
            frames.append(
                f'<text x="{x + 12}" y="{y + 40}" opacity="0" class="value" style="fill:{color}">'
                f'{html.escape(format_metric(shown))}{events}</text>'
            )
        card_parts.append(
            f'<g class="metric" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{y}" width="223" height="52" rx="8" class="card"/>'
            f'<text x="{x + 12}" y="{y + 16}" class="label">{html.escape(label)}</text>'
            f'{"".join(frames)}'
            f'<text x="{x + 105}" y="{y + 40}" class="note">{html.escape(str(note))}</text>'
            '</g>'
        )

    bar_parts = []
    for index, (month, amount) in enumerate(month_items):
        x = 25 + index * 36
        height = max(8, round(int(amount) / max_month * 105))
        y = 374 - height
        delay = 0.82 + index * 0.07
        bar_parts.append(
            f'<g class="bar" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{y}" width="22" height="{height}" rx="4" fill="#39d353">'
            f'<title>{html.escape(month)}: {int(amount)} contributions</title>'
            f'<animate attributeName="y" from="374" to="{y}" dur="0.7s" fill="freeze" begin="{delay:.2f}s"/>'
            f'<animate attributeName="height" from="0" to="{height}" dur="0.7s" fill="freeze" begin="{delay:.2f}s"/>'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" fill="freeze" begin="{delay:.2f}s"/>'
            '</rect>'
            f'<text x="{x + 11}" y="394" text-anchor="middle" class="axis">{html.escape(month[5:])}</text>'
            '</g>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 494 415" role="img" aria-label="Contribution statistics">
<style>
.bg{{fill:#0d1117;stroke:#30363d;stroke-width:2}}
.card{{fill:#161b22;stroke:#30363d}}
.label,.note,.axis{{fill:#8b949e;font:11px ui-monospace,SFMono-Regular,Menlo,monospace}}
.value{{font:700 22px ui-monospace,SFMono-Regular,Menlo,monospace}}
.title{{fill:#c9d1d9;font:700 13px ui-monospace,SFMono-Regular,Menlo,monospace}}
@keyframes slideIn{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes barIn{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
.metric{{opacity:0;animation:slideIn .55s cubic-bezier(.2,.8,.2,1) both}}
.bar{{opacity:0;animation:barIn .55s cubic-bezier(.2,.8,.2,1) both}}
.terminal{{opacity:0;animation:slideIn .45s ease-out .05s forwards}}
</style>
<rect class="bg" x="1" y="1" width="492" height="413" rx="12"/>
<text x="18" y="24" class="title terminal">vishu@github ~ $ stats.sh</text>
{''.join(card_parts)}
<text x="18" y="236" class="title terminal" style="animation-delay:.72s">$ contributions / month</text>
{''.join(bar_parts)}
</svg>'''
    Path(args.output).write_text(svg, encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
