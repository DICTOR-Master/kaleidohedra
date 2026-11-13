# Do the open fans follow one law? Hexa-Key discs exact (13 Nov 2026; Platonic book Ch 4 open item)

**Conclusion (13 Nov 2026): for convex solids, yes, and it is proved. A central plane holds a closed #87 disc exactly when it meets the surface only along edges (it cuts across no face). When it does cut across faces, its edges break into open fans, one fan between each two cuts. For non-convex solids this is not a law: it fails both ways, with exact counterexamples in the Sunstar tetrahedral cluster, the Admiral Cap, the Hexa-Key and the Jewel tetrahedral cluster. Exact (Q(√5)): the Hexa-Key has 3 octagon discs and 6 dodecagon discs, 96 of its 360 edges = 4/15 = 26.7 %, and Delilah has 3 square discs, 12 of 12 edges = 100 %, both as in the float census.**

**Follow-up (section 4): a rule stated on the fins instead of the section holds for every solid, convex or not, and is proved: a central plane holds a disc exactly when its edges that do not point at the centre include a closed loop that goes once round the centre, turning the same way at every corner, with no other such edge at its corners. Exact on all 91 recognised solids (4304 planes, no exceptions); the convex law is a corollary.**

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
Jewel tetrahedral cluster). Section 4 turns this into a proved rule for every solid.

## 4. Non-convex rule (follow-up, 13 Nov 2026)
**Conclusion: one rule holds for every solid, convex or not, and it is proved. It is stated on the fins of the plane, not on the
section. A central plane holds a #87 disc exactly when the edges in that plane that do not point at the centre include a closed loop
that goes once round the centre, turning the same way at every corner, with no other such edge at any of its corners. The convex law of
section 2 follows from it. Exact on all 91 recognised registry solids (1390 convex planes, 2914 non-convex planes, disc for disc,
0 exceptions); in floats on all 389 registry solids. The rule stays close to the #87 definition. What it adds is that the joining
step of #87 can be replaced by plain connection in the plane, and that cuts of faces do not enter.**

Setting: P is any solid made of flat faces (convexity and star shape are not needed), O the mean of its corners, Π a central plane.
A **fin** is an edge whose line misses O. The **fin graph** G(Π) is the set of fins lying in Π, with their corners; its **pieces** are
its connected parts. A loop of fins **turns one way** when every fin of it turns round O in the same sense (seen along the normal of Π).
#87, as fans_law.py implements it: two fins at a common corner v are joined when O, v and their two other ends lie in one plane and
the two fins lie on opposite sides of the line Ov; a sheet is a class of joined fins; a disc is a sheet that is a single closed cycle
(at least 3 fins, every corner on exactly 2 of them) that turns one way and winds once round O.

**Theorem N.** Π holds a #87 disc exactly when some piece of G(Π) is a simple closed loop that turns one way and winds once round O.
The disc is then that piece. For a loop that turns one way, "winds once" is the same as "its angles at O add to exactly 2π".

*Proof.* (1) A fin AB spans with O a single plane, and joined fins share it, so every sheet lies in one central plane. The sheets in Π
therefore split the fins of G(Π) among them, and each sheet, being connected, lies inside one piece.
(2) Let L be a loop of fins in Π that turns one way. At a corner v of L with neighbours u and w along L, the sides uv and vw turn the
same way round O, so u and w lie on opposite sides of the line Ov. The two fins of L at v are therefore joined, and all of L lies in one
sheet.
(⇐) Let the piece K be a loop that turns one way and winds once. By (2), K lies in one sheet, and by (1) that sheet lies in K. So the
sheet is K: a closed cycle that turns one way and winds once, which is a disc.
(⇒) Let D be a disc in Π, and K the piece of G(Π) that contains it. If K were larger than D, some fin f of K outside D would meet D at a
corner v. The far end of f is not on the line Ov (else the line of f would pass through O), so f lies on one side of Ov. The two fins
of D at v lie on opposite sides of Ov by (2), so f is on the opposite side to one of them, in the same plane: #87 joins them, and f
would belong to D. So K = D.
Last sentence: along a loop that turns one way, the angles at O all have the same sign, and their sum is 2π times the winding number. ∎

**Corollary (convex solids, section 2).** If P is convex and O lies inside it, no edge line passes through O and no face lies in Π,
and G(Π) lies on the section curve C = ∂P ∩ Π, a simple closed curve round O. A loop of fins that winds once round O is a simple closed
curve inside C, so it is all of C. Hence Π holds a disc exactly when C consists of edges, that is, when Π cuts no face. This is
Theorem (a) of section 2.

