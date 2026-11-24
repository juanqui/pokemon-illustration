"""Card chrome around the EXACT source window at its source geometry.

Window (incl. silver frame): x=60..690, y=95..491 (630x396). The 30th sticker
is preserved as a decal. Only the area outside that union is generated.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
import numpy as np
from compose_card import flame, droplet, star, rarity_star, drop_text, vgrad, rounded_mask

ROOT = Path(__file__).resolve().parents[1]
W, H = 732, 1024
WIN = (66, 101, 683, 484)
FONTS = ROOT / "assets/fonts"
INK = (38, 22, 12)
CREAM = (255, 250, 238)


def font(style, size):
    return ImageFont.truetype(str(FONTS / f"Lato-{style}.ttf"), size)


def spaced(d, xy, text, fnt, fill, spacing, stroke=0, stroke_fill=INK):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += d.textlength(ch, font=fnt) + spacing


def main():
    p = argparse.ArgumentParser()
    p.add_argument("generated")
    p.add_argument("out")
    p.add_argument("--no-grade", action="store_true")
    a = p.parse_args()

    src = Image.open(ROOT / "assets/source-card.png").convert("RGB")
    window = src.crop(WIN)
    sticker = np.array(Image.open(ROOT / "work/sticker_mask_final.png").convert("L")) > 127
    protect = Image.open(ROOT / "work/content_known_mask.png").convert("L").crop((0, 0, W, H))

    gen = Image.open(a.generated).convert("RGB")
    if gen.size != (736, 1024):
        gen = gen.resize((736, 1024), Image.LANCZOS)
    art = gen.crop((0, 0, W, H)).convert("RGBA")

    # grade/vignette only outside the protected window+sticker
    if a.no_grade:
        card = art
    else:
        graded = ImageEnhance.Contrast(art.convert("RGB")).enhance(1.05)
        graded = ImageEnhance.Color(graded).enhance(1.04).convert("RGBA")
        yy, xx = np.mgrid[0:H, 0:W]
        rr = np.sqrt(((xx - W / 2) / (W * .65)) ** 2 + ((yy - H * .5) / (H * .65)) ** 2)
        va = (np.clip((rr - .72) / .55, 0, 1) ** 1.4 * 40).astype(np.uint8)
        vig = Image.new("RGBA", (W, H), (24, 16, 10, 0)); vig.putalpha(Image.fromarray(va))
        graded.alpha_composite(vig)
        card = Image.composite(art, graded, protect)

    # exact illustration content; 3 px anti-aliased outer edge only
    wm = Image.new("L", (W, H), 0)
    wm.paste(Image.new("L", window.size, 255), (WIN[0], WIN[1]))
    # hard edge: the full window must be pixel-exact
    # wm is used as-is
    wlayer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wlayer.paste(window, (WIN[0], WIN[1])); wlayer.putalpha(wm)
    card.alpha_composite(wlayer)
    st = src.convert("RGBA"); st.putalpha(Image.fromarray((sticker * 255).astype(np.uint8)))
    card.alpha_composite(st)
    d = ImageDraw.Draw(card)

    # readability gradients: stop above/below the exact window
    card.alpha_composite(vgrad((W, H), [
        (0.000, (26, 20, 12, 100)), (0.055, (26, 20, 12, 34)),
        (0.092, (26, 20, 12, 0)), (0.490, (26, 18, 10, 0)),
        (0.620, (28, 17, 9, 34)), (0.850, (24, 13, 8, 138)),
        (1.000, (20, 10, 6, 232)),
    ]))

    # header, above the window
    f_basic = font("Bold", 10)
    d.rounded_rectangle((34, 8, 118, 24), 8, fill=(214, 214, 214, 235), outline=(255, 255, 255, 220), width=1)
    spaced(d, (44, 10), "BASIC", f_basic, (46, 36, 28, 255), 1.6, 1, (255, 255, 255, 180))
    drop_text(card, (34, 24), "Vulpix", font("Heavy", 46), (24, 16, 10, 255),
              stroke=4, stroke_fill=(255, 255, 255, 235), shadow=(0, 3), shadow_alpha=120, shadow_blur=4)
    drop_text(card, (566, 50), "70", font("Heavy", 38), (22, 14, 8, 255),
              stroke=3, stroke_fill=(255, 255, 255, 235), shadow=(0, 2), shadow_alpha=110, shadow_blur=3, anchor="rs")
    drop_text(card, (532, 52), "HP", font("Bold", 17), (30, 20, 12, 255),
              stroke=2, stroke_fill=(255, 255, 255, 235), shadow=(0, 1), shadow_alpha=100, shadow_blur=2, anchor="rs")
    fire = flame(36)
    card.alpha_composite(fire, (650, 24))
    d.ellipse((650, 24, 686, 60), outline=(255, 255, 255, 210), width=2)

    # attack, below the window
    cost = flame(30)
    card.alpha_composite(cost, (44, 638))
    drop_text(card, (88, 630), "Wild Kick", font("Heavy", 34), CREAM,
              stroke=3, shadow=(0, 3), shadow_alpha=170, shadow_blur=4)
    drop_text(card, (666, 630), "30", font("Heavy", 36), CREAM,
              stroke=3, shadow=(0, 3), shadow_alpha=170, shadow_blur=4, anchor="ra")
    drop_text(card, (90, 674), "Flip a coin. If tails, this attack does nothing.",
              font("Semibold", 19), (255, 253, 246, 245), stroke=2,
              shadow=(0, 2), shadow_alpha=150, shadow_blur=4)

    # footer rules
    d.line((40, 848, W - 40, 848), fill=(255, 255, 255, 70), width=1)
    f_lab = font("Bold", 12); f_val = font("Heavy", 17)
    drop_text(card, (40, 862), "weakness", f_lab, (255, 250, 238, 230), stroke=1,
              shadow=(0, 1), shadow_alpha=120, shadow_blur=2)
    wi = droplet(22); card.alpha_composite(wi, (122, 858))
    drop_text(card, (148, 860), "×2", f_val, CREAM, stroke=1, shadow=(0, 1), shadow_alpha=120, shadow_blur=2)
    d.line((206, 856, 206, 888), fill=(255, 255, 255, 45), width=1)
    drop_text(card, (226, 862), "resistance", f_lab, (255, 250, 238, 230), stroke=1,
              shadow=(0, 1), shadow_alpha=120, shadow_blur=2)
    drop_text(card, (330, 860), "—", f_val, (255, 250, 238, 210), stroke=1,
              shadow=(0, 1), shadow_alpha=120, shadow_blur=2)
    d.line((360, 856, 360, 888), fill=(255, 255, 255, 45), width=1)
    drop_text(card, (382, 862), "retreat", f_lab, (255, 250, 238, 230), stroke=1,
              shadow=(0, 1), shadow_alpha=120, shadow_blur=2)
    rs = star(24); card.alpha_composite(rs, (470, 856))

    d.line((40, 896, W - 40, 896), fill=(255, 255, 255, 50), width=1)
    drop_text(card, (40, 906), "Illus. miki kudo", font("Italic", 13), (255, 251, 242, 238),
              stroke=1, shadow=(0, 1), shadow_alpha=110, shadow_blur=2)
    # set info
    d.rounded_rectangle((40, 932, 58, 950), 2, fill=(18, 14, 10, 235), outline=(255, 255, 255, 150), width=1)
    d.text((49, 941), "J", font=font("Heavy", 13), fill=(255, 255, 255), anchor="mm")
    drop_text(card, (64, 932), "30EN", font("Bold", 13), (255, 251, 242, 238), stroke=1,
              shadow=(0, 1), shadow_alpha=110, shadow_blur=2)
    drop_text(card, (112, 932), "009/128", font("Bold", 13), (255, 251, 242, 238), stroke=1,
              shadow=(0, 1), shadow_alpha=110, shadow_blur=2)
    d.ellipse((196, 939, 206, 949), fill=(18, 14, 10, 255), outline=(255, 255, 255, 130), width=1)
    for k in range(2):
        rstar = rarity_star(14); card.alpha_composite(rstar, (214 + k * 16, 934))

    flavor = "As its body grows larger, its six warm tails become more beautiful, with a more luxurious coat of fur."
    f_fl = font("Medium", 13)
    words, lines, line = flavor.split(), [], ""
    for w in words:
        t = (line + " " + w).strip()
        if d.textlength(t, font=f_fl) <= 240:
            line = t
        else:
            lines.append(line); line = w
    lines.append(line)
    for i, ln in enumerate(lines[:4]):
        drop_text(card, (460, 900 + i * 16), ln, f_fl, (255, 251, 242, 240), stroke=1,
                  shadow=(0, 1), shadow_alpha=120, shadow_blur=2)
    drop_text(card, (W // 2, 994), "©2026 Pokémon / Nintendo / Creatures / GAME FREAK",
              font("Medium", 8), (255, 255, 255, 120), shadow=None, anchor="ma")

    # silver card frame
    silver = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(silver)
    sd.rounded_rectangle((1, 1, W - 2, H - 2), 26, outline=(86, 86, 88, 160), width=1)
    sd.rounded_rectangle((0, 0, W - 1, H - 1), 26, outline=(238, 240, 243, 255), width=5)
    sd.rounded_rectangle((5, 5, W - 6, H - 6), 22, outline=(150, 154, 160, 255), width=1)
    card.alpha_composite(silver)
    card.alpha_composite(st)  # sticker sits over the card frame, as in the source
    card.putalpha(rounded_mask((W, H), 26))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    card.save(a.out, optimize=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
