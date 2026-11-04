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
