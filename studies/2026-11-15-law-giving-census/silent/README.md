# Silent coincidences in the seed spaces of Wythoff polytopes (15 Nov 2026)

## Verdict

No unexplained over-determined silent coincidence was found in the interiors of any seed space. In 3D the enumeration is exact and
complete for every pair of harmonic degrees up to 16 (A3 up to 14), with all tones checked up to degree 30. Every over-determined
point found there is explained by extra symmetry: the Icosaxes (B3, c = (1, phi, 0), silent in degrees 4, 8 and 14, explained by
the regular icosahedra that make up its two half-orbits), and the A3 seeds with c1 = c3 (central symmetry, which silences every odd
degree). In 4D the orbit-space algebra gives exact impossibility results: no B4 orbit is silent in degrees 4, 6 and 8 together, no F4
orbit in 6, 8 and 12, no H4 orbit in 12, 20 and 24, and no D4 orbit in 4, 6 and 8. So there are no 9-designs from B4, 13-designs from
F4, 29-designs from H4 or 9-designs from D4. The 5-designs of D4 are all fixed by triality, so they are F4-symmetric and explained. Only one
thing is new and over-determined: two golden A4 edge members. These are permutations of (phi^2, phi^2, phi^2, phi, 0), silent in
degrees 5 and 7 (20 corners), and permutations of (phi^2, phi^2, 1, 1, 0), silent in degrees 3 and 6 (30 corners). Each has two
conditions on a one-parameter edge, and neither corner set has symmetry beyond A4 (order 120 exactly). For the second one, a numerical
continuation finds a curve of joint T3 = T6 zeros that runs from the edge point into the interior. In the 3-parameter seed space it
is therefore the place where a curve of the expected dimension meets an edge, which is still a codimension-one coincidence. For the
first one this was not settled. The two exact findings below the over-determined level are a unique B3 7-design orbit (48 points)
and a unique A4 5-design orbit (120 points, centrally symmetric). H3 has no 11-design orbit at all, interior or boundary (exact).

## Method

- **Silence as polynomial conditions.** T_k(v) = 0 holds exactly when every G-invariant harmonic polynomial of degree k vanishes at
  v. `scripts/hinv.py` builds the invariant harmonics exactly. The basic invariants are u_1 = |v|^2 and power sums over the orbit of
  a fundamental weight; their algebraic independence is checked by a nonzero Jacobian, and with the basic degrees they generate the
  invariant ring. The Laplacian is written exactly in u-coordinates (the metric is fitted by evaluation at rational seeds with
  consistency rows), and its kernel in each degree is computed. Each dimension equals N(k) - N(k-2). Silence in degree k is
  therefore dim_k conditions, not one.
- **3D (`scripts/three_d.py`).** For the interior (chart c3 = 1), every minimal system (two one-dimensional degrees, or one degree of
  dimension 2 or more) is eliminated by resultants in both variables, and the norm to Q is taken. Each pair of positive real roots is
  then either excluded (arb ball away from 0) or certified by a Krawczyk test. Common curves are found by gcd. Edges are handled by
  exact univariate roots over Q(sqrt D), with equal minimal polynomials and overlapping balls. Vertices are evaluated exactly.
  Extra zeros at a point are given exactly where proven: on the c1 = c3 line of A3 and on the edges. Otherwise they are interval
  "zero?" results; none occurred in the B3 and H3 interiors.
- **Over-determined** means the number of conditions vanishing (summed over degrees up to 30, or 24 in 4D) is larger than the
  dimension of the stratum (interior, facet, edge, vertex). For A-type seeds fixed by the diagram reversal, only even degrees are
  counted, and they are counted on the symmetric locus. The explanation checks are floats: the full symmetry order of the corner set,
  sub-orbits under index-2 subgroups, and candidate extra isometries (-I, diagram maps, B4 -> F4, D4 -> B4/F4).
- **4D (`scripts/four_d.py`, `ustruct.py`).** Exact Groebner bases in u-space (sympy) for the design hierarchy, and every
  three-condition interior system from low degrees, with real seeds found by Newton and certified by Krawczyk. On each design curve,
  every later degree is restricted exactly. Facets are handled by the 3D resultant method, and edges and vertices exactly.
