# Aim 2: a Hopscotch line from the permutohedron (the crystal) to the associahedron (the law-giving shape) (12 Nov 2026)

**Conclusion.** On Postnikov's straight line from the permutohedron to Loday's associahedron the shape keeps the permutohedron's face lattice right up to the end, and all the non-interval facets vanish together at t = 1 (5 facets in 3D, 16 in 4D), so the line has one wall. On the equal-speed (Hopscotch) line each such facet vanishes on its own at s = D_S, which gives walls at s = 1, 2 in 3D and s = 1, 2, 3, 4 in 4D. Tiling by translations is lost at once: only t = 0 tiles, on every line to the associahedron. The canonical form at the centre falls as an exact rational function, from 16/3 to 88/27 = m_6 in 3D and from 10/3 to 49/36 = m_7 in 4D. At the ABHY end it is chunk 4's amplitude exactly. FINAL ok for n = 4 and n = 5.

Script `scripts/gp_line.py` (exact `fractions`; sympy only for the closed forms in the line parameter). Logs `data/gp-line-n4.log`,
`data/gp-line-n5.log`. **Facet-height data for the app:** `data/gp-line-n4.json`, `data/gp-line-n5.json`. These hold every z_S at every station, the vertices (full x-coordinates), the facets with their vertex lists, the f-vector, the generalized-permutohedron and tiling verdicts, Ω at Y, the closed forms Ω(parameter) on every open stretch, the wall table, and the facet sizes along line A. Run on the compute node through the job gate: pilot n = 4 in 11 s, main n = 5 in 368 s, 4 GB cage, 2 cores.

## Setup

A generalized permutohedron in R^n is P(z) = {x : Σ x_i = z_[n], Σ_{i∈S} x_i ≥ z_S for every nonempty proper S} (Postnikov 2009). Its
deformation cone is the cone of submodular z (Postnikov–Reiner–Williams 2008; Ardila–Castillo–Eur–Postnikov 2020 for all Coxeter types).
Coordinates u = (x_1, …, x_{n−1}); d = n − 1; fixed interior point Y = the permutohedron's centre ((n+1)/2, …).

- **Π** = Σ_{i<j} Δ_ij on coordinates 1..n: z_Π(S) = C(|S|+1, 2) (the truncated octahedron for n = 4).
- **L** = Loday's associahedron = Σ over intervals Δ_[i,j] (Postnikov's y_I = 1 on intervals): z_L(S) = the number of intervals inside S.
  Interval heights agree with Π's, so on the way only the **non-interval** facets move. Each has deficit D_S = z_Π(S) − z_L(S) = Σ_{blocks b<b'} k_b k_b'
  (k_b = the block lengths of S).
- **Line A (Postnikov line):** z(t) = (1−t) z_Π + t z_L = the Minkowski path (1−t)Π + tL.
- **Line B (equal-speed, Hopscotch style):** every non-interval height moves at the same speed, z_S(s) = z_Π(S) − s, s ∈ [0, max D].
- **Line C (ABHY line):** z(t) = (1−t) z_Π + t z_A. A is the kinematic associahedron of Arkani-Hamed–Bai–He–Yan with **chunk 4's own random c**
  (setup(N), N = n + 2), written as a generalized permutohedron through interval [i, j] ↔ diagonal (i, j+2). Its non-interval heights are its tight support values, and it is
  translated so that its vertex centroid is Π's centre. Lines A and B end at **Loday's** realisation; line C ends at the **ABHY** one.
- **Line Z (control):** Π0 = Σ_{i<j} Δ_ij → the cube Σ Δ_{i,i+1} (graphic zonotopes of K_n → the path).

**Method.** At every station the script finds all vertices exactly (every d-subset of the 2^n − 2 inequalities), the face lattice, the f-vector, simplicity, and the
generalized-permutohedron test (every edge parallel to some e_i − e_j). It runs the **Venkov–McMullen parallelohedron test** (centrally symmetric, centrally
symmetric facets, every belt of 4 or 6 facets; Venkov 1954, McMullen 1980), and it computes Ω(Y) by the pulling-triangulation formula, with Warren's vertex formula as
an independent check. Where Y lies on an inner wall of the triangulation, it takes an exact Laurent-series limit (the poles are checked to cancel). **Walls exactly:** z is
affine in the parameter, so each d-subset is a vertex on a closed parameter interval. The type can change only at the ends of these
intervals, and each end is tested by comparing the labelled vertex–facet structure at the point and on both sides.

## Walls along the lines

