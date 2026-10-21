# The DICTO square

DICTO's idea (2026-10-22): a word square like SATOR AREPO TENET OPERA ROTAS, with a twist, built from the five Platonic solids of DICTO's emblem key D-I-C-T-O (Dodecahedron, Icosahedron, Cube, Tetrahedron, Octahedron).

- Cyclic Latin square: cell (i, j) holds letter (i + j) mod 5. DICTO reads across the top and down the left; each solid appears once in every row and every column; each solid runs in one diagonal stripe (the long anti-diagonal is all octahedra).
- Checked by exhaustive search: 6 squares have DICTO on the top row and left column with every solid once per row and column; NONE also has the SATOR property (reading DICTO backwards from the bottom-right corner). SATOR manages it only because letters repeat.
- dicto_square.py -> dicto-square.png (1800 px): solids on a square lattice (spacing 1), each scaled to the same circumsphere (radius 0.44); #18 colours.
