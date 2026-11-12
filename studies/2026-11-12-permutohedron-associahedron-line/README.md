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
exactly at s = D_S** (checked for every facet, n = 4, 5). The stations of line B all stay generalized permutohedra (these are the
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
