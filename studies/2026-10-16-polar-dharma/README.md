# Spheres of Dharma turned inside out: polar reciprocation (DICTO's 2026-10-13 idea; step 1, 2026-10-16)

After the flip test (studies/2026-10-16-flip-test: no skin turns over into a closed shell), the inside-out version by duality: each
station of the Ritsudō cycle replaced by its polar in the unit sphere; nesting reverses. `scripts/polar.py` (exact corners in Q(√5),
snapped from data/dharma_cycle.json; poles exact) -> `data/polar-step1.txt`, `data/reversed-chain.json`.

Reversed chain, inside to outside: dodecahedron ⊂ icosidodecahedron ⊂ dual of the Hecatodihedron (102 corners, 80 faces) ⊂ pentakis
dodecahedron ⊂ icosahedron ⊂ rhombic triacontahedron ⊂ dodecahedron φ³ larger. Closure exact: volume ratio 38 + 17√5 = φ⁹. Touching
carries over by duality (e.g. ID's 30 corners on the Hecatodihedron-dual's faces; the icosahedron's 12 corners are the triacontahedron's
5-fold corners). Layer volumes exact (see data). Sizes invert: Dharma's thick inner layer becomes the thick outer one.

Next (step 2): exact pieces for each layer; reciprocation does not carry Dharma's pieces over.

## Step 2 (2026-10-16): one kind of piece per layer

Each layer A ⊂ B cut into one piece per face F of A, cone(F) ∩ B ∩ {beyond F} (convex by construction; the Kion construction of #29);
faces of A lying on B's surface give nothing. `scripts/polar_pieces.py` -> `data/polar-step2.txt`, `data/polar-pieces.json`.

| Layer | Pieces | Each piece |
|---|---|---|
| D -> ID | 12 | 15 corners; 7 pentagons, 5 triangles |
| ID -> Hecatodihedron-dual | 12 (ID's 20 triangles lie on the outer surface) | 11 corners; 1 pentagon, 5 quadrilaterals, 5 triangles |
| Hecatodihedron-dual -> pentakis D | 20 (60 of 80 faces lie on the outer surface) | hexagonal pyramid |
| pentakis D -> I | 60 | 5 corners, 6 triangles (triangular bipyramid) |
| I -> RT | 20 | tetrahedron (Kepler's pyramids) |
| RT -> D(φ³) | 30 | 8 corners; 5 quadrilaterals, 2 triangles |

Every layer is ONE kind of piece (Dharma needs 2-3 in some); 154 pieces round the inner dodecahedron; sums match the layers (1e-9,
floats). No two neighbours fuse without a dent. Next: exact volumes, identify the shapes, renders, prior-art check.
