# Is the DICTO Ogdoecontahedron a real periodic ↔ aperiodic bridge? (2026-10-16)

DICTO asked whether the Ogdoecontahedron is a real bridge between periodic and aperiodic structure (its regular hexagons belong to the honeycomb; its icosahedral symmetry belongs to quasicrystals), and whether researching that would justify Fable. We agreed to run three cheap checks first and to call in Fable only on a real hit. The script is `scripts/bridge.py` and its output is `data/bridge.txt`. It uses `studies/_lib/geomcheck.py` for the frame check and the known-case checks.

## Results: no hit on any of the three

1. **6D lift (the cut-and-project test).**
   - **Known case:** first, a known case passes. The triacontahedron spanned by the six unit 6D vectors fits the canonical window (a triacontahedron, as in the Ammann–Kramer–Neri tiling) at once, and its 60 edges all run along 5-fold axes.
   - **Lift:** the Ogdoecontahedron's corners lift to integer 6D points after scaling by 171 (no golden factor φᵐ gives a smaller lift). Their perpendicular images reach radius 116, against a window of 1.9.
   - **Window fit:** they first fit after 9 φ-inflations, and by then the solid's radius is about 4,750 tiling edges. Any finite golden point set fits eventually, so this means only that its corners are scattered points of a huge patch.
   - **Edges:** none of its 180 edges runs along any symmetry axis, while the tiling's edges all run along 5-fold axes. So it is not a cluster of the canonical quasicrystal.
2. **Cluster shells.**
   - **One real match:** its 30 two-fold corners are exactly the corners of the icosidodecahedron inside it. That is the 30-atom icosidodecahedral shell of the Tsai and Mackay clusters, and it is classical.
   - **No other match:** its 60 other corners lie on the same sphere, at 16.47° from the nearest 5-fold axis. That matches neither the Bergman 60-shell (truncated icosahedron, 20.08°) nor the Tsai 60 (triacontahedron edge midpoints, 17.78°). Its 12 five-fold corners sit slightly outside that sphere.
3. **Faces against tiles.** No corner angle of a face can be made from tile angles with up to 6 tiles at the corner. This covers the hexagon's 120° and the kite's 117.85°, 68.62° and 55.69°, tested against golden-rhombus angles (63.43°, 116.57°, the faces of the golden rhombohedra) and Penrose angles (multiples of 36°). So its faces cannot be tiled by those rhombi.

## Verdict

The bridge stays poetic. The Ogdoecontahedron combines honeycomb hexagons with icosahedral symmetry, but it is neither a patch nor a cluster of the canonical icosahedral quasicrystal, and its faces do not decompose into its tiles. Its one real tie is the classical icosidodecahedral shell it contains. On the agreed rule, this does not justify Fable. Scope: these are the canonical primitive tiling and the three standard cluster shells. Other 6D lattices (face- or body-centred), other windows, and decorated tilings were not tested.

Shell sources: Takakura et al. 2007 (Tsai); the Bergman and Mackay shells are standard (see the library's quasicrystal section).