**What each clause does, with registry examples (exact, data/fans-nonconvex.log).** Planes without a disc, by the clause that fails:
- *no loop of fins at all* (open fans only): 1354 convex planes, 2870 non-convex planes;
- *edges pointing at O break the loop* (the section consists of edges, but some of them have their line through O, so they are not
  fins): the 10 planes of the Sunstar tetrahedral cluster (6 or 9 such edges in each);
- *the loop does not go round O*: the Admiral Cap's plane y = 0 (a loop of 3 fins, winding 0, not turning one way; angles add to
  0.97 × 2π);
- *a loop goes round O, but a further fin meets one of its corners*: 12 planes, x ± y ± z = 0 of the Hexa, the Hexa-Key and the Hexa
  rhombohedral cluster. Each of these planes contains faces of the solid (12, 12 and 24 or 36), and the fin graph there is one branched
  piece of 36, 36 and 72 or 108 fins. The relaxed rule without this clause (job check N3b) would give these 12 planes a disc, wrongly.
What does not matter: cuts of faces elsewhere in the plane, even where the cut faces touch the loop's corners (the Hexa-Key's 6 dodecagon
discs, the Jewel tetrahedral cluster's 3 octagon discs, each in a plane that cuts 8 faces), and edges pointing at O that are not part of
the loop (each octagon plane of the Jewel tetrahedral cluster holds 8 of them and still holds its disc).
In the registry, the angle-sum test alone separates the loops (check N5: no loop of fins with angles adding to 2π fails to turn one
way), but the proof needs the turning clause: a loop of fins can sweep forward through π and back through π, adding to 2π without going
round O. No registry plane holds more than one disc. For non-convex solids this is an observation, not a theorem: two nested loops
round O in one plane are not excluded by the rule.

**Checked by computer** (job fansnc, scripts/fans_nonconvex.py; 9 checks, 0 failed, FINAL ok). The script runs fans_law.py's own
recognition and #87 code unchanged (exec'd, with only its sheets and exact corners exported) and computes the rule independently:
N1 rule = #87 definition, same edge sets, on every plane of all 91 exactly recognised solids (76 convex, 1390 planes; 15 non-convex,
2914 planes); N2 convex corollary (rule ⇔ no face cut, no face in the plane); N3 every disc plane holds a loop round O among its fins;
N3b the 12 planes above; N4 every loop the rule accepts has angles adding to 2π (float); N5 above; N6 the rule in floats gives the
float census's disc sizes on all 389 registry solids; N7 plane totals 1390 + 2914 as in fans-law.json; N8 the 20 exceptions of section 3
reproduced (11 + 9), each now agreeing with the rule. The rule needs no closed surface and no star shape, so the Hexa-Key caveat of
section 1 does not touch it.
Running: pilot fansnc-pilot (17 named solids) on the second compute host through the job gate, memory cage 4 GB, 3 cores. Two pilots
FAILED and were fixed before any result was used. (1) Check N3 first required the relaxed rule R0 to equal #87; it does not (12 planes,
above), so N3 now checks only that R0 is necessary and N3b records the planes. (2) The float rule took its plane normal rounded to
6 digits, so the cuboctahedron's angle sums missed 2π by more than the tolerance (N6 failed twice); it now uses the unrounded normal,
as the float census does. Also fixed after pilot 1: the winding of a loop that does not turn one way was reported by the half-open
ray count, which is a winding number only for a loop that turns one way; such loops now report the float angle sum (the Admiral
Cap's winding 0; this changed no check). The third pilot passed (FINAL ok). The first full run passed but wrote its per-plane data to /dev/null (the exec'd fans_law.py code reset the output name); the name was
fixed and the full run repeated: 389 solids, 40 s, FINAL ok. Logs: data/fans-nonconvex-pilot.log (third pilot), data/fans-nonconvex.log;
per-plane data: data/fans-nonconvex.json.

**Proposed text for Ch 4, replacing the last three sentences of the proposed text below (DICTO to place; the book is not edited here):**
> One rule holds for every solid, convex or not. A central plane holds a disc exactly when the edges in that plane that do not point at
> the centre include a closed loop that goes once round the centre, turning the same way at every corner, with no other such edge at
> any of its corners. For a convex solid this is the same as the plane cutting no face. The non-convex solids show each part of the
> rule at work. On ten planes of the Sunstar tetrahedral cluster, edges pointing at the centre break the loop. On the Admiral Cap's
> plane y = 0 the loop of three edges does not go round the centre. On the planes x ± y ± z = 0 of the Hexa and the Hexa-Key a loop
> goes round the centre, but further edges meet its corners. Faces cut elsewhere in the plane do not matter: the Hexa-Key's six
> dodecagon discs lie in planes that also cut eight faces. (Proof, study 2026-11-13-platonic-fans-law §4; exact on 91 solids,
> 4304 planes, no exceptions.)

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
