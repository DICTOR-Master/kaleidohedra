# Gap "Archimedean stretches (#49)": every equal-edged solid of the three permutohedron cones (12 Nov 2026)

**Conclusion.** Inside the deformation cones of the truncated octahedron (A3), truncated cuboctahedron (B3) and truncated
icosidodecahedron (H3) the equal-edged solids are a finite, exact list (17, 101 and 4427 solids up to symmetry). #49's theorem covers every
member with a segment summand, and its caps corollary covers those with a triangle or tetrahedron summand. The rest is new to #49: 2 indecomposable solids in A3/B3 and
367 in H3 (with 54 sums of them and 13 pentagon caps). Within these cones the only Platonic or Archimedean solids that can be stretched along a cone direction are the
tetrahedron, octahedron, cuboctahedron, truncated tetrahedron and truncated octahedron (B3, along the cube axes). No H3 solid can.

Status: listing done for these three cones. Prior art: none found for the 367 + 2 new atoms. One lead to check: Subbotin's RR-polyhedra.

## Question and route (DICTO approved the permutohedron route)
#49 (The Polyhedral Stretching Theorem) proves that sliding any equal-edged solid one edge-length gives an equal-edged solid, and leaves
open which stretches of the Archimedean solids are known or new. The truncated octahedron is the A3 permutohedron; the truncated
cuboctahedron and truncated icosidodecahedron are the B3 and H3 Coxeter permutohedra. The polytopes whose normal fan coarsens the
Coxeter fan form the deformation cone of the permutohedron. That theory belongs to **Postnikov** (generalized permutohedra, 2009) and
**Ardila, Castillo, Eur and Postnikov** (Coxeter generalized permutohedra, 2020); we use it and do not claim it. Describing deformations
through edge lengths goes back to **Shephard** and **McMullen**.

## Method (exact)
- **Reduction.** On the closed cone every edge length is a *linear* form l_e(h) in the cone parameters (wall-crossing forms). An edge of a
  member is a union of walls of the Coxeter fan, and every wall in it carries that edge's length; all other walls carry 0. So "all edges
  equal (= 1)" is the polynomial system l_e(h)(l_e(h) − 1) = 0 on every wall. Its solutions are exactly the 0/1 wall labellings
  that close around every face. Solving the system exactly therefore means enumerating a finite 0/1 constraint problem. No floating point decides anything.
- `scripts/coxeter.py`: the fans exactly, over Q(√2) (A3, B3) and Q(√5) (H3), with own field arithmetic. `scripts/gp_setup.py`: ranks and
  per-face closed labellings. `scripts/gp_enum.c`: complete enumeration with one representative per orbit (least image under the
  symmetry group, 48 or 120). It also counts sub-members, which identifies the atoms. `scripts/gp_analyse.py`: rebuilds every representative exactly from its
  labels and finds faces from exact support values. It checks every edge (squared length exactly 1) and Euler's formula, then finds face kinds, segment
  summands, the core and an exact split into atoms. `scripts/gp_tables.py`: cyclic corner configurations (Johnson ortho/gyro names) and the tables.
- Run on the compute machine through the job gate: pilot 1 (setup + enumeration, 35 s), pilot 2 (analysis), main run (2 min, 8 cores), tables. All ended FINAL ok
  (`data/gpee-*.log`). Setup: 46/46 checks. Analysis: 50/50. Tables: 1/1.

## Checks
- Fans: Coxeter matrices, |W| = 24, 48, 120, Euler on the permutohedra. The map h → l has rank R − 3 (11, 23, 59 = cone dimensions). The face
  closures hold on every h (K·L = 0) and cut out exactly that space (closure-space dimension = R − 3), so local closure is the full
  condition.
- Positive controls: a generic permutohedron has every wall length > 0. All 7 Wythoff solids of each group, built independently, are found and named correctly.
  #49's own shapes are found: tetrahedron with four caps = cuboctahedron, octahedron with four caps = truncated tetrahedron, three caps =
  J3, octahedron stretched through a corner = J15, the stretched cube (hexagonal prism). The truncated octahedron stretched along a four-fold axis is also found.
  Every A3 solid reappears in B3 (B3's fan refines A3's).
