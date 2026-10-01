"""Fetch the open-licensed fonts and prepare them for the web and the map.

- UI fonts: the variable TTFs from google/fonts (pinned commit) compressed to WOFF2
  in public/generated/fonts/, with their OFL license files.
- Map label fonts: static instances (Regular, Italic, SemiBold...) written to
  data/build/fonts/, which scripts/build-glyphs.mjs turns into SDF glyph PBFs.
  The Libre Franklin variable font defaults to Thin (100), so every instance sets
  its weight explicitly.

    uv run --directory pipeline python -m bam_pipeline.fonts
"""

from __future__ import annotations

import shutil
import urllib.parse
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from . import config

BASE = f"https://raw.githubusercontent.com/google/fonts/{config.GOOGLE_FONTS_COMMIT}/ofl"

SOURCES = {
    "LibreFranklin[wght].ttf": "librefranklin/LibreFranklin[wght].ttf",
    "LibreFranklin-Italic[wght].ttf": "librefranklin/LibreFranklin-Italic[wght].ttf",
    "LibreFranklin-OFL.txt": "librefranklin/OFL.txt",
    "SourceSerif4[opsz,wght].ttf": "sourceserif4/SourceSerif4[opsz,wght].ttf",
    "SourceSerif4-Italic[opsz,wght].ttf": "sourceserif4/SourceSerif4-Italic[opsz,wght].ttf",
    "SourceSerif4-OFL.txt": "sourceserif4/OFL.txt",
}

# Map label fontstack name -> (variable source file, axis locations)
INSTANCES = {
    "Libre Franklin Regular": ("LibreFranklin[wght].ttf", {"wght": 400}),
    "Libre Franklin Medium": ("LibreFranklin[wght].ttf", {"wght": 500}),
    "Libre Franklin SemiBold": ("LibreFranklin[wght].ttf", {"wght": 600}),
    "Libre Franklin Italic": ("LibreFranklin-Italic[wght].ttf", {"wght": 400}),
    "Source Serif 4 Regular": ("SourceSerif4[opsz,wght].ttf", {"wght": 400, "opsz": 16}),
    "Source Serif 4 SemiBold": ("SourceSerif4[opsz,wght].ttf", {"wght": 600, "opsz": 16}),
    "Source Serif 4 Italic": ("SourceSerif4-Italic[opsz,wght].ttf", {"wght": 400, "opsz": 16}),
}

WEB = {
    "LibreFranklin[wght].ttf": "LibreFranklin-Variable.woff2",
    "LibreFranklin-Italic[wght].ttf": "LibreFranklin-Italic-Variable.woff2",
    "SourceSerif4[opsz,wght].ttf": "SourceSerif4-Variable.woff2",
    "SourceSerif4-Italic[opsz,wght].ttf": "SourceSerif4-Italic-Variable.woff2",
}


def main() -> None:
    raw = config.ROOT / "data" / "raw" / "fonts" / config.GOOGLE_FONTS_COMMIT[:7]
    raw.mkdir(parents=True, exist_ok=True)
    for local, remote in SOURCES.items():
        dest = raw / local
        if not dest.exists():
            url = f"{BASE}/{urllib.parse.quote(remote)}"
            with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
                shutil.copyfileobj(r, f)
    print(f"[fonts] sources in {raw}")

    static = config.BUILD / "fonts"
    static.mkdir(parents=True, exist_ok=True)
    for name, (src, axes) in INSTANCES.items():
        font = TTFont(raw / src)
        inst = instancer.instantiateVariableFont(font, axes, updateFontNames=False)
        inst.save(static / f"{name}.ttf")
    print(f"[fonts] {len(INSTANCES)} static instances for map glyphs in {static}")

    config.FONTS_OUT.mkdir(parents=True, exist_ok=True)
    for src, out in WEB.items():
        font = TTFont(raw / src)
        font.flavor = "woff2"
        font.save(config.FONTS_OUT / out)
    for lic in ("LibreFranklin-OFL.txt", "SourceSerif4-OFL.txt"):
        shutil.copy(raw / lic, config.FONTS_OUT / lic)
    print(f"[fonts] web fonts in {config.FONTS_OUT}")


if __name__ == "__main__":
    main()
