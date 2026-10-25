# Lead 1: the weight walk on other close-packed stackings (2026-10-25, DICTO "lets go with 1")
scripts/stackings.py builds the octahedral + tetrahedral holes of any stacking word (A/B/C) and runs the census engine (exact).
Checks: ABC reproduces the cubic octet walk (−3/8 rhombic dodecahedra, −1/8 octet, 3/8 cubes), AB the twinned walk (−11/24, −1/8, 5/24, 3/8);
stackings-checks.txt 87 PASS 0 FAIL. New: ABAC (double hexagonal, hchc) and ABCACB (6H, hcchcc): stackings-new.txt 206 PASS 0 FAIL.
Both new stackings have the stops −3/8, −1/8, 5/24, 3/8 and mix the cubic and twinned pieces (cubes beside Blockheads at 3/8,
Ian Durys at 5/24), plus three pieces neither pure stacking has:
- −3/8 octahedral piece: 19 corners, faces 3 triangles, 3 squares, 6 pentagons, one 9-gon (bonds 10 oct + 3 tet);
- 5/24 octahedral piece: 7 corners, 4 triangles + 3 squares (bonds 7 tet);
- 5/24 tetrahedral piece: 16 corners, 4 triangles + 6 hexagons (bonds 4 oct + 6 tet).
ABCACB adds nothing beyond ABAC's pieces and the pure cubic ones: hypothesis — each piece is fixed by the local h/c pattern of the
layers round it (Jagodzinski symbols). Test next on 9R (ABACACBCB, hhc).

9R (ABACACBCB, hhc): stackings-9r.txt 183 PASS 0 FAIL; stops −3/8, −1/8, 5/24, 3/8. Every piece is one already met at the same λ in AB, ABC
or ABAC (its 24-corner octahedral piece at −3/8, faces 6 tri + 6 hex + 2 nonagons, is AB's piece on the stretch (−11/24, −1/8)):
NO NEW PIECES — the local h/c rule survives its first test. Volumes of the three ABAC pieces (floats): 0.705265, 0.021824, 0.344824.
Render: new-pieces.png (export_new.py, render_new.py).
