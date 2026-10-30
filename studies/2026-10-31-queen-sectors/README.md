# Queen sectors (DICTO, 31 October 2026)

DICTO's idea: break the Red Queen into pieces along the axes of Aristotle's five-sided pyramids (her core dodecahedron = 12 pentagonal pyramids), and the White Queen along her core's 20 (the Cleo-Icos). Name (placeholder): **Twelve sectors** / **Twenty sectors**.

Sector = the cone, from the seed axis v, over one face of the core (12 pentagons of the Red Queen's core dodecahedron; 20 triangles of the White Queen's core icosahedron). A cell's place is its centre's direction across v (component orthogonal to v); the cones are the Voronoi regions of the core's face normals. scripts/sectors.py (float, 1e-9; 600-cell built from its 120 unit corners).

| | cells | whole in one sector | on a sector boundary | on the axis |
|---|---|---|---|---|
| White Queen | 600 | 15 per sector (300) | 300, each between exactly 2 sectors (heights ±0.6545, ±0.5295, ±0.3273 along v, unit radius) | 0 |
| Red Queen | 120 | 4 per sector (48) | 70, between 2 or 3 sectors (heights 0.5, 0, −0.5) | 2 (core and the opposite cell, split by all 12) |

**Decision:** whole cells cannot be dealt out (half of the White Queen and most of the Red Queen sit on boundaries), so the view CUTS the cells along the sector planes. Every sector boundary is a plane through the seed axis; in any picture projected along v (Shells, RCP, DICTO RCP) it is a plane through the centre, so each drawn cell is cut by those planes into convex wedges, exactly. The core falls apart into Aristotle's 12 pentagonal pyramids (Red) / the 20 Cleo-Icos (White); the slider pulls the sectors apart along their own axes.

Conclusion: sectors by whole cells are impossible; sectors by cutting are exact and symmetric. Status: geometry decided; app view queued after the DICTO RCP change (same file).
