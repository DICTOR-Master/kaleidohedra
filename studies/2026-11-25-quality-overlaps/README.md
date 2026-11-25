# Where the five qualities overlap: Vacuus, Resonus, Aequus, Tacitus, Sphericus (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-quality-overlaps · with Claude (Anthropic).

> **Status box.** Study note, not published. Checks, all FINAL ok: `scripts/aequi_overlaps.py` (logs/qo-aequi.log, 15 192 dice),
> `scripts/cat_overlaps.py` (logs/qo-cat.log: the 163 polyhedra, 9 compounds, 11 root systems), `scripts/post_aequi.py`,
> `scripts/post_join.py`, `scripts/post_bigger_groups.py` (logs/qo-post, qo-join, qo-big), `scripts/table28.py`. All runs on the
> compute hosts at low priority, each under 5 minutes. Nothing running. Every item below ends PROVED POSSIBLE, PROVED IMPOSSIBLE
> (with its exact scope) or OPEN (with its blocker).

DICTO's five qualities (his names): **Vacuus** (the plates through the centre O and each edge, #110 §2), **Resonus** (the planes
through O parallel to the faces), **Aequus** (a fair die: equal face solid angles about O, that is, equal Vacuus regions),
**Tacitus** (the face directions silence the harmonics beyond what symmetry forces; study 2026-11-25-tacitus), **Sphericus** (the
network of great circles of a plate set and its crossings; working measures of study 2026-11-25-plate-harmony, exact definition
still to be fixed with DICTO). Mirrors are the mirrors of the full symmetry group. The shapes are polyhedra and polytopes.

## Conclusion

1. **Resonus = Vacuus comes from root systems (Theorem 2, PROVED).** For each root system A2–A5, D4, D5, E6, E7, E8, H3, H4 the
   polytope cut out by the planes x·α ≤ 1 (α a root) has its Resonus equal to its Vacuus: both are the root mirrors. In 3D these
   are the rhombic dodecahedron (A3) and the rhombic triacontahedron (H3); in 4D the 24-cell (D4) and the 120-cell (H4), already
   known, and **one new 4D example: the polar of the runcinated 5-cell (A4)**, with 10 = 10 planes. For A, D and E these
   polytopes are the Voronoi cells of the root lattices (Conway and Sloane, cited, not opened).
2. **Resonus = Vacuus = mirrors (Theorem 3, PROVED)** exactly when the lattice symmetry adds no mirror: the rhombic
   triacontahedron, the 120-cell, the A4 polytope above (and A_n for n ≥ 4, E7, E8). The rhombic dodecahedron and the 24-cell
   miss it (their mirrors are 9 and 24).
3. **Two impossibility theorems.** A polyhedron whose Vacuus lies inside its mirrors is face-transitive (Theorem 5); one whose
   Resonus lies inside its mirrors is centrally symmetric (Theorem 6). So "Vacuus = mirrors" is impossible for all 15 192
   catalogued Aequi, and "Resonus = mirrors" for every polyhedron without a centre.
4. **Harmonious Sphericus is rare (Theorem 7, PROVED).** It happens only for three perpendicular planes. A fair die with a
   harmonious Resonus is the cube, and one with a harmonious Vacuus is an octahedron whose three diagonals are perpendicular
   and bisect each other.
5. **The Aequi.** 6 253 of the 15 192 dice share a Resonus plane with their Vacuus (exact; at most 6 285). The largest overlap
   is 30 planes. Two dice have their whole Resonus inside their Vacuus: Aequus RDRT-24 and one T die. These are the first 3D
   cases of the 4D permutohedron's "Resonus ⊂ Vacuus". One die has Resonus = mirrors: Aequus CRD-18. Nine dice are both
   Tacitus and simplicial.

## 1. The 28 polyhedra with shared planes (Part 1)

