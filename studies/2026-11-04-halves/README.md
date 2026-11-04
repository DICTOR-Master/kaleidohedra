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
