"""Prep a photo for ASCII conversion: remove bg, boost contrast, white backdrop.
Usage: python scripts/prep_photo.py my-photo.jpg   ->  source-prepped.png
"""
import sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image
from rembg import remove

src = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "source-prepped.png"

cut = remove(Image.open(src).convert("RGB")).convert("RGBA")      # 1. isolate subject
bg = Image.new("RGBA", cut.size, (255, 255, 255, 255))
flat = Image.alpha_composite(bg, cut).convert("L")                 # 3. onto pure white
gray = np.array(flat)
mask = np.array(cut)[:, :, 3] > 10
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))        # 2. local contrast
boosted = clahe.apply(gray)
gray = np.where(mask, boosted, 255).astype("uint8")
Image.fromarray(gray).save(out)
print("saved", out)
