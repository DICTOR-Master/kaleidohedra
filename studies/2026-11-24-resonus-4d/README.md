# The Resonus in 4D: the regular polytopes, the permutohedron and the walls of #110 (24 Nov 2026)

DICTO · study for the V SF A project. The **Resonus** (DICTO, 24 Nov): for a convex polytope P with centre O, one hyperplane
through O parallel to each facet, parallel facets sharing one (study 2026-11-24-resonus). The **Vacuus** (#110 §2): one
hyperplane through O and each ridge (two-face in 4D), its plate (study 2026-11-24-vacuus-enumeration). **Mirrors**: the
hyperplanes whose reflection maps P to itself.

> **Status box.** Study note, not published. Theorems 1–4 are proved below; every count is exact in Q(√5) (`scripts/resonus_4d.py`,
> log `logs/resonus_4d.log`, 323 exact checks, FINAL ok, 27 s). Nothing running. Prior-art search for Theorems 1 and 2 as stated
> was not done online (LEAD 1).

**Conclusion.**
1. **The conjecture is true.** The Resonus of the 120-cell is exactly the 60 mirrors of H4 (Theorem 3). Its facet normals point
   to the 600-cell's corners, which are the H4 roots (exact reflection test: each of the 120 corners reflects the corner set to itself).
2. **The 600-cell's Resonus is exactly #110's 300 cross walls**, and none of them is a mirror. Its Vacuus is the 60 mirrors.
   So #110's 360 walls of the 600-cell are its Resonus (300) plus its Vacuus (60), with nothing shared.
3. **Two laws, any polytope, any dimension (Theorems 1, 2).** A Resonus hyperplane is a mirror exactly when a reflection of P
   carries the facet to its opposite facet. A Vacuus plate is a mirror exactly when a reflection of P swaps the two facets at the ridge.
   For regular polytopes the second always holds, so **the Vacuus of a regular polytope always lies in its mirrors**; the first
   holds exactly when the facets are centrally symmetric.
4. **The 120-cell is the 4D twin of the rhombic dodecahedron and triacontahedron**: Resonus = Vacuus (60 = 60, both the mirrors).
   The 24-cell is the other 4D case with Resonus = Vacuus (12 = 12, half its 24 mirrors). The 4D permutohedron has its whole
   Resonus (15) inside its Vacuus (65).

## 1. Table (exact; the catalogue fields)

| polytope | mirrors | Resonus (facets each) | Vacuus (ridges each) | Resonus ∩ Vacuus | Resonus on mirrors | Vacuus on mirrors |
|---|---|---|---|---|---|---|
| 5-cell | 10 | 5 (1) | 10 (1) | 0 | 0 | 10 = all |
| tesseract | 16 | 4 (2) | 12 (2) | 0 | 4 | 12 |
| 16-cell | 16 | 8 (2) | 4 (8) | 0 | 0 | 4 |
| 24-cell | 24 | 12 (2) | 12 (8) | **12** (equal) | 12 | 12 |
| 600-cell | 60 | **300** (2) | 60 (20) | 0 | 0 | 60 = all |
| 120-cell | 60 | **60** (2) | 60 (12) | **60** (equal) | 60 = all | 60 = all |
| 4D permutohedron (#105) | 10 | 15 (2) | 65 (2 or 6) | **15** (Resonus ⊂ Vacuus) | 0 | 0 |

Mirrors are found by exact reflection, independently of the facets. f-vectors (corners, edges, two-faces, cells) are checked
against the known ones and Euler's relation: (5,10,10,5), (16,32,24,8), (8,24,32,16), (24,96,96,24), (120,720,1200,600),
(600,1200,720,120), (120,240,150,30). The Vacuus counts agree with the vacuus-enumeration study's Table 4 and with A402191(5) = 65.

What each Resonus is:
- **5-cell:** the 5 hyperplanes "coordinate k = mean" (normals along its own corners; no parallel facets). Its Vacuus is the full A4
  arrangement x_i = x_j.
- **tesseract:** the 4 coordinate hyperplanes x_i = 0 (the short-root mirrors of B4). Vacuus: the 12 long-root mirrors x_i = ±x_j.
- **16-cell:** the 8 hyperplanes ±x₁ ± x₂ ± x₃ + x₄ = 0, not mirrors of B4. Vacuus: the 4 short-root mirrors x_i = 0.
- **24-cell** (corners the permutations of (±1, ±1, 0, 0)): the 12 mirrors of the short roots of F4 (normals (±1,0,0,0), ½(±1,±1,±1,±1));
  the Vacuus is the same 12.
- **600-cell:** 300 hyperplanes, normals along the 120-cell's 600 corners; none a mirror.
- **120-cell:** the 60 mirrors of H4.
- **4D permutohedron:** Σ_{i∈S} y_i = 0 for the 15 splits {S, complement}: the restricted all-subset arrangement A′₅ of
  Kamiya–Takemura–Terao (confirmed exactly; resonus study Theorem 2). All 15 are Vacuus plates: they are the two-valued plates of
  A402191 Theorem A(iv) (n = 5 odd, so every resonance hyperplane occurs). None is a mirror.

## 2. The two laws

Setting: P is a convex polytope in R^d with O = 0 inside it, G its symmetry group (all fix O). Facet F lies on a_F·x = 1, so a_F
is the corner of the polar P\* dual to F. From the resonus study, Theorem 1: the Resonus hyperplane of F is a_F^⊥, and the Vacuus
plate of the ridge F ∩ F′ is (a_F − a_F′)^⊥. A reflection s ∈ G with mirror r^⊥ acts by s(x) = x − 2(x·r)/(r·r) r, and it permutes
the facets, so it permutes the polar corners: s(a_F) = a_{s(F)}.

**Theorem 1 (Resonus law).** The Resonus hyperplane of F is a mirror of P if and only if P has a facet F′ parallel and opposite
to F and some reflection in G maps F to F′. That reflection is then the one in the Resonus hyperplane.

*Proof.* If a_F^⊥ = r^⊥ is a mirror with reflection s, then a_F ∥ r, so s(a_F) = −a_F. Since s permutes the polar corners, −a_F
is the polar corner of a facet F′ = s(F), which lies on −a_F·x = 1: parallel and opposite to F. Conversely, if a reflection s with
root r maps F to such an F′, then s(a_F) = a_{F′} = −a_F, and x − s(x) = 2(x·r)/(r·r) r gives 2a_F ∥ r, so a_F^⊥ = r^⊥. ∎

**Corollary 1.** If −1 ∈ G and the stabiliser of F in G acts on F as F's full symmetry group (true for regular polytopes), then the
Resonus hyperplane of F is a mirror exactly when F is centrally symmetric about its own centre.

*Proof.* Let c = a_F/|a_F|², the centre of F's hyperplane. If s is the reflection in a_F^⊥, then g = −s fixes c and acts as −1
on a_F^⊥: on F's hyperplane it is the point inversion through c. If the Resonus hyperplane is a mirror, s ∈ G, so g ∈ G maps F
to itself, and F is centrally symmetric about c. Conversely, if F is centrally symmetric, its inversion through c is induced by
some g ∈ G fixing F; g fixes c, hence the line of a_F, and is −1 on a_F^⊥ (the linear part of the inversion), so s = −g ∈ G. ∎

For the regular 4-polytopes: cubes, octahedra and dodecahedra are centrally symmetric, tetrahedra are not. So the Resonus lies
in the mirrors for the tesseract, 24-cell and 120-cell (4, 12, 60 hyperplanes) and misses them entirely for the 16-cell and
600-cell; the 5-cell has no parallel facets. This is the "Resonus on mirrors" column, proved.

**Theorem 2 (Vacuus law).** The Vacuus plate of the ridge R = F ∩ F′ is a mirror of P if and only if some reflection in G swaps F
and F′. That reflection is the one in the plate.

*Proof.* If s swaps F and F′, then s(a_F) = a_{F′}, so a_F − a_{F′} ∥ r and the plate (a_F − a_{F′})^⊥ is r^⊥. Conversely, let
the plate H be the mirror of s. Since R ⊂ H, s fixes R pointwise, so it maps F to a facet containing R: F or F′. If s(F) = F,
then s(a_F) = a_F, so a_F ∈ H; likewise s(F′) = F′ and a_{F′} ∈ H; then a_F − a_{F′} ∈ H, but it is also the normal of H, and it
is non-zero. Contradiction. So s swaps F and F′. ∎

**Corollary 2.** For every regular polytope (any dimension), every Vacuus plate is a mirror. *Proof.* The base flag's reflection
ρ_{d−1} swaps the two facets at the base ridge (Coxeter, *Regular Polytopes*), and G is transitive on ridges, so
every ridge has a reflection swapping its two facets. Theorem 2 applies. ∎

This proves the last-but-one column for the six regular 4-polytopes, and explains the vacuus-enumeration finding "each Vacuus lies
entirely in the mirrors"; it is also that study's LEAD 2 ("the edge plates of a polar P\* are mirrors exactly at the edges whose
ends a reflection swaps"), now proved in every dimension. The 4D permutohedron has 0 on mirrors: its symmetry group S5 × {±1} has
only the 10 transposition reflections in 4D, and none swaps two adjacent facets or maps a facet to its opposite (A402191 study,
Theorem A(v)).

## 3. Theorem 3 (the 120-cell and the 600-cell)

**Theorem 3.** Put the 600-cell P with its 120 corners at the unit icosians (the permutations of (±1, 0, 0, 0), all ½(±1, ±1, ±1, ±1),
and the even permutations of ½(±φ, ±1, ±1/φ, 0)), and the 120-cell Q = P\* (in the same frame; the standard 120-cell of radius √8
is the polar of the 600-cell built with odd permutations, checked exactly). Then:
- (a) **Resonus(Q) = the 60 mirrors of H4** = the reflection arrangement of Q's symmetry group.
- (b) **Resonus(P)** = the 300 hyperplanes normal to Q's corners; none is a mirror.
- (c) Vacuus(P) = Vacuus(Q) = the 60 mirrors, with 20 triangles of P and 12 pentagons of Q on each.
- (d) Resonus(Q) = Vacuus(Q); Resonus(P) ∩ Vacuus(P) = ∅.

*Proof.* (a) The resonus study's Theorem 1: the Resonus normals of Q are the corners of Q\* = P, 60 lines. The 120 unit icosians are
the root system H4 (Coxeter, *Regular Polytopes*; Humphreys, *Reflection Groups and Coxeter Groups*): the
reflection in each corner v maps the corner set to itself (checked exactly for all 120), and the reflection group they generate is W(H4), of order 14400, the full symmetry group (Coxeter). It has exactly 60
reflections (exact search: every reflection symmetry moves one of four spanning corners b to another corner w, so its root is
∥ b − w; all 4 × (corners − 1) candidates were tested, for P and for Q). So the 60 Resonus
hyperplanes are the 60 mirrors. Equally, by Corollary 1: Q's cells are dodecahedra, centrally symmetric.
(b) By Corollary 1, tetrahedral cells are not centrally symmetric, so no Resonus hyperplane of P is a mirror. There are 300 because
P's 600 cells come in 300 opposite pairs.
(c) By Corollary 2. Counts by exact computation: 1200/60 = 20 and 720/60 = 12, as in #110 Lemma 3(a).
(d) From (a)–(c). ∎

**When is a Resonus the whole reflection arrangement?** By Theorem 1, Resonus(P) = the mirrors of G exactly when the corner lines
of P\* are exactly the root lines of G. Among the regular polytopes of dimension ≥ 2 this happens **only for the 120-cell**: it needs opposite facets (Theorem 1), which for a regular polytope means −1 ∈ G,
and then centrally symmetric facets (Corollary 1), which leaves the 2m-gons (m of 2m mirrors), the n-cubes (n of n² mirrors), the
24-cell (12 of 24) and the 120-cell (60 of 60). Beyond the regular ones, the same holds for the polar
of any root polytope conv(Φ) whose corners are all the roots and whose symmetry group is W: the rhombic triacontahedron (polar of the icosidodecahedron, the H3
roots) in 3D, and the 120-cell in 4D.

## 4. Theorem 4 (#110's walls)

#110 defines the walls of the 600-cell P as its 60 mirrors and its 300 cross walls, "the hyperplanes through O parallel to a pair of
opposite cells that are not already mirrors", and of the 120-cell Q as its 60 mirrors and the 300 hyperplanes normal to its corner axes.

**Theorem 4.** (a) #110's cross walls are exactly the Resonus of the 600-cell, all 300 of them; #110's mirrors are exactly the
Resonus of the 120-cell. (b) For either Queen X, #110's wall system is **W(X) = Resonus(X) ∪ Resonus(X\*)**, 300 + 60 = 360, disjoint.
For the 600-cell this is also **Resonus(P) ∪ Vacuus(P)**. (c) The 300 cross walls are the Resonus of the 25 inscribed 24-cells,
12 each, all distinct (#110's second description, recomputed here independently). (d) In #110's own frame (sum-zero R⁵, the five
S5-orbits A, −A, B, −B, C3), the Resonus of the 5-cell of S5 is 5 of the cross walls, the planes "coordinate k = mean" that carry C3's
70 faces (#110 Theorem A), and the Vacuus of that 5-cell is the 10 mirrors of S5 shared by A and B (#110 Theorem A).

*Proof.* (a) By Theorem 3(b) no Resonus hyperplane of P is a mirror, so "parallel to a pair of opposite cells, not a mirror" is the
whole Resonus. By Theorem 3(a) the mirrors are Resonus(Q). (b) From (a), with Theorem 3(c) for the second form; for Q, the 300
corner-axis walls are Resonus(Q\*) = Resonus(P) by the resonus study's Theorem 1 (normals along the corners of Q). (c) Exact
computation: the 25 inscribed 24-cells are the orbit of the 24 Hurwitz units under the 60 reflections; each one's Resonus was found
from its own facets; the 25 × 12 hyperplanes are distinct and equal Resonus(P) as sets. (d) Exact computation in #110's frame: the
120 points of the five orbits form a 600-cell (f-vector, Euler), its Resonus contains the 5 hyperplanes y_k = 0 and its mirrors
contain the 10 hyperplanes x_i = x_j. ∎

So in DICTO's terms: the steak of #110 is two Resoni, the White Queen's own (the cross walls) and the Red Queen's (the mirrors), and
the mirrors are at the same time the Vacuus of both Queens. #110's counts (60, 300, 360; 20 triangles and 12 pentagons per mirror)
are reproduced exactly.

## 5. Method and checks

`scripts/qsqrt5.py`: exact arithmetic in Q(√5) (pairs of rationals; signs decided exactly). `scripts/resonus_4d.py`, for each polytope:
1. exact corners (centroid at O and one radius checked);
2. **mirrors by exact reflection**, independent of the facets (candidates b − w for b in four spanning corners);
3. facets through one corner from triples of its nearest corners, kept only if exactly supporting; all facets as their orbit under
   the mirror reflections (each polytope here is corner-transitive under them);
4. ridges = pairs of facets meeting in a plane; edges = sides of the ridge polygons (exact side test);
   **f-vector equals the known one, Euler's relation holds, every ridge lies in exactly two facets**;
5. Resonus = lines of the a_F; Vacuus normal computed **twice** (a_F − a_F′, and the exact null vector of the ridge's corners),
   equal for every ridge;
6. cross-checks: the 120 icosians are closed under their own reflections; the standard 120-cell's corner lines equal the 600-cell's
   Resonus (in the matching frame); the 25 inscribed 24-cells; #110's frame; the permutohedron against A′₅.
Run on the compute host in 27 s (log `logs/resonus_4d.log`, 323 checks, FINAL ok); results `data/resonus_4d.json`.

## Sources checked

#110 *Walls of Silence* v3 (paper.html: §2 definitions of mirrors and cross walls, Lemma 3, Theorems A, B); #105 (4D Vacuus,
65 plates); studies 2026-11-24-resonus (Theorem 1, the polar link; Theorem 2, the permutohedron), 2026-11-24-vacuus-enumeration
(§5 and Table 4, the 4D Vacuus; LEAD 2), 2026-11-24-a402191-vacuus (Theorem A). Classical facts used and credited at point of use:
Coxeter, *Regular Polytopes* (flag reflections; the 600-cell and 120-cell coordinates and H4); Humphreys, *Reflection Groups and
Coxeter Groups* (H4 roots as icosians); Kamiya–Takemura–Terao 2011 (the restricted all-subset arrangement); Schoute and Denney et
al. (the 25 inscribed 24-cells, via #110). The catalogue study 2026-11-24-vacuus-resonus-catalogue had no README yet; its fields
were matched as Resonus count, Vacuus count and their overlap.

## LEADS

1. Prior art: search whether Theorems 1 and 2 (a central hyperplane parallel to a facet, or through a ridge, is a mirror exactly
   when a reflection carries the facet to its opposite, or swaps the ridge's two facets) are stated anywhere.
2. 3D check of Corollary 1: the Resonus on mirrors should be exactly the solids whose opposite faces a reflection exchanges
   (cube 3 of 9; rhombic dodecahedron 6 of 9; rhombic triacontahedron 15 of 15). Test it on the vacuus-enumeration rows.
3. The other uniform 4D polytopes (the A4, B4, F4, H4 families): which have Resonus = Vacuus, as the 24-cell and 120-cell do?
4. The 4D permutohedron's Resonus ⊂ Vacuus holds for every odd n (A402191 Theorem A(iv)); for even n only half. A one-line law?