Source: the exact catalogue of study 2026-11-24-vacuus-resonus-catalogue (Theorem B there: a plane through O is in both exactly
when it holds an edge and is parallel to a face). Table: `data/table28.md` (made by `scripts/table28.py` from that study's
exact data). The column "each shared plane" gives how many edges of P lie in the plane and the side counts of the faces
parallel to it ("3+3" means two opposite triangles; "3 alone" means a triangle without an opposite face).

| polyhedron | family | symmetry | shared | of them mirrors | mechanism |
|---|---|---|---|---|---|
| rhombic dodecahedron | Catalan | Oh | **6** (R = V = 6) | 6 | 4 edges per plane, rhombi 4+4 |
| rhombic triacontahedron | Catalan | Ih | **15** (R = V = 15) | 15 | 4 edges per plane, rhombi 4+4 |
| cuboctahedron | Archimedean | Oh | 4 (all 4 Vacuus planes) | 0 | the 4 hexagonal equators (6 edges), triangles 3+3 |
| icosidodecahedron | Archimedean | Ih | 6 (all 6 Vacuus planes) | 0 | the 6 decagonal equators (10 edges), pentagons 5+5 |
| truncated octahedron | Archimedean | Oh | 3 | 3 | the 3 coordinate planes (4 edges each), squares 4+4 |
| 6- and 10-gonal prisms | prism | D6h, D10h | 3, 5 | all | two opposite side edges, squares 4+4 (Prop. B1) |
| J18, J20, J21, J35, J36, J38–J43, J55, J57, J67 | Johnson | – | 2–5 | 0 | the same prism-belt planes, mirror broken by the caps |
| J27, J28, J29, J30, J31, J34 | Johnson | – | 1–11 | 0 or 1 | the equator of edges between the two cupolas or rotundas (6, 8 or 10 edges); for J27, J29, J30, J34 also planes parallel to a single face (inherited from the cuboctahedron or icosidodecahedron half) |
| J26 gyrobifastigium | Johnson | D2d | 2 | 2 | one edge, triangles 3+3 |

**Pattern (observation, exact scope: the 28).** Every shared plane is one of four kinds:
- (a) a **belt plane** through two opposite side edges of a 6- or 10-sided prism belt;
- (b) an **equator of edges** (hexagon, octagon or decagon) parallel to two faces;
- (c) a **zonohedral plane** (rhombic dodecahedron and triacontahedron: every plane);
- (d) in a turned bicupola or birotunda, an equator plane of the uncut parent that survives on one side only.

Kinds (a) and (b) both rest on one fact about regular polygons (Lemma 1). Kind (c) is Theorem 2.

**Lemma 1 (regular polygons, PROVED).** A regular n-gon centred at O has an edge parallel to a line from O to a corner exactly
when n ≡ 2 (mod 4), and then every edge is.
*Proof.* The corners are at angles 2πk/n, and the edge from corner k to corner k + 1 has direction (2k + 1)π/n + π/2. It is
parallel to corner j when (2k + 1)/n + 1/2 ≡ 2j/n (mod 1), that is, when n/2 ≡ 2(j − k) − 1 (mod n). This needs n even with n/2
odd. ∎ (This is Proposition B1 of the catalogue study, written for the polygon itself.)

**Theorem 1 (the polar test, any dimension; PROVED).** Let P be a convex polytope in R^d with O inside, and P\* its polar. Then
Resonus(P) = {v^⊥ : v a corner of P\*} and Vacuus(P) = {(v − w)^⊥ : [v, w] an edge of P\*}. Hence:
- (a) R ∩ V ≠ ∅ exactly when some edge of P\* is parallel to a line from O to a corner of P\*;
- (b) R = V exactly when the corner lines of P\* are the edge lines of P\*; R ⊆ V when every corner line is an edge line;
  V ⊆ R when every edge line is a corner line;
- (c) each of these properties holds for P exactly when it holds for A^{−T}P, for every invertible linear map A.

