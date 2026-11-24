"""Mask-guided Qwen edit + composite only inside the mask."""
import argparse, json, sys
from pathlib import Path
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc

ROOT = Path(__file__).resolve().parents[1]


def workflow(img_name, mask_name, prompt, seed, steps, prefix):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "qwen_image_2.1_int8_convrot.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen3vl_8b_int8_convrot.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "4": {"class_type": "LoadImage", "inputs": {"image": img_name}},
        "5": {"class_type": "LoadImageMask", "inputs": {"image": mask_name, "channel": "red"}},
        "6": {"class_type": "MaskToImage", "inputs": {"mask": ["5", 0]}},
        "7": {"class_type": "TextEncodeQwenImage21", "inputs": {
            "clip": ["2", 0], "prompt": prompt, "negative_prompt": "",
            "vae": ["3", 0], "resolution": 0,
            "images.image_1": ["4", 0], "images.image_2": ["6", 0]}},
        "8": {"class_type": "QwenImage21Cache", "inputs": {
            "model": ["1", 0], "device": "auto", "dtype": "default"}},
        "9": {"class_type": "KSampler", "inputs": {
            "model": ["8", 0], "positive": ["7", 0], "negative": ["7", 1],
            "latent_image": ["7", 2], "seed": seed, "steps": steps, "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "10": {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}},
        "11": {"class_type": "SaveImage", "inputs": {"images": ["10", 0], "filename_prefix": prefix}},
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--mask", default="work/corner_mask.png")
    p.add_argument("--prompt", required=True)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--steps", type=int, default=25)
    p.add_argument("--prefix", default="cornerfix")
    p.add_argument("--out", required=True)
    p.add_argument("--feather", type=float, default=26)
    a = p.parse_args()

    img = cc.upload(ROOT / a.input, name=f"{a.prefix}_img.png")
    msk = cc.upload(ROOT / a.mask, name=f"{a.prefix}_mask.png")
    pid = cc.submit(workflow(img, msk, a.prompt, a.seed, a.steps, a.prefix))
    print("prompt_id", pid, flush=True)
    item = cc.wait(pid)
    imgs = cc.output_images(item)
    if not imgs:
        raise RuntimeError("no image")
    tmp = ROOT / "work" / f"{a.prefix}_raw.png"
    cc.download(imgs[0], tmp)

    base = Image.open(ROOT / a.input).convert("RGBA")
    gen = Image.open(tmp).convert("RGBA")
    if gen.size != base.size:
        gen = gen.resize(base.size, Image.LANCZOS)
    mask = Image.open(ROOT / a.mask).convert("L")
    if mask.size != base.size:
        mask = mask.resize(base.size, Image.LANCZOS)
    mask = mask.filter(ImageFilter.GaussianBlur(a.feather))
    out = Image.composite(gen, base, mask)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
