# Vulpix 009 — exact-window illustration-rare sleeve

The source graphic is **not redrawn, scaled, shifted, cropped or re-composited**:
the 617×383 art window is copied 1:1 at its exact source coordinates and only the
card area outside it is out-painted.

## Source

- `source/card.png` — 732×1024 user-supplied 30th Celebration Vulpix mockup.
- Official 009 image: `../../cards/30th-celebration/images/main/009.png`.
- Window: `x 66..683, y 101..484` → **617×383**, aspect **1.611**.

## Exact-window result

- Full window vs source: **236,311 px, MAE 0.0, max 0**.
- Hard-edge paste; no feather, grade, vignette, text or border over the window.
- The out-painted surround, chrome and sticker are outside the window.
- The window’s own inner rim is part of the source image, not a generated frame.

## Outputs

| path | what |
|---|---|
| `output/cards/vulpix_exact_spring.png` | final card, 732×1024 RGBA |
| `output/cards/vulpix_exact_blossom.png` | alternate scene |
| `output/previews/` | 732×1024 previews |
| `output/art/` | full art with exact window (no chrome) |
| `output/print/` | UV sleeve print, white mask, real/alpha previews |
| `output/verification/window_exact.jpg` | source vs final + zero-diff proof |
| `output/verification/metrics.json` | exact-window metrics |

## UV sleeve print

`output/print/vulpix_exact_spring_print_300dpi.png` — 750×1050 px at 300 DPI
(2.5×3.5 in), RGBA. Alpha is **0 inside the window hole** and opaque on the
printed surround; the printed frame/panel hides the real card’s frame and the
real card’s window shows through.

- Hole: **70,106–698,494** (source window scaled + 2 px inset for registration).
- White underbase: `..._white.png` (white = ink, black = window/corners).
- Real-card preview: `..._print_preview_real.jpg`.
- Alpha preview: `..._print_preview_alpha.jpg`.
- Mirror only if printing the reverse/inside of a clear sleeve.

Print the RGBA on the sleeve, insert the real card, align the window. The 2 px
inset hides minor registration error under the printed surround.

## Reproduce

```bash
# 1. exact-content canvas (requires the SAM sticker mask in work/)
python pipeline/segment_sticker.py
python pipeline/make_content_canvas.py

# 2. out-paint only the gray outside (ComfyUI 8188, Qwen-Image-2.1 + outpaint LoRA)
python pipeline/outpaint.py --input work/content_canvas_gray.png \
  --prompt "<scene prompt>" --seed 606 --steps 25 --prefix content_a \
  --out out/win_raw/content_a_606.png

# 3. compose exact-window card
python pipeline/compose_window_card.py out/win_raw/content_a_606.png \
  projects/vulpix-30th/output/cards/vulpix_exact_spring.png

# 4. verify + print
python pipeline/verify_window.py --card projects/vulpix-30th/output/cards/vulpix_exact_spring.png \
  --source projects/vulpix-30th/source/card.png --window 66,101,683,484
python pipeline/make_print.py --card projects/vulpix-30th/output/cards/vulpix_exact_spring.png \
  --source projects/vulpix-30th/source/card.png --window 66,101,683,484 \
  --dpi 300 --inset 2 --out-dir projects/vulpix-30th/output/print --name vulpix_exact_spring
```

Per-card settings are in `config.json`; the reusable procedure is the
`tcg-window-outpaint` skill (`skill://tcg-window-outpaint`).

## Textless final-final + clear-window print (skill requirement)

The reusable skill requires the **textless** card and the **clear-window print**
as the final-final output. Both are generated from the exact art plate with
`pipeline/make_textless.py` (window MAE 0.0, print hole alpha 0):

| output | file |
|---|---|
| textless final card | `output/cards/vulpix_exact_blossom_textless.png` |
| clear-window UV print | `output/print/vulpix_exact_blossom_textless_print_300dpi.png` |
| white-ink mask | `output/print/vulpix_exact_blossom_textless_print_300dpi_white.png` |
| real-card preview | `output/print/vulpix_exact_blossom_textless_print_preview_real.jpg` |
| checkerboard clear-window proof | `output/print/vulpix_exact_blossom_textless_print_preview_alpha.jpg` |
| three-panel comparison | `output/verification/textless_blossom.jpg` |

The worded chrome cards (`vulpix_exact_spring.png`, `vulpix_exact_blossom.png`)
remain as optional previews; the **textless clear-window print** is what goes on
the sleeve. The real card supplies the Pokémon/window; the printed surround is
textless and covers the real card's frame/panel.
