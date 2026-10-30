"""Build mogul.json: what each "Mogul ..." font (kok.mn Mogul pack, 2010) really is.

Source: the research table D:\\Claude\\font-packs\\mogul_map.csv (one row per Mogul family).
Each row in mogul.json:
  [Mogul name without "Mogul ", real name ("" = not found), designer, maker,
   licence of the original (c paid, w comes with Windows, u unknown, fc free incl. commercial, fp personal use only, o open),
   official source URL, original has Ө/Ү (y/n/u), free look-alike in the MonFont library, confidence (h/m/l),
   short real name and short maker for one-line card text (no bracketed notes)]

usage: python tools/build_mogul.py [path/to/mogul_map.csv]
"""
import csv, json, os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else r"D:\Claude\font-packs\mogul_map.csv"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mogul.json")
LIC = {"commercial": "c", "unknown": "u", "free-commercial": "fc", "free-personal": "fp",
       "OFL": "o", "Apache": "o", "other-open": "o"}

def short(s):
    s = re.sub(r"\s*\([^)]*\)", "", s)
    return re.sub(r",?\s*(probably|unconfirmed)$", "", s).strip(" ,")


rows = []
for r in csv.DictReader(open(SRC, encoding="utf-8-sig")):
    name = r["mogul_name"]
    assert name.startswith("Mogul "), name
    orig = r["original_name"].strip()
    if orig.startswith("unknown"):
        orig = ""
    rows.append([
        name[len("Mogul "):],
        orig,
        r["designer"].strip() if orig else "",
        r["foundry"].strip() if orig else "",
        ("w" if "ships with Windows" in r["foundry"] else LIC[r["original_licence"]]) if orig else "u",
        r["legal_source_url"].strip() if orig else "",
        {"yes": "y", "no": "n"}.get(r["original_has_OoUu"], "u") if orig else "u",
        r["free_lookalike"].strip(),
        {"high": "h", "medium": "m"}.get(r["confidence"], "l"),
        short(orig),
        re.sub(r"^sold by\s+", "", short(re.split(r"[;,]", short(r["foundry"]))[0])) if orig else "",
    ])
rows.sort(key=lambda x: x[0].lower())
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump({"v": 1, "rows": rows}, f, ensure_ascii=False, separators=(",", ":"))
    f.write("\n")
print(f"{len(rows)} Mogul families -> {OUT} ({os.path.getsize(OUT) // 1024} KB), "
      f"{sum(1 for x in rows if x[1])} identified")