- Negative controls (fail the cone inequalities): cube in A3 (12 of 36 wall lengths < 0); rhombic dodecahedron in B3 (24 of 72); #49's
  dodecahedron stretched along a five-fold axis in H3 (30 of 180), while the dodecahedron itself passes.
- Congruence: two B3 orbit pairs share a distance invariant: the cube, and the cube stretched along a face diagonal, each built along
  two different sets of axes. They were proved congruent exactly and counted once (103 orbits = 101 solids). All other invariants are distinct.

## Results

| | A3 (truncated octahedron) | B3 (truncated cuboctahedron) | H3 (truncated icosidodecahedron) |
|---|---|---|---|
| equal-edged members (all positions up to translation) | 162 | 1296 | 390 970 |
| of which solids | 128 | 1223 | 390 711 |
| solids up to symmetry | 17 | 101 (103 orbits) | 4427 |
| regular-faced (known) | 7 | 18 | 23 |
| zonohedra (sums of segments) | 5 | 43 | 675 |
| stretch of a Platonic/Archimedean solid | 0 | 8 | 0 |
| other #49 stretches (segment summand) | 3 | 32 | 3137 |
| #49 caps (triangle or tetrahedron summand) | 0 | 0 | 158 |
| pentagon caps (regular pentagon summand) | – | – | 13 |
| **new atoms** (no equal-edged summand, not regular-faced) | 2 | 2 (the same two) | **367** |
| **sums of atoms** with no segment, polygon or tetrahedron summand | 0 | 0 | 54 |

**Known solids found (exact names, ortho/gyro settled by cyclic corners):** all Platonic and non-snub Archimedean solids of each group
(16 kinds), cube and octagonal prism, pentagonal antiprism. Johnson solids: J1, J3, J4, J8, J15, J19, J28 (A3/B3); J2, J5, J6, J11, J31,
J32, J62, J63, J76, J80, J81, J83, J91 bilunabirotunda, J92 triangular hebesphenorotunda (H3).

