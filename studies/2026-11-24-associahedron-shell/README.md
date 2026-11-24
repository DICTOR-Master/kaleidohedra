# The associahedron shell (24 Nov 2026)

DICTO · project V SF A (Vacuus, Scutoid Frusta, Aequus). This is LEAD 2 of study 2026-11-24-permutahedron-leads. "Scutoid Frusta",
"amber cell" and the combined method are DICTO's. The two division rules below have plain working descriptions only, not names.

> **Status box.** Study note, not published. Every count and check is exact. Numbers lie in towers of real quadratic fields:
> Q(√3) for A3, Q(√2)(√3) for B3, Q(√5)(√3)(√((5+√5)/2)) for H3. Signs are decided exactly, and floats appear only in the JSON
> preview coordinates. One fault came up and was fixed (below). Resume: everything committed; nothing running.

**Verdict.** Each hidden associahedron has a shell around its permutahedron. That shell divides cleanly, with one piece standing on
each removed face. But **no piece is a Scutoid Frustum proper, in any of the 24 cases** (3 groups × 4 Coxeter elements × 2 rules).
No piece has a Y-corner, and no piece changes its neighbours between inside and outside. The two patterns do differ (Lemma 3 says
they must), but that is not enough: within the shell the walls never meet. Most pieces fail the definition earlier still. Their two
ends touch along the rim where a removed face meets a kept one, and this cannot be avoided (Lemma A). The pieces with disjoint ends
are all frusta: 0 / 1 / 16–17 per shell (A3 / B3 / H3), including 4 to 7 convex frusta SF 4-4-0 and SF 6-6-0 in H3. **Side count:
no piece changes it** when it is counted by walls (neighbours). Counted by the edges of the outer end, many pieces do change, but only
because that end bends over the associahedron's edges. Those are not Y-corners.

## 1. Setting

The shell runs from the permutahedron P (uniform, the same coordinates as study 2026-11-24-permutahedron-leads) out to the
c-associahedron Asso_c of Hohlweg–Lange–Thomas (arXiv 0709.4241; Adv. Math. 226 (2011)). That is Asso_c minus P. The kept faces of
P (9 / 12 / 18) lie on the associahedron's faces, so the shell has zero thickness there. The shell is the cap over the removed faces
(5 / 14 / 44). For every group and every c it is **one connected cap** whose rim is a closed chain of edges between removed and kept
faces. The rim has 16, 14 edges for A3 (linear, bipartite); 26, 24 for B3; and 46, 44 for H3.

## 2. Division rule (decided from the combined method)

DICTO's combined method fills the two ends first: the core's faces inside, a pattern on the mould outside. It then cuts the resin to fit.
Here the core is P, the mould is Asso_c, and the outer pattern is the associahedron's own faces. The rule decided on, as its
straight-skeleton form:

- **Equal-speed rule (main).** The kept faces of P stay where they are. Every removed face moves outward, parallel to itself, at the same
  speed, until the solid fills Asso_c: P_t = {kept inequalities, d_R ≤ t for every removed R}, where d_R is the Euclidean distance
  to the plane of R. Each point of the shell belongs to the face that reaches it first:
  piece(R) = {x ∈ Asso_c : d_R(x) ≥ 0, d_R(x) ≥ d_F(x) for every removed F}.
  The inner end is exactly the face R. The outer end is the part of the associahedron's surface inside the piece, made of
  associahedron faces. Walls are the bisector planes, and a Y-corner would be a vertex where three walls meet inside the shell.
  Every piece is convex, being cut out by planes.
- **Cone rule (baseline).** The same, with d_R replaced by the gauge (n_R·x − b_R)/b_R. The walls are then planes through the centre,
  as in Lemma 3 of the permutahedron-leads study.

## 3. Results (`scripts/shell.py`, `logs/shell.log`, `data/shell-*.json`; table by `scripts/summary.py`)

| group | c | pieces | Y-corners | neighbours change | ends disjoint | convex frusta | frusta (general tier, bent outer end) | ends meet (not SF) |
|---|---|---|---|---|---|---|---|---|
| A3 | linear (both) | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| A3 | bipartite (both) | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| B3 | linear (both) | 14 | 0 | 0 | 0 | 0 | 0 | 14 |
| B3 | bipartite (both) | 14 | 0 | 0 | 1 | 0 | 1 (a square) | 13 |
| H3 | linear (both), equal-speed | 44 | 0 | 0 | 16 | 6 (5 × SF 4-4-0, 1 × SF 6-6-0) | 10 | 28 |
| H3 | linear (both), cone | 44 | 0 | 0 | 16 | 7 | 9 | 28 |
| H3 | bipartite (both), equal-speed | 44 | 0 | 0 | 17 | 4 (3 × SF 4-4-0, 1 × SF 6-6-0) | 13 | 27 |
| H3 | bipartite (both), cone | 44 | 0 | 0 | 17 | 6 | 11 | 27 |

