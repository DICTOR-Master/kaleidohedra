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