| line | n | parameter | facets shrinking to nothing (S) | face they shrink to | f-vector before → at |
|---|---|---|---|---|---|
| A Postnikov | 4 | t = 1 | 13, 14, 24, 124, 134 (all 5 non-intervals) | edges | (24,36,14) → (14,21,9) |
| B equal speed | 4 | s = 1 | 13, 14, 24 (D = 1) | edges | (24,36,14) → (18,27,11) |
| B equal speed | 4 | s = 2 | 124, 134 (D = 2) | edges | (18,27,11) → (14,21,9) |
| C ABHY | 4 | t = 1 | the same 5 | edges | (24,36,14) → (14,21,9) |
| A Postnikov | 5 | t = 1 | all 16 non-intervals | 2-faces; 135 → an edge | (120,240,150,30) → (42,84,56,14) |
| B equal speed | 5 | s = 1 | 13, 14, 15, 24, 25, 35 (D = 1) | 2-faces | (120,240,150,30) → (82,166,108,24) |
| B equal speed | 5 | s = 2 | 124, 125, 134, 145, 235, 245 (D = 2) | 2-faces | → (58,118,78,18) |
| B equal speed | 5 | s = 3 | 135, 1235, 1345 (D = 3) | edge (135), 2-faces | → (46,92,61,15) |
| B equal speed | 5 | s = 4 | 1245 (D = 4) | 2-face | → (42,84,56,14) |
| C ABHY | 5 | t = 1 | all 16 non-intervals | as line A | (120,240,150,30) → (42,84,56,14) |
| Z control | 4, 5 | t = 1 | 8 / 22 facets (to the cube) | vertices, edges, 2-faces | → (8,12,6) / (16,32,24,8) |

**1. Face lattice.** Lines A, C and Z have **no wall inside**: for 0 ≤ t < 1 the shape has the permutohedron's labelled face lattice. This is a theorem, and the
computation agrees with it: a Minkowski sum (1−t)P + tQ has the common refinement of the two normal fans as its fan, and the braid fan refines every other
generalized permutohedron's fan. A straight line from the interior of the deformation cone to its face (Loday's type cone) therefore meets the walls
only at its end. In type-cone language (Padrol–Pilaud–Ritter; Padrol–Palu–Pilaud–Plamondon), the open line lies in the interior of the braid fan's type
cone, and t = 1 is the face that is the sylvester fan's type cone. Along A every non-interval facet shrinks to zero size **linearly**, (1 − t)·(a polynomial with no root at 1), except 135 in 4D,
which shrinks to an edge as (1 − t)²(3t + 1); the facet-size polynomials are in the json. On the **equal-speed line B every non-interval facet S vanishes
exactly at s = D_S** (checked for every facet, n = 4, 5). For n = 4, 5 the stations of line B all stay generalized permutohedra (not for n = 6: see the section of 13 Nov below) (these are the
removahedra between Π and L; Pilaud–Pons permutreehedra and Albertin–Pilaud–Ritter study this family combinatorially). In 4D line B is **not simple**
for 1 < s < 3.

**2. Space-filling.** The permutohedron passes the test (belts all 6: 6 belts in 3D, 25 in 4D). Loday's and the ABHY associahedron fail it: they are not
centrally symmetric. **On lines A, B and C, tiling is lost at once: no station with t > 0 tiles.** This holds exactly on the whole open line, not
only at the stations. While the facet set is fixed, central symmetry is a linear condition on z (one centre must give every width), and z is affine in t, so
failing at one t ≠ 0 means failing at every t ≠ 0. The control line Z tiles at every station (graphic zonotopes are unimodular, so they tile), so the test is not
simply rejecting everything that moves. The truncated octahedron is an isolated tiler on the way to the associahedron: switching on any interval simplex
Δ_I with |I| ≥ 3 breaks central symmetry.

**3. Canonical form at Y.** Ω(Π; centre) = 2^{n−1} n/(n−1)! (16/3, 10/3), the sum over the n! vertices (the maximal flags of subsets) of
∏ 1/X_S. Along line A it is one rational function:
- 3D: Ω(t) = 8(8t² + 33t + 36) / (9(t + 2)(4t + 3)), from 16/3 to **88/27 = m_6**;
- 4D: Ω(t) = 2(8t⁵ + 74t⁴ + 264t³ + 447t² + 342t + 90) / (3(t + 1)(t + 3)(2t + 1)(2t + 3)(3t + 2)), from 10/3 to **49/36 = m_7**.

