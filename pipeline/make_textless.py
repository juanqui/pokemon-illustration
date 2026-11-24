"""Textless final card + clear-window UV print + 3-panel comparison.

The card is illustration-only: no name, HP, attacks, footer or copyright. The
source window is pasted hard-edged at its exact source rect, then the print
layer is generated with alpha 0 in that window so a real card shows through.
The comparison always has three panels: source | textless final | print alpha.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BG_DEFAULT = "F5F4EF"
INK = (50, 44, 37)


def parse_rect(s):
    x0, y0, x1, y1 = [int(v) for v in s.split(",")]
    return x0, y0, x1, y1


def parse_color(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def rounded_mask(size, radius):
    # 4x supersampled so the card silhouette is anti-aliased.
    w, h = size
    m = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle(
        (0, 0, w * 4 - 1, h * 4 - 1), radius * 4, fill=255
    )
    return m.resize(size, Image.LANCZOS)


def load_font(path, size):
    candidates = [path] if path else []
    candidates += [
        "assets/fonts/Lato-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def panel(img, size, bg):
    if img.size != size:
        img = img.resize(size, Image.LANCZOS)
    if img.mode != "RGBA":
        return img.convert("RGB")
    out = Image.new("RGB", size, bg)
    out.paste(img, (0, 0), img)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--art", required=True,
                   help="textless full-bleed art plate at card size")
    p.add_argument("--source", required=True, help="real/source card image")
    p.add_argument("--window", required=True,
                   help="x0,y0,x1,y1 in card pixels")
    p.add_argument("--out-card", required=True,
                   help="output textless RGBA card PNG")
    p.add_argument("--print-dir", required=True)
    p.add_argument("--name", required=True, help="print output basename")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--card-in", default="2.5,3.5")
    p.add_argument("--inset", type=int, default=2,
                   help="hole inset in print pixels")
    p.add_argument("--mirror", action="store_true")
    p.add_argument("--radius", type=int, default=26,
                   help="card corner radius in card pixels")
    p.add_argument("--sticker-mask",
                   help="optional L mask for the source sticker/decal")
    p.add_argument("--compare", required=True,
                   help="output 3-panel JPEG: source | textless final | print")
    p.add_argument("--font", help="TTF for comparison labels")
    p.add_argument("--background", default=BG_DEFAULT)
    a = p.parse_args()

    source = Image.open(a.source).convert("RGB")
    card = Image.open(a.art).convert("RGBA")
    if card.size != source.size:
        card = card.resize(source.size, Image.LANCZOS)
    x0, y0, x1, y1 = parse_rect(a.window)

    # Exact source window, hard-edged at source coordinates.
    win = source.crop((x0, y0, x1, y1))
    wm = Image.new("L", card.size, 0)
    wm.paste(Image.new("L", win.size, 255), (x0, y0))
    wlayer = Image.new("RGBA", card.size, (0, 0, 0, 0))
    wlayer.paste(win, (x0, y0))
    wlayer.putalpha(wm)
    card.alpha_composite(wlayer)

    # Exact sticker/decal, when its mask is available.
    if a.sticker_mask:
        mask = Image.open(a.sticker_mask).convert("L")
        if mask.size != card.size:
            raise SystemExit("sticker mask must match card size")
        sticker = source.convert("RGBA")
        sticker.putalpha(mask)
        card.alpha_composite(sticker)

    # Transparent rounded card silhouette; no text/chrome is drawn.
    card.putalpha(rounded_mask(card.size, a.radius))
    out_card = Path(a.out_card)
    out_card.parent.mkdir(parents=True, exist_ok=True)
    card.save(out_card, optimize=True)

    # Clear-window print layer and previews.
    print_script = Path(__file__).resolve().with_name("make_print.py")
    cmd = [
        sys.executable, str(print_script),
        "--card", str(out_card),
        "--source", a.source,
        "--window", a.window,
        "--dpi", str(a.dpi),
        "--card-in", a.card_in,
        "--inset", str(a.inset),
        "--out-dir", a.print_dir,
        "--name", a.name,
    ]
    if a.mirror:
        cmd.append("--mirror")
    subprocess.run(cmd, check=True)

    # Verify: exact window in the card, alpha 0 throughout the print hole.
    card_arr = np.array(card)
    src_arr = np.array(source)
    diff = np.abs(card_arr[y0:y1, x0:x1, :3].astype(np.int16)
                  - src_arr[y0:y1, x0:x1].astype(np.int16))
    print_path = Path(a.print_dir) / f"{a.name}_print_{a.dpi}dpi.png"
    pr = Image.open(print_path).convert("RGBA")
    pw, ph = pr.size
    sx, sy = pw / source.width, ph / source.height
    hole = (
        round(x0 * sx) + a.inset, round(y0 * sy) + a.inset,
        round(x1 * sx) - a.inset, round(y1 * sy) - a.inset,
    )
    if a.mirror:
        hole = (pw - hole[2], hole[1], pw - hole[0], hole[3])
    alpha = np.array(pr.getchannel("A"))
    hole_zero = bool((alpha[hole[1]:hole[3], hole[0]:hole[2]] == 0).all())

    metrics = {
        "window": [x0, y0, x1, y1],
        "pixels": int((x1 - x0) * (y1 - y0)),
        "mae": round(float(diff.mean()), 6),
        "max": int(diff.max()),
        "print_size": [pw, ph],
        "hole_px": list(hole),
        "alpha_zero_inside": hole_zero,
        "mirror": a.mirror,
    }
    print(json.dumps(metrics, indent=2))
    if diff.max() != 0 or not hole_zero:
        raise SystemExit("verification failed: window not exact or hole not clear")

    # 3-panel comparison: source | textless final | print alpha preview.
    bg = parse_color(a.background)
    size = source.size
    alpha_preview = Path(a.print_dir) / f"{a.name}_print_preview_alpha.jpg"
    panels = [
        panel(source, size, bg),
        panel(card, size, bg),
        panel(Image.open(alpha_preview), size, bg),
    ]
    w, h = size
    margin, gap, header, bottom = 20, 40, 58, 22
    canvas = Image.new("RGB", (margin * 2 + w * 3 + gap * 2, header + h + bottom), bg)
    xs = [margin + i * (w + gap) for i in range(3)]
    for x, p in zip(xs, panels):
        canvas.paste(p, (x, header))
    d = ImageDraw.Draw(canvas)
    d_font = load_font(a.font, 20)
    labels = [
        f"source · {w}×{h} · window {x1 - x0}×{y1 - y0} @ ({x0},{y0})",
        "final card · all words removed · window exact",
        "UV print layer · clear window (checkerboard) · no text",
    ]
    for x, label in zip(xs, labels):
        d.text((x, 16), label, font=d_font, fill=INK)
    out_compare = Path(a.compare)
    out_compare.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_compare, quality=95, subsampling=0, optimize=True)
    print("wrote", out_card)
    print("wrote", out_compare)


if __name__ == "__main__":
    main()
