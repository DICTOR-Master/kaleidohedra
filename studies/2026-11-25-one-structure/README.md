# One structure: the Aequus, the Vacuus, the Resonus, Tacitus and the factor 3; shadows and crossings (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-one-structure · with Claude (Anthropic).

> **Status box.** Study note, not published. Checks: extract.py FINAL ok (logs/extract.log); shadows.py FINAL ok (7 056 shadows);
> control_yantra.py and yantra_sat.py on the control FINAL ok (SAT, as required); yantra_sat.py FINAL ok; internal.py FINAL ok
> (18 frames); a_items.py FINAL ok; yantra_degree.py FINAL ok; summarize.py FINAL ok. Full tables: `data/tables.md`.
> A4 is waiting for the five-cube Aequi sweep (still running). Nothing of this study is running.

Every item ends as **PROVED POSSIBLE** (with a construction), **PROVED IMPOSSIBLE** (with a proof and its scope) or **OPEN**
(with the blocker), as DICTO asked on 25 Nov: "inspiration is useless without thorough examination of possibility and
impossibility".

## Verdict

| item | result |
|---|---|
| A1 Aequus ⇔ equal fin regions | **PROVED** (both directions, any interior centre). On the boundary both sides are false (proved). With the full plates instead of fins it fails both ways (two exact counterexamples). |
| A2 Resonus and Tacitus | **PROVED**: even degrees are decided by the Resonus *with plane weights*; odd degrees are not decided by the Resonus at all; the unweighted Resonus decides the even degrees exactly when the plane weights are equal (e.g. centrally symmetric, unit weights). **PROVED POSSIBLE**: a cube-octahedron polyhedron with the truncated octahedron's Resonus that is silent in degree 4 beyond symmetry (t* ∈ certified interval). **PROVED**: a three-plane Resonus with degree-2 silence is the three coordinate planes. |
| A3 the factor-3 bridge | **PROVED POSSIBLE (exact)**: r = √3/φ = [corner ÷ inradius of a regular octahedron] × [one ladder step φ⁻¹], the octahedron being any of the five that circumscribe I_{k−1} (8 faces shared, corners on the midsphere of I_k); √3 is the cube's diagonal ÷ edge. **PROVED IMPOSSIBLE**: in no die are the S and B faces a diagonal and a face of one same cube. Explains the two appearances of 3/φ² (polarity). |
| A4 O ⊂ rTI and the Sunstar vs the five-cube Aequi | **WAITING**: the sweep (study 2026-11-25-aequi-five-cubes) has no results yet. |
| B1 yantra as shadow | **PROVED IMPOSSIBLE (exact copy)** for every shadow examined and every direction of field degree ≤ 39 (DICTO Yantra) or ≤ 86 (Kulaichev). **PROVED IMPOSSIBLE (combinatorial pattern)** in all 7 056 shadows (pencil test for 7 048; exhaustive SAT for the 8 others, the rational yantra as positive control). **OPEN** beyond the scanned directions (blocker named). Marma counts: tables. |
| B2 internal crossings | **COMPUTED EXACTLY** for all 18 Platonic and Archimedean frames: tables; patterns stated below. |

## Part A

### A1. The Aequus seen through its fins

Let P be a convex polyhedron and O a point of P. For an edge e the **fin** is the triangle conv(O ∪ e) (the part of its Vacuus
plate between O and the edge). Let π be the radial projection from O onto the unit sphere S centred at O. A fin of an edge
not through O projects onto the great-circle arc π(e); the fins cut S along Γ = ∪ π(e). (When the in-ball of P about O has
radius ≥ 1 the fins cut S along Γ literally; scaling P about O changes neither π nor any area.)

