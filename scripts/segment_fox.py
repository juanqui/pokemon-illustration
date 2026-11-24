"""Segment the source fox with SAM; output a binary mask + overlay."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import torch
from segment_anything import sam_model_registry, SamPredictor

ROOT = Path(__file__).resolve().parents[1]
plate = Image.open(ROOT / "work/plate.png").convert("RGB")
w, h = plate.size
sam = sam_model_registry["vit_b"](checkpoint=str(ROOT / "work/sam_vit_b.pth"))
sam.to("cpu")
pred = SamPredictor(sam)
pred.set_image(np.array(plate))

# plate coordinates (1440x889): body, face, ears, tails, feet; negatives on path/hedge/sticker
pts = [(640, 470), (640, 300), (450, 110), (800, 90), (350, 430),
       (980, 430), (300, 650), (1060, 650), (600, 780)]
labels = [1] * len(pts)
neg = [(200, 220), (1250, 220), (100, 820), (1350, 820), (1200, 350)]
pts += neg
labels += [0] * len(neg)
box = np.array([120, 0, 1320, 885])

masks, scores, logits = pred.predict(point_coords=np.array(pts), point_labels=np.array(labels),
                                     box=box, multimask_output=True)
print("scores", scores.tolist())
for i, (m, s) in enumerate(zip(masks, scores)):
    out = plate.copy()
    overlay = Image.new("RGB", (w, h), (255, 0, 255))
    out = Image.composite(overlay, out, Image.fromarray((m * 160).astype(np.uint8)))
    out.save(ROOT / f"work/fox_mask_overlay_{i}.png")
    Image.fromarray((m * 255).astype(np.uint8)).save(ROOT / f"work/fox_mask_{i}.png")
    print(i, "area", int(m.sum()), "score", float(s))
