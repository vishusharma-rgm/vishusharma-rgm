"""Prepare a portrait for the optional ASCII SVG generator."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--output", default="data/portrait.png")
    args = parser.parse_args()
    try:
        from PIL import Image, ImageOps
    except ImportError as error:
        raise SystemExit("Install Pillow first: pip install -r scripts/requirements.txt") from error
    image = Image.open(args.image).convert("L")
    image = ImageOps.fit(image, (160, 160), method=Image.Resampling.LANCZOS)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(f"Saved prepared portrait to {output}")


if __name__ == "__main__":
    main()
