"""Builds WOFF2 preview subsets for the non-Google free fonts in EXTRA_FREE (added 2026-10-31).

Each source is the font's official file (or Fontsource's unsubsetted copy). The preview keeps only
Latin + Cyrillic + ₮ №, and is renamed "MonFont Preview NN" inside the font: under the OFL (and the
Bitstream Vera / Hack licences) a subset is a Modified Version, which may not use a Reserved Font
Name. Copyright and licence name records are kept. Downloads on the site point at the official files.

Usage:
    python tools/make_extra_previews.py
"""
import io, pathlib, sys, tempfile, urllib.request, zipfile

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

here = pathlib.Path(__file__).resolve().parent.parent
out = here / "previews"
FS = "https://cdn.jsdelivr.net/fontsource/fonts/{}@latest/latin-400-normal.ttf"
FL = "https://fontlibrary.org/assets/fonts/"
GH = "https://raw.githubusercontent.com/"

# preview name: (source URL, member inside a zip or None, variable-font location or None)
SOURCES = {
    "DMSansMN": (GH + "gege-mn/dm-sans-mn/main/fonts/ttf/DMSansMN-Regular.ttf", None, None),
    "AdwaitaSans": (FS.format("adwaita-sans"), None, None),
    "AdwaitaMono": (FS.format("adwaita-mono"), None, None),
    "ArgentumSans": (FS.format("argentum-sans"), None, None),
    "FiraGO": (FS.format("firago"), None, None),
    "HauoraSans": (FS.format("hauora-sans"), None, None),
    "OpenRunde": (FS.format("open-runde"), None, None),
    "OpenDyslexic": (FS.format("opendyslexic"), None, None),
    "iAWriterQuattro": (FS.format("ia-writer-quattro"), None, None),
    "iAWriterMono": (FS.format("ia-writer-mono"), None, None),
    "iAWriterDuo": (FS.format("ia-writer-duo"), None, None),
    "Iosevka": (FS.format("iosevka"), None, None),
    "PitagonSansMono": (FS.format("pitagon-sans-mono"), None, None),
    "MapleMono": (FS.format("maple-mono"), None, None),
    "DINish": (GH + "playbeing/dinish/main/fonts/ttf/DINish/DINish-Regular.ttf", None, None),
    "Hack": (GH + "source-foundry/Hack/master/build/ttf/Hack-Regular.ttf", None, None),
    "LibraSans": (FL + "libra-sans/f603cd30e6aad824e4dd78e06303b91f/898f406452e8fe1ca12b9574aa949094/LibraSansRegular.ttf", None, None),
    "LibraSansModern": (FL + "libra-sans-modern/13740f175661b2eeb8442a7f55c7df37/a95712201f58677073ac3718faeaea40/LibraSansModernRegular.ttf", None, None),
    "LibraSerifModern": (FL + "libra-serif-modern/c4e1a594856aa86de73232004f7a2c14/fde8169988340ae66da188a2e335dd1a/LibraSerifModernRegular.otf", None, None),
    "Veleka": (FL + "veleka/584f559fc3138f92770b06014a7c119c/60771242ce2eeec807d9ea08b58b1d7a/VelekaRegular.otf", None, None),
    "CMUSerif": (FL + "cmu-serif/6fcdeb7a603e986ae49da1030eb1966b/01643be9fa75a4523c77ac348b242aed/CMUSerifRoman.ttf", None, None),
    "CMUSansSerif": (FL + "cmu-sans-serif/0da0d92e6bacf5e091c1ae85c4da581d/1b24573c1e6cf956df63c20903efe11d/CMUSansSerifMedium.ttf", None, None),
    "CMUBright": (FL + "cmu-bright/89df0df002bd3fe4185cc5d8f98a124c/ab3d145179022fb663f55f6a94e39ea8/CMUBrightRoman.ttf", None, None),
    "CMUConcrete": (FL + "cmu-concrete/4dc4d9812272fbd7cb913c389a001c50/c2cea5877a5cc064896ca11526a7dc46/CMUConcreteRoman.ttf", None, None),
    "CMUTypewriter": (FL + "cmu-typewriter/b6d120f7029a2f8b50af39054e05f1ef/c6d367cd3cb9d5b4c8fd3aca0fd169c7/CMUTypewriterTextRegular.ttf", None, None),
    "Coelacanth": (FL + "coelacanth/d40b6b08e184c21574151115a61a208d/e4100f3b73ad2317cc51d753e58a934d/CoelacanthRegular.otf", None, None),
    "Pfennig": (FL + "pfennig/8b5fa73ca4cf4cfa42d21b9f73f6060b/5f9297cd1d1e3d12b590f49735516e68/PfennigMedium.ttf", None, None),
    "Xolonium": (FL + "xolonium/e00c124f3e1b130e5ec2a7eee2f4f1b8/15f3a5a7a8424c8f843ba6c83bfc360d/XoloniumRegular.ttf", None, None),
    "MiamaNueva": (FL + "miama-nueva/9b82b0348ab54160865bc8cc9a6c434f/5a0aabc0ca89e6fc01dc68c23b1110cd/MiamaNuevaMedium.ttf", None, None),
    "DoulosSIL": ("https://software.sil.org/downloads/r/doulos/DoulosSIL-7.000.zip", "DoulosSIL-7.000/DoulosSIL-Regular.ttf", None),
    "FantasqueSansMono": ("https://github.com/belluzj/fantasque-sans/releases/download/v1.8.0/FantasqueSansMono-Normal.zip", "TTF/FantasqueSansMono-Regular.ttf", None),
    "IBM3270": ("https://github.com/rbanffy/3270font/releases/download/v3.0.1/3270_fonts_d916271.zip", "3270-Regular.ttf", None),
    "Fungal": ("https://gitlab.com/velvetyne/fungal/-/raw/main/fonts/ttf/Fungal-Grow400Thickness500.ttf", None, None),
    "Pecita": ("http://pecita.eu/b/Pecita.otf", None, None),
}
# Basic Latin, Latin-1 punctuation, Cyrillic, the tugrik and numero signs, general punctuation, minus
UNICODES = [*range(0x20, 0x7F), 0xA0, 0xAB, 0xBB, *range(0x400, 0x500), *range(0x2010, 0x2028), 0x2030, 0x20AE, 0x2116, 0x2212]
KEEP_NAMES = {0, 7, 8, 9, 11, 12, 13, 14}   # copyright, trademark, vendor, designer, URLs, licence


