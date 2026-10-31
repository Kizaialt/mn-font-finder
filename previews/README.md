# Preview subsets

Small WOFF2 subsets (Basic Latin + Cyrillic + ₮ №) used only for the library cards, so they load fast.
They are not meant for download.

- `*MN.woff2`, `OrangerieMN.woff2`: subsets of the Mongolian editions in
  [Kizaialt/mn-font-editions](https://github.com/Kizaialt/mn-font-editions), SIL Open Font License 1.1.
  The full fonts, licenses and FONTLOG are in that repository.
- `DejaVu*.woff2`: subsets of DejaVu fonts (Bitstream Vera and public domain changes,
  https://dejavu-fonts.github.io/License.html). Copyright Bitstream, Inc. and the DejaVu authors.

- The other non-Google free fonts in the library (DM Sans MN, Adwaita, CMU, Libra, Iosevka and the rest of
  `EXTRA_FREE` in `index.html`): subsets of each font's official file, renamed **"MonFont Preview NN"** inside the
  font. Under the SIL Open Font License a subset is a Modified Version, which may not use a Reserved Font Name, so the
  subsets carry a neutral name. Each keeps its original copyright and licence records (OFL 1.1, MIT for Hack, the
  Bitstream Vera licence for Fungal). The full fonts are at the official links on each library card.

Regenerate with `python tools/make_previews.py` (MN editions + DejaVu) and `python tools/make_extra_previews.py`
(the other free fonts).
