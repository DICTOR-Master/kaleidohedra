# New cycles after #43 DICTO Kyushindo Cores (DICTO's ideas, 2026-10-21)

Three follow-up cycles, built exactly in Q(sqrt5) on the node with the #38/#39 machinery (`exact_cycle.step` = T, `rev` = P,
`solid`, `polytope`, `volume`, `inside`, `kinds`) and the patches of `og-turned-out/polar_turned.py`; shared code in `nc_common.py`.
Golden turned-out step: S_k = phi^k P^k(core). Towers = cone from the centre over each face of the inner solid, cut by the outer solid;
"one volume per orbit, sum = shell exactly" is checked for every shell. Lemma 3: polar(P S) = T(polar S) (unit sphere).
Every log line is PASS (A 53, B 25, C 44; no FAIL). Figures are float copies of the exact boundaries (#18 standard).

| item | status |
|---|---|
| A. CLEO turned out, beats 0-7, shells 1,1,2,3, towers, polar | exact |
| B. Polar of the OG upward family, k <= 4, nesting, towers | exact |
| C. DICTO OTT turned out, beats 0-7, t_min, shells 1,1,2,3, towers, polar | exact |
| Figures A, B, C | float (pictures of the exact solids) |
| Congruence of equal-volume tower orbits (B, C) | not reached (only volumes compared) |

## A. CLEO turned out (`cleo_turned.py`, `cleo-turned.log`, `cleo-turned.json`, `figures/cleo-turned-out.jpg`)
Start: the CLEO sphere core = the ID of Cleo Towers (radius phi, standard frame), all 60 rotations.
- The turned-out CLEO is the UP cycle run BACKWARDS: S_0 = ID, S_1 = (11/20 + sqrt5/4) x FPD (32 corners, 60 triangles),
  S_2 = (9/10 + 2 sqrt5/5) x GTI (60 corners, 12 pentagons + 20 hexagons), S_3 = (29/20 + 13 sqrt5/20) x RT (32 corners, 30 rhombi),
  each exactly a multiple of the UP-cycle solid (T^j ID). P^4(ID) = (phi^4/10) ID, so S_(k+4) = (phi^8/10) S_k,
  phi^8/10 = (47 + 21 sqrt5)/20 = 4.697871 (per beat 1.472229 < phi). Beats 0-7 built; all fully symmetric; each S_(k-1) inside S_k
  exactly (Theorem B, checked).
- Shells (boundaries 0, 1, 2, 4, 7): S0->S1: 32 towers, 20 on triangles 0.518041 + 12 on pentagons 1.874290 (gap 32.852295);
  S1->S2: 60 towers on triangles, one shape, 1.699619 (gap 101.977169); S2->S4 (2 beats): 12 on pentagons 10.184169 + 20 on hexagons
  58.180999 (gap 1285.830010); S4->S7 (3 beats): 20 on triangles 678.788483 + 12 on pentagons 2978.679005 (gap 49319.917720).
  One shape per orbit; every shell exact.
- Polar: polar(ID) = T(ID)/phi^2 (the RT) exactly; polar(S_k) = phi^-k T^k(RT) exactly for k = 0..7 (RT, GTI, FPD, ID, ...),
  nested inward. Inward shells (phi^7 frame): 32 towers (12 pent 232.396685, 20 hex 810.321926); 60 on triangles 94.716547;
  30 on rhombi 77.957025; 32 (20 tri 3.518860, 12 pent 15.441566).

## B. Polar of the OG upward family (`og_up_polar.py`, `og-up-polar.log`, `og-up-polar.json`, `figures/og-up-polar.jpg`)
P^k(H) = polar(T^k OG) exactly for k = 0..4 (H = DICTO Hecatodihedron). All 60 rotations. Volumes in the phi^4 frame.
- H: 80 corners, 102 faces (60 triangles, 30 four-sided, 12 pentagons). P H = polar KRE: 90 corners (102 foot points, 12 not
  corners), 92 faces (60 tri, 12 pent, 20 hex). P^2 H = polar PHE: 92 corners, 180 triangles (2 kinds). P^3 H = polar TPP: 180 corners,
  212 faces (120 tri, 60 four-sided, 12 pent, 20 hex). P^4 H = polar DPHP: 152 corners (212 foot points, 60 not corners), 270 faces
  (240 triangles in 3 kinds, 30 four-sided).
- Nesting, all 10 pairs, exact, both sides agree: every pair nests EXCEPT P^4 H not inside P^3 H (120 corners outside, largest excess
  0.039), which is TPP not inside DPHP (60 corners outside). So the polar breaks at exactly the one place #39 breaks. P^4 H is inside
  P^2 H, P H and H.
- Towers: P H -> H: 80 towers (60 tri 0.083986, 20 hex 1.437327) + 12 flat (P H's 12 pentagons lie on H's pentagons, volume 0
  exactly), gap 33.785689. P^2 H -> P H: 180 towers, 3 orbits (60 at 0.093254, two orbits of 60 at 0.121083), gap 20.125202.
  P^3 H -> P^2 H: 212 towers, 5 orbits (2 x 60 tri 0.022899, 60 four-sided 0.407514, 12 pent 0.028590, 20 hex 0.009861), gap 27.739060.
  Across the break, P^4 H -> P^2 H: 270 towers, 5 orbits (2 x 60 tri 0.070807, 60 tri 0.167173, 60 tri 0.188535, 30 four-sided
  0.214584), gap 36.276870.

## C. DICTO OTT turned out (`ott_turned.py`, `ott-turned.log`, `ott-turned.json`, `figures/ott-turned-out.jpg`)
Exact OTT from `2026-10-20-ott-rays/cut8-exact.json` (24 corners, 38 faces: 24 + 8 triangles, 6 four-sided; 3 kinds).
- Symmetry, found exactly (48 signed permutations + 60 icosahedral rotations tested): 12 rotations (the tetrahedral group T), 24
  symmetries with the central inversion (T_h, pyritohedral). NOT the octahedral rotation group (24): the RT has no 4-fold axes.
  Towers are grouped by T orbits (and T_h / icosahedral orbits where they apply).
- Surprise: after ONE beat the family is icosahedral. P(OTT) has 38 foot points; 8 are not corners, and the other 30 are exactly
  c x ID (the CLEO sphere core), c = (sqrt5 - 1)/3 = 0.412023. Hence S_k = phi c x (CLEO turned out S_(k-1)) exactly for k = 1..7:
  the OTT cycle is A one beat behind (S_1 ID, S_2 FPD type, S_3 GTI type, S_4 RT type, S_5 ID, ...).
- t_min exact (all <= phi by exact sign; nesting S_k inside S_(k+1) exact for k = 0..6, agreeing with t_min):
  t_min(OTT) = (5 - sqrt5)/2 = 1.381966 (phi - t_min = sqrt5 - 2 = 0.236068; equals R/r_next); ID type (D_1, D_5) and
  GTI type (D_3) = 3/phi^2 = (9 - 3 sqrt5)/2 = 1.145898; FPD type (D_2, D_6) = 5 - 5 sqrt5/3 = 1.273220; RT type (D_4) = 1.381966, the
  same value as the OTT. Theorem B covers every beat from 1 on; the only non-icosahedral step, OTT -> S_1, has margin 0.236.
  The same values are the t_min of A's solids (t_min is scale-free and the solids are exact multiples).
- Shells (boundaries 0, 1, 2, 4, 7): S0->S1: 38 towers, 5 T-orbits / 3 T_h orbits (24 tri 0.045008, 8 tri 0.143930, 6 four-sided
  0.090016), gap 2.771739. S1->S2: 32 towers (20 tri 0.153494, 12 pent 0.555345; 2 icosahedral orbits), gap 9.734013. S2->S4: 60 towers
  on triangles, one icosahedral orbit, 2.186826 each, gap 131.209535. S4->S7: 30 towers on rhombi, one icosahedral orbit, 147.401121
  each, gap 4422.033619.
- Polar: polar(OTT) = 38 corners, 24 faces: 12 triangles + 12 HEPTAGONS (the only heptagons in these studies). polar(S_k) =
  phi^-k T^k(polar OTT) exactly for k = 0..7; T(polar OTT) is already an RT (30 rhombi), then GTI, FPD, ID, ... All nested inward.
  Inward shells (phi^7 frame): 30 towers on rhombi (6 at 5924.435828, 24 at 6131.342035); 32 (12 pent 784.338810, 20 hex 2734.836500);
  32 (20 tri 315.710786, 12 pent 1587.068371); 60 on triangles 41.958741.

## Figures (`cycles_figs.py` + `cycles_compose.py`, shots with jewel-shots.mjs on the node)
`figures/cleo-turned-out.jpg`, `figures/og-up-polar.jpg`, `figures/ott-turned-out.jpg`: boundary solids (faces by kind: triangles gold,
four-sided purple, pentagons lilac, hexagons bronze, heptagons grey-blue), each shell's towers drawn apart on the faint inner solid;
A and C add a row of polar solids.

Run: `python3 <script> ~/og-poly/2026-10-19-five-fold-octet` (C also takes `.../2026-10-20-ott-rays/cut8-exact.json 7`); A 47 s, B 8 min, C 2 min.

DICTO · dictospheres.com
