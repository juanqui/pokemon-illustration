---
name: tcg-window-outpaint
description: Turn any TCG card into a full-art sleeve print with its original art window preserved 1:1 and only the outside out-painted; always emit a textless final card, a UV print layer with an exactly aligned transparent window, white-ink mask, real-card preview, and a source | textless final | clear-window print comparison.
---

# TCG window outpainting → UV sleeve print

Use when the user wants a full-art version of a card **without changing the
Pokémon window**, and/or a UV-printable sleeve where the real card's window shows
through the printed surround.

Reference implementation + scripts: https://github.com/juanqui/pokemon-illustration
(local: `~/Git/pokemon-illustration`). The three helper scripts in this skill are
`make_textless.py`, `make_print.py` and `verify_window.py`; the
canvas/outpaint/compositor live in the repo.

## Required outputs (always)

Every run must produce and show all three, side by side:

1. **Source card** — unchanged reference.
2. **Textless final card** (`projects/vulpix-30th/output/cards/NAME_textless.png`) — illustration only:
   no name, HP, attack, footer, flavor, artist or copyright text. Rounded RGBA
   silhouette; exact source window pasted hard-edged at its source coordinates.
3. **Clear-window UV print layer**
   (`projects/vulpix-30th/output/print/NAME_textless_print_300dpi.png`) — RGBA, alpha 0 through the
   scaled window hole (default 2 px inset), opaque surround. This is the
   **final-final output**. The
   Pokémon must be **absent from this layer** because the real card inserted
   behind the sleeve supplies the window. Always include both
   `..._print_preview_alpha.jpg` (checkerboard) and
   `..._print_preview_real.jpg` (real card behind).

Show the three as `source | textless final | clear-window print`. Never present
the textless card, the worded card, or the art-only plate as the final print.
The clear-window print layer is what goes on the sleeve.

## Non-negotiables

1. The art window rectangle comes from the source card pixels and is copied
   **hard-edged 1:1 at the same x/y**. No scale, shift, crop, stretch, feather,
   or repaint. The full window must measure **MAE 0.0** vs the source.
2. Only the gray area **outside** the window is generated. The model must not
   touch the window; the compositor pastes it back last.
3. No text, gradient, grade, vignette, border, or sticker may be drawn over the
   window. Stop the top gradient above it; start the bottom gradient below it;
   protect the window from the global grade.
4. Print file: RGBA PNG, **alpha 0 inside the window hole**, opaque outside; hole
   at the scaled window rect (default 2 px inset for registration). Do not mirror
   unless printing the reverse/inside; then pass `--mirror` and re-check.
5. Verify before delivering: full-window MAE 0, print hole alpha 0, print size /
   DPI / hole coordinates recorded.
6. Always emit the textless card and the clear-window print layer. The print
   layer is not the textless card and not the chrome card: its window is
   transparent, and the Pokémon is not printed. A comparison without the
   checkerboard print panel is incomplete.

## Workflow

1. **Measure** the source art content rect `(x0,y0,x1,y1)` in source pixels.
   Do not guess; inspect the source and confirm the crop excludes the silver
   frame but includes the full illustration. Record the aspect.
2. **Exact canvas** (repo `pipeline/make_content_canvas.py`): 736×1024 gray,
   paste the 617×383 window at its source coords, add the sticker/decal mask if
   present. Everything else flat `#808080`.
3. **Outpaint outside** (repo `pipeline/outpaint.py`): Qwen-Image-2.1 INT8
   convrot + `outpaint-v2.safetensors`, 25 steps, CFG 1, euler/simple. Prompt
   describes the whole card scene and explicitly says: keep the illustration and
   sticker unchanged; only outside. Use 1–2 seeds; 736×1024 is enough. Pause the
   vLLM GPU services first if VRAM is tight; resume after.
4. **Textless final (required).** Save the out-painted art plate at card size
   with the exact window/sticker, then run:
   ```bash
   python pipeline/make_textless.py --art projects/vulpix-30th/output/art/NAME.jpg \
     --source projects/vulpix-30th/source/card.png --window 66,101,683,484 \
     --sticker-mask work/sticker_mask_final.png \
     --out-card projects/vulpix-30th/output/cards/NAME_textless.png \
     --print-dir projects/vulpix-30th/output/print --name NAME_textless \
     --dpi 300 --inset 2 --compare projects/vulpix-30th/output/verification/textless_NAME.jpg
   ```
   It pastes the exact window and sticker, applies the rounded silhouette, writes
   the textless card, generates the clear-window print layer and previews,
   verifies window MAE 0 and hole alpha 0, and writes the three-panel comparison.
