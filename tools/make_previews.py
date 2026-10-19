"""Builds small WOFF2 preview subsets of the Mongolian editions for the library cards.

The full fonts are 350-420 KB each; the cards only need Latin + Cyrillic, so each preview is
a few tens of KB. Downloads still point at the full fonts in mn-font-editions.

Usage (both repos side by side in D:\\Claude):
    python tools/make_previews.py [path-to-mn-font-editions]
"""
import sys, pathlib, subprocess

here = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent / "mn-font-editions"
out = here / "previews"
out.mkdir(exist_ok=True)

FILES = {
    "UnboundedMN": "UnboundedMN[wght].ttf",
    "SofiaSansMN": "SofiaSansMN[wght].ttf",
    "SofiaSansSemiCondensedMN": "SofiaSansSemiCondensedMN[wght].ttf",
    "SofiaSansCondensedMN": "SofiaSansCondensedMN[wght].ttf",
    "SofiaSansExtraCondensedMN": "SofiaSansExtraCondensedMN[wght].ttf",
    "YanoneKaffeesatzMN": "YanoneKaffeesatzMN[wght].ttf",
    "JuraMN": "JuraMN[wght].ttf",
    "AlumniSansMN": "AlumniSansMN[wght].ttf",
    "AlumniSansSCMN": "AlumniSansSCMN[wght].ttf",
    "AlumniSansPinstripeMN": "AlumniSansPinstripeMN-Regular.ttf",
    "WixMadeforTextMN": "WixMadeforTextMN[wght].ttf",
    "WixMadeforDisplayMN": "WixMadeforDisplayMN[wght].ttf",
    "MurechoMN": "MurechoMN[wght].ttf",
    "MartianMonoMN": "MartianMonoMN[wdth,wght].ttf",
    "BonaNovaMN": "BonaNovaMN-Regular.ttf",
    "BonaNovaSCMN": "BonaNovaSCMN-Regular.ttf",
    "OrangerieMN": "OrangerieMN-Regular.ttf",
    "JostMN": "JostMN[wght].ttf",
    "TuulOneMN": "TuulOneMN-Regular.ttf",
    "AltoSansMN": "AltoSansMN-Regular.ttf",
    "DelaGothicOneMN": "DelaGothicOneMN-Regular.ttf",
    "GidoleMN": "GidoleMN-Regular.ttf",
    "ElMessiriMN": "ElMessiriMN[wght].ttf",
    "PlainOneMN": "PlainOneMN-Regular.ttf",
    "SelengeSansMN": "SelengeSansMN-Regular.ttf",
}
# Basic Latin, Latin-1 punctuation, Cyrillic, the tugrik and numero signs, general punctuation, minus
UNICODES = "U+0020-007E,U+00A0,U+00AB,U+00BB,U+0400-04FF,U+2010-2027,U+2030,U+20AE,U+2116,U+2212"

total = 0
for name, fn in FILES.items():
    f = src / "build" / name / fn
    dst = out / f"{name}.woff2"
    subprocess.run([sys.executable, "-m", "fontTools.subset", str(f), f"--unicodes={UNICODES}", "--flavor=woff2",
                    "--layout-features=*", "--no-hinting", "--desubroutinize", f"--output-file={dst}"], check=True)
    total += dst.stat().st_size
    print(f"{name:28} {f.stat().st_size // 1024:4d} KB -> {dst.stat().st_size // 1024:3d} KB")
# DejaVu (Bitstream Vera licence: redistribution and subsetting allowed, names don't contain "Bitstream"/"Vera")
import urllib.request, tempfile
DEJAVU = {n: f"https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/{n}.ttf" for n in ("DejaVuSans", "DejaVuSerif", "DejaVuSansMono")}
with tempfile.TemporaryDirectory() as tmp:
    for name, url in DEJAVU.items():
        f = pathlib.Path(tmp) / f"{name}.ttf"
        urllib.request.urlretrieve(url, f)
        dst = out / f"{name}.woff2"
        subprocess.run([sys.executable, "-m", "fontTools.subset", str(f), f"--unicodes={UNICODES}", "--flavor=woff2",
                        "--layout-features=*", "--no-hinting", "--desubroutinize", f"--output-file={dst}"], check=True)
        total += dst.stat().st_size
        print(f"{name:28} {f.stat().st_size // 1024:4d} KB -> {dst.stat().st_size // 1024:3d} KB")
print(f"total previews: {total // 1024} KB")