- **Controls (`scripts/controls.py`, all ok).** The zonal formula for T_k over the orbit is an independent check: it vanishes in
  exactly the degrees without invariant harmonics, for all 8 groups, and it agrees with the zero degrees at every listed point (329
  points). The silent zonohedron is re-found: on B3 c = (1, 1, t), T4 = 0 at t = sqrt2 a* = 0.5417368097863..., exactly (its minimal
  polynomial divides the norm of (t^2/2 + sqrt2 t)^2 = 5/6). The Icosaxes is re-found: on B3 c = (1, t, 0), the exact common zero
  at t = phi is in degrees 4, 8 and 14 (not 6), and the sub-orbit symmetry order is 120. The method flags it as over-determined and
  explains it.

## Degrees that can be nonzero (invariant harmonics, dimension in brackets)

A3: 3, 4, 6, 7, 8, 9, 10, 11, 12(2), 13, 14, 15(2), 16(2), ...; B3: 4, 6, 8, 10, 12(2), 14, 16(2), ...; H3: 6, 10, 12, 16, 18, 20,
22, 24, 26, 28, 30(2); A4: 3, 4, 5, 6, 7, 8(2), 9(2), ...; B4: 4, 6, 8(2), 10, 12(3), 14(2), ...; D4: 4(2), 6, 8(3), 10(2), ...;
F4: 6, 8, 12(2), 14, 16, 18(2), 20(2), 22, 24(4) (none in 10); H4: 12, 20, 24, 30, 32, 36, 40, 42, 44, 48, ..., 60(3).
Note: F4 degree 12 and B4 degree 8 are two conditions each, so a 13-design from F4 or a 9-design from B4 needs 4 conditions on 3
parameters.

## Results table

| group | locus | seed / exact data | orbit | strength | over-determined? | prior art |
|---|---|---|---|---|---|---|
| B3 | T4 = T6 = 0, interior, **unique** (exact) | c ~ (1.176750, 0.413396, 1); c1/c3 root of 20x^12 - 360x^10 + 1716x^8 - 2968x^6 + 1989x^4 - 402x^2 + 6; c2/c3 degree 24 (data/three-B3.json) | 48 | 7 | no (T8 nonzero) | Hardin-Sloane list 48-point 7-designs; whether theirs is this orbit was not checked |
| B3 | Icosaxes, edge c = (1, phi, 0) | T4 = T8 = T14 = 0 exact | 24 | 5 | YES on its edge; explained (two regular icosahedra) | the control |
| B3 | other pairs up to 16 | 22 further interior points (pairs 4+10, 6+8, ..., single 12 and 16), all strength 3 or 5 | 48 | <= 5 | no | - |
| H3 | T6 = T10 = 0 | **none** in interior, on edges or at vertices (exact) | - | - | - | consistent with Hardin-Sloane (no 11-design below 70 points; 120 not icosahedral) |
| H3 | 9-designs (T6 = 0) | a curve in the interior; edge points t = 1.166734824... (nodes 0,2) and t = 0.829679397... (nodes 1,2), degree-12 minimal polynomials | 120 / 60 | 9 | no | Goethals-Seidel 1981 (icosahedral orbit designs; original not read) |
| A3 | pairs up to 14 | 108 interior points; the non-symmetric ones come in diagram pairs, strength 2 | 24 | 2 | no | - |
| A3 | c1 = c3 line | every odd degree vanishes (central symmetry); point (1, 1/phi, 1) also silent in 4, 8, 14 | 24 | 5 | yes, explained (B3 Icosaxes) | - |
| B4 | T4 = T6 = T8 = 0 | **impossible** (Groebner basis {1}, exact) | - | - | - | - |
| B4 | 7-design curve | u = (4, 5, z) (unit sphere), real for z in [6.5957, 6.6195] (sampled); ends on facets c1 = 0 and c2 = 0 (certified, 192 points); T10 = 0 only at z = 20/3, outside | 384 | 7 | no | not found in sources checked |
| F4 | T6 = T8 = T12 = 0 | **impossible** (exact) | - | - | - | - |
| F4 | 11-design curve | u = (120, 336, z), seeds exist (sampled z in [3156.53, 3157.47]) | 1152 | 11 | no | not found in sources checked |
| H4 | T12 = T20 = T24 = 0 | **impossible** (exact): no 29-design orbit | - | - | - | - |
| H4 | T12 = T20 = 0 line | u-line exact; **no real seed found** (300 Newton starts, numeric only) | - | - | open | GS81 1440-point 19-design (needs T12 only) |
| D4 | T4 = 0 (5-designs) | u = (4, 4, z): all sampled seeds have c0 = c2 = c3 (triality-fixed, so F4-symmetric) | 192 | 5 | the extra zeros (8, 10, 14, 16) are all explained by F4 symmetry | Liouville / Kempner (D4 roots 5-design) |
| D4 | T4 = T6 = T8 = 0 | **impossible** (exact); the unique 7-design u-point (4, 4, 5) has no real seed found (numeric) | - | - | - | - |
| A4 | T3 = T4 = T5 = 0 | unique u-point (0, 8/5, 0); seed c ~ (0.321803, 0.178197, 0.178197, 0.321803), certified | 120 | 5 | only through -I (odd degrees), explained | not checked |
| A4 | T3..T6 | impossible (exact) | - | - | - | - |
| A4 | golden edge, nodes (0,1) / (2,3), t = 1/phi | T5 = T7 = 0 exact; permutations of (phi^2, phi^2, phi^2, phi, 0) | 20 | 2 | **YES on its edge; NOT explained** by any isometry tested (symmetry order 120) | main-census lead |
| A4 | golden edge, nodes (0,2) / (1,3), t = phi | T3 = T6 = 0 exact; permutations of (phi^2, phi^2, 1, 1, 0) | 30 | 2 | **YES on its edge; NOT explained** by symmetry; on an interior T3 = T6 curve (numeric continuation) | main-census lead |
| B4 | edge (0,2), t = 1, and vertex 1 | T4 = T10 = 0 | 96 / 24 | 5 | yes, explained (F4 symmetry: 24-cell family) | GS81 (24-cell, F4) |

