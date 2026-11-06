# Footballs and scutoids (DICTO 11-06: "could make an interesting spacefill with footballs and scutoids"; "A please first, might be a
scutoid paper if we managed a few novel moves"; "go ahead with the football search")
Reading A: footballs (truncated icosahedra, edge 1) joined face to face by bridge pieces, every link a pentagon facing a hexagon on one axis.

**Conclusion so far:** a layer exists: every ball on two link lines (its 5-fold axis and a 3-fold axis at 79.19 deg), checkerboard of two
orientations, every link pentagon-to-hexagon. Step 2b (7 Nov): the space is cut into one cell per ball (nearest body, each bridge split between its balls) - a space-fill of
football cells - and every cell makes the SCUTOID MOVE twice (below and above its layer's middle plane). Status: step 3 (7 Nov): closest stacking found continuously with bridges included and solved at 60 digits (h = 3.43700237509909..., shift
(1/2, 0.56107350871...)); the scutoid corners located from exact distances at +-0.34113 of the middle plane, all four one orbit.

- football.py: centre to pentagon 2.327438, to hexagon 2.267284 (edge 1). Axis angles (as lines): 5-5 only 63.43; 3-3 only 41.81, 70.53;
  5-3 only 37.38, 79.19.
- OBSERVATION 1 (two kinds of ball): if every ball links through pentagons only or hexagons only, and each kind is one orientation, all link
  directions lie on one line (the 5-5 and 3-3 angle sets share no value): chains only.
- OBSERVATION 2 (lines): a link line continues through a ball as the same face kind (5-fold axis: pentagons both ends; 3-fold: hexagons), so
  balls along a line alternate pentagon role / hexagon role. With three line families through every ball, the roles force a 63.43 deg angle
  between a 3-fold axis and another axis, which does not occur: no 3D lattice of this kind. Two families work: the grid layer.
- grid_layer.py (gap 0.6, link length 5.1947): 50 links all pentagon-hexagon, coaxial; 0 ball overlaps; bridges (hull of the two faces) meet
  balls only in their faces. The 37.38 deg grid makes diagonal neighbours overlap; 79.19 deg is the one.
- Figure football-layer.png (also in papers-to-read).
- NEXT: stack layers and cut the remaining space; find where pieces change neighbours top to bottom (the scutoids); the bridge itself is a
  pentagon-hexagon prismatoid (no middle vertex) unless its sides meet different pieces above and below.

## Step 2a: stacking the layers (scripts/stack_layers.py -> data-stack.txt; overnight 6-7 Nov)
Layer periods 2D e1 (10.389) and D(e1 + e2) (8.006). The closest stacking found (shift grid 9 x 9 of the cell, separating-plane overlap
test): layer spacing h = 3.6224 at shift (0, 0.444) of the cell - less than a ball's diameter, so each layer's balls sit in the hollows of
the one below. Balls fill 0.5758 of space; bridges + gap 0.4242. Next (2b): cut the gap into pieces (power/Voronoi cells of the balls and
bridges, or wave basins) and find the pieces whose neighbours change from bottom to top: the scutoids. Coarse shift grid: refine before any claim.

