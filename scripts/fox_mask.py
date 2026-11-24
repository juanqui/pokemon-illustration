"""Refine SAM mask, composite exact fox over a raw outpaint, verify pixels."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
PLATE_Y = 350
mask = np.array(Image.open(ROOT / "work/fox_mask_0.png").convert("L")) > 127
# largest connected component
lab, n = ndimage.label(mask)
sizes = ndimage.sum(mask, lab, range(1, n + 1))
keep = (np.argmax(sizes) + 1)
mask = lab == keep
# fill enclosed holes (eyes, chest)
mask = ndimage.binary_fill_holes(mask)
# close pinholes, keep silhouette
mask = ndimage.binary_closing(mask, iterations=2)
mask = ndimage.binary_fill_holes(mask)
ys, xs = np.where(mask)
print("mask bbox", xs.min(), xs.max(), ys.min(), ys.max(), "area", mask.sum())
Image.fromarray((mask * 255).astype(np.uint8)).save(ROOT / "work/fox_mask_final.png")
soft = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
soft.save(ROOT / "work/fox_mask_soft.png")

# composite exact fox over raw scene
base = Image.open(sys.argv[1]).convert("RGBA")
plate = Image.open(ROOT / "work/plate.png").convert("RGBA")
layer = Image.new("RGBA", (1440, 2016), (0, 0, 0, 0))
layer.paste(plate, (0, PLATE_Y))
alpha = Image.new("L", (1440, 2016), 0)
alpha.paste(soft, (0, PLATE_Y))
layer.putalpha(alpha)
out = Image.alpha_composite(base, layer)
out.convert("RGB").save(sys.argv[2])
out.resize((720, 1008), Image.LANCZOS).convert("RGB").save(ROOT / "work/fox_on_scene_preview.png")

# verification: inside an eroded mask the result must equal the plate exactly
er = ndimage.binary_erosion(mask, iterations=5)
a = np.asarray(out.convert("RGB"))[PLATE_Y:PLATE_Y + 889]
b = np.asarray(plate.convert("RGB"))
d = np.abs(a.astype(int) - b.astype(int))
print("interior pixels", er.sum(), "MAE", float(d[er].mean()), "max", int(d[er].max()))
print("global plate band MAE (reference)", float(d.mean()))
