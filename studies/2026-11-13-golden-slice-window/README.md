# The golden slice by the window method (13 Nov 2026; The Permutohedron Paradigm, Open question 12.2)

**Conclusion (13 Nov 2026): the golden slice itself has infinitely many shapes in every one of its 35 kinds (PROVED, exact), so the
window method cannot cut it down; its window (cut-and-project) version has finitely many: 60 tetrahedra up to translation (30 up to
congruence) and exactly 69 corner configurations = the 69 window regions, 35 up to point reflection = the 35 kinds. CORRECTION to
Theorem 12.1 (i): both fillings repeat along a plane (periods 5(1,0,-2,1,0), 5(0,1,0,-2,1)); they are non-periodic in one direction only.**

Script `scripts/slice_window.py` (pure Python, exact in Q(phi): pairs a + b phi, a, b rational). Run on the compute node through the
job gate: pilot `slicewin-pilot` (radius 14, 15 s; 39 of 40 checks ok, D4 failed only because a patch of radius 14 has no inner face),
full `slicewin` (radius 50, 10 s, **40 checks, FINAL ok**). Logs `data/slicewin-pilot.log`, `data/slicewin.log`; all numbers in
`data/slice-window-full.json`.

## Setting
P = the 4D permutohedron with corners the 120 orderings of (-2, -1, 0, 1, 2), the Voronoi cell of the lattice
L = {x in Z^5 : sum x = 0, all x_i congruent mod 5} (basis 5e_i - (1,1,1,1,1); covolume 125 sqrt5 = vol P, check A4).
l(x) = u.x with u = (1, phi, phi^2, phi^3, phi^4); the slice is E_c = {l = c}, c generic (c = 1/3 in the runs).
The cell P + lambda is cut iff its height h = c - l(lambda) lies in the **window W = l(P) = (-3 - 7 phi, 3 + 7 phi)** (length
6 + 14 phi), the projection of the cell to the internal line. This is the cut-and-project scheme of the chapter: physical space
E_0 = (direction space of E_c), internal space the line along u' = u - mean(u); pi_E is injective on L (no lattice vector is parallel to
u', whose coordinate ratios are irrational) and **l(L) = 5Z + phi Z** (l of the basis: -7 phi, -5 - 2 phi, -2 phi, 3 phi), dense.
The 120 corner heights take 70 values (Theorem 12.1); they cut W into **69 regions** (bands). In a 1D internal space the "projected
face planes" of de Bruijn's window subdivision are these 70 points.

## Theorem A (the slice has infinitely many shapes in each kind; PROVED)
In every band the section's 3-volume is a polynomial of h that is **not constant**: degree 3 in 68 bands, degree 2 in the middle band.
Hence the heights h_lambda, dense in every band, give infinitely many volumes, so every one of the 35 kinds occurs in infinitely many
shapes, even up to congruence.
Proof. P is simple and l is generic on its edges (l(e) = phi^j - phi^i != 0). Lawrence's formula gives
vol4{x in P : l(x) <= h} sqrt5 = sum over corners v of (h - l(v))_+^4 |det[W_v, 1]| / (24 prod_{w in W_v} l(w)), W_v the four edge
vectors at v (|det[W_v, 1]| = 5 for all v, check C1). The section volume is |u'| times its derivative, i.e. in band k the cubic
sum_{l(v) <= lev_k} c_v (h - l(v))^3 / 6. Checked exactly: the full sum is the constant 625 = (125 sqrt5) sqrt5 and its derivative
vanishes identically (Brion identities, C2, C3: this certifies the formula and its signs); the cubic of each band has a nonzero
coefficient of h^3 or h^2 (C4); it is positive at every band midpoint and obeys V_k(h) = V_(68-k)(-h) (C6). A second proof up to
translation (C5): the section corner on the straddling edge e moves with velocity e / l(e); in every band two straddling edges have
different velocities, so for each h only finitely many h' in the band give a translate.
So the window subdivision fixes only the kind (which edges, 2-faces, facets are cut); the shape inside a kind is a continuous,
non-constant function of the internal coordinate h. This is the general rule for sections (the Fibonacci control F2 shows it in 2D:
the square grid cut by a golden line has a constant middle band but varying outer bands).

