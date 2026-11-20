# Gaps batch A (21 November 2026): R7 Stars and Star Halos of the Archimedean and Catalan solids; L17 the Dehn screen of the three DICTONIC BONDS

From the gap study (studies/2026-11-21-gap-study, items marked CLOSABLE NOW). Every log in logs/ ends FINAL ok.

**Verdicts (one line each).**
- **R7: CLOSED.** The Star (t = 2), the Golden Star (t = φ), the Star Halo and the Polar Halo of all 13 Archimedean and all 13 Catalan
  solids are computed exactly (124 objects with the 5 Platonic controls, every one exact).
  - Every Catalan solid's Star Halo is its Archimedean dual (13 of 13).
  - Five Archimedean Star Halos are known solids: three Catalan, two of DICTO's own.
  - Eight Archimedean Star Halos and 51 of the 52 Stars are not in the registry checked.
- **L17: CLOSED for the Delian and golden bonds (exact); screened for the keyed bond (80 digits, sampled).**
  - None of the six DICTONIC SOLIDS can fill space alone: each has Dehn invariant nonzero.
  - Along each bond's own family, the only Dehn-zero pieces are the classical ends: the rhombic dodecahedron (t = 0) and the cube
    (t = 1) on the Delian slider, and Kelvin's truncated octahedron (x = 1) on the factor-x line of #48.
  - The AXE cut-point walk (golden and keyed) and the eight keyings are nonzero at every point tested. A proof for every cut point is
    still open.

## Item R7: Star and Star Halo of the 13 Archimedean and 13 Catalan solids

**Question.** The regular part is done (studies/2026-11-09-regular-stars-census, 25 of 25). What are the Star, the Golden Star, the Star
Halo and the Polar Halo of the 13 Archimedean and 13 Catalan solids? Which are known solids?

