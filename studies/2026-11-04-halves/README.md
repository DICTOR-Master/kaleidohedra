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
