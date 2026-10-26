# The icosahedral Hexa treatment and the Icosaxes Kagome network (DICTO, 2026-10-27)

DICTO's idea: "a stella jewel icosahedral kagome style network", "maybe needs a hex jewel style treatment" — the DICTO Hexa
(#18) as the inspiration, not the shape: pieces passing into each other until they close, with icosahedral symmetry (A), and a
Kagome network as in the Kagome Hulls (#17) (B). DICTO chose the golden-split pair, **Icosaxes and Unborn Axes** (#48), as the
icosahedral counterparts of the DICTO Jewel and the stella. Study with Claude; exact checks in sympy, solids joined with manifold3d.

## Pieces (golden split, krp-core `polyhedra/golden-split.js`; icosahedron edge 1)
- Icosaxes = {|x|, |y|, |z| ≤ φ/2} ∩ {|x| + |y| + |z| ≤ φ²/2}: a cube cut by an octahedron; its hexagons lie at φ²/(2√3), the
  inradius of its icosahedron. Volume 1 + 2√5/3. Unborn Axes 1 + √5/3. Lotus Jewel Axes √5. Dodecaxes 2. Tricap (1 − √5/3)/8.

## A: twenty on the corners of a dodecahedron (icosahedral)
20 Icosaxes, one on each corner of a dodecahedron, each turned by the icosahedral rotation that carries (1,1,1) there (a hexagon
faces straight out), brought in from first touch. **Exact stops** (`scripts/exact.py`, output `data/exact-output.txt`):

| Stop | Distance d of each centre | d / first touch |
|---|---|---|
| first touch: a cage of 20, meeting along the dodecahedron's 30 edges, 12 open windows | φ²√3/2 | 1 |
| the 12 windows close at once: a sealed shell round a hollow | √3/2 | 1/φ |
| the hollow fills (Icosaxes): one solid, no holes | φ²/(2√3) (the icosahedron's inradius) | 1/3 |
| the hollow fills (Lotus Jewel Axes, dented): the Tricap tips meet | √3/(2φ) | 1/φ³ |

First touch by separating axes (face normals and edge cross products, exact); the window stop as a two-variable linear programme on
the five-fold axis; the hollow stops by the centre point. That the last point of a window is on its axis and the last point of the
hollow is the centre is by symmetry; the float sweeps (`twenty*.py`) agree at every stop. Renders: `twenty-sheet.png` (Icosaxes,
green), `twenty-lja-sheet.png` (Lotus Jewel Axes, gold), seen down a five-fold axis; `S0–S3`, `L0–L3` single views.

## Cubic blocks on the way (kept for B)
- H1/H2: 8 Icosaxes on a cube round an Unborn Axes = 9 Icosaxes passing through each other (each overlap √5/24; what is left of the
  middle one is exactly an Unborn Axes): one closed solid, volume 9 + 6√5. Open: whether this holds along the whole golden bond.
- K1: 8 Lotus Jewel Axes round a Dodecaxes, 8√5 + 2; K2: keys outward (Hexa-style roofs), 23.454. Both closed, genus 0, no overlaps.
- A1/A2 (icosahedra / Lotus Jewels round a void dodecahedron with 12 AXE): first pictures only; Blender's join was unreliable, no
  numbers kept (`data/blender-join-report.txt` is that unreliable run, for the record).

## B: Kagome networks of the golden split (`scripts/kagome-b.py`, `data/kagome-b.json`)
Icosaxes on (2Z)³, Unborn Axes on (2Z+1)³ (×φ/2). #17's rules: no Icosaxes in more than two clusters, no two clusters sharing more
than one.

| Cluster | Net | Neighbours | Icosaxes held twice / once / none |
|---|---|---|---|
| **cube8** (8 Icosaxes round an Unborn Axes) | BCC, anchors (1,1,1) + ⟨(2,2,−2), (2,−2,2), (−2,2,2)⟩ | 8 | **100% / 0 / 0** |
| octa7 / octa6 | BCC | 6 | 74% / 26% / 0 ; 74% / 0 / 26% |
| cubocta12 / 13 | FCC | 12 | 42% / 0–4% / 54–58% |
| rd14 / rd15 | BCC with second neighbours | 14 | 24% / 0–3% / 74–76% |

cube8 is perfect, as the rhombohedron was in #17: every Icosaxes in exactly two clusters; a quarter of the Unborn Axes sites hold the
cluster centres, the rest are the network's voids. **Keyed** (`check-net.py`, `data/NK1.json`, `NK2.json`): Dodecaxes at the
centres; NK1 every Icosaxes a Lotus Jewel Axes; NK2 each Icosaxes dented towards its two centres (opposite hexagons) and keyed
outward with the mirrored Tricap on the six facing voids. Both: no overlaps, no broken pieces. **NK2's piece has volume exactly
φ² = (3 + √5)/2** (Icosaxes + 4 Tricaps). Renders: `N2-parts.png` (framed clusters), `NK2x-parts.png` (keyed, pulled apart).

## Open questions for DICTO
- Names: the 20-corner shell and solid, NK2's piece (2 dents, 6 keys, volume φ²), the cube8 network.
- Is "the hollow fills at 1/3" etc. true along the whole golden bond (not only at x = τ)?
- DICTO asked whether the Icosaxes relate to #57: same weighted-division method (#52); a direct link is untested.
- Prior art: not yet searched (reference library, then web) — needed before any claim of novelty.

## Data
`data/*-union.obj`: joined solids (manifold3d), sites scaled ×φ/2; `*.json`: pieces as vertices + triangles. Scripts need
krp-core from ~/k-mix and ~/geom (numpy, scipy, sympy, manifold3d, trimesh) on dicto-big-brother.
