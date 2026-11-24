"""UV sleeve print: RGBA card with an exactly aligned transparent window,
white-ink mask, and real-card/alpha previews."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np


def parse_rect(s):
    x0, y0, x1, y1 = [int(v) for v in s.split(",")]
    return x0, y0, x1, y1


def checker(size, step=24):
    im = Image.new("RGBA", size)
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            fill = (218, 218, 218, 255) if (x // step + y // step) % 2 == 0 else (255, 255, 255, 255)
            d.rectangle((x, y, x + step - 1, y + step - 1), fill=fill)
    return im


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--card", required=True, help="final card PNG/RGBA")
    p.add_argument("--source", required=True, help="real/source card image")
    p.add_argument("--window", required=True, help="x0,y0,x1,y1 in card pixels")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--card-in", default="2.5,3.5")
    p.add_argument("--inset", type=int, default=2, help="hole inset in print pixels")
    p.add_argument("--mirror", action="store_true", help="for reverse/inside printing")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--name", required=True)
    a = p.parse_args()

    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    cw, ch = [float(v) for v in a.card_in.split(",")]
    W, H = round(cw * a.dpi), round(ch * a.dpi)
    card = Image.open(a.card).convert("RGBA")
    sx, sy = W / card.width, H / card.height
    card = card.resize((W, H), Image.LANCZOS)
    x0, y0, x1, y1 = parse_rect(a.window)
    wh = (round(x0 * sx) + a.inset, round(y0 * sy) + a.inset,
          round(x1 * sx) - a.inset, round(y1 * sy) - a.inset)
    alpha = np.array(card.getchannel("A"))
    alpha[wh[1]:wh[3], wh[0]:wh[2]] = 0

    if a.mirror:
        card = card.transpose(Image.FLIP_LEFT_RIGHT)
        alpha = np.array(Image.fromarray(alpha).transpose(Image.FLIP_LEFT_RIGHT))
        wh = (W - wh[2], wh[1], W - wh[0], wh[3])
    card.putalpha(Image.fromarray(alpha))
    card.save(out / f"{a.name}_print_{a.dpi}dpi.png", optimize=True)
    Image.fromarray(((alpha > 0).astype(np.uint8)) * 255).save(out / f"{a.name}_print_{a.dpi}dpi_white.png")

    real = Image.open(a.source).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
    Image.alpha_composite(real, card).convert("RGB").save(out / f"{a.name}_print_preview_real.jpg", quality=94)
    Image.alpha_composite(checker((W, H)), card).convert("RGB").save(out / f"{a.name}_print_preview_alpha.jpg", quality=94)

    meta = dict(dpi=a.dpi, print_size=[W, H], window_px=[x0, y0, x1, y1],
                hole_px=list(wh), inset=a.inset, mirror=a.mirror,
                alpha_zero_inside=bool((alpha[wh[1]:wh[3], wh[0]:wh[2]] == 0).all()))
    print(meta)


if __name__ == "__main__":
    main()
