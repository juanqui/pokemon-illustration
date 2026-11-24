"""Low-denoise Qwen-Image-2.1 harmonization pass.

image_1 = full outpainted art, image_2 = original plate (style reference).
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc

ROOT = Path(__file__).resolve().parents[1]


def workflow(img_name, style_name, prompt, seed, steps, denoise, prefix):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "qwen_image_2.1_int8_convrot.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen3vl_8b_int8_convrot.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "4": {"class_type": "LoadImage", "inputs": {"image": img_name}},
        "5": {"class_type": "LoadImage", "inputs": {"image": style_name}},
        "6": {"class_type": "TextEncodeQwenImage21", "inputs": {
            "clip": ["2", 0], "prompt": prompt, "negative_prompt": "",
            "vae": ["3", 0], "resolution": 0,
            "images.image_1": ["4", 0], "images.image_2": ["5", 0]}},
        "7": {"class_type": "QwenImage21Cache", "inputs": {
            "model": ["1", 0], "device": "auto", "dtype": "default"}},
        "8": {"class_type": "VAEEncode", "inputs": {"pixels": ["4", 0], "vae": ["3", 0]}},
        "9": {"class_type": "KSampler", "inputs": {
            "model": ["7", 0], "positive": ["6", 0], "negative": ["6", 1],
            "latent_image": ["8", 0], "seed": seed, "steps": steps, "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple", "denoise": denoise}},
        "10": {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}},
        "11": {"class_type": "SaveImage", "inputs": {"images": ["10", 0], "filename_prefix": prefix}},
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--style", default="work/plate.png")
    p.add_argument("--prompt", required=True)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--steps", type=int, default=25)
    p.add_argument("--denoise", type=float, default=0.28)
    p.add_argument("--prefix", default="refine")
    p.add_argument("--out", required=True)
    a = p.parse_args()

    img = cc.upload(ROOT / a.input, name=f"{a.prefix}_img.png")
    sty = cc.upload(ROOT / a.style, name=f"{a.prefix}_style.png")
    wf = workflow(img, sty, a.prompt, a.seed, a.steps, a.denoise, a.prefix)
    pid = cc.submit(wf)
    print("prompt_id", pid, flush=True)
    (ROOT / "work/last_refine.json").write_text(json.dumps(wf, indent=2))
    item = cc.wait(pid)
    imgs = cc.output_images(item)
    if not imgs:
        raise RuntimeError("no images")
    cc.download(imgs[0], Path(a.out))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
