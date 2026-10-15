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

## Step 4: a partner shape for the 12 free hexagons? (DICTO, exploratory, float, `scripts/partner.py`)

There are 3 partner sites per OCD, at the square-face centres of its cell. Each meets 4 free hexagons (2 from each OCD on that cube axis), so 3 × 4 = all 12 free hexagons. Giving each gap piece to its nearest site, each site collects 24 pieces whose volume is **exactly one third of the gap per OCD**. But the union is **not convex**: its hull is twice its volume, so the partner is a dented solid cradled between OCDs. Partners meet each other on irregular triangles and other polygons, **no rhombi** (`data/partner.txt`); they touch the OCDs on 18 face planes (quadrilaterals, pentagons, 2 hexagons).

## Step 5: twinning, turning copies into the other golden frame (DICTO: "would rotating out of their connections change the shadow shapes?"; `scripts/twin.py` → `data/twin.txt`)

A twinned copy is the OCD turned 90° about a cube axis, which puts it in the other golden frame. That turn maps the 8 joint directions onto themselves. Positions stay the same (so still 77.43%), and no arrangement collides anywhere. At a joint between a plain copy and a twinned copy, the two hexagons share plane, centre and size but are **turned 15.52° against each other**. The contact becomes a 12-gon covering **94.4%** of the hexagon, and the six slivers join the gap, so the gap shapes change.

| Arrangement | Full joints | Twisted joints |
|---|---|---|
| (a) one network, B twinned | 0 | 40 |
| (b) double network, second network twinned | 64 (within each network) | 64 (between the networks) |
| (c) bcc alternating | 0 | 128 |

In (b) the two interpenetrating networks are the two golden frames, as in the toggle.

## Step 6: octahedral or tetrahedral bridges with hexagon faces? (DICTO; `scripts/bridge_shapes.py` → `data/bridge-shapes.txt`)

- **Octahedral sites (square-face centres): yes, a closed solid.** The planes of the 8 free hexagons facing the site enclose a solid with 8 corners and 8 faces (4 triangles, 4 quadrilaterals), volume 0.021229. It collides with no OCD. Each face lies in a hexagon's plane but only partly overlaps the hexagon: the face reaches past the hexagon edge, over the kites, which slope away. Three such bridges per OCD fill **19.0%** of the gap.
- **Tetrahedral sites (cell corners): no.** The planes of the facing hexagons do not close; the region runs off to infinity.

## Step 7: hexagonal prisms as limbs (DICTO: "hexagonal prisms of different angles as limbs"; `scripts/limbs.py` → `data/limbs.txt`)

Every copy has the same orientation and is centrally symmetric. So the copy at lattice point c has a hexagon exactly parallel, opposite and equally turned to our free hexagon H (centre p): it equals H + v with v = c − 2p. Sweeping H along v gives a **hexagonal prism**. It is right only for the existing joints (v = 0) and oblique otherwise. Its side faces are parallelograms with sides s and |v|, which are rhombi only if |v| = s.

- **One limb per free hexagon.** Each free hexagon has exactly one limb that hits no other OCD. It runs to the copy across the nearest square face: length 0.522476 = 2.196 s, **tilted 79.19°** from the hexagon normal, a steeply sheared prism. Its sides are parallelograms of 0.2379 × 0.5225, **not rhombi**.
- **Limb classes.** A limb's two ends are a hexagon and the opposite hexagon of the next copy, so the 12 free hexagons give **6 limbs per copy**. These come in 3 crossing pairs, one per cube axis, crossing at the square-face centres.
- **Collision-free choice.** Choosing one limb from each pair gives **3 limbs per copy** (8 ways), using 6 of the 12 free hexagons. They fill 12.9% of the gap.
- **Competition.** The limbs pass through the octahedral sites, so they compete with the octahedral bridges of step 6 for the same space.

## Step 8: pyrochlore sharing of the conflict zones (DICTO; `scripts/conflict.py` → `data/conflict.txt`)

Keep all 6 limbs per copy and let each crossing pair **share** its conflict zone, as pyrochlore tetrahedra share corners.

- **The zone.** It is the intersection of the two crossing limbs, one at each square-face centre (3 per copy): **12 corners, 10 faces, all quadrilaterals**, volume 0.002140 (14.9% of a limb). It lies inside the octahedral bridge of step 6 but is not the same solid.
- **Golden rhombi.** **2 of its faces are golden rhombi**: angles 63.4349° and 116.5651°, diagonals in the golden ratio 1.618034. These are the faces of the rhombic triacontahedron and of the golden rhombohedra. The other 8 faces are quadrilaterals with angles 80.12°–99.88°. (Float so far; exact check pending.)
- **Filling.** All 6 limbs with each zone counted once fill 23.8% of the gap per copy.