def fetch(url, member):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (MonFont preview builder)"})
    data = urllib.request.urlopen(req, timeout=120).read()
    if member:
        data = zipfile.ZipFile(io.BytesIO(data)).read(member)
    return data


def build(name, data, location, index):
    font = TTFont(io.BytesIO(data))
    if "fvar" in font:   # pin every axis: wght at 400 when it can be, the rest at their defaults
        pins = {a.axisTag: 400 if a.axisTag == "wght" and a.minValue <= 400 <= a.maxValue else a.defaultValue
                for a in font["fvar"].axes}
        font = instancer.instantiateVariableFont(font, {**pins, **(location or {})})
    opts = Options()
    opts.flavor = "woff2"
    # default feature set (kerning, ligatures, contextual forms, marks); stylistic alternates are not needed for a preview
    opts.hinting = False
    opts.desubroutinize = True
    opts.name_IDs = ["*"]
    sub = Subsetter(opts)
    sub.populate(unicodes=UNICODES)
    sub.subset(font)
    for t in ("STAT", "fvar", "avar", "gvar", "HVAR", "MVAR"):
        if t in font:
            del font[t]
    nt = font["name"]
    nt.names = [n for n in nt.names if n.nameID in KEEP_NAMES]
    fam = f"MonFont Preview {index:02d}"
    for nid, val in ((1, fam), (2, "Regular"), (3, f"{fam};preview"), (4, fam), (6, fam.replace(" ", "") + "-Regular"),
                     (10, f"Latin+Cyrillic preview subset of {name} for monfont.space, renamed as the font licence requires for modified versions. Not for download.")):
        nt.setName(val, nid, 3, 1, 0x409)
    if "CFF " in font:   # CFF fonts carry their names a second time
        cff = font["CFF "].cff
        cff.fontNames = [fam.replace(" ", "") + "-Regular"]
        top = cff.topDictIndex[0]
        top.FullName, top.FamilyName, top.Weight = fam, fam, "Regular"
    dst = out / f"{name}.woff2"
    font.save(dst)
    return dst


def main():
    out.mkdir(exist_ok=True)
    total = 0
    for i, (name, (url, member, location)) in enumerate(SOURCES.items(), 1):
        data = fetch(url, member)
        dst = build(name, data, location, i)
        total += dst.stat().st_size
        print(f"{name:20} {len(data) // 1024:5d} KB -> {dst.stat().st_size // 1024:3d} KB")
    print(f"total extra previews: {total // 1024} KB")


if __name__ == "__main__":
    sys.exit(main())