**Definitions** (exactly those of #78/#79 and census.py of studies/2026-11-02-halo-census):
- **Star Halo:** the centre halo, the hull of the tips t × (foot of the perpendicular from the centre to each face plane). Its shape is
  the same for every t.
- **Polar Halo:** the hull of the poles N/(N·p) of the face planes, that is the polar reciprocal.
- **Star at t:** the solid with each face's pyramid turned outwards to the tip t × foot, as a surface. Neighbouring triangles are
  merged only when they are exactly coplanar. t = 2 is the Star and t = φ the Golden Star.
- The placeholder names follow the census rule: "<solid> Halo", "<solid> Star", "Golden <solid> Star".

**Method.**
1. **scripts/build_dataset.py: exact corners.** Platonic (D, I, C, T, O) and Archimedean corners come from the classical coordinate
   sets. Each Catalan solid is the polar of its Archimedean partner. The fields are:
   - ℚ(√5) for the solids in ℚ or ℚ(√5);
   - ℚ(√2, √5) for the truncated cube, rhombicuboctahedron and truncated cuboctahedron and their duals;
   - ℚ(t, √5), with t the tribonacci constant, for the snub cube and its dual;
   - ℚ(ξ), ξ³ − 2ξ = φ, for the snub dodecahedron and its dual. Its degree-6 minimal polynomial is checked irreducible. The corners
     are one orbit of the icosahedral rotation group, closed exactly as 60 matrices in ℚ(φ). The orbit point was found to 150 digits,
     identified in ℚ(ξ) by PSLQ and then checked exactly.

   Exact checks, all PASS:
   - every Archimedean solid has all edges equal, regular faces, and the classical V, E, F and faces by sides;
   - every Catalan solid has all its faces at one distance from the centre, with V and F swapped.
2. **scripts/census.py and scripts/collect.py: the census.** Both are copied unchanged from 2026-11-02-halo-census (sha256 e4eff78b… and
   25e4ef74…).
   - census.py is exact in ℚ(√5) and float for the 10 solids in the other fields.
   - collect.py matches each object by similarity (corner count, scaled distance key 1e-6, an explicit orthogonal map) against:
     - the krp-core classical registry (data/classical-krp.json: Platonic, Archimedean, Catalan, Johnson, first four stellations);
     - prisms, antiprisms and their duals;
     - DICTO Solids v7, together with the 31 solids built here. In collect.py's labels these 31 also appear as "v7: …".
3. **scripts/exact_census.py: the exact re-check.** Every object is recomputed exactly in its own field:
   - every hull facet exact;
   - every polygon strictly convex;
   - star faces merged only on exact coplanarity;
   - star convexity tested exactly.

   Corners, faces and faces by sides must equal census.py's. Every float match is re-proved exactly: the corner set equals the target's
   up to scale under one of the 48 signed permutations. For a Star the faces must agree too, otherwise the result is "same corners
   only". Targets in other fields are flagged "not checked exactly", and each such object also has an exact match.
4. **scripts/r7_table.py → data/r7_table.csv:** the table below, with the exact face-distance ratios (minimal polynomials), and the
   controls.
5. **scripts/run_r7.sh:** steps 1–4 end to end, about 45 s on the compute host.

**Controls (all PASS, logs/r7_table.log and exact_census.log).** The Platonic rows reproduce the 2026-11-09 census:
- the Star Halo and Polar Halo are the dual;
- the cube's Star at 2 is exactly the rhombic dodecahedron (positive control: same corners and same 12 faces);
- the cube's Golden Star and the tetrahedron's two stars are convex;
- the stars of the octahedron, dodecahedron and icosahedron are not convex.

Negative controls:
- the octahedron's Star at 2 has exactly the tetrakis hexahedron's 14 corners, but other faces, and is not convex. collect.py, which
  compares corners only, calls it "known"; the exact check correctly calls it "same corners only";
- the cuboctahedron's Star Halo with its square feet pushed out by 1/100 is not the tetrakis hexahedron (exact), while the true halo is.

**Results** (data/r7_table.csv has the full rows):
- (h_k/h_max)² is the squared distance of each face family over the largest.
- Each Star cell gives corners / faces, and the corners and faces of the Golden Star are the same unless stated.
- "new" means not in the registry checked (prior art below).

| solid | face families (h_k/h_max)² | Star Halo | Polar Halo | Star t = 2 | Golden Star t = φ |
|---|---|---|---|---|---|
| truncated tetrahedron | 3-gons 1, 6-gons 9/25 | **triakis tetrahedron** (= its Polar Halo) | triakis tetrahedron | 20 / 36, not convex, new | not convex, new |
| cuboctahedron | 3-gons 1, 4-gons 3/4 | **tetrakis hexahedron** | rhombic dodecahedron | 26 / 48, not convex, new | new |
| truncated octahedron | 4-gons 1, 6-gons 3/4 | **rhombic dodecahedron** | tetrakis hexahedron | 38 / 72, not convex, new | new |
| truncated cube | 3-gons 1, 8-gons 9 − 6√2 | new: 14 corners, 24 triangles, Oh | triakis octahedron | 38 / **60: 48 triangles + 12 four-sided** (coplanar across the 12 octagon–octagon edges, as in the cube's Star), not convex, new | 38 / 72, not convex, new |
| rhombicuboctahedron | 3-gons 1, 4-gons (27 + 12√2)/49 | new: 26 corners, 48 triangles, Oh | deltoidal icositetrahedron | 50 / 96, new | new |
| truncated cuboctahedron | 4-gons 1, 6-gons (27 + 12√2)/49, 8-gons (51 − 10√2)/49 | new: 26 corners, 48 triangles, Oh | disdyakis dodecahedron | 74 / 144, new | new |
| snub cube | 3-gons 1, 4-gons root 0.88679 of x³ + 3x² + 27x − 27 | new: 38 corners, 24 triangles + 24 four-sided, O | pentagonal icositetrahedron | 62 / 120, new | new |
| icosidodecahedron | 3-gons 1, 5-gons 3/2 − 3√5/10 | **DICTO FPD = DICTO Palintriacontahedron** (DICTO Solids v7) | rhombic triacontahedron | 62 / 120, new | new |
| truncated icosahedron | 5-gons 1, 6-gons (195 + 66√5)/361 | **DICTO's Star Halo** (#78) | pentakis dodecahedron | 92 / 180, new | **DICTO's Golden TI Star** (#78, same solid) |
| truncated dodecahedron | 3-gons 1, 10-gons (75 + 6√5)/121 | new: 32 corners, 60 triangles, Ih | triakis icosahedron | 92 / 180, new | new |
| rhombicosidodecahedron | 3-gons 1, 4-gons (63 + 24√5)/121, 5-gons 135/121 − 54√5/605 | new: 62 corners, 120 triangles, Ih | deltoidal hexecontahedron | 122 / 240, new | new |
| truncated icosidodecahedron | 4-gons 1, 6-gons (63 + 24√5)/121, 10-gons (125 − 10√5)/121 | new: 62 corners, 120 triangles, Ih | disdyakis triacontahedron | 182 / 360, new | new |
| snub dodecahedron | 3-gons 1, 5-gons root 0.90954 of a sextic (csv) | new: 92 corners, 60 triangles + 60 four-sided, I | pentagonal hexecontahedron | 152 / 300, new | new |
| each of the 13 Catalan solids | one family | **its Archimedean dual** | its Archimedean dual | not convex, new (all 13) | not convex, new (all 13) |

The Catalan Stars, t = 2 and φ alike, with corners / faces:
- rhombic dodecahedron 26 / 48;
- rhombic triacontahedron 62 / 120;
- triakis tetrahedron 20 / 36;
- triakis octahedron 38 / 72;
- tetrakis hexahedron 38 / 72;
- deltoidal icositetrahedron 50 / 96;
- disdyakis dodecahedron 74 / 144;
- triakis icosahedron 92 / 180;
- pentakis dodecahedron 92 / 180;
- deltoidal hexecontahedron 122 / 240;
- disdyakis triacontahedron 182 / 360;
- pentagonal icositetrahedron 62 / 120;
- pentagonal hexecontahedron 152 / 300.

All faces are triangles: no two neighbouring spike sides are coplanar.

**Verdict R7: CLOSED.**
1. **Catalan (13 of 13).** Star Halo = Polar Halo = the Archimedean dual. The reason: one face family, so the feet are h² times the
   poles.
2. **Archimedean (13 of 13).** The Polar Halo is the Catalan dual, which is classical. The Star Halo is a known solid for five:
   - the truncated tetrahedron gives the triakis tetrahedron, its own dual, so its Star Halo and Polar Halo coincide;
   - the cuboctahedron gives the tetrakis hexahedron, and the truncated octahedron the rhombic dodecahedron. The two swap: each one's
     Star Halo is the other's Polar Halo;
   - the icosidodecahedron gives DICTO FPD = DICTO Palintriacontahedron;
   - the truncated icosahedron gives DICTO's Star Halo (#78).

   It is new for eight: the truncated cube, rhombicuboctahedron, truncated cuboctahedron, truncated dodecahedron, rhombicosidodecahedron,
   truncated icosidodecahedron, snub cube and snub dodecahedron. Thumbnails of these are in data/thumbs/.
3. **Stars (52).** All are not convex (exact). All are new except DICTO's Golden TI Star (#78). Only one Star merges faces: the truncated
   cube's at t = 2. Its octagon pyramids lie in 12 common planes across the octagon–octagon edges, the same coincidence that turns the
   cube's Star at 2 into the rhombic dodecahedron.

**Status:** exact in each field (ℚ(√5), ℚ(√2, √5), ℚ(t, √5), ℚ(ξ)). "New" is limited to the registry and sources checked.

**Proposed home:** Star Cores v3, a chapter "The classical solids" after the regular census. The CO ↔ TO halo swap and the truncated
cube's t = 2 coincidence are its two structural lines.

**Prior art, sources checked (21 Nov 2026).**
- Library, ask-library, 4 queries, top 5 each:
  - "hull of the feet of the perpendiculars from the centre to the faces of an Archimedean solid"
  - "Kleetope of Archimedean solid pyramids on every face height"
  - "pedal polyhedron of a convex polyhedron face feet"
  - "stellation of Catalan solids pyramids on faces"

  Hits: Richter-Gebert 2026, Hynd 2023, Murphy–Weed 2024, Torquato–Jiao 2009 (both papers), Datta–Maity 2018, Johnson 1966, Wikipedia
  Goldberg polyhedron, Montejano et al. 2019, Yoshino–Chaidee 2026, Kubala 2019, Kabai 2010. None gives these halos or stars.
- Registry: krp-core POLYHEDRA (Platonic, Archimedean, Catalan, Johnson, first four stellations of the Platonic and Catalan solids),
  uniform prisms and antiprisms and their duals for n = 3–40, and DICTO Solids v7.
- The operations are classical: Kleetope/kis (Grünbaum) and polar reciprocation, as recorded in 2026-11-02-halo-census.
- Not checked this time: web searches, Wenninger's Dual Models, and Stella's library.

**LEADS (R7).**
1. **Why the CO ↔ TO swap?** The cuboctahedron is the rectified cube and the truncated octahedron its truncated neighbour in the
   cube–octahedron family. Test whether the Star Halo of the rectified
   (or truncated) member is always the polar of the other member, and why it fails for the icosahedral pair: the ID's halo is DICTO FPD,
   not the pentakis dodecahedron.
2. **The truncated cube's t = 2 coplanarity.** It happens whenever a face sits on a cube face direction and neighbours another such
   face across an edge parallel to a cube edge. List the t at which each Archimedean Star's spike sides become coplanar: the star-line
   walls of the 2026-11-09 census, extended to two- and three-family solids.
3. **Star Cores of the 26.** Run core_turn turn by turn, as #81 did for DICTO's solids. Not done here.
4. **The eight new Star Halos as solids.** Look for them as known Kleetopes at a non-canonical height (the TC halo is a cube with
   pyramids, the TD halo a dodecahedron with pyramids), then check face by face.

## Item L17: one solid per bond that fills alone (#51)

**Question (#51, open point):** "a single solid for each bond whose copies alone fill space". The DICTONIC BONDS are:
- golden: Icosaxes + Unborn Axes;
- keyed: Lotus Jewel Axes + Dodecaxes;
- Delian: Samson + Delilah.

Already done: O(t) on the Delian walk is never Dehn-zero except at the RD (study 2026-11-04-dehn-screen, float). The six bond solids
themselves are nonzero in studies/2026-11-19-dehn-atoms.

**Method.** scripts/l17_dehn.py builds every piece exactly (ℚ or ℚ(√5), with exact volume checks) and screens it with dehn_mp.py.
- dehn_mp.py is copied unchanged from 2026-11-19-dehn-words / dehn-atoms (sha256 396d9f2e…9217). It works at 80 digits, uses PSLQ
  among the dihedrals and π (tol 1e-50), calls a result ZERO below 1e-45 and NONZERO above 1e-6.
- A solid glued from convex parts is screened as the disjoint union of its parts, since the Dehn invariant is additive.
- **Lattice relation, used as a control.** If one copy of each piece per lattice cell fills space, the cell is scissors-congruent to
  their union, because any two fundamental domains of a lattice are equidecomposable by translations. So the pieces' Dehn invariants
  add to 0, and dehn_mp must return ZERO for every whole cell at every parameter.

**Controls (all PASS, logs/l17_cal.log).**
- dehn_mp's own calibration, 11 of 11:
  - zero: cube, RD, TO, RT, both golden rhombohedra, RD centre pyramid;
  - nonzero: tetrahedron, octahedron, icosahedron, dodecahedron.
- Union mode:
  - two cubes give ZERO;
  - one tetrahedron + one octahedron gives NONZERO;
  - one octet cell (2 tetrahedra + 1 octahedron) gives ZERO.
- Every cell in the walks below gives ZERO: 8 Delian, 7 factor-x and 10 golden cells.

**Results.**

| bond | family screened | pieces | result |
|---|---|---|---|
| Delian | the #51 slider, t = 1/10, 1/5, 1/3, 2/5, 1/2, 3/5, 4/5, 9/10 (exact volumes = #51 Main theorem) | T(t), O(t) | all NONZERO; cells 2T + O ZERO; t = 0 (RD) and t = 1 (cube) ZERO |
| golden | #48 Theorem 4, T(x), x = 1/3, 1/2, 1/τ, 1, τ, 2, 3 | T(x) (x = τ Icosaxes; partner x·T(1/x) = Unborn Axes at τ) | NONZERO except **x = 1 (Kelvin): ZERO**; coefficient sums 16√2, 12√2, … match the closed form below; cells ZERO |
| golden | AXE cut point s = 1/10, 1/5, 3/10, 2/5, 1/2, 3/5, 1/φ, 7/10, 4/5, 9/10 | I(s) = icosahedron + 12 pyramids, U(s) = Unborn + 12 pyramids | all NONZERO; cells ZERO |
| keyed | the same 10 cut points | Dodecaxes(s) = dodecahedron (edge 1/φ) + 12 pyramids, built two ways (also as Unborn + 8 Tricaps + 12 pyramids) | all NONZERO (both ways); Lotus Jewel Axes(s) = −Dodecaxes(s) by the lattice relation |
| keyed | keyings at the golden cut, k = 0, 1, …, 8 Tricap keys on the small piece | Unborn Axes + k Tricaps; the big piece is Icosaxes − k Tricaps | all NONZERO (coefficient sums grow 3k for k ≥ 3) |

**Exact statements (no floating point needed).**
- **Delian slider, every t in (0, 1).**
  - For t ≤ 1/3, T(t) is a regular tetrahedron and O(t) is the rhombic dodecahedron with its 8 three-fold corners cut. The RD edges
    have dihedral 120°, which is rational in π. The 24 cut edges, all of the same positive length, have dihedral π − ½ arccos(1/3).
  - For t ≥ 1/3, O(t) is a regular octahedron and T(t) is the cube with 4 corners cut. The cube edges are 90°. The 12 cut edges, all
    of positive length, have dihedral π − α, where α = arccos(1/√3) and 2α = π − arccos(1/3).
  - arccos(1/3)/π is irrational: 2cos(rπ) is an algebraic integer for rational r, and 2/3 is not.
  - So each piece's Dehn invariant is (positive length) ⊗ (an irrational angle), never 0. Both pieces are nonzero for every
    0 < t < 1, including the Delian bond t_D = 1 − (2/3)·2^(−1/3) (Samson, Delilah).
  - The Dehn invariant is zero only at the ends: t = 0 (rhombic dodecahedra alone) and t = 1 (cubes alone). By the lattice relation
    2·Dehn T(t) + Dehn O(t) = 0, so either piece is zero exactly when the other is.
- **Factor-x line (golden bond), every x > 0.** T(x) = hull of the signed orders of (1 + x, x, 0), at scale s:
  - Its 24 square–hexagon edges have length √2·x·s and dihedral π − α. Its 12 hexagon–hexagon edges have length √2·s and dihedral 2α.
  - So **Dehn T(x) = 24√2·s·(1 − x) ⊗ α**, which is zero exactly at x = 1, Kelvin's cell.
  - The golden pair, the DICTO 1:2 and 2:1 Truncated Octahedra, and every other member are nonzero. The screen's coefficient sums
    agree with this closed form at all 7 values of x.

**Verdict L17: CLOSED** as far as a Dehn screen can close it.
- **No DICTONIC SOLID fills space alone.** The Dehn invariant is nonzero for:
  - Icosaxes and Unborn Axes (exact, closed form);
  - Samson and Delilah (exact, single angle class);
  - Lotus Jewel Axes and Dodecaxes (80 digits, here and in dehn-atoms D69, D70).
- **Within each bond's own family, the only Dehn-zero pieces are the classical ends:**
  - Delian slider: the rhombic dodecahedron (t = 0) and the cube (t = 1), exact;
  - golden factor-x line: Kelvin's truncated octahedron (x = 1), exact;
  - the AXE cut-point walk (golden and keyed) and the 0–8 keyings: no Dehn-zero piece at any point tested (80 digits, sampled).

  All three ends are classical lone fillers. So "one solid per bond that fills alone" has the answer: **only where the bond collapses to
  a classical one-piece filling (RD, cube, Kelvin's cell); never at a bond itself.** Dehn zero is only necessary, but here it already
  rules every bond member out.
- **Still open:**
  - a proof for every cut point s of the AXE walk. Each angle class varies with s, so a transcendence argument is needed; a finite
    screen cannot prove it;
  - the second half of L17, "printed Samson and Delilah", which is a making task and not computed here.

**Proposed home:** #51 next version (a short section "No bond solid fills alone", with the two exact statements), cross-referenced in
#100 The Dehn Test Picks the Lone Tilers.

**LEADS (L17).**
1. **The AXE walk for every s.** The coefficient on one basis angle stays 24.0 at every non-golden s. Find which edges carry it. If it is
   the icosahedron's own dihedral arccos(−√5/3), prove that it is independent of the pyramid dihedrals mod ℚπ for every s. The
   Conway–Radin–Sadun criterion for angles with rational squared cosines may apply, since the pyramid apex moves on a line with
   rational s.
2. **Mixed keyings.** k keys per cell in a periodic pattern give a big piece and a small piece that are both nonzero for every k tested.
   A pattern with two different small pieces needs a two-piece relation instead. Not screened.
3. **The lattice relation as a tool.** Dehn(big) = −Dehn(small) for every two-piece bcc or octet filling. It gives a free consistency
   check for any future bond.

## Files

- scripts/:
  - nf.py (number fields), exactgeo.py (exact hulls and stars), build_dataset.py, exact_census.py, r7_table.py, run_r7.sh, l17_dehn.py;
  - copied unchanged: census.py, collect.py, dehn_mp.py.
- data/:
  - for R7: slugs.txt, classical-krp.json (registry, copied), collect_census.json (collect.py output), exact_census.json, r7_table.csv,
    thumbs/ (the 8 new Star Halos);
  - for L17: l17_cal.json, l17_delian.json, l17_factorx.json, l17_golden.json, l17_keyed.json.
- logs/: one per run, each ending FINAL ok.
- Computed on the compute host in the foreground; every call took under 280 s. The work/ folder (dataset, per-shape census JSON, DICTO
  Solids v7) stays on the host and is not committed.
- Python on the host: ~/venvs/indep (numpy, scipy, sympy, mpmath), and ~/venvs/plates for collect.py's thumbnails. ~/venvs/voids has
  no sympy there.

## Concordance ledger lines (proposed)

{"question": "R7: Star (t = 2), Golden Star (t = phi), Star Halo and Polar Halo of the 13 Archimedean and 13 Catalan solids", "method": "exact corners in Q(sqrt5), Q(sqrt2,sqrt5), Q(t,sqrt5), Q(xi); census.py + collect.py (2026-11-02-halo-census, unchanged) and an exact re-check of every hull, star surface and match (studies/2026-11-21-gaps-batch-a)", "status": "SETTLED", "result": "Catalan: Star Halo = Polar Halo = Archimedean dual (13/13). Archimedean Star Halos known for 5: TT -> triakis tetrahedron (= its Polar Halo), CO -> tetrakis hexahedron, TO -> rhombic dodecahedron (CO and TO swap), ID -> DICTO FPD = Palintriacontahedron, TI -> DICTO Star Halo (#78); new for 8 (TC, rCO, tCO, TD, rID, tID, snub cube, snub dodecahedron). All 52 stars not convex; new except the Golden TI Star (#78); only the truncated cube's Star at 2 merges faces (12 four-sided, as cube -> RD)", "retry": "never; only LEADS (halo swap reason, coplanarity walls of two-family stars, Star Cores of the 26)", "study": "studies/2026-11-21-gaps-batch-a", "date": "2026-11-21"}

{"question": "L17 (#51): one solid per DICTONIC BOND that fills space alone", "method": "dehn_mp.py (80 digits, unchanged) on exact pieces; disjoint unions for glued pieces; lattice-cell ZERO controls; exact single-angle proofs (studies/2026-11-21-gaps-batch-a)", "status": "SETTLED (Delian, golden exact); keyed walk screened", "result": "no DICTONIC SOLID is Dehn-zero; Delian slider: T(t), O(t) nonzero for all 0 < t < 1 (exact), zero only at RD (t = 0) and cube (t = 1); factor-x: Dehn T(x) = 24 sqrt2 s (1 - x) (x) arccos(1/sqrt3), zero only at Kelvin x = 1; AXE cut walk (golden, keyed) and keyings k = 0..8 nonzero at all points tested", "retry": "only LEAD 1 (proof for every cut point s)", "study": "studies/2026-11-21-gaps-batch-a", "date": "2026-11-21"}
