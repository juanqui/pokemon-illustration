import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc
from outpaint import workflow
from jobs3 import JOBS
ROOT = Path(__file__).resolve().parents[1]
dest = Path(sys.argv[1]); which = sys.argv[2]
dest.mkdir(parents=True, exist_ok=True)
canvas = cc.upload(ROOT / "work/canvas_gray.png", name=f"canvas_{cc.BASE.rsplit(':',1)[-1]}.png")
jobs = [j for j in JOBS if which in j["name"]]
print(f"{cc.BASE}: {len(jobs)} jobs", flush=True)
for j in jobs:
    out = dest / f"{j['name']}.png"
    if out.exists(): continue
    t0 = time.time()
    pid = cc.submit(workflow(canvas, j["prompt"], j["seed"], 25, j["name"]))
    item = cc.wait(pid); imgs = cc.output_images(item)
    cc.download(imgs[0], out)
    (dest / f"{j['name']}.json").write_text(json.dumps({**j, "prompt_id": pid}, indent=2))
    print("done", out.name, f"{time.time()-t0:.0f}s", flush=True)
