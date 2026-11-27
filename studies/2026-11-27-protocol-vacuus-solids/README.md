# New-shape protocol on the eleven special Vacuus-Solids (27 November 2026)

DICTO · study ("2, run the new-shape protocol"; "getting the build right for a representative sector ... then replicating it into the
whole shape ... to save computational time and energy"). With Claude (Anthropic). Protocol: papers/new-shape-protocol.md.

**Sector build.** One pit (the sector over one face) built exactly, copied to every face by the symmetries of P; control: the copied
walls equal the directly built walls, all eleven (groups 120, 48, 24). After this control a sector suffices for every later measurement.

**Results (scripts/protocol.py, logs/protocol.log, data/protocol.json; FINAL ok; Dehn screen calibrated: cube 0, octahedron not 0, TO 0).**
| P on Q | s | V E F (Euler) | volume (exact) | IQ | Dehn screen |
|---|---|---|---|---|---|
| dodecahedron / icosahedron (excavated dodecahedron) | 5 − 2√5 | 32 90 60 (2) | 30 − 10√5 | 0.106 | not 0 |
| dodecahedron / triakis icosahedron | (10 − 3√5)/11 | 32 90 60 | (70 − 10√5)/11 | 0.020 | not 0 |
| dodecahedron / deltoidal hexecontahedron | √5/3 | 32 90 60 | (10 + 10√5)/3 | 0.331 | not 0 |
| icosahedron / dodecahedron (great dodecahedron) | 3√5 − 6 | 32 90 60 | −10 + 10√5 | 0.209 | not 0 |
| icosahedron / pentakis dodecahedron | (6√5 − 9)/11 | 32 90 60 | (10 + 30√5)/11 | 0.021 | not 0 |
| icosahedron / deltoidal hexecontahedron | (30 − 9√5)/11 | 32 90 60 | (150 + 10√5)/11 | 0.602 | not 0 |
| rhombic triacontahedron / itself | 3 − √5 | 62 180 120 | 940 − 420√5 | 0.274 | **zero (screen)** |
| triakis icosahedron / deltoidal hexecontahedron | (42 − 11√5)/19 | 92 270 180 | (5702 − 2542√5)/209 | 0.549 | not 0 |
| tetrahedron / triakis octahedron | 9 − 6√2 | 8 18 12 | 24 − 16√2 | 0.068 | not 0 |
| octahedron / deltoidal hexecontahedron | (12 − 3√5)/11 | 14 36 24 | (16 − 4√5)/11 | 0.073 | not 0 |
| octahedron / disdyakis triacontahedron | 3 − 6√5/5 | 14 36 24 | 4 − 8√5/5 | 0.023 | not 0 |
(Volumes in each solid's frame of exact_check.py; no two walls of one solid are coplanar and adjacent: every wall is its own face.)

Step 9 (tiles alone?): ten have nonzero Dehn invariant (screen) and so cannot fill space by copies (Debrunner 1980, via the Dehn
invariant page). The rhombic triacontahedron's special member has Dehn zero on the screen: to be confirmed EXACTLY; zero is
necessary, not sufficient, for filling space (the rhombic triacontahedron itself has Dehn zero, its dihedral angle 4π/5, and does
not fill space), so it is a candidate only.
Steps 3 and 19 (known solid, prior art): the excavated dodecahedron (Wenninger 28) and the great dodecahedron are classical; the
draft's Section 6 reads the special sizes as stellations; which of Messer's 226 is the rhombic triacontahedron's member stays open.
Not run here (reason): 4-5 (no line family), 8 harmonic fingerprint (next), 10-13 (no tiling found), 14-16 (Vacuus census of these
non-convex solids: their faces are the walls, every pit already a Vacuus pyramid), 17 field: Q(√5) or Q(√2) as listed, 18 none yet.
