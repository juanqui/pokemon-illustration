# Pokémon TCG: 30th Celebration — gallery image archive

Source: [official card gallery](https://tcg.pokemon.com/en-us/galleries/30th-celebration/)
· downloaded 2026-11-24 · official 2× PNG assets (660×920).

## What is here

| collection | count | files |
|---|---:|---|
| Main set (001–158) | 158 | `images/main/001.png` … `158.png` |
| Classic Collection | 30 | `images/classic/001.png` … `030.png` |
| **distinct card images** | **188** | 194 MB PNG |

- [`manifest.json`](manifest.json) — every card: id, collection, number,
  original number for Classic, name, local file, official source URL, tags.
- [`contact-main.jpg`](contact-main.jpg) — all 158 main cards.
- [`contact-classic.jpg`](contact-classic.jpg) — all 30 Classic cards.
- [`docs/30c_web_cardlist_en.pdf`](docs/30c_web_cardlist_en.pdf) — official
  checklist.

## Gallery counts / caveats

The gallery’s filters were followed with a real browser (the site is behind an
Incapsula challenge):

- **See All** loads **158** main cards.
- **Classic Collection** loads **30** distinct cards.
- **Futuristic Rare** adds only tiles for **157/158**, which are already in the
  main set; its `EN_1` image is a **404 placeholder**.
- Observed gallery tiles: **191**; distinct card images served: **188**.

The official checklist also lists 8 Basic Energy entries and the 191-card set.
The three Ultra Secret / Basic Energy entries are not exposed as separate card
images by the gallery; the 188 Pokémon card illustrations above are complete for
what the gallery serves. If the missing checklist entries are needed, source
them from the official card database/checklist PDF rather than inventing them.

Tags: `pikachu_rare` (main 023–052), `futuristic_rare` (main 157/158),
`classic_collection` (Classic files).

## Copyright

Unofficial fan archive for reference and non-commercial artwork. Pokémon and
all card images are © Nintendo / Creatures Inc. / GAME FREAK inc. / The Pokémon
Company. Card images belong to their respective rights holders; do not sell or
redistribute commercially.

`images/futuristic/157.png` and `158.png` are category copies of the two
Futuristic Rare cards already in the main set; `images/futuristic/README.md`
explains the empty `EN_1` tile and the 3 unexposed checklist entries.
