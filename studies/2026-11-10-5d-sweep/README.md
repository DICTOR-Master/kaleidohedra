# The 5D test (10 Nov 2026; DICTO: "can we use it to predict other unperceived elements of the higher dimensions"; "yes queue the 5D test")
scripts/sweep5d.py (FINAL ok). For a simple d-polytope and a generic height, a corner with i edges down changes the slice's facet tiling as
follows (the corner argument: a pair of facets touches below / above the corner iff their common ridge has a downward / upward edge there):
d = 4: i = 1 birth, i = 2 a SWAP (one pair lets go, one meets), i = 3 death. d = 5: i = 1 birth, i = 2 ONE CONTACT GAINED, i = 3 ONE CONTACT
LOST, i = 4 death. Counts h1 .. h_{d-1}, every generic direction. PREDICTED before computing, then counted in three random directions:
- 4D permutohedron (control): 120 corners, 30 facets: 26 births, 66 swaps, 26 deaths = h (1, 26, 66, 26, 1). MATCH.
- 5-cube: 32 corners, 10 facets: 5 births, 10 contacts gained, 10 lost, 5 deaths = h (1, 5, 10, 10, 5, 1). MATCH.
- 5D permutohedron (orderings of 1..6; DICTO's "shape of the permutahedron?!"): 720 corners, 62 facets: 57 births, 302 gained, 302 lost,
  57 deaths = the Eulerian numbers (1, 57, 302, 302, 57, 1). MATCH.
One dimension up the 4D scutoid swap splits into two separate moves (contact gained / contact lost), each counted by an h-number.
FLATLAND RECONSTRUCTION (4D): a 3D observer counting a simple 4-polytope's sweep recovers cells = births + 4 and corners = 2 + 2·births + swaps
(bitruncated 600-cell: 720 and 3600 from 716 and 2166).

## Random irregular simple 4-polytopes (DICTO: "why did we first understand this only in terms of beautiful regular geometry?";
"test a random irregular simple 4D polytope"; scripts/random4d.py, FINAL ok)
Random points near the 3-sphere (radii 0.8-1.2) -> hull -> its polar: a simple 4-polytope with no symmetry; cells taken from the construction
(one per original point). Predicted from face counts alone (h1 = cells - 4, h2 = corners - 2 - 2 h1), counted in three random directions:
#1 99 corners, 24 cells: 20 / 57 / 20 MATCH; #2 169, 36: 32 / 103 / 32 MATCH; #3 244, 54: 50 / 142 / 50 MATCH. The law needs no regularity.
(Fault fixed on the way: the ridge test used a float rank check that rejected thin ridges, so a few swaps were seen as halves; in a convex
polytope two facets sharing >= d - 1 corners share a ridge: rank check removed; the 5D and permutohedron controls still match.)
