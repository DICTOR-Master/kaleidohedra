# Ogdoecontahedron pyrochlore networks (DICTO, 2026-10-16)

DICTO's idea: the Ogdoecontahedron (OCD) might form pyrochlore attachment networks, growing or interacting around its faces with rhombic tilings.

## Step 1: the hexagon-joined network (exact in ℚ(√5), `scripts/network.py` → `data/network.txt`)

- **Joins.** Copies join face to face on hexagons. The OCD is centrally symmetric, so a copy shifted by t = 2dn/|n|² puts its opposite hexagon exactly on the shared one; this is checked exactly for all four bonds. No rotation is needed.
- **Network.** Joining through one tetrahedral set of four hexagons (pairwise cos −1/3) gives a **diamond network**. The bond vectors satisfy |t|² = 8/9 + 8√5/27.
- **No collisions.** The exact test: copies overlap iff half their offset lies inside the OCD, since K − K = 2K for a centrally symmetric K. Over 60 sites (1,770 pairs) no copies overlap. The only contacts are the 82 full-hexagon joints.
- **Pyrochlore joints.** The four joint hexagons around every site have centres at the corners of an exact regular tetrahedron (edge² 16/27 + 16√5/81). The joints sit at the diamond bond midpoints, which form the pyrochlore lattice of corner-sharing tetrahedra.
- **Packing.** One network fills (9225 − 3915√5)/1216 = 38.72% of space.

## Step 2a: the gaps hold a second network

A second copy of the network, shifted by 2t₀ (the diamond's empty sites), fits with no overlap. It touches the first network only on hexagons (69 more full-hexagon contacts in the test). Together the two networks fill **(9225 − 3915√5)/608 = 77.43%** of space, more than the densest packing of equal spheres (74.05%). The two networks are one **body-centred cubic lattice packing**: every copy is in the same orientation, and each touches 8 neighbours through 8 of its 20 hexagons, the four tetrahedral ones plus their opposites, which point to the corners of a cube. The other 12 hexagons and all 60 kites face the remaining **22.57%** of space.

Renders (`scripts/network_render.py`, `render_network.html`, `shoot_network.mjs`): `renders/ocdnet-*.png`, orthographic along a cube axis (a two-fold axis of the OCD). They show one network, the double network (first network warm, second cool), and sheet `ocdnet-sheet.png`. The "cut" views did not slice through; fix that when rendering the gaps.

## Step 3: the gaps filled (exact, `scripts/gaps.py` → `data/gaps.txt`)

In the bcc packing each copy has a Voronoi cell V: a truncated octahedron with 24 corners and volume 512/729 + 256√5/729. The OCD lies inside V and touches V's 8 hexagons, which are the joints. Each copy's share of the gap is therefore **V − OCD = 18728/13851 − 6296√5/13851 = 0.335695 (22.57% of space)**.

Cones from the centre over the OCD's 72 free faces (12 hexagons, 60 kites) fill it with **72 convex pieces of 3 kinds**, and the pieces sum to the gap exactly (remainder 0):

| Pieces | On | Shape | Volume |
|---|---|---|---|
| 48 | kites | wedge, 6 corners: 2 triangles, 3 quadrilaterals | 0.001891 |
| 12 | kites | 11 corners: 6 quadrilaterals, 2 pentagons | 0.004409 |
| 12 | free hexagons | 13 corners: 4 triangles, 1 quadrilateral, 4 pentagons, 1 hexagon | 0.016001 |

So the OCD plus these three gap pieces tile space: 1 + 48 + 12 + 12 per lattice point. **None of the piece faces is a rhombus.** The canonical cone fill works, but it is not the rhombic tiling DICTO pictured; rhombi would need a different division of the same gap (open).

Renders: `renders/ocdgap-{closed,cut,apart}.png` (`render_gaps.html`, `shoot_gaps.mjs`). The "cut" still does not slice (same issue as step 2).

## Open
- Fusions across the cell faces: gap pieces of neighbouring cells meet on V's square and hexagon faces and may fuse into fewer, nicer pieces.
- A rhombic division of the gap, for example around the free hexagons that face each other across V's square faces.
