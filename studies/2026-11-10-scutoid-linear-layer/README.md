# Scutoid linear layer L (DICTO 6 Nov 2026, opened 10 Nov)
DICTO 6 Nov: "adapt it to a linear transition between octet and hexagonal and pentagonal prisms"; "a spherical skin version and a
linear layer version, both filling space"; S and L separate, connected projects (football search A the third, linked). 10 Nov:
"what happened to scutoids … disappeared from my desired projects?" → never started, re-listed; "yes open L".

**Construction (sketch, 10 Nov).** Bottom of a layer: hexagonal prisms. In every hexagon exactly one edge shrinks to a point going up
(brick pairing of neighbouring cells; the shrinking edges never touch), so at the middle level every cell is a PENTAGON (a
pentagonal-prism level) with four cells meeting at each shrunk point. Edges keep their three directions, so every side face of a
cell stays flat (trapezoids, and one triangle where the edge vanishes). Realised with exact closure (residual 3e-15), every kept edge
positive (0.19–0.77 of the hexagon edge). Figure: l-levels-sketch.png (scripts/levels.py).
**Found by hand (10 Nov):** above the middle, the points reopen across and cells get new neighbours; with the brick pairing half the
cells in a row end with 7 sides and half with 5 (each gains two or none), the classical scutoid mix, not hexagons everywhere.
All-hexagon tops need a pairing in which every cell sits at the tip of exactly one shrinking edge: open.
**Next:** (1) DICTO's read of the sketch; (2) search pairings for the all-hexagon top; (3) the octet start (triangles) in place of
hexagons; (4) 3D cells (prism + transition + prism), their volumes and the stacked space-fill.

## Step 3 (10 Nov, DICTO "scutoids?!"): free edge directions (scripts/free_dirs.py)
Least squares on a periodic 4 x 4 patch, bottom and middle corners free, conditions: paired edges collapse, every other edge parallel
between the levels (flat trapezoid side faces), convex cells, edge floors. Every start stalls at the same violation 1.25 = the floor
penalty of a BOTTOM edge forced towards zero: to keep all side faces flat the solver must collapse an edge that is not paired.
Same obstruction as the three-direction LP. **Conjecture: with hexagons again at the top (double-row pairing) the side faces cannot all
be flat, for any edge directions.** (Search evidence, not a proof; a proof would go through the cycle space of the parallel conditions.)
**The choice for DICTO:** (a) the brick pairing: every side face flat (exact polyhedral cells), top a mix of 5- and 7-sided cells (the
classic scutoid mix); (b) the double-row pairing: hexagons everywhere at the top, side faces bent (as in living scutoids, whose faces
are curved). Either gives a space-filling layer stack.

## Step 4: the geometric scutoid solid (10 Nov, DICTO "did we get a scutoid solid … like a geometric one"; scripts/scutoid_solid.py)
Brick layer (version a), all side faces flat at both stages: middle by LP (kept edges parallel to the hexagon edges, shortest 0.30),
top by LP (each collapsed point reopened across into a horizontal edge, every other edge parallel to its middle edge, shortest 0.25),
each level kept as close as possible to the one below. Top side counts in the patch: 12 pentagons, 12 heptagons.
A cell that gains nothing: bottom hexagon (z = 0) → middle pentagon (z = 1, one edge shrunk to a point: the Y) → top pentagon (z = 2):
a GEOMETRIC SCUTOID with 13 faces, every face flat (8.6e-16). Data: data-scutoid-solid.json; render in papers-to-read.
Next (DICTO: "as a block linear group and as a near sphere"; "as a core a football"): (1) the block: the whole brick layer as a group
of scutoids; (2) the near sphere: a skin of scutoids round a truncated icosahedron core.

## Step 5: the block (DICTO "as a block linear group")
Top polygons are now the faces of the actual top tiling, traced geometrically (the earlier bookkeeping put 14 edges that are not in the
top tiling; fixed). 16 interior cells: bottom hexagon → middle pentagon for all; top 5 (8 cells), 6 (4), 8 (4); average 6 as it must be.
Every face of every cell flat (7.4e-15). The top polygons tile with no overlap (3.6e-15) and no holes; 42 of 48 convex (the 8-gons are not).
Data data-scutoid-block.json; render papers-to-read/scutoid-block.png. Next: the near sphere (skin round a truncated icosahedron core).

## Step 6: the near sphere (DICTO "as a near sphere", core a truncated icosahedron; scripts/scutoid_sphere.py)
Inner truncated icosahedron (circumradius 1) → middle icosidodecahedron (1.18): every hexagon-hexagon edge shrinks to a point (the Y) →
outer truncated dodecahedron (1.42): each point reopens ACROSS, the new edge now between the two pentagon cells (a true T1).
32 cells: 12 pentagon scutoids 5 → 5 → 10 (pentagon below, decagon above) and 20 hexagon scutoids 6 → 3 → 3.
Every face flat (4e-13; by mirror symmetry each inner edge is parallel to its middle edge, so flat for ANY radii); every cell volume
positive (0.111 .. 0.287); the 32 volumes add to V(TD) − V(TI) = 5.6660707968 exactly (shell filled once). Render papers-to-read/scutoid-near-sphere.png.
Block question ("how many to fill space"): the LP block has 16 different cells (not forced to repeat); its pattern repeats in tops
2 pentagons : 1 hexagon : 1 octagon, so the periodic version needs 4 cells (+ mirror layer to return to hexagons). Next: periodic block.
