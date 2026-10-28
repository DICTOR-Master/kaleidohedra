# The HexOct square (book cover)

DICTO's idea (2026-10-29): a square cover for "HexOct: The Laws of Stacking" like the DICTO square, 6 × 6, letters H E X O C T, with the two HexOct tiles.

**Conclusion:** first version made, hexoct-square.png (1800 px). Status: shown to DICTO, awaiting his read.

- Cyclic Latin square: cell (i, j) holds letter (i + j) mod 6 of HEXOCT. HEXOCT reads across the top and down the left; each letter appears once in every row and every column and runs in one diagonal stripe.
- Shapes: H, E, X on the h-tile and O, C, T on the c-tile (Hex | Oct). The tiles are the exact c-tile (from ABC) and h-tile (from AB) of #75 at λ = 1/10, built by tiles.py. Colours as in #75: tetrahedral pieces gold, octahedral halves violet. Same view and scale for both tiles.
- Letters: Trajan-style (Cinzel, OFL), V-cut and gilded with platinum leaf, as in the DICTO square (studies/2026-10-22-dicto-square). No outer lettering.
- scripts/hexoct_square.py; run on dicto-big-brother (~/geom/bin/python) from scripts/.
