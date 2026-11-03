# Dual pairs through the dimensions (study, 2026-11-03)

DICTO proposed: "can we find out similar interactions with the other Platonic solids with their duals through the dimensions".
Follow-ups proposed the same day: OG and the D·I interactions, new golden cycles, hyper-lattice cycles, RD/TO cycles, and the
golden cut rhombic dodecahedra as 4D slices. This study follows the 6D study (studies/2026-11-03-6d-golden-cubes; its
cubes_lib.py and sixd_lib.py are copied here unchanged). The results note (typeset, 9 pages) is
`~/Documents/papers-to-read/dual-pairs-through-dimensions.pdf`, from `note/paper.html`, printed on dicto-big-brother with
~/kres-tmp/cw-print/print.mjs (footer "study, not published").

Setting: P = {n.x <= 1}, P* = conv(n). The sections of P x P* by y = x/mu are S(mu) = P cap mu P*. Their polars are the hulls
H(mu) = conv(P cup mu P*) = mu polar(S(mu)). nu = mu/r^2.

## Results (exact in Q(sqrt2, sqrt5) unless marked)

- **Lemma 1 (proof).** A corner cut at edge fraction x is S(mu) with mu = R^2 - x e^2/2 (dual side: 1/mu = R*^2 - x e*^2/2).
  So all golden cuts of #88 lie on the sweeps.
- **Sanity (s1 co, 22/22).** The 6D study's cube x octahedron sweep is reproduced exactly, including both Golden Cut Cube mu as
  exact strings.
- **D·I (s1 di, 20/20).** D has corners (+-1)^3 and (0, +-1/phi, +-phi), so R^2 = 3. The values are r^2 = 1 + 2/sqrt5,
  rho^2 = phi^2, and in mu:
  - icosahedron 1 + 2/sqrt5;
  - Lesser GCI **sqrt5**;
  - truncated icosahedron (24 + 9sqrt5)/19;
  - Greater GCI (13 + 6sqrt5)/11;
  - icosidodecahedron **phi^2**;
  - Greater GCD 2 + sqrt5/3;
  - truncated dodecahedron 1 + 4/sqrt5;
  - Lesser GCD (20 + 5sqrt5)/11;
  - dodecahedron 3.

  All are in Q(sqrt5). No golden nu is a power of phi. Over all three pairs, the only golden station whose nu is a power of phi
  is Icosaxes (nu = phi).
- **Theorem 3 (s2, 9/9; proof).** No lattice is invariant under the diagonal icosahedral action on D x D*: the trace of a
  5-fold rotation is phi, so the character is irrational. So the cut-equals-shadow test cannot be posed for D·I. Icosahedral
  Z^6 gives:
  - Voronoi sections: Z^6 -> dodecahedron, D6* -> icosidodecahedron, D6 -> RT;
  - shells: norm 1 -> icosahedron; roots -> 2 icosidodecahedra in ratio phi; (+-1/2)^6 -> dodecahedra and icosahedra.

  These are the ends and the rectified stage only.
- **T·T (s1 tt, s3: 20 + 9 checks).**
  - Golden mu: 2sqrt5 - 3 (Greater), 1 + 2/sqrt5 (Lesser), and their reciprocals on the dual side.
  - Theorem 4 (proof + exact): the tesseract's slice x1+..+x4 = 2h is T cap mu(-T) with mu = (2 + h)/(2 - h). The ratio is
    (1 - h)/h, which gives #89's heights 1/phi^2, 1/2, 1/phi.
  - Lattice Z^3 + Z^3 (T_d): the sweep vectors (norm 8) cast the corners at every mu. The isolated golden selectors have norm
    34 (Lesser) and 46 (Greater), minima in the box {-6..6}^6. So no golden selection.
