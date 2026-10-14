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

## Step 3 (2026-10-16): exact, shapes, renders

`scripts/polar_exact.py` -> `data/polar-exact.txt`: every piece's corners exact (three exact planes each, Cramer in Q(√5)); each layer
one exact volume, sum − layer = 0 exactly in all six. Shapes: D→ID columns (7 pentagons incl. both stations' regular ones, 5 triangles
30-30-120°); ID→H* caps (regular pentagon, 5 quadrilaterals, 5 triangles 30-30-120°); H*→PD low pyramids on a regular hexagon (side edge
1.07 × base; not FUJI-family); PD→I irregular 5-corner wedges (incl. 30-60-90° triangles); I→RT Kepler's pyramids; RT→D roofs on the
rhombi, each ridge one dodecahedron edge, end triangles 54-72-54° (classical D/RT edge relation). Renders `renders/` (`scripts/render_polar.html`).

## Step 4: the tight nest (2026-10-16)

DICTO asked for a more even nest. The faithful polar version leaves two ends loose, because the original cycle's closure forces the outer dodecahedron to be the inner one × φ³. The triacontahedron could grow ×1.894 before touching the outer dodecahedron, and the inner dodecahedron ×1.232 before touching the icosidodecahedron. The four middle stations already touch, so they stay as they are. `polar_tight.py` tightens both ends (inner ×1.232241, outer ×0.527864):

- The outer layer drops from 25.23 to 1.915, and the closure goes from φ³ linear to 1.814635.
- The inradii are now 0.495, 0.567, 0.623, 0.653, 0.714, 0.764, 0.898.
- Each layer still has one kind of piece, and each layer sum equals the layer volume.
- The inner layer becomes 12 near-antiprism columns (10 corners, 2 pentagons, 10 triangles).
- The outer layer becomes 30 wedges (6 corners, a rhombus and 6 triangles) on the rhombi. Each wedge's ridge is a dodecahedron edge, and the 12 five-fold tips of the triacontahedron now touch the face centres of the outer dodecahedron.

The originals are unchanged: `reversed-chain.json`, `polar-pieces.json`, `polar-render.json` and `renders/polar-*.png`. The tight versions are named `*-tight*`: `data/polar-tight.txt`, `reversed-chain-tight.json`, `polar-tight-pieces.*`, `polar-tight-render.json` and `renders/polar-tight-*.png` (`node shoot_polar.mjs tight`). This step is not exact yet; the numbers above are floats.
