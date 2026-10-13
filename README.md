# Фонт Шүүгч · Mongolian Font Finder

**https://kizaialt.github.io/mn-font-finder/**

Компьютер дээрээ суусан фонтуудаас **Ө ө Ү ү** үсгийг бүрэн агуулсныг нь олж, сурталчилгаанд хууль ёсоор ашиглаж болох эсэхийг харуулдаг үнэгүй хэрэгсэл. Фонт бүрийн үсгийн хүснэгтийг (cmap) болон файлд бичигдсэн лицензийн мэдээллийг шууд уншдаг.

A free tool that finds which fonts on your computer really contain the Mongolian Cyrillic letters **Ө ө Ү ү**, and whether they can legally be used in ads. It reads each font file's character map and embedded license information directly.

- **My fonts:** scans installed fonts (Chrome / Edge on a computer, via the Local Font Access API). Sorts them by Mongolian support (ready / partial / no Cyrillic), checks every style (so a family that breaks only in, say, Narrow is flagged), and labels each font's license from what the file says: open license, comes with Windows, license required, personal/demo, or unknown.
- **Check font files:** drop `.ttf`, `.otf` or `.ttc` files to check them before installing. Works in any modern browser.
- **Font library:** fonts verified to contain every Mongolian letter:
  - **Free:** open-license fonts from Google Fonts plus DejaVu and Liberation, each with its license and official download link.
  - **Comes with Windows:** Windows fonts that pass the check, usable in ads, logos and print under Microsoft's font terms.
  - **Paid:** places to buy fonts with Mongolian support, plus a way for designers to suggest their fonts.
  - Click any library font for the same detail view as installed fonts: every style, variable-axis sliders, the Mongolian alphabet and its license (designer, license text link, source).
- **License guide:** what you can and can't do with each kind of font, in Mongolian and English.
- **Shortlist:** star fonts for a project and share the list as a link.

Everything runs in the browser. No fonts or font lists are uploaded anywhere. Free-font previews load from Google Fonts and jsDelivr. License information is general guidance, not legal advice.

## Updating the Google Fonts list

```bash
pip install fonttools brotli
python tools/update_gallery.py
```

The script checks every Google Font with an extended-Cyrillic subset against the full Mongolian alphabet, looks up each family's license in the google/fonts repository, and rewrites the list in `index.html`. The non-Google free fonts, the Windows list and the paid sources are maintained by hand in `index.html` (`EXTRA_FREE`, `WINDOWS_LIB`, `PAID_LIB`).

## Suggesting a font

Made a font with full Mongolian Cyrillic support? [Open an issue](https://github.com/Kizaialt/mn-font-finder/issues/new?title=Font%20suggestion%3A%20) with the font name, where to get it and its license.
