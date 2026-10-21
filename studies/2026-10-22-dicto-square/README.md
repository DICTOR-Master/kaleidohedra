# The DICTO square

DICTO's idea (2026-10-22): a word square like SATOR AREPO TENET OPERA ROTAS, with a twist, built from the five Platonic solids of DICTO's emblem key D-I-C-T-O (Dodecahedron, Icosahedron, Cube, Tetrahedron, Octahedron).

- Cyclic Latin square: cell (i, j) holds letter (i + j) mod 5. DICTO reads across the top and down the left; each solid appears once in every row and every column; each solid runs in one diagonal stripe (the long anti-diagonal is all octahedra).
- Checked by exhaustive search: 6 squares have DICTO on the top row and left column with every solid once per row and column; NONE also has the SATOR property (reading DICTO backwards from the bottom-right corner). SATOR manages it only because letters repeat.
- dicto_square.py -> dicto-square.png (1800 px): solids on a square lattice (spacing 1), each scaled to the same circumsphere (radius 0.44), seen straight on in true grid squares. Colours of Plato's elements: fire tetrahedron red, air octahedron yellow, water icosahedron blue, earth cube green, the dodecahedron (the whole, aether) violet. Each form carries its Roman (Trajan-style) initial, V-cut into the form and gilded with platinum leaf (lit wall and shadowed wall), set in Cinzel (OFL, Cinzel.ttf + OFL-Cinzel.txt). No outer lettering (DICTO).

## Emblem, forms iteration (DICTO 2026-10-22)
emblem_forms.py -> dicto-emblem-forms.png; STAR=1 -> dicto-emblem-forms-star.png. The emblem's gold ring with each mark replaced by its form and V-cut platinum initial, at the mark's measured angle (D 86.6°, I 19.8°, C −47.0°, T −124.7°, O 162.4°) and distance (0.625 of the ring radius) from dicto-logo.png. Variant: five golden Penrose rhombi (fat, 72° corners at the centre) V-cut and laid with platinum leaf, one pointing towards each form. An additional iteration; the emblem itself is unchanged.
