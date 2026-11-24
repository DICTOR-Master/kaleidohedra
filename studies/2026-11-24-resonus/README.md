# The Resonus: polar link, permutahedra, name check (24 Nov 2026)

DICTO · study for the V SF A project. The **Resonus** (plural Resoni) is DICTO's name (24 Nov): for a convex solid P with centre O, the
set of planes through O, one parallel to each face (equal planes merged). For a centrally symmetric solid these are the middle planes
between opposite faces. It is the sibling of the **Vacuus** (#110: one plane through O and each edge; definition in study
2026-11-24-vacuus-enumeration, Section 1). In that study and in 2026-11-24-permutahedron-leads the Resonus was called "face-parallel
planes" or "face plates"; it is the same object.

> **Status box.** Study note, not published. Theorems 1 and 2 are proved below. Every count is exact: Q(√5) arithmetic for the
> solids, finite-field point counts for the region numbers. The 31-line identification in Theorem 3 matches every invariant in
> Grünbaum's table, but it is not proved to be an isomorphism (LEAD 1). Resume: everything committed; nothing running.

**Conclusion.**
1. **Polar link (Theorem 1, proved).** Each Resonus plane of P is at right angles to the line from O to a corner of the polar P\*.
   Each Vacuus plate of P is at right angles to an edge of P\*. So the Resonus of P belongs to the **corners** of P\*, and the Vacuus of
   P belongs to its **edges**.
2. **Permutahedron (Theorem 2, proved).** The Resonus of the permutahedron of 1..n is the arrangement Σ_{i∈S} x_i = 0 (S a nonempty
   proper subset), restricted to the sum-zero hyperplane. This arrangement is known as the **restricted all-subset arrangement**
   A′_n (Kamiya–Takemura–Terao 2011). Up to a change of coordinates it is the **resonance arrangement** in n − 1 variables, named by
   Shadrin–Shapiro–Vainshtein. It is also the adjoint of the braid arrangement. Region counts for n = 3, 4, 5, 6: **6, 32, 370, 11292**,
   which are OEIS **A034997**(2..5). We recomputed these exactly.
