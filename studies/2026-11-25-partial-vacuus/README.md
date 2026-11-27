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
| octahedron | 0.3167184 | disdyakis triacontahedron | 3 − 6√5/5 |
| octahedron | 0.4810724 | deltoidal hexecontahedron | (12 − 3√5)/11 |
| dodecahedron | 0.2992542 | triakis icosahedron | (10 − 3√5)/11 |
| dodecahedron | 0.5278641 | icosahedron | 5 − 2√5 (the excavated dodecahedron, DICTO's chain stage 3) |
| dodecahedron | 0.7453560 | deltoidal hexecontahedron | √5/3 |
| icosahedron | 0.4014916 | pentakis dodecahedron | (6√5 − 9)/11 |
| icosahedron | 0.7082039 | dodecahedron | 3√5 − 6 (the great dodecahedron) |
| icosahedron | 0.8977626 | deltoidal hexecontahedron | (30 − 9√5)/11 |
| rhombic triacontahedron | 0.7639320 | **a smaller rhombic triacontahedron** (scale 1/φ) | 3 − √5 |
| triakis icosahedron | 0.9159606 | deltoidal hexecontahedron | (42 − 11√5)/19 |

No Archimedean solid and no other Catalan solid has a special depth against these solids. The rhombic triacontahedron is the one
solid whose pits end on a smaller copy of itself (scale 1/φ, pits reaching 3 − √5 of the way in): a self-similar partial Vacuus.
All twelve depths are roots of quadratics over Q (scripts/exact_forms.py + sympy factor; data-exact-forms.json; logs/exact_forms*.log): each depth refined over every wall at double precision, its integer polynomial found, factored, and the factor with the matching root kept. A symbolic proof from exact coordinates (as part 1) remains LEAD 4.


**Permutahedra and associahedra (DICTO 26 Nov: "any permutahedra or associahedra etc").** The three permutahedra (truncated
octahedron A3, truncated cuboctahedron B3, truncated icosidodecahedron H3) and their duals (tetrakis hexahedron, disdyakis
dodecahedron, disdyakis triacontahedron) are in the run above: none has a special depth of its own; the disdyakis triacontahedron is
the core for the octahedron's pits at s ≈ 0.3167. The twelve associahedra of study 2026-11-24-permutahedron-leads (A3, B3, H3, every
Coxeter element computed there), in their permutahedra's Coxeter frames (checked: three half-turn axes on x, y, z, as the common frame),
tried as pitted solid and as core against all 31 solids and each other (scripts/special_depths_all.py with ASSOC=1,
logs/special_assoc.log): **no special depth**. Their low symmetry (order 2) leaves nothing to carry every wall onto one solid's faces.

4. (LEAD) Exact derivation of every depth in part 1b, as part 1 did for the Platonic pairs.
5. (LEAD) Which of these excavated solids are classical stellations (as the excavated dodecahedron and the great dodecahedron are).

## Next
1. DONE (part 1b above).
2. Thickness rule: plates of thickness t, the smallest open core per solid (DICTO: a true Vacuus barely exists; every build is partial).
3. DICTO's B1NR cube as a measured example (core size from his build, when he gives it).

## Prior art (DICTO 26 Nov: "prior art"; sources checked 26 Nov 2026)
- The **excavated dodecahedron**: Wenninger, *Polyhedron Models* (1971), model 28, "third stellation of icosahedron" (the Ef1g1
  stellation in Coxeter, Du Val, Flather and Petrie, *The Fifty-Nine Icosahedra*, 1938). Who first called it "excavated" was not found.
  Sources: Wikipedia "Excavated dodecahedron" and "List of Wenninger polyhedron models" (checked); the books themselves not opened.
- The **great dodecahedron**: Poinsot (1809); Kepler–Poinsot polyhedron (Wikipedia, checked).
- **Excavating any solid by face pyramids of a chosen height** is a standard operation (augment faces with pyramids of negative height)
  in Robert Webb's *Stella4D*; Robert Austin's blog (robertlovespi.net, tags "excavation"/"excavated") shows excavated tetrahedra,
  octahedra, snub cubes and truncated icosahedra made with it, and notes that taller pits on the octahedron meet at the centre.
  Polytope Wiki has "excavated truncated rhombicuboctahedron". Checked: search pages only, posts not each opened.
