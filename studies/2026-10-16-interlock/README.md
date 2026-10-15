# The interlock: both cycles as one solid (DICTO, 2026-10-16)

DICTO's question: the wireframes of the up–down toggle can only be read by the two of us. Can the two cycles form one real, buildable solid?

**Method.**
1. `chains.py` builds one turn of the original Spheres of Dharma (I … I·φ³) and its polar image at the ends setting (ρ² = φ²/4, so the cycles share I and D), in one frame and at full precision.
2. Both chains are cut by cones over their inner faces (`../2026-10-16-polar-dharma/scripts/polar_pieces.py`), which gives convex pieces: 174 in the original turn and 154 per flipped turn.
3. `interlock.py` (run on dicto-node, `~/plotenv`) intersects every original piece with every piece of flipped turns 0 and 1, which together cover the original turn exactly.

**Result (float).** There are 536 convex pieces. Each lies in exactly one layer of each cycle. Every original piece is the sum of its parts, with a worst relative error of 4.1e-9. By symmetry orbit the float corners gave 13 kinds (seven of 60, one of 48, one of 20, four of 12). That was float noise: the exact check below finds 12 kinds. The data is in `data/interlock-ends.txt` and `.json`.

Several original layers lie wholly inside one flipped layer, so their pieces pass through unchanged. For example, the 12 dodecahedron → truncated icosahedron columns sit inside the next flipped turn's first layer. The cutting happens in the outer layer, the triacontahedron → I·φ³ roofs, which four flipped layers cut into 240 pieces.

**Views.** These are oriented orthographic sections through the centre (DICTO: fixed bearings, no perspective). Each looks along a five-fold, three-fold or two-fold axis with a two-fold axis up, so every picture is left–right symmetric. They carry crosshairs, up/down/left/right labels, and rings at the shared I and D and at I·φ³. Each is coloured once by the original layers and once by the flipped layers. They are made with `render_interlock.html` and `shoot_interlock.mjs` and saved as `renders/il-*.png` and `renders/sheet-*.png`. The hole at the centre is the shared icosahedron, where the next turn inward begins.

**Explorer.** The interlock is the third tab of the Polar Dharma Explorer (`../2026-10-16-polar-dharma/explorer`).

**Exact check (`interlock_exact.py`, run on dicto-node → `data/interlock-ends-exact.txt`).**
- Both cycles' pieces are rebuilt with exact ℚ(√5) corners. The flipped cycle is exact too: polar in ρ² = (3 + √5)/8, with its next turn scaled by φ³ = 2 + √5.
- Every interlock corner is solved from three exact planes. 1284 float points that lie only on edges are dropped, by a rank test on the plane normals.
- **Every original piece is exactly the sum of its parts, and every layer exactly the sum of its interlock pieces (remainder 0).**
- **12 kinds**: 12 exact volumes, and 12 symmetry orbits on the exact corners (eight of 60, three of 12, one of 20). The float count of 13 split one 60-kind into 48 + 12.

**Not yet done:** the middle setting, and naming or fusing the 12 kinds.

## The middle setting (DICTO, 2026-10-16)

At ρ² = 3φ²/4 = 3(3 + √5)/8 the cycles share ID and RT. The flipped cycle is exactly 3 times its ends-setting size, so its pieces are the ends pieces scaled by 3, and its turns −1 and 0 cover the original turn. Run with `interlock.py ../_lib middle` and `interlock_exact.py middle`; output in `data/interlock-middle*.txt` and `.json`.

- **502 convex pieces.** Every original piece is exactly the sum of its parts, and every layer exactly the sum of its pieces, with remainder 0. 1656 float edge points were dropped.
- **11 kinds:** 11 exact volumes and 11 orbits on the exact corners (eight of 60, one of 30, one of 20... see the data file). The float orbit count had 12, splitting a 20-kind into 12 + 8: float noise again.
- **Pieces that pass through whole.** Several original pieces lie inside one flipped piece and pass through uncut: the 30 roofs (RT → I·φ³, 0.773811), the 20 truncated icosahedron → Hecatodihedron pyramids, and the 20 icosidodecahedron → dodecahedron tetrahedra. The 60 small Hecatodihedron → RT tetrahedra (−93/152 + 21√5/76) pass through whole in both settings.
- **Comparison.** The ends setting cuts the outer roofs the most (240 pieces) and leaves the middle columns whole. The middle setting leaves the roofs whole and cuts the middle layers (the dodecahedron → truncated icosahedron columns into 132, the Hecatodihedron → RT layer into 180). The toggle moves where the two cycles cut each other.
