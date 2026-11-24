# The associahedron shell, part 2: two patterns overlaid (24 Nov 2026)

DICTO · project V SF A (Vacuus, Scutoid Frusta, Aequus). LEAD 1 of study 2026-11-24-associahedron-shell. "Scutoid Frusta",
"amber cell" and the combined method are DICTO's. The division rules have plain working descriptions only, not names.

> **Status box.** Study note, not published. Every count and check is exact, in the same towers of real quadratic fields as the
> first study (Q(√3), Q(√2)(√3), Q(√5)(√3)(√((5+√5)/2))). Floats appear only in the JSON preview coordinates. LEAD 3 of the first
> study (enlarged mould) was not run, because LEAD 1 already gives Y-corners. Resume: everything committed; nothing running.

**Verdict.** Overlaying the two patterns gives **convex Scutoid Frusta proper, which change their side count and their neighbours**.
It happens in B3 (linear c: SF 3-4-1 once, SF 6-5-1 twice) and in H3 (linear c: 4 pieces; bipartite c: 14 pieces, among them SF 3-4-1,
4-5-1, 5-4-1, 5-6-1, 6-7-1, 8-7-1 and 9-10-1). Each Y-corner sits where the two patterns cross, or at a corner of the associahedron's
own pattern. Neither pattern alone gives a single Scutoid Frustum proper in this shell, and Lemma B says why for the outer one.
A3 gives none in any division.

## 1. The two patterns and their overlay

The shell is Asso_c minus P, as in the first study (P the uniform permutahedron, Asso_c the Hohlweg–Lange–Thomas
c-associahedron, arXiv 0709.4241). It has zero thickness on the kept faces. DICTO's combined method fills both ends first: the core's
faces inside, a pattern on the mould outside. Here both patterns are grown at equal speed, each from its own side.

- **Inner pattern I (equal-speed, from P outward).** The first study's rule: piece_I(R) = {x ∈ Asso_c : d_R(x) ≥ 0, d_R(x) ≥ d_R'(x)
  for every removed R'}, with d the Euclidean distance to the face plane. This is the straight skeleton of the outward offset.
- **Outer pattern O (nearest associahedron face, from Asso_c inward).** cell(A) = {x ∈ Asso_c : D_A(x) ≤ D_A'(x) for every face A'
  of Asso_c}, with D_A(x) the distance from x to the plane of A. This is the inward straight skeleton of Asso_c (a standard
  construction). piece_O(A) = cell(A) minus the interior of P. Its outer end is the whole shell part of A, and it is flat.
- **Overlay I ∧ O.** The common refinement: piece(R, A) = piece_I(R) ∩ cell(A). Each such piece is convex, and it has at most one
  inner face (a part of R) and at most one outer face (a part of A).

Each piece is classified under the decided definition (study 2026-11-24-scutoid-frusta-enumeration, "Decisions (24 Nov)").
The ends are the faces on P and on Asso_c. They must be disjoint. The piece must be simple, and every lateral face must meet an
end along an edge. A Y-corner is a vertex on neither end. A piece meeting all this with one flat face per end is a **convex** Scutoid
Frustum. Its type is SF n-m-k, with n inner sides, m outer sides and k Y-corners.

## 2. Results (`scripts/shell2.py`, `logs/shell2.log`, `data/shell2-*.json`)

c and c⁻¹ give the same piece-type lists in every case, so each row stands for both. "Proper" means k ≥ 1.

| group | c | overlay pieces | convex Scutoid Frusta proper (k ≥ 1) | convex frusta (k = 0) | not Scutoid Frusta |
|---|---|---|---|---|---|
| A3 | linear | 16 | 0 | 0 | 16 (ends meet) |
| A3 | bipartite | 15 | 0 | 1 (SF 4-4-0) | 14 (ends meet) |
| B3 | linear | 33 | **3**: SF 3-4-1, 2 × SF 6-5-1 | 4 (3 × SF 4-4-0, SF 6-6-0) | 26 (ends meet) |
| B3 | bipartite | 34 | 0 | 10 (2 × 3-3-0, 5 × 4-4-0, 2 × 5-5-0, 6-6-0) | 24 (ends meet) |
| H3 | linear | 84 | **4**: SF 3-4-1, SF 6-6-2, 2 × SF 9-7-2 | 30 | 50 (46 ends meet, 1 no inner end, 1 no outer end, 2 with a lateral face meeting no end) |
| H3 | bipartite | 86 | **14**: 2 × SF 3-4-1, SF 4-4-2, SF 4-5-1, 3 × SF 5-4-1, SF 5-5-2, SF 5-6-1, SF 6-6-2, SF 6-7-1, SF 7-7-2, SF 8-7-1, SF 9-10-1 | 24 | 48 (44 ends meet, 3 no inner end, 1 no outer end) |

