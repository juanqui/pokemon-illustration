"""Build the gray-padded outpaint input, the known-pixel mask, and previews.

Source card window interior measured from assets/source-card.png:
  x 68..682, y 103..482  (614x379)
The 30th-anniversary Pikachu sticker overlaps the bottom-right corner; that
corner is cut out to gray so the outpaint model invents matching foliage there.
"""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
W, H = 1440, 2016                 # 2x card canvas, ratio 0.7143
CROP = (68, 103, 682, 482)        # art window interior
PLATE_W = W                       # plate fills card width
PLATE_Y = 350                     # top of known art on the canvas
NOTCH = (476, 244)                # plate-space start of sticker corner (x, y)
GRAY = (128, 128, 128)

src = Image.open(ROOT / "assets/source-card.png").convert("RGB")
plate = src.crop(CROP)
scale = PLATE_W / plate.width
plate_h = round(plate.height * scale)
plate_big = plate.resize((PLATE_W, plate_h), Image.LANCZOS)
plate_big.save(ROOT / "work/plate.png")

canvas = Image.new("RGB", (W, H), GRAY)
canvas.paste(plate_big, (0, PLATE_Y))

# Sticker corner in canvas pixels.
nx = round(NOTCH[0] * scale)
ny = PLATE_Y + round(NOTCH[1] * scale)
notch = (nx, ny, W, PLATE_Y + plate_h)

# Gray input: rounded notch.
gray = canvas.copy()
d = ImageDraw.Draw(gray)
d.rounded_rectangle(notch, radius=44, fill=GRAY)
gray.save(ROOT / "work/canvas_gray.png")

# Known mask: plate area minus notch, with a soft edge for later blending.
mask = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(mask)
d.rectangle((0, PLATE_Y, W, PLATE_Y + plate_h), fill=255)
d.rounded_rectangle(notch, radius=44, fill=0)
mask = mask.filter(ImageFilter.GaussianBlur(1.2))
mask.save(ROOT / "work/known_mask.png")

# Composition preview: known art + a soft green/orange wash standing in for
# the extension, so framing can be judged before sampling.
bg = canvas.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(18)).resize((W, H))
bg.paste(plate_big, (0, PLATE_Y))
bg.save(ROOT / "work/composition_preview.png")

meta = dict(canvas=[W, H], plate_y=PLATE_Y, plate_h=plate_h, scale=round(scale, 5),
            crop=CROP, notch=list(notch))
(ROOT / "work/input_meta.json").write_text(json.dumps(meta, indent=2))
print(json.dumps(meta, indent=2))
