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

## Exact Dehn invariant of the rhombic triacontahedron member (scripts/rt_dehn_exact.py, logs/rt_dehn_exact.log, FINAL ok)
Sector build: one pit carries every edge type. Material angles, exact in Q(sqrt5), each proved a rational multiple of pi (equal
minimal polynomials of cos^2): knife edges (the RT's 60 edges) 2pi/5; pit edges to the 5-fold corners: pyramid angle 2pi/3; pit
edges to the 3-fold corners: pyramid angle 4pi/5 (material angles 2pi minus these). Every term length (x) angle vanishes in
R (x) R/Q pi: the Dehn invariant is EXACTLY ZERO. Controls: the plain RT's dihedral is 4pi/5; the excavated dodecahedron's angles
(cos^2 = 5/9) are not rational multiples of pi. Consequence: Dehn does not rule out space-filling for this solid; whether it
fills space is OPEN (zero is necessary, not sufficient; the plain RT also has Dehn zero and does not fill space).

## Are the Star Cores stars Vacuus-Solids? (27 Nov 2026; DICTO: "turn 4 star from star cores app, turn 5 same, turn 3 star; turn 1 too spikey")
scripts/dump_star_turns.mjs (the app's own chain, shape D109 Ophelia, doubling rule t = 2), star_is_vs.py (region test), star_vs_volume.py.
- Exact structure (Section 8 of #123): a Vacuus-Solid of P with polar core is core + edge wedges + corner pyramids. A star "core with a
  spike to each corner of P" is core + corner pyramids only. So such a star is the Vacuus-Solid WITH ITS EDGE WEDGES REMOVED: the same
  tips and the same hollows, but the spikes stand apart where the Vacuus-Solid is joined by knife-edge wedges along P's edges. Check:
  icosahedron + 20 spikes to the dodecahedron's corners has volume 2.918; the excavated dodecahedron 30 - 10 sqrt5 = 7.639 (my first
  'positive control' assumed they were equal: they are not; the region test correctly called them different).
- Ophelia, turns 3-5 (S = 60 corners, 32 faces; turns 3 and 5 identical, period two): the star's hull has 32 corners (all spike tips) and
  60 faces; the deepest star points under the 60 faces lie at ONE common size (spread 1e-11), so the hull's Vacuus-Solid with pits
  down to the star is a genuine family member. The star holds 57% (turns 3, 5) and 59% (turn 4) of its volume; the rest is the material
  along the hull's edges. Numerically: not a Vacuus-Solid, but its edge-stripped relative. Turn 1 (642 corners, 440 faces): far apart.

## All 386 Star Cores stars (scripts/dump_all_stars.mjs, star_vs_all.py, depth.py; data/stars_vs.json; numerical)
Share of the hull's pitted solid (pits under each hull face down to the star) that the star fills, 330 meaningful cases:
- Lahdeli (D77) turn 4, t = 2: 100%: trivial, the star is convex (cube + six half-height pyramids = the rhombic dodecahedron), no pits.
- Samson (D71) turn 1, t = 2: 99.7%, pits deep (0.29-0.33 of the face distance) but not at one size: the closest real near-miss.
- Samson from turn 2 on is a FIXED POINT (DICTO: "turn 3 the solid is the core itself"): 12 corners, 8 faces (truncated-tetrahedron
  shaped), its own core; star fills 88%, pits at one size. Ophelia (D109) settles into period two instead (57-59%).
Render: renders/SAMSON-STAR-VS-PITTED-HULL.png (turn 1 and turn 3; star, pitted hull, both). Off-axis pit test not settled: at turn 1
Samson's own corners lie on hull faces, so the pits there are not simple pyramids (to rethink, not patch).

## Four tetrahedra at their tips vs Samson's fixed point (27 Nov 2026; DICTO: four tetrahedra meeting at their tips form the four outward
triangles of a truncated tetrahedron; "check its worth a look")
- Four regular tetrahedra (edge 1) with their tips at the centre, pointing to the four tetrahedral directions, base corners toward the
  other directions: outline = a truncated tetrahedron with triangles of side 1, hexagons with sides alternating 1 and 2/3, all corners on
  the sphere of radius 1 (turned 60 degrees instead: the cuboctahedron). Not the regular truncated tetrahedron (that needs radius 1.1726).
- Samson's fixed point (turns 2-5, both rules t = 2 and t = phi: the same shape): also a truncated tetrahedron with all corners on one
  sphere, but the other way round: small triangles (side 0.29706), long hexagon sides 0.76194, ratio 2.56488, radius / triangle side
  2.06141. So NOT the four-tetrahedra shape (ratio 2/3). Both rules reaching the same fixed shape is itself notable (closed form open).

## Samson's fixed shape: closed form (27 Nov; DICTO "yes do please"; scripts/samson_cf.py; identified, not proved)
The ratio hexagon side / triangle side of Samson's fixed truncated tetrahedron is r = 2.56488140124198 (float data of the app's chain),
a root of 27r^3 - 54r^2 - 36r - 8 = 0 (integer relation found by mpmath findpoly, tolerance 1e-11). With r = 2s/3 this is
s^3 - 3s^2 - 3s - 1 = 0, i.e. (s + 1)^3 = 2 s^3, so s = 1/(cbrt2 - 1) and
    r = 2 / (3 (cbrt2 - 1)) = (2/3)(1 + cbrt2 + cbrt4)        (checked to 30 digits: the cubic vanishes; data agree to 1e-14).
The cube root of 2 (the Delian number, doubling the cube) fits the October exact study, which put Samson's chain in Q(cbrt2) (radius^2
falls by exactly 1/9 per turn: the shape repeats at a third of the size, up to a turn). For comparison the four-tetrahedra truncated
tetrahedron has r = 2/3 exactly: Samson's ratio is that 2/3 times 1 + cbrt2 + cbrt4 (an observation, no reason known).
Status: identified numerically to the precision of the data; an exact derivation from the core rule is the next step.
