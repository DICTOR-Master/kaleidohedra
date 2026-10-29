# The HexOct square (book cover)

DICTO's idea (2026-10-29): a square cover for "HexOct: The Laws of Stacking" like the DICTO square, 6 × 6, letters H E X O C T, with the two HexOct tiles.

**Conclusion:** version 2 made, hexoct-square.png (1800 px): B1NR-style letters, matching tiles in teal. Status: shown to DICTO, awaiting his read.

- Cyclic Latin square: cell (i, j) holds letter (i + j) mod 6 of HEXOCT. HEXOCT reads across the top and down the left; each letter appears once in every row and every column and runs in one diagonal stripe.
- Shapes: H, E, X on the h-tile and O, C, T on the c-tile (Hex | Oct). The tiles are the exact c-tile (from ABC) and h-tile (from AB) of #75 at λ = 1/10, built by tiles.py. Colours as in #75: tetrahedral pieces gold, octahedral halves violet. Same view and scale for both tiles.
- Letters (DICTO 10-29: not classic DICTO Trajan; "a bit sixties distorted script like B1NR logo", the logo centred on the spherical security-ring icosidodecahedron, Flickr album B1NR Sculptures, not the zip-tie version): heavy rounded letters in Righteous (OFL, Righteous-Regular.ttf + OFL-Righteous.txt), white with a thick black outline, swollen by a gentle barrel warp. Tried and dropped: Trajan V-cut platinum (v1), glowing 5 × 7 dot-matrix (hid the tiles).
- Matches picked out (DICTO): where the tile matches its letter, H on the h-tile and C on the c-tile, the tetrahedral pieces are teal instead of gold: two diagonal stripes, 12 cells.
- scripts/hexoct_square.py; run on dicto-big-brother (~/geom/bin/python) from scripts/.
