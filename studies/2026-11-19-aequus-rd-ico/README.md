# A fair 32-face die from the rhombic dodecahedron and the icosahedron, with two depths (19 November 2026)

**Verdict: found, and confirmed to 100 digits (exact.log); no closed form found.** With the RD's 12 faces at depth 1, the icosahedron's 8 cube-diagonal faces at m1 = 1.002759250954 and its 12 other faces at m2 = 1.010663942602, every one of the 32 faces subtends 4π/32 (largest error 4.4e-11). It is the only solution found in 0.8 ≤ m1, m2 ≤ 1.3.

**100 digits** (scripts/rd_ico_exact.py, Newton on the two shares with corners by Cramer's rule): m1 = 1.0027592509652673651138588224943292169120…, m2 = 1.0106639425964276013947211797925550524897…; all 32 faces at 4π/32 to 2e-111; 60 corners. No integer polynomial of degree ≤ 8 (coefficients ≤ 10⁶) and no identify() form in √2, √3, √5, √6, √10, √15 for m1, m2, m1², m2². Unlike the Equanimity dice, it has no regular face whose corner angle fixes the cut, which may be why.

- **Why two depths:** under the shared pyritohedral group the icosahedron's 20 face directions split 8 + 12, so one depth cannot make all faces fair (Equanimity §2); the control confirms that the two shares differ on the one-depth line.
- **Shape:** 60 corners; the RD faces are pentagons and all 20 icosahedron faces are hexagons (12 pentagons, 20 hexagons, the counts of the truncated icosahedron, here with pyritohedral symmetry only); r/R = 0.8836.
- **Method:** half-space intersection (scipy), solid angle by Van Oosterom–Strackee (1983) on a fan from the face centre, as in Equanimity; root by fsolve from an 11 × 11 grid of starts.
- **Script:** scripts/rd_ico_fair.py (run with a numpy/scipy Python). Log: run1.log.

## The Vacuus of D191 (19 November 2026)

**Verdict: no hidden polygon.** Unlike the ten Equanimity dice with regular faces, D191 hides no regular polygon in its Vacuus: no face is regular, and at 100 digits no corner angle of any face's spherical polygon and no angle of any sloping plate is a rational multiple of π (PSLQ, coefficients ≤ 500). It is like the two Equanimity dice without regular faces (cube ∩ dodecahedron, rhombic dodecahedron ∩ dodecahedron). **Girard check: passed**, the excess is 4π/32 on all 32 faces (to 1e-80).

- **Plates:** 90 (one per edge). 6 lie on mirrors of Th (the coordinate planes): the 6 edges where two of the 12 icosahedron faces meet across a coordinate axis, each crossed by a 2-fold axis. The other 84 slope. No plate lies on a mirror of the full cube or icosahedron groups other than these. No rhombic dodecahedron face and no cube-diagonal face has a plate on a mirror.
- **Faces (side lengths, 100-digit corners in data/verts-rdi.json):** the 12 pentagons have sides 0.366677, 0.595283, 0.645233 (symmetric about the mirror through the face normal) and corner angles 0.522786π (twice), 0.681461π (twice), 0.716505π. The 8 hexagons on the cube's diagonals have alternating sides 0.265888 and 0.595283 and alternating corner angles 0.801328π and 0.573672π. The 12 other hexagons have sides 0.265888, 0.366677, 0.645233, 0.664664 and corner angles 0.744867π, 0.675885π, 0.641748π (each twice). All irrational to PSLQ.
- **What the Vacuus shows instead:** the 8 hexagons on the 3-fold axes turn without a mirror. Their plates fan round the axis in three pairs, and each pair of neighbouring corners sums to exactly 11π/8. That follows from Girard and the 3-fold turn alone (3 × 11π/8 − 4π = π/8 = 4π/32); neither corner is rational by itself. The only rational plate angles are those of the 6 mirror plates to the fixed symmetry axes (π/3, π/4, π/5, 2π/5), which belong to the coordinate planes, not to this die.
- **Dehn invariant: nonzero** (4 distinct dihedral angles, 3 independent mod π, largest coefficient sum 14.3; the screen of study 2026-11-19-dehn-words, calibrated there, 80 digits).
- **Method:** the root from scripts/rd_ico_exact.py refined again to 1e-95. Solid angles by Van Oosterom and Strackee (1983). Corner angles between consecutive plates, checked by Girard's theorem. Rational tests by the PSLQ algorithm of Ferguson and Bailey (mpmath), as in study 2026-11-18-fair-32-die (scripts/corners.py). Plates on mirrors were tested against the 3 coordinate planes, the 9 mirrors of the cube and the 15 of the icosahedron. Plate angles were tested against every rotation axis of both groups and the plane through the face's normal and either end of its edge (the angle of Equanimity Theorem 6).
- **Scripts:** scripts/vacuus_rdi.py (log data/vacuus.log, FINAL ok; it also writes data/verts-rdi.json and the catalogue picture input data/aequus-32-rdi.json). scripts/fig_vacuus_d191.py (log data/fig.log, FINAL ok).
- **Figure:** figures/vacuus-d191.png, drawn as a panel of Equanimity's Figure 2. Each plate is drawn as the triangle from the centre to its edge, with a see-through shell. Slate marks the 84 sloping plates and pale sand the 6 plates on mirrors of Th. Colours are labels only.

## In the DICTOnary (19 November 2026)

Added as D191, Aequus 32 (rhombic dodecahedron ∩ icosahedron), in the DICTOnary's catalogue (both copies). The picture was drawn with the atoms renderer of study 2026-11-17-atoms-missing-2, unchanged, from data/aequus-32-rdi.json.

LEADS: exact closed form (identify m1, m2 beyond degree 8); whether the die is fair under the face-areas model too; whether its 12 + 8 + 12 faces are all distinct shapes (the side lengths above say yes: the three kinds differ).