The H3 frusta are SF 4-4-0 (14 / 14), SF 5-5-0 (7 / 4), SF 6-6-0 (3 / 2), SF 7-7-0 (5 / 4) and SF 8-8-0 (1 / 0), for linear / bipartite c.
**Every Scutoid Frustum proper changes its neighbours** between the inner and the outer end. The law Y ≥ |n − m|, Y ≡ n + m (mod 2) holds
for all 90 pieces that meet the definition (one c of each pair: 0 / 1 / 7 / 10 / 34 / 38). That is expected, since Proposition 1 proves it for this class.

**Where the Y-corners are.** Each is labelled by the three walls that meet there: W for a wall of the inner pattern, O for one of the
outer pattern.

| group, c | OOO | OOW | OWW | WWW |
|---|---|---|---|---|
| B3 linear | 3 | 0 | 0 | 0 |
| H3 linear | 1 | 6 | 0 | 0 |
| H3 bipartite | 0 | 9 | 9 | 0 |

(Counted over the Scutoid Frusta proper; a corner shared by two such pieces is counted in each.)

**The two patterns alone.** The inner pattern alone reproduces the first study (no Y-corner; the ends meet in 5, 14 / 13 and 28 / 27
pieces). The outer pattern alone has 8 / 7 pieces (A3), 10 / 9 (B3) and 14 / 13 (H3), counted linear / bipartite. Each has a bent inner
end. Some do have Y-corners: 4 pieces in B3 linear and 4 in H3 linear, all of kind OOO. But **in every one of them the two ends meet**,
as Lemma B requires.

**Exact checks, all passed in all 12 runs** (3 groups × 4 Coxeter elements):
- the overlay volumes add up to vol(Asso_c) − vol(P), and so do the inner pieces;
- the outer cells add up to vol(Asso_c);
- for each removed face R, the overlay pieces add up to piece_I(R);
- for each associahedron face A, they add up to vol(cell(A)) − vol(cell(A) ∩ P);
- every wall (W or O) matches its partner piece vertex for vertex;
- the inner ends tile each removed face, by area;
- the outer ends tile each associahedron face minus its kept face, by area;
- every overlay piece is a closed surface with V − E + F = 2;
- every Y-corner lies strictly outside P and strictly inside Asso_c (exact signs).

## 3. Lemmas

**Lemma B (outer pattern: no Scutoid Frustum, ever).** In the zero-thickness shell, every piece of the nearest-associahedron-face
division either has no outer end or has two ends that meet. *Proof.* Let A be a face of Asso_c and K_A the kept face of P in its plane,
so K_A ⊆ A. If K_A = A, the shell part of A is empty and piece_O(A) has no outer end. Otherwise K_A is a convex polygon properly contained in
the convex polygon A. If every edge of K_A lay in the boundary of A, the boundary curve of K_A would be that of A and K_A = A. So some
edge e of K_A is not contained in the boundary of A. Its relative interior then misses the boundary of A: a segment in a convex polygon
that touches the boundary at an inner point of the segment lies along a boundary edge. The face of P across e is not in the plane of A.
It is not a kept face K' either: then e would lie in A ∩ A', which is in the boundary of A. So it is a removed face R, and e lies on the
inner surface of the shell. Every point x in the relative interior of e has D_A(x) = 0 and D_A'(x) > 0 for every other face A'
(x is in the relative interior of A, the only face of Asso_c through x), so x ∈ cell(A). The segment e therefore lies in the inner end (on R) and in the outer end
(on A) of piece_O(A). ∎ Lemma A of the first study is the same statement for the inner pattern, for every removed face with a kept
neighbour.

**Lemma C (where Y-corners can be, in the overlay).** Let v be a Y-corner of an overlay piece piece(R, A). Then v lies in the open shell,
on at least three walls, and these are of kinds WWW, WWO, WOO or OOO. *Proof.* If x ∈ piece_I(R) also lies in P, then d_R(x) ≤ 0
(x ∈ P) and d_R(x) ≥ 0 (x ∈ piece_I(R)), so x is on the plane of R. Likewise inside cell(A), x ∈ ∂Asso_c forces D_A(x) = 0. Hence the only
faces of the piece on ∂P or ∂Asso_c lie in the planes of R and A, which are its ends, and a vertex on neither end lies on at least three
of the remaining faces, which are walls. (The exact check above confirms that v is strictly inside the shell.) ∎
WWW is a corner of the inner pattern and OOO a corner of the outer one. WWO is an edge of the inner pattern passing through an outer
wall, and WOO is an edge of the outer pattern passing through an inner wall. So OOW and OWW Y-corners are **crossings of the two
patterns**, which is the scutoid mechanism. WWW never occurs here. The first study found that the inner pattern has no corner in the
open shell, in all 24 cases (12 equal-speed, 12 cone).

