# The rule of halves on pyrochlore polytypes (DICTO, 2026-10-27) — stage 1 (float)

DICTO's idea: "close packing halves rule pyrochlore network" — #57's rule of halves on the pyrochlore network, its layers (kagome
and triangular, seen down a three-fold axis) stacked in any order.

## Construction (`scripts/pyro.py`)
For any close-packed stacking word, the diamond-type crystal (as SiC) is the balls plus #57's tetrahedral hole "over X at 3/4" above
each ball. The **pyrochlore network** is the midpoints of its bonds: each atom's four bond midpoints a regular tetrahedron (edge 1/2,
ball spacing 1), neighbours sharing a corner. Checked for 3C, 2H, 4H, 6H: every corner in exactly two tetrahedra, every edge 1/2
(`pyro-output.txt`). 3C is the cubic pyrochlore; 2H a hexagonal one.

## The weighted division (`scripts/cells.py`)
Sites per gap k: S (ball, layer k), C (hole over X at 3/4, a diamond atom), O (octahedral hole), Y (hole over Y at 1/4); the two
empty holes per gap are exactly the network's voids. Power cells with w_S = w_C = a, w_O = w_Y = 0. At **a = −1/4** the 3C division is
the pyrochlore tetrahedra (S, C) and truncated tetrahedra (O, Y; 23√2/96 each): the tetrahedral–truncated-tetrahedral honeycomb.
In h layers the same weight gives other pieces (S a 10-cornered piece; C small): the regular tetrahedra are cells only on c layers.

## The rule of halves (`scripts/halves.py`, `halves-output.txt`)
O and Y cut at the gap's mid-height into a bottom half (layer k) and a top half (layer k+1); S whole (its layer); C whole (nearest
layer k+1). Every piece of 4H, 6H, 9R and 15R equals the same piece of the pure stacking of its layer (3C if c, 2H if h):
**204 pieces at each of a = −1/4, −1/5, −1/10, 0, 1/10, none off** (float, 7 decimals).

## Name (placeholder)
**Pyrochlore Halves**: the weighted division of a diamond-type stacking (balls, diamond atoms and #57's two empty holes).

## Prior art (library of 302 references, then web; 2026-10-27)
**Known, credited:** the pyrochlore lattice as the bond-midpoint (medial) lattice of diamond, and as alternating kagome and triangular
layers along [111] (standard in frustrated-magnetism papers); the cubic and hexagonal stackings of diamond-type crystals
(diamond/lonsdaleite, zincblende/wurtzite); the tetrahedral–truncated-tetrahedral (quarter cubic) honeycomb (classical); the rule of
halves (#57, DICTO).
**Not found in the sources searched:** the rule of halves for pyrochlore stackings, or their weighted division.

## Conclusion
The rule of halves of #57 holds on every pyrochlore polytype tested: each piece is borrowed, whole or in half, from the pure cubic or
pure hexagonal stacking. **Status: stage 1 done (float); next: exact proof, then pictures; prior art checked.**
