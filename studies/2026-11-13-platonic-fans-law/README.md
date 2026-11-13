# Do the open fans follow one law? Hexa-Key discs exact (13 Nov 2026; Platonic book Ch 4 open item)

**Conclusion (13 Nov 2026): for convex solids, yes, and it is proved. A central plane holds a closed #87 disc exactly when it meets the surface only along edges (it cuts across no face). When it does cut across faces, its edges break into open fans, one fan between each two cuts. For non-convex solids this is not a law: it fails both ways, with exact counterexamples in the Sunstar tetrahedral cluster, the Admiral Cap, the Hexa-Key and the Jewel tetrahedral cluster. Exact (Q(√5)): the Hexa-Key has 3 octagon discs and 6 dodecagon discs, 96 of its 360 edges = 4/15 = 26.7 %, and Delilah has 3 square discs, 12 of 12 edges = 100 %, both as in the float census.**

## 1. Hexa-Key and Delilah, exact
- **Hexa-Key** (registry DICTO_HEXA_KEY, 122 corners, 240 triangles, 360 edges). Every coordinate was recognised as (a + b√5)/4 (largest
  difference from the registry 9.1e-9; the registry stores about 8 digits). Exact checks: closed oriented surface (each edge in two
  faces, opposite ways), Euler 2, corner mean exactly at the origin, and volume exactly 6φ³ = 3/4 of the bounding cube of edge 2φ. This is
  the Hexa-Key of the Jewel study (studies/2026-10-20-dicto-jewel/jewel_exact.py: 48 of the 64 of its block). It is not convex.
  #87 discs, exact: **3 octagons** in the coordinate planes x = 0, y = 0, z = 0, and **6 dodecagons** in the planes x = ±y, y = ±z,
  z = ±x. That puts **96 of 360 edges on discs, 4/15 = 26.7 %**, as in the float census. The float apex sum agrees on every sheet.
  The octagon planes meet the surface only along edges. Each dodecagon plane also cuts across 8 faces. Those cuts lie in the same
  section piece as the disc, joined to it at corners. The Hexa-Key has 61 central planes carrying fins (data/fans-ce.log): the 3 + 6
  disc planes; 12 planes that cut faces and hold two opposite fans of 2 fins; 4 planes (x ± y ± z = 0) that contain faces and hold
  one open sheet of 36 fins; and 36 planes that hold two single fins.
  Caveat: some of the Hexa-Key's face cones from its centre have non-positive volume. The solid is not star-shaped from its centre, so
  the #87 Vacuus is applied here, as in the census, outside the hypothesis of #87 Theorem 1.
- **Delilah** (registry DICTO_DELILAH). Its registry corners are ±a·e_i with a = 2^(-5/6), so they are the corners of a regular
  octahedron (exact after scaling by 1/a). Its 8 faces are triangles, as on the octahedron. Exact: **3 square discs, 12 of 12 edges, 100 %**.

## 2. The law (convex solids): theorem and proof
Setting: P is a convex solid, and O is the mean of its corners, which lies strictly inside P. Π is a central plane through O that
carries at least one fin, so C = ∂P ∩ Π is the boundary of the convex polygon P ∩ Π, with O in its interior. A face is **cut** by Π when
it has corners strictly on both sides of Π.

**Theorem.** (a) Π holds a #87 disc exactly when Π cuts no face. In that case the disc is the whole of C, and every side of the section
polygon lies along edges of P.
(b) Otherwise the edges of P in Π split into open fans. Each fan is a maximal run of consecutive edges along C. Runs and cuts
alternate round C, so the number of fans equals the number of gaps, where a gap is a maximal stretch of C that passes through faces.
(c) Each central plane holds at most one disc.

*Proof.* (1) An edge lying in Π lies in ∂P ∩ Π = C. Since O is inside P, no edge line passes through O (an edge lies in a supporting
plane, which misses the interior), so every edge in Π is a fin. No face lies in Π, since a supporting plane cannot pass through O.
(2) C is star-shaped from O: each ray from O in Π meets C exactly once, so the polar angle round O runs monotonically along C. At a
corner v in Π, the edges of P in Π through v lie on C, and C is a simple closed curve, so there are at most two of them. If there are two,
they are the neighbours of v along C, and by monotonicity they lie on opposite sides of the ray Ov. #87 joins two fins at v exactly when
they are coplanar (both in Π) and on opposite sides of Ov. So the sheets in Π are exactly the maximal runs of edges along C.
(3) If Π cuts no face, every face meets Π in a face of itself: nothing, a corner or an edge. So C is a closed curve made of corners and
edges, which means of edges only. The single run is then all of C: a closed cycle whose polar angle increases monotonically by 2π. Its
apex angles sum to 2π, so it is a disc. If Π cuts a face f, the points of f's interior on Π lie on C and on no edge, so C is not covered
by edges. A disc in Π would be a closed cycle of edges in C that winds once round O. But a closed path in C that misses a point of C
lies in an arc, which can be shrunk to a point without crossing O, so it winds 0 times. So there is no disc, and every run is an open
fan. Part (c) follows from (2): there is only one curve C. ∎