3. **B3, H3 (Theorem 3).** The Resonus has 7, 13 and 31 planes for the A3, B3 and H3 permutahedra. All three are simplicial, with
   32, 96 and 480 regions. The claim in 2026-11-24-permutahedron-leads is confirmed. In Grünbaum's catalogue they are
   **A(7,1)** (proved via Cuntz's classification), **A(13,2)** (proved the same way) and **A(31,1)** (every invariant matches; not proved).
   - B3: the Resonus is the 9 mirrors of B3 (= A(9,1)) plus 4 planes at right angles to the 3-fold axes.
   - H3: the Resonus is the 15 mirrors of H3 (= A(15,1)) plus 10 + 6 planes at right angles to the 3-fold and 5-fold axes.
   - None of the three is a reflection arrangement. The rank-3 reflection arrangements have 6, 9 and 15 planes.
4. **Name.** We found no mathematical use of "Resonus". The word is a Latin adjective, *resonus*, meaning resounding or echoing
   (Lewis & Short). It is also the name of a UK classical record label, Resonus Classics. The **meaning** comes close to an existing
   name: on the permutahedron, the Resonus is the resonance arrangement.

## How the Vacuus and the Resonus relate

Take a solid P with a centre O inside it. Its **polar** P\* is the solid you get by turning faces into corners. Each face F of P,
lying on the plane a·x = 1, becomes the corner a of P\*. Each edge of P, where two faces F and G meet, becomes the edge of P\* that
joins their two corners.

- **The Resonus looks at faces.** The Resonus plane for F is the plane a·x = 0. It is the face's own plane, slid back until it
  passes through O. The arrow from O to the corner a of P\* sticks straight out of this plane. So **each Resonus plane of P is the
  plane at right angles to one corner-arrow of P\***.
- **The Vacuus looks at edges.** The Vacuus plate for the edge where F and G meet is the plane through O and that edge. The edge of
  P\* that joins a and b sticks straight out of this plate. So **each Vacuus plate of P is the plane at right angles to one edge of
  P\***.

In short, the polar turns "plane through the centre" into "a direction". The Resonus takes the corner directions of P\*, and the
Vacuus takes the edge directions of P\*. Two faces of P give the same Resonus plane exactly when they are opposite and parallel. Two
edges give the same Vacuus plate exactly when their polar edges are parallel.

Among all the solids in the Vacuus tables, the two coincide in only two: the rhombic dodecahedron and the rhombic triacontahedron
(vacuus-enumeration, under "Coincidences"). There the Resonus planes and the Vacuus plates are the same.

On the permutahedron the Resonus is a classical object. The permutahedron's face directions are the subsets of {1..n}, so its
Resonus is the "resonance" (all-subset) arrangement. This arrangement counts thermal Green functions in physics and Hurwitz-number
chambers in geometry.

## 1. Theorem 1 (polar link)

**Setting.** P is a convex polytope in R^d, O = 0 is in its interior, and P\* = {y : y·x ≤ 1 for all x ∈ P}. Each facet F lies on
a plane a_F·x = 1 with a_F ≠ 0 (possible because O is interior), and a_F is the corner of P\* dual to F. Two facets F and G meeting
in a ridge R (an edge, in 3D) give the edge [a_F, a_G] of P\*, dual to R. This is the standard face duality (Ziegler, *Lectures on
Polytopes*, Thm 2.11).

**Theorem 1.** (a) The Resonus plane of F, the plane through O parallel to F, is {x : a_F·x = 0}. It is at right angles to the
vector from O to the corner a_F of P\*. (b) The Vacuus plate of the ridge R = F ∩ G, the hyperplane through O and R, is
{x : (a_F − a_G)·x = 0}. It is at right angles to the edge [a_F, a_G] of P\*.

*Proof.* (a) The plane of F is a_F·x = 1, so the parallel plane through O is a_F·x = 0, with normal a_F.
(b) Every x in R lies on both facets, so a_F·x = a_G·x = 1, that is, (a_F − a_G)·x = 0. Also a_F ≠ a_G, because distinct facets
have distinct planes. So H = {(a_F − a_G)·x = 0} is a hyperplane through O that contains R. It remains to show that O and R span
exactly one hyperplane, so that H is the plate. The affine hull of R has dimension d − 2, and it lies in a_F·x = 1, which misses O.
Hence O together with R spans a space of dimension d − 1, and that space is H. ∎

**Degenerate cases.**
- *O on the line of an edge.* This cannot happen while O is interior. The edge's line lies in a_F·x = 1, and a_F·O = 0 ≠ 1. So the
  Vacuus plate is always defined. If O is on the boundary, P\* is unbounded and both statements lose their dual object; this case
  is excluded.
- *Parallel faces.* Two facets with the same outward normal direction are the same facet. So parallel facets F and G are opposite,
  with a_G = −λ a_F for some λ > 0, and they give one Resonus plane. Their polar corners lie on one line through O, on opposite
  sides. Hence the number of Resonus planes equals the number of lines through O that carry a corner of P\*. Similarly, two ridges
  give the same Vacuus plate exactly when their dual edges are parallel (both are at right angles to that plate). Example: e and −e
  in a centrally symmetric P, as in Lemma 1 of the vacuus-enumeration study.

**Exact check.** `scripts/resonus_3d.py` checks (a) on every face and (b) on every edge of the three permutahedra (36, 72 and 180
edges), exactly in Q(√5). The normal of the plane through O, u and v is u × v, and it is parallel to a_F − a_G every time.

## 2. Theorem 2 (the permutahedron)

**Theorem 2.** Let Π be the permutahedron, the convex hull of all permutations of (1, 2, …, n), with centre c = ((n+1)/2)(1, …, 1).
Write y = x − c, so that Π lies in the hyperplane V = {Σ y_i = 0}. Then the Resonus of Π (in V) is
{ Σ_{i∈S} y_i = 0 : ∅ ≠ S ⊊ [n] } restricted to V. It has 2^(n−1) − 1 distinct hyperplanes, one per pair {S, complement of S}.

*Proof.* The facets of Π are Σ_{i∈S} x_i ≥ |S|(|S|+1)/2, one for each nonempty proper S. This is Rado's description (R. Rado,
"An inequality", J. London Math. Soc. 27 (1952) 1–6; see Ziegler, *Lectures on Polytopes*, Example 0.10). The plane through c
parallel to facet S is Σ_{i∈S} y_i = 0 within V. On V, Σ_S y = −Σ_{S^c} y, so S and its complement give the same plane. These are
the parallel opposite facets of Theorem 1. No other planes coincide. The normal within V is 1_S − (|S|/n)·1, which takes one value
on S and another off S. Two such vectors are proportional only if they have the same level sets, that is, only if T = S or
T = S^c. ∎

