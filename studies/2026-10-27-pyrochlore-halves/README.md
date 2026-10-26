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

## Exact weight walk (`scripts/pyro_walk.py`: #57's census engine, unchanged, exact rational arithmetic; `pyro-walk-exact.json`)
- **3C:** stops −3/8 (atom pieces vanish), **−1/4** (tetrahedra + truncated tetrahedra: the quarter cubic honeycomb), **+1/4** (roles
  swapped: atoms truncated tetrahedra, holes tetrahedra), +3/8 (hole pieces vanish).
- **2H:** stops −11/36, −1/4, −3/20, 0, 1/8, 1/6, 1/4; at −1/4 the diamond atoms over h layers are regular tetrahedra but the balls are
  10-cornered pieces.

## Pictures
`patches-sheet.png`: the network's pieces at −1/4 in 3C (gold), 2H (platinum) and 4H (both), voids left out.

## Exact proof (`scripts/pyro_exact.py`, `scripts/pyro_stretch.py`; logs in `exact/`)
#57's method with #57's census engine unchanged, over the 16 windows (h/c of the four layers round a gap; every close-packed stacking
looks like one of them near any gap) and the stretches of the common walk −11/36 < λ < 1/4 (stops −11/36, −1/4, −3/20, 0, 1/8, 1/6, 1/4):
- **Exact at sample weights:** every piece congruent to its pure piece (exact squared corner distances), 12 weights spanning every
  stretch: **768 PASS, 0 FAIL**.
- **Stretch-wide:** on every stretch one symmetry of the layer carries the corner functions (affine in λ) of each whole piece (ball,
  diamond atom) onto the pure piece's, and of each half (octahedral, Y hole: corners above/on/below the gap's mid-plane and the section
  points as exact rational functions of λ) onto the pure half's: **384 ok, 0 bad** (16 windows × 6 stretches × 4 sites).
- **Locality:** every corner of every central piece within squared distance **11/32** of its site. A site whose letter the window does not
  fix lies at least 2¼ layer spacings away in height (h² = 27/8) with weights differing by at most 11/36, so its bisector is at squared
  distance ≥ ((27/8 − 11/36)/(2h))² ≈ 0.698 > 11/32: it cannot meet the piece; by convexity the piece is the window's.
**Theorem (proved):** in every close-packed stacking, for −11/36 ≤ λ ≤ 1/4, every piece of the weighted division is borrowed from the
pure stackings: balls by their own layer, diamond atoms by their nearest layer, octahedral and Y holes as two halves by the layers on
their two sides.

## Name (placeholder)
**DICTO Janus c/h Pyrochlore** (title by DICTO; study name Pyrochlore Halves): the weighted division of a diamond-type stacking (balls, diamond atoms and #57's two empty holes).

## Prior art (library of 302 references, then web; 2026-10-27)
**Known, credited:** the pyrochlore lattice as the bond-midpoint (medial) lattice of diamond, and as alternating kagome and triangular
layers along [111] (standard in frustrated-magnetism papers); the cubic and hexagonal stackings of diamond-type crystals
(diamond/lonsdaleite, zincblende/wurtzite); the tetrahedral–truncated-tetrahedral (quarter cubic) honeycomb (classical); the rule of
halves (#57, DICTO).
**Not found in the sources searched:** the rule of halves for pyrochlore stackings, or their weighted division.

## Conclusion
The rule of halves of #57 holds on every pyrochlore polytype tested: each piece is borrowed, whole or in half, from the pure cubic or
pure hexagonal stacking. **Status: proved exactly (768 + 384 checks, locality bound); paper #60 drafted for DICTO.**
