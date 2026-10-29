"""Turn data/portrait.png into a small optional ASCII portrait SVG."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


CHARS = " .:-=+*#%@"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/portrait.png")
    parser.add_argument("--output", default="portrait.svg")
    args = parser.parse_args()
    try:
        from PIL import Image
    except ImportError as error:
        raise SystemExit("Install Pillow first: pip install -r scripts/requirements.txt") from error
    image = Image.open(args.input).convert("L")
    image.thumbnail((70, 35))
    rows = []
    for y in range(image.height):
        line = "".join(CHARS[pixel * (len(CHARS) - 1) // 255] for pixel in [image.getpixel((x, y)) for x in range(image.width)])
        rows.append(f'<text x="20" y="{38 + y * 14}" class="ascii">{html.escape(line)}</text>')
    height = 60 + image.height * 14
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 {height}" role="img" aria-label="ASCII portrait">
<style>.bg{{fill:#0d1117}}.ascii{{fill:#7ee787;font:12px monospace;white-space:pre}}</style><rect class="bg" width="100%" height="100%" rx="14"/>{''.join(rows)}</svg>'''
    Path(args.output).write_text(svg, encoding="utf-8")
    print(f"Rendered {args.output}")


if __name__ == "__main__":
    main()
