"""neofetch-style info card SVG. Edit ROWS to change content."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"

ROWS = [
    ("", "vishu@github", None),
    ("", "-" * 30, None),
    ("Role", "Java / Backend Developer", "#79c0ff"),
    ("Edu", "B.Tech CSE, BBDITM Lucknow (2024-28)", "#79c0ff"),
    ("Stack", "Java, MERN, JavaScript, DSA", "#d2a8ff"),
    ("Now", "DSA Visualizer IDE, ClientFlow, Nova", "#7ee787"),
    ("Built", "Task-Forge, Review-Sync, ResumePilot,", "#ffa657"),
    ("", "Smart-Expense-Tracker, Agentic-Task-Executor", "#ffa657"),
    ("DSA", "LeetCode: vishu___00 | CF: vishu__00", "#ff7b72"),
    ("Goal", "SDE internships, open source, GSoC", "#7ee787"),
]
W, LH, TOP = 490, 24, 56
H = TOP + len(ROWS) * LH + 24

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
o.append(f"""<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13px;fill:#c9d1d9}}
.k{{font-weight:bold}}
.r{{{'' if STATIC else 'opacity:0;'}animation:in .6s ease-out forwards}}
@keyframes in{{from{{opacity:0;transform:translateX(-12px)}}to{{opacity:1;transform:none}}}}
</style>""")
o.append(f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>')
o.append('<circle cx="18" cy="18" r="5" fill="#ff5f56"/><circle cx="36" cy="18" r="5" fill="#ffbd2e"/><circle cx="54" cy="18" r="5" fill="#27c93f"/>')
o.append(f'<text x="{W/2}" y="22" text-anchor="middle" style="fill:#8b949e;font-size:12px">neofetch</text>')
for i, (k, v, c) in enumerate(ROWS):
    y = TOP + i * LH
    d = 0.35 * i + 0.3
    if not k and c is None:
        first = i == 0
        o.append(f'<g class="r" style="animation-delay:{d:.2f}s"><text x="22" y="{y}" '
                 f'style="fill:{"#39d353" if first else "#484f58"};font-weight:bold">{escape(v)}</text></g>')
    else:
        key = f'<tspan class="k" style="fill:{c}">{escape(k + ": " if k else "")}</tspan>'
        pad = "" if k else " " * 7
        o.append(f'<g class="r" style="animation-delay:{d:.2f}s"><text x="22" y="{y}" xml:space="preserve">'
                 f'{key}{pad}{escape(v)}</text></g>')
o.append("</svg>")
(ROOT / "info-card.svg").write_text("\n".join(o))
print("wrote info-card.svg")
