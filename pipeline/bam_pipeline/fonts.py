"""Fetch the open-licensed fonts and prepare them for the web and the map.

- UI fonts: the variable TTFs from google/fonts (pinned commit), cut to the characters the
  site can show and compressed to WOFF2 in public/generated/fonts/, with their OFL license
  files. Source Serif 4 reserves the name "Source", so its subsets ship as Megaprojects Serif.
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
from pathlib import Path

from fontTools import subset
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

# Source Serif 4's own name records reserve the name "Source" for Adobe, and the OFL doesn't let a
# Modified Version (a subset or an instance) keep a Reserved Font Name. So everything made from it
# here is renamed Megaprojects Serif (Matthew, 2026-10-13).
SERIF = ("Source Serif 4", "Megaprojects Serif")

# Name records kept as the authors wrote them: copyright, trademark, license and license URL.
KEPT_NAMES = {0, 7, 13, 14}

# Map label fontstack name -> (variable source file, axis locations)
INSTANCES = {
    "Libre Franklin Regular": ("LibreFranklin[wght].ttf", {"wght": 400}),
    "Libre Franklin Medium": ("LibreFranklin[wght].ttf", {"wght": 500}),
    "Libre Franklin SemiBold": ("LibreFranklin[wght].ttf", {"wght": 600}),
    "Libre Franklin Italic": ("LibreFranklin-Italic[wght].ttf", {"wght": 400}),
    "Megaprojects Serif Regular": ("SourceSerif4[opsz,wght].ttf", {"wght": 400, "opsz": 16}),
    "Megaprojects Serif SemiBold": ("SourceSerif4[opsz,wght].ttf", {"wght": 600, "opsz": 16}),
    "Megaprojects Serif Italic": ("SourceSerif4-Italic[opsz,wght].ttf", {"wght": 400, "opsz": 16}),
}

WEB = {
    "LibreFranklin[wght].ttf": "LibreFranklin-Variable.woff2",
    "LibreFranklin-Italic[wght].ttf": "LibreFranklin-Italic-Variable.woff2",
    "SourceSerif4[opsz,wght].ttf": "MegaprojectsSerif-Variable.woff2",
    "SourceSerif4-Italic[opsz,wght].ttf": "MegaprojectsSerif-Italic-Variable.woff2",
}

# The characters the web fonts keep: Latin with Latin-1 and Latin Extended-A, general punctuation,
# arrows and a few symbols. tests/fonts.test.ts checks the data and interface text against it.
WEB_UNICODES = (
    "U+0000-017F, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, "
    "U+2190-2193, U+2212, U+2215, U+2248, U+2260, U+2264-2265"
)

# The serif sets only summaries (15.5 px, regular), so its web copies fix the optical size at 15.5,
# what browsers pick for that size, and keep weights 400-700 (as the @font-face rules in
# src/styles.css say). If the summary size changes, change opsz with it.
WEB_AXES = {
    "SourceSerif4[opsz,wght].ttf": {"opsz": 15.5, "wght": (400, 700)},
    "SourceSerif4-Italic[opsz,wght].ttf": {"opsz": 15.5, "wght": (400, 700)},
}


def rename(font: TTFont, old: str, new: str) -> TTFont:
    """Swap a family name through the name table, PostScript spellings included."""
    name = font["name"]
    for rec in name.names:
        if rec.nameID not in KEPT_NAMES:
            rec.string = rec.toUnicode().replace(old, new).replace(old.replace(" ", ""), new.replace(" ", ""))
    reserved = old.split()[0]
    left = sorted({r.nameID for r in name.names if r.nameID not in KEPT_NAMES and reserved in r.toUnicode()})
    if left:
        raise SystemExit(f"[fonts] {new}: name records {left} still say {reserved!r}")
    name.setName(f"{new} is {old}, modified under the SIL Open Font License.", 10, 3, 1, 0x409)
    return font


def named(font: TTFont, src: str) -> TTFont:
    """Source Serif 4's derivatives renamed Megaprojects Serif; other fonts as they are."""
    return rename(font, *SERIF) if src.startswith("SourceSerif4") else font


def web_font(path: Path, axes: dict | None) -> TTFont:
    """A variable font cut to WEB_UNICODES (and WEB_AXES), every OpenType feature kept."""
    font = TTFont(path)
    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=subset.parse_unicodes(WEB_UNICODES))
    subsetter.subset(font)
    # Subset first: an instanced font's in-memory glyph variations trip the subsetter.
    if axes:
        font = instancer.instantiateVariableFont(font, axes, updateFontNames=False)
    font.flavor = "woff2"
    return font


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
        named(inst, src).save(static / f"{name}.ttf")
    print(f"[fonts] {len(INSTANCES)} static instances for map glyphs in {static}")

    config.FONTS_OUT.mkdir(parents=True, exist_ok=True)
    for src, out in WEB.items():
        named(web_font(raw / src, WEB_AXES.get(src)), src).save(config.FONTS_OUT / out)
    for lic in ("LibreFranklin-OFL.txt", "SourceSerif4-OFL.txt"):
        shutil.copy(raw / lic, config.FONTS_OUT / lic)
    print(f"[fonts] web fonts in {config.FONTS_OUT}")


if __name__ == "__main__":
    main()
