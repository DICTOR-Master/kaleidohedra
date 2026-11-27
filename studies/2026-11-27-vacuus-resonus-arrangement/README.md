# The joint Vacuus + Resonus arrangement (study, 27 Nov 2026)

DICTO's conjecture, his words: "create intersecting planes of vacuus and resonus to define their intersectionality and resolve
desired outcomes via those planes through trigonometry ... including but not limited to calculating new combinations of or
alternative spacefilling solutions." Fairness of dice is one use, not the aim. DICTO "yes to all" (27 Nov) to:
1. state it as an arrangement theorem (finite explicit angle basis; space-filling, combinations and fair faces become exact linear
   conditions on cell counts), fairness a corollary; 2. n = 4 exactly; 3. Dehn-invariant filter on cells and unions, then tiling
   tests; 4. its own paper. With Claude (Anthropic).

## Step 1: n = 4, the truncated octahedron (scripts/joint4.py, logs/joint4.log, data/joint4.json)
P4 centred in the 3-space sum y = 0. All exact (fractions).
- 36 edges give **15 Vacuus planes**; 14 facets give **7 Resonus planes**; 3 Resonus planes are also Vacuus planes, so the joint
  arrangement has **19 distinct planes** (agrees with #120 and the Lean entry: A402191(4) = 15, 2^3 - 1 = 7, 2^2 = 4 not ridge planes).
- **93 lines** through the centre: 75 where 2 planes meet, 12 where 3 meet, 6 where 5 meet (the 6 four-fold-type axes of P4's
  square faces... to confirm by direction).
- **248 cones** (cells from the centre): 2 + 2 x sum (m - 1).
- Plane-pair angles, exact cos^2: 0 (15 pairs), 1/81 (12), 1/27 (24), 1/9 (18), 16/81 (24), 1/3 (24), 4/9 (24), 49/81 (6),
  64/81 (12), 25/27 (12).
- Angle basis (identified by PSLQ at 60 digits, NOT yet proved): every plane-pair angle is a rational combination of pi and
  five basic angles arccos sqrt(25/27), arccos sqrt(64/81), arccos sqrt(4/9), arccos sqrt(16/81), arccos sqrt(1/27); e.g.
  arccos(1/9) = pi - 2 arccos(2/3) (exact by the double-angle formula), arccos sqrt(1/3) = pi/3 - (1/3) arccos sqrt(25/27).
  Whether the five are independent over Q (with pi) is open (step 2).

## Next
2. Exact proofs of the relations (double/triple-angle identities, checked symbolically) and of independence where possible.
3. The pieces of P4 cut by the 19 planes (bounded cells); their Dehn invariants in the angle basis; unions with Dehn invariant 0
   = space-filling candidates; then tiling tests.