**Literature names.** Every source below was opened through a free route (arXiv, OEIS, author pages). Credit:
- **Kamiya, Takemura, Terao**, "Ranking patterns of unfolding models of codimension one", Adv. Appl. Math. 47 (2011) 379–400
  (arXiv:1003.0040), Section 3. They define the all-subset arrangement A_m = {H_I : ∅ ≠ I ⊆ [m]} in R^m and its restriction
  A′_m to H_0 = H_[m] = {Σ x = 0}. **A′_n is exactly the Resonus of Theorem 2**, the same arrangement with the same name for the
  same restriction. Their Lemma 5.3 gives χ(A′_m, t) and the region counts for m ≤ 8. They note that L(A′_m) ≅ L(A_{m−1}).
- **Shadrin, Shapiro, Vainshtein**, "Chamber behavior of double Hurwitz numbers in genus 0", Adv. Math. 217 (2008) 79–96
  (arXiv:math/0611442, where the title is "On double Hurwitz numbers in genus 0"). They call the hyperplanes x_I = y_J (in
  R^(m+n), on Σx = Σy) **resonances**, and the regions between them **chambers**. Kühne credits them with coining "resonance
  arrangement".
- **Cavalieri, Johnson, Markwig**, "Wall crossings for double Hurwitz numbers", Adv. Math. 228 (2011) 1894–1937 (arXiv:1003.1805,
  "Chamber structure of double Hurwitz numbers"). They extend SSV to all genera and show the chambers are the domains of
  polynomiality.
- **Kühne**, "The universality of the resonance arrangement and its Betti numbers", Combinatorica 43 (2023) 277–298
  (arXiv:2008.10553). He defines the resonance arrangement 𝒜_n in R^n (all nonzero 0/1 normals) and notes that it is the adjoint
  of the braid arrangement [Aguiar–Mahajan, *Topics in hyperplane arrangements*, 2017, §6.3.12] and the "(restricted)
  all-subsets arrangement" of Kamiya–Takemura–Terao. He also proves that every rational arrangement is a minor of some 𝒜_n.
  - By Theorem 2, the Resonus of the n-permutahedron is isomorphic to 𝒜_{n−1}: eliminate y_n, so that each pair {S, S^c} keeps its
    member that avoids n.
- **"Billera–Tatarevic–Moore"** is not a correct citation. The paper is L. J. Billera, J. Tatch Moore, C. Dufort Moraites, Y. Wang
  and K. Williams, "Maximal unbalanced families", arXiv:1209.2309 (2012). It puts the chambers in bijection with maximal unbalanced
  families.
- Also on this arrangement: Liu, Norledge, Ocneanu, "The adjoint braid arrangement as a combinatorial Lie algebra via the Steinmann
  relations" (arXiv:1901.03243); Gutekunst, Mészáros, Petersen, "Root cones and the resonance arrangement" (arXiv:1903.06595).
  The physics origin is T. S. Evans (Nucl. Phys. B 374 (1992); arXiv:hep-ph/9404262), where the regions are "generalized retarded
  functions".

**Region counts (exact, recomputed).**

| n (permutahedron of 1..n, dimension n − 1) | Resonus planes | χ(t) | regions | OEIS |
|---|---|---|---|---|
| 3 (hexagon) | 3 | t² − 3t + 2 | **6** | A034997(2) |
| 4 (truncated octahedron) | 7 | t³ − 7t² + 15t − 9 | **32** | A034997(3) |
| 5 | 15 | t⁴ − 15t³ + 80t² − 170t + 104 | **370** | A034997(4) |
| 6 | 31 | t⁵ − 31t⁴ + 375t³ − 2130t² + 5270t − 3485 | **11292** | A034997(5) |

