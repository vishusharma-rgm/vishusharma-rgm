#!/usr/bin/env python3
"""Render Vishu's personal terminal-style profile card."""

import html
import os


OUT = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")
WIDTH = 720
HEIGHT = 390
ROWS = [
    ("Role", "Java / Backend Developer", "#79c0ff"),
    ("Edu", "B.Tech CSE, BBDITM Lucknow (2024-28)", "#79c0ff"),
    ("Stack", "Java, MERN, JavaScript, DSA", "#d2a8ff"),
    ("Now", "DSA Visualizer IDE, ClientFlow, Nova", "#7ee787"),
    ("Built", "Task-Forge, Review-Sync, ResumePilot", "#ffa657"),
    ("", "Smart-Expense-Tracker, Agentic-Task-Executor", "#ffa657"),
    ("DSA", "LeetCode vishu___00 | Codeforces vishu__00", "#ff7b72"),
    ("Goal", "SDE internships, open source, GSoC", "#7ee787"),
]


def esc(value):
    return html.escape(value, quote=True)


def render():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" aria-label="Vishu Sharma profile card">',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}</style>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<circle cx="22" cy="22" r="5" fill="#ff5f56"/>',
        '<circle cx="40" cy="22" r="5" fill="#ffbd2e"/>',
        '<circle cx="58" cy="22" r="5" fill="#27c93f"/>',
        f'<text x="{WIDTH / 2:.1f}" y="27" text-anchor="middle" fill="#8b949e" font-size="13">vishu@github ~ $ whoami</text>',
        '<text x="28" y="64" fill="#39d353" font-size="16" font-weight="700">vishu@github</text>',
        '<text x="28" y="84" fill="#484f58" font-size="13" font-weight="700">' + "-" * 76 + '</text>',
    ]

    y = 116
    for key, value, color in ROWS:
        if key:
            parts.append(
                f'<text x="28" y="{y}" fill="#c9d1d9" font-size="15">'
                f'<tspan fill="{color}" font-weight="700">{esc(key)}: </tspan>{esc(value)}</text>'
            )
        else:
            parts.append(f'<text x="28" y="{y}" fill="#c9d1d9" font-size="15">{esc(value)}</text>')
        y += 30

    parts.append(
        f'<text x="28" y="{HEIGHT - 24}" fill="#7d8590" font-size="12">'
        'building useful software, one commit at a time</text>'
    )
    parts.append('</svg>')
    return ''.join(parts)


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as file:
        file.write(render())
    print(f"wrote {OUT}")