*Proof.* The facet F of P lies on a_F·x = 1, and a_F is the corner of P\* dual to F. Its Resonus hyperplane is a_F^⊥. The ridge
F ∩ G is dual to the edge [a_F, a_G], and its plate is (a_F − a_G)^⊥ (resonus study, Theorem 1, and resonus-4d §2). This gives
(a) and (b). For (c), (A^{−T}P)\* = A·P\*. A linear map carries corner lines to corner lines and edge lines to edge lines. ∎

**Theorem 2 (root polytopes, PROVED).** Let Φ be one of A2, A3, A4, A5, D4, D5, E6, E7, E8, H3, H4. In conv(Φ) every edge is
parallel to a root, and every root line carries an edge. So the polytope Π(Φ) = {x : x·α ≤ 1 for all α ∈ Φ} has Resonus = Vacuus,
and both are the |Φ|/2 root mirrors.
- *Members.* A2: the hexagon. A3: the rhombic dodecahedron. H3: the rhombic triacontahedron. D4: the 24-cell. H4: the 120-cell.
  **A4: the polar of the runcinated 5-cell (20 facets, Resonus = Vacuus = 10).** A5, D5, E6, E7 and E8 give the same in 5–8
  dimensions.
- The regular 2m-gon with m odd (the root system I2(m)) is the 2D case, by Lemma 1.

*Proof* (`scripts/cat_overlaps.py`, part C, exact: rationals for A, D, E, and Q(√5) for H). The Weyl group is transitive on the
roots, so one root a0 suffices. Every other root b gets a certificate:
- **edge:** c = a0 + b attains its maximum over Φ exactly at a0 and b;
- **not an edge:** one of
  - b = −a0;
  - a0 + b = g + h for another pair of roots;
  - a0 + b = t·g with |t| < 2 (then the midpoint cannot lie on a face where only a0 and b are maximal);
  - for H3 and H4, the cone test: every g − a0 is a nonnegative combination of the edge vectors found, so those are all the
    edges at a0.

Then every edge vector a0 − b is checked to lie on a root line, and transitivity carries this to every edge and every root.
Neighbours of a corner: A2 2, A3 4, A4 6, A5 8, D4 8, D5 12, E6 20, E7 32, E8 56, H3 4, H4 12; no pair left uncertified. Theorem 1
turns this into Resonus = Vacuus for Π(Φ). ∎

For the simply laced case, a proof that does not depend on the computation:
- Normalise |α|² = 2.
- If (a0, b) = 1, then c = a0 + b gives 3 at a0 and b and at most 2 elsewhere, so [a0, b] is an edge, and a0 − b = s_b(a0) is a
  root.
- If (a0, b) = −1, then a0 + b is a root, so the midpoint is half a root and lies strictly inside.
- If (a0, b) = 0, one needs a root g with (g, a0) = (g, b) = 1; then a0 + b = g + (a0 + b − g). That lemma was checked for each
  system here; a general proof is LEAD 2.

**Theorem 3 (Resonus = Vacuus = mirrors, PROVED).** For Π(Φ) the mirrors are the reflections in Aut(Φ). The Resonus and the
Vacuus are the root mirrors, so R = V = M exactly when Aut(Φ) contains no reflection outside the Weyl group. This holds for:
- H3 (the rhombic triacontahedron), H4 (the 120-cell), E7 and E8: here Aut(Φ) is the Weyl group, which contains −1;
- A_n for n ≥ 4, including the new A4 polytope. Here Aut = W × {±1}. The map −w is a reflection only if w has eigenvalue −1 with
  multiplicity n − 1. A permutation of n + 1 letters has as many eigenvalues −1 as it has cycles of even length, so this needs
  2(n − 1) ≤ n + 1, that is, n ≤ 3.