**Theorem 1 (two patterns give side-changing Scutoid Frusta).** In the shell between the uniform H3 permutahedron (the truncated
icosidodecahedron) and the hidden H3 associahedron, for each of the four Coxeter elements c, the overlay of the two equal-speed
patterns has 4 (linear c) or 14 (bipartite c) pieces that are convex Scutoid Frusta proper. The types are listed in the table. 13 of these 18
pieces have n ≠ m. Eleven have exactly one Y-corner: SF 3-4-1 (3 of them), SF 4-5-1, SF 5-4-1 (3), SF 5-6-1, SF 6-7-1, SF 8-7-1 and
SF 9-10-1. The other two are SF 9-7-2 (linear c). In B3 linear c the overlay has SF 3-4-1 and 2 × SF 6-5-1. Every one of them changes its neighbours
between its ends. *Proof.* An exact computation (`scripts/shell2.py`) gives each piece as an exact convex polyhedron cut out by half-spaces.
It decides its faces and vertices by exact sign tests in the tower field (the fields are justified in the first study, §4). It then reads
off the type, under the checks listed above. ∎

**So, which divisions can never give Y-corners, or never Scutoid Frusta?** In this zero-thickness shell:
(i) any division in which a piece contains a rim edge R ∩ K of P fails for that piece, since its ends meet (Lemma A, in a form that
does not depend on the rule);
(ii) the outer pattern alone never gives a Scutoid Frustum (Lemma B, proved for every group and every c);
(iii) the inner pattern alone gives none in the 12 equal-speed cases computed (24 with the cone rule). That is Lemma A, together with the computed fact that it has no
corner in the open shell; for the inner pattern that fact is an observation, not a proof.
The Scutoid Frusta proper all arise in the overlay, away from the rim, at crossings of the two patterns or at corners of the outer
pattern (Lemma C).

## 4. Method and exactness

`scripts/shell2.py` imports the first study's `shell.py` unchanged (tower field, groups, exact clipping). Its function `geometry` is
copied from that study's `run()` up to the construction of Asso_c. The outer cells are cut from Asso_c by the bisector half-spaces
D_A ≤ D_A'. Each overlay piece is piece_I(R) clipped by the wall planes of cell(A). The pieces of each single pattern are
classified as unions of their overlay parts. A corner of a union is a point on at least three of its boundary planes whose normals
are independent, tested exactly with determinants. Labels in the data: ("R", r) is a removed face of P (inner end), ("F", a) an
associahedron face (outer end), ("W", r') a wall of the inner pattern, ("O", a') a wall of the outer pattern.

**Fault (fixed, same session).** `from shell import *` also imported the first study's folder variables, so the first full run wrote
its JSON into the first study's data folder. The JSON was moved here unchanged. The script now computes its own folder after the import and
asserts it. The first study's committed files were not touched.

Run: `python scripts/shell2.py A3 B3 H3` (A3 2 s, B3 15 s, H3 about 3 min on one core). The log ends FINAL ok.
`--c <name>` restricts the run to one Coxeter element.

## 5. Sources checked

Hohlweg, Lange, Thomas (arXiv 0709.4241; Adv. Math. 226 (2011)), through the first study and 2026-11-24-permutahedron-leads.
The Scutoid Frusta definition, Proposition 1 (the law) and the 24 Nov decisions are in 2026-11-24-scutoid-frusta-enumeration.
Gómez-Gálvez et al. 2018 (Nat. Commun. 9, 2960) is the source of the biological picture in which neighbours change between two
surfaces: there the scutoid comes from Voronoi patterns that differ between the surfaces. The straight skeleton, inner and outer, is
standard (Aichholzer, Aurenhammer, Alberts, Gärtner 1995, for polygons; the 3D offset form used here is the same idea). No source on
dividing a permutahedron–associahedron shell was found. This is not a prior-art search.

## 6. LEADS

1. **Enlarged mould (LEAD 3 of the first study).** Scale Asso_c by λ > 1 so that the shell has thickness everywhere. Lemmas A and B
   then no longer apply, and many more pieces should qualify. This is an amber cell with an associahedral mould.
2. **Prove that the inner pattern has no corner in the open shell** (the observation in (iii)), or find the reason.
3. **Pictures** of H3 bipartite SF 9-10-1 and SF 3-4-1 inside the shell, with the two patterns drawn on the two ends. The data has
   the preview coordinates.
4. **A tiling statement.** The overlay is a division of the shell, but it is not a tiling by one kind of piece. Whether one SF type
   from here also tiles space alone is open.
