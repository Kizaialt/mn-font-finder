# Фонт Шүүгч · Mongolian Font Finder

**https://kizaialt.github.io/mn-font-finder/**

Компьютер дээрээ суусан фонтуудаас **Ө ө Ү ү** үсгийг бүрэн агуулсныг нь олж харуулдаг үнэгүй хэрэгсэл. Фонт бүрийн үсгийн хүснэгтийг (cmap) шууд уншдаг тул хөтөч өөр фонтоор орлуулж харуулсан үсэгт хууртагдахгүй.

A free tool that finds which fonts on your computer really contain the Mongolian Cyrillic letters **Ө ө Ү ү**. It reads each font file's character map directly, so a letter the browser quietly borrows from another font never counts.

- **My fonts:** scans installed fonts (Chrome / Edge on a computer, via the Local Font Access API) and sorts them into Mongolian ready / Partial / No Cyrillic.
- **Check font files:** drop `.ttf`, `.otf` or `.ttc` files to check them before installing. Works in any modern browser.
- **Free fonts:** free Google Fonts verified to contain every Mongolian letter, with download links.
- **Shortlist:** star fonts for a project and share the list as a link.

Everything runs in the browser. No fonts or font lists are uploaded anywhere. Free-font previews load from Google Fonts.

## Updating the free-fonts list

```bash
pip install fonttools brotli
python tools/update_gallery.py
```

The script checks every Google Font with an extended-Cyrillic subset against the full Mongolian alphabet and rewrites the list in `index.html`.
