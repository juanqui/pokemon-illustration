"""Assert the window is pixel-exact and the print hole is transparent."""
import argparse, json
from pathlib import Path
from PIL import Image
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--card", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--window", required=True)
    p.add_argument("--print", dest="print_file", default=None)
    p.add_argument("--out", default=None)
    a = p.parse_args()
    x0, y0, x1, y1 = [int(v) for v in a.window.split(",")]
    src = np.asarray(Image.open(a.source).convert("RGB"))
    card = np.asarray(Image.open(a.card).convert("RGB"))
    d = np.abs(card[y0:y1, x0:x1].astype(int) - src[y0:y1, x0:x1].astype(int))
    res = dict(window=[x0, y0, x1, y1], pixels=int((x1 - x0) * (y1 - y0)),
               mae=float(d.mean()), max=int(d.max()))
    if a.print_file:
        pr = Image.open(a.print_file).convert("RGBA")
        al = np.array(pr.getchannel("A"))
        res["print_alpha_zero_center"] = bool(al[int(pr.height * .35):int(pr.height * .45),
                                                 int(pr.width * .4):int(pr.width * .6)].max() == 0)
        res["print_size"] = list(pr.size)
    print(json.dumps(res, indent=2))
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
