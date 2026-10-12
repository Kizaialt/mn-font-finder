"""Rebuild the Google Fonts part of the font library in index.html.

Takes every Google Font that ships an extended-Cyrillic subset, downloads the
files Google actually serves, and keeps only the families whose character map
contains every Mongolian Cyrillic letter (А–Я а–я Ё ё Ө ө Ү ү). Each family's
license comes from the folder it lives in on github.com/google/fonts (ofl/,
apache/, ufl/). The result is written between the GALLERY START/END markers in
index.html, most popular first.

Usage:  pip install fonttools brotli
        python tools/update_gallery.py
"""
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fontTools.ttLib import TTFont

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
MN = list(range(0x410, 0x450)) + [0x401, 0x451, 0x4E8, 0x4E9, 0x4AE, 0x4AF]
CATS = {"Sans Serif": "S", "Serif": "R", "Display": "D", "Handwriting": "H", "Monospace": "M"}
LICENSE_DIRS = {"ofl": "O", "apache": "A", "ufl": "U"}
INDEX = Path(__file__).resolve().parent.parent / "index.html"


def get(url, tries=3):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception:
            if i == tries - 1:
                raise


def css_query(fam):
    """css2 family query for the face closest to Regular."""
    name, fonts = urllib.parse.quote_plus(fam["family"]), fam["fonts"]
    if "400" in fonts:
        return name
    weights = sorted(int(k) for k in fonts if k.isdigit())
    if weights:
        return f"{name}:wght@{min(weights, key=lambda w: abs(w - 400))}"
    italics = sorted(int(k[:-1]) for k in fonts if k.endswith("i"))
    return f"{name}:ital,wght@1,{italics[0]}"


def check(fam):
    q = css_query(fam)
    css = get("https://fonts.googleapis.com/css2?family=" + q).decode()
    cps = set()
    for url in set(re.findall(r"url\((https://[^)]+)\)", css)):
        cps |= set(TTFont(io.BytesIO(get(url))).getBestCmap().keys())
    return {
        "family": fam["family"], "q": q, "cat": CATS.get(fam["category"], "S"), "pop": fam["popularity"],
        "ok": all(c in cps for c in MN), "tug": 0x20AE in cps,
        "axes": " ".join(a["tag"] for a in fam.get("axes", [])),
    }


def license_map():
    """family slug -> O/A/U, from the top-level license folders of google/fonts."""
    api = "https://api.github.com/repos/google/fonts/git/trees/"
    root = json.loads(get(api + "main"))["tree"]
    out = {}
    for entry in root:
        if entry["path"] in LICENSE_DIRS:
            for sub in json.loads(get(api + entry["sha"]))["tree"]:
                out[sub["path"]] = LICENSE_DIRS[entry["path"]]
    return out


def main():
    raw = get("https://fonts.google.com/metadata/fonts").decode()
    meta = json.loads(raw[4:] if raw.startswith(")]}'") else raw)["familyMetadataList"]
    candidates = [f for f in meta if "cyrillic-ext" in f.get("subsets", [])]
    print(f"{len(candidates)} families with an extended-Cyrillic subset; checking…")
    with ThreadPoolExecutor(12) as ex:
        results = list(ex.map(check, candidates))
    ok = sorted((r for r in results if r["ok"]), key=lambda r: r["pop"])
    print(f"{len(ok)} contain every Mongolian letter; {len(results) - len(ok)} do not.")

    licenses = license_map()
    for r in ok:
        r["lic"] = licenses.get(re.sub(r"[^a-z0-9]", "", r["family"].lower()))
    unknown = [r["family"] for r in ok if not r["lic"]]
    if unknown:
        sys.exit(f"No license folder found for: {', '.join(unknown)}")

    rows = ",\n".join("  " + json.dumps([r["family"], r["q"], r["cat"], int(r["tug"]), r["axes"], r["lic"]], ensure_ascii=False) for r in ok)
    block = f"// ==GALLERY START==\nconst GALLERY_DATA = [\n{rows},\n];\n// ==GALLERY END=="
    html = INDEX.read_text(encoding="utf-8")
    new, n = re.subn(r"// ==GALLERY START==.*?// ==GALLERY END==", lambda _: block, html, flags=re.S)
    if n != 1:
        sys.exit("GALLERY markers not found in index.html")
    INDEX.write_text(new, encoding="utf-8")
    print(f"Wrote {len(ok)} fonts to {INDEX}")


if __name__ == "__main__":
    main()
