# Unused tools 4, 5, 6 (DICTO 4 Nov: "4,5,6") — hopf_interlock.py, hopf-interlock.json
(4) HOPF RINGS OF THE WHITE QUEEN. The 600-cell's 120 corners are the unit icosians (a group, checked). Left cosets of cyclic subgroups split them into great-circle rings,
and the Hopf map sends each ring to one point of the 2-sphere (checked for every ring):
  C10: 12 decagons -> 12 points, 5 nearest neighbours each = the ICOSAHEDRON
  C6:  20 hexagons -> 20 points, 3 each = the DODECAHEDRON
  C4:  30 squares  -> 30 points, 4 each = the ICOSIDODECAHEDRON
Classical (discrete Hopf fibrations of the 600-cell: Coxeter; Sadoc & Mosseri). For us: the White Queen, read as rings, IS the first stations of the golden cycle (I, D, ID).
App view: the Queen as 12 rings over the icosahedron (and 20, 30).
(5) INTERLOCKING (Dyskin et al. 2003). Octet slab between two (111) layer planes, kinematic test (free velocity v with v·n <= 0 on every face shared with a neighbour):
  every octahedron is LOCKED; every tetrahedron is FREE (it slides out obliquely through its face on the slab plane). So the octet slab is not topologically interlocking;
  its octahedra are. LEAD: the same test on the Vacuus builds, the HexOct tiles and DICTO's node/ring builds; which stacking layers lock their tetrahedra.
(6) Not computed today, recorded as statements to check: Aurenhammer–Hoffmann–Aronov 1998 guarantee that #51's equal-volume weight (Samson and Delilah) exists and is unique
  up to a constant; #53's stops should be bistellar flips of the weighted Delaunay triangulation (Edelsbrunner–Shah 1996) — test by counting the change at each stop;
  Dechant–Bœhm–Twarock's golden affine translations vs the φ³ cycle step — open.

## Interlocking of DICTO's pieces (4 Nov) — interlock_pieces.py, interlock-pieces.json (translational test; rotations not yet)
Calibration: Dyskin et al.'s tetrahedron layer (square midsections, neighbours turned 90°): all 21 interior blocks locked — as published.
- #47 Admiral slab (engine data): ALL 21 interior Admiral Caps LOCKED (each cap a rigid pair of tetrahedra); all 3 icosahedra locked; tetrahedron face pyramids 18 locked, 4 free.
- Octet slab cut into centre pyramids: T pyramids 39 locked / 13 free; O pyramids 33 / 12.
- Cube layer cut into C6 pyramids: pyramids inside the layer all locked (32); pyramids with base on the layer surface all free (24).
Pattern: a pyramid with its base on a free surface, narrowing inward, can always slide out through that surface; turned the other way it is locked.
So the Admiral Cap slab is translationally interlocking (Dyskin's sense) apart from a thin skin of tetrahedron pyramids — relevant to building it in cardboard or stone without glue.
NEXT: rotational test (small rotations, LP on twists), and the same test on the Vacuus builds, HexOct tiles and DICTO's node/ring builds.
