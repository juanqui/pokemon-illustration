"""Build a labelled contact sheet from art candidates."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets/fonts"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("dirs", nargs="+")
    p.add_argument("--out", required=True)
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--thumb", type=int, default=440)
    a = p.parse_args()

    files = []
    for d in a.dirs:
        files += sorted(Path(d).glob("*.png"))
    files = [f for f in files if not f.name.endswith("_732.png")]
    if not files:
        raise SystemExit("no images")
    tw = a.thumb
    th = round(tw * 2016 / 1440)
    lab = 38
    rows = (len(files) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * (tw + 16) + 16, rows * (th + lab + 16) + 16), (18, 18, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(str(FONTS / "Lato-Bold.ttf"), 22)
    for i, path in enumerate(files):
        r, c = divmod(i, a.cols)
        x = 16 + c * (tw + 16)
        y = 16 + r * (th + lab + 16)
        im = Image.open(path).convert("RGB").resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + th + 8), path.stem, font=f, fill=(235, 235, 238))
    sheet.save(a.out, quality=92)
    print(a.out, sheet.size)


if __name__ == "__main__":
    main()
