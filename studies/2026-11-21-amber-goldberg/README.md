# Amber cells on Goldberg cores (21 Nov 2026)

Study 3 of DICTO's scutoid thread: an infinite family of cores for DICTO's combined method ("fill the ends in 2D, then cut the resin
to fit"), to look for an integer sequence. Method, Fullerene Star and Fullerene-Amber Cell: DICTO's. Goldberg polyhedra: Goldberg (1937).

## Result

152 runs: GP(m,n) for every m >= n >= 0 with T <= 100 (38 cores, from GP(1,0) = dodecahedron to GP(10,0)), two forms, bcc mould at
s0 and 6/5 s0. 107 runs valid, all checks passed (logs/summary.txt ends FINAL ok; the long job log logs/amber-goldberg.log too).

- **No Y vertex and no scutoid in any valid run** (Y = 0, scutoids = 0 in all 107). Every piece is a frustum-like piece whose
  core-side and mould-side neighbours agree. The scutoid count along the family is the zero sequence: no integer sequence arises.
- **6/5 s0: valid for every member in both forms** (76/76).
- **s0, insphere form: valid exactly when m ≢ n (mod 3)** (23 of 38; all 15 with m ≡ n (mod 3) fail: self-intersecting pieces,
  one collinear wall). m ≡ n (mod 3) is exactly when a hexagon (pentagon never; T=1 has m-n=1) sits on each 3-fold axis; at s0 these
  8 faces lie on the mould's 8 hexagons (seen as "faces on the mould 8" in the logs), leaving zero resin over them.
- **s0, canonical form: valid only for GP(k,0) with k ≢ 0 (mod 3)** (k = 1, 2, 4, 5, 7, 8, 10); all others fail (walls that cannot be
  triangulated, or self-intersecting pieces).
- Kinds at 6/5 s0 (congruence classes of pieces) depend on the form, so they are not a clean invariant:
  GP(k,0), k = 1..10: insphere 1, 3, 6, 8, 11, 16, 20, 25, 31, 36; canonical 1, 3, 6, 9, 12, 17, 21, 26, 32, 38.
  The face-orbit counts under T_h (combinatorial, not from the method) are 1, 3, 6, 9, 13, 19, 24, 31, 39, 47; kinds can be smaller
  because pieces in different orbits can be congruent (float test 1e-7, volume 1e-9), and for chiral cores pieces from different
  T-orbits can be mirror images (e.g. GP(2,1): 6 T-orbits, 5 kinds).

Full table: logs/summary.txt (form, GP(m,n), T, faces, face orbits, same-kind edges on 2-fold axes, faces centred on 2-fold axes, s,
valid, kinds, scutoids, Y, reason when not valid).

## Family and realisation

- GP(m,n), m >= n >= 0, m >= 1: the Goldberg polyhedra (M. Goldberg, *A class of multi-symmetric polyhedra*, Tôhoku Math. J. 43 (1937)
  104-108): 12 pentagons, 10(T-1) hexagons, T = m² + mn + n², all vertices 3-valent, icosahedral (chiral for 0 < n < m).
  Built by the Goldberg-Coxeter subdivision of the icosahedron cyc(0, ±1, ±φ) (lattice triangle 0, m e1 + n e2, turned 60°),
  points projected onto the unit sphere (the geodesic sphere, 10T + 2 points), then:
- **Form 1, insphere form (main, label GP)**: the polar of the geodesic sphere. Face i is the plane p_i · x = 1, tangent to the unit
  sphere at the geodesic point p_i. Planar by construction; vertices at 60 digits.
- **Form 2, canonical form (label GPc)**: every edge tangent to the unit sphere (Gauss-Newton on the face planes from form 1,
  minimum-norm steps, symmetry kept; tangency residual below 1e-15; each tangency point checked inside its edge). Planar by
  construction. Control: canonical GP(1,1) has all edges equal (0.412022659167), i.e. it is the Archimedean truncated icosahedron.
- Both forms checked at 60 digits: 10T + 2 faces, 20T vertices, every vertex on exactly 3 face planes and strictly inside all others
  (convex, simple), 12 pentagons at the 5-fold axes, Euler 2.
- Orientation: 2-fold axes on the coordinate axes, so T_h (T for chiral members) is a symmetry of core + mould.

## Setting and method

- bcc lattice, mould = truncated octahedron (Voronoi cell), core at every lattice point; s0 = smallest scale with the core inside
  the mould; runs at s0 and 6/5 s0. Seeds = face centroids.
- `scripts/amber.py` is a byte-identical copy of the amber-cell sweep's amber.py (sha256 d1bafbdb...). Goldberg coordinates are not
  in Q(√5), so `scripts/resin.py` replaces the exact field by 60-digit reals: sign 0 when |x| < 1e-40, vertex identity by rounding to
  25 digits. Every "exact" test of the sweep is therefore a 60-digit test with tolerance 1e-40 here (volume gaps are about 1e-59).
  For chiral cores the symmetry group used for orbits is T (12 rotations).
- Checks on every valid run (unchanged from the sweep): each piece a closed oriented embedded 2-manifold, positive volume; wall
  triangles cancel in pairs; volumes add to mould − core (gap < 1e-40); independent winding-number sampling (0 miscounted).
- Kinds = congruence classes of pieces (proper or improper isometry, float 1e-7). Scutoid = piece with a Y vertex whose
  neighbours on the core side and on the mould side differ.

## Why no Y vertex appears

In the insphere form the core's face pattern is exactly the 3D Voronoi pattern of the tangent points p_i: all have |p_i| = 1, so every
bisector plane passes through the centre and the Voronoi cell of p_i is the cone from the centre over face i. With the p_i as seeds the
outer pattern would be the central projection of the inner one for every T and every mould: no swap, no Y, no scutoid. The centroids
lie close to the p_i, and every vertex is 3-valent (no near-tie of four seeds), so the outer pattern keeps the inner adjacency. The
canonical form behaves the same. In the sweep, scutoids came from cores whose large faces meet small ones (the Fullerene Star's
spike triangles, C2's triangles, the truncated dodecahedron's triangles): there the centroid pattern differs from the face pattern.
So the sweep's rule needs that condition: Goldberg cores have 30 same-kind edges on 2-fold axes (hexagon-hexagon; pentagon-pentagon
for T = 1) whenever m, n are not both even, yet give no Y vertex.

## Sequence and OEIS

No sequence from the method: Y and scutoid counts are 0 for every member. Searched on oeis.org by terms (21 Nov 2026):
- kinds along GP(k,0), insphere form, 1, 3, 6, 8, 11, 16, 20, 25, 31, 36: not found (and form-dependent, so not a candidate).
- face-orbit counts under T_h along GP(k,0), 1, 3, 6, 9, 13, 19, 24, 31, 39, 47: the terms match A394684 (ordered pairs (x, y),
  0 <= x <= y, x² + y² < n²), a different definition; whether this is more than a coincidence was not examined, and the count is
  combinatorial (Burnside on the faces), not a result of the amber method.
No OEIS draft (one draft open at a time).

## Files

- scripts/solids.py (both forms), scripts/resin.py (60-digit field), scripts/amber.py (unchanged copy), scripts/cases.py,
  scripts/run_cases.sh, scripts/summary.py (table + combinatorial counts; ends FINAL ok).
- data/amber_*.json.gz (one per run, gzipped after the job; summary.py reads both), logs/run_*.log, logs/summary.txt, logs/amber-goldberg.log (the long job).
