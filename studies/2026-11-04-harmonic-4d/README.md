# Harmonic fingerprint in four dimensions (2026-11-04) — DICTO: "can the harmonics test a whole 4D structure, 600-cell etc"
Corner directions on the 3-sphere; Q_l² = mean over pairs of U_l(u_i·u_j)/(l+1) (U_l Chebyshev of the 2nd kind = zonal harmonic on S³).
Calibration (classical spherical designs): 5-cell silent at l = 2 only; 16-cell and tesseract silent through l = 3; 24-cell silent through l = 5 (and at 10);
600-cell (120 corners) silent at every l from 1 to 11, first tone at 12 (Q12 = 0.277) — the 600-cell / White Queen is a spherical 11-design. All as known.
#91's 4D sweep S(μ) = K ∩ μK* (tesseract cut by the 16-cell), exact with the B4-invariant harmonics:
- Q4 = 0 only at μ = 2, the 24-cell (fixed point of μ ↔ 4/μ; the 4D analogue of the 3D core turn's fixed point √3).
- Q6 = 0 exactly at μ = √2 and μ = 1 + √3. No zero at the All-Golden stations φ² and 2 + 1/φ² — their golden content lives in the cells, not in the corner set, so it is outside this test's competence.
LEADS: fingerprint the 600-cell's slices and the Queens' paths (#62, #63, #76); the 120-cell (also an 11-design); 4D isoperimetric maximum of the sweep (is it μ = 2?).

## 600-cell slices (4 Nov) — scripts/slices600.py, slices600.json (heights h for circumradius 1; grid 1201 heights; zeros located to ~0.002, not yet exact)
- Corner-first: every slice is icosahedral, so Q4 and Q8 are always silent (as they must be). Q6 falls silent at |h| ≈ 0.128, 0.396, 0.638:
  slices that sound only from degree 10 up ("deep icosahedral silence").
- Cell-first (tetrahedral slices): Q4 silent at |h| ≈ 0.157, 0.330, 0.583, 0.737; Q8 silent at |h| ≈ 0.137, 0.453, 0.829, 0.854 — never at the same height.
  So no cell-first slice hides icosahedral order the way Icosaxes does on the cube–octahedron sweep (there Q4 and Q8 vanish together).
LEADS: exact heights of these zeros; are the corner-first Q6-silent slices named solids in #62's atlas; edge-first and face-first directions; the 120-cell.

## Red Queen and the path between the Queens (4 Nov) — scripts/queens_path.py, queens-path.json
- 120-cell (600 corners): silent in degrees 2..11, first tone at 12 (Q12 0.087, Q20 0.106) — an 11-design like the 600-cell (calibration passes).
- Path S(μ) = 600-cell ∩ μ·120-cell, μ from r² ≈ 0.8567 to 1 (r = 600-cell inradius 0.92562): degrees 1..11 silent throughout (H4).
  PRELIMINARY (float; corners merged at 1e-5; one corner count, 1536, is not an H4 orbit sum and must be checked):
  Q12 dips to 0.008 near μ ≈ 0.925 (close to r = 0.9256); Q20 dips to 0.001 near μ ≈ 0.887 (3600 corners) and 0.007 near 0.955.
  Exact check needed before any claim of a "deep silence" station.

## Queens path, exact corners (4 Nov) — resolves the 1536 anomaly
For μ in ((1 + φ/2)/2, 1) = (0.904508, 1) the section is the 600-cell with its 120 corners cut: 1440 corners, exactly the points
v + s(w − v) on the 1440 directed edges, s = (1 − μ)/(1 − φ/2). (The hull routine had produced 1536 because every corner lies on 6 walls.)
- Q12 = 0 at μ* ≈ 0.924165 (Q 9e-5 on a 400-point scan): with H4 symmetry every degree 1..11 and 13..19 is silent (no H4 harmonics there),
  so these 1440 points would form a spherical 19-design — the deepest silence on the path. LIKELY KNOWN: H4 orbits tuned to kill the degree-12
  invariant are the classical route to 19-designs (Goethals–Seidel 1981, Sobolev's theorem; Hardin–Sloane) — to check and credit.
- Q20 = 0 near μ ≈ 0.9540 (Q12 ≠ 0 there).
- Earlier "1536"-based dips are superseded by these values. Exact μ* (root in Q(√5)?) still to compute.
CREDIT (4 Nov, checked): the 19-design is the classical construction — an orbit of the reflection group W(H4) through a suitable point on S³ is a spherical 19-design
(Bannai's survey of spherical designs; Goethals & Seidel, "Cubature formulae, polytopes, and spherical designs", 1981). Our 1440 points are the W(H4) orbit of a point on a
600-cell edge (stabiliser of order 10, orbit 14400/10 = 1440). What is ours: that this design is a station of the path between the Queens, the truncated 600-cell at μ ≈ 0.92417.
