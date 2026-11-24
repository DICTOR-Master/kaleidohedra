# The RVCMG adapter pieces as Scutoid Frusta (24 November 2026)

DICTO · project V SF A (Vacuus, Scutoid Frusta, Aequus), row SF. RVCMG = Reversible Vertex-Coalescence Morphing Geometry, DICTO's
specification of 15 September 2026; the adapter pieces are its physical outcome in the Polyhedraverse app. The term "Scutoid Frusta" and
its definition are from study 2026-11-24-scutoid-frusta-enumeration (Decisions of 24 Nov).

> **Status box.** Study note, not published. All 16 pieces done in exact arithmetic (run FINAL ok, 23 checks ok). DICTO accepted (24 Nov)
> that these pieces are DEGENERATE Scutoid Frusta. The resolution remark (merged corner → Y-corner) is combinatorial only (LEAD 1).

## Result

**Theorem.** Each of the 16 RVCMG pieces (8 of version 2, 7 adapters of version 1, and the bare RD-Hemi) is a convex polyhedron with two
disjoint ends: the hexagon (n = 6) and the target polygon (m = 3, 4, 5 or 6; m = 4 for the RD-Hemi). Every vertex lies on an end, so the
number of Y-corners is **k = 0** in every piece. Every lateral face meets an end along an edge (condition 2 holds).

1. **Fifteen pieces are degenerate Scutoid Frusta.** For m < 6 the law k ≥ |n − m| fails (k = 0 < 6 − m), so the solid cannot be simple,
   and it is not: the side count drops from 6 to m **at the target end, through merged corners** (corners with four edges), never at
   Y-corners between the ends. In the bent-wall reading (one lateral face for each hexagon edge) exactly 6 − m target corners have four
   edges and every other corner has three. Each such corner is two hexagon corners coalesced: the Y-corner of a scutoid frustum has
   slid up its edge into the end. The regular-hexagon piece of version 1 (m = 6) is also degenerate in its flat faces (its four bent
   wall quadrilaterals are cut into triangles, corners of up to five edges), but in the bent reading it is a simple frustum.
2. **One piece is a true frustum:** Regular-Hexagon-to-U-Hex (version 2). Its six walls are flat trapezoids; it is simple and convex,
   type **SF 6-6-0**: the frustum of a regular hexagonal pyramid (both hexagons regular, aligned, centred: target corners at angles
   0, π/3, …, 5π/3 exactly). The law holds with k = 0 = |6 − 6|.

**Seen.** Hexagon at the bottom, target end on top; a gold ball marks each merged corner (four edges in the bent reading: a Y-corner sits
merged into the end). `renders/preview-sheet.jpg` shows all sixteen; one render per piece in `renders/`.

## Dates (Polyhedraverse git history)

| Date | What |
|---|---|
| 15 Sep 2026 | DICTO's RVCMG specification; the core library (stages 0–7); the version 1 adapters on the rhombic dodecahedron's hexagon ("to RD-H"), in order Triangle, Square, Pentagon, Golden rhombus, DI and DH kites, Regular hexagon; then real 3D solids, the convex-wall fix, the bare RD-Hemi, the hexagon rescaled to the rhombic dodecahedron's own size |
| 17 Sep 2026 | Version 2 (commit 2726f41): 8 adapters on a new regular hexagon ("to U-Hex"), version 1 archived. The same day the Regular-Hexagon-to-U-Hex piece was given its own neck height (commit fe598d3); this study uses the 2726f41 geometry |
| 23 Sep 2026 | RD-Hemi restored to the live registry |

Version 1 pieces are rebuilt from 2726f41 (archived code, the state at 2726f41^ unchanged), version 2 from 2726f41.

## The pieces

Every adapter is built the same way: the hexagon in the plane z = 0, the target polygon lifted to height h, and walls of triangles. A
target corner that owns two hexagon corners (their coalescence) gets a fan triangle on the hexagon edge between them; every other
hexagon edge gives a wall quadrilateral (two hexagon corners, two target corners), split by the app into two triangles.

