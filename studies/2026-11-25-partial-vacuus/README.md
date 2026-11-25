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

## Next
1. Archimedean and Catalan P and Q (does any other pair excavate exactly?).
2. Thickness rule: plates of thickness t, the smallest open core per solid (DICTO: a true Vacuus barely exists; every build is partial).
3. DICTO's B1NR cube as a measured example (core size from his build, when he gives it).
