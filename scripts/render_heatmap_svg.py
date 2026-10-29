"""Render data/contributions.json as an animated 53x7 heatmap SVG."""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "contributions.json").read_text())

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX, GAP = 12, 3
PITCH = BOX + GAP
LEFT, TOP = 40, 56
W = LEFT + 53 * PITCH + 20          # ~855
H = TOP + 7 * PITCH + 62

days = DATA["days"]
mx = max((d["count"] for d in days), default=1) or 1
first = dt.date.fromisoformat(days[0]["date"])
first_dow = (first.weekday() + 1) % 7   # Sunday = 0


def level(d):
    if d["level"] >= 4 and d["count"] >= 0.6 * mx:
        return 5
    return min(d["level"], 4)


out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a("""<style>
text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e;font-size:10px}
.t{fill:#c9d1d9;font-size:12px}
.g{fill:#39d353}
.c{opacity:0;transform-box:fill-box;transform-origin:center;animation:in .5s ease-out forwards}
@keyframes in{from{opacity:0;transform:translateY(-10px) scale(.6)}to{opacity:1;transform:none}}
.f{opacity:0;animation:fd .8s ease-out forwards}
@keyframes fd{to{opacity:1}}
</style>""")
a(f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>')
a('<circle cx="18" cy="18" r="5" fill="#ff5f56"/><circle cx="36" cy="18" r="5" fill="#ffbd2e"/><circle cx="54" cy="18" r="5" fill="#27c93f"/>')
a(f'<text class="t" x="{W/2}" y="22" text-anchor="middle">vishu@github: ~/contributions</text>')

# month labels (skip a label if it would crowd the previous one)
last_m, last_week = None, -10
for i, d in enumerate(days):
    date = dt.date.fromisoformat(d["date"])
    week = (i + first_dow) // 7
    if date.month != last_m:
        last_m = date.month
        if week - last_week >= 3:
            a(f'<text x="{LEFT + week*PITCH}" y="{TOP-8}">{date.strftime("%b")}</text>')
            last_week = week
# weekday labels
for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    a(f'<text x="8" y="{TOP + r*PITCH + 10}">{name}</text>')

# cells
for i, d in enumerate(days):
    idx = i + first_dow
    week, dow = divmod(idx, 7)
    x, y = LEFT + week * PITCH, TOP + dow * PITCH
    delay = (week + dow) * 0.018
    a(f'<rect class="c" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="3" '
      f'fill="{PALETTE[level(d)]}" style="animation-delay:{delay:.2f}s">'
      f'<title>{d["count"]} on {d["date"]}</title></rect>')

# legend + footer
fy = TOP + 7 * PITCH + 24
a(f'<text class="f g" x="{LEFT}" y="{fy}" style="animation-delay:2.4s;font-size:12px">'
  f'{DATA["total"]:,} contributions in the last year</text>')
a(f'<text class="f" x="{LEFT}" y="{fy+20}" style="animation-delay:2.6s">'
  f'current streak: {DATA["current_streak"]}d  |  longest streak: {DATA["longest_streak"]}d  |  '
  f'best day: {DATA["best_day"]["count"]} ({DATA["best_day"]["date"]})</text>')
lx = W - 20 - (6 * PITCH) - 60
a(f'<text x="{lx-30}" y="{fy+8}">Less</text>')
for k, c in enumerate(PALETTE):
    a(f'<rect x="{lx+k*PITCH}" y="{fy-2}" width="{BOX}" height="{BOX}" rx="3" fill="{c}"/>')
a(f'<text x="{lx+6*PITCH+4}" y="{fy+8}">More</text>')
a("</svg>")
(ROOT / "contrib-heatmap.svg").write_text("\n".join(out))
print("wrote contrib-heatmap.svg", W, H)
