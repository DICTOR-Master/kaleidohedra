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

## Next (step 3)

- Measure the shape of the remaining gaps, which face 12 free hexagons and 60 kites per copy.
- Test whether rhombic pieces can fill them: golden rhombohedra, the RT family, or a rhombic tiling grown from the kites.
