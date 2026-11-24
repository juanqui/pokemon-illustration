# Pokémon TCG: 30th Celebration — archive + exact-window sleeve pipeline

Two linked deliverables:

1. **The official 30th Celebration gallery archive** — every distinct card image
   the official gallery serves, organized with a manifest, contact sheets and the
   official checklist.
2. **The Vulpix 009 exact-window sleeve** — a full-art card built *outside* an
   untouched 617×383 source window, with a UV print file whose window is
   transparent so the real card shows through the sleeve.

## Repository map

```
cards/30th-celebration/        188 distinct official card images
  images/main/                 158 cards (001–158)
  images/classic/              30 Classic Collection cards
  manifest.json                names, numbers, source URLs, tags
  contact-main.jpg             all 158 main cards
  contact-classic.jpg          all 30 Classic cards
  docs/                        official checklist PDF
projects/vulpix-30th/          Vulpix 009 project
  source/card.png              user-supplied 732×1024 mockup
  output/cards/                final exact-window cards
  output/print/                UV sleeve print + white mask + previews
  output/verification/         source-vs-final zero-diff proof
pipeline/                      canvas, ComfyUI outpainting, compositor, print/verify
skill/tcg-window-outpaint/     reusable skill (also installed in ~/.agents/skills)
```

## 1. 30th Celebration archive

**188 distinct card images** downloaded from the official gallery as 2× PNGs
(660×920): **158 main** + **30 Classic Collection**.

- [Main contact sheet](cards/30th-celebration/contact-main.jpg) ·
  [Classic contact sheet](cards/30th-celebration/contact-classic.jpg)
- [Manifest](cards/30th-celebration/manifest.json) ·
  [Dataset notes](cards/30th-celebration/README.md) ·
  [Official checklist PDF](cards/30th-celebration/docs/30c_web_cardlist_en.pdf)

The gallery’s Futuristic Rare filter repeats main 157/158 and its `EN_1` tile is
a 404 placeholder; 191 gallery tiles were observed but only **188 distinct card
images** are served. The checklist’s 3 Ultra Secret / Basic Energy entries are
not exposed as gallery card images. Details and the full caveat are in the
dataset README.

## 2. Vulpix 009 exact-window sleeve

The source window is **not scaled, shifted, cropped, feathered or repainted**:
617×383 at `(66,101)`, copied hard-edged 1:1. Full-window verification:
**236,311 px, MAE 0.0, max 0**. Only the outside is out-painted.

- [Spring card](projects/vulpix-30th/output/cards/vulpix_exact_spring.png) ·
  [Blossom card](projects/vulpix-30th/output/cards/vulpix_exact_blossom.png)
- [Preservation proof](projects/vulpix-30th/output/verification/window_exact.jpg)
- [UV print file](projects/vulpix-30th/output/print/vulpix_exact_spring_print_300dpi.png) ·
  [real-card preview](projects/vulpix-30th/output/print/vulpix_exact_spring_print_preview_real.jpg) ·
  [alpha preview](projects/vulpix-30th/output/print/vulpix_exact_spring_print_preview_alpha.jpg)
- Print details: 750×1050 @ 300 DPI, window hole 70,106–698,494 (2 px inset),
  white-ink mask, RGBA transparency; see the
  [project README](projects/vulpix-30th/README.md).
- **Skill-required final-final:** [textless card](projects/vulpix-30th/output/cards/vulpix_exact_blossom_textless.png) ·
  [clear-window print](projects/vulpix-30th/output/print/vulpix_exact_blossom_textless_print_300dpi.png) ·
  [real-card preview](projects/vulpix-30th/output/print/vulpix_exact_blossom_textless_print_preview_real.jpg) ·
  [three-panel comparison](projects/vulpix-30th/output/verification/textless_blossom.jpg).

## 3. Pipeline

`pipeline/` contains the reproducible chain: exact-content canvas → Qwen-Image-2.1
INT8 convrot + outpaint LoRA (outside only) → exact-window composite + chrome →
MAE-0 verification → UV print with transparent window, white mask, real-card
preview, inset/DPI/mirror controls.

## 4. Skill

**`tcg-window-outpaint`** — invoke `skill://tcg-window-outpaint`. Installed at
`~/.agents/skills/tcg-window-outpaint/` and copied under
[`skill/tcg-window-outpaint/`](skill/tcg-window-outpaint/). It encodes the
non-negotiables (hard-edged window, only outside generated, MAE 0, print hole)
and the per-card `config.example.json`.

## Copyright

Unofficial fan work. Pokémon and all card images are © Nintendo / Creatures Inc.
/ GAME FREAK inc. / The Pokémon Company. Card images belong to their respective
rights holders; do not sell or redistribute commercially.
