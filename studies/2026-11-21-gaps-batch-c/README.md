# Gaps batch C (21 November 2026): R14 / L4, L13, L36

For DICTO, not for publication. From the gap study (studies/2026-11-21-gap-study, items marked CLOSABLE NOW). Nothing was published; concordance.json and the paper folders are untouched. Computed on the compute host (scripts run in the foreground, each well under 280 s); logs end `FINAL ok`.

Files: `scripts/q5.py` (exact Q(√5) arithmetic with fractions; exact facets and vertices of convex polytopes, every inequality re-checked exactly), `scripts/item1_o_rti_stations.py`, `scripts/item2_reuleaux_largest_width.py`, `scripts/item3_ekp_vs_aflow.py`; `logs/item1.log`, `logs/item2.log`, `logs/item3.log`; `data/ref-floats-35.json` (ID, O, rTI, TI of #35, from studies/2026-10-16-progenitors/data/full-cycle.json, used to identify the exact solids corner for corner); `data/aflow_A12B_cP13_200_j_b-001.cif` (the public AFLOW CIF).

## Item 1 (R14 / L4): the loose step O ⊂ rTI of #35 (Vajrayana)

**Question.** Does any golden-cut station S of #88 / #91 fit between the DICTO Ogdoecontahedron O and the rectified truncated icosahedron rTI, O ⊂ λS ⊂ rTI for some scale λ (common centre and axes, as for every station of the cycle)? Does one touch both, closing the step as the DICTO Metaxyhexecontahedron closes RT ⊂ I·φ³?

**Method.** O built exactly as #91 Theorem 5, OG = H(μ_TI) ∩ φ²D*, and rTI as the edge midpoints of the Dharma TI; both placed in the Dharma frame and matched corner for corner with #35's data (102/102, 90/90). For each station: λ_min = least λ with O ⊂ λS (max of n·a/d over corners of O and faces of S), λ_max = largest λ with λS ⊂ rTI; it fits exactly when λ_min ≤ λ_max, and closes the step when λ_min = λ_max. All in Q(√5), exact. For the stations without icosahedral symmetry (the golden cuts of the cube, tetrahedron, octahedron), a bound valid in every position, rotated or moved: O ⊂ S ⊂ rTI forces (R_S/r_S)² ≤ (R_rTI/r_O)² = 243 − 108√5 ≈ 1.5047.

**Controls.** Reproduced #35 Table 1: ID ⊂ O tight (30 corners), rTI ⊂ TI tight (90), O ⊂ rTI loose (factor (195 + 66√5)/361 ≈ 0.9490; room 13/3 − 22√5/15 ≈ 1.0538). λ test: O itself and rTI itself fit (pass); ID and the icosahedron do not (fail).

**Result (D·I·C·T·O order).**

| Station | λ_min (O ⊂ λS) | λ_max (λS ⊂ rTI) | Fits |
|---|---|---|---|
| Greater Golden Cut Dodecahedron | (15 + 27√5)/76 ≈ 0.9918 | (9 + 45√5)/124 ≈ 0.8841 | no |
| Lesser Golden Cut Dodecahedron | (15 + 27√5)/76 ≈ 0.9918 | (−3 + 9√5)/20 ≈ 0.8562 | no |
| Greater Golden Cut Icosahedron | (405 + 159√5)/836 ≈ 0.9097 | 9/10 | no (narrowly) |
| Lesser Golden Cut Icosahedron | (165 − 45√5)/76 ≈ 0.8471 | (−90 + 63√5)/58 ≈ 0.8771 | **yes, loosely** |
| Lesser Golden OG (#91) | (165 + 69√5)/380 ≈ 0.8402 | (11 + 3√5)/20 ≈ 0.8854 | **yes, loosely** |
| Greater Golden OG (#91) | (1 + √5)/4 = φ/2, 90 corners of O touch | (135 − 53√5)/20 ≈ 0.8244 | **yes, loosely** |
| Greater / Lesser Golden Cut Cube | radius bound fails ((R/r)² ≈ 2.09, 2.28) | | no, in any position |
| Greater / Lesser Golden Cut Tetrahedron | radius bound fails (3.33, 4.20) | | no, in any position |
| Icosaxes / Unborn Axes | radius bound fails (1.58, 1.80) | | no, in any position |

**Verdict.** Three golden stations fit inside the step, the Lesser Golden Cut Icosahedron and DICTO's Lesser and Greater Golden OG; none touches both sides (λ_min < λ_max strictly), so no golden-cut station closes O ⊂ rTI. The closest to a closing solid is the Greater Golden OG: at λ = φ/2 it holds O tightly with 90 corners of O on its faces, and it sits loosely in rTI. The step stays loose; it can now be filled by a golden station but not closed by one.

**Proposed home.** #35 (Vajrayana), next version, open point "the loose step O ⊂ rTI": one sentence and the table. Cite #88, #91.

**LEADS.** (a) The Golden OGs belong to the one-parameter family Q(μ, φ²) of #91; λ_min(μ) and λ_max(μ) are both exact and continuous in μ, so a member touching O and rTI at once may exist (solve λ_min = λ_max exactly; a candidate closing solid in OG's own family). (b) O ⊂ (φ/2)·Greater Golden OG is tight with 90 contacts: check whether that layer is filled by one kind of piece, as M's layers are. (c) The Greater Golden Cut Icosahedron misses by a hair (λ_max = 9/10 exactly against 0.9097): no action, recorded as near miss.

## Item 2 (L13): #45 Conjecture 1, the largest width of the Reuleaux Platonic solids

**Question.** For the cube, octahedron, dodecahedron and icosahedron, is the largest width of DICTO's body B = ∩ B(v, D) the face-axis width 2(√(3/4 + r²) − r) of #45's main theorem?

**Method.** B is centrally symmetric, so w(u) = h(u) + h(−u) = 2h(u), and the largest width is 2·max |x| over B. The maximum of the convex |x|² lies on the boundary, at a point on one, two, or three or more spheres. (1) On one sphere the only local maximum is x = v + D·v/|v|, not in B: no maximum inside a face. (2) On a circle of two spheres |x|² = D² − R² + 2x·v_i, whose only interior maximum is x = c + r·c/|c| (antipodal pairs: the circle misses B, since a point on it would need x·v ≥ 0 for every corner and its opposite). (3) Points on three spheres lie on the line through 0 along (v_j − v_i) × (v_k − v_i), two roots of opposite sign. Exact lemma: for x on the sphere of v_i, x lies in the ball of v_m exactly when x·(v_m − v_i) ≥ 0; with the forms above its sign is a sign in Q(√5), so membership and ties are exact. The finitely many candidate values are compared at 60 digits.

**Controls.** The face-axis values reproduce #45's widths.log to all 12 digits (1.248391589161; 1.110988655456). Failing control: without the membership test, the cube's arc maxima reach |x| ≈ 1.3657, far above 0.6242: the membership test is what bounds the answer.

**Result.** In all four bodies, every candidate in B is a face-axis point (dodecahedron 12 points, each on 5 spheres; icosahedron 20 on 3; cube 6 on 4; octahedron 8 on 3); no arc maximum lies in B. So max |x| is attained exactly on the face axes, and equals the main theorem's value to 40 digits: largest width (√30 − √3)/3 ≈ 1.248392 for the cube and octahedron, (√(50 + 2√5) − √(5 + 2√5))/√15 ≈ 1.110989 for the dodecahedron and icosahedron.

**Verdict.** Conjecture 1 is PROVED for the cube, octahedron, dodecahedron and icosahedron, the part that #45 calls new. The tetrahedron part (√3 − √2/2) is the classical Reuleaux tetrahedron value and was not re-proved here (B is not centrally symmetric there; its largest width is the diameter of B).

**Proposed home.** #45 (The Reuleaux Platonic Solids), next version: Conjecture 1 becomes Theorem 2 for the four bodies, with the proof above in a paragraph. By-product for the same version: the vertices of B are exactly the face-axis points, one per face of the solid (exact), which supports the observed face pattern.

**LEADS.** (a) The tetrahedron: its largest width = diam(B); the same candidate method applied to pairs of boundary points would prove the classical value from scratch if wanted. (b) The by-product (vertices of B = face points) plus arcs along edges could turn #45's "observed numerically" face-pattern statement into an exact one.

## Item 3 (L36): #8, the 1b + 12j point set in crystal-structure databases

**Question.** Is the EKP cell's node set (Pm-3, No. 200; 1b and 12j (0, y, z), y = 1/(2φ), z = 1/(2φ²)) in a free prototype database?

**Sources checked (21 November 2026; topics only).**
1. AFLOW Encyclopedia of Crystallographic Prototypes: web search "AFLOW prototype encyclopedia cP13 Pm-3 200 1b 12j", and "cP13" "Pm-3" prototype structure icosahedron 12j; entry page aflow.org/p/7KWV and its CIF (data/). The Pearson-symbol index page (prototype-encyclopedia/pearson_symbol.html) returned 404; the cubic-lattice index was fetched but lists no group-200 labels in its text.
2. Crystallography Open Database (COD), REST query: space group "P m -3", experimental entries: 70 entries; none has a 13-site cell of the 1b + 12j kind (the nearest, Ba Cu~5.7 (Se,Te)~7, has about 7 anions, which no single 12j site can carry).
3. Bilbao Crystallographic Server, WYCKPOS for group 200: not reachable (certificate error on cryst.ehu.es; protocol error on cryst.ehu.eus). The site letters were taken from the AFLOW CIF (symmetry operators included) and the International Tables, as #8 does.
Not checked: ICSD (paid), Materials Project and OQMD (account/API), Pearson's Crystal Data (paid).

**Result.** FOUND as a Wyckoff set: AFLOW prototype **A12B_cP13_200_j_b-001**, "Theoretical Cubic LiH12 Structure" (Li 1b, H 12j; a = 2.8013 Å, y = 0.24009, z = 0.64734; reference A. K. Verma and P. Modak, Physica B 728, 418355 (2026)). NOT the EKP parameters: under every setting change that keeps 1b and 12j (sign changes, y ↔ z, lattice translations) the LiH12 parameters reduce to (0.24009, 0.35266) against EKP's (0.19098, 0.30902); its 12 points about 1a are a distorted cluster (ratio 0.6808 against 1/φ = 0.6180; 30 shortest distances 0.441 to 0.480 a), not a regular icosahedron (script item3, controls pass and fail).

**Verdict.** The Wyckoff set 1b + 12j of Pm-3 is known (theoretical LiH12, AFLOW, 2026); the EKP cell with the golden parameters, a regular icosahedron, was not found in the sources checked. #8's "not yet checked: structure databases" is now checked for the free ones.

**Proposed home.** #8 (The Euclid–Kepler–Pacioli Cell), next version, prior-art paragraph: replace "Not yet checked: structure databases (Bilbao, ICSD)" by the AFLOW entry (same sites, other parameters, theoretical LiH12, cite Verma and Modak 2026 and the AFLOW library) and the list of sources checked.

**LEADS.** (a) The EKP cell is the regular-icosahedron point of the LiH12 prototype's two-parameter family: one line in #8. (b) ICSD, Materials Project and OQMD remain unchecked (paid or account-only); Bilbao to retry when the site answers.
