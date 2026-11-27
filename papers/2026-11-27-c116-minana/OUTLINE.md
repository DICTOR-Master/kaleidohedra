# C116 to Minana #377 (outline, 27 Nov 2026)

DICTO · paper · with Claude (Anthropic). Home decided by DICTO 27 Nov: its own paper (not the Scutoid-Frusta paper).
Gold standard #43 v3; Winston style; first paragraph = known, new, question answered. Data: study 2026-11-24-aequi-vacuus-scutoids.


## CORRECTION 27 Nov (DICTO: "I have never wanted or asked for the core to be the same as the outer... it is a transformation!!!")
DICTO's Hollow-straw fixes BOTH ends: C116 in its own shape inside, Minana #377 outside; the straws are swept as each C116 face plane
turns and moves into its die face plane, all together (a transformation). The flat-walled layer (hollow_straw.py, hollow_straw_exact.py)
moved the core parallel to the die: it is MY variant, not his method, and its certificate is not a certificate of his method.
Next: build his method as a transformation (fixed ends, moving planes), check nesting and the swaps; then the theorems are rewritten.

## Working title
From a Fullerene to a Fair Die: C116 Turned into Minana #377 by One Layer of Scutoid-Frusta

## First paragraph (known, new, question)
Known: fair dice (Aequi, #105/#118 catalogue); fullerenes and their enumeration (fullgen, Brinkmann and Dress); scutoids in
biology (Gómez-Gálvez et al. 2018); Scutoid-Frusta (DICTO, #118 and the Scutoid-Frusta paper). Question: can a fullerene core
be wrapped in one layer of pieces whose outside is a fair die, face to face, and how few side changes does it take?
New: the unique C116 fullerene with symmetry T_h becomes Minana #377 in one layer (floating resin: the core keeps C116's own shape);
with DICTO's Hollow-straw method every piece is convex with flat walls, but the core then keeps only C116's face pattern: its faces are
pressed parallel to the die's, so it no longer looks like C116 (DICTO 27 Nov: never display what is not true; say this every time).

## Arc
- Pledge. A fullerene core and a fair die with 60 faces each, the same orbit sizes under T_h (12+12+12+24). Wrap one in the other,
  one piece per face; where neighbours differ a piece must change its side count (a Y corner, a swap).
- Turn. The obvious match (pentagons to squares) needs 90 swaps in 3 layers. Scoring every orbit assignment gives 30 swaps in one
  layer, the least among symmetric pairings. Letting the core float (DICTO's floating resin) gives 18 swaps, one layer.
- Prestige. DICTO's Hollow-straw (straws pumped up between paired faces until they meet) makes every wall flat: 60 convex
  Scutoid-Frusta, the core's faces parallel to the die's. Its core has C116's face pattern, NOT C116's shape (pressed into the die's
  planes); every figure and sentence must say so. Open: an exact certificate for the floating-resin layer, whose core is C116 itself.

## Sections
1. Introduction: promise (Theorem 1 in one sentence), vision figure (Hollow-straw layer pulled apart), contributions.
2. Background: Minana #377 (catalogue no. 377, T_h, 12 squares, 12 heptagons, 36 hexagons); C116 T_h unique among 1,207,119
   isomers (fullgen); face patterns as triangulations; swaps = dual edge flips; neighbour pairs kept; bound swaps >= 174 - kept.
3. Theorem 2 (symmetric): over all 6 orbit assignments x 1536 equivariant pairings, at most 144 of 174 pairs kept; the best needs
   exactly 30 swaps, non-touching, ONE floor; one valid layer, 30 Y corners. Near miss: pentagons -> squares, 108 kept, 90 swaps, 3 layers.
4. Floating resin (DICTO): method, 4000 starts; 156 kept, 18 swaps, one floor, symmetry S6. Bound: no pairing keeps more than 165
   (quadratic assignment, Koopmans-Beckmann; solver bound, to be certified).
5. Theorem 1 (Hollow-straw, DICTO): pressures f_k = mu_k (distance to Minana plane k); straws = cells of the weighted distance
   diagram; an LP gives the offsets; exact rational offsets: 60 convex flat-walled pieces, 18 Y corners. Fence: with the symmetric
   pairing no parallel-faced core exists (LP margin 0); non-parallel cores open.
6. The method for other Aequi (five steps).
7. Contributions; open questions (156 vs 165; symmetric convex layer; next die/core pairs).
Sources checked; data and reproducibility; references.

## Figures
1. Lead figure: floating-resin layer in the Aequi colours (RENDER-c116-minana-aequi.png): C116 core in its own shape, pulled apart,
   assembled. 2. Hollow-straw layer, captioned 'core with C116's face pattern, pressed parallel to the die's faces'.
2. The four routes side by side: 90 / 30 / 18 swaps (floating-resin amber layer, folded walls, beside Hollow-straw).
3. Face-pattern diagram: the 18 swaps marked on C116's pattern.

## Before drafting: decisions (mine; say no by number)
1. Title as above.
2. Theorem 1 = Hollow-straw convex layer; Theorem 2 = symmetric optimum (30 swaps). Floating resin a Proposition (best found).
3. EXACT first (rule: exact before claimed): redo the Hollow-straw piece checks in exact rationals (now floats, volume diff 1e-15)
   and certify the 165 bound (or state it as a solver bound only) before the draft reaches you.
4. Prior art (corrected 27 Nov): the weighted straight skeleton (Aichholzer et al. 1995; Eppstein-Erickson 1999; Aurenhammer 2008;
   Barequet et al. 2008; Aurenhammer-Walzl 2016) describes ONLY my flat-walled VARIANT (faces moved parallel, core pressed into the die's
   planes). It is NOT DICTO's Hollow-straw: his fixes both ends and each C116 face turns and moves into its die face (a transformation),
   which is not a straight skeleton. The skeleton credit goes nowhere near his method; it appears only if the variant is reported, as mine.
   Prior art for HIS method: to search once it is built (what it actually is decides what to search).
5. Names: Hollow-straw and floating resin are DICTO's, first use explained; Scutoid-Frusta hyphenated; "Scutoid-bubble Frusta"
   not used (Occam, as decided).