It fails for:
- A2 (the hexagon: 6 mirrors against 3);
- A3 (the rhombic dodecahedron: 9 against 6);
- D4 (the 24-cell: 24 against 12);
- D_n for n ≥ 5 (W(B_n) adds the coordinate mirrors).

E6 is OPEN (does W(E6) contain −r for a reflection r?). In the 163 the rhombic triacontahedron is the only polyhedron with
R = V = M (exact table). ∎

**The extreme case in 3D: Resonus = Vacuus exactly.**
- **PROVED POSSIBLE:** by Theorem 1(c), every linear image A^{−T}RD and A^{−T}RT, with O at the centre. These are two families of
  shapes with five parameters each.
- **Exhaustive within scope:** among the 163 catalogue polyhedra, the 15 192 Aequi and the 9 compounds, exactly the rhombic
  dodecahedron and the rhombic triacontahedron.
- **Full classification: OPEN.** Blocker: by Theorem 1 the question is which convex polyhedra Q have their edge lines equal to
  their corner lines. No bound on the number of corners is known, so no finite search settles it. Every known example is a
  linear image of conv(A3) or conv(H3) and is centrally symmetric. One small fact: among centrally symmetric hexagons only the
  linear images of the regular one qualify (the edges b − a, c − b and a + c are forced to be parallel to c, a and b, so c = b − a).

**Vacuus ⊊ Resonus (PROVED POSSIBLE):** the cuboctahedron (4 ⊊ 7), the icosidodecahedron (6 ⊊ 16), J27 (7 ⊊ 13) and J34
(11 ⊊ 31). In the polar picture, the edges of the rhombic dodecahedron all run along its 4 cube-corner lines. None of the 15 192
Aequi qualifies (exact).

**Resonus ⊊ Vacuus (PROVED POSSIBLE in 3D, new):** Aequus RDRT-24 (T: RD12 + RT24/12; all 18 Resonus planes are Vacuus plates)
and the T die "D12 + RT24/12 + RT24′/12 (2)" (row 365 of the 1 232; all 30). None of the 163 qualifies. In 4D the A4
permutohedron has 15 ⊊ 65 (study 2026-11-24-resonus-4d), and Π(A4) has equality.

**4D analogues (exact).**

| polytope | Resonus | Vacuus | shared | mirrors | relation |
|---|---|---|---|---|---|
| 24-cell (Π(D4)) | 12 | 12 | 12 | 24 | R = V ⊊ M |
| 120-cell (Π(H4)) | 60 | 60 | 60 | 60 | R = V = M |
| Π(A4), polar of the runcinated 5-cell (new) | 10 | 10 | 10 | 10 | R = V = M |
| 4D permutohedron (A4) | 15 | 65 | 15 | 10 | R ⊊ V |
| 600-cell | 300 | 60 | 0 | 60 | disjoint |

## 2. The table of combinations (Part 2)

Sets:
- **163**: the catalogue polyhedra.
- **Aequi**: the 15 192 certified dice (1 232 + 4 404 + 5 935 + 336 + 1 375 + 1 910).
- **cycle**: the stellation-cycle members (I, D, the four Kepler–Poinsot stars, the Dogstar, the Sunstar, the hub).
- **compounds**: the stella octangula; five cubes; five octahedra; five and ten tetrahedra; cube + octahedron;
  dodecahedron + icosahedron; three cubes; three octahedra.
- **perm**: the permutahedra (truncated octahedron, truncated cuboctahedron and truncated icosidodecahedron in 3D; the A4
  permutohedron in 4D).

