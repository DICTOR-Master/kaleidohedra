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

## Step 3b (11-05): where the key sits on Narcissus (design note, no computation yet)
Narcissus N (HexOct chapter): two N joined on their hexagonal faces, the upper turned over, make the twisted cube when put on STRAIGHT and Covenant
when TURNED by 60°. So the stacking choice at each layer interface is already a join type of N on its hexagon: straight or turned.
Mapping of the Kari key: (1) vertical Wang colours (north/south digits 0, 1, 2) and the row's multiplier tag sit as keys on N's hexagonal faces;
(2) horizontal carries (tagged by multiplier) sit on the lateral faces along one in-layer row direction (the vertical plane's rows); the other
in-layer directions carry no key, so planes repeat sideways; (3) the multiplier ↔ join type coupling: hexagon keys drawn so that x2-tagged keys
mate only when the join is straight and x2/3-tagged keys only when turned by 60° (a key pattern with 3-fold symmetry plus a 60°-distinguishing mark).
Count: one keyed N per Kari tile (Kari: 14; our generated set: see kari-key.json), so step 3b gives ~14 keyed copies of ONE shape.
Open for 3c (one piece): fold the ~14 key patterns into a single key pattern on N, as Socolar–Taylor fold their rules into one hexagon (their
R2 is realised by heights in a corrugated slab: a model for using N's height in the layer). Check first with SAT: N-shaped cells on the actual
close-packed vertical-plane neighbourhoods (2 in-layer, 2 above, 2 below) instead of the square Wang grid.

## Step 3b RESULTS (11-05 evening; scripts n_slabs.py, n_faces.py, reversed_rows.py, keyed_n_sat.py)
1. NARCISSUS ALONE, ONE FREE BIT PER LAYER (n_slabs.py): a slab of N (down-N on X, up-N on Y, mid corners over Z) has both faces tiled by
   the hexagons; the next slab = mirror in the top plane (STRAIGHT) or mirror + 60° turn about a hexagon centre (TURNED). Every word fills:
   10 words incl. SSSSS (= h-tiling), TTTTT (= Covenant pairs), random mixes: every sample point in exactly one N (20 000 points each).
   Exactly two choices per interface (the 60° turn is a honeycomb symmetry but not a slab symmetry). Closes "mixed stackings: open" (halves E13).
2. FACE MAP (n_faces.py): hexagon -> the N across the interface; 3 quads -> the 3 opposite-pointing N of the slab; 6 vertical triangles ->
   the 6 same-pointing N (triangular lattice). Turned slabs rotate pieces by 60°, a piece can turn only by 120°: rows read reversed there.
3. REVERSED ROWS (reversed_rows.py): Kari's 14 tiles also tile right-to-left rows (carries K - g, K = -1 for x2, 1/3 for x2/3): no extra pieces.
4. KEYED SET = 17 copies of N: 14 tile pieces (hexagon: input digit n + 3 bumps, x2 at the corners not over mid corners -> mates only TURNED,
   x2/3 at the corners over mid corners -> only STRAIGHT; quad Q0 = output digit s; Q1,Q2 'p'; triangles az 0 / 180 = carry out / in, tagged
   by q; others 'side') + 3 relays d = 0,1,2 (hexagon digit d + 3 holes over mid corners; one quad receives d; two 'r'; triangles 'rt').
   p<->r forces every slab to be tiles on one sublattice and relays on the other.
5. THEOREM (density argument, Kari's): in a slab every tile piece has q n + in = s + out, carries bounded -> dens(s) = q dens(n);
   relays carry s down to n one slab lower by a lattice bijection -> x_{k-1} = q_k x_k, q = 2 (turned) or 2/3 (straight), x in [1/2, 2].
   A periodic word multiplies x by 2^a/3^b != 1 per period: impossible. So EVERY tiling by the 17 keyed Narcissus has a NON-PERIODIC
   stacking word (no tiling has a period with a vertical component). Existence: Kari's tilings (rows reversed in turned slabs) give one.
6. SAT ON REAL GEOMETRY (keyed_n_sat.py; proper rotations only, actual face contacts; pilot W=6, D=2, 3 interfaces): 7 of 8 words SAT,
   TTT UNSAT (three x2 rows exceed the range) as Kari predicts. Bug found and fixed first: coplanar triangles at other heights were taken as contacts.
   Full scan (64 words, W=10): DBB study-runs/2026-11-05-one-piece/keyed-n-scan.log.
Next (3c): fold the 17 keys into ONE keyed N (or few), as Socolar–Taylor fold theirs; physical key shapes (bumps/notches) for a print.

## Step 3b full scan (DBB keyed-n-scan.log, W=10, D=2, 6 interfaces): 48/64 words SAT; all 16 UNSAT words contain TTT (Kari: no three x2 rows);
   4 words with TTT stay SAT where the TTT touches the free top slab. FINAL ok 433 s.
## Step 3c (11-05 late): reductions tried
- Culik-type set (x3 on [1/3,2/3], x1/2 on (2/3,2]; culik_tiles.py): 12 q-tagged tiles, reversed rows OK (K=-2, 1/2), BUT it contains the
  all-zero tile (n=s=0, carries 0) in x1/2 rows: an all-zero, all-straight tiling is periodic. REJECTED (Kari's digit sets keep x >= 1/2).
- One relay instead of three (digit = relay rotation, mark on hexagon): the slab below reads the mark relative to ITS OWN row direction, and
  row directions of consecutive slabs are independent (3 choices each), so digits could be read cyclically shifted: proof breaks. A relay would
  need digit x orientation = 9 states > 3 rotations. REJECTED in this architecture.
CONCLUSION 3c (so far): with layered Kari keying, 17 keyed Narcissus is where this architecture stands (14 tiles + 3 relays); fewer needs a
new mechanism: (a) Socolar–Taylor-type rules reaching second neighbours (shape features across a neighbour), folding tile identity into
placements; (b) carrying the row direction through the relays by shape (would allow the single relay -> 15); (c) mirror placements (6 per site).

## Route (a), step 1 (11-06): how much one piece can carry per site
- In an N-only slab every site is fixed as down (X) or up (Y); a keyed piece fits a site in at most 6 ways (3 turns, and 3 mirror placements
  if mirror copies of the keyed piece are allowed), only 3 ways without mirror copies.
- Kari's set has 4 tiles for x2 and 10 tiles for x2/3 (keyed_n_sat.py list). In this design, tiles sit on down sites, so a x2/3 slab needs 10 states per down site.
  10 > 6: ONE KEYED PIECE CANNOT CARRY ONE KARI TILE PER SITE. This holds with or without mirror copies; it is a count, not a search.
- Way out: spread each tile over a PAIR of sites. The pair is the down tile piece plus the up piece at its output quad Q0, which is the relay already joined
  to it in the 17-piece set. The pair must carry the tile (10) and the slab's row direction (3), which is 30 states:
    with mirror copies 6 x 6 = 36 >= 30: the count passes;
    without mirror copies 3 x 3 = 9 < 30, and even 3^3 = 27 < 30: it needs clusters of 4 or more sites.
- DECISION: route (a) continues with mirror copies allowed (6 placements per site) and tile+relay pairs. Next step (2): a SAT search for ONE key
  pattern on N (keys on the 10 faces, with positions, so mirror placements can be told apart) together with a decoding of pair placements to
  (Kari tile, row direction). Contact compatibility must imply Kari compatibility, and every Kari adjacency must be realised. Pilot first (<= 5 min, dicto-big-brother).

## Route (a), step 2 pre-check (11-06): pairs fail per piece
- Split a tile over a pair: the down piece shows the digit n and takes carry w; the up piece takes m = qn + w, shows s and gives carry e.
  Kari x2/3: the down piece needs 8 states and the up piece 8 (scripts/mult_scan.py); one piece offers <= 6. So PAIRS FAIL locally;
  step 1's 36 >= 30 count was too coarse (each piece must show its own faces).
- Other multiplier pairs, as (tiles, down states, up states):
    Culik-type x3 (6,4,6) / x1/2 (6,6,4) fits <= 6 everywhere but has the all-zero tile (rejected 11-05);
    x3/2 + x1/2 still needs 8; x2 [1,2] + x1/3 needs 9.
- So route (a) needs tiles spread over >= 3 sites (carry in bits, using the slab's second direction), or a fix for the Culik zero tile.
  Next: (i) whether a marker can forbid the all-zero periodic tiling in the Culik set (that set fits 6 per piece); (ii) a 3-site split for Kari.

## Route (a)(i) (11-06): repairing the Culik-type set (dicto-big-brother, culik_nozero.py, culik_rule.py; each FINAL in 6-22 s)
- Removing only the all-zero tile: 11 tiles; tori 2x2..6x6 are still SAT, because (n=0,s=0,w=e=1/2) gives an x=0 row. REJECTED.
- Removing both n=s=0 tiles: tori UNSAT, but the 16x16 square is UNSAT, so the set no longer tiles. REJECTED.
- KEY "no two side-by-side n=0 in x1/2 rows" (true rows have x >= 2/3, so two steps add >= 1): tori 2x2..6x6 all UNSAT; free squares
  8..64 all SAT. Proof idea: a vertical period gives densities; x1/2 rows have n-density >= 1/2 by the key, and x3 rows put s >= 1 into the row
  below; all densities are bounded away from 0 and Theorem 2's argument applies. WORKS as a Wang set (12 tiles + key).
- Cost (culik_rule_counts.py): the key's flag makes the x1/2 down piece need 8 states (> 6). Not yet one piece.
- Next: rescale the interval so that zero digits cannot arise at all (scale_scan.py).
- Rescaling (scale_scan.py, a = 1/4 ... 1, both families): ONLY Culik at a = 1/3 keeps every piece at <= 6 states, and it is the one with the
  zero tiles. Every zero-free scale needs 8-12 states per piece. So (i) ends at: Culik a = 1/3 + key, with the key's flag costing 8. Open: carry the flag
  through the vertical neighbour or a third site, which is (ii).
- (ii) flag carried by the UP pieces through their side contacts (culik_flag_on_up.py): down 6 / up 7 in x1/2 rows (x3: 4 / 6). ONE STATE SHORT of 6; next: merge two of the up states (e.g. drop z_prev where the check cannot fire).
- Split B (culik_split2.py): the DOWN piece holds the whole tile (6 states in x3 rows, 6 in x1/2 rows: fits); the UP piece shows s, passes
  carry e and the key flag. Up piece: 6 (x3), and 5 (x1/2) WITHOUT the flag, 7 with it. The flag alone costs the extra state: a rigid key
  cannot "accept either value" (a hole facing a flat face leaves a cavity, a bump facing a flat face overlaps), so every receiver needs one
  placement per value it accepts.
- So by count: one keyed piece fails by exactly the zero-key's flag. Without the zero-key, the Culik set fits 6 everywhere but tiles
  periodically. THREE keyed pieces pass the count (down piece; up piece for x3 slabs and up piece for x1/2 slabs, or the x1/2 up role split
  over two pieces), against 17 now.
- Ways round the flag for ONE piece: (1) a key at an EDGE where three or more pieces meet (Socolar–Taylor-type, second neighbours), so that a bump can
  go into either of two pieces and "accept either" becomes possible; (2) a scale or multiplier pair with no zero digits that still fits 6
  (scale_scan: none among the families tried).
- Next: SAT on real Narcissus geometry for a 3-piece key pattern (counts allow it), then try the edge key (1) to merge to one.
