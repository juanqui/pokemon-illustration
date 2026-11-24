"""Run a list of outpaint jobs sequentially against one ComfyUI server."""
import json, sys, time, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc
from outpaint import workflow
from jobs import JOBS

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dest", required=True)
    p.add_argument("--only", default="", help="comma-separated name filters")
    p.add_argument("--limit", type=int, default=0)
    a = p.parse_args()
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)

    jobs = JOBS
    if a.only:
        keys = [k.strip() for k in a.only.split(",")]
        jobs = [j for j in jobs if any(k in j["name"] for k in keys)]
    if a.limit:
        jobs = jobs[:a.limit]

    canvas = cc.upload(ROOT / "work/canvas_gray.png", name=f"canvas_{cc.BASE.rsplit(':',1)[-1]}.png")
    print(f"[{cc.BASE}] uploaded {canvas}; {len(jobs)} jobs", flush=True)
    for j in jobs:
        out = dest / f"{j['name']}.png"
        if out.exists():
            print("skip", out.name, flush=True)
            continue
        t0 = time.time()
        wf = workflow(canvas, j["prompt"], j["seed"], 25, j["name"])
        pid = cc.submit(wf)
        item = cc.wait(pid)
        imgs = cc.output_images(item)
        if not imgs:
            raise RuntimeError(f"no output for {j['name']}")
        cc.download(imgs[0], out)
        (dest / f"{j['name']}.json").write_text(json.dumps({**j, "prompt_id": pid}, indent=2))
        print(f"done {out.name} in {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
