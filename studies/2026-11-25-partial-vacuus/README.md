# Partial Vacuus: a Vacuus that stops short of the centre (25 November 2026)

DICTO · study, V SF A project. The idea is **DICTO's** (25 Nov): "the excavated dodecahedron is kind of a vacuus"; "it reminded me of
my B1NR build as depth doesn't go all the way to center"; "it may be just a practical solid as a true vacuus or resonus barely exists";
"it's a chain stage 3" (his Lotus seed and Dodecahedral Chain, stage 3 = the excavated dodecahedron, Polyhedraverse TRANS_LOTUS_3).

> **Status box.** Study note, not published. Part 1 exact (sympy over Q(√5), faces found numerically, every wall checked).
> Part 2 (thickness rule for real builds) and the Archimedean/Catalan extension still to run.

**Definition.** A partial Vacuus of a solid P: every face dug in as a pyramid pit with its apex on the face's axis at a fraction s of the
face's distance from the centre (s = 0: the Vacuus pyramids meet at the centre; s = 1: the solid). A depth is **special** when every wall
of every pit lies in a face plane of one other solid Q (then the pits end exactly on Q, the core).

## Part 1 (scripts/special_depths.py, logs/special_depths.log, FINAL ok)
Among the five Platonic solids (P and Q both Platonic, same centre) there are exactly two special depths:

| P | pits end on Q | apex at s = | solid |
|---|---|---|---|
| dodecahedron | icosahedron | 5 − 2√5 ≈ 0.528 | the excavated dodecahedron (DICTO's Lotus seed / Dodecahedral Chain, stage 3); all 60 faces equilateral, each pit half a J13 |
| icosahedron | dodecahedron | 3√5 − 6 ≈ 0.708 | the great dodecahedron (Kepler–Poinsot), read as an icosahedron with its 20 faces dug in as triangular pits |

Rejected (only some walls on Q): cube pits at s = 1/φ on icosahedron planes; dodecahedron pits on tetrahedron and octahedron planes.
The tetrahedron, octahedron and cube have no special depth within the Platonic solids.


## Part 1b: all Platonic, Archimedean and Catalan solids (scripts/special_depths_all.py, special_check.py; data-special-*.json; FINAL ok)
Every solid put in a common frame (three perpendicular half-turn axes on x, y, z), the other solid tried in all 24 frame orientations
(both icosahedron placements, both tetrahedron placements). A depth is kept once per solid (pits ending on the icosidodecahedron's
triangles are the icosahedron's planes again). For every depth below the pits were checked to be interior-disjoint (the excavated
body is a solid). Control: both depths of part 1 found again.

| P (pits on its faces) | apex at s = | walls lie on the faces of (scaled) | closed form |
|---|---|---|---|
| tetrahedron | 0.5147186 | triakis octahedron | 9 − 6√2 |
| octahedron | 0.6000000 | triakis tetrahedron | 3/5 |
| octahedron | 0.3167184 | disdyakis triacontahedron | numerical (exact pending) |
| octahedron | 0.4810724 | deltoidal hexecontahedron | numerical (exact pending) |
| dodecahedron | 0.2992542 | triakis icosahedron | (10 − 3√5)/11 |
| dodecahedron | 0.5278641 | icosahedron | 5 − 2√5 (the excavated dodecahedron, DICTO's chain stage 3) |
| dodecahedron | 0.7453560 | deltoidal hexecontahedron | √5/3 |
| icosahedron | 0.4014916 | pentakis dodecahedron | (6√5 − 9)/11 |
| icosahedron | 0.7082039 | dodecahedron | 3√5 − 6 (the great dodecahedron) |
| icosahedron | 0.8977626 | deltoidal hexecontahedron | numerical (exact pending) |
| rhombic triacontahedron | 0.7639320 | **a smaller rhombic triacontahedron** (scale 1/φ) | 3 − √5 |
| triakis icosahedron | 0.9159606 | deltoidal hexecontahedron | numerical (exact pending) |

No Archimedean solid and no other Catalan solid has a special depth against these solids. The rhombic triacontahedron is the one
solid whose pits end on a smaller copy of itself (scale 1/φ, pits reaching 3 − √5 of the way in): a self-similar partial Vacuus.
Closed forms marked are fitted and checked to 1e-7; a symbolic proof (as part 1) is LEAD 4.

4. (LEAD) Exact derivation of every depth in part 1b, as part 1 did for the Platonic pairs.
5. (LEAD) Which of these excavated solids are classical stellations (as the excavated dodecahedron and the great dodecahedron are).

## Next
1. DONE (part 1b above).
2. Thickness rule: plates of thickness t, the smallest open core per solid (DICTO: a true Vacuus barely exists; every build is partial).
3. DICTO's B1NR cube as a measured example (core size from his build, when he gives it).