- **Version 2 hexagon (U-Hex):** regular, edge = circumradius = √2/2; neck height h = 1/4.
- **Version 1 hexagon (RD-H):** the six corners of the rhombic dodecahedron (circumradius 1) in a plane through its centre: two corners
  at distance 1, four at √3/2; edges √3/2 (four) and 1 (the opposite pair); only four symmetries; h = √2/4.
- **Target faces:** equilateral triangle, square, regular pentagon and regular hexagon, all of edge 1; the golden rhombus (rhombic
  triacontahedron face); the rhombic dodecahedron's own rhombus (version 2 only); the kites of the deltoidal icositetrahedron (DI) and
  deltoidal hexecontahedron (DH). Rhombus and kite faces are the app's Catalan face 0, rebuilt exactly (checks below).
- **RD-Hemi (version 1 only):** half of the rhombic dodecahedron cut through its centre; ends = the hexagon and the one rhombus face
  disjoint from it (the crown).

## Exact verdict per piece

V = vertices. Type SF n-m-k from the flat solid. "Walls" = the m wall quadrilaterals: flat (planar, one face) or bent (two triangles).
Degree = most edges at one corner, flat solid / bent reading. Merged = target corners with four edges in the bent reading (RD-Hemi:
its own faces, all flat).
Laws: k ≥ |n − m| and k ≡ n + m (mod 2). All 16 are convex and meet condition 2.

| Piece | V | Type | Walls flat / bent | Degree | Merged | k ≥ \|n−m\| | parity | Simple |
|---|---|---|---|---|---|---|---|---|
| **Version 2 (U-Hex)** | | | | | | | | |
| Triangle | 9 | SF 6-3-0 | 3 / 0 | 4 / 4 | 3 | no | no | no |
| Square | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| Pentagon | 11 | SF 6-5-0 | 1 / 4 | 4 / 4 | 1 | no | no | no |
| Golden rhombus | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| RD-native rhombus | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| DI kite | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| DH kite | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| Regular hexagon | 12 | SF 6-6-0 | 6 / 0 | 3 / 3 | 0 | yes | yes | **yes: a frustum** |
| **Version 1 (RD-H)** | | | | | | | | |
| Triangle | 9 | SF 6-3-0 | 1 / 2 | 6 / 4 | 3 | no | no | no |
| Square | 10 | SF 6-4-0 | 2 / 2 | 4 / 4 | 2 | no | yes | no |
| Pentagon | 11 | SF 6-5-0 | 1 / 4 | 4 / 4 | 1 | no | no | no |
| Golden rhombus | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| DI kite | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| DH kite | 10 | SF 6-4-0 | 0 / 4 | 5 / 4 | 2 | no | yes | no |
| Regular hexagon | 12 | SF 6-6-0 | 2 / 4 | 5 / 3 | 0 | yes | yes | no (bent reading: yes) |
| RD-Hemi | 10 | SF 6-4-0 | 4 rhombi, 2 triangles (all flat) | 4 | 2 | no | yes | no |

Version 2 target corners, exact (proved): triangle −π/2, π/6, 5π/6; square 0, π/2, π, −π/2; pentagon π/30, 13π/30, 5π/6, −23π/30,
−11π/30; hexagon kπ/3. Version 1 phases come out in closed form for the triangle (−7π/12 or −11π/12, + ½·atan(√2/4)), pentagon (−17π/20 or −21π/20,
+ ½·atan(√2/4)) and regular hexagon (−π/2 or −5π/6, − atan(√2/2)); two values each, because a hexagon corner at angle π may be read as
+π or −π, and both candidates are built (the one matching the app is kept):
the fit is mirror-symmetric, so the phase is an input angle minus a corner angle (proved by an exact zero test).

**Why the parity law fails for odd m but the bound fails for all m < 6.** With k = 0 the bound needs m = 6; parity needs m even. Both
laws assume three edges at every corner; here the merged corners carry the missing Y-corners. Resolving each merged corner into an end
corner plus one Y-corner just below the end would give 6 − m Y-corners, type SF 6-m-(6−m), which meets the bound with equality and the
parity law (a combinatorial remark; LEAD 1).

