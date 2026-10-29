"""source-prepped.png -> monochrome ASCII portrait that types in row by row."""
from pathlib import Path
import numpy as np
from PIL import Image
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
COLS = 100
RAMP = " .:-=+*#%@"              # bright (sparse) -> dark (dense)
CW, CH = 3.7, 6.6              # char cell size in px (monospace 6px font)

img = Image.open(ROOT / "source-prepped.png").convert("L")
rows = round(COLS * img.height / img.width * (CW / CH))
g = np.array(img.resize((COLS, rows), Image.LANCZOS)) / 255.0
lines = []
for r in g:
    # dark pixel -> dense glyph
    lines.append("".join(RAMP[int((1 - v) * (len(RAMP) - 1))] for v in r).rstrip())

W, H = COLS * CW, rows * CH + 42
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">',
     '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:6px;fill:#c9d1d9;white-space:pre}.title{font-size:13px;font-weight:700}</style>',
     f'<rect width="{W:.0f}" height="{H:.0f}" rx="10" fill="#0d1117" stroke="#30363d"/>', "<defs>"]
o.insert(3, '<circle cx="18" cy="18" r="5" fill="#ff5f56"/><circle cx="36" cy="18" r="5" fill="#ffbd2e"/><circle cx="54" cy="18" r="5" fill="#27c93f"/>')
o.insert(4, f'<text x="{W/2:.1f}" y="23" text-anchor="middle" class="title">vishu@github ~ $ portrait.sh</text>')
for i, t in enumerate(lines):
    w = max(len(t), 1) * CW
    begin = i * 0.07
    o.append(f'<clipPath id="c{i}"><rect x="0" y="{i*CH+34:.1f}" width="0" height="{CH+1}">'
             f'<animate attributeName="width" from="0" to="{w+4:.1f}" dur="0.5s" begin="{begin:.2f}s" fill="freeze"/>'
             f'</rect></clipPath>')
o.append("</defs>")
for i, t in enumerate(lines):
    if t.strip():
        o.append(f'<text x="0" y="{34+(i+1)*CH:.1f}" xml:space="preserve" clip-path="url(#c{i})" '
                 f'textLength="{len(t)*CW:.1f}" lengthAdjust="spacing">{escape(t)}</text>')
o.append("</svg>")
(ROOT / "portrait-ascii.svg").write_text("\n".join(o))
print("wrote portrait-ascii.svg", rows, "rows")
