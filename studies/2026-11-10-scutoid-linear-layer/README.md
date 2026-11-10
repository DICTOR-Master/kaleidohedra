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
