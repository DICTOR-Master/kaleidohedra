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