5. **Chrome card (optional).** If card text/chrome is wanted, compose it with
   `pipeline/compose_window_card.py`: paste the exact window (hard edge) and
   sticker; keep chrome/text outside; protect the window from the grade; add the
   card frame and rounded silhouette. Adapt the text fields for the target card.
   The chrome card and its print are separate optional assets; never use them as
   the textless final or as the comparison's final panel.
6. **Verify** any chrome card too:
   ```bash
   python pipeline/verify_window.py --card projects/vulpix-30th/output/cards/NAME.png \
     --source projects/vulpix-30th/source/card.png --window 66,101,683,484
   ```
   Full window must be `mae: 0.0, max: 0`.
7. **UV print** is already generated by step 4:
   ```bash
   python pipeline/make_print.py --card projects/vulpix-30th/output/cards/NAME_textless.png \
     --source projects/vulpix-30th/source/card.png --window 66,101,683,484 \
     --dpi 300 --inset 2 --out-dir projects/vulpix-30th/output/print --name NAME_textless
   ```
   Outputs `NAME_textless_print_300dpi.png` (RGBA, transparent window),
   `..._white.png` (white-ink mask), `..._print_preview_real.jpg` (real card
   behind) and `..._print_preview_alpha.jpg` (checkerboard).
8. **Show** the three-panel comparison `source | textless final | clear-window
   print` and link the real-card preview. Do not show only the illustration card.

## Print / sleeve notes

- Print size default **2.5×3.5 in @ 300 DPI = 750×1050 px**; set `--dpi` and
  `--card-in` for other cards. The real card is inserted behind; the printed
  surround hides its frame/panel and its chrome; the real card’s window shows
  through the hole.
- The textless print layer is the final-final output. Its checkerboard preview
  is the proof that the window is clear; its real-card preview is the assembled
  sleeve. Keep both.
- `--inset 2` shrinks the hole by 2 print px so slight registration error is
  hidden under the printed surround. Increase for loose registration, decrease
  to show more of the real card.
- `--mirror` only for printing on the inside/reverse of a clear sleeve; otherwise
  print unmirrored.
- White mask: white = white-ink underbase, black = no ink (window + card
  corners). Follow the printer’s convention; if it expects an inverted mask,
  invert it.
- For a bleed, pad the artwork by 2–3 mm and keep the window hole in the same
  physical position; the repo print script is card-size by default.

## Why the earlier attempts were wrong (keep these rules)

- Raw outpaint re-rendered the window (MAE 4.64, max 255). Rejected.
- Preserving only the fox but scaling the window to card width / replacing its
  background was still wrong: the whole window’s size, position, aspect and
  content are fixed.
- The correct unit is the **art window rectangle**, not the character silhouette.
- A whole-window paste with a soft feather hides the seam but changes edge
  pixels; the final invariant is a hard, exact paste.
- Showing the wordless illustration as the final was incomplete: it still
  contains the Pokémon and no clear window. The final-final output is the print
  layer with alpha 0 in the window; the real card supplies the Pokémon.
- The model only ever fills the outside; the compositor is the authority on the
  window.

## Any card

Copy `config.example.json`, set `source`, `window_rect`, `card_size`, the chrome
fields, the outpaint prompt/seed, and print DPI/inset. The compositor template is
a 732×1024 SIR layout; scale positions/font sizes by `card_size / [732,1024]`.
The window rect and the hard-edge/verification rules never change. Always run
`make_textless.py` for the required textless card, clear-window print and
three-panel comparison.

## Current example

Vulpix 30th window, 617×383 at (66,101): full window 236,311 px, MAE 0.0,
max 0. Textless blossom card:
`projects/vulpix-30th/output/cards/vulpix_exact_blossom_textless.png` (window MAE 0.0). Clear-window
print: `projects/vulpix-30th/output/print/vulpix_exact_blossom_textless_print_300dpi.png`, hole
70,106–698,494 at 300 DPI (2 px inset, alpha 0), with
`..._print_preview_real.jpg` and `..._print_preview_alpha.jpg`. Three-panel
comparison: `projects/vulpix-30th/output/verification/textless_blossom.jpg`.
