# Aim 2, chunk 7: E8 at the Golden Ladder's top rung as a positive geometry (12 Nov 2026; `scripts/e8_canon.py`, log `data/e8canon.log`, FINAL ok)

**Conclusion.** The canonical form of the Gosset polytope 4_21 (the hull of the 240 E8 roots) at its centre is exactly 8! = 40320, because
its polar is the Voronoi cell of E8, whose volume is 1. The golden cut-and-project pair turns the same bridge into a law for the E8
quasicrystal: the canonical form at the centre of the golden slice of 4_21 is 4! times the quasicrystal's point density,
Ω(4_21 ∩ E_perp; 0) = 20φ³ = 40 + 20√5, so the density is 5φ³/6 = 3.530057. The golden twist sends one side's numbers exactly to the
other side's.

**The top rung (restated).** In the Golden Ladder's closing chapter (study 2026-11-05-golden-ladder-e8), the 240 roots of E8 are the
120 unit icosians and the 120 unit icosians divided by φ. In four dimensions they are two 600-cells, of radii 1 and 1/φ. The golden twist
√5 → −√5 swaps the two 4D spaces E_par (q) and E_perp (σq), in which the roots' sizes read 1 and φ instead.
**Object chosen:** the E8 root polytope 4_21 and its polar, the E8 Voronoi cell, both in 8D, and their golden shadows and slices in
E_par and E_perp. The Voronoi shadow π_perp(Voronoi) is the acceptance window of the Elser–Sloane H4 quasicrystal. This object ties
the top rung to aim 1 (periodic E8 ↔ aperiodic H4 quasicrystal, through the window) and to aim 2 (canonical form = volume of the polar).

**Method.** Ω(A; Y) = n!·vol((A − Y)°) uses two independent exact formulas. F1 is a pulling triangulation of the boundary of the polar,
built from the face lattice of A as vertex/facet bitsets: Σ |det N_s| / Π(1 − N_f·Y). F2 is a pulling triangulation of the boundary of
A itself: a sum of simplex forms 1/(|det Z|·Π t_i). Hulls are proposed by qhull and decided in exact arithmetic: every facet normal is
solved exactly through d points and every incidence is tested exactly. Arithmetic is in Q (lattices, E8 in standard coordinates) and in
Q(√5) (icosian coordinates). The icosian map is fixed by matching simple roots (Gram matrices equal) and checked on all 240 roots. For
E8 the symmetry is used once: all 240 polar facets are congruent (W(E8) is transitive on roots), and the result is repeated at a root of
the other coordinate type. The volume of 4_21 uses no symmetry (all 19440 facet cones). Runtime: 86 s on 12 cores.

## Checks (all held; FINAL ok)
- **Lattice chain, exact.** For A2, A3, A4, D4, D5, E6, E7 (simple-root coordinates) the polar of conv(roots) has coordinate volume
  exactly 1, i.e. Ω(conv roots; 0) = n!·√det. F1 = F2 holds at 2 generic points for A2–E6. For E7 (131040 F1 simplices) this test is
  skipped by a size limit; qhull agrees to 1e-12 for all seven.
- **24-cell:** Ω = 4!·2 = 48. **600-cell:** Ω(0) = 4!·vol(polar), and the polar's volume equals the 120-cell closed form
  (15/4)(105 + 47√5)a⁴ exactly. F1 = F2 holds at a generic Q(√5) point for both 600-cell shadows and both windows.
- **E8:** 2160 deep holes (norm-4 vectors / 2, β7 facets, 14 roots each) + 17280 shallow holes (norm-8 vectors other than 2r, / 3, α7
  facets, 8 roots each) = the 19440 facets. Every root is on 702 of them. The polar facet at a root has a pulled triangulation of 47872
  simplices; 240 × its cone volume = 1 exactly, at root 0 and again at root 112.
- **Icosian map:** the 240 standard roots go exactly onto the 120 + 120 icosian roots, with B(q(x), q(y)) = 2(a + b) = x·y.
- **Negative controls (all caught):**
  - bcc with only its 8 shortest vectors gives 9/16 ≠ covolume 1/2 (the truncated octahedron also needs its 6 square walls); with all
    14 relevant vectors it gives 1/2.
  - Dropping one pulled child (D4) gives 95/96.
  - One F1 term with its sign flipped breaks F1 = F2 (all four 4D hulls).
  - Swapping the par/perp scale factors misses the count by more than 30%.
  - Using the roots' shadow (the 600-cell of radius φ) as the window gives 2.3× the points.
- **Fibonacci control:** points of Z² per unit length = window length 1.376382 (count 551, expected 550.6).

