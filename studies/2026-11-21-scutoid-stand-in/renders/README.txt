DICTO · dictospheres.com — renders of the resin solution (scutoid stand-in, tree branch D), 21 Nov 2026
Arrangement: bcc lattice at its smallest scale s0 = (10 + 4 sqrt5)/3, truncated-octahedron mould, central division (R1).
Coordinates exact from tree/branch-D-resin/data/resin.json (five kinds, moved by the 24 elements of T_h) and C1 rebuilt as
branch D's resin.py builds it; scripts/scenes.log lists the checks (vol C1, 80 pieces, sum of piece volumes = mould - C1,
every piece inside the mould and on one C1 face), FINAL ok.

resin-c1.png      C1 whole, and with its 12 pyramids pulled out along their 5-fold axes (pyramids violet = dodecahedron colour)
resin-cell.png    one cell: C1 with the 80 resin pieces pulled apart from the centre (mould see-through, enlarged with the pull),
                  and the same cell together
resin-tiling.png  six bcc cells face to face; the front cell shows C1 inside its see-through mould
resin-kinds.png   kinds 1-5 alone, each standing on its C1 face, same scale

Kind colours are neutral labels only (sand, bronze, slate, rose-beige, ash); C1's hexagon faces neutral pearl.
scripts/: scenes.py (scenes + checks), render3d.py and shots.mjs (house three.js renderer, copied unchanged from paper #115),
compose.py (figures). Rendered on the compute host with Playwright.