| pair | members | extreme example | impossible cases (proof) | status |
|---|---|---|---|---|
| **Resonus ∩ Vacuus ≠ ∅** | 163: 28. Aequi: 6 253 exact (≤ 6 285, see †). cycle: 0 for the 6 regular members and the Dogstar; the Sunstar is open. compounds: cube + octahedron 3, three cubes 3, the other 7 none. perm: truncated octahedron 3, the other two 0; the A4 permutohedron 15 | 163: the rhombic triacontahedron, 15 of 15 (R = V). Aequi: 30 shared planes (6 dice, e.g. O: C6 + RD12 + D12+D12′/24 + I12+I12′/24 + RT24+RT24′/24) | the regular cycle members: their Resonus planes are at right angles to five- or three-fold axes, while their Vacuus is the 15 mirrors, at right angles to two-fold axes (exact); in general, by Theorem 1(a), whenever no edge of the polar points along a corner line | PROVED POSSIBLE; the Aequi count is exact as a lower bound |
| **Vacuus = mirrors** | 163: 19 (D, I, T, the 9 Catalans of the list, the odd bipyramids, J12, J13). Aequi: 0. cycle: I, D and the 4 stars (V = the 15 Ih mirrors); the Dogstar has 15 against its own 3, so no. compounds: five octahedra, cube + octahedron, dodecahedron + icosahedron, three octahedra. perm: none (their Catalan polars, the disdyakis dodecahedron and triacontahedron, have it) | the 15 Ih mirrors (dodecahedron, icosahedron, the stars) | **Theorem 5**: Vacuus ⊆ mirrors forces face-transitivity. So it is impossible for every Aequus with ≥ 2 face orbits (all 15 192), every Archimedean polyhedron, every prism other than the cube, and every Johnson polyhedron except J12 and J13 | PROVED (exact) |
| **Resonus = mirrors** | 163: the rhombic triacontahedron only (R ⊊ M: the cube, the RD, the even prisms). Aequi: 1, **Aequus CRD-18** (Oh: C6 + RD12; R = the 9 Oh mirrors). R ⊊ M for the D6h, D8h and D10h prism dice. compounds: five cubes (15 = 15), three cubes (9 = 9). cycle, perm: none | the rhombic triacontahedron and the compound of five cubes (15 = 15) | **Theorem 6**: Resonus ⊆ mirrors forces central symmetry, so it is impossible for every polyhedron without a centre (tetrahedron, snubs, most Johnson polyhedra and Aequi) | PROVED (exact) |
| **Resonus ⊆ the 31 hub planes** | 163: 41 (list in data). Aequi: 4 039 (confirms the stellation-cycle count; the rule is that every face family lies in one icosahedral placement). cycle: all (by construction). compounds: the 7 built in Ih or Oh-in-Ih; three cubes and three octahedra no. perm: the truncated octahedron and the hub (TID) yes; the TCO no | the hub itself (31 of 31: RID, TID, J76); among the Aequi, Yo (No.4) uses all 31 | more than 31 face lines; an angle between face lines that is not a hub angle (three cubes: margin 0.038); the rhombic dodecahedron: its angles fit, but an exhaustive search over all hub-line pairs finds no orthogonal map | PROVED (Aequi exact by face families; 163 and compounds decided in double precision with stated margins, yes-cases also exact for the Platonic, Archimedean and Catalan rows by Theorem C2 of the catalogue) |
| **Aequus ∧ Tacitus** | 163: J12 (fair, silent beyond symmetry in degree 5). Aequi: 813 dice (987 die-degree pairs: 701 composite, 286 accidental; study 2026-11-25-tacitus, joined here for 15 126 of the 15 192). compounds: not convex, so not dice; their direction sets are silent only where forced | Aequi silent beyond symmetry up to degree 14; no accidental silence above degree 5 | none beyond symmetry among the Platonic and Catalan polyhedra, prisms or bipyramids (k ≤ 20, Tacitus census) | PROVED POSSIBLE (exact zero for every accidental pair) |
| **Aequus ∧ equal curvature** (doubly fair) | 163: the 5 Platonic polyhedra (and their copies among the prisms and bipyramids). Aequi: **24, confirmed** (recount of the inversions data: exactly 24 without certified-distinct curvatures). Outside: every disphenoid | Aequus D·I·RT-62 (62 faces, 120 corners) | the other 15 168 Aequi (certified-distinct curvatures, ball arithmetic); the Catalans and the face-transitive Nos. 1233–1235 (their polars are not fair) | PROVED (exhaustive in the catalogue) |
| **Aequus ∧ Resonus ∩ Vacuus ≠ ∅** | 163: the RD and the RT. Aequi: 6 253 (≤ 6 285 †). Doubly fair and sharing: 3 (Aequus CO-14 with 3 planes, the D10h die with 5, the D6h die with 3) | the RT (15 of 15); among the dice, 30 shared planes | – | PROVED POSSIBLE |
| **Tacitus ∧ simplicial Resonus** | 163: 0. Aequi: **9** (D2d: C6/4 + O8/4, degree 5, 6 planes; D2d: C6/4 + O8/4 + RD12/4; D2d: C6/4 + C6/2 + O8/4 + RD12/4; D3: C6+RT24/6 + RT24/6a + RT24/6b + RT24/3 (2); Yaiyao (No.8180); Yaiyamu (No.8186); Yaniyaha (No.8288); Yamioyo (No.8304); Yanagoni (No.8752), the last with 21 planes and 240 triangles) | Yanagoni (No.8752): silent beyond symmetry in degree 3, simplicial Resonus with 240 triangles | in the 163 the 9 Tacitus Johnson polyhedra all have non-simplicial Resonus (the only simplicial Johnson Resonus are J3, J19 and J76, and none is Tacitus; k ≤ 20) | PROVED POSSIBLE (Aequi); PROVED IMPOSSIBLE within the 163 |
| **Aequus ∧ harmonious Sphericus** | 163: the cube (Resonus) and the octahedron (Vacuus). Aequi: 0. Outside the catalogue: every octahedron with three perpendicular, mutually bisecting diagonals | the 3 coordinate planes (score 6/6 in plate-harmony) | **Theorem 7**: harmonious crossings force three perpendicular planes. Then a fair die is the cube (Resonus) or a "diagonal octahedron" (Vacuus); no catalogued Aequus is either | PROVED (complete classification) |

