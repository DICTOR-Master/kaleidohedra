# Halves as a standing option — evidence (4 Nov 2026; plan: PLAN.md)
PRIOR ART: the operation is classical (Johnson 1966 ortho/gyro, gyrate; CO/J27 and RD/TRD dual pairs; gyrated honeycombs; Coxeter/Wikipedia: TRD = RD
with one half turned 60°). DICTO's framing (the halves stay cut; the twist is a STANDING option) is what is tested here.
E1 (twist_local.py, ../2026-11-04-dehn-screen): fcc RD packing, twist ONE cell's upper half 60°: 3 overlapping pairs, gaps and double cover — a single
   cell cannot twist. Twist one whole LAYER but leave the layers above in place: 63 overlaps — the layer above must re-seat (a stacking change).
E2 (twist_word.py, running): each ball's halves turned to face its actual neighbours in mixed stacking words (fcc, hcp, ABCB, ABCACB, Fibonacci
   approximant) — expected clean: then THE TWIST IS A FREE CHOICE PER LAYER, AND ONLY PER LAYER (states = stacking words).
E3 (dictionary): the same "one free bit per layer" in HexOct (c/h tiles), Narcissus/cube, and the Admiral network's ground states (golden-twin choice
   on cube layers — a different operation, same structure). Consequence for all four: the 1D obstruction, no shape-forced aperiodicity.
E4 (sweep_twist.py): twist convex along the whole CO–RD sweep; on the cube–octahedron sweep only at the CO (-> J27); the regular TO's twist is dented.
   permuto_twist.py: the B3 permutohedron (DICTO's "TO with irregular hexagons") twists convexly, but the twist is not Dehn-zero (seam angles 109.5°, 141.1°).
E5 (twist_map.py, family cube ∩ μ·octahedron ∩ ν·RD, 2,045 points, golden/Fibonacci marks included): 513 twist-convex; NO member with a Dehn-zero
   convex twist except the RD itself (ν = 1, calibration -> TRD); just off it (ν = 1.0005) Dehn nonzero. => RD/TRD looks ISOLATED. Caution: the
   numerical Dehn screen is fragile near tiny edges; the count of Dehn-zero solids (586) needs re-checking before use.
E6 (halves.py census, all classical + OG family): calibration CO -> J27, RD -> TRD; OG family twists all dented so far (2- and 3-fold axes); 5-fold to check.
E7 (cut_shadow.py, DICTO "solids with a central band"): a band between the halves keeps every twist convex iff the central cut equals the shadow.
   RD: cut = shadow on its 2-, 3- and 4-fold axes; TO and cube: on 2- and 4-fold, NOT 3-fold (0.84, 0.75 — why the TO's 3-fold twist dents);
   elongated dodecahedron: 2- and 4-fold. Only a hexagon cut (3-fold) gives a real twist option in a tiling (each cut tile turned in place still
   tiles the plane); so the RD gives banded space-fillers half + hexagonal-prism band + half, straight or twisted, any band height, any stacking.
   Prior art for the 3-fold-banded RD/TRD to check (the known elongated dodecahedron is banded along the 4-fold axis).
E8 (slant_band.py, DICTO "slanted hexagonal prisms with a double angle"): a LEANING band dents at every lean and height (the half's walls meet the
   hexagon vertically — cut = shadow — so any lean kinks); the chevron (out and back) is worse. Leaning the WHOLE cell (a shear) stays convex and keeps
   the tiling: each layer slid along its lean (DICTO Hex Prism; Kaleidohedra's shear). Again: the option lives on the layer.
E2 SETTLED: fair test (twist_word.py) clean on ABC (fcc), AB (hcp), ABCB, ABCACB and the Fibonacci approximant ABACBCAC: 0 overlaps, every point covered once. With E1: the twist is a free choice per layer, and only per layer.
E6 census (classical): only the CO (-> J27) and the RD (-> TRD) twist convexly; every other classical solid's twist dents. OG family: incomplete
   (3 of 9 processed, no 5-fold axes found: tolerance on float data) — rerun with tolerance 1e-4 (halves-og.log).
E9 PRIOR ART: banded STRAIGHT join = the known general trapezo-rhombic dodecahedron ("tall hexagonal prism with 3 angled cuts top and bottom",
   space-filling; hcp Voronoi cell only at long side = 2 × short side). Banded TWISTED join (RD banded along its 3-fold axis) not found; the known
   elongated dodecahedron is banded along the 4-fold axis (Fedorov). Fuller search before any claim.
E10 (hexoct_voronoi.py): along the whole HexOct walk neither tile is ever the RD / TRD (never a convex 14-corner solid) — the dictionary HexOct <->
   half-cells is STRUCTURAL (same one-bit-per-layer law, different pieces), not an identity.
E11 NARCISSUS AS A SPLIT-AND-ROTATE PIECE: two Narcissus on their hexagons — straight = the twisted cube (11 corners; fills with the brick); turned 60° =
   a convex, centrally symmetric dodecahedron with 12 PARALLELOGRAM faces (14 corners, volume one ball) = a 4-zone parallelohedron: three orthogonal
   edges 1/√2 (the small fcc cube's) + one along the body diagonal, 1/3 of it (c = 1/3 in the family Z(e1, e2, e3, c·(1,1,1)): c = 0 cube, c = 1 RD).
   Fills space alone by translation. Prior art: the family is classical; its c = 1/3 member splitting into two copies of a self-mirroring piece
   (that also gives the twisted cube) — to check. NAMED COVENANT by DICTO (4 Nov).
E12 PRIOR ART (Covenant): tiling classical (Fedorov via Grünbaum 2010); c = 1/3 member unnamed, faces not rhombi; the Narcissus split (and the twisted-cube relation) not found — the chapter's claim.
E13 Covenant tiles by the fcc LATTICE itself: 6 face-to-face translations, all length 1 (ball spacing); 12 nearest at 1, 6 at √2; one Covenant per
   ball. So NARCISSUS FILLS BOTH PURE STACKINGS ALONE: fcc as Covenant pairs (turned 60°), hcp as h-tiles. Mixed stackings: open (next fair test).
   CAUTION (checked): in the Covenant tiling, with the lower Narcissus point on a ball, its 3 hexagon ball-corners are fcc balls but the UPPER point
   is not (2/3 of a lattice vector) — so Covenant is an fcc fundamental domain, NOT a ball-tied c-layer cell. Ball-tied: Narcissus fills h layers,
   the cube c layers (HexOct pairing, every stacking). Free of the balls: Narcissus alone fills space as the h-tiling and as Covenant (fcc lattice).
   "One piece for everything, ball-tied" -> the Narcissus–cube common-dissection study (2026-11-04-narcissus-cube).
