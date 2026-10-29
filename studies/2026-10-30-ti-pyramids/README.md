# TI Pyramids (DICTO, 2026-10-30)

**Idea (DICTO):** fill TI core (the truncated icosahedron, the midpoint cell of #76) with a combination of pentagonal and hexagonal pyramids.

**One-line conclusion.** TI is exactly 12 pentagonal + 20 hexagonal pyramids from its centre; its hexagonal pyramid carries the Cleo-Icos angle θ_I/2 on all six base edges, and the truncated tetrahedron's hexagonal pyramid carries the tetrahedron pyramid's α/2. Base to base they make a hexagonal bipyramid. Face to face, the four pyramids (TI 5 and 6, truncated tetrahedron 3 and 6) keep to their solids, and no face-to-face tiling uses a TI at all.
**Status:** done (exact, sympy; edge test complete to 5 solids per edge, closest miss 1.57°). Placement: ask DICTO (candidate: #76 v2 section, or a short note).

## Results (edge 1; data/pyramids.json)
| Pyramid | Count | Height | Volume | Side edge | Base-edge angle |
|---|---|---|---|---|---|
| TI pentagonal | 12 | √(1250+410√5)/20 = 2.32744 | 1.33477 | √(58+18√5)/4 = 2.47802 | 73.528° (cos² = (5+√5)/90) |
| TI hexagonal | 20 | √(42+18√5)/4 = 2.26728 | 3√(14+6√5)/8 = 1.96353 | 2.47802 | 69.095° = θ_I/2 on every edge (cos² = 1/2 − √5/6), the Cleo-Icos angle |
| truncated tetrahedron triangular | 4 | 5√6/12 = 1.02062 | 5√2/48 = 0.14731 | √22/4 = 1.17260 | 74.207° (cos² = 2/27) |
| truncated tetrahedron hexagonal | 4 | √6/4 = 0.61237 | 3√2/8 = 0.53033 | 1.17260 | 35.264° = α/2 on every edge, the tetrahedron pyramid's angle |

- Totals: TI (125+43√5)/4 = 55.2877 (12 × 1.33477 + 20 × 1.96353, exact); truncated tetrahedron 23√2/12.
- Why the angles: TI's hexagons lie in the face planes of the icosahedron of edge 3, the truncated tetrahedron's in those of the tetrahedron of edge 3; so each hexagonal pyramid is its Platonic face pyramid (Cleo-Icos, Q) of edge 3 with its three corners cut off.
- Hexagonal bipyramid (TI hexagon pyramid on the truncated tetrahedron's): height (√6 + √(42+18√5))/4 = 2.87966, volume 2.49386; the base-to-base meeting of the two midpoint cells of #76, as Q on the octahedron's pyramid in the octet.
- Side faces: both TI pyramids have the same side triangle (legs 2.47802, apex 23.28°), both truncated-tetrahedron pyramids another (legs 1.17260, apex 50.48°); the two solids' pyramids never share a side face.
- Round a side edge (apex to a corner): TI wedges 111.381° (pentagonal) and 124.309° (hexagonal); only 1 + 2 makes 360°. Truncated tetrahedron: 67.115° and 146.443°; only 1 + 2. So in a face-to-face tiling the pyramids round each apex make the whole solid (the #77 argument).
- Whole solids round an edge (dihedrals TI 6-6 θ_I = 138.19°, 5-6 142.62°; truncated tetrahedron 6-6 α = 70.53°, 3-6 π − α = 109.47°): the only combination of up to 5 that makes 360° is 2 × (3-6) + 2 × (6-6) of truncated tetrahedra alone; none contains a TI (closest miss 1.57°: TI 5-6 + 2 truncated-tetrahedron 3-6). Up to 5 is complete (smallest angle 70.5°).
- Hence: no face-to-face tiling of space by these four pyramids contains a TI pyramid; truncated tetrahedra alone do not fill space (known; with regular tetrahedra they make the quarter cubic honeycomb, whose pyramids join the tetrahedron's pyramid Q base to base). In four dimensions the two cells do fill: the bitruncated 600-cell (#76).

## Prior art (sources checked)
- Library (ask-library, 30 Oct): "truncated icosahedron face pyramids decomposition from the centre space filling truncated tetrahedron" → Richter-Gebert 2026; Wikipedia "Rhombic dodecahedron"; Sommerville 1922; Messer 1995; Kepler 1619 p. 271; Al-Siyabi–Koca–Koca 2020 p. 6 (two copies); Goldberg 1937 p. 1. None treats TI's face pyramids.
- Cutting any convex solid from its centre into face pyramids is classical; the quarter cubic honeycomb and the bitruncated 600-cell are classical (Wikipedia pages not re-read).
- New here: the angle identities of the two hexagonal pyramids (Cleo-Icos θ_I/2, Q's α/2), the bipyramid, and the face-to-face exclusion of TI's pyramids.

## Files
scripts/pyramids.py (exact data, edge test), scripts/figure.py (figures/ti-pyramids.png). Run on dicto-big-brother (~/kres-tmp/TI).