**Theorem A1.** (a) If O is inside P, then S \ Γ has exactly F components, one for each face f, namely π(relint f), and its
area is the solid angle Ω_f of f at O. Hence P is an Aequus about O ⇔ all the regions cut by its fins have equal area
(each then 4π/F).
(b) If O lies on the boundary of P (on at least one face plane), P is not an Aequus about O, and the fin regions are not all of
equal area: the equivalence holds with both sides false.
(c) O outside P is out of scope (no centre; each direction of P's cone meets the surface twice, so faces overlap in projection).

*Proof.* (a) P is convex with O inside, so every ray from O meets ∂P exactly once and π: ∂P → S is a homeomorphism. It maps the
union of the edges onto Γ, so S \ Γ = π(∂P \ edges) = ⊔ π(relint f): disjoint open connected sets, hence the components.
Ω_f is the area of π(f), and π(f) \ π(relint f) ⊂ Γ has area 0. (b) Let C = π(P \ {O}), the spherical image of P's cone at O:
a closed hemisphere (O inside a face), a lune of angle < π (O on an edge) or a convex polygon of area < 2π (O a corner). Every
fin arc lies in C, so S \ C is one extra region, of area ≥ 2π, while the face regions lie in C and have total area ≤ 2π, and there
are at least two of them unless O is a corner with one face opposite (then 4π − A > A). So the areas are never all equal; and
the faces through O have Ω = 0 while the others have Ω > 0, so P is not fair. ∎

*With the full plates the statement fails both ways (exact).*
- Fair, plates unequal: the 5-gonal trapezohedron (face-transitive, so fair about its centre); its 10 Vacuus planes cut 60 regions
  of three areas π/30, π/15, π/10 (study 2026-11-25-plate-harmony, exact).
- Plates equal, not fair: J59 (parabiaugmented dodecahedron; centrally symmetric, so both centroids are the dodecahedron's
  centre). Its Vacuus is the 15 mirror planes (vacuus-resonus catalogue), 120 congruent regions of area π/30. Its 10 pentagons
  are dodecahedron faces, 10 mirror triangles each: Ω = π/3. Each pyramid triangle has its side edges in the mirror planes
  through the five-fold axis and a corner, so it covers 2 mirror triangles: Ω = π/15. Not fair.

So the right carriers of the Aequus are the fins, not the plates: an Aequus is exactly a polyhedron whose Vacuus fins divide
the sphere about O into equal parts.

### A2. What Tacitus says about the Resonus

Notation as in study 2026-11-25-tacitus: weights w_f (i) 1 or (ii) Ω_f; silent in degree k when Σ w_f h(n_f) = 0 for every
harmonic h of degree k. The Resonus R(P) is the set of planes through O parallel to faces: it keeps the face **axes** ±n_f and
loses both the signs and the multiplicities. Give each Resonus plane L the weight W_L = Σ of w_f over the faces parallel to L
(one or two faces; for an Aequus W_L = (4π/N)·m_L, m_L ∈ {1, 2}).

**Theorem A2.** (a) *Even degrees transfer, with weights.* For even k, P is silent in k ⇔ Σ_L W_L h(n_L) = 0 for every harmonic h
of degree k (h(−n) = h(n)). So the weighted Resonus decides every even degree.
(b) *Odd degrees do not transfer.* The tetrahedron and the octahedron have the same Resonus (4 planes at right angles to the
three-fold axes) but Σ xyz over the face normals is 4 (tetrahedron, unnormalised (±1, ±1, ±1) with an even number of minus
signs) and 0 (octahedron): not silent / silent in degree 3 (a-items.json, exact).
(c) *Weights matter in even degrees.* Let P_t = cube [−1, 1]³ ∩ {|x| + |y| + |z| ≤ t}. For 1 < t ≤ 2 its faces are 6 squares and
8 hexagons, and its Resonus is the 7 planes of the truncated octahedron (t = 3/2). The degree-4 Oh-harmonic
x⁴ + y⁴ + z⁴ − 3/5 takes 2/5 on the square axes and −4/15 on the diagonals, so P_t is silent in degree 4 exactly when
Ω_square : Ω_hexagon = 8 : 9, i.e. Ω_square = 4π/15, Ω_hexagon = 3π/10. **PROVED POSSIBLE:** there is exactly one such t*,
t* ∈ [994134708034889649/576460752303423488, 497067354017444825/288230376151711744] (t* ≈ 1.7245488163),
certified by the signs of Ω_square(t) − 4π/15 at the two ends in ball arithmetic (Van Oosterom–Strackee); uniqueness by the
monotone-cell lemma (Lemma 9 of study 2026-11-25-stellation-cycle). With solid-angle weights P_t* is silent in degrees 1–5 and
every odd degree ≤ 20 (exact rational zonal sums); Oh forces only 2 and the odd degrees, so **degree 4 is silence beyond
symmetry**. The truncated octahedron itself (unit weights) is not silent in 4. Same Resonus, different Tacitus.
(d) *When the bare Resonus suffices.* If all plane weights are equal (for instance P centrally symmetric with unit weights: by
Theorem A of the vacuus-resonus catalogue every Resonus plane then carries two faces), every odd degree is silent and the even
degrees are those of the unweighted Resonus axes. Then forced silence passes through: if the symmetry group of the Resonus axis
set has no invariant harmonic of even degree k, P is silent in k.
(e) *A rigidity.* If the Resonus has exactly three planes and P is silent in degree 2, the three planes are mutually
perpendicular and carry equal weight. *Proof:* Σ W_i n_i n_iᵀ = cI with n_1, n_2, n_3 independent; for x at right angles to
n_2 and n_3, W_1(n_1·x)n_1 = cx, so x ∥ n_1, i.e. n_1 ⊥ n_2, n_3; likewise for the others; then W_i = c. ∎ So the only three-plane
Resonus that can be silent is the three coordinate planes, the arrangement that scored 6/6 in the plate-harmony study.

### A3. The factor-3 bridge

Frame of the stellation-cycle study: I_k = φ^k·I0, I0 = cyclic (0, ±φ, ±1); D0 = (±1, ±1, ±1) and cyclic (0, ±1/φ, ±φ).
Theorem 8 there: in 41 station dice the depth ratio r of a two-fold orbit B (on RT_k) over a three-fold orbit S (on I_k) satisfies
r² = 3/φ²; that is, r = midradius(I_k)/inradius(I_k).

**Theorem A3 (exact, a_items.py).**
1. The regular octahedron O_k = {|x| + |y| + |z| ≤ φ^{k+1}} circumscribes I_{k−1}: its 8 face planes are 8 of I_{k−1}'s 20 face
   planes, and the 12 corners of I_{k−1} lie on its 12 edges, dividing each in the golden ratio (ratio exactly φ). This is the
   classical icosahedron in the octahedron (cited, not opened: Coxeter, *Regular Polytopes*).
2. Its 6 corners lie at distance φ^{k+1} = the midradius of I_k: on the rhombus planes of RT_k.
3. Hence r = mid(I_k)/in(I_k) = [R(O_k)/in(O_k)] · [in(I_{k−1})/in(I_k)] = **√3 · φ⁻¹**, where R/in of the regular octahedron
   is √3 = the diagonal ÷ edge of its polar cube, and φ⁻¹ is one step of the ladder.
4. The five octahedra polar to the five cubes inscribed in D0 (5 cubes found exactly; every corner of D0 is in exactly 2 of
   them) do the same for all 20 three-fold planes. So for **every one of the 41 dice** (42 hits: 11 two-fold over three-fold,
   31 three-fold over two-fold, all with r² = 3/φ² or its inverse) the factor 3 = (√3)² is the octahedron's (cube's) ratio and
   the rest is one φ-step. **The hypothesis holds.**