On line B it is piecewise: one formula per stretch between walls in 3D; in 4D the two non-simple stretches have station values only. It is continuous at every
wall, and it falls monotonically, because the shape only grows (Π ⊂ P ⊂ L), so its polar shrinks. **At the associahedron end:** Loday's heights satisfy the ABHY mesh
relations with every c = 1, and Ω(L; Y) = m_{n+2}(X = Loday facet values at Y). At the ABHY end, Ω(A; Y) equals chunk 4's amplitude m_6 / m_7, computed from chunk 4's
own X functions at the same point. A tree-dropped amplitude differs (negative control). Ω is in the coordinates u, and no Jacobian factor appears at either end.

## Literature check (web, 12 Nov 2026)

Queries: "interpolation permutohedron associahedron deformation cone generalized permutohedra canonical form amplitude"; "permutohedron canonical form
scattering amplitude positive geometry"; "Padrol Pilaud Ritter shard polytopes type cone"; "Padrol Palu Pilaud Plamondon … type cone kinematic";
"permutohedron canonical form sum over time orderings … cosmological polytope"; "Pilaud Pons permutrees … interpolate"; "canonical form of the
permutohedron sum over permutations … eikonal"; "Nick Early generalized permutohedra kinematic space". Sources read (abstracts or excerpts):
- Postnikov, *Permutohedra, associahedra, and beyond*, IMRN 2009 (y_I description; Loday = Σ Δ_[i,j]). Postnikov–Reiner–Williams 2008.
  Ardila–Castillo–Eur–Postnikov, *Coxeter submodular functions and deformations of Coxeter permutahedra*, 2020 (deformation cone).
- Padrol–Pilaud–Ritter, *Shard polytopes*, arXiv:2007.01008 (type cones, Minkowski summands); Padrol–Palu–Pilaud–Plamondon, *Associahedra for finite type
  cluster algebras and minimal relations between g-vectors*, arXiv:1906.06861 (the type cone of the g-vector fan is simplicial; ABHY = all realisations);
  Bazier-Matte–Douville–Mousavand–Thomas–Yıldırım, *ABHY associahedra and Newton polytopes of F-polynomials*, arXiv:1808.09986.
- Pilaud–Pons, *Permutrees*, Algebraic Combinatorics 2018 (permutreehedra interpolate permutahedron, associahedra, cube by deleting facets);
  Albertin–Pilaud–Ritter, *Removahedral congruences versus permutree congruences*, EJC 2021.
- Arkani-Hamed–Bai–He–Yan, arXiv:1711.09102 (kinematic associahedron, m_n). Arkani-Hamed–Bai–Lam, *Positive geometries and canonical forms*,
  arXiv:1703.04541, §10 (the permutohedron's canonical form = Σ_σ 1/∏ partial sums).
- N. Early, *Generalized permutohedra in the kinematic space*, arXiv:1804.05460 (JHEP 2024): the poles of the ABHY form carry permutohedral geometry, and
  m(I_n, I_n) on an (n−2)-dimensional subspace is read as a sum over the boundary of the root cone.
- He–Li–Raman–Zhang, *Stringy canonical forms and binary geometries from associahedra, cyclohedra and generalized permutohedra*, arXiv:2005.07395.
- T. Lam, dual mixed volumes (FPSAC 2025) and *The combinatorial geometry of particle physics*, arXiv:2509.25372 (m_n as the dual mixed volume of an associahedron).
- *In-in zonotope* (arXiv:2601.18903, 2026): canonical form at the origin = the flat-space equal-time correlator; for K3 it is a permutohedron (seen only through
  an AI-written review summary; primary text not read).

**Answer:** no paper was found that follows the straight line Π → associahedron in the deformation cone, records its walls, its loss of tiling, or its canonical form along the way. The
combinatorial interpolation by deleting facets is known (Pilaud–Pons; Hohlweg–Lange), and the permutohedron's canonical form is known (Arkani-Hamed–Bai–Lam
§10). Whether it is a known amplitude is partly answered: Early reads m(I_n, I_n) through permutohedral geometry, and the 2026 in-in zonotope work gives a
permutohedral canonical form a correlator meaning. No source gives the permutohedron's canonical form itself as a standard scattering amplitude.
Credit: Postnikov; Ardila–Castillo–Eur–Postnikov; Arkani-Hamed–Bai–He–Yan; Padrol–Pilaud–Ritter. The lines, checks and code are ours.

