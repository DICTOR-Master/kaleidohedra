# One piece, any stacking — step 2: which keys can work (5 Nov 2026)
DICTO's aim (5 Nov): a single RD/TRD-cross piece that fills space alone and can only do so aperiodically.

1. Stacking-bit keys only: CLOSED. The per-layer twist law (fair test, 4 Nov) makes the turn one bit per seam plane, so the stacking is a 1D sequence.
   Rules over finitely many layers make it a 1D subshift of finite type, and every non-empty one of those has a periodic point.
2. Irrational screw (Schmitt–Conway–Danzer route): CLOSED for this family. The hexagon seam allows only 0/60/120 degrees, and Narcissus is convex only there.
3. In-plane key: OPEN. Each layer is a triangular lattice of cells, which is exactly the Socolar–Taylor setting: a hexagonal tile with markings, used in 12 orientations including mirrors.
   Narcissus is achiral, so its mirror images come free. Expected result: weakly aperiodic (no in-plane translation; z-periodicity still possible).
   PRIOR ART to read first: Socolar & Taylor, "An aperiodic hexagonal tile", JCTA 118 (2011), including their 3D connected-tile realization.
4. In-plane plus vertical coupling: OPEN, and the strongest form. A single row bit cannot be forced, but the rows of a 2D SFT can be forced to be Sturmian/Fibonacci
   (Aubrun–Sablik 2013; Durand–Romashchenko–Shen 2012: every effective 1D subshift is a row projection of a 2D SFT). So the stacking can be forced
   only if the in-plane pattern carries hierarchical information and the turn reads it. Hard, but not ruled out.
NEXT (step 3): read Socolar–Taylor, then map their markings onto the Narcissus layer and SAT-test.

## Step 3 (11-05, DICTO "go ahead with 1")
Socolar–Taylor digest (DBB study-runs/2026-11-05-one-piece/digest.md, from arXiv 1003.4279 and 1009.1419):
- 2D monotile: R1 stripes continuous across edges; R2 flags agree between SECOND neighbours (tiles one edge apart); mirror image required
  (Narcissus is self-mirroring: free); hierarchical, scale factor 2, limit-periodic; paperfolding sequences along rays.
- Their 3D tile ("congruent to its reflection", can be a topological sphere): "corrugated slabs of the limit-periodic pattern that stack
  PERIODICALLY in the direction orthogonal to the nonperiodic tiling plane"; one slab = three sublattices at different heights (R2 made geometric).
=> ROUTE 3 ALONE CLOSED for the aim: an in-layer ST key gives aperiodic layers but allows periodic stacking (their own 3D tile does exactly that).
DESIGN for ROUTE 4 ("the hierarchy on its side"): in a close-packed stacking, a vertical plane along a row of touching pieces is combinatorially a
triangular lattice (2 neighbours in-layer, 2 above, 2 below) = ST's hexagon tiling with its ROWS = our LAYERS. Put a scale-2 hierarchical SFT
(ST or Robinson type) into that plane; add a ROW label equal along each row and tied to the row's level parity (v2 of the row index mod 2);
tie the layer's c/h choice to that label → the stacking word is forced to be the PERIOD-DOUBLING sequence (aperiodic). Planes repeat
periodically sideways. This is the Aubrun–Sablik / Durand–Romashchenko–Shen escape from the 1D obstruction, made concrete.
NEXT: (a) SAT model of the combinatorial key (vertical-plane hierarchy + row label + c/h), test: no periodic solution on tori up to a size,
patches exist, stacking word forced; (b) geometry: can the c/h layer shift be read by Narcissus faces in the vertical plane; (c) compress the
labels into keys on ONE piece (as ST compress Robinson-like rules into one hexagon).

## Step 3a: the combinatorial key works (kari_key.py; exact arithmetic, SAT)
Engine: Kari's aperiodic Wang tiles (rows multiply by 2 or 2/3), generated exactly; carries tagged by multiplier so a row cannot mix (first run
without tags let periodic tilings through: caught by the calibration). Rows = layers; x2 row = c, x2/3 row = h; each row's left/right shift in
the vertical plane decides c/h (c iff consecutive shifts equal).
- Calibration: open 24x24 block exists; NO periodic tiling on any torus up to 10x10 (100 tori).
- Key: on a 12x12 torus UNSAT (no periodic stacking survives).
- Stacking words allowed (width 24): height 6: 9, height 8: 12, height 10: 18 (unkeyed: 64, 256, 1024). Read top-down, every word of Kari's
  map itself is allowed and only ONE extra appears (the tie at x = 1, which both multipliers accept).
Overnight (DBB study-runs/2026-11-05-one-piece/kari-overnight.log): tori to 30x30, words to height 16 at width 40, orbit comparison.
Next: 3b geometry (Narcissus faces in the vertical plane carrying the shift and the tile colours as keys); 3c one piece.