## Summary

The RVCMG pieces change a hexagon into a triangle, square, pentagon, rhombus or kite in one short neck. They are Scutoid Frusta of the
degenerate kind: no corner sits between the two ends; the hexagon loses its extra corners by merging them pairwise into the target's
corners, right at the target end. Every piece is convex. Only the version 2 hexagon-to-hexagon piece is a plain frustum.

## Method and checks

`scripts/rvcmg_exact.py` rebuilds each piece in exact arithmetic (SymPy), following the app's own formulas (target angle assignment,
least-error polygon fit, Catalan face measurements, the version 1 square's edge alignment), takes the face lists from the app's output
(`data/app_pieces.json`, `data/app_hemi_rd.json`, written by `scripts/dump.ts`, `dump2.ts` at commit 2726f41) and checks the exact model
against the app's vertices: all pairwise distances agree to 3e-14 or better and the handedness agrees, for all 15 adapters; the RD-Hemi
is rational and exact (error 0). Catalan faces: exact = app to 3e-14 and planar exactly (4 checks). Every sign (convexity, face
planes) is read from a rigorous ball (python-flint arb, F. Johansson's Arb library, 700-bit balls); a value is called zero only when
proved zero exactly (SymPy expansion, minimal polynomial (SymPy), or after rewriting every atan into nested square roots). 23 checks,
all ok; FINAL ok (`data/rvcmg_exact.log`). Results: `data/verdicts.json` (both readings for every piece), `data/exact_pieces.json`
(exact vertices; the two DH-kite pieces record coordinates to 60 digits, as their exact expressions are too long to print; the exact
form is the construction in the script), `data/pieces/` (one file per piece; the run resumes from these).

Fixes made on 24 Nov while finishing the run (recorded per the run log): (1) resume per piece and parallel pieces; (2) SymPy's own
atan2 became a complex logarithm form when it could not prove its arguments real, and the DH kite (version 1) crashed ("cannot
convert complex to float"): atan2 is now atan(y/x) ± π or ±π/2 − atan(x/y), with the branch read from arb balls, real by construction;
(3) the version 1 triangle and pentagon needed a zero proved for a flat wall: done by the closed-form phase above; (4) SymPy's
numerical evaluation and automatic simplification stalled on the DH kite (over 2 hours): numbers now come from arb balls, long
angles keep unevaluated sine and cosine, and the fit cost (used only to rank the four assignments) is numeric. A clean rerun of all 16
pieces with the final script reproduced the first-run verdicts of all 13 pieces that had finished before, exactly.

Renders: `scripts/pieces_render.py` (house renderer of study 2026-11-21-scutoid-stand-in, coordinates from `data/exact_pieces.json`),
frames by that study's `shots.mjs` (Playwright), sheet by `scripts/compose.py`. Clean exact renders, no photos.

## Sources checked

Polyhedraverse `docs/rvcmg-adapter-pieces-spec.md` and `docs/RVCMG.md` (DICTO's specification and the build record), its git history,
and `app/lib/rvcmg/solid.ts` at 2726f41; study 2026-11-24-scutoid-frusta-enumeration (definition, law, Decisions). "Scutoid" as a term:
Gómez-Gálvez et al., Nat. Commun. 9, 2960 (2018). No literature search for hexagon-to-polygon adapter solids was made here.

## LEADS

1. Resolve each merged corner into a Y-corner just below the target end and check, exactly, that a convex simple SF 6-m-(6−m) results
   (it would place every RVCMG piece next to a type in the enumeration).
2. Which of the 45 enumerated convex types (n, m ≤ 8, k ≤ 2) are those resolutions? (m = 4 and m = 5 give k = 2 and 1.)
3. The Regular-Hexagon-to-U-Hex neck height changed after 2726f41 (fe598d3): rerun that one piece at the new height (the verdict cannot
   change: still a frustum).