## Theorem B (the window version has finitely many shapes; PROVED, with certificates)
Vertices: the model set pi_E(lambda), lambda in L with c - l(lambda) in W (the cells the slice meets). Tiles: pi_E(D(e)), where D(e) is
the Delaunay tetrahedron of a crossed honeycomb edge e (the 4 cell centres round e; every corner of P lies in 5 cells, every edge in
4: checks A2, A3). Then:
1. **They tile the slice face to face.** For x in E_c, |x - lambda|^2 = |x - pi(lambda)|^2 + d_lambda^2 (d_lambda the distance of
   lambda to E_c), so the slice of the Voronoi honeycomb is the power diagram of the sites pi(lambda) with weights -d_lambda^2, and its
   cells are exactly the slice cells. Every slice corner lies inside one honeycomb edge, hence in exactly 4 cells; the dual of such a
   power diagram is its regular (weighted Delaunay) triangulation (Aurenhammer 1987), whose tetrahedra are the pi(D(e)). This is the
   dualisation scheme of Oguey-Duneau-Katz (1988) and Kramer-Schlottmann (1989) for the A4* Voronoi/Delaunay pair. Certificates:
   patch of radius 50 (11 438 vertices, 76 907 tiles): every tile corner is a model-set point (D2), 45 366 inner faces each shared by
   exactly two tiles on opposite sides (D4), covering number exactly 1 at 12 random rational points (D5); on average the volume
   balances exactly: sum_e |l(e)| |det[D(e), u, 1]| = 15000 |u'|^2 = 108000 + 138000 phi (B12), i.e. the tiles fill the slice at the
   model-set density with no gap or overlap.
2. **60 tile shapes up to translation, 30 up to point reflection, 30 up to congruence.** pi(lambda + D) = pi(lambda) + pi(D), and
   pi is injective on L, so the shapes are the translation classes of Delaunay tetrahedra: one per edge orbit, 240 / 4 = 60 (B9, B11);
   D and -D pair up (30), and the projected distance matrices show no further coincidences (B10). All 60 occur (no edge is level).
   On average **6 tiles per vertex** exactly; tile frequencies are proportional to |l(e)| (8 values, exact in Q(phi), in the JSON).
3. **69 corner configurations, one per window region.** The tiles at vertex pi(lambda) are pi(lambda + D(e)) for the edges e of P that
   straddle the level h_lambda, so the configuration depends only on the band of h_lambda: at most 69; all 69 are distinct (B4) and all
   occur (density; all 69 seen in the patch, D6). Band 68-k gives minus band k (B5). The configuration at lambda is the dual of the
   slice cell at lambda, so its combinatorial classes are the kinds: recomputed independently by colour refinement and backtracking
   isomorphism, **35 classes, each = a band and its mirror band, no other coincidence** (B7, B8). So the 35 kinds of Theorem 12.1 are
   exactly the 69 window regions up to point reflection (34 mirror pairs + the symmetric middle band). Frequency of configuration k =
   (band length) / |W| (uniform distribution of the model set), exact; the rarest is 0.00509.
4. **First coronas: 187**, = the effective regions of W cut by the 70 heights and their translates by l(t) for the 30-odd neighbour
   vectors t (194 breakpoints, 193 raw regions, 187 distinct coronas, E2); 165 of them seen in the patch, none outside the prediction (D7).

Why 60 and 35 differ: tiles are dual to the honeycomb's edges (the corners of the slice cells), corner configurations to its cells.
The 35 kinds survive in the window version as the corner configurations; the infinitely many cell shapes are replaced by 60 tiles.

## Proposition C (periods; PROVED) - a correction to Theorem 12.1 (i)
l(lambda) = 0 for lambda in L means sum lambda_i F_(i-1) = sum lambda_i F_i = 0 (phi^i = F_(i-1) + F_i phi); with sum 0 and the mod-5
condition the solutions are exactly **K = 5Z(1,0,-2,1,0) + 5Z(0,1,0,-2,1)** (rank 2; B14, B15; e.g. 1 - 2phi^2 + phi^3 = 0). Every
lambda in K maps the honeycomb to itself and keeps E_c, so **the golden slice repeats along the plane spanned by K**, and so does its
window version. No third independent period: for the window tiling a period t = pi(mu) needs W - l(mu) = W, so l(mu) = 0 and mu in K;
for the slice, three independent periods would leave finitely many cells per period cell, hence finitely many shapes, contradicting
Theorem A. So Theorem 12.1 (i) "the slice repeats nowhere" is false: it is non-periodic across the plane only. This cannot be avoided in
the golden field: for any u in Q(phi)^5, l(L) has rank at most 2, so the periods have rank at least 2. A filling that repeats in no
direction needs a direction whose coordinates span rank 4 over Q (not golden), or a cut of higher codimension.

