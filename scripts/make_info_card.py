"""Create the terminal-style profile information card."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


# Edit this list when the profile changes.
ROWS = [
    ("role", "Java & Backend Developer"),
    ("stack", "Java · Spring · Node · React · MongoDB"),
    ("building", "PrePora · Nova · Agentic tools"),
    ("practice", "LeetCode · Codeforces · DSA"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="info-card.svg")
    args = parser.parse_args()
    lines = []
    for index, (label, value) in enumerate(ROWS):
        y = 92 + index * 34
        lines.append(f'<text x="38" y="{y}" class="label">{html.escape(label.upper())}</text><text x="155" y="{y}" class="value">{html.escape(value)}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" role="img" aria-label="Vishu Sharma profile information">
<style>.bg{{fill:#0d1117;stroke:#30363d;stroke-width:2}}.bar{{fill:#161b22}}.title{{fill:#f0f6fc;font:700 24px ui-monospace,SFMono-Regular,Menlo,monospace}}.label{{fill:#7ee787;font:700 12px ui-monospace,SFMono-Regular,Menlo,monospace}}.value{{fill:#c9d1d9;font:14px ui-monospace,SFMono-Regular,Menlo,monospace}}</style>
<rect class="bg" x="1" y="1" width="898" height="258" rx="16"/><rect class="bar" x="1" y="1" width="898" height="43" rx="16"/><circle cx="28" cy="22" r="7" fill="#ff7b72"/><circle cx="50" cy="22" r="7" fill="#d29922"/><circle cx="72" cy="22" r="7" fill="#7ee787"/><text x="38" y="76" class="title">vishu@github:~$ whoami</text>{''.join(lines)}</svg>'''
    Path(args.output).write_text(svg, encoding="utf-8")
    print(f"Rendered {args.output}")


if __name__ == "__main__":
    main()
