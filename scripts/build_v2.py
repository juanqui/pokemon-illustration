"""Final v2: outpainted scene + exact source fox, protected from grading."""
import subprocess, json
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
JOBS = {
    "vulpix_blossom_stream": "out/raw/k_blossom_stream_303.png",
    "vulpix_spring_stream": "out/raw/h_stream_303.png",
    "vulpix_cherry_blossom": "out/raw2/c_blossom_303.png",
    "vulpix_spring_grove": "out/raw/vulpix_a3_101.png",
    "vulpix_bluebell": "out/raw2/i_bluebell_303.png",
}
mask = np.array(Image.open(ROOT / "work/fox_mask_final.png").convert("L")) > 127
er5 = ndimage.binary_erosion(mask, iterations=5)
er2 = ndimage.binary_erosion(mask, iterations=2)
plate = np.asarray(Image.open(ROOT / "work/plate.png").convert("RGB")).astype(int)
metrics = {}
for name, raw in JOBS.items():
    comp = ROOT / f"work/fox_{name}.png"
    subprocess.run([str(ROOT / "comfy-venv/bin/python"), str(ROOT / "scripts/fox_mask.py"), raw, str(comp)],
                   check=True, stdout=subprocess.DEVNULL)
    card = ROOT / f"final/cards/{name}.png"
    subprocess.run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/compose_card.py"),
                    str(comp), str(card), "--protect", str(ROOT / "work/fox_protect.png")],
                   check=True, stdout=subprocess.DEVNULL)
    prev = ROOT / f"final/previews/{name}.png"
    Image.open(card).resize((732, 1024), Image.LANCZOS).save(prev)
    a = np.asarray(Image.open(card).convert("RGB"))[350:1239].astype(int)
    d = np.abs(a - plate)
    metrics[name] = dict(interior_pixels=int(er5.sum()), interior_mae=float(d[er5].mean()),
                         interior_max=int(d[er5].max()), edge2_mae=float(d[er2].mean()),
                         edge2_max=int(d[er2].max()))
    print(name, metrics[name], flush=True)
Path("final/verification").mkdir(parents=True, exist_ok=True)
Path("final/verification/metrics.json").write_text(json.dumps(metrics, indent=2))