5. The numbers behind it: every corner of D0 has squared radius 3, because 1 + 1 + 1 = 0 + φ⁻² + φ² (= the Lucas number L₂):
   the cube corners and the golden-rectangle corners of the dodecahedron lie on one sphere. This is where the cube family
   meets the φ-ladder. N(3/φ²) = 9 ≠ ±1 and 3 is inert in Z[φ], so 3/φ² is not ±φ^k (a second proof of the #33 fact).
6. **PROVED IMPOSSIBLE (scope: the 41 dice):** the S and B faces of a die are never a diagonal and a face of one same cube or
   octahedron: neighbouring S and B normals make cos² = (in/mid)² = φ²/3 = 1/2 + √5/6, a cube's diagonal and face normal 1/3.
   The bridge is metric (radii through the octahedron at the neighbouring scale), not an incidence of S and B with one cube.
7. The polarity of I0 and D0 in the midsphere m (R(D0)·in(I0) = m², checked) gives R(D0)/in(I0) = (m/in(I0))² = r².
   This is why 3/φ² appears both as r² (gap b) and as the size of the gap-(d) octahedron |x| + |y| + |z| ≤ 3 against I0's planes
   (x + y + z = 3 vs φ²): the "observation, no reason claimed" of the stellation-cycle study is now proved.

### A4. The loose step O ⊂ rTI and the Sunstar: WAITING

Study 2026-11-25-aequi-five-cubes says "STATUS: running"; it has no dice yet. Recorded as waiting (follow-up added). When it
ends: screen its dice with scripts/gaps.py and gapcheck.py of the stellation-cycle study against (a) O ⊂ rTI and (d) D0 ⊂ the
Sunstar's hull.

## Part B

### Definitions used

- **Skeleton**: the edges plus the **Vacuus struts** (the segments from the centre O to every corner, as in the Vacuus builds of
  study 2026-11-24-vacuus-build-renders). Kepler–Poinsot stars: their 30 true edges; Dogstar and Sunstar: visible-surface edges.
- **Shadow**: orthographic projection onto a plane; collinear projected segments are merged into drawn pieces.
- **Marma**: a point inside the drawn pieces of three or more different lines (a true triple crossing). The projected centre is
  counted separately. **Mixed point**: three or more drawn lines through a point, not all crossing inside (a corner image on a line).
- **Combinatorial Sri Yantra in a shadow**: an injective map of the yantra's 27 lines (9 bases, 18 legs) to shadow lines that sends
  each of its 31 triple points (18 marmas, 6 corner touches, 7 apex-on-base points; Chiodo's numbering, as in the sri-yantra study)
  to its own drawn point of the shadow, with the right lines crossing inside, and the 9 bases to one pencil (parallel or concurrent).
  This is a necessary condition for the pattern (9 triangles, 18 marmas, hence the 43 small triangles); exact equality of
  pictures (up to similarity) is the stronger "exact copy".

### B1. Results

**Directions.** Symmetry-adapted: the corner, edge-midpoint and face-centre directions of each Platonic/Archimedean polyhedron
(they contain every rotation axis; the 3D Coxeter planes are the planes at right angles to the 5-, 3- and 4-fold or 2-fold axes),
the 31 axes of the icosahedral frame for the stars, Dogstar and Sunstar; one per exact signature. Dense: **every primitive integer
direction with coordinates up to 4 (289 per skeleton)**. 4D: the H4 Coxeter plane (exact in Q(2cos(2π/30))) and the planes
"vertex-first, then a 5-, 3- or 2-fold axis" and "cell-first, then a 3- or 2-fold axis" (projecting to 3D and then to 2D is the
projection onto the plane at right angles to both directions); the cell-first planes turn out to equal vertex-first ones up to
symmetry (identical counts). 7 044 3D shadows and 12 4D shadows, all exact.

**Marma counts (highlights; all in data/tables.md).**
- Platonic and Archimedean, symmetric directions: at most 20 marmas (icosidodecahedron along a five-fold axis: 20 triple points);
  cube, octahedron, tetrahedron: none besides the centre.
- Kepler–Poinsot stars: great stellated dodecahedron along a three-fold axis 36 (24 triple, 12 five-fold); small stellated
  dodecahedron and great icosahedron 20 (five-fold axis) and 18 (three-fold axis).
- **Sunstar along a five-fold axis: 38 marmas, the most of any 3D shadow.** Along three-fold axes 28 and 18.
- Dense scan: 1 271 of 6 936 scan shadows have a marma; the most is 36 (great stellated dodecahedron, direction (1, −1, −1),
  a three-fold axis). None passes the pencil test.
- 4D: 600-cell on the Coxeter plane **1 440 marmas** (1 320 triple, 30 four-fold, 90 five-fold); 120-cell on the Coxeter plane
  **1 320** (1 290 triple, 30 five-fold); the vertex-first planes 10–52.

**Theorem B1a (no exact copy).** Let t7 be the yantra's great triangle (apex at the top point, leg slope u). Its apex angle α has
tan α = 2u/(1 − u²). u has degree exactly 160 (DICTO Yantra) and 348 (Kulaichev): both polynomials are irreducible over Z
(FLINT, yantra_degree.py), and u satisfies τu² + 2u − τ = 0 over Q(τ), τ = tan α, so deg τ ≥ 80 (resp. 174). In an
orthographic shadow of a skeleton with corners in a field K, along a direction (or plane) defined over L ⊇ K, the tangent of the
angle between two shadow lines lies in L(√g) (g the Gram determinant of the plane basis), of degree ≤ 2[L:Q]. So **if [L:Q] ≤ 39
no two shadow lines meet at the DICTO Yantra's t7 angle (≤ 86 for Kulaichev's), and the shadow contains no figure similar to it.**
Every shadow here has [L:Q] ≤ 6 (snub dodecahedron; 4 for the Coxeter plane): **PROVED IMPOSSIBLE for all 7 056, and for every
direction of degree ≤ 39 (≤ 86) over Q.** (The rational yantra R1 is not covered by this argument: its tan α is rational.)

**Theorem B1b (no combinatorial pattern), exhaustive per shadow.** Pencil test (necessary, implied by the definition): 9 lines of
one pencil whose numbers of drawn triple points dominate the bases' needs (5, 5, 5, 4, 4, 3, 3, 1, 1; inside the piece:
5, 5, 3, 3, 3, 2, 2, 1, 1). 7 048 shadows fail it. The 8 that pass (the five vertex-/cell-first 120-cell planes, both Coxeter
planes, the Sunstar along a five-fold axis) were given to an exhaustive SAT search (CaDiCaL 1.5.3 via PySAT) of the full
definition. Positive control: the rational Sri Yantra R1 drawn exactly through the same code gives 18 marmas, passes the pencil
test and is found SAT.

