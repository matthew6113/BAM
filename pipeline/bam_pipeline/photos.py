"""Project photos from Wikimedia Commons (openly licensed or public domain only).

data/photos.json lists one Commons file per project, approved by Matthew. For each, this reads
the file's own Commons page (author, license, date taken), refuses anything outside the
allowed licenses, downloads a 1200 px copy once into data/raw/photos/, and re-encodes it
without metadata into public/photos/<id>.jpg (committed, so the site never hotlinks). The
credit fields are written back into data/photos.json.

    uv run --directory pipeline python -m bam_pipeline.photos [project-id ...]
"""

from __future__ import annotations

import hashlib
import html
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image

from . import config

MANIFEST = config.ROOT / "data" / "photos.json"
RAW = config.ROOT / "data" / "raw" / "photos"
OUT = config.ROOT / "public" / "photos"
API = "https://commons.wikimedia.org/w/api.php"
WIDTH = 1200
# Wikimedia asks automated clients to identify themselves.
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]
UA = "BAM-megaprojects-map/1.0 (https://github.com/matthew6113/BAM)"


def get(url: str) -> bytes:
    """GET politely: one request at a time, backing off when Wikimedia says to slow down."""
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            time.sleep(3)
            return data
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == 5:
                raise
            wait = max(int(e.headers.get("Retry-After") or 0), 15 * 2**attempt)
            print(f"  HTTP {e.code}, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise AssertionError("unreachable")


def plain(value: str) -> str:
    """Commons metadata is HTML; keep the text."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", value))).strip()


def commons_info(title: str) -> dict:
    cache = RAW / (hashlib.sha256(title.encode()).hexdigest()[:16] + ".json")
    if not cache.exists():
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "formatversion": "2", "titles": title,
            "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": WIDTH,
        })
        RAW.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(get(f"{API}?{q}"))
    page = json.loads(cache.read_text())["query"]["pages"][0]
    if "imageinfo" not in page:
        raise SystemExit(f"{title}: not found on Commons")
    return page["imageinfo"][0]


def taken(meta: dict) -> str | None:
    """The date the photo was taken, as YYYY-MM-DD or YYYY-MM or YYYY."""
    raw = plain(meta.get("DateTimeOriginal", {}).get("value", ""))
    m = re.search(r"(\d{4})(?:[-:](\d{2}))?(?:[-:](\d{2}))?", raw)
    if not m:
        return None
    if not m.group(2):  # e.g. "15 December 2022"
        d = re.search(r"(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", raw)
        if d:
            month = MONTHS.index(d.group(2)) + 1
            return f"{d.group(3)}-{month:02d}-{int(d.group(1)):02d}"
    return "-".join(p for p in m.groups() if p)


def build(photo: dict, allowed: list[str]) -> dict:
    info = commons_info(photo["file"])
    meta = info["extmetadata"]
    license_ = plain(meta.get("LicenseShortName", {}).get("value", ""))
    if license_.lower() in ("public domain", "pd"):
        license_ = "Public domain"
    if license_ == "CC0 1.0":
        license_ = "CC0"
    if license_ not in allowed:
        raise SystemExit(f"{photo['id']}: license {license_!r} is not allowed")
    author = plain(meta.get("Attribution", {}).get("value", "")) or plain(meta.get("Artist", {}).get("value", ""))
    if not author:
        raise SystemExit(f"{photo['id']}: no author on the Commons page")

    # Small originals come straight from the file; large ones from Commons' resized copy.
    src = info["url"] if info.get("size", 0) < 3_000_000 else (info.get("thumburl") or info["url"])
    raw = RAW / f"{photo['id']}{'.jpg' if src.lower().endswith(('.jpg', '.jpeg')) else '.img'}"
    if not raw.exists():
        raw.write_bytes(get(src))
    im = Image.open(io.BytesIO(raw.read_bytes())).convert("RGB")
    if im.width > WIDTH:
        im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{photo['id']}.jpg"
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True, progressive=True)  # no EXIF: drops GPS and camera data
    out.write_bytes(buf.getvalue())

    record = {k: photo[k] for k in ("id", "file", "caption", "note") if k in photo}
    record.update({
        "page": info["descriptionurl"],
        "author": author,
        "license": license_,
        "licenseUrl": meta.get("LicenseUrl", {}).get("value") or None,
        "taken": taken(meta),
        "src": f"photos/{photo['id']}.jpg",
        "width": im.width,
        "height": im.height,
        "sha256": hashlib.sha256(buf.getvalue()).hexdigest(),
    })
    if license_.startswith("CC BY"):
        record["modified"] = "Resized and re-encoded"
    return record


def main(argv: list[str]) -> None:
    manifest = json.loads(MANIFEST.read_text())
    allowed = manifest["_meta"]["allowedLicenses"]
    wanted = set(argv)
    for i, photo in enumerate(manifest["photos"]):
        if wanted and photo["id"] not in wanted:
            continue
        print(photo["id"], file=sys.stderr)
        manifest["photos"][i] = build(photo, allowed)
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")  # keep progress


if __name__ == "__main__":
    main(sys.argv[1:])