**Stretches of Platonic and Archimedean solids (the gap's listing, within these cones).** Every stretch here runs along the cube axes (B3).
Faces are written as count and kind; "45/135" etc. are rhombus or hexagon angles.

| core | +1 axis | +2 axes | +3 axes |
|---|---|---|---|
| tetrahedron | B3-16: 4 triangles, 4 rhombi 45/135 (8 corners) | B3-32: 4 triangles, 4 rhombi, 2 hexagons 90/135 (12) | B3-58: 4 triangles, 6 hexagons 90/135 (16) |
| octahedron | J15 | J28 square orthobicupola | rhombicuboctahedron |
| cuboctahedron | B3-49: 8 triangles, 2 squares, 4 hexagons 90/135 (16) | B3-75: 8 triangles, 4 hexagons, 2 regular octagons (20) | truncated cube |
| truncated tetrahedron | B3-87 (20 corners) | B3-105 (28) | B3-112: 4 triangles, 12 squares, 6 hexagons 90/135, 4 regular hexagons (36) |
| truncated octahedron | B3-110 (32, zonohedron) | B3-114 (40, zonohedron) | truncated cuboctahedron |

Every other Platonic or Archimedean solid has an edge along every root direction of its cone, so any root-direction stretch doubles an
edge (the case #49's theorem excludes). #49's dodecahedron and icosahedron stretches run along five-fold, three-fold or face-diagonal
directions. Those are not roots, so they lie outside these cones (shown by the negative control).

**What the theorem already covers.** Every member with a segment summand is a #49 stretch, P ⊕ segment with P equal-edged. That is
3 + 40 + 3137 orbits here, plus the zonohedra. Every member with a triangle or tetrahedron summand is a #49 cap form (158). In these cones #49's
theorem extends with the same proof: **P ⊕ P′ is equal-edged exactly when P and P′ are equal-edged and no wall of the fan carries an
edge of both** (edge lengths add on the cone). This covers the pentagon caps and every sum of atoms.

**New (the goal of the gap).** The *atoms* are equal-edged members with no equal-edged Minkowski summand other than a point and themselves.
- A3 = B3: A3-10, the octahedron with a tetrahedron on one face (4 triangles, 3 rhombi 60/120, 7 corners). This shape is known (the 60° rhombohedron
  with one corner cut). A3-16 is a 13-corner solid on the octet lattice (4 triangles, 4 rhombi 60/120, 5 squares, 24 edges) that we did not find named; DICTO named it the **DICTO 13-Corner Octet Atom** (12 Nov 2026): a square cupola (J4) whose octagon is closed by four 60° rhombi meeting at one apex; not centrally symmetric (6 of 13 faces in parallel pairs). Render: figures/a3-16-render.png (scripts/render_a316.py, exact corners in the log).
- H3: 367 atoms, mostly pieces with regular triangles and pentagons together with rhombi of 36/144, 60/120 and 72/108 and hexagons of
  72/144 and 108/144 (e.g. H3-16: 5 triangles, 5 rhombi 36/144, 1 pentagon, 11 corners; H3-81: 10 triangles, 3 rhombi 72/108, 10
  corners). Full list: `data/raw/solids-H3.csv`, `data/raw/tables.json` (new_atoms), exact labels in `data/raw/members-H3.json`.

## Prior art (sources checked)
- DICTO's reference library: six ask-library queries (`data/raw/ask-library.txt`): generalized permutohedra / deformation cone /
  submodular; Coxeter permutohedron Minkowski summands; equal-edged convex polyhedra; Minkowski sum of an Archimedean solid and a
  segment; equilateral zonohedra; polyhedra with regular and rhombic faces. Hits were Fedorov 1885 ch. 13 (zonohedra), Grünbaum 2010
  (zones), Dutour Sikirić–Schürmann–Vallentin 2008, Garber 2019 and Erdahl 1999 (parallelohedra), Betke–Henk 2000, Torquato–Jiao 2009, Johnson 1966,
  Goldberg 1937 and Al-Siyabi–Koca–Koca 2020. None lists equal-edged members of these cones. Postnikov and Ardila et al. are not in the library.
- Web (12 Nov 2026), three searches: equilateral generalized permutohedra; enumeration of unit-edged polyhedra on icosahedral two-fold
  directions; Ardila–Castillo–Eur–Postnikov H3 edge lengths. Found: Postnikov 2009 (arXiv math/0507163), Ardila–Castillo–Eur–Postnikov 2020
  (arXiv 1904.11029), Castillo–Liu (nested braid fans, arXiv 1710.01899), Padrol–Pilaud–Poullot (deformed graphical zonotopes),
  indecomposability via edge dependencies (arXiv 2512.05307; Shephard, Kallay, Edmonds' question on rays of the submodular cone),
  Subbotin 2023 (convex RR-polyhedra: rhombic stars + regular faces, icosahedral; **may overlap some H3 atoms, to check**), Steven Dutch's
  polyhedron enumeration pages, the rhombic icosahedron, and edge-transitive polyhedra. No classification of equal-edged members was found.
- #49's own sources (Hart–Picciotto sums of tetrahedra, Baumann's near misses, Deza–Pournin, Erdahl–Grishukhin) are not repeated here.
  Their shapes lie in other directions.

## LEADS
1. Prior-art pass on the 367 H3 atoms and the 54 atom sums: Subbotin's RR-polyhedra first, then the Johnson near-miss lists. Then pick the
   cleanest few for DICTO to name and for figures.
2. A3-16 (13-corner octet solid): identify it, and test whether it fills space with octahedra and tetrahedra.
3. Other directions: a finer fan (H3 mirrors plus the planes through five-fold and three-fold axes) would bring #49's five-fold and
   body-diagonal stretches into one exact cone. Same method.
4. 4D: the same 0/1 reduction for the A4, B4, F4 and H4 permutohedra (equal-edged 4-polytopes; the H4 cone joins the Queens work).
5. Which members tile space alone (zonohedra among B3 members; the A3 atoms on the octet lattice).

## Files
`scripts/` (run: `bash scripts/run_main.sh data/raw`, then `python3 scripts/gp_tables.py data/raw`). Data in `data/raw/`:
representatives `*.reps` (hex 0/1 wall labels), `members-*.json` (exact analysis of every orbit), `solids-A3.md`, `solids-B3.md`,
`solids-*.csv` (full tables), `setup.json`, `summary.json`, `tables.json`. Logs in `data/`.
