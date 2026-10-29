# The HexOct square (book cover)

DICTO's idea (2026-10-29): a square cover for "HexOct: The Laws of Stacking" like the DICTO square, 6 × 6, letters H E X O C T, with the two HexOct tiles.

**Conclusion:** LED cover: upright DSEG14 Classic, letters 0.06 of the width, full black letter edges, letters at full brightness with a soft glow; H (always on the h-tile, hexagonal) yellow and C (always on the c-tile, cubic) purple, on teal, the pieces' colourway; other letters white. Status: final candidate, awaiting DICTO.

- Cyclic Latin square: cell (i, j) holds letter (i + j) mod 6 of HEXOCT. HEXOCT reads across the top and down the left; each letter appears once in every row and every column and runs in one diagonal stripe.
- Shapes: H, E, X on the h-tile and O, C, T on the c-tile (Hex | Oct). The tiles are the exact c-tile (from ABC) and h-tile (from AB) of #75 at λ = 1/10, built by tiles.py. Colours as in #75: tetrahedral pieces gold, octahedral halves violet. Same view and scale for both tiles.
- Letters (DICTO 10-29): an LED display like his font Timer (DS-Digital, LED Real): DSEG14 Classic (OFL, keshikan; DSEG-LICENSE.txt), 14 segments, lit segments glowing cool white on a thin dark edge, unlit segments faint. Italic (hexoct-square.png) and upright (hexoct-square-upright.png, LEDFONT=DSEG14Classic-Regular.ttf OUT=...) both made for DICTO. Tried and dropped: Trajan V-cut platinum, glowing dot-matrix, Righteous (too fat, not stepped), Baumans (after the B1NR logo).
- Matches picked out (DICTO): where the tile matches its letter, H on the h-tile and C on the c-tile, the tetrahedral pieces are teal instead of gold: two diagonal stripes, 12 cells.
- scripts/hexoct_square.py; run on dicto-big-brother (~/geom/bin/python) from scripts/.