For A3 and B3 the two rules give the same combinatorial types, though not the same shapes. In H3 they differ only in how many
associahedron faces an outer end crosses. "Both" means that c and c⁻¹ give equal multisets of piece types in every case, which fits
the known isometry Asso_c ≅ Asso_{c⁻¹}. The full type lists, one line per type (face sides, inner walls, rim edges, outer faces,
outer edges, Y, shared end vertices, simplicity, tier), are in the log.

**Exact checks, all passed in all 24 runs:**
- the piece volumes add up to vol(Asso_c) − vol(P);
- the inner end of each piece equals its removed face, vertex for vertex;
- every wall appears in exactly the two pieces it separates, with equal vertex sets;
- for each associahedron face, the outer faces of the pieces add up to area(associahedron face) − area(kept face of P);
- every piece is a closed surface with V − E + F = 2, and every vertex has degree 3;
- P has |W| corners and 14 / 26 / 62 faces; Asso_c has 14 / 20 / 32 corners (the W-Catalan numbers), as before.

**Laws Y ≥ |n − m|, Y ≡ n + m (mod 2).** They hold for every piece (44 of 44 and so on) when n and m count wall neighbours inside
and outside. Every piece has Y = 0 and n = m. They fail for many pieces when m counts the edges of a bent outer end. That is expected,
because the law is proved for flat ends.

**Side count (against Lemma 3).** Lemma 3 says homothetic shells give frusta only. In this shell the patterns differ, yet
**0 pieces change their side count** by walls. By outer-end edges the counts are 5 of 5 (A3), 10 / 12 of 14 (B3) and 23–29 of 44
(H3). Every one of those comes from bending over associahedron edges, none from a Y-corner. So two different patterns are needed for
Scutoid Frusta, but they are not enough.

**Lemma A (the rim; by hand).** Take any division of this shell in which each piece's inner end is a whole removed face R. Then every
R with a kept neighbour K gives a piece whose two ends meet. *Proof.* The edge R ∩ K lies in K, and K lies in a face of Asso_c, so
the edge lies on the outer surface as well as in R. ∎ So under the decided definition (two disjoint ends) such pieces are never
Scutoid Frusta, whatever the rule. The candidates are only the removed faces with no kept neighbour: 0, 1 and 16–17 of them.

**Why no Y-corner (observation, not proved).** A Y-corner needs a wall between two removed faces to shrink to nothing before the growth
reaches the associahedron. In all 24 runs every wall reaches the associahedron first. The kept faces do not move, and they hold each
cap open along its whole rim.

## 4. Method and exactness

The code is self-contained, with no sympy. The tower field stores a + b√r as nested pairs over Fractions. A sign is decided by
comparing a² with b²r, recursively. This is exact provided each radicand is not a square in the field below. For 3, 2 and 5 over Q
that is clear. 3 over Q(√2) or Q(√5): x² + d y² = 3 with xy = 0 has no rational solution. (5+√5)/2 over Q(√5)(√3): its norm to
Q is 5, not a square, and (5+√5)/6 has norm 5/9, also not a square. The unit normals are exact: |n|·(1/|n|) = 1 is asserted.
Polytopes are built by exact half-space clipping, from a box through P and Asso_c to each piece. The group, the facets and the
c-singletons follow `assoc.py` of the permutahedron-leads study (logic re-implemented in the new field; the counts agree with that study).

**Fault (fixed, same session).** In the first full run H3 stopped on "empty piece". The base-field square root could return the
negative root for the five-fold normals, which turned the weights negative. Fixed by taking the positive root. Guard: the unit normal
is now asserted positive with norm exactly 1. A3 and B3 were not affected (their roots took the positive branch), and the rerun
reproduced them.

Run: `python scripts/shell.py A3 B3 H3` (A3 0.4 s, B3 5 s, H3 69 s), then
`python scripts/summary.py`. The log ends FINAL ok.

## 5. Sources checked

Hohlweg, Lange, Thomas (as above, through study 2026-11-24-permutahedron-leads §1). DICTO's combined method and amber cell: #117 and
the amber-cell sweep README (2026-11-21-amber-cell-sweep), and the draft #118 (papers/2026-11-22-amber-ammann). The Scutoid Frusta
definition and its decisions are in study 2026-11-24-scutoid-frusta-enumeration. The equal-speed rule is the straight skeleton of
the outward offset, a standard construction. No source on shells between a permutahedron and an associahedron divided into pieces
was searched for or found. This is not a prior-art search.

## 6. LEADS

1. **Outer pattern by distance from the associahedron's faces.** Assign each point to its nearest associahedron face, so that the
   outer ends are flat and whole. Then refine this together with the equal-speed cells. Pieces in the refinement could change
   neighbours where the two divisions cross. This is the most direct route to Y-corners in this shell.
2. **The amber-sweep outer pattern.** Use the Voronoi pattern of the face centroids on Asso_c, as in `amber.py`, with the zero-thickness
   rule (1) of that script for the kept faces.
3. **Thicken the rim.** Use Asso_c scaled by λ > 1 about the centre (or another point a inside the chamber) as the mould, so that the
   ends no longer meet (Lemma A no longer applies). This is an amber cell with an associahedral mould.
4. **4D.** The same computation for the A4 associahedron shell (Loday); the clipping code is 3D only and needs extending.
