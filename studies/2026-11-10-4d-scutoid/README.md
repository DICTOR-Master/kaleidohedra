# A 4D scutoid (10 Nov 2026; DICTO: "a 4th dimensional scutoid?!", "4D build?!") - scripts/scutoid4d.py, data-scutoid4d.log
Each hole's power cell stacked over the slider λ is the convex 4D polytope {(x, λ): n·x <= b0 + b1 λ, λa <= λ <= λb} (linear in x and
λ); its 3D slices are the power cells. At s = 1/5, λ from -19/120 to -1/40 (across #61's wall -5s/8 = -1/8), six words:
25 holes have 4D cells with facets that END or BEGIN exactly at λ = -1/8: the octahedral cells' facets towards the octahedral holes two
layers away end there; the tetrahedral cells' new facets towards tetrahedral holes begin there. Example: word ACABC, hole 3 (octahedral):
48 corners, 26 facets; three facets (towards octahedral holes two layers up) run from λ = -0.1583 to -0.1250 and stop. Slices: below the
wall the cell touches octahedral holes in layers ±1 and ±2; at and above it only ±1. A flat-faced 4D cell whose 3D slices change
neighbours: a 4D scutoid. The first try (word AC, hole 0) changed nothing (an octahedron × interval) - that hole is not in the flip.
NEXT: a render (the three slices side by side); the truncated 600-cell slice walk (DICTO: "it could be a scutoid build").
Render: scutoid4d-strip.png (scripts/render4d.py): slices at λ = -0.155, -0.140, -0.125 (wall), -0.110, -0.060: 17, 17, 14, 14, 14 faces; the 3 gold faces (towards octahedral holes two layers away) shrink and vanish exactly at the wall.

## The 3D build (DICTO "lets do a 3D build, it's a lot easier for humans to understand") - scripts/build3d.py, render_build3d.py
A vertical plane through octahedral hole 3 of ACABC (s = 1/5): in the plane each hole's cell is a polygon (2D power diagram, weight minus
squared distance to the plane); stacked over λ in [-0.155, -0.095] each hole becomes a flat-faced 3D column (linear in u, v, λ): 42
columns (24 octahedral, 18 tetrahedral). The centre (gold) column keeps its six neighbours and GAINS two tetrahedral neighbours exactly at
the wall λ = -1/8: in the plan views two thin tetrahedral cells push in at its upper corners from the wall on (at the wall: a point where
four cells meet, red); in 3D the two green columns start as wedges at the wall. Picture build3d.png (papers-to-read/scutoid-4d-as-3d-build.png).
Interactive page (piece 1 of DICTO's 'all in 3D'): the-4d-scutoid.html, published privately as 'The 4D Scutoid' (https://claude.ai/artifact/1pNG17r8kunHnnkXRaZKWP): turnable columns, λ slider, plan of the cut with the gold cell's neighbour count (6 below the wall, 8 above).