† **The 60 depth coincidences** (`data/candidates.json`). In 60 dice a plate between faces of two different orbits would be a
Resonus plane if the depth ratio of those orbits equalled an exact number r\* in Q(√5, √3). The certified depth balls (radius
≤ 1e-40) contain r\*, for example √3/φ, φ, 1/φ or 1. 10 of these dice are station dice of the stellation-cycle study
(Theorem 8 there proves their ratio √3/φ exactly), and 18 are on its list of dice with two orbits of one axis type at equal depth.
None is used in the counts. If all held, 32 more dice would join "R ∩ V ≠ ∅", giving at most 6 285. OPEN (LEAD 1).

## 3. Theorems found here

**Theorem 5 (Vacuus inside the mirrors ⇒ face-transitive; PROVED).** If every Vacuus plate of a convex polyhedron P is a mirror
of P, then the symmetry group of P is transitive on the faces.
*Proof.* The plate of the edge between faces F and G is a mirror exactly when a reflection of P swaps F and G (resonus-4d,
Theorem 2). So every two faces meeting at an edge lie in one orbit. The graph of faces meeting at edges is connected, so there is
only one orbit. ∎
The converse fails: the snub Catalans and the trapezohedra with n ≥ 4 are face-transitive without it.

**Theorem 6 (Resonus inside the mirrors ⇒ centrally symmetric; PROVED).** If every Resonus plane of P is a mirror, then P is
centrally symmetric.
*Proof.* The Resonus plane of F is u_F^⊥. If it is a mirror, the reflection σ in it is a symmetry of P, and σ(F) is a face with
normal −u_F and the same area as F. So the faces come in parallel pairs of equal area, and P is centrally symmetric by Minkowski's
theorem (catalogue study, Theorem A(d)). ∎

