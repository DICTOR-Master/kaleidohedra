# Star Cores studies 1 and 2: exact gains, the polar-spike fill, and the cores' two-turn cycle (DICTO, 2026-10-30)

**One-line conclusion.** All ten closed chains of DICTO's growth rule T (#38) are confirmed exactly, with exact gains. The polar-spike fill
is proved for every convex solid with its centre inside, and checked exactly on all ten.
**Status:** done (exact, in each solid's own field: Q(√5), Q, Q(∛2)). Prior art for the theorem: see below.

## 1. Closed chains of T, exact (dataset v6 coordinates; T(S) = {x : v·x ≤ v·v for every corner v})

| Solid | Symmetry | Enters cycle | Period | Radius gain per period | Field norm of the gain |
|---|---|---|---|---|---|
| GTI, FPD, Palintriacontahedron (one orbit) | Ih | at once | 4 | 35 − 15√5 = 10/φ⁴ ≈ 1.4590 | 2²·5² |
| Icosaxes | Oh | at once | 4 | 65 − 28√5 ≈ 2.3901 | 5·61 |
| Unborn Axes | Oh | at once | 4 | (72 − 27√5)/5 ≈ 2.3252 | 3⁴·19/5² |
| Metaxyhexecontahedron | Ih | at once | 4 | 939725/9 − 140084√5/3 ≈ 1.4400 | 5·2081·2341/3⁴ |
| Tweedledum | Ih | at once | 4 | 293 − 652√5/5 ≈ 1.4167 | 41·101/5 |
| Samson | Td | after one step | 4 | r² in Q(∛2) (cubic, data/gains.txt) ≈ 3.8555 | r²: 83²·64283²/(5⁴·23⁴) |
| David | D2d | at once | 2 | 10 | 2·5 |
| Delilah | Oh | at once | 2 | 3 | 3 |

The return is checked exactly: every corner of the returning step is k times a corner of the earlier step (parallel, with the exact squared
ratio). The GTI orbit's gain is 10/φ⁴, the same as ID's in #38. Samson's own shape is not on its cycle: its first step is.
Fixed: the float survey's "recognised" gains for Metaxyhexecontahedron, Tweedledum and Samson (mixing √2, √3, √5) were wrong; these are the exact ones.

## 2. The polar-spike fill: theorem and exact check

**Theorem.** Let P be a convex solid with the centre O inside, R its circumradius, and ρ > R. Put each spike's tip at the pole of its face
plane n·x = c in the sphere of radius ρ, p = ρ² n / c. Then the hull of the tips (the halo) is the polar of P, and the layer between the
star (P with its spikes) and the halo is filled exactly, with no overlaps and no gaps, by one pyramid over each corner v (base: the tips of
the faces round v, which lie in the plane v·x = ρ²) and one tetrahedron over each edge ab (corners a, b and the tips of its two faces).

**Proof.** The pieces fit face to face: each spike side (a, b, p_f) is shared with the edge tetrahedron of ab, each triangle (v, p_f, p_g) of a
corner pyramid with the tetrahedron of the edge between f and g, and the outer faces left over are exactly the halo's facets. So the pieces
cover the halo exactly once as soon as each piece has positive volume. Spike: p_f lies beyond its face since ρ² > c². Corner pyramid: v lies
below its plane v·x = ρ² since |v|² ≤ R² < ρ². Edge tetrahedron: projecting along the edge, its orientation is the sign of ρ² − d², with
d the distance from O to the edge line (a two-line calculation in the plane across the edge); d ≤ R < ρ. ∎
At ρ = midradius on a solid with a midsphere every edge tetrahedron is flat: the edge and its dual edge cross, and the layer becomes the
rhombic faces of Conway's join. So the theorem is the "thick" version of the join, valid for every convex solid and every ρ > R.

**Exact check:** for all ten solids above, at ×2 (and ×φ for the Q(√5) solids), every piece has nonzero volume of one orientation per kind,
and the pieces add up exactly to the halo's volume (data/study1.json, `polar`).

Files: scripts/study1.py (exact, uses the dataset's exactlib), scripts/gains.py; data/study1.json, study1.log, gains.txt. Run on dicto-big-brother.

## 3. Prior art for the theorem (searched 2026-10-30)

**Verdict:** the ingredients are classical, and the decomposition itself is elementary. We found no source that states it with the
condition ρ > R. The papers present it as a lemma with its proof, not as a discovery.
- Polar reciprocation, with the polar's corners at the poles of the face planes: classical (Wikipedia, "Dual polyhedron", read).
- At the midsphere, a solid and its dual cross edge to edge, and the hull's faces are the rhombi of Conway's join, jX = daX (G. W. Hart,
  "Conway Notation for Polyhedra", georgehart.com; Wikipedia, "Conway polyhedron notation"; Antiprism `conway` and `pol_recip` docs, read).
- The hull Π+ of a regular polytope and its reciprocal, and their common core Π−: H. S. M. Coxeter, "Reciprocating the Regular Polytopes",
  J. London Math. Soc. 55 (1997) 549–557. Only the abstract was read (the full text is paywalled).
- Not read: D. Eppstein's COMB-01 slides (the fetch failed), which a search snippet links to hulls of a polytope and its polar.
- Library (`ask-library`, 4 queries: hull of a polyhedron and its dual/join; polar spikes and Kleetope; dissection between a polyhedron and its
  polar; Conway notation, join, kis and the midsphere): no relevant hit. The closest were O'Rourke 2023 "Polar Zonohedra Edge-Unfold to Nets"
  (on unfolding) and Cunningham–Mixer 2016 "Internal and external duality in abstract polytopes" (combinatorial).
- Web queries: "convex hull of a polyhedron and its polar reciprocal dual compound triangulated faces kis join"; "Conway polyhedron notation
  join operator dual of ambo rhombic faces canonical compound"; "Eppstein Kuperberg Ziegler fat 4-polytopes edge-tangent"; "Reciprocating
  the regular polytopes".

## 4. Study 2: the core of each turn, followed exactly (scripts/study2.py; data/study2.json, study2.log)

**One-line conclusion.** For all ten solids the cores alternate with period two, either at once or after one turn. Two turns
scale the core by t² cos²θ, where θ is the angle between the two kinds of symmetry axis that carry its faces. This proves the plan's
main statement for two families of planes.

| Solid | Core cycle from turn | Period | Cores (corners; faces) | Two-turn radius scale |
|---|---|---|---|---|
| GTI | 0 | 2 | GTI ↔ 30 corners (20 triangles, 12 pentagons) | t²(5+2√5)/15 |
| FPD, Palintriacontahedron | 1 | 2 | 60 corners (12 pentagons, 20 hexagons) ↔ 30 corners (20 triangles, 12 pentagons) | t²(5+2√5)/15 |
| Metaxyhexecontahedron | 1 | 2 | 60 corners (12 pentagons, 20 hexagons) ↔ 60 corners (20 triangles, 12 decagons) | t²(5+2√5)/15 |
| Tweedledum | 1 | 2 | 60 corners (12 pentagons, 20 hexagons) ↔ the same kinds, other proportions | t²(5+2√5)/15 |
| Icosaxes | 0 | 2 | 24 corners (6 squares, 8 hexagons), two proportions | t²/3 |
| Unborn Axes | 0 | 2 | 24 corners (8 triangles, 6 octagons) ↔ 24 corners (6 squares, 8 hexagons) | t²/3 |
| Delilah | 0 | 2 | cube ↔ octahedron | t²/3 |
| Samson | 1 | 2 | 12 corners (4 triangles, 4 hexagons), two proportions | t²/9 |
| David | 0 | 2 | its own 4-face shape (one family) | t²/10 |

The face-transitive solids (one family of faces: FPD, Palintriacontahedron, Metaxyhexecontahedron, Tweedledum) take one turn to reach
two families on the symmetry axes. From then on they alternate like everything else. Their T-chains have period four (study 1), while
their cores have period two.

**Proposition (two families on two kinds of axis).** Let a core's faces lie on two families: family A perpendicular to one kind of axis
(say the 5-fold axes) at distance h_A, and family B perpendicular to another (the 3-fold axes) at distance h_B. Let θ be the angle from
an axis of the first kind to the nearest axis of the second kind. Then the next core again has faces on the same two kinds of axis, with
the distances swapped and scaled: h_A' = t cosθ · h_B and h_B' = t cosθ · h_A. So two turns scale the core by t² cos²θ and give back its
shape.
*Proof.* The tips of family A lie on the A-axes at distance t h_A. Their hull is the regular solid with corners on those axes (the
icosahedron for the 5-fold axes), whose faces are perpendicular to the B-axes at distance t h_A cosθ. Likewise the hull of the B tips has
faces perpendicular to the A-axes at distance t h_B cosθ. The core is the intersection of the two hulls. ∎
The values: icosahedral (5-fold to 3-fold) cos²θ = (5+2√5)/15, which is #78's TI value, now seen to hold for every icosahedral two-family
core; octahedral (4-fold to 3-fold) cos²θ = 1/3; tetrahedral (one 3-fold axis to the other kind of 3-fold axis) cos²θ = 1/9. The proof needs
both families to cut the core, which holds for all ten. The exact runs match the formula in every case. David (D2d, one family of
four faces) is the only case outside the proposition: its own two-turn scale is 1/10.