| shadow | exhaustive search |
|---|---|
| control: rational Sri Yantra R1 | **SAT** (the map is found, as it must be) |
| 120-cell: vertex-first then 5-, 3-, 2-fold axis; cell-first then 3-, 2-fold axis | UNSAT, each under 1 s |
| 120-cell on the H4 Coxeter plane | UNSAT (1 197 s; 192 875 variables, 667 211 clauses) |
| 600-cell on the H4 Coxeter plane | whole instance undecided in 1 500 s; split by its 151 pencils (the bases lie in exactly one pencil, so the instance is the union): **all 151 UNSAT** (150 within 90 s, pencil 47 in a separate run) |
| Sunstar along a five-fold axis | UNSAT (0.09 s) |

So **no shadow examined (7 056) contains the Sri Yantra's incidence pattern**: PROVED IMPOSSIBLE within these directions,
exhaustively (pencil test for 7 048, SAT for the other 8; the SAT verdicts rest on the solver, no proof log was kept).

**OPEN (combinatorial pattern, other directions).** Directions outside the scan (integer coordinates > 4, or irrational
directions other than the symmetric ones) are not covered. *Blocker:* for three pairwise skew lines the directions along which
their shadows are concurrent form a conic (the lines meeting all three form a regulus); 18 simultaneous marmas need a direction
on 18 such curves at once, i.e. at intersection points of the curve arrangement. Enumerating those points exactly for every
segment triple (about 4.5 million triples for the hub) would make the search exhaustive over all directions. Not done.