**Theorem 7 (harmonious Sphericus; PROVED).** Let A be a central arrangement of planes in R³ that do not all pass through one
line. Suppose its crossings are harmonious: every crossing point lies on the same number m of great circles, and every crossing
angle is the same. Then A is three mutually perpendicular planes.
*Proof.* At a point on m circles there are 2m equal angles, so each is π/m and the pencil there is regular. All pencils regular
means a reflection arrangement (plate-harmony, Theorem 1). The rank-3 reflection arrangements (Coxeter 1934) and their point
multiplicities are:
- A1³: {2};
- A1 × I2(p), p ≥ 3: {2, p};
- A3: {2, 3};
- B3: {2, 3, 4};
- H3: {2, 3, 5}.

Only A1³ has one multiplicity. ∎

*Corollary (Aequus).*
- (i) The Resonus is harmonious exactly when the face normals lie on three perpendicular lines, so P is a box. A box is fair
  about an interior point O only if it is a cube centred at O.
  - Of two opposite faces, the one nearer to O subtends strictly more: its cone contains the mirror image of the other's.
  - So O is the centre.
  - Then, by the same containment after swapping two axes, the faces across the shortest axis subtend strictly more unless all
    three half-lengths are equal.
- (ii) The Vacuus is harmonious exactly when P is an "axial octahedron", with one corner on each of the six half-axes of an
  orthonormal frame at O.
  - Every edge lies in one of the three planes.
  - Two edges of one face cannot share a plane through O, so every face is a triangle with its corners on the axes.
  - Convexity and O inside give one corner per half-axis.
  - Every axial octahedron is fair about O: each face is seen from O as a whole octant (π/2).
  - Its corner centroid and its volume centroid are O exactly when it is centrally symmetric. The x-moment of the volume is
    (a₂² − a₁²)(b₁ + b₂)(c₁ + c₂)/24.
  - So the fair dice with a harmonious Vacuus are the octahedra whose three diagonals are perpendicular and bisect each other: a
    two-parameter family that contains the regular octahedron. ∎

## 4. Observations (labelled as such)

- Equal corner curvature in the 163 also holds for J16, J27, J34, J37, J45 and J72–J75, besides the corner-transitive
  polyhedra. For polyhedra with regular faces, the curvature at a corner depends only on the faces there.
- The compound of five tetrahedra has the icosahedron's face directions. Against its own group I it is silent beyond symmetry
  in degree 15, the Dogstar mechanism. Against the group of its directions (Ih) it is not.
- The triple R = V = M appears exactly where a root system "fills" its own symmetry: H3, H4, E7, E8, A_{n≥4}. Two of the space-filling
  members of the 3D catalogue, the RD and the truncated octahedron, are the Voronoi cells of A3 and A3\*.
  - RD: R = V ⊊ M.
  - TO, the 3D permutohedron: R ∩ V = 3.
  - The 4D permutohedron (Voronoi cell of A4\*): R ⊊ V.
  - A402191 Theorem A(iv) says that every resonance hyperplane occurs when n is odd; this fits the 4D case (n = 5).
- 63 dice (two-placement dihedral dice) have a symmetry group larger than the frame maps realise. Their mirror columns use the
  frame group, except that Resonus ⊆ mirrors was decided directly (`data/bigger-groups.json`: 3 prism dice). Theorem 5 settles
  Vacuus = mirrors for them. "Mirrors ⊆ Vacuus" is not claimed for them.

## 5. Method