## Results
| object | exact | value |
|---|---|---|
| Ω(4_21; 0) = 8!·vol(Voronoi E8) | **8! = 40320** | (vol Voronoi = 1, E8 unimodular) |
| vol(4_21), roots of norm 2 | **57/7** | 17280 α7 cones of 1/13440 + 2160 β7 cones of 1/315 |
| Ω(Voronoi E8; 0) = 8!·vol(4_21) | **328320** | Mahler product of the pair = 57/7 = 0.4943 of the Blaschke–Santaló bound (π⁴/24)² |
| shadows π(4_21) in E_par, E_perp | 600-cells (120 vertices, 600 tetrahedra), true radius² 1 + 1/√5 on both sides | Ω_true(0) = 4!·vol(Voronoi ∩ E) = −495000 + 221400√5 = 65.4502 (Voronoi slice = 120-cell) |
| window W = π_perp(Voronoi) | 720 vertices (600 on 4 facets, 120 on 30), 1200 facets with 5 vertices each | vol_true = **5φ³/6 = 5/3 + 5√5/6 = 3.530057** = density |
| slice 4_21 ∩ E_perp = W° | 1200 vertices on one sphere, 720 facets (600 with 4 vertices, 120 with 30) | Ω_true(0) = 4!·density = **20φ³ = 40 + 20√5** |
| Ω_true(W; 0) = 4!·vol(4_21 ∩ E_perp) | −17574000 + 7859400√5 | 152.6624 |
| twin window π_par(Voronoi) | same true radii, volume, Ω and counts as W | the golden twist maps one side's numbers exactly to the other's |

1. **Ω(4_21; 0) = 8! (proved).** For any lattice the Voronoi cell is {x : x·r ≤ |r|²/2, r relevant} = the polar of
   conv(2r/|r|²). Its volume is the covolume, so Ω(conv(2r/|r|²); 0) = n!·covolume. For root lattices the relevant vectors are the roots
   (Conway–Sloane, SPLAG ch. 21), so Ω(conv roots; 0) = n!·√det. E8 is unimodular: Ω(4_21; 0) = 8!. The general statement is a direct
   consequence of the bridge plus classical facts. The new part is that it is computed exactly through the whole chain A2…E8, and that
   the bcc lattice (Voronoi cell = truncated octahedron) is the case where the shortest vectors alone fail.
2. **The quasicrystal law (proved).** The polar of a projection is the section of the polar: (π_perp V)° = V° ∩ E_perp. With V = the
   Voronoi cell, V° = 4_21, so Ω(4_21 ∩ E_perp; 0) = 4!·vol(W) = 4!·(point density of the cut-and-project set) (covolume 1). The
   exact value 20φ³ is computed. The density 5φ³/6 is confirmed by counting E8 points: ratio 0.981 at radius 5 with a generically shifted
   window. The closed window counts 10% more, because lattice points on the window's boundary have positive density.
3. **Shapes.** The window W has the vertex and facet counts of the dual of the rectified 120-cell. The golden slice of 4_21 has those of
   the rectified 120-cell, with all 1200 vertices on one sphere. Whether it is the uniform one (equal edges) is not checked (lead 1).
4. **Golden twist.** In the true 8D metric the E_par and E_perp pictures have equal radii, volumes, Ω values and lattice counts. The two
   shadows are the same 600-cell, and the two windows agree in every computed number. The twist acts as an isometry of the whole
   picture. Congruence of the two windows is indicated by the data, not proved (lead 2).

**What this gives the aim.** At the top rung, "geometry gives laws" holds in a precise, small form. The canonical form of the golden
slice of the E8 root polytope is a counting law: 4! times the number of quasicrystal points per unit volume. At the centre of the 8D
polytope itself it is 8! times the volume of the lattice's cell. No physical amplitude is claimed. The E8 masses of the closing chapter
are not used here.

**Prior art and sources checked.** The private reference library is not cloned on the machine where this README was written, so no
library item was searched (lead 3). Cited from standard knowledge:
- Conway & Sloane, SPLAG, ch. 8 (icosians) and ch. 21 (Voronoi cells of root lattices; E8 deep and shallow holes);
- Elser & Sloane (1987, J. Phys. A 20, 6161), the 4D quasicrystal from E8;
- Moody & Patera (1993, J. Phys. A 26, 2829), quasicrystals and icosians;
- Arkani-Hamed, Bai & Lam (2017), positive geometries and canonical forms;
- Blaschke–Santaló (Mahler bound).

The window and its density may be stated in Elser–Sloane; the canonical-form reading and the exact values here are computed afresh.

**Faults fixed on the way.** (1) The first full run summed the 4_21 cone determinants without the 1/8! factor (it printed 328320 as the
volume). The Mahler check caught it, and the value is now 57/7. (2) The first density count used the closed window, and boundary lattice
points biased it by 10%. A generic shift was added; the closed count is still reported.

Credit: E8 from the icosians is classical (Conway–Sloane). The Golden Ladder and its top-rung reading are DICTO's (closing chapter, 5 Nov).
Canonical forms: Arkani-Hamed, Bai, Lam. The quasicrystal: Elser–Sloane, Moody–Patera.

## LEADS
1. Is the golden slice 4_21 ∩ E_perp the uniform rectified 120-cell (equal edges), and is W its exact polar shape? This is one exact
   edge-length check.
2. Prove the twin symmetry: find the E8 isometry that exchanges E_par and E_perp (or show that the windows are congruent).
3. Check Elser–Sloane and Moody–Patera in the reference library for the window shape and the density 5φ³/6; record the sources.
4. Chunk-2 style sweep: Ω of the slices 4_21 ∩ (E_perp + t) along a line in E_par (walls = where the slice's combinatorics change). These
   are the local densities of patches of the quasicrystal, the Hopscotch analogue at the top rung.
5. The 3D descent: E8 → H4 → H3 (icosahedral slice) gives the 3D window for DICTO's "golden slice → window" plan for the 3D hat (aim 3).
6. Ω of the E7 and E6 root polytopes at generic points (F1 = F2 was skipped for E7 by size; modular arithmetic would make it cheap).
