# The hollow DICTO-ICOSA star: how the core is held (DICTO, 2026-10-15)

DICTO: "check the hollow first", then "couldn't it be held in place better by Cleo-Icos ... points on faces".

**As built (2026-10-12, scripts/build-dodeca-data.py):** the centre icosidodecahedron (edge 1) removed, a pyramid with all edges 1
pointing inward on each of its 32 faces, and a core icosahedron with its corners on the 12 pentagonal-pyramid tips (`scripts/hollow.py`).
- The 32 inward pyramids never overlap (496 pairs, separating axes); none cuts the core.
- The core is regular, edge exactly 2/√5, corners at √((5+√5)/10) = 0.850651.
- The 20 inward tetrahedra stop 0.019053 short of the core's faces (φ²/√3 − √(2/3) − φ²/√15): the core touches only at its 12 corners.
- It is loose: turned about a 5-, 3- or 2-fold or a random axis it first touches anything at 13.7°, 14.3°, 13.45° and 13.5°
  (`data/tips_hold_turning.txt`).

**DICTO's Cleo-Ico hold:** the 12 inward pentagonal pyramids and 20 tetrahedra replaced by 20 Cleo-Icos (an edge-1 icosahedron's
face pyramids from its centre) standing on the icosidodecahedron's triangles, points inward (`scripts/cleo_hold.py`, `data/cleo_hold.txt`).
- Exact fit: the triangles lie at φ²/√3 and a Cleo-Ico is φ²/(2√3) tall, so its point is at φ²/(2√3), the inradius of an icosahedron of
  **edge 1**: the core is the same edge as every other piece, and all 20 points sit on its 20 face centres (to 1e-16).
- No overlaps: the Cleo-Icos meet one another only at the shell's corners (190 pairs) and the core only at the 20 points.
- **Locked:** every one of 303 turn axes collides at 0.5°, 1° and 2°, and every one of 303 shift directions at 0.001. The lock is a
  point contact, so a turn presses in only as the square of the angle (depth 2.9e-5 at 0.5°); a shift presses in at once.
- The core's corners reach 0.951057 and stop 0.425325 short of the 12 pentagonal windows, which are now open.
- Volumes: shell (45 + 17√5)/6 = 13.835526; core and the 20 Cleo-Icos 2.181695 each (the holders are a second edge-1 icosahedron, cut
  into its 20 face pyramids); empty exactly 5 + 2√5 = 9.472136.

Renders (`renders/`, `scripts/render.html` + `shoot.mjs` on dicto-node): closed in the glass shell, cut in half, shell removed, pulled apart.
Status: a study; the app's hollow view still shows the 2026-10-12 version. Not claimed; no prior-art search yet.

**In the app (DICTO 2026-10-15, "Cleo-Icos + 12 flat pyramids"):** the hollow view now holds the edge-1 core with the 20 Cleo-Icos
on its face centres and 12 flat pentagonal pyramids on its corners (base the pentagonal window, height 0.425325, side edges 0.951057,
the Cleo-Ico's own side length, so its side triangles are the Cleo-Ico's). 217 pieces (scripts/build-dodeca-data.py).

**Cleo core step 1 (docs/PLAN-CLEO-CORE.md; `scripts/core_step1.py`, `data/core_step1.txt`):** the hollow is exactly the edge-1 core +
12 flat pentagonal pyramids + 20 triangular antiprisms: volumes add up to 1.8e-15, no overlaps among the 33, 16 159 sampled points each
covered once, and all 60 pyramid–antiprism contacts are whole faces. Each antiprism is two edge-1 triangles 0.755761 apart joined by six
triangles of sides 1, 0.951057, 0.951057, again the Cleo-Ico's side triangle; each holds one outer Cleo-Ico. Next: step 2, cut the
antiprism around its Cleo-Ico.

