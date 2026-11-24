"""Compose a full-bleed, SIR-style Vulpix card from a finished art plate.

Everything is drawn at 1440x2016 (2x the source card) with Lato, a close
humanist match for the TCG's proprietary face, and vector-ish energy symbols.
"""
import argparse, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W, H = 1440, 2016
M = 84
FONTS = ROOT / "assets/fonts"
INK = (42, 20, 8)
CREAM = (255, 249, 236)


def font(style, size):
    return ImageFont.truetype(str(FONTS / f"Lato-{style}.ttf"), size)


def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def vgrad(size, stops):
    """Vertical RGBA gradient. stops = [(y_fraction, (r,g,b,a)), ...]."""
    w, h = size
    col = Image.new("RGBA", (1, h))
    px = col.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            y0, c0 = stops[i]
            y1, c1 = stops[i + 1]
            if y0 <= t <= y1:
                f = (t - y0) / max(1e-6, y1 - y0)
                px[0, y] = tuple(round(c0[j] + (c1[j] - c0[j]) * f) for j in range(4))
                break
        else:
            px[0, y] = stops[-1][1]
    return col.resize(size)


def drop_text(base, xy, text, fnt, fill, stroke=0, stroke_fill=INK, shadow=(0, 7),
              shadow_alpha=150, shadow_blur=9, anchor="la"):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if shadow is not None:
        d.text((xy[0] + shadow[0], xy[1] + shadow[1]), text, font=fnt, fill=(0, 0, 0, shadow_alpha),
               stroke_width=stroke, stroke_fill=(0, 0, 0, shadow_alpha), anchor=anchor)
        layer = layer.filter(ImageFilter.GaussianBlur(shadow_blur))
    d = ImageDraw.Draw(layer)
    d.text(xy, text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, anchor=anchor)
    base.alpha_composite(layer)


def spaced_text(d, xy, text, fnt, fill, spacing, stroke=0, stroke_fill=INK):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, anchor="la")
        x += d.textlength(ch, font=fnt) + spacing


def flame(size):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad = S * 0.04
    d.ellipse((pad, pad, S - pad, S - pad), fill=(232, 78, 43, 255))
    d.ellipse((pad * 2.2, pad * 2.2, S - pad * 2.2, S - pad * 2.2), fill=(203, 52, 27, 255))
    # stylised flame
    f = [(0.50, 0.16), (0.60, 0.33), (0.58, 0.43), (0.69, 0.36), (0.74, 0.50),
         (0.73, 0.62), (0.64, 0.74), (0.50, 0.82), (0.36, 0.74), (0.27, 0.62),
         (0.26, 0.50), (0.33, 0.40), (0.41, 0.49), (0.38, 0.34)]
    d.polygon([(x * S, y * S) for x, y in f], fill=(255, 212, 92, 255))
    g = [(0.50, 0.40), (0.59, 0.54), (0.57, 0.65), (0.50, 0.72), (0.43, 0.65), (0.41, 0.54)]
    d.polygon([(x * S, y * S) for x, y in g], fill=(255, 248, 214, 255))
    return im.resize((size, size), Image.LANCZOS)


def droplet(size):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((S * .02, S * .02, S * .98, S * .98), fill=(58, 137, 208, 255))
    d.ellipse((S * .10, S * .10, S * .90, S * .90), fill=(34, 107, 177, 255))
    cx, cy, r = S * .5, S * .58, S * .23
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(240, 250, 255, 255))
    d.polygon([(cx, S * .20), (cx + r * .92, cy - r * .45), (cx - r * .92, cy - r * .45)],
              fill=(240, 250, 255, 255))
    d.ellipse((cx - r * .35, cy - r * .45, cx, cy + r * .1), fill=(150, 205, 245, 255))
    return im.resize((size, size), Image.LANCZOS)


def star(size):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((S * .02, S * .02, S * .98, S * .98), fill=(214, 214, 214, 255))
    d.ellipse((S * .10, S * .10, S * .90, S * .90), fill=(247, 247, 247, 255))
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = S * (0.30 if i % 2 == 0 else 0.125)
        pts.append((S / 2 + rr * math.cos(a), S / 2 + rr * math.sin(a)))
    d.polygon(pts, fill=(246, 184, 52, 255), outline=(150, 96, 18, 255))
    return im.resize((size, size), Image.LANCZOS)


