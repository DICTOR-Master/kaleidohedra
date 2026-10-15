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
