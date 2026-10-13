# AXE, CLEO and FUJI: the gap pieces of the icosahedron (paper draft, DICTO, 2026-10-14)

Draft for DICTO's review; not released. Working title; the title is DICTO's.

- `paper/paper.md`: the text. `paper/build_house.py` makes `paper-house.html` in the house style, and `paper/print.mjs` prints
  `paper/axe-cleo-fuji.pdf` (run both on dicto-node).
- `paper/figures/`: figures 1, 3–6 and 9 composed from the DICTO Icosa-13 and icosahedral-networks study renders; 2, 7 and 8 from
  the Chain of Karma kit, the In-betweens paper and the Chain of Karma study.
- `scripts/checks.py`: recomputes every volume, angle and count in the paper from studies/2026-10-10-icosa-13/data;
  writes `CHECKS.json` (0 failures) and `nets/pieces.json`.
- `nets/`: `nets.py` (adapted from the In-betweens nets), `axe-cleo-fuji-nets.pdf` (A4, 45 mm per unit: AXE, FUJI, CLEO,
  J11, dodecahedron), `nets-checks.json` (all ok).

DICTO · dictospheres.com