## LEADS
1. Prove the equal-speed rule for every n: on line B the facet S vanishes exactly at s = D_S = Σ_{b<b'} k_b k_b'. The walls are the distinct
   block-product sums (1, 2 in 3D; 1, 2, 3, 4 in 4D; n = 6 not yet computed).
2. 4D line B is not simple for 1 < s < 3: name the non-simple vertices and get Ω(s) there in closed form (a triangulation with symbolic s).
3. Which generalized permutohedra tile by translations? Line Z and line A suggest exactly the y supported on pairs (graphic zonotopes); test any y_I > 0 with
   |I| ≥ 3 for a tiler.
4. The true Hopscotch for the permutohedron: P ∩ μP* (the truncated octahedron against its dual) along the polar slider, with walls, tiling and Ω, for comparison with the
   deformation-cone lines here.
5. Read Ω_Π = Σ over flags ∏ 1/X_S against Early's m(I_n, I_n) boundary formula and the in-in correlator; is the line-A family Ω(t) a one-parameter
   family of amplitudes?
6. The app: the json files hold every station exactly, so build the slider (A, B, C) with facet colours by S and the wall marks.

## Conjectures 1 and 2 proved; n = 6 computed (13 Nov 2026)

**Conclusion.** Both conjectures of the Permutohedron Family draft are proved for every n, and both hold exactly at n = 6 (5D).
Conjecture 1: on the equal-speed line B, facet S is present for every s < D_S and gone from s = D_S on, so the walls are exactly the values
of D_S (n = 6: s = 1, 2, 3, 4, 5, 6). Conjecture 2: Ω(Π; centre) = 2^{n−1} n/(n−1)! (n = 6: 8/5). At the Loday end Ω(L; centre) = m_8 =
2288/5625 at n = 6. **New at n = 6:** the stations of line B are **not** all generalized permutohedra: for 1 < s < 5 the shape has 16 edges
off the root directions e_i − e_j (e.g. at s = 2 the edge from (1, 6, 1, 2, 7, 4) to (2, 5, 1, 2, 8, 3), direction (−1, 1, 0, 0, −1, 1)),
so the earlier remark "the stations of line B all stay generalized permutohedra" holds for n = 4, 5 only. Status: SETTLED.

**Proof of Conjecture 1 (every n).** The proved half (S gone at s = D_S, and for s > D_S the plane misses P) is in the draft. For the other
half fix a non-interval S and let ε*(s) be the largest ε such that some x has x(S) = z_S(s), x([n]) = z_[n] and x(U) ≥ z_U(s) + ε for
every other U. S is a facet at s exactly when ε*(s) > 0 (a relative-interior point of a facet lies on no other supporting plane, since all
normals are distinct; conversely such a point spans a (d−1)-face). The constraints are linear in (s, x, ε) jointly, so ε* is concave in s.
ε*(0) > 0 (every S is a facet of Π). If ε*(D_S) ≥ 0, concavity gives ε*(s) ≥ (1 − s/D_S) ε*(0) > 0 for all s < D_S. So it is enough to
give one point x of P(z(D_S)) with x(S) = z_L(S). Let S have blocks b_1 < … < b_m (lengths k_1..k_m, K = Σ k_p, D = D_S = Σ_{p<q} k_p k_q),
complement G. Put the values 1..k_p on block b_p, the values K+1..n on G, and add E_p = k_p(k_{p+1} + … + k_m) to the first element of
the gap after b_p (Σ E_p = D). Then x(S) = Σ C(k_p+1, 2) = z_L(S) and x([n]) = C(n+1, 2). For any U with u_p = |U ∩ b_p|, u_T = Σ u_p,
u_G = |U ∩ G|: x(U) − C(|U|+1, 2) ≥ (K − u_T) u_G − Σ_{p<q} u_p u_q + E(U), using x(U ∩ b_p) ≥ C(u_p+1, 2) and the smallest u_G values of
G. This is ≥ −D, so every non-interval inequality x(U) ≥ C(|U|+1, 2) − D holds. If U is an interval meeting blocks i..j it contains the gaps
between them, so E(U) ≥ Σ_{p=i}^{j−1} E_p ≥ Σ_{i≤p<q≤j} k_p k_q ≥ Σ u_p u_q, and x(U) ≥ C(|U|+1, 2). ∎
`scripts/conj1_witness.py` checks this point for every non-interval S, n = 3..13 (15 914 facets, all valid); negative control: the same
point with all the extras on the last complement element fails for some S at every n ≥ 4 (the gap placement is needed).

**Proof of Conjecture 2 (every n).** Π is simple and every vertex cone is unimodular (the normals of a flag ∅ ⊂ T_1 ⊂ … ⊂ T_{n−1} form a
triangular 0/±1 matrix), so Ω(Π; Y) = Σ over the n! flags of ∏_k 1/X_{T_k} (Arkani-Hamed–Bai–Lam §10). At the centre Y = ((n+1)/2, …),
X_T = |T|(n+1)/2 − C(|T|+1, 2) = |T|(n − |T|)/2 depends only on |T|, so every flag gives ∏_{k=1}^{n−1} 2/(k(n−k)) = 2^{n−1}/((n−1)!)², and
Ω = n! · 2^{n−1}/((n−1)!)² = 2^{n−1} n/(n−1)!. ∎

**n = 6 on line B (exact).** f-vectors (vertices, edges, 2-faces, 3-faces, facets): (720, 1800, 1560, 540, 62) for 0 ≤ s < 1;
at s = 1 (452, 1150, 1034, 386, 52); (468, 1182, 1054, 390, 52) on 1 < s < 2; (332, 842, 758, 286, 40) on [2, 3); (236, 590, 528, 202, 30)
on [3, 4); (176, 440, 398, 157, 25) on [4, 5); (152, 380, 344, 136, 22) on [5, 6); Loday (132, 330, 300, 120, 20) at s = 6.
Facets vanishing: s = 1: 13 14 15 16 24 25 26 35 36 46; s = 2: 124 125 126 134 145 156 235 236 245 256 346 356; s = 3: 135 136 146 246 1235
1236 1345 1456 2346 2456; s = 4: 1245 1256 2356 12346 13456; s = 5: 1246 1346 1356; s = 6: 12356 12456 (each exactly its D_S). Not simple for
1 ≤ s < 3, simple from s = 3 on; not a generalized permutohedron for 1 < s < 5 (16 edges off the root directions at every
station there, each confirmed as an edge independently by the rank of the common facet normals). Euler at every station.

**Method.** `scripts/gp_enum.c` (C, integer arithmetic): every d-subset of the 2^n − 2 inequalities (n = 6: 6 471 002 subsets, 3 337 152
nonsingular), its vertex u(s) = (P0 + s P1)/det by Cramer and the exact closed s-interval on which it is a vertex; 1420 candidates at n = 6.
`scripts/gp_line_b.py` (stdlib, Fractions): stations at every interval end point (s = 0, 1, …, 6) and every midpoint; vertices, tight sets,
facets by affine rank, face lattice by closure and grading, f-vector, Euler, simplicity, edge directions; forms by Warren's vertex formula and
the flag sum; m_{n+2} over the Catalan triangulations (interval [i, j] ↔ diagonal (i, j+2)). Data: `data/lineb-cand-n{4,5,6}.txt`,
`data/lineb-n{4,5,6}.json`, logs `data/lineb.log`, `data/lineb-pilot.log`. Run on the compute node through the job gate (plans `pa-line6-pilot`,
`pa-line6`; 2.5 GB cage, one core; n = 6 in 13 s after the enumeration). **Controls:** the n = 4, 5 walls (1, 2 / 1, 2, 3, 4), facet lists and
f-vectors of the table above reproduced exactly, Ω(Π) = 16/3, 10/3 and Ω(L) = m_6 = 88/27, m_7 = 49/36 reproduced; n! and Catalan(n) vertices
at the ends, unimodular vertex cones of Π, Catalan(6) = 132 triangulations; negative: m_N with one tree dropped differs. A first n = 6 run ended
FINAL FAIL only because the generalized-permutohedron test was written as a control; it is a finding, now reported, and the rerun is FINAL ok.
(At n = 5 the station s = 1 itself is also not simple, besides 1 < s < 3.) LEAD 1 above is answered.

**Reader's recheck (13 Nov 2026).** Both proofs above read line by line by an independent reader: no gap. The job `perm-proof-check`
(compute node, 2 GB cage, one core) reran `gp_enum 6` (1420 candidates, identical to `data/lineb-cand-n6.txt`), `gp_line_b.py 6`
(station data identical to `data/lineb-n6.json`; LINEB ok), `conj1_witness.py 11` (3797 facets; WITNESS ok) and the change-ringing
`geodesics.py 8` (GEO ok), plus a separately written `scripts/reader_check.py`: the flag sum vs 2^(n-1) n/(n-1)! for n = 3..9, m_6, m_7,
m_8 = 2288/5625 at the Loday centre by recursion over triangulations, the n = 6, s = 2 edge (1,6,1,2,7,4)-(2,5,1,2,8,3) confirmed an edge
(direction (1,-1,0,0,1,-1), not a root), its own BFS for the ringing count n = 3..8, and the even-n placement step of the Conjecture 13.1
proof. FINAL ok; log `data/reader-check.log`. Both results are written into the Permutohedron Family draft as Theorem 1 (iii), (iv) with proofs.