- Not found anywhere: the family read **from the Vacuus outward** (the centre built out into a scaled dual core), the special sizes
  as the points where every pit wall lies on a face of a core solid, and the census over all Platonic/Archimedean/Catalan pairs
  (12 depths, including the rhombic triacontahedron on a 1/φ copy of itself). Those are DICTO's reading and this study's results.
- **As a key** (DICTO 26 Nov: "its a kind of key" — a pit takes a spike of the same height, lock and key; given to steer the prior-art
  search): the nearest prior art is **topological interlocking** (Dyskin, Estrin et al., 2001: term coined; Platonic solids and the
  concavo-convex "osteomorphic" blocks interlock), Belov-Kanel et al., arXiv:0812.5089 (interlocking of convex polyhedra), and
  Akpanya, arXiv:2405.01944 (interlocking blocks built from tetrahedra and octahedra in the tetroctahedrille). Abeille's flat vault
  (1699) is the classical ancestor. None found uses face pyramids (pits and matching spikes) as the key on a space-filling piece.
  Checked: search pages and abstracts only.

## Part 3: building out the core of any Vacuus, and solidity (scripts/build_out_general.py; data-build-out-*.json; FINAL ok)
Core = the solid's polar dual scaled by lam (corners lam n_f/d_f on the face axes); t = lam / min d_f² from 0 (Vacuus) to 1 (solid).
Solidity: the thinnest material wedge between two pits along an edge. Yardstick (DICTO: "just the classics for models"): the
excavated dodecahedron, 41.81° (the great dodecahedron: 63.43°).
- Platonic + cuboctahedron (control: both classics found again): cuboctahedron no special size; as solid as the classics from
  t ≈ 0.64 (tetrahedron 0.64, cube 0.56, octahedron 0.54, dodecahedron 0.54, icosahedron 0.58; grid step 0.02).
- McCooey's 162 self-duals (dbb job build-out-mccooey, 0 errors): **no special size** in any; pits disjoint at every size tested in
  all 162; **32 of 162** reach the classics' solidity (median from t ≈ 0.78), the other 130 never do (their thinnest wedge stays
  below 41.8° at every core size).

