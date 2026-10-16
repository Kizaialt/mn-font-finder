# Preview subsets

Small WOFF2 subsets (Basic Latin + Cyrillic + ₮ №) used only for the library cards, so they load fast.
They are not meant for download.

- `*MN.woff2`, `OrangerieMN.woff2`: subsets of the Mongolian editions in
  [Kizaialt/mn-font-editions](https://github.com/Kizaialt/mn-font-editions), SIL Open Font License 1.1.
  The full fonts, licenses and FONTLOG are in that repository.
- `DejaVu*.woff2`: subsets of DejaVu fonts (Bitstream Vera and public domain changes,
  https://dejavu-fonts.github.io/License.html). Copyright Bitstream, Inc. and the DejaVu authors.

Regenerate with `python tools/make_previews.py`.
