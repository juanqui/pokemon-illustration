"""Compose every raw candidate into a card."""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = sorted((ROOT / "out/raw").glob("*.png")) + sorted((ROOT / "out/raw2").glob("*.png"))
for f in files:
    if f.name.endswith("_732.png"):
        continue
    out = ROOT / "out/cards" / f"{f.stem}_card.png"
    subprocess.run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/compose_card.py"), str(f), str(out)],
                   check=True)
    print(out.name)