## Sources checked (free only)

- Hardin and Sloane, arXiv math/0207211 (abstract and existence table: 7-designs for N = 24, 30, 32, 34, >= 36; 9-designs for N =
  48, 50, 52, >= 54; 11-designs for N = 70, 72, >= 74). The full paper was not read, so its point sets were not compared with ours.
- de la Harpe, Pache and Venkov, arXiv math/0505510 (read). It reports Goethals-Seidel 1981 Section 5: every H4 orbit is an
  11-design, and one special orbit of size 1440 is a 19-design. It also reports Salikhov 1975: a weighted 19-cubature of size 720 (120
  vertices + 600 face centres of the 600-cell, two orbits), and Liouville / Kempner on D4 root designs.
- Goethals and Seidel 1981 (The Geometric Vein, pp. 203-218) and Salikhov 1975: originals not available free; known only through the
  secondary source above.
- Web search: "Goethals Seidel 1981 Cubature formulae polytopes spherical designs 600-cell 19-design".

## Not covered

- H4: the realizability of the T12 = T20 curve (numeric search found no seed; this is not a proof), the H4 facets, edges and vertices
  (so the 1440-point 19-design was not re-found here), and interior systems beyond the hierarchy.
- D4 and F4: the runs stopped during the interior systems; facets, edges and vertices were not covered. B4 facets were covered for
  degrees <= 6 and interior systems for degrees <= 10. A4 facets were covered for degrees <= 6 and interior systems for degrees <= 7.
- 4D interiors: only the design hierarchy and three-condition systems from low degrees. A general all-triples sweep was not done.
  "No real seed found" results are numeric. The sampled ranges of the curves are numeric, while their endpoints on facets are
  certified.
- The A4 T5 = T7 edge point: whether a curve of joint zeros passes through it was not settled.
- The explanation checks for 4D sub-orbit symmetry were not run (only isometries normalising G).

Files: `scripts/` (code), `data/` (JSON and logs). The data was produced by quick runs on a compute host; no queued jobs.