**Controls, all exact.** The octahedron holds 3 discs of 4 fins (as does Delilah), the cuboctahedron 4 of 6, the icosidodecahedron 6
of 10; the cube and the dodecahedron hold none. In each case the disc planes are exactly the planes that cut no face. **Rhombic
dodecahedron:** each of its 6 planes cuts 2 faces, corner to corner along a diagonal, and holds **two opposite fans of 2 fins**.
**Rhombic triacontahedron:** each of its 15 planes cuts **4** faces, again corner to corner, and holds **4 single-fin fans** (two
opposite pairs). It does not hold two fans per plane. Its fins in a plane never chain, because every one of its corners in the plane
has only one edge in the plane. The Dogstar is not convex, but it still obeys the law on all 27 of its planes. On its 15 mirror planes it
holds two opposite fans (4 + 4 on 12 planes, 3 + 3 on 3), as in the exact study.

**Checked by computer, exact** (job fanslaw, 28 checks, 0 failed): T1 (disc ⇔ no face cut), T2 (sheets = runs of edges, at most one
disc) and T3 (O strictly inside) hold on all **76 convex registry solids recognised exactly, 1390 central planes**. In all, 91 of the 389
registry solids were recognised exactly (Q(√5), Q(√2), Q(√3), Q(√6), with rationals). The other 298 are not covered by the computer
check: their coordinates are not in one quadratic field at one common scale (tetrahedron frame, Johnson solids, snub solids,
Dodeca-13, ...). The proof covers every convex solid regardless.

## 3. Non-convex solids: the law fails both ways (exact counterexamples)
On the 15 non-convex solids recognised exactly (2914 planes) the law holds on 2894 planes and fails on 20.
- **Plane meets the surface only along edges, yet no disc** (11 planes):
  - **Sunstar tetrahedral cluster**, 10 planes. Each plane meets the surface only along edges and cuts no face, but some of those
    edges point straight at the centre: their line passes through O, so they carry no fin (apex angle 0). The loop of edges
    therefore breaks at them. On the 4 planes x ± y ± z = 0 there are 30 fins and 9 radial edges, and the fins form three open paths
    of 10, each ending at two corners where a radial edge continues. On the 6 golden planes (normal (1, φ², 0) and its images) there
    are 28 fins and 6 radial edges, in paths of 22 and 6. No corner has more than two fins of the plane (data/fans-ce.log).
  - **Admiral Cap**, plane y = 0. The section is a triangle of 3 edges that does not go round the centre (winding number 0; two of its
    corners turn back). The result is fans of 1 and 2 fins.
- **Disc, yet the plane cuts faces** (9 planes):
  - **Hexa-Key**, all 6 dodecagon planes. Each disc is a closed loop of edges round O, but the same plane also cuts 8 faces.
  - **Jewel tetrahedral cluster**, its 3 octagon planes, which also cut 8 faces each.
- The guess holds on every plane of the Dogstar (27), the Sunstar octahedral cluster (460), the Hexa (85), the Hexa rhombohedral
  cluster (571), the stella octangula and the other non-convex solids.

What remains for every solid is the #87 definition itself: a plane holds a disc exactly when its edges contain a closed loop that
goes once round O, turning the same way at every corner, with no edge pointing at O and no third edge of the plane at any of its
corners. For a convex solid the only such loop is the whole section, and that is what turns the definition into the section law. The
three ways a non-convex solid departs from it all occur in the registry: edges pointing at the centre (Sunstar tetrahedral cluster), a
loop of edges that does not go round the centre (Admiral Cap), and further cuts of faces elsewhere in the plane of a disc (Hexa-Key,
Jewel tetrahedral cluster).