**Check of the cores (scripts/special_scenes.py, 26 Nov):** the core bounded by ALL pit-wall planes was computed (halfspace
intersection) and its face count compared with Q's. In **8 of the 12** (all icosahedral: dodecahedron on icosahedron, triakis
icosahedron and deltoidal hexecontahedron; icosahedron on dodecahedron, pentakis dodecahedron and deltoidal hexecontahedron; rhombic
triacontahedron on itself; triakis icosahedron on deltoidal hexecontahedron) **the core is exactly Q** (scaled). In the other 4
(tetrahedron on triakis octahedron; octahedron on triakis tetrahedron, deltoidal hexecontahedron, disdyakis triacontahedron) every wall
lies in a face plane of Q, but the walls do not make up Q (core 12 or 24 faces against Q's 24, 12, 60, 120): a weaker coincidence,
listed separately from now on. LEAD 6: identify those four cores (likely a Td/Oh solid on a subset of Q's planes).
- **The whole Vacuus catalogue (163 solids; dbb job build-out-catalogue, 0 errors):** with the dual as core, the only special sizes
  are the two classics (dodecahedron 5 − 2√5, icosahedron 3√5 − 6); pits disjoint at every size tested in all 163. As solid as the
  classics at some core size: all 31 Platonic, Archimedean and Catalan solids, all 10 bipyramids and 10 trapezohedra, 22 of 92
  Johnson solids, 1 of 10 prisms, 1 of 10 antiprisms.

## Golden and silver forms of the depths; parallel with Poinsot (DICTO 26 Nov question)
5 − 2√5 = √5/φ³ (excavated dodecahedron); 3√5 − 6 = 3/φ³ (great dodecahedron); 3 − √5 = 2/φ² (rhombic triacontahedron on itself,
core scale 1/φ); 9 − 6√2 = 3/δ², δ = 1 + √2 the silver ratio (tetrahedron on triakis octahedron). (Checked numerically to 1e-15.)
Parallel: Kepler (1619) and Poinsot (1809) found the star solids; Cauchy (1813) showed they are stellations (faces of the
dodecahedron/icosahedron extended); Bertrand (1858) obtained them by faceting. At a special size of the build-out the pit walls lie in
the core's face planes, so the outer surface is made of the core's planes: the excavation meets the stellation route there. At every
other size the walls lie in new planes (the Vacuus plates swung about the edges): no stellation, the build-out's own family.
To check (LEAD 7): which of the 8 true-core depths are stellations of their core in the classical sense (Fifty-Nine Icosahedra
diagram), beyond the two classics.

## Stellations and Tacitus of the twelve special solids (26 Nov; DICTO "do that and then run the harmonic silence scan")
- **Stellations.** In the 8 true-core cases every pit wall lies in a face plane of the core Q, and the body has no other faces (the
  pits cover all of P's faces), so its whole surface is made of Q's planes: it is a union of cells of Q's stellation diagram, i.e.
  a stellation of Q in the general sense. The two on the icosahedron/dodecahedron are classical (Fifty-Nine Icosahedra Ef1g1; the great
  dodecahedron); the six on the triakis icosahedron, deltoidal hexecontahedron, pentakis dodecahedron and rhombic triacontahedron
  are stellations of Catalan solids; which cells they use (and whether they meet Miller's rules) is LEAD 7.
- **Tacitus (scripts/tacitus_excavated.py, logs/tacitus_excavated.log; FINAL ok).** Face directions = the pit walls (merged when
  coplanar), unit and area weights, degrees 1–20: **no silence beyond symmetry in any of the twelve.** Every icosahedral one has the
  full group (order 120) and is silent in degrees 1, 2, 3, 4, 5, 7, 8, 9, 11, 13 (and the odd degrees beyond), the octahedral ones
  (order 48) in 1, 2, 3, 5 and the odd degrees, the tetrahedral one (order 24) in 1, 2, 5: exactly what symmetry forces.
  Fault met and fixed: a first pass chose each wall's outward side by a test along the wall itself (sign effectively random), which
  broke the symmetry and showed false "silences"; fixed to point into the pit; the other scripts' sign rules checked (origin-based).

## Nested-shell gaps (DICTO 26 Nov, open)
Golden cycle data (study 2026-10-25-gnomon-shapes, stations-exact.json) hold CORNERS only. First test, step 2 (Cleo star -> D′, which
adds 12 inward pentagonal pyramids): the icosahedron I's corners do not lie on D′'s face axes in the stored frame (0 of 12), so the pits
of step 2 are not shown to be the excavated dodecahedron's pits; the apex fraction from I's radius would be 0.7918, not 5 − 2√5.
Not settled: the pyramids' apexes must be read from the Vajrayana #35 construction itself (faces, not corners). Double Vision not yet
looked at. No claim either way.
**Settled for step 2 (26 Nov, from the piece coordinates in pieces.json):** the 12 inward pentagonal pyramids of step 2 (Cleo star →
D′) are pits of the build-out family of the dodecahedron D′ exactly: every apex on its face axis, all at one depth
**s = 15/2 − 3√5 ≈ 0.7918** (= 3/2 − (3√5 − 6)). So the step-2 gap = the 12 pits of the excavated dodecahedron of the family at that
size + 30 valley tetrahedra. It is not a special size (not chain stage 3, 5 − 2√5): a member of DICTO's family, not one of the
stellation points. The other steps' added pieces are outward (Shields, pyramids over faces): no other inward pits in the cycle.
Double Vision: not yet tested.

## Prior art, stellations of the cores (searched 26 Nov; search pages and summaries, papers not opened)
- Rhombic triacontahedron: Ede (1958, 13 basic series); **Messer (1995), all 226 fully supported stellations named** (MathWorld
  "Rhombic Triacontahedron Stellations"; G. Hart, "Stellations of the Rhombic Triacontahedron"); Pawley (restrictions for a complete
  enumeration); Gingrich (Miller's-rules counts 358 833 097 / 155 014 690); R. Webb (Great Stella reproduces Messer's 227; software3d.com).
  The self-similar excavation of the RT (depth 3 − √5, core 1/φ) is a stellation of the RT, so it is almost certainly one of Messer's
  226: to be identified by its cells and credited (LEAD 7).
- Archimedean duals (triakis icosahedron, pentakis dodecahedron, deltoidal hexecontahedron): stellations enumerated in part by
  R. Webb (MathWorld "Archimedean Dual Stellations", from Webb's tables); Wenninger, Dual Models (1983). The three cores' excavations
  are stellations of these: likely in those enumerations as shapes; to identify and credit.
- What remains ours (DICTO): reaching them from the Vacuus by building out the core; the special sizes as the only points of each
  family where the excavation is a stellation; their exact depths (all quadratic; golden 1/φ³, 2/φ² and silver 3/δ² forms); the census
  over the whole Vacuus catalogue and McCooey's self-duals; the golden cycle's step-2 pits as a family member (15/2 − 3√5).
**All nested pairs of the golden-cycle / Double Vision stations (26 Nov):** for every pair X ⊂ Y among I, D′, ID, OG, rTI, TI, H, jtI,
RT, M, I·φ³ (convex hulls), tested whether every face of Y has exactly one corner of X on its axis with the pyramid (face + that
corner) clear of X (sampled): **only I in D′** (s = 15/2 − 3√5, the step-2 pits above). No other shell gap holds a full set of pits of
any family; the Double Vision chain I ⊂ ID ⊂ O ⊂ TI ⊂ H ⊂ RT ⊂ I·φ³ included as far as its shells are in the station data (its
octahedron O is not in that file: not tested).
**Double Vision's O rebuilt and stored (26 Nov, DICTO "rebuild octahedron shell and store data"; scripts/rebuild_O.py, FINAL ok):** the
Ogdoecontahedron O (80 faces; polar of H) at its Double Vision station, exact in Q(√5): O = c · poles(H), **c = (9 + 3√5)/8 = 3φ²/4**
(the middle toggle), matching the stored render copy (progenitors data/full-cycle.json st.O) at every corner, frames shared through
the ID. Stored as data-double-vision-O.json (corners a + b√5). Gap test with O against every station, both ways: **no pair holds a
full set of pits.** So in the golden cycle and Double Vision together, only I in D′ (step 2, s = 15/2 − 3√5) does.

## Polar test: a Resonus counterpart? (26 Nov; DICTO "get it happening asap; even a negative result is a result")
scripts/polar_test.py, data-polar-test.json, logs/polar_test.log (FINAL ok; control: great dodecahedron -> small stellated
dodecahedron, 12 spike tips). Polar reciprocal D of each special Vacuus-Solid (one corner per distinct wall plane, its pole).
- **Always (all 12, and by a one-line argument for every Vacuus-Solid):** every corner of D lies on an edge line of the polar P*.
  Each wall contains an edge of P, so its pole lies on the polar line of that edge, which is the line of the matching edge of P*.
- **Spiked P* (the hypothesis) only for the two classics:** the great dodecahedron's polar is the small stellated dodecahedron
  (12 tips on the dodecahedron's face axes, height √5 in units of its face distance), and the excavated dodecahedron's polar has
  20 corners on the icosahedron's face axes at height 3: the corners of the great stellated dodecahedron (DICTO's Cleo star).
  There, several extended edges of P* meet at one point on a face axis, which is the stellation point.
- **The other 10:** corners on the extended edges of P*, not meeting at face axes: no spikes.
**Answer:** the Resonus-side counterpart of a Vacuus-Solid is an *edge-extended* polar (corners pushed out along P*'s edge lines),
and it is a spiked polar exactly at the two classics. Negative for the spike hypothesis in general; positive as a law (corners on
P*'s edge lines always), and it singles out the classics again. Into the Vacuus-Solids paper as a section (DICTO to confirm).

## Exact check of the special sizes (26 Nov 2026; scripts/exact_check.py, logs/exact_check.log, FINAL ok)
Every number in Q(√5) or Q(√2) as a pair of fractions; Platonic solids from standard coordinates, Catalan cores as polars of the
Archimedean solids; floats only to find candidates. Claim per pair: for one axis rotation of Q, every pit wall of P at s lies on a
face plane of λQ with ONE λ > 0. Controls: the two classics pass; both at s ± 1/1000 fail.
- **Eleven special sizes proved exactly**, minimal polynomials as listed in part 1b. Eight build the whole core (every face of λQ
  carries a wall); three are planes only (tetrahedron/triakis octahedron 12 of 24, octahedron/deltoidal hexecontahedron 24 of 60,
  octahedron/disdyakis triacontahedron 24 of 120). Exact λ: e.g. dodecahedron/icosahedron λ = (3−√5)/2 = 1/φ², rhombic
  triacontahedron λ = 1/φ, triakis icosahedron/deltoidal hexecontahedron λ = 1.
- **Correction:** octahedron / triakis tetrahedron at s = 3/5 is NOT special. Exactly, 12 walls lie on face planes of Q (λ = 1)
  and 12 on those of −Q (λ = −1): the octahedron is centrally symmetric, Q is not. The float search compared normals up to sign.
  It stays in the paper as a near miss (walls on the planes of Q and its opposite). Count: 11, not 12.

## Core or planes only? (27 Nov 2026; DICTO: "is it really mathematically sound to include the figs with the far more complex inner cores?")
scripts/core_or_planes.py, logs/core_or_planes.log, data-core-or-planes.json (numerical: sampling and 1e-7 tests; exact check to follow).
Theorem 1's condition (every pit wall lies in a face plane of lam Q) is about PLANES only. Tested for all 26 (P, s, Q) of the search:
- The pit walls cover NONE of any Q's faces (0% in all 26): the walls extend Q's face planes outward; they never lie on Q's faces.
- Q = the hull of the pit tips (a real core, the family's polar core) in exactly 2: the excavated dodecahedron (Q icosahedron) and the
  great dodecahedron (P icosahedron, Q dodecahedron). The pits touch Q at its corners only.
- Pit tips at corners of Q, Q larger than their hull, no pit entering Q: tetrahedron/triakis octahedron (4 of 4 tips),
  dodecahedron/deltoidal hexecontahedron (12 of 12), icosahedron/deltoidal hexecontahedron (20 of 20).
- Pits ENTER Q: octahedron/triakis tetrahedron (4 tips inside Q): Q is not a core at all.
- All other pairs: every pit tip lies outside Q; Q floats inside without touching any pit: planes only.
Consequence for the Vacuus-Solids draft: Figure 2 may draw Q inside as a core only for the two classics; the corner-touching three
must be described as such; the others show shared planes, not a core.
EXACT (scripts/exact_core_or_planes.py, logs/exact_core_or_planes.log, FINAL ok; Q(sqrt5) / Q(sqrt2), the eleven members of Theorem 1):
for each pit tip, exact position against lamQ; for each wall, exact 2D separating-axis test of the wall triangle against lamQ's face in
the same plane; for each pit, a wall plane with the whole pit on its far side. Result, agreeing with the numerical pass:
CORE (every corner of lamQ a tip, every tip a corner, walls meet lamQ only at points): dodecahedron/icosahedron, icosahedron/dodecahedron.
TOUCH (tips at some corners of lamQ, no tip inside, walls meet lamQ only at points): dodecahedron and icosahedron/deltoidal
hexecontahedron (12 of 62, 20 of 62 corners), tetrahedron/triakis octahedron (4 of 14). PLANES (every tip outside lamQ, every wall
triangle apart from lamQ's face): the other six. In all eleven every pit is separated from lamQ by one of its own wall planes: no pit
enters lamQ.
