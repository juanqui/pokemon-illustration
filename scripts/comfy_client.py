"""Minimal ComfyUI HTTP client: upload, queue a workflow, fetch outputs."""
import json, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

import os
BASE = os.environ.get("COMFY_URL", "http://127.0.0.1:8188")


def _req(path, data=None, headers=None, method=None):
    url = BASE + path
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def up() -> bool:
    try:
        _req("/system_stats")
        return True
    except Exception:
        return False


def upload(path: Path, name: str | None = None) -> str:
    path = Path(path)
    name = name or path.name
    boundary = "----vulpixform"
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + path.read_bytes() + (
        f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n"
        f"--{boundary}--\r\n"
    ).encode()
    out = json.loads(_req("/upload/image", body,
                          {"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    return out["name"]


def submit(workflow: dict) -> str:
    payload = json.dumps({"prompt": workflow, "client_id": "vulpix"}).encode()
    out = json.loads(_req("/prompt", payload, {"Content-Type": "application/json"}))
    if "prompt_id" not in out:
        raise RuntimeError(f"queue failed: {out}")
    return out["prompt_id"]


def wait(prompt_id: str, timeout: float = 1800) -> dict:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            h = json.loads(_req(f"/history/{prompt_id}"))
        except urllib.error.HTTPError:
            h = {}
        if prompt_id in h:
            item = h[prompt_id]
            status = item.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(json.dumps(status)[:4000])
            if status.get("completed") or item.get("outputs"):
                return item
        time.sleep(2)
    raise TimeoutError(prompt_id)


def output_images(item: dict) -> list[dict]:
    imgs = []
    for node in item.get("outputs", {}).values():
        imgs += node.get("images", [])
    return imgs


def download(image: dict, dest: Path) -> Path:
    q = urllib.parse.urlencode({"filename": image["filename"],
                                "subfolder": image.get("subfolder", ""),
                                "type": image.get("type", "output")})
    data = _req("/view?" + q)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest
