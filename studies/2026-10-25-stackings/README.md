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

NAMES (DICTO 2026-10-25): DICTO Chucky (−3/8 octahedral piece, 19 corners), DICTO Fang (5/24 octahedral piece, 7 corners), DICTO Triskelion Tetrahedron, short TT (5/24 tetrahedral piece, 16 corners).

CATALOGUE (catalogue.py → catalogue.txt/json; reach.py): no piece is wider than 1/√2, so a gap's sites are shaped only by the six layers
around it; the 16 h/c windows of those layers were walked exactly (all PASS, 0 FAIL): 21 combinatorial piece types over all stops and
stretches = every piece of every close-packed stacking. Congruence (congruent2.py, corner-distance fingerprints):
- TT (ABAC tet at 5/24) is congruent to the cubic octet's tet piece at 5/24 (a member of #51's sliding Samson family) — not a new shape.
- Fang (0.021824) and Chucky (0.705265) are congruent to nothing in AB or ABC; each volume is exactly the MEAN of the cubic and
  hexagonal pieces at that λ (Fang: octahedron 0.017459 / rhombohedron 0.026189; Chucky: rhombic dodecahedron 0.707107 / AB 24-corner
  0.703424). Hypothesis (half-and-half rule): an interface piece is half the cubic piece + half the hexagonal piece, glued on the
  site's mid-plane. To check exactly next.

HALF-AND-HALF (halves.py, halves_vol.py; 2026-10-25 evening): cut each octahedral piece of ABAC / ABCACB at the horizontal plane through
its site. VOLUME form holds at every λ tested (−3/8, −1/4, 0.1, 5/24, both stackings): each half has exactly (6 digits) the volume of the
matching half of the cubic (ABC) or hexagonal (AB) piece — hence Fang and Chucky are exact means. SHAPE form NOT confirmed: the halves'
corner-distance fingerprints mostly do not match (24 matched, 76 not), possibly a cutting artefact (extra points on the cut plane) or a
real difference. If shapes differ while volumes always match: a Cavalieri-type theorem — to investigate next session.

SLICES (slices.py → slices.txt): horizontal slices of the ABAC octahedral piece vs the cubic (ABC) and hexagonal (AB) pieces at the same
height from the site, λ = 5/24, 0.1, −1/4. At almost every height the slice AREA is the same in all three stackings (6 digits), even
where the polygons differ (e.g. 6 vs 8 vs 11 sides); some slices are congruent, many only equal in area; areas differ only near the far
ends (where ABC and AB themselves differ). Cavalieri-type law: slice areas ignore the stacking almost everywhere. Lead for next session:
find the reason (2D power diagram of each horizontal plane? weights w − (z − z_q)²) and prove it exactly.

EXACT HALF-PIECE RULE (exact_halves.py, exact_tets.py → exact_tets.txt; rational arithmetic, census engine; 16 windows × λ in every
stretch: −7/16, −1/4, −1/16, 1/300, 1/10, 1/4, 1/3):
- octahedral pieces: 0 failures — each is a top half + bottom half, each congruent to the matching half of the pure cubic (ABC) or pure
  hexagonal (AB) piece, chosen by the layer on that side;
- tetrahedral pieces: 208/208 — each is a whole pure piece, cubic or hexagonal, chosen by its NEAREST layer (rule B; first guess A
  had the layers swapped: 104/104).
THEOREM CANDIDATE: every piece of every close-packed stacking is built from the two pure stackings by this rule of halves.
To make airtight: congruence along whole stretches (corners affine in λ: same isometry at two λ per stretch ⇒ whole stretch; stops by
continuity); fuller literature check.
