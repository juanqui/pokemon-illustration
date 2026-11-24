"""Outpaint one gray-padded canvas with Qwen-Image-2.1 + outpaint LoRA."""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc

ROOT = Path(__file__).resolve().parents[1]


def workflow(image_name, prompt, seed, steps, prefix, render_size=None, lora="outpaint-v2.safetensors"):
    wf = {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "qwen_image_2.1_int8_convrot.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen3vl_8b_int8_convrot.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "4": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "model": ["1", 0], "lora_name": lora, "strength_model": 1.0}},
        "5": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "6": {"class_type": "TextEncodeQwenImage21", "inputs": {
            "clip": ["2", 0], "prompt": prompt, "negative_prompt": "",
            "vae": ["3", 0], "resolution": 0, "images.image_1": ["5", 0]}},
        "7": {"class_type": "QwenImage21Cache", "inputs": {
            "model": ["4", 0], "device": "auto", "dtype": "default"}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["7", 0], "positive": ["6", 0], "negative": ["6", 1],
            "latent_image": ["6", 2], "seed": seed, "steps": steps, "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": prefix}},
    }
    return wf


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="work/canvas_gray.png")
    p.add_argument("--prompt", required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=25)
    p.add_argument("--prefix", default="vulpix")
    p.add_argument("--out", required=True)
    p.add_argument("--lora", default="outpaint-v2.safetensors")
    p.add_argument("--submit-only", action="store_true")
    a = p.parse_args()

    name = cc.upload(ROOT / a.input, name=f"{a.prefix}_{a.seed}.png")
    wf = workflow(name, a.prompt, a.seed, a.steps, a.prefix, lora=a.lora)
    pid = cc.submit(wf)
    print("prompt_id", pid, flush=True)
    (ROOT / "work/last_prompt.json").write_text(json.dumps(wf, indent=2))
    if a.submit_only:
        return
    item = cc.wait(pid)
    imgs = cc.output_images(item)
    if not imgs:
        raise RuntimeError("no images in history")
    dest = Path(a.out)
    cc.download(imgs[0], dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()
