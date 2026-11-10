# Is the truncated 600-cell a scutoid build? (10 Nov 2026; DICTO: "looking at the truncated 600 cell it could be a scutoid build by
appearance"; "lets move to the scutoid build test of truncated 600") - scripts/t600_scutoid.py, data-t600_scutoid.json, FINAL ok
Built as in the queen-stages atlas (corners at 1/3 along every 600-cell edge): 1440 corners, 720 cells (120 icosahedra, 600 truncated
tetrahedra), 3600 shared faces (2400 icosahedron-tt triangles, 1200 tt-tt hexagons). Sliced along the four main directions of #63 and a
generic one; the slice surface is tiled by the cells' cross-sections; neighbours = shared face crossing the hyperplane; compared below
and above every corner height.
RESULT: 0 pure scutoid swaps (two cells stop touching, two start, nothing else) in any direction. Generic direction (each of the 1440
corners passed once), neighbour changes among surviving cells, in mirror pairs: 1 lost / 3 gained and 3 / 1: 118 each; 2 / 0 and 0 / 2:
371 each; 1 / 0 and 0 / 1: 109 each; cells appearing / disappearing 714 each.
WHY: the classic swap needs FOUR cells at a point (a tetrahedral vertex figure split 2 | 2); at every corner of the truncated 600-cell SIX
cells meet (1 icosahedron + 5 truncated tetrahedra: DICTO's "groups of five"; vertex figure a pentagonal pyramid), so every change at a
corner involves the whole group: generalised scutoid moves (1 ↔ 3 etc.), never the 2 ↔ 2 swap.
Contrast: #61's walls are made of pure 2 ↔ 2 swaps (114 ↔ 114, 42 ↔ 42, 252 ↔ 252).
LEADS: the same test on the other Queen stages (rectified, bitruncated: vertex figures differ); is there a stage whose corners join exactly
four cells (then pure swaps)? The bitruncated 600-cell's vertex figure is a tetrahedron (4 cells: 2 truncated icosahedra + 2 truncated
tetrahedra) - the natural candidate for a TRUE 4D scutoid build.

## The bitruncated 600-cell IS a true 4D scutoid build (DICTO "yes test the bitruncated 600 cell"; t600_scutoid.py stages.py bitruncated)
Built as in the atlas (3/5 of the way from each edge's middle to its triangle's centre): 3600 corners, 720 cells (120 truncated
icosahedra, 600 truncated tetrahedra), 4320 shared faces (2400 TI-tt hexagons, 1200 tt-tt triangles, 720 TI-TI pentagons).
Every corner joins exactly FOUR cells (2 TI + 2 tt).
GENERIC direction (each corner passed once): ONLY three kinds of event: cells appear 716, cells disappear 716, PURE SCUTOID SWAPS
(two cells stop touching, two start, nothing else) 2166 - nothing else at all (716 + 716 + 2166 = 3598 = all corners but the two ends).
Main directions: the swaps come in symmetric balanced batches (vertex-first 30 ↔ 30, 60 ↔ 60; edge-first 20 ↔ 20 …; face-first 18 ↔ 18 …;
cell-first 24 ↔ 24, 12 ↔ 12, 6 ↔ 6) beside cells appearing / leaving.
So, sliced along any generic direction, the bitruncated 600-cell's 720 cells cross the slice as a 2D tiling that changes ONLY by cells
being born / dying and pure scutoid moves: each cell is a 4D scutoid-like column. The truncated 600-cell (six cells per corner, DICTO's
groups of five) gives group moves and no swap; one stage on, at the midpoint between the Queens (DICTO's intermediate body, the truncated
icosahedron as cell), every change is a clean scutoid move.
LEADS: the other stages (rectified 600-cell, rectified / truncated 120-cell); a picture (one TI cell's cross-sections through a slice
sweep, with its swaps marked); compare the swap batches with #61's walls (114, 42, 252).