- **OG (s4, s4b, s4c: 21 + 3 + 4 checks).**
  - OG = H(mu_TI) cap phi^2 D* = Q(mu_TI, phi^2), with mu_TI = (24 + 9sqrt5)/19 (norm 9/19). Checked: 102 corners, 60 kites,
    20 regular hexagons, and equal to the chain's OG.
  - The polar Dharma cycle is (3/phi^3) D ⊂ S(phi^2) ⊂ OG ⊂ H(mu_TI) ⊂ 3D* ⊂ (3/phi^2) H(phi^2) ⊂ 3D. The middle four
    stations are unscaled and touch (factor 1). The given closure is phi^3; with every link tight it is
    225/2 - 99sqrt5/2 = 1.814635, matching polar-Dharma step 4.
  - Golden relatives Q(sqrt5, phi^2) and Q((13 + 6sqrt5)/11, phi^2) have the same combinatorics as OG.
  - Lift into the Z^6 shadow module (smallest integer scale): OG 228 in our frame and 342 = 2 x 171 in the chain frame (the
    bridge study found 171; the factor 2 is presumably a module convention). The truncated icosahedron and the pentakis
    dodecahedron need 38, the dodecahedron and the Lesser GCI need 2, and the Golden OG (DICTO's name, 11-03; the golden relative at sqrt5) needs **4**. The 19
    comes from mu_TI.
- **4D first look (s5, 17/17).**
  - Tesseract x 16-cell: at mu = phi^2 the cells are Icosaxes + Lesser GCT; at 2 + 1/phi^2 they are Unborn Axes + Greater GCT.
    Both are exact corner matches.
  - Truncated-16-cell stage: GCT + octahedra at phi and 3 - phi.
  - Truncated-tesseract stage: Golden Cut Cubes at 1 + mu_G and 1 + mu_L, which need Q(sqrt2, sqrt5).
  - 24-cell x 24-cell: the self-dual point is sqrt2, where the bitruncated 24-cell has truncated-cube cells (exact). Icosaxes
    cells occur at phi and Unborn Axes cells at (15 + sqrt5)/10.
  - 600 x 120 (R = 1): the radii are r^2 = (7 + 3sqrt5)/16, triangle centres (3 + sqrt5)/6, edge midpoints (5 + sqrt5)/8.
    Golden-cell stations on every stage. In the bitruncated stage Greater GCI + Lesser GCT occur at 2 - sqrt5/2, and Lesser
    GCI + Greater GCT at (19 + 9sqrt5)/44, exact from the linear cell rules. The cell rules are checked exactly at three
    points; cell types are float.
- **Cycles (s6, s8).**
  - Two-link rule: P ⊂ H(mu) ⊂ nu P.
  - Golden cycles: C·O cube ⊂ H(phi) ⊂ phi cube. D·I closes at phi through 4 links, e.g.
    D -> ID -> Greater GCD -> triakis icosahedron -> D, or D -> RT -> ID -> Lesser GCI -> D. T·T closes at phi^6 = 9 + 4sqrt5.
  - Silver: cube ⊂ H(1 + sqrt2) ⊂ (1 + sqrt2) cube.
  - Sweep cycles close at (R/r)^2: 15 - 6sqrt5, 3, 9. The Dharma pattern closes at D·I 225/2 - 99sqrt5/2, C·O 9/2, T·T 27,
    none golden.
  - RD = H(2) and TO = S(3/2): cube ⊂ RD ⊂ 2 TO ⊂ 2 cube closes at 2. Other cycles through the RD or TO close at 1 + sqrt2 and
    phi^2.
  - Space-filler-only nesting cycles (64 of them): none closes golden.
- **Hyper-lattice cycles (s7, 14/14).**
  - The 24-cell honeycomb sliced cell-first gives the BCC pairs C cap (2 - h)O and C cap (1 + h)O: Icosaxes + Unborn Axes at
    h = 1/phi^2 and Kelvin at 1/2. This is #48's family. Volume 8 per cell is an identity.
  - Sliced vertex-first, it gives RD (FCC) -> RD cap cube -> cubes. Volume 2 per cell is an identity.
  - The tesseractic honeycomb sliced vertex-first gives both GCTs at s ≡ 1/phi^2.
  - Golden tilt: the tile heights {k/phi} coded at the Unborn Axes height form the Fibonacci word (300 letters, exact). This
    is a coding only.
  - D·I has no periodic version (rank >= 6).
- **Golden cut RD/RT as 4D slices (s9, s9b, floating point): negative within scope.** Only axes with an O_h (I_h) stabiliser
  can give such a slice. Over all 15 B4, F4 and H4 Wythoff polytopes, the RD signature appears in 9 F4 stages and the RT
  signature in 2 H4 stages, but never with equal corner sides (the only point with equal sides has ratio 0.2539).

## Prior art (library + light web search)
- Kepler, and Hart's pages: Archimedean solids as the intersection of a Platonic solid and its dual.
- Conway's ambo and truncation operations.
- Wikipedia "Truncated tesseract" and "Truncated 24-cells": bitruncation as the intersection of a dual compound, and halfway
  to the dual.
- Wikipedia "24-cell honeycomb": its vertex-first slices (RD, cubic) and cell-first slices (rectified, bitruncated cubic).
- Boole Stott and Coxeter on sections of the regular 4D solids.
- Zefiro 2011 on truncations of cubic solids.
- Kramer–Neri, Duneau–Katz and Elser on the icosahedral Z^6; Al-Siyabi–Koca–Koca 2020 on polyhedra from D6.
- #48 (Koca's orbit family), #88, #89, the 6D study, and the polar-Dharma and OG-bridge studies.

Not found anywhere: the golden stations of the D·I and T·T sweeps as 6D sections, OG as Q(mu_TI, phi^2), the all-golden 4D
cells, or the golden tight cycles.

## Uncertain / open
- Lemma 6 (120-cell cell rule) has no general proof.
- The lattice-vector minima are box minima.
- The cycle search is floating point; quoted cycles are exact.
- The 4D golden-rhombic search excludes off-base sections of prism tiles.
- The tilted slice is a coding of tile heights, not exact stations.
- The TRD (hcp, D3h) is outside the cubic sweep and was not reached.
- The 171 vs 342 module factor is not re-derived.

Naming candidates (for DICTO):
- Golden OG = the golden relative at mu = sqrt5 (NAMED by DICTO 11-03); the second relative at mu = (13+6sqrt5)/11 still unnamed;
- the all-golden 4D polytopes;
- the golden tight cycles.

## Files
- scripts/: dp_lib.py (+ cubes_lib.py and sixd_lib.py copied unchanged), s1_sweeps.py, s2_di_lattice.py, s3_tt.py,
  s4_og_dharma.py, s4b_og_lattice.py, s4c_relatives.py, s5_fourd.py, s6_cycles.py, s7_hyper.py, s8_rd_to.py,
  s9_golden_rhombic.py, s9b_rhombic_ratios.py, figs.py.
- data/: every json carries its checks (all pass); reversed-chain*.json are copied from studies/2026-10-16-polar-dharma.
- figures/: fig1-sweeps, fig2-og-dharma, fig3-fourd, fig4-honeycomb-slices.

Run on dicto-big-brother (~/kres-tmp/dual-pairs) with ~/geom/bin/python, each step under 170 s. Arguments:
s1/s6 `co|di|tt` (s6 also takes max path length 6), s4c `L|G`, s9 `B4|F4|H4`, s9b `F4|H4`; figs: `python figs.py <out> <logo>`.