### B2. Internal crossings (exact)

For each of the 18 Platonic and Archimedean polyhedra: struts S, face diagonals FD, space diagonals SD, and plate lines PL (every
line through O where two Vacuus plates meet, clipped to the polyhedron). Every crossing point is exact; corners are left out.

| polyhedron | plates | plate lines = lines at O | inside points with 3+ lines (marmas) | densest inside points |
|---|---|---|---|---|
| tetrahedron, cube, octahedron | 6, 6, 3 | 7, 7, 3 | 0 | – |
| truncated tetrahedron | 18 | 85 | 6 | 6 × 3 lines (PL + 2 SD) |
| cuboctahedron | 4 | 6 | 12 | 12 × 3 (axis + 2 SD) |
| icosahedron | 15 | 31 | 20 | 20 × 4 (PL + 3 SD) |
| dodecahedron | 15 | 31 | 102 | 12 × 6 (PL + 5 SD) |
| truncated octahedron | 15 | 69 | 144 | 6 × 7 (PL + 6 SD) |
| truncated cube | 18 | 85 | 110 | 32 × 4 (PL + 3 SD) |
| rhombicuboctahedron | 24 | 153 | 170 | 24 × 6 (PL + 5 SD) |
| snub cube | 48 | 669 | 26 | 6 × 5 (PL + 4 SD) |
| icosidodecahedron | 6 | 15 | 242 | 60 × 5 (axis + 4 SD), 12 × 5 (5 SD) |
| truncated cuboctahedron | 36 | 537 | 492 | 24 × 5 (PL + 4 SD) |
| truncated icosahedron | 45 | 481 | 1 052 | 12 × 6 (PL + 5 SD) |
| truncated dodecahedron | 45 | 481 | 1 322 | 20 × 7 (PL + 6 SD) |
| rhombicosidodecahedron | 60 | 1 395 | 2 212 | 12 × 10 (10 SD) |
| snub dodecahedron | 150 | 9 171 | 64 | 24 × 6 (PL + 5 SD) |
| truncated icosidodecahedron (hub) | 90 | 3 675 | 4 910 | 30 × 7 (PL + 6 SD) |

