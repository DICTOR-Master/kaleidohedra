DICTO · dictospheres.com — renders of the scutoid stand-in study, 21 Nov 2026. The core solid (working name C1 in the study) is
DICTO's Fullerene Star: truncated icosahedron, edge 1, with a dodecahedron centre pyramid on each pentagon.

Resin solution (tree branch D): bcc lattice at its smallest scale s0 = (10 + 4 sqrt5)/3, truncated-octahedron mould, central division R1.
  resin-c1.png       the Fullerene Star whole, and with its 12 pyramids pulled out along their 5-fold axes (pyramids violet)
  resin-cell.png     one cell: the 80 resin pieces pulled apart from the centre (mould see-through, enlarged with the pull), and together
  resin-tiling.png   six bcc cells face to face; the front cell shows the Fullerene Star inside its see-through mould
  resin-kinds.png    kinds 1-5 alone, each standing on its face of the Fullerene Star, same scale
Scutoid divisions, bcc mould at 6/5 s0:
  scutoid-combi-cell.png        DICTO's combi method (tree branch E, centroid seeds): one cell pulled apart, 80 scutoids, 5 kinds
  scutoid-combi-kinds.png       its kinds 1-5 from above and from below; Fullerene Star side dark, mould side light, Y vertices white dots
  scutoid-skeleton-kinds.png    exact straight skeleton (branch D round 3): the two scutoid kinds, 2 (6 -> 5) and 3 (3 -> 4), above and below
  scutoid-skeleton-hexagons.png the 12 kind-2 hexagon scutoids round the Fullerene Star, Y vertices marked

Coordinates exact from the study data: tree/branch-D-resin/data/resin.json and skeleton_exact.json; data/geom_combi_bcc_6-5_cen.json
is written by scripts/combi_dump.py (branch E's combi.py, unchanged but for storing the float geometry; its run repeats branch E's
result: valid, 80 scutoid pieces, 5 kinds, 30 Y vertices). Checks in scripts/scenes.log and scenes2.log (volumes add to mould minus
the Fullerene Star in all three divisions; piece counts; Y vertices), both FINAL ok.
Kind colours are neutral labels only (sand, bronze, slate, rose-beige, ash); hexagon faces neutral pearl; violet = dodecahedron colour.
Near-side glass of the moulds is left out so that edges behind it stay visible; the far side is drawn see-through.
scripts/: scenes.py, scenes2.py (scenes + checks), render3d.py and shots.mjs (house three.js renderer, copied unchanged from paper #115),
compose.py (figures). Rendered on the compute host with Playwright.