## Controls (all ok)
- F0: det[a,b,c,u,1] by Laplace = Leibniz on 40 random triples.
- F1, F3 Fibonacci: lattice 2Z^2, square cell, u = (1, phi): 4 corner heights, 3 window regions -> 3 vertex types (LL, LS, SL; never
  SS), 2 tile lengths 2 phi and 2; a 144-tile patch has only these gaps, L/S = 1.6182.
- F2 Fibonacci sections: outer bands vary, the middle band is constant (two parallel edges cross) - the velocity test detects both.
- F4 rational direction (1,-1,0,0,0): 8 heights, 7 bands, l(L) = 5Z discrete, L cap E rank 3: periodic, and at c = 1/3 one height
  falls in W: one shape (the chapter's repeating one-piece filling).
- F5 generic Q(phi) direction (0, 3+phi, 1+4phi, 7+2phi, 2+9phi): 120 heights, 119 bands, 119 distinct stars, 60 classes (agrees
  with the generic row of the chapter's table).
- A1-A4 geometry; B12 volume balance; C2, C3 Brion identities.
Faults on the way: none in the exact parts; the pilot's D4 failure (radius too small for an inner face) is the only one.

## Sources checked
- Read here (library): M. Baake, A guide to mathematical quasicrystals (1999), the passages on the dualisation scheme and its
  references [9], [46], [57]; R. V. Moody, Model sets: a survey (2000), the cut-and-project scheme (pi_1 injective on the lattice,
  pi_2 dense); P. Kramer, Gateways towards quasicrystals (2011), Voronoi and Delone cells as dual tilings.
- Bibliographic records only (not read in this study): C. Oguey, M. Duneau, A. Katz, A geometrical approach of quasiperiodic tilings,
  Commun. Math. Phys. 118 (1988) 99-118; P. Kramer, M. Schlottmann, Dualization of Voronoi domains and klotz construction, J. Phys. A
  22 (1989) (as cited by Baake 1999); M. Baake, P. Kramer, M. Schlottmann, D. Zeidler, Planar patterns with fivefold symmetry as
  sections of periodic structures in 4-space (as cited by Baake 1999); N. G. de Bruijn, Algebraic theory of Penrose's non-periodic
  tilings of the plane, Indag. Math. 43 (1981) 39-66; M. Baake, U. Grimm, Aperiodic Order, Vol. 1, CUP (2013); M. Senechal,
  Quasicrystals and Geometry, CUP (1995); F. Aurenhammer, Power diagrams: properties, algorithms and applications, SIAM J. Comput. 16
  (1987) 78-96; J. Lawrence, Polytope volume computation, Math. Comp. 57 (1991) 259-271.
- Ledger: no entry on the golden slice's window; [180], [183] (golden slices of E8, a different lattice) read.
- Chapter 12 draft and studies/2026-11-11-paradigm-ch12 (golden_types.py): the 70 heights, 69 bands, 35 kinds reproduced exactly.

## LEADS
1. The transverse structure: modulo K the slice is a 1D golden cut-and-project (the rank-2 lattice L/K); identify its sequence of
   "layers" (Fibonacci or another golden Sturmian word) and draw the periodic plane.
2. A golden filling that repeats in no direction: codimension-2 cuts of A4* or the 6D / E8 routes of the Golden Ladder; Proposition C
   shows codimension 1 in Q(phi) cannot do it.
3. The 30 tile pairs and the 35 corner configurations as figures (and a DICTO model set of 30 shapes).
4. Inflation: l(L) = 5Z + phi Z is not closed under multiplication by phi; is there any self-similarity (window scaling) at all?
5. Prove exactly that the period group of the section tiling is K (here only: contains K, rank exactly 2).

## Ledger line
Concordance ledger entry dated 2026-11-13, question "Paradigm Open question 12.2: golden slice by the window method".