(Full histograms, boundary points and every family pattern: data/tables.md and data/internal.json.)

**Patterns (exact, for these 18).**
1. The centre O is the only point where struts, plate lines and the central space diagonals all meet; there every plate line
   passes (the "lines at O" column equals the number of plate lines).
2. Every densest inside point except two lies on one plate line, with the rest of its lines space diagonals: the internal marmas
   gather on the plate lines (the rotation axes for the Platonic ones). The exceptions: the rhombicosidodecahedron (12 points
   where 10 space diagonals cross, no plate line) and the icosidodecahedron (12 points of 5 space diagonals).
3. Face diagonals never take part in an inside point; their crossings are on the faces (boundary column).
4. The snubs have few marmas for their size (26 and 64) though they have the most plate lines (observation; no reason claimed).

## Method

- Exact number fields: nf.py of study 2026-11-25-plate-harmony (FLINT fmpq_poly modulo the minimal polynomial, signs from Arb
  balls). Skeletons: the exact builders of studies 2026-11-24-vacuus-resonus-catalogue and -vacuus-enumeration (uniform
  polyhedra) and cycle.py of 2026-11-25-stellation-cycle (stars, Dogstar, Sunstar), unchanged.
- Shadows (shadow_core.py) and internal crossings (internal.py): double-precision screening with stated tolerances, every kept
  pair and every multiple point confirmed exactly; near-parallel pairs decided exactly (see the docstrings for the bounds).
- 4D: 600-cell from four_d.py of the plate-harmony study; the 120-cell as the 600 cell centres of the 600-cell, edges between
  cells sharing a triangle; the Coxeter plane computed as there (Coxeter element of the simple roots).
- Yantra incidence: yantra_inc.py (from the sri-yantra study's model); SAT encoding yantra_sat.py (sequential-counter
  cardinality constraints); control with the rational yantra R1.
- Part A: a_items.py (exact Q(√5) with q5.py of the stellation-cycle study; Arb solid angles; exact rational zonal sums).
- All runs on the compute machines through the job runner, under nice.

## Sources and credit

Classical results used and credited: Alexandrov's uniqueness and the monotone-cell lemma (via the stellation-cycle study);
Van Oosterom and Strackee (1983), solid angles; the zonal test of Delsarte, Goethals and Seidel and forced silence of Sobolev and
Goethals–Seidel (via the Tacitus study); the icosahedron inscribed in the octahedron (classical; Coxeter, *Regular Polytopes*,
cited, not opened); reguli (lines meeting three skew lines; classical); Niven-type degree arguments as in the plate-harmony study;
the Sri Yantra model and numbering of Chiodo (2021) and Huet, Kulaichev (1984), as used in study 2026-11-08-sri-yantra; FLINT/Arb
(Johansson); PySAT (Ignatiev, Morgado, Marques-Silva 2018) and CaDiCaL (Biere). Studies read: 2026-11-25-stellation-cycle,
-tacitus, -plate-harmony, -aequi-five-cubes (status only), 2026-11-24-vacuus-resonus-catalogue, -vacuus-build-renders,
2026-11-08-tetra-yantra, -yantra-4d, -sri-yantra. No outside search was run; the novelty of A1–A3 and B1–B2 is not claimed beyond
these sources.