## Proposed text for Ch 4's open item (DICTO to place; the book is not edited here)
> Do the open fans follow one law? For convex solids, yes. A central plane holds a closed disc exactly when it meets the surface only
> along edges, so that the section is a polygon whose sides are all edges of the solid. When the plane cuts across faces instead, its
> edges break into open fans, one between each two cuts. So the octahedron, the cuboctahedron and the icosidodecahedron have 3, 4 and
> 6 discs, and the cube none. Each of the rhombic dodecahedron's 6 planes cuts 2 faces from corner to corner and holds two opposite
> fans of two fins. Each of the rhombic triacontahedron's 15 planes cuts 4 faces and holds four single fins. For non-convex solids the
> rule is not a law. The Dogstar follows it on all its planes, but the Hexa-Key's six dodecagon discs lie in planes that also cut
> faces. On ten planes of the Sunstar tetrahedral cluster the plane meets the surface only along edges, yet some of those edges point
> straight at the centre, carry no fin and break the loop into open fans. (Exact, study 2026-11-13-platonic-fans-law: proof for convex solids; checked on 76 convex solids, 1390 planes, and on
> 15 non-convex solids, 2914 planes, with 20 exceptions.)

## Running
`scripts/fans_law.py` (exact; field class `scripts/qf.py`, copied verbatim from studies/2026-11-02-dicto-vacuus/scripts/qf.py, md5
a497ecfd…) ran on the second compute host through the job gate. Memory cage 4 GB, one process. Pilot `fanslaw-pilot` (24 solids): the
first two pilots FAILED and were fixed before any result was used. (1) The fins' turning sense was read in stored edge order, not
along the cycle. (2) The fixed ray of the winding count could pass through a corner, which wrongly dropped one Hexa-Key dodecagon; the
ray now runs through a corner of the cycle and is counted half-open. The third pilot passed (28 checks, FINAL ok). Full run `fanslaw`:
389 solids, 28 s, 28 checks, 0 failed, FINAL ok. Follow-up `fanslaw-ce` (scripts/inspect_ce.py, same exact helpers): the edge
structure of the 11 counterexample planes and the Hexa-Key's plane types, FINAL ok; it corrected a first README draft that had called
the Sunstar planes "branched". Logs: data/fans-pilot.log, data/fans-law.log, data/fans-ce.log; per-plane data: data/fans-law.json.
Inputs: ../2026-11-13-platonic-disc-ranking/data/registry-solids.json and disc-ranking.json (the float census, used for check X8).
Signs of plane tests use a float filter (float sign taken when |value| > 1e-6; otherwise exact). The coordinates are exact, so the
float error is below 1e-12.

## Sources checked
studies/2026-11-13-platonic-disc-ranking (README, LEADS 2 and 3, disc_ranking.py, data/disc-ranking.json, registry export);
studies/2026-11-13-platonic-exact-checks (README C, platonic_exact.py: recog, disc_census); studies/2026-11-02-dicto-vacuus (#87
definition, qf.py); studies/2026-10-20-dicto-jewel/jewel_exact.py (Hexa-Key = odd block minus 24 roofs, volume 48 of 64);
studies/2026-10-09-dicto-hexa/README.md (Hexa-Key description); papers/book-platonic/chapters/ch04.html §4.4-4.5 and the claims box
(read only, not edited); Concordance ledger [204], [209]. Reference library: the 564-work list (studies/2026-11-03-reference-library/
data/works.json) was searched for central section, central plane, great circle and zonohedra. Hits: Hart, Zonohedrification (1999);
Building systems with non-regular polyhedra based on subdivisions of zonohedra; Structural Topology 21 (1995). None states this law.
The convex statement is elementary and may well be known; no priority is claimed.

## LEADS
1. Ch 4 (DICTO's to place): the text above closes the open item. §4.5's sentence on the RD and RT should say that the RT's planes hold
   four single fins, not two fans; the Hexa-Key line can cite the exact 3 + 6 discs and 4/15.
2. The Hexa-Key and the Jewel tetrahedral cluster have discs in planes that also cut faces. A figure of one Hexa-Key dodecagon plane
   (disc plus the 8 cut faces) would show the non-convex case.
3. Edges pointing at the centre break the Sunstar tetrahedral cluster's loops. A census of such radial edges over the registry
   would show how often this kind of failure occurs.
4. The exact check covers only 91 of 389 solids. Recognition in two-field or cubic coordinates (tetrahedron frame, snub solids,
   Dodeca-13) would widen it. For convex solids the proof already covers them.
5. studies/2026-11-13-platonic-exact-checks picks its winding ray from fixed candidates, and these can all pass through corners (here
   they did on one Hexa-Key plane). Its Dogstar result stands, because its float apex sum agreed on all 54 sheets and Dogstar has no
   closed sheet. A future reuse of that function should take the half-open ray of this study.

DICTO · dictospheres.com
