# Build plan: the 13-dodecahedron block

*DICTO's cluster (DISCOVERIES.md #13). Exact values are checked on every push by krp-core's
`scripts/verify-dodeca-cluster.mjs`; the bcc stacking at the end is a study, measured but not yet made
exact. Dimensions are for a dodecahedron edge **a** (multiply by your edge: a = 40 mm makes a block
about 29 cm across, 7.26a).*

## 1. The pieces

| Piece | How many | Shape | Volume |
|---|---|---|---|
| Dodecahedron | 13 | regular, edge a (1 centre + 12 around it) | (15 + 7√5)/4 · a³ ≈ 7.6631 a³ |
| Wedge | 30 | two regular pentagons (edge a) hinged on one shared edge at **10.3048°**; closed by 2 end triangles (a, a, 0.1708a) and 2 outer trapezoids (a, 0.1708a, a, 0.2764a) | φ³/20 · a³ ≈ 0.2118 a³ |
| Needle | 20 | tetrahedron: three edges a from its tip, base an equilateral triangle of 0.1708a | (45 − 19√5)/600 · a³ ≈ 0.004191 a³ |

Exact forms: 0.1708a = a/(φ²√5); 0.2764a = a/(φ√5); 10.3048° = 360° − 3 × 116.5651°
(three dodecahedra round an edge).

## 2. Separable units

The filled block comes apart (DICTO's requirement), so build it as units rather than gluing it all:

- Cut each **wedge** in half along its mirror plane (the plane through the centre's edge that bisects
  the 10.3048° gap): 60 half-wedges, each a thin 5.1524° wedge on one pentagon.
- Cut each **needle** in thirds along the same planes (through its tip and its long edges): 60
  needle-thirds.
- Each of the **12 outer dodecahedra** carries, as fins, the 5 half-wedges on the 5 faces that border
  the face it shares with the centre, and the 5 needle-thirds at that shared face's 5 corners.
- The **centre** dodecahedron carries nothing.

So the block is 13 parts: the bare centre and 12 finned dodecahedra. Every fin meets its neighbour's
fin flat, on a mirror plane, so each unit lifts straight out.

## 3. Assembly (DICTO's order)

Hold the centre with a corner straight up (a 3-fold axis vertical). Its 12 faces sit in four layers
of three around that axis:

1. The **snowflake belt**: the six faces round the middle (two rings of three), seen from above as a
   six-pointed snowflake.
2. The **three dimples on top**, round the upward corner.
3. **Turn the block over** and fill the last three dimples.

Each outer dodecahedron is the centre's mirror image across their shared face (it sits turned 36°
on that face). Check as you go: neighbours meet only along the centre's edges, and each gap there
is the 10.3048° wedge, filled by two facing half-wedge fins.

Finished block: volume 13(15 + 7√5)/4 + 30φ³/20 + 20(45 − 19√5)/600 ≈ 106.06 a³; its
outside is 72 pentagons, 60 thin trapezoids and 20 small triangles.

## 4. Stacking blocks (tentative: grown fins)

Blocks cannot meet whole face to whole face as plain copies (every face contact turns the next block
36°), so stacking uses **grown fins**:

- **Lattice**: body-centred cubic, cube edge **6.668a**; each block touches its 8 nearest neighbours
  along its corner (3-fold) directions, centres **5.775a** apart; the block's own orientation is the
  same in every position (translations only).
- **Fill**: the blocks fill **71.5%**; the remaining 28.5% is the grown fins, shared out so each block
  owns the part of space nearest to it. Each grown unit is then one shape that fills space by the bcc
  translations.
- **Shape of a grown unit**: close to the bcc cell, a truncated octahedron (8 hexagons, 6 squares),
  but the block pokes out of it by up to **0.185a** at 48 corners, so the unit's boundary zigzags
  round those points and neighbouring units interlock.

**Not yet worked out** (needed before building the stack): the exact shape of the grown fins
(measured on a grid so far, not computed exactly), and whether the interlocked units can be lifted
apart (separability of the grown units is unchecked). The fins are chunky (28.5% of each unit),
not slim stars.

## 5. Status

- Block (sections 1–3): exact and checked; recorded as DISCOVERIES #13, Zenodo
  [10.5281/zenodo.23247392](https://doi.org/10.5281/zenodo.23247392).
- Stacking (section 4): a study, recorded in #13, not claimed.
- Shown nowhere in the apps yet; the pieces could join Polyhedraverse's Space-Filling Pairs once the
  grown units are exact.