A034997, "Number of generalized retarded functions in quantum field theory", is indexed by the number of variables d = n − 1:
2, 6, 32, 370, 11292, 1066044, … The polynomials agree with Kamiya–Takemura–Terao, Lemma 5.3, coefficient for coefficient.

*Method* (`scripts/resonance_regions.py`, log `logs/resonance_regions.log`). We used the finite field method (Athanasiadis, Adv. Math.
122 (1996)). χ(q) counts the points of F_q^d off every hyperplane, for primes q that divide no nonzero minor of the 0/1 normal
matrix. Minors of 0/1 matrices of size at most 5 have |det| ≤ 5 (the maximal values are 1, 1, 2, 3, 5), so every q ≥ 7 is good. χ was
solved from d primes and checked on two further primes, on χ(1) = 0, and on the t^(d−1) coefficient. Regions = (−1)^d χ(−1)
(Zaslavsky 1975).

## 3. Theorem 3 (B3 and H3; the simplicial claim)

**Data** (`scripts/resonus_3d.py`, log `logs/resonus_3d.log`, `data/resonus_3d.json`). The solids are those of
2026-11-24-permutahedron-leads: the truncated octahedron, the B3 permutahedron through (1,2,3), and the uniform truncated
icosidodecahedron, all exact. The Resonus depends only on the face directions. Those form the Coxeter fan and are the same for
every generic starting point, so the (1,2,3) B3 solid gives the Resonus of the uniform truncated cuboctahedron.

The arrangement is read in the projective plane. f = (corners, edges, regions) of the line arrangement; t_j = number of points on
exactly j lines; r_j = number of lines carrying exactly j points.

| | A3 (truncated octahedron) | B3 (truncated cuboctahedron) | H3 (truncated icosidodecahedron) |
|---|---|---|---|
| Resonus planes (from faces) | 7 = 3 (squares) + 4 (hexagons) | 13 = 6 (squares) + 4 (hexagons) + 3 (octagons) | 31 = 15 (squares) + 10 (hexagons) + 6 (decagons) |
| each plane from | 2 opposite faces | 2 opposite faces | 2 opposite faces |
| f | (9, 24, 16) | (25, 72, 48) | (121, 360, 240) |
| t | t2 = 3, t3 = 6 | t2 = 12, t3 = 4, t4 = 9 | t2 = 60, t3 = 40, t5 = 6, t6 = 15 |
| r | r3 = 4, r4 = 3 | r4 = 3, r6 = 10 | r10 = 6, r12 = 25 |
| simplicial (2f1 = 3f2) | **yes** | **yes** | **yes** |
| regions in space (2f2) | 32 | 96 | 480 |
| planes that are mirrors of the solid | 3 (squares: the coordinate mirrors of B3, not of A3) | 9 = all mirrors of B3 (squares + octagons) | 15 = all mirrors of H3 (squares) |
| Grünbaum (2009) | **A(7,1)** | **A(13,2)** | **A(31,1)** (invariants) |

*Simplicial test.* Each region of a line arrangement in the projective plane has at least 3 sides, and each edge borders 2 regions.
So the side counts add up to 2f1 ≥ 3f2, with equality exactly when every region is a triangle. f2 = 1 − f0 + f1 by Euler. All
counts come from exact intersection points (projective keys in Q(√5)).

*Identification.*
- B. Grünbaum, "A catalogue of simplicial arrangements in the real projective plane", Ars Math. Contemp. 2 (2009) 1–25, table
  pp. 6–10.
- M. Cuntz, "Simplicial arrangements with up to 27 lines", Discrete Comput. Geom. 48 (2012) (arXiv:1108.3000). Cuntz proves that
  the catalogue is complete up to 27 lines, apart from four new arrangements with 22–25 lines, and he lists automorphism groups.
- Our 7- and 13-line arrangements are simplicial. By Cuntz they are isomorphic to listed arrangements.
  - A(7,1) is the only non-near-pencil with 7 lines.
  - A(13,2) is the only 13-line entry with t = (12, 4, 9). Cuntz gives Aut = B3 for both, as expected.
- 31 lines is beyond Cuntz's range. Our f, t, r equal those of A(31,1) and differ from A(31,2) and A(31,3) (f = (127, 378, 252)).
  The isomorphism with A(31,1) is not proved here (LEAD 1). Grünbaum marks A(31,1) as maximal.