## Step 2b: cells and the scutoid move (scripts/cut_cells.py, cell_track.py, render_slices.py; data-track.txt; figure football-slices.png)
Every point of space goes to the nearest body (ball + half of each attached bridge; Euclidean distance to dense surface samples, 0.056
apart). These cells fill space, one per ball. Sliced parallel to the layers, each cell (X and Y alike) reads, bottom to top
(w = height in layer periods, 0 = its own layer's middle plane):
  4 -> 6 -> 8 neighbours up to w = -0.12; at w = -0.12 THE SCUTOID MOVE: the two diagonal neighbours of the same layer (offsets +-(1,-1))
  meet and push out a cell of the layer below that is still present in the slice (a neighbour hand-over among cells present on both
  sides of the event, i.e. a four-cell vertex inside the cell's side wall) -> 9; at w = -0.06 the cells of the layer below end -> 6:
  in the middle band (w -0.06 .. +0.08) only this layer's cells are there and they tile the plane in HEXAGONS; above it the same story
  mirrored with the layer above (move at w = +0.14).
Same events at voxel 0.25 and 0.08 (heights to +-0.03 of a period). Numerical, not exact. The ball's cell is therefore not a prism: in
the slab from w = -0.3 to 0 its bottom is an octagon, its top a hexagon, with a vertex in between - the scutoid signature (Gomez-Galvez
et al., Nature Communications 9 (2018) 2960) - though here the other layer's cells end inside the slab rather than spanning it.
NEXT (step 3): exact positions of the move (planes of the nearest-body faces), the cells as solids (volume, faces), and whether a gap
other than 0.6 or a different stacking shift turns the 9-neighbour band into a clean prism - or makes the move the whole story.

## Step 3 (exact geometry; DICTO 11-07 "move to step 3 exact geometry")
(a) CLOSEST STACKING, bridges included (scripts/stack_exact.py -> data-stack-exact.txt; stack_solve.py -> data-stack-solve.txt).
The step 2a stacking (coarse 9 x 9 grid, balls only) is free of overlaps with bridges too, but NOT the closest. Searching every shift
continuously (Minkowski differences of all 6 bodies of a cell: 2 balls, 4 bridges; least free height per shift; Nelder-Mead from the
12 best of a 40 x 40 grid) gives
   h = 3.437002375099093176690586445664303449286 (layer spacing), shift a = 1/2 exactly, b = 0.5610735087101498959736905116890006
   (and its mirror twin 1 - b), held by four ball-ball contacts on three distinct planes (no bridge touches).
   Balls fill 0.606881 of space (was 0.5758), bridges 0.029405, gap pieces 0.363714.
The 60-digit values solve the three contact planes built from exact football corners (coordinates in Q(sqrt 5); gap g = 3/5); the float
search agrees to 4e-8 (its normals are rounded to 1e-7). No integer polynomial of degree <= 16 with coefficients < 1e7 fits h or b
(the numbers mix sqrt 5, sqrt 3 and the unit-axis radicals); a closed form in radicals is still open (sympy run timed out).
(b) CELLS AT THE CLOSEST STACKING (cell_track.py with STACK=tight -> data-track-tight.txt): the same story as in step 2b - 4, 6, 8, 9
neighbours, the move, then hexagons - but the pure-hexagon band shrinks to (almost) the middle plane itself.
(c) THE SCUTOID CORNERS, from exact distances (move_refine.py: slices every 0.002 of a period, all pair contacts tracked ->
data-move-events-*.json; corner_solve.py: a gained and a lost pair with no common cell -> solve "distance equal to all four",
accepted only if spread < 1e-9 AND no other cell nearer -> data-corners-tight-*.json):
   four true corners round the reference cell, at w = -0.0992527 and +0.0992527 of a period, i.e. 0.341132 below and above the middle
   plane, common distance to the four bodies 1.0258288 (next cell 1.365452 away):
     below: X(0,0,0)+X(-1,1,0) meet, X(0,1,-1)|Y(-1,1,0) part;   Y(-1,0,0)+Y(0,-1,0) meet, X(0,0,0)|Y(0,0,-1) part;
     above: the same mirrored with the layer above.
   All four have one common distance and height: ONE orbit of corners under the crystal's symmetry. The voxel heights (-0.094/+0.118)
   were off by resolution; the move is symmetric about the middle plane. At each corner the nearest features are three faces and one
   edge, so its exact position is the meeting point of two bisector planes and one parabolic sheet (a quadratic: closed form next).
Guards (DICTO's only-happens-once law): every script here prints FINAL ok only after a check of its own result; runs go through
tools/runjob.py. Two corner runs that did not converge were caught as FAIL, not OK.
NEXT: closed forms (corner: quadratic from the edge; stacking: radicals); the cells as solids (volume and faces) at the closest stacking;
the figure redrawn at the closest stacking with the four corners marked.
