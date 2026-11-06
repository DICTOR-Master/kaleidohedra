# Footballs and scutoids (DICTO 11-06: "could make an interesting spacefill with footballs and scutoids"; "A please first, might be a
scutoid paper if we managed a few novel moves"; "go ahead with the football search")
Reading A: footballs (truncated icosahedra, edge 1) joined face to face by bridge pieces, every link a pentagon facing a hexagon on one axis.

**Conclusion so far:** a layer exists: every ball on two link lines (its 5-fold axis and a 3-fold axis at 79.19 deg), checkerboard of two
orientations, every link pentagon-to-hexagon. Step 2b (7 Nov): the space is cut into one cell per ball (nearest body, each bridge split between its balls) - a space-fill of
football cells - and every cell makes the SCUTOID MOVE twice (below and above its layer's middle plane). Status: step 2 of 3 (numerical).

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
