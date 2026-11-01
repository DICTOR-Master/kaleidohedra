# HexOct as two single pieces (2 November 2026)

DICTO's aim: "really want to sort out HexOct into two true simple pieces". In #75 (HexOct: Two Tiles for Every Stacking) the
h-tile is one solid, but the c-tile is two towers touching only at the layer's ball (at λ = 1/10 and at the ring-build λ = −1/8).

**Conclusion:** shifting one tower of the c-tile by one in-layer lattice step makes it one solid at every weight; at λ = 3/8 both
tiles are convex (c = brick of two cubes, 6 faces; h = "twisted cube", 6 squares + 6 triangles, 12 faces) — recommended pair,
placeholder name **HexOct II** (DICTO names it).
**Status:** exact enumeration over 16 weights done; exact fill check over all 42 stackings of period ≤ 6 for the five pairs (0 overlaps);
sheet `hexoct-connected-tiles.pdf` (also in ~/Documents/papers-to-read), awaiting DICTO's read. Not for publication.

## Method (dicto-big-brother, ~/kres-tmp/hexoct-connect, ~/geom/bin/python; tiles.py etc. from studies/2026-10-29-endless-stack-cell, exactfaces.py from studies/2026-10-31-hexoct-ring-build)
1. `scripts/connect.py <λ>`: per tile type, piece 0 fixed, pieces 1–3 shifted by (a, b), −2 ≤ a, b ≤ 2 (15 625 choices; 25 at the walk's
   ends where a tile has 2 pieces). Exact face contacts (coplanar opposite facets, positive-area overlap). Keep face-connected choices;
   merge congruent ones (12 lattice symmetries × z-flip × shift); exact merged faces, surface check (every side in exactly two faces),
   hull ratio, neck (least contact area over all splits of the pieces in two, unit triangles), symmetry order. → `data/conn_<λ>.json`, `data/log_<λ>.txt`.
   Weights: −11/24, −5/12, −3/8, −1/3, −7/24, −1/4, −3/16, −1/8, −1/16, 0, 1/10, 1/8, 5/24, 1/4, 1/3, 3/8 (every stretch of the ring-build scan).
2. `scripts/verify.py <λ> <tc> <th> [RoH|W]`: all 42 words of period 2–6; every layer's chosen pieces matched one-to-one to the
   engine's pieces up to in-layer lattice shifts (through the #75 motion), volume of each tile = one layer cell, and exact separating
   planes between every piece of a tile and every piece of every nearby tile copy. → `data/verify_*.txt`.
3. `scripts/split_check.py` (→ `data/split.txt`): which layer's letter fixes each whole piece. At −1/3, 1/10, 1/4 the whole octahedral
   piece depends on both layers (3 shapes), tetrahedral pieces on their base layer: the Rule of Halves is the only two-tile split of
   whole pieces / mid-plane halves. At −1/8 all pieces are context-free; `scripts/alt_split.py` (→ `data/alt_split.json`) tries split W
   (layer = its two tetrahedra + whole octahedron above; pair B) and the gap slab (one tile: the known 60° rhombohedron, Lalvani 1990;
   no c/h, not proposed). Other cut planes not tried.
4. `scripts/describe.py`: exact faces, side lengths, exact convexity (every merged face a hull facet).
5. `scripts/render.py` (+ `build_render.py`, the ring-build renderer) with `scripts/pairs.json` → `figs/pair-*-views.png`, `figs/pair-*-stacks.png`
   (c gold, h blue, solid faces, crisp edges; stacks 2H ABAB, 3C ABCABC, 4H ABCB, 4 layers, 2 × 2 tiles, drawn apart). Sheet: `paper.html`
   printed with papers/print.mjs.

## Pairs (same λ for c and h; translates per piece in tiles.py order)
| pair | λ | split | c faces | h faces | convex | c translates | h translates | fill check |
|---|---|---|---|---|---|---|---|---|
| **A · HexOct II** | 3/8 | Rule of Halves | 6 (brick) | 12 (twisted cube) | both | (0,0) (−1,−1) | (0,0) (0,0) | 7 472 pairs, 0 overlaps |
| B | −1/8 | whole octahedra | 8 | 10 | no (6/7, 6/7) | (0,0) (−1,−1) (0,0) | (0,0) (0,0) (−1,0) | 6 480, 0 |
| C | −1/8 | Rule of Halves | 10 | 14 | no (0.800, 0.735) | (0,0) (0,1) (0,0) (0,1) | unchanged | 11 232, 0 |
| D | −11/24 | Rule of Halves | 18 | 8 (hexagonal prism) | h only | (0,0) (0,1) | unchanged | 4 080, 0 |
| E | 1/10 (#75) | Rule of Halves | 24 | 30 | no (0.745, 0.778) | (0,0) (0,1) (0,0) (0,1) | unchanged | 13 520, 0 |

Findings: the c-tile becomes one solid at every weight tested (best choice always: shift one tower one step); the h-tile was already one
solid (between 5/24 and 1/3 the best h-choice shifts its upper octahedral half (piece 3) one step). Only the two ends of the walk give convex tiles. Necks
shrink to near zero near 1/3 and near −5/12. At 3/8 the octahedral halves have vanished: each tile is its two tetrahedral parts.
Twisted cube: 6 squares of side 1/√2, 6 isosceles triangles (1/√2, 1/√2, √(2/3)), 11 corners at heights −1, −½, 0, ½, 1 (1+3+3+3+1).

## Prior art checked (2 Nov)
ask-library, 1 query ("convex space-filling polyhedron with six squares and six triangles, twisted cube, hexagonal close packing"):
Kerckhoff–Storm 2008, Zong 2012, Fang et al. 2013, Sommerville 1922, Torquato–Jiao 2009, Kramer 1982 (catalogue hits); pages:
Wikipedia Tetrahedral-octahedral honeycomb p.1, Koskinen 2011 p.2, Krishnamurthy–Akleman–Subramanian 2020 p.3; notes: Fedorov 1885 ch. 13.
Web, 1 query: en.wikipedia.org/wiki/Space-filling_polyhedron, en.wikipedia.org/wiki/Honeycomb_(geometry),
mathworld.wolfram.com/topics/Space-FillingPolyhedra.html, close-packing teaching pages. No twisted cube found; brick and 60°
rhombohedron classical. Not claimed new until a fuller check.