## LEADS

1. A4: when the five-cube sweep ends, test its dice against O ⊂ rTI and the Sunstar (scripts of the stellation-cycle study).
2. B1 OPEN: the conic (regulus) arrangement of directions, to make the combinatorial yantra test exhaustive over all directions,
   starting with the Sunstar (the 3D record, 38 marmas).
3. A2(c): P_t* is a cube-octahedron polyhedron silent beyond symmetry; is any Aequus of the cube frame silent in 4 for the same
   reason (orbit weights in ratio 8 : 9 on C6 and O8)?
4. A3: the same octahedron bridge for the D12/2 die (ratio φ/√(φ + 2)): which polyhedron mediates √(φ + 2)?
5. B2: the internal marmas on the plate lines as a new "nested yantra" along each axis; their spacing along the axis, exactly.
6. A1 into the Vacuus–Resonus paper (§ Aequus): "an Aequus is a polyhedron whose fins divide the sphere into equal parts". To ask
   DICTO where it goes.

## Job record (job runner, all under nice)

| job | host | outcome |
|---|---|---|
| onestruct-pilot | compute node | FINAL ok: 24 skeletons extracted (83 s); cube and icosahedron shadows. Found the centre-detection bug (the projected centre was counted as a marma when a corner projects onto it); fixed before every later run. |
| onestruct-pilot2 | compute node | FINAL ok: timing (TID, Sunstar, 600-cell; under 2 min). |
| onestruct-pilot3 | compute node | **did not end FINAL ok**, because its command printed the results after the FINAL ok line, so the tail check saw none. Its content: the first (backtracking) yantra search, capped at 2 million nodes on the 600-cell vertex-first and Coxeter planes. That search was replaced by the SAT search and deleted, so the pilot is not rerun (method superseded). |
| onestruct-pilot4 | compute node | FINAL ok: a stronger backtracking search, still capped on two shadows. This is why the search was moved to SAT. |
| onestruct-pilot5 | compute node | stopped at the 5-min cap in the 600-cell Coxeter SAT instance (Sunstar UNSAT in 0.08 s). This led to the per-instance time limit. |
| onestruct-control | compute node | the first run gave UNSAT on the yantra itself, which exposed a wrong interior condition for the corner touch (2, 6, 6): the touching leg is t2's, not t6's. Fixed in yantra_inc.py; the control is SAT inside onestruct-sat. No reported result used the wrong condition. |
| onestruct-shadows | compute node | FINAL ok: 7 056 shadows. |
| onestruct-dbbpilot | compute machine | FINAL ok: a_items, yantra_degree (both polynomials irreducible), internal pilot. |
| onestruct-internal | compute machine | FINAL ok, but TID and the snub dodecahedron capped at 4 million candidate pairs; superseded. |
| onestruct-internal2 | compute machine | FINAL ok; TID done (same numbers as run 3); the snub dodecahedron capped (its 9 171 plate lines all meet at O); superseded. |
| onestruct-internal3 | compute machine | FINAL ok: all 18 frames (pairs of two lines through O are skipped and O is counted directly). This is data/internal.json. |
| onestruct-sat | compute node | FINAL ok: control SAT; 7 of 8 shadows UNSAT (the 120-cell Coxeter plane in 1 197 s); the 600-cell Coxeter plane undecided in 1 500 s. |
| onestruct-pencils | compute node | FINAL ok: the 600-cell Coxeter instance split by its 151 pencils: 150 UNSAT within 90 s each, pencil 47 undecided. |
| onestruct-pencil47 | compute node | stopped by me after 9 silent minutes (it printed only at the end; the stall guard fired). Replaced by pencil47b, which prints a start line and a heartbeat. |
| onestruct-pencil47b | compute node | FINAL ok: pencil 47 UNSAT, so all 151 pencils are UNSAT. |

## Files

scripts/: extract.py, shadow_core.py, shadows.py, yantra_inc.py, yantra_sat.py, control_yantra.py, internal.py, a_items.py,
yantra_degree.py, summarize.py. data/: skeletons.json, shadows.json, yantra-sat.json, control-yantra.json,
control-yantra-sat.json, internal.json, a-items.json, yantra-degree.json, tables.md. logs/.
