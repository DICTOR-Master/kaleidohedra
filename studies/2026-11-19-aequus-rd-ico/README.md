# A fair 32-face die from the rhombic dodecahedron and the icosahedron, with two depths (19 November 2026)

**Verdict: found, and confirmed to 100 digits (exact.log); no closed form found.** With the RD's 12 faces at depth 1, the icosahedron's 8 cube-diagonal faces at m1 = 1.002759250954 and its 12 other faces at m2 = 1.010663942602, every one of the 32 faces subtends 4π/32 (largest error 4.4e-11). It is the only solution found in 0.8 ≤ m1, m2 ≤ 1.3.

**100 digits** (scripts/rd_ico_exact.py, Newton on the two shares with corners by Cramer's rule): m1 = 1.0027592509652673651138588224943292169120…, m2 = 1.0106639425964276013947211797925550524897…; all 32 faces at 4π/32 to 2e-111; 60 corners. No integer polynomial of degree ≤ 8 (coefficients ≤ 10⁶) and no identify() form in √2, √3, √5, √6, √10, √15 for m1, m2, m1², m2². Unlike the Equanimity dice, it has no regular face whose corner angle fixes the cut, which may be why.

- **Why two depths:** under the shared pyritohedral group the icosahedron's 20 face directions split 8 + 12, so one depth cannot make all faces fair (Equanimity §2); the control confirms that the two shares differ on the one-depth line.
- **Shape:** 60 corners; the RD faces are pentagons and all 20 icosahedron faces are hexagons (12 pentagons, 20 hexagons, the counts of the truncated icosahedron, here with pyritohedral symmetry only); r/R = 0.8836.
- **Method:** half-space intersection (scipy), solid angle by Van Oosterom–Strackee (1983) on a fan from the face centre, as in Equanimity; root by fsolve from an 11 × 11 grid of starts.
- **Script:** scripts/rd_ico_fair.py (run with a numpy/scipy Python). Log: run1.log.

LEADS: exact closed form (100-digit refine, then identify m1, m2); whether the die is fair under the face-areas model too; Dehn invariant; whether its 12 + 8 + 12 faces are all distinct shapes; name and number (DICTO's choice).
