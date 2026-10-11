# Chain of Karma (DICTO, 2026-10-11)

DICTO's infinite expansion of the Lotus seed (DICTO Icosa-13, #19). Name by DICTO.

## The rule
The Lotus seed's outer shape is exactly an icosahedron enlarged by φ² (20 face planes; volume
(235 + 105√5)/12 = (9 + 4√5) × the edge-1 icosahedron = φ⁶ × it). So it is a golden inflation rule:

> icosahedron × φ² = 12 icosahedra + 1 small icosahedron (edge 1/φ) + 60 AXE + 20 FUJI + 20 CLEO

Put a Lotus seed in place of every icosahedron (each Lotus seed matched to its icosahedron's size and turn), keep
the AXE, FUJI and CLEO whole, and repeat, upward without end, or downward ("build back down", DICTO).

## Checks (`scripts/lotus_nest.py`)
| Step | Size | Pieces | Icosahedra | AXE · FUJI · CLEO | Icosahedra's share | Volume / φ^(6n) |
|---|---|---|---|---|---|---|
| 1 | φ² | 113 | 13 | 60 · 20 · 20 | 68.19% | 1 + 1.3e-9 |
| 2 | φ⁴ | 1,569 | 169 | 840 · 280 · 280 | 46.50% | 1 + 2.2e-9 |
| 3 | φ⁶ | 20,497 | 2,197 | 10,980 · 3,660 · 3,660 | 31.71% | 1 + 2.8e-9 |

No overlaps by construction (every step is exact similar copies of the checked Lotus seed). The icosahedra's share
falls by (12 + φ⁻³)/φ⁶ = 0.6823 each step; pieces after n steps: 13ⁿ icosahedra, 100(13ⁿ − 1)/12 gap pieces of each
kind ratio 3 : 1 : 1. Data for steps 1–2: `chain-of-karma-steps-1-2.json`; render `renders/step2.png`.

## Why the gap pieces stay whole (`scripts/inflate_test.py`)
φ²·AXE, φ²·FUJI and φ²·CLEO cannot be refilled by the edge-1 family (icosahedra, AXE, FUJI, CLEO): Archimedes' test
(volume) allows it (e.g. φ²·AXE = 9 AXE + 2 FUJI + 2 CLEO in volume), but the Dehn invariant (basis 37.3774° and
41.8103° = arccos(√5/3)) rules out every whole-number solution. Sanity check: the same program recovers the Lotus
seed's own counts for φ²·I. So the Chain of Karma is a hierarchy with gap pieces in every size step of φ², not a
single-size tiling.

## Next
With the roof icosahedron (#21: icosahedron + 6 Admiral Caps = octahedron, octet truss) the Chain can grow inside a
periodic frame: DICTO's infinite EKP icosahedral network. To check: how the Admiral Caps scale with the Chain.
Literature search not yet done (hierarchical icosahedral clusters and inflation tilings, e.g. Kramer, Danzer, Mackay).
