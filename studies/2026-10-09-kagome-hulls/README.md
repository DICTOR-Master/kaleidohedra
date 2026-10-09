# Kagome hulls (DICTO, 2026-10-09)

DISCOVERIES.md #17. DICTO tested whether the hulls DICTO has worked with for months behave as expected
with the DICTO Jewel and the Sunstar. Design study with Claude (Fable), checked in krp-core v0.11.0.

## What was found
Six hulls give Kagome configurations (clusters sharing single pieces corner to corner) in both the
Stella–Jewel and the Sunstar lattice, and keep to one rule: **a hull with n corners sits on a network
where each cluster has n neighbours.**

| Hull | Pieces | Network | Neighbours | Even cells held twice / once / single |
|---|---|---|---|---|
| octahedron (`octa6`) | 6 + 1 inside | simple cubic (perovskite) | 6 | 0.77 / 0 / 0.23 |
| rhombohedron (`rhombo8`) | 8 + 1 inside | BCC, in block coordinates | 8 | 1 / 0 / 0 (perfect) |
| cuboctahedron, hollow (`cubocta12`) | 12 | FCC | 12 | 0.70 / 0 / 0.30 |
| cuboctahedron, solid (`cubocta13`) | 13 | FCC | 12 | 0.70 / 0.15 / 0.15 |
| cube (`cube14`) | 14 + 1 inside | BCC | 8 | 0.23 / 0.38 / 0.38 |
| rhombic dodecahedron (`rd33`) | 19 + 14 | BCC with second neighbours | 14 | 0.22 / 0.78 / 0 |

## Data (`data/`)
- `definitions.json`: each hull's cells from its anchor, the anchor rule, the net and its shares.
- `<hull>-jewel-raw/-unit.json`, `<hull>-sunstar-raw/-unit.json`: each cluster as one solid
  (raw: cube edge 2 per cell; unit: the Jewel rhombus edge 1, krp-core's scale).
- `<hull>-network.json`: a patch of each network.

## Checks
krp-core `scripts/verify-kagome-hulls.mjs`, every push: each solid closed, with the exact volume of its
pieces, in both lattices; each network Kagome style on a window (no cell in more than two clusters, no
two clusters sharing more than one) with the study's shares. In the study: no overlap by sampling,
consistent winding, Euler characteristic.

## Renders (`renders/`)
`<hull>-jewel`, `<hull>-sunstar` (one cluster in each lattice) and `<hull>-network` (a patch).

## Prior art
Not found (web search 2026-10-09) for the rhombohedral, cuboctahedral and rhombic dodecahedral nets
as regroupings of a space filling. Credited: corner-sharing octahedra (ReO₃, perovskite),
corner-sharing tetrahedra (pyrochlore), corner-coalesced cube nets (Molecules 24(7):1221, 2019), the
FCC primitive cell as a rhombohedron.

## DICTO's decisions
Keep all six, in both lattices, as arrangements in the Stella–Jewel and Sunstar worlds.