- Sub-arrangements: the 9 B3 mirrors are A(9,1) = the B3 reflection arrangement. The 15 H3 mirrors are A(15,1) = the H3 reflection
  arrangement (Cuntz: Aut H3).
- The A3 Resonus x, y, z, x ± y ± z is the complete quadrilateral x ± y ± z with its three diagonals. It is not the A3 reflection
  arrangement A(6,1), and it is the resonance arrangement 𝒜_3 of Section 2, as Theorem 2 predicts (n = 4).

**Why the planes sit on the axes** (proposition, by the standard fact cited). The face directions of a W-permutahedron are the
rays of the Coxeter fan, the W-orbits of the fundamental weights (see e.g. Hohlweg, Lange, Thomas, "Permutahedra and generalized
associahedra", Adv. Math. 226 (2011), §1). So the Resonus of a W-permutahedron is the set of planes at right angles to those rays.
In rank 3 these rays are the lines where two or more mirrors meet, which are the rotation axes of W. This gives 3 + 4, 6 + 4 + 3 and
15 + 10 + 6 planes, matching the table. For W = A_{n−1} the rays are the 1_S directions, which is Theorem 2 again.

## 4. Name check: "Resonus"

Searched on 24 Nov 2026 (web search for "Resonus" with mathematics, geometry, polytope, arrangement, theorem; the arXiv and OEIS
entries above). No mathematical term "Resonus" was found, in geometry or elsewhere in mathematics. Other uses found:
- the Latin adjective *rĕsŏnus, a, um*, "resounding, re-echoing" (poetic; Ovid, Lucan; Lewis & Short, Perseus);
- **Resonus Classics**, a UK classical record label founded in 2011.

The close existing name is "resonance arrangement" (Section 2). On the permutahedron, DICTO's Resonus **is** that arrangement, so
the name echoes it fittingly. Papers should say so at first use: Resonus of the permutahedron = restricted all-subset
(resonance) arrangement, after Kamiya–Takemura–Terao and Shadrin–Shapiro–Vainshtein.

## Sources checked

Kamiya–Takemura–Terao 2011 (arXiv:1003.0040, full text); Shadrin–Shapiro–Vainshtein 2008 (arXiv:math/0611442, full text);
Cavalieri–Johnson–Markwig (arXiv:1003.1805, abstract); Kühne 2023 (arXiv:2008.10553, full text); Billera et al. 2012 (via OEIS and
Kühne's references); Liu–Norledge–Ocneanu (arXiv:1901.03243, abstract); OEIS A034997 (entry and references); Grünbaum 2009 (author's
catalogue, University of Washington repository copy); Cuntz 2012 (arXiv:1108.3000, full text); Lewis & Short via Perseus (search
listing); Resonus Classics (label pages, search listing).

## LEADS

1. **Prove the H3 Resonus is A(31,1).** Either write down an explicit line bijection with Grünbaum's figure of A(31,1), or compare
   oriented matroids (Cuntz's data).
2. **Type B in every dimension.** By the proposition, the Resonus of the B_n permutahedron is the arrangement of all hyperplanes with
   normals in {−1, 0, 1}^n (a signed all-subset arrangement). Its region counts are a candidate OEIS check.
3. **Polar reading for the dice.** The Aequi A3-24, B3-48 and H3-120 are the polars of the permutahedra. By Theorem 1 the Resonus of
   a permutahedron is the set of planes at right angles to the dice's corners, and its Vacuus is the set of planes at right angles to
   the dice's edges. For the dice these edges lie in the mirrors (Proposition 2 of vacuus-enumeration).
4. **Resonus of the 4D permutahedra** (A4, B4, H4): from the 4D pilot data of the Vacuus study. For A4 this is 𝒜_4, with 370 regions.

## Files

`scripts/resonus_3d.py` (Theorems 1 and 3: exact checks, arrangement invariants); `scripts/resonance_regions.py` (Section 2 counts);
`logs/`, `data/resonus_3d.json`. The scripts import the exact solids of 2026-11-24-permutahedron-leads and 2026-11-21-amber-cell-sweep.
