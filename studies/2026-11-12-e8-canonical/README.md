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
   the rectified 120-cell, with all 1200 vertices on one sphere. It IS the uniform rectified 120-cell, and W is exactly its polar
   (proved exactly below, "Leads 1-3").
4. **Golden twist.** In the true 8D metric the E_par and E_perp pictures have equal radii, volumes, Ω values and lattice counts. The two
   shadows are the same 600-cell, and the two windows agree in every computed number. The twist acts as an isometry of the whole
   picture. The two windows are congruent: proved exactly below (an automorphism of E8 exchanges E_par and E_perp).

**What this gives the aim.** At the top rung, "geometry gives laws" holds in a precise, small form. The canonical form of the golden
slice of the E8 root polytope is a counting law: 4! times the number of quasicrystal points per unit volume. At the centre of the 8D
polytope itself it is 8! times the volume of the lattice's cell. No physical amplitude is claimed. The E8 masses of the closing chapter
are not used here.

**Prior art and sources checked.** At first written without the reference library; the library check is lead 3, done below. Cited:
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
1. DONE (below): the golden slice is the uniform rectified 120-cell; W is its polar, the dual of the rectified 120-cell.
2. DONE (below): Ψ = φ⁻¹Pσ is an automorphism of E8 exchanging E_par and E_perp; the two windows are congruent.
3. DONE (below): library checked; Koca–Koca–Al-Ajmi 2011 §5.3 misnames the window (it is their §5.2 polytope).
4. Chunk-2 style sweep: Ω of the slices 4_21 ∩ (E_perp + t) along a line in E_par (walls = where the slice's combinatorics change). These
   are the local densities of patches of the quasicrystal, the Hopscotch analogue at the top rung.
5. The 3D descent: E8 → H4 → H3 (icosahedral slice) gives the 3D window for DICTO's "golden slice → window" plan for the 3D hat (aim 3).
6. Ω of the E7 and E6 root polytopes at generic points (F1 = F2 was skipped for E7 by size; modular arithmetic would make it cheap).

## Leads 1-3 closed, and the window against Koca 2011 (12 Nov 2026; `scripts/e8_leads.py`, `scripts/e8_koca.py`; logs `data/e8leads.log`, `data/e8koca.log` and pilots; FINAL ok, exact over Q(√5) unless stated)

**Conclusion.** The golden slice 4_21 ∩ E_perp is exactly the uniform rectified 120-cell, and the window W = π_perp(Voronoi) is exactly
its polar, the dual of the rectified 120-cell: 720 corners on two spheres (radius ratio 1.0607), 1200 cells, all triangular dipyramids.
The two golden windows are congruent through an automorphism of E8. Koca–Koca–Al-Ajmi (2011, §5.3) name a different polytope as the
projected Voronoi cell (the dual of the rectified 600-cell, 720 pentagonal dipyramids); that sentence is wrong. The right one is their own
§5.2 polytope.

**Lead 1: the slice is the uniform rectified 120-cell (proved).** W is rebuilt as the exact hull of all 19440 shadows of the Voronoi
vertices (720 vertices, 1200 facets). Its polar S (vertices = W's facet normals) is checked exactly:
- f-vector (1200, 3600, 3120, 720); all 1200 vertices on one sphere; all 3600 edges of one length; every vertex of degree 6;
- 2-faces: 2400 triangles + 720 pentagons, each a cycle of equal edges on the sphere, so each is cyclic and regular;
- cells: 600 regular tetrahedra + 120 icosidodecahedra (30 vertices, 60 equal edges, 20 triangles + 12 pentagons, two of each at
  every vertex, every edge in one triangle and one pentagon). So the cells are icosidodecahedra and tetrahedra, not icosahedra;
- symmetry: the 60 reflections in the 120 H4 roots (the roots' shadow) map S onto itself; H4 has order 14400 (free orbit of a generic
  point); it is transitive on the 1200 vertices; a vertex is fixed by exactly 4 reflections, of type A1 × A2 (cos² = 0 for 3 pairs,
  1/4 for 3 pairs). S's vertex set is exactly a positive multiple of the Wythoff orbit o5x3o3o (ring next to the 5-branch). This is
  the uniform rectified 120-cell by Wythoff's construction.
Controls: the 600-cell (o5o3o3x: f = (120, 720, 1200, 600), stabilizer H3 with 15 reflections) and the 120-cell (x5o3o3o:
f = (600, 1200, 720, 120), stabilizer A3 with 6) pass the same test; the 600-cell does not match the wrong ring; S with one vertex
moved 1/1000 leaves the sphere and loses H4 invariance; W itself fails uniformity (two radii, edge lengths of two kinds: 2400 + 720).

**Lead 2: the two windows are congruent (proved).** Let σ be the golden twist √5 → −√5 on icosian coordinates. σ alone does not keep
the icosian ring (Moody 2000, §4.1: I* ≠ I). But Ψ(q) = φ⁻¹·P(σq), with P an odd signed permutation of the four coordinates (192 of the
384 signed permutations work, all odd), maps the 240 roots onto themselves. In standard E8 coordinates Ψ is an orthogonal rational
8 × 8 matrix (det 1, order 4) mapping roots to roots, so it is an automorphism of E8. It maps the 19440 Voronoi vertices onto themselves
and exchanges the golden spaces: par(Ψx) = φ⁻¹P·perp(x) and perp(Ψx) = −φP·par(x). Hence W_par = φ⁻¹P·W_perp (checked on all 19440
shadows), and φ⁻²c_par = c_perp exactly, so φ⁻¹P is an isometry of the true metrics. The windows are congruent, and so are the slices.
Negatives: φ⁻¹σ without P and φ·Pσ do not keep the roots; φ²c_par ≠ c_perp.

**Lead 3 and the Koca question.**
- *Koca, Koca, Al-Ajmi (2011), "Branching of the W(H4) polytopes and their dual polytopes under the Coxeter groups W(A4) and W(H3)
  represented by quaternions", library file bridges/Koca-Koca-AlAjmi-2011-Branching-H4-polytopes.pdf; §3.3–3.4 and §5.1–5.3 read in the text layer:*
  §5.2 builds the dual of O(0,1,0,0) (the rectified 120-cell): vertices O(1,0,0,0) ∪ O(0,0,0,1) on two spheres with R4/R1 = 1.061,
  cells triangular dipyramids. §5.3 builds the dual of O(0,0,1,0) (the rectified 600-cell, their "720-cell" of 600 octahedra and
  120 icosahedra): 720 vertices, R4/R1 = 1.023, 720 cells, pentagonal dipyramids. It ends: "This polytope is the projection of the
  Voronoi cell of W(E8) [24] with 19,440 vertices into 4D space with the residual symmetry W(H4)" ([24] = Elser–Sloane 1987). The text
  is not garbled at that point: the claim sits under the pentagonal-dipyramid polytope.
- *Exact comparison (`e8_koca.py`).* Both candidates are built as polars of their Wythoff orbits and reproduce Koca's descriptions
  exactly (controls): dual rectified 120-cell f = (720, 3120, 3600, 1200), 1200 triangular dipyramids, ratio 1.0607; dual rectified
  600-cell f = (720, 3600, 3600, 720), 720 pentagonal dipyramids, ratio 1.0233. The window, from all 19440 projected Voronoi vertices,
  has f = (720, 3120, 3600, 1200), 1200 triangular dipyramids, ratio 1.0607. Its vertex set equals the dual rectified 120-cell's up to one
  positive scale, exactly, and does not equal the dual rectified 600-cell's. Both have 720 corners in two H4 orbits (120 + 600), which
  explains the mix-up. By Lead 2 the other golden window gives the same answer. True volume of W: 5φ³/6 (chunk 7, exact), confirmed by the
  lattice count (numerical).
  **Verdict:** Koca 2011 §5.3's last sentence is wrong. The projected E8 Voronoi cell is the dual of the rectified 120-cell (their §5.2).
- *Elser & Sloane 1987* (J. Phys. A 20, 6161–6168, doi 10.1088/0305-4470/20/18/016) and *Moody & Patera 1993* (J. Phys. A 26,
  2829–2853, doi 10.1088/0305-4470/26/12/022): **not in the library** (link-only entries, paywalled). Web sources checked: both
  publisher abstract pages (iopscience.iop.org). Neither abstract states the window's shape or the density; the full texts were not read.
- *In the library and read:* Baake & Gähler 1998 (arXiv cond-mat/9809100): the window is "a special polytope with H4 symmetry"; no shape
  and no density. Moody 2000, "Model sets: a survey", §4.1: the icosian cut-and-project scheme, I* ≠ I; no window shape and no density.
- *Web, not in the library:* Corradetti, Chester, Aschheim, Irwin 2023 (arXiv 2303.12219, §6.4, eq. 6.22): the Elser–Sloane window is
  the hull of 720 vertices (orbit representatives given). This agrees with our count; they do not name the polytope or give a density.
- So: the window's name (dual of the rectified 120-cell) and the density 5φ³/6 were found stated in no source read. Elser–Sloane's full
  text may state them, and that is open.

**Precision.** Everything in this section is exact over Q(√5), except the radius ratios printed to 4 decimals (their squares are exact)
and the lattice count of chunk 7, which is numerical.

**Further leads.** (a) Read Elser–Sloane 1987 in full (needs a copy). (b) Ψ has order 4 and det 1: is it in W(E8), and does Ψ² = −1?
(c) A short note to the Koca group on §5.3, DICTO's call.