def rarity_star(size):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = S * (0.47 if i % 2 == 0 else 0.20)
        pts.append((S / 2 + rr * math.cos(ang), S / 2 + rr * math.sin(ang)))
    d.polygon(pts, fill=(244, 196, 92, 255), outline=(92, 58, 15, 255))
    return im.resize((size, size), Image.LANCZOS)


def compose(art_path, out_path, seed_note="", holo=False):
    art = Image.open(art_path).convert("RGB").resize((W, H), Image.LANCZOS)
    art = ImageEnhance.Contrast(art).enhance(1.055)
    art = ImageEnhance.Color(art).enhance(1.035)
    card = art.convert("RGBA")

    # gentle radial vignette; keeps focus on the subject and unifies the plate
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.46) / (H * 0.62)) ** 2)
    va = (np.clip((rr - 0.72) / 0.55, 0, 1) ** 1.4 * 46).astype(np.uint8)
    vig = Image.new("RGBA", (W, H), (24, 16, 10, 0))
    vig.putalpha(Image.fromarray(va))
    card.alpha_composite(vig)

    # Cinematic grade: lift the canopy light, deepen the bottom for type.
    card.alpha_composite(vgrad((W, H), [
        (0.00, (28, 22, 12, 92)),
        (0.10, (28, 22, 12, 40)),
        (0.22, (28, 22, 12, 0)),
        (0.60, (28, 18, 10, 0)),
        (0.78, (30, 17, 9, 30)),
        (0.88, (28, 15, 9, 130)),
        (1.00, (22, 11, 7, 238)),
    ]))
    if holo:
        sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(sheen)
        d.polygon([(-200, H * .25), (W * .55, -100), (W * .78, -100), (W * .2, H * .55)],
                  fill=(255, 255, 255, 16))
        d.polygon([(W * .35, H), (W * .8, H * .2), (W * .92, H * .2), (W * .55, H)],
                  fill=(180, 230, 255, 10))
        card.alpha_composite(sheen)

    draw = ImageDraw.Draw(card)

    # ---- header -------------------------------------------------------
    f_basic = font("Bold", 27)
    spaced_text(draw, (M + 4, 48), "BASIC", f_basic, (255, 255, 255, 225), 7, 2, (53, 27, 12, 160))
    drop_text(card, (M - 4, 64), "Vulpix", font("Heavy", 112), (255, 255, 255, 255),
              stroke=7, shadow=(0, 9), shadow_alpha=165, shadow_blur=12)

    f_hp = font("Bold", 34)
    f_num = font("Heavy", 82)
    drop_text(card, (1268, 182), "70", f_num, (255, 255, 255, 255), stroke=6, shadow=(0, 7),
              shadow_alpha=150, shadow_blur=10, anchor="rs")
    drop_text(card, (1156, 176), "HP", f_hp, (255, 255, 255, 245), stroke=4, shadow=(0, 5),
              shadow_alpha=150, shadow_blur=8, anchor="rs")
    icon = flame(104)
    card.alpha_composite(icon, (1288, 88))
    draw.ellipse((1288, 88, 1288 + 104, 88 + 104), outline=(255, 255, 255, 210), width=4)

    # ---- attack -------------------------------------------------------
    cost = flame(68)
    card.alpha_composite(cost, (M, 1472))
    drop_text(card, (M + 92, 1460), "Wild Kick", font("Heavy", 70), CREAM,
              stroke=4, shadow=(0, 6), shadow_alpha=170, shadow_blur=10)
    drop_text(card, (W - M, 1460), "30", font("Heavy", 74), CREAM,
              stroke=4, shadow=(0, 6), shadow_alpha=170, shadow_blur=10, anchor="ra")
    drop_text(card, (M + 92, 1556),
              "Flip a coin. If tails, this attack does nothing.",
              font("Semibold", 39), (255, 252, 243, 245),
              stroke=3, shadow=(0, 4), shadow_alpha=150, shadow_blur=7)

    # ---- footer rules -------------------------------------------------
    draw.line((M, 1730, W - M, 1730), fill=(255, 255, 255, 60), width=2)

    f_lab = font("Bold", 25)
    f_val = font("Heavy", 38)
    drop_text(card, (M, 1788), "weakness", f_lab, (255, 250, 238, 220), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    wicon = droplet(52)
    card.alpha_composite(wicon, (M + 150, 1770))
    drop_text(card, (M + 218, 1778), "×2", f_val, CREAM, stroke=2, shadow=(0, 3),
              shadow_alpha=140, shadow_blur=5)
    draw.line((M + 330, 1770, M + 330, 1840), fill=(255, 255, 255, 45), width=2)
    drop_text(card, (M + 370, 1788), "resistance", f_lab, (255, 250, 238, 220), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    drop_text(card, (M + 610, 1782), "—", f_val, (255, 250, 238, 200), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    draw.line((M + 720, 1770, M + 720, 1840), fill=(255, 255, 255, 45), width=2)
    drop_text(card, (M + 770, 1788), "retreat", f_lab, (255, 250, 238, 220), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    sicon = star(54)
    card.alpha_composite(sicon, (M + 950, 1769))

    draw.line((M, 1862, W - M, 1862), fill=(255, 255, 255, 40), width=2)

    # ---- artist / set / flavour --------------------------------------
    f_art = font("Italic", 29) if (FONTS / "Lato-Italic.ttf").exists() else font("Medium", 29)
    drop_text(card, (M, 1890), "Illus. miki kudo", f_art, (255, 251, 240, 235), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    box = (M, 1952, M + 42, 1994)
    draw.rounded_rectangle(box, 6, fill=(20, 16, 12, 235), outline=(255, 255, 255, 160), width=2)
    draw.text((M + 21, 1972), "J", font=font("Heavy", 30), fill=(255, 255, 255, 255), anchor="mm")
    f_set = font("Bold", 29)
    drop_text(card, (M + 58, 1955), "30EN", f_set, (255, 251, 240, 235), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    drop_text(card, (M + 172, 1955), "009/128", f_set, (255, 251, 240, 235), stroke=2,
              shadow=(0, 3), shadow_alpha=130, shadow_blur=5)
    draw.ellipse((M + 316, 1966, M + 338, 1988), fill=(18, 14, 10, 255), outline=(255, 255, 255, 120), width=2)
    for k in range(2):
        st = rarity_star(30)
        card.alpha_composite(st, (M + 352 + k * 34, 1960))

    f_flav = font("Medium", 31)
    flavor = ("As its body grows larger, its six warm tails become "
              "more beautiful, with a more luxurious coat of fur.")
    words, lines, line = flavor.split(), [], ""
    maxw = 800
    for w in words:
        test = (line + " " + w).strip()
        if draw.textlength(test, font=f_flav) <= maxw:
            line = test
        else:
            lines.append(line); line = w
    lines.append(line)
    for i, ln in enumerate(lines[:2]):
        drop_text(card, (520, 1868 + i * 40), ln, f_flav, (255, 251, 240, 240),
                  stroke=2, shadow=(0, 3), shadow_alpha=140, shadow_blur=5)
    drop_text(card, (W // 2, 1988), "©2026 Pokémon / Nintendo / Creatures / GAME FREAK",
              font("Medium", 17), (255, 255, 255, 128), shadow=None, anchor="ma")

    return finish(card, out_path, seed_note)


def finish(card, out_path, seed_note=""):
    # outer silver frame
    border = 9
    silver = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(silver)
    d.rounded_rectangle((0, 0, W - 1, H - 1), 52, outline=(238, 240, 243, 255), width=border)
    d.rounded_rectangle((border, border, W - 1 - border, H - 1 - border), 46,
                        outline=(150, 154, 160, 255), width=2)
    d.rounded_rectangle((border + 2, border + 2, W - 3 - border, H - 3 - border), 44,
                        outline=(255, 255, 255, 120), width=1)
    card.alpha_composite(silver)
    # clip to card silhouette
    card.putalpha(rounded_mask((W, H), 52))
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    card.convert("RGB").save(out_path, quality=95)
    small = card.convert("RGB").resize((732, 1024), Image.LANCZOS)
    small.save(out_path.with_name(out_path.stem + "_732.png"))
    return out_path


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("art")
    p.add_argument("out")
    p.add_argument("--holo", action="store_true")
    a = p.parse_args()
    compose(a.art, a.out, holo=a.holo)
