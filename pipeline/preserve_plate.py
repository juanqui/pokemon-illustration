"""Strict outpainting composite.

The source plate is pasted back untouched; only pixels outside the plate can
come from the generative model. A soft, edge-replicated band bridges the plate
boundary so the extension does not show a hard rim, but it never reaches inside
the plate (the exact plate is composited last).
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 1440, 2016
PLATE_Y = 350
F = 96  # outward seam band, px


def main():
    p = argparse.ArgumentParser()
    p.add_argument("generated")
    p.add_argument("out")
    p.add_argument("--feather", type=int, default=96)
    a = p.parse_args()

    gen = Image.open(a.generated).convert("RGB").resize((W, H), Image.LANCZOS)
    plate = Image.open(ROOT / "work/plate.png").convert("RGB")
    ph = plate.height
    F = a.feather

    # Edge-extended plate: top/bottom rows stretched into soft bands.
    top = plate.crop((0, 0, W, 1)).resize((W, F), Image.LANCZOS).filter(ImageFilter.GaussianBlur(9))
    bot = plate.crop((0, ph - 1, W, ph)).resize((W, F), Image.LANCZOS).filter(ImageFilter.GaussianBlur(9))
    ext = Image.new("RGB", (W, ph + 2 * F))
    ext.paste(top, (0, 0))
    ext.paste(plate, (0, F))
    ext.paste(bot, (0, F + ph))

    # Alpha for the edge layer: 0 at outer band edge, 1 at the plate boundary.
    am = Image.new("L", (W, ph + 2 * F), 0)
    px = am.load()
    for y in range(F):
        px_row = round(255 * (y + 1) / F)
        for x in range(W):
            px[x, y] = px_row
            px[x, F + ph + y] = 255 - px_row
    for y in range(F, F + ph):
        for x in range(W):
            px[x, y] = 255
    am = am.filter(ImageFilter.GaussianBlur(0.8))

    # Sticker corner: remove it from both the plate mask and the edge layer.
    meta = json.loads((ROOT / "work/input_meta.json").read_text())
    nx, ny, nx1, ny1 = meta["notch"]
    ny -= PLATE_Y
    ny1 -= PLATE_Y
    notch = Image.new("L", (W, ph + 2 * F), 0)
    ImageDraw.Draw(notch).rounded_rectangle((nx, F + ny, nx1, F + ny1), radius=44, fill=255)
    notch = notch.filter(ImageFilter.GaussianBlur(11))
    am = Image.composite(Image.new("L", am.size, 0), am, notch)  # 0 in notch

    edge_layer = ext.convert("RGBA")
    edge_layer.putalpha(am)

    # Exact plate mask: 255 inside, 0 outside, 0 in the sticker notch.
    pm = Image.new("L", (W, ph), 255)
    nd = Image.new("L", (W, ph), 0)
    ImageDraw.Draw(nd).rounded_rectangle((nx, ny, nx1, ny1), radius=44, fill=255)
    nd = nd.filter(ImageFilter.GaussianBlur(11))
    pm = Image.composite(Image.new("L", (W, ph), 0), pm, nd)
    plate_layer = plate.convert("RGBA")
    plate_layer.putalpha(pm)

    out = gen.convert("RGBA")
    out.alpha_composite(edge_layer, (0, PLATE_Y - F))
    out.alpha_composite(plate_layer, (0, PLATE_Y))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