**The core as 20 Cleo-Icos too (DICTO 2026-10-15; `scripts/cleo40.py`, `data/cleo40.txt`, run inside the real DICTO-Star):** the hollow
then holds 40 identical Cleo-Icos, 20 meeting at the centre and 20 on the shell's triangles, point to base along each three-fold axis. No
overlaps among the 40 or with the 12 dodecahedra and 20 J63s; every outer point on its inner partner's base centre (to 2e-16). Each
loose piece on its own is locked: 0 of 1200 small shifts and 0 of 1200 one-degree turns are free, for the inner and the outer pieces alike.
Left empty: 5 + 2√5 (now filled in the app by the 12 flat pentagonal pyramids and, in the Cleo core project, by the antiprisms' remainders).

**X-ray check in the app (`scripts/xray.mjs`, `renders/app-xray-5fold.jpg`):** X-ray, 5-fold axis, cut through the centre, seen from the
cut side: the gold core with the violet Cleo-Icos round it. Two things a user meets: the cut shows only when the camera is on the cut
side (Flip turns it round), and faces that touch whole-face show speckles in the cut (coincident faces); a later polish.

**Cleo core step 2 (`scripts/core_step2.py`, `core_step2b.py`, `data/core_step2.txt`):** each antiprism is exactly its Cleo-Ico + 3 tetrahedra
X on its top (shell) edges + 3 tetrahedra Y on its bottom (core) edges. X: edges 1, four of 0.951057, 0.57735 (= 1/√3); Y: edges 1, three of
0.951057, two of 0.57735. Volumes Cleo-Ico : X : Y = 3 : 2 : 1 (0.109085, 0.072723, 0.036362); an antiprism is exactly 4 Cleo-Ico volumes.
The predicted 12 + 30 + 20 shell (Karma pattern) does NOT appear: the Y pairs over the 30 core edges are not convex, nor the flat pyramids
with their 5 X, nor any X + Y inside an antiprism. None of the pieces is a kit piece (AXE, FUJI, CLEO, ...) or J2 or a regular tetrahedron
by shape. The 1/√3 lengths (triangle centres) are what keep them out of the golden kit.

**Cleo core to the DICTO Hecatodihedron (DICTO 2026-10-15, "new standalone object"; `scripts/cleo_heca.py`, `heca_bipyr.py`, `data/`):** our
step (edge-1 core in the icosidodecahedron of edge 1; Dharma's own first step has the core 1/1.309 as large) followed by the Spheres of
Dharma layers scaled by 2/φ (20 triangular pyramids to the dodecahedron, 12 twisted pentagonal frusta + 30 t1 to the truncated icosahedron,
20 caps to the Hecatodihedron). 235 pieces, no overlaps (6956 nearby pairs; Dharma's data is stored to 6 places). Convex fusions of
face-sharing pairs: Cleo-Ico + triangular pyramid (20, a symmetric triangular bipyramid from a core face to a dodecahedron corner, edges
1/φ, 0.9511, 0.9763, 1), Cleo-Ico + one X (60 options, breaks symmetry), t1 + frustum (24 options, not enough t1 for all). DICTO chose the
bipyramids: 215 pieces; the hull is the Hecatodihedron, 102 faces (60 triangles, 30 rhombi, 12 pentagons), 80 corners; volumes agree to
1e-4 (data rounding). Renders `renders/heca-*.jpg`.

**Down to 102 pieces? (DICTO 2026-10-15; `scripts/f102.py`):** the pieces come in symmetry sets of 1, 12, 20, 30 and 60. With the core split
into its 20 Cleo-Icos, exactly one grouping reaches the Hecatodihedron's 102: 20 (inner Cleo-Ico + its 3 Y) + 20 (bipyramid + its 3 X) +
20 caps + 12 (flat pentagonal pyramid + the frustum on its axis) + 30 t1 = 102. The count works, but none of the three fused kinds is
convex: inner Cleo-Ico + 3 Y, bipyramid + 3 X, flat pyramid + frustum (also bipyramid + cap) all have dents. A set of 12 + 30 + 60 is
impossible while the 20 bipyramids stay whole (20 does not divide into sets of 12, 30 or 60).