- `scripts/aequi_overlaps.py`. It reuses the loader of study 2026-11-25-inversions (`polar_aequi.records`) and the exact frame
  directions and combinatorics of study 2026-11-24-aequi-certify-extend.
  - The 122 directions are exact over Q(√5); separation 0.188.
  - Every determinant below 1e-6 is checked to be exactly zero; the smallest nonzero one is 0.021.
  - Same-orbit plate tests are exact. Different-orbit tests use the depth balls (60-digit data, or the certified enclosures of
    radius about 1e-40; 15 dice have only double-precision depths, and 2 of them are among the 60 candidates).
  - Mirrors use the mirror laws of study 2026-11-24-resonus-4d.
  - Simplicial Resonus uses the exact projective count (3f₂ = 2f₁).
  - Tacitus is joined from the Tacitus study by name, or by face set for catalogue-2. Equal curvature is joined from the
    inversions study.
- `scripts/cat_overlaps.py`:
  - part A reads the exact catalogue table, the Tacitus polyhedra and their silences. Solid angles and curvatures are in double
    precision; every spread is either below 1e-11 (equal, and then exact by symmetry or by the regular faces) or above 1e-8.
  - part B builds the compounds exactly in Q(√2, √5): the five cubes are found inside the dodecahedron, and the mirrors are
    reflections that permute the components.
  - part C gives the root certificates.

## Sources checked

Studies:
- 2026-11-24-vacuus-resonus-catalogue (Theorems A–D, the 28);
- 2026-11-24-resonus (Theorem 1, the polar link);
- 2026-11-24-resonus-4d (the two mirror laws, the 4D table);
- 2026-11-25-tacitus;
- 2026-11-25-inversions (the 24 doubly fair dice, the polar of an Aequus);
- 2026-11-25-plate-harmony (Theorem 1, the Sphericus measures, the score of the 3 coordinate planes);
- 2026-11-25-stellation-cycle (the hub, Theorem 8, the equal-depth list, the 4 039);
- 2026-11-24-aequi-certify-extend and 2026-11-24-aequi-uniqueness;
- 2026-11-25-one-structure README (read; nothing used).

Classical results credited at point of use:
- H. S. M. Coxeter, "Discrete groups generated by reflections" (Ann. Math. 35, 1934): the rank-3 reflection arrangements;
- Minkowski's uniqueness theorem (1897);
- J. H. Conway and N. J. A. Sloane, *Sphere Packings, Lattices and Groups*, ch. 4 and 21: the root lattices and their Voronoi
  cells (cited, not opened);
- the automorphism groups of root systems (Bourbaki, *Groupes et algèbres de Lie* ch. VI, cited, not opened).

No web search was run (LEAD 6).

## LEADS

1. Prove or refute the 60 depth coincidences († above) with the station method of the stellation-cycle study (Theorem 8); up to
   32 dice would join R ∩ V.
2. General proof of the lemma behind Theorem 2 for all ADE systems: orthogonal roots α, β have a root g with (g, α) = (g, β) = 1.
   Also extend Theorem 2 to all A_n, D_n.
3. The 3D classification of Resonus = Vacuus (convex polyhedra whose edge lines are their corner lines). Is central symmetry
   forced? Is every example a linear image of conv(A3) or conv(H3)?
4. E6 in Theorem 3: does W(E6) contain −r for some reflection r?
5. The Sunstar: is any of its 69 plates parallel to one of its 6 Resonus planes? One rerun of the stellation-cycle arrangement
   script.
6. Prior art: "polytopes whose edges are parallel to their vertex vectors" and Resonus = Vacuus for Voronoi cells; root
   polytopes (Cellini–Marietti and others); open the free copies.
7. The 66 dice of the inversions set that are not in the Tacitus census; Tacitus for them.
8. The uniform compounds with a free angle (Skilling's list): the overlaps as functions of the angle.

## Files

- `scripts/`: aequi_overlaps.py, post_aequi.py, post_join.py, post_bigger_groups.py, cat_overlaps.py, table28.py.
- `data/`:
  - aequi-overlaps.jsonl.gz: one row per die;
  - aequi-summary.json;
  - candidates.json;
  - bigger-groups.json;
  - cat-overlaps.json: the 163, the compounds and the root systems;
  - table28.md.
- `logs/`.
