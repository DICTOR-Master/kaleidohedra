# Star Cores study 1: exact gains and the polar-spike fill (DICTO, 2026-10-30)

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
