# The web of bonds of the keyed DICTONIC pair (2026-10-25)

## Question

In the keyed network (all keyed: Lotus Jewel Axes + Dodecaxes, paper #48 Theorem 3; app `goldenPieces(size, { pattern: 'allKeyed' })`, the DICTONIC keyed view), which pieces share a boundary region of positive area (a bond, the web of bonds of study 2026-10-25-web-of-bonds taken to non-convex pieces), and how does it compare with the golden pair's web at x = τ (Icosaxes + Unborn Axes)? Either (a) the same adjacency, with only the shared faces keyed, or (b) bonds born or lost through the Tricap dents.

## Answer: (a)

The web does not change. Each piece keeps the same 14 neighbours, bond for bond. Each of the 8 big–small hexagons becomes a **keyed hexagon**: the hexagon minus the Tricap's base (the central triangle, √3/4), plus the Tricap's 3 side faces. The Tricap is the one from #54 Part B (keyed = golden ∓ the same 8 Tricaps). Its side faces lie inside the Icosaxes and touch no other face, so no new contact appears: no Lotus–Lotus or Dodecaxes–Dodecaxes bond through the dents. The 6 squares of each piece do not change.

| piece | bonds | shared region | exact area | ≈ |
|---|---|---|---|---|
| Icosaxes (x = τ) | 8 × Unborn Axes | hexagon | (√3/16)(1 + 3√5) | 0.8344375529 |
| | 6 × Icosaxes | square | 1/2 | 0.5 |
| Unborn Axes (x = τ) | 8 × Icosaxes | hexagon | (√3/16)(1 + 3√5) | 0.8344375529 |
| | 6 × Unborn Axes | square | 1/(2φ²) | 0.1909830056 |
| **Lotus Jewel Axes** | 8 × Dodecaxes | keyed hexagon = hexagon − √3/4 + 3 · (tan 36°)/4 | 3√3/(8φ) + (3/4) tan 36° | 0.9463317470 |
| | 6 × Lotus Jewel Axes | square | 1/2 | 0.5 |
| **Dodecaxes** | 8 × Lotus Jewel Axes | keyed hexagon | 3√3/(8φ) + (3/4) tan 36° | 0.9463317470 |
| | 6 × Dodecaxes | square | 1/(2φ²) | 0.1909830056 |

tan 36° = √(5 − 2√5). The Tricap's side face has area (tan 36°)/4 ≈ 0.18164. The square areas lie in Q(√5). The hexagon areas lie in √3·Q(√5) + Q(√5)·tan 36°.

**Total area (the pieces fill space).** Each piece's surface equals the sum of its shared regions:
- Icosaxes: 3 + (√3/2)(1 + 3√5) ≈ 9.67550
- Unborn Axes: 3/φ² + (√3/2)(1 + 3√5) ≈ 7.82140
- Lotus Jewel Axes: 3 + 3√3/φ + 6 tan 36° ≈ 10.57065
- Dodecaxes: 3/φ² + 3√3/φ + 6 tan 36° ≈ 8.71655

Keying adds the same amount to both pieces: 8 · (3 side faces − base) = 6 tan 36° − 2√3 ≈ 0.89515.

## Method

The frame is #48's (icosahedron edge 1, lattice spacing φ, so the squares match study 2026-10-25-web-of-bonds at x = τ).

**Exact part.** `scripts/keyed_web_exact.py` runs in sympy and Q(√5) on dicto-big-brother. It reuses `../2026-10-23-shadow-forms/polar/keyed_polar_exact.py`, which supplies the exact Tricaps in the corrected, non-mirrored orientation, and requires that script's 15 checks to pass first.
- Each piece's boundary is written as a signed sum of convex polygons.
  - Lotus Jewel Axes: the Icosaxes faces, minus the 8 Tricap bases, plus the 8 × 3 side faces.
  - Dodecaxes: the Unborn Axes faces, minus the 8 Tricap bases, plus the 8 × 3 side faces.
- A bond is Σ s·s′ · area(a ∩ b) over polygons that lie in the same plane and face opposite ways. This sum is taken over every piece within reach of the central two.
- The golden pair goes through the same code as a control.

**Float part.** `scripts/app_dump.mjs` and `scripts/check_app.py` run on the Pi. They take the app's own keyed meshes (size 2), intersect the coplanar, oppositely facing mesh faces in floats, and compare the result with the closed forms.

## Checks: 16 PASS, 0 FAIL

- **Exact (14), `data/keyed-web-exact.txt`.**
  - Control: the golden web at x = τ equals the one in study 2026-10-25-web-of-bonds, and surface = Σ bonds for both pieces.
  - Validity: each Tricap base lies inside a hexagon of its piece, and no side face lies on another face of the piece.
  - Keyed web: 8 keyed hexagons + 6 squares for each piece and nothing else, surface = Σ bonds for both pieces.
  - Same adjacency as the golden web.
  - Surface difference 8(3 sides − base).
  - Closed forms.
- **App floats (2), `data/check-app.txt`.** For the central Lotus Jewel Axes and the central Dodecaxes: 8 keyed hexagons and 6 squares, with error ≤ 2.2e-16, and surface = Σ bonds.
