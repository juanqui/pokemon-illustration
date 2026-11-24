"""Restore the untouched original art window over a generated outpaint."""
import argparse
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 1440, 2016


def main():
    p = argparse.ArgumentParser()
    p.add_argument("generated")
    p.add_argument("out")
    p.add_argument("--feather", type=float, default=20)
    a = p.parse_args()

    gen = Image.open(a.generated).convert("RGB")
    if gen.size != (W, H):
        gen = gen.resize((W, H), Image.LANCZOS)
    plate = Image.open(ROOT / "work/plate.png").convert("RGB")
    mask = Image.open(ROOT / "work/known_mask.png").convert("L")
    if a.feather:
        mask = mask.filter(ImageFilter.GaussianBlur(a.feather))
    known = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    known.paste(plate, (0, 350))
    known.putalpha(mask)
    out = Image.alpha_composite(gen.convert("RGBA"), known)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
