# One world for all (DICTO 10 Nov 2026: "how about inside their skins as other solids" → "yes verify the skins, one world for all")
**Result.** Every mix of the five Platonic solids with RD and CO (127 mixes) fills space in ONE world: the cubic grid of edge φ, whose
alternating cubes hold dodecahedron-shaped cells and RD cells. Each solid sits inside a SKIN that makes it the dodecahedron (edge 1):
| inside | edge | skin (exact, skins.py; volumes add to (15 + 7√5)/4) |
|---|---|---|
| D | 1 | none |
| C | φ | 6 roofs (Euclid: dodecahedron = cube + 6 roofs) |
| T | φ√2 | 4 right-angled corner tetrahedra (legs φ) + 6 roofs |
| O | φ/√2 (corners at the cube's face centres) | 8 octant pieces (cube of edge φ/2 minus its corner tetrahedron) + 6 roofs |
| CO | φ/√2 (corners at the cube's edge midpoints) | 8 corner tetrahedra (legs φ/2) + 6 roofs |
| I | 1/φ | Karma shell (#22): 12 pentagonal pyramids + 30 AXE + 20 CLEO |
RD cells: cube + 6 square pyramids. Between them the Dogstar-type remainder cells; edging X, XR, and whole cubes (or Y).
No octet and no seam at all. Check (one_world.py, data-one-world.log): random points, every one covered exactly once, every solid of
each mix present, all 127 mixes: FINAL ok. (Contrast: #47 used four worlds; the free-scale core two worlds with one seam.)
Note: in a skinned cell the solid sits concentric with Euclid's cube, all in the dodecahedron's own (pyritohedral) frame.

## Sphere-unit sizes (10 Nov, sizes.py, data-sizes.log, FINAL ok; DICTO 22 Oct "about the size of a unit sphere")
Larger exact choices inside the same dodecahedral cell:
- O of edge φ²/√2 (corners = the 6 roof-ridge midpoints of the dodecahedron): skin = 8 congruent caps, each 9/32 + 13√5/96 (exact).
- I of edge 1, Pacioli in that octahedron (= #47's I + six Admiral Caps, each Admiral Cap exactly (1 + √5)/24 = φ/12), also inscribed
  in Euclid's cube (one edge in each face): skin = 6 Admiral Caps + the 8 caps.
Surrounding-sphere radii: D, C, T 1.401 (one sphere: Euclid's cube and its tetrahedron are inscribed in the dodecahedron's sphere);
O 1.309; CO 1.144; I 0.951; RD 1.618. Largest/smallest 2.753 → 1.701.
Further option (not yet checked): the icosahedron dual to the cell (corners at the 12 face centres, radius 1.114, edge ≈ 1.171);
RD (1.618) is then the outlier, fixed by the grid.
- 13 Nov 2026 cover_render.py (Platonic book cover, DICTO's choice of #106 Figure 1): the skins row re-rendered at 7200 x 1440 px (one-world sizes, D·I·C·T·O, element colours, crisp edges); controls (edge lengths, corners inside the cell) pass, FINAL ok; job platonic-cover on the compute host. Output: papers/book-platonic/cover/cover-skins.png.
