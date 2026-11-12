# The hop's 4D Vacuus, built like the permutohedron's (study 2026-11-12)

**Conclusion: built the permutohedron's way, the hop's 4D Vacuus has no sophisticated centre. With the centre inside the solid, the walls
never line up beyond one or two symmetry orbits (largest drop 12.9 % of the slices at k = 5, 3.5 % at k = 7; the permutohedron's
centre merges 57 %). Neither slice type nor wall mixing tells cut cells from surviving ones better than random orbit labels (k = 5–7).**
**Status: CLOSED for k = 5–7 (a negative answer, exact where marked). k = 8–11 SKIPPED: the float 4D enumeration fails Euler there (LEAD 1).**

## DICTO's idea, in his words
11 Nov 2026, evening, on #43 step A1 (why the OG hop never cuts more than half the faces): "most likely a 4D vacuus that is very
sophisticated but that should narrow it down", then "c the permutahedron 4D vacuus".
Restated: build the Vacuus of the hop's 4D sweep the way the 4D permutohedron's Vacuus was built (#105: central 3D slices that
together carry every 2-face; there 150 two-faces lie on 65 central slices in four classes, five of them truncated octahedra), and see
whether that Vacuus tells the faces that die (cut) from the faces that survive.

## What was already done (read first; nothing here is a retry)
- og-margin §31 (float pilot) and §31a (centred and centre-free, 60 digits from Q(√5), k = 5–11; ledger [149] FOUND): generic slice
  counts 465 … 1695; hundreds of special heights, each merging ONE orbit (drop 48 or 60); wall types (aa / ac / cc) never mixed with
  other types on one slice except the 15 mirror sheets. That run listed heights mostly BELOW the bottom of the sweep (centre outside the
  solid) and did not compute the 3D slices themselves.
- NOT done, and asked for in the plan of 11 Nov: (a) a positive control with the SAME code reproducing the permutohedron's 65;
  (b) a negative control; (c) the heights where the centre is INSIDE the solid, separated from the outside ones; (d) the slices' own
  3D shapes, grouped into classes, and the test "cut against surviving cells by slice class".
  Ledger read: [116] (permutohedron Vacuus, SETTLED), [144] (roundness: "proof must use the OG orbit structure (DICTO: a sophisticated
  4D Vacuus)"), [147] 600-cell FAILED, [149] (this sweep's Vacuus counts, FOUND, lead: border sheets), [151]–[155] (A1 possibilities).

## The precise question
The hop k → k+1 of the OG downward family has candidates X_j (the corners of X_k, exact in Q(√5)), b_j = |X_j|². Its sweep is the 4D
solid P = {(y, λ) : X_j·y − λ ≤ b_j, λ ≥ 0} (capped at a height Λ above every event, as §27). Its 3D cells are the facets X_j·y − λ = b_j;
a WALL is a 2-face between two cells. For a centre c = (O, t) on the slider axis, each wall spans with c exactly one central 3D slice.
1. N(t) = number of distinct central slices carrying the walls. Which heights t make walls line up (N drops), and do any of them lie
   INSIDE the solid (t > 0)? How large is the largest drop (one orbit, or a collapse like the permutohedron's 150 → 65)?
2. Slice classes: at a generic inside height and at the inside special heights, group the slices into classes under I_h; for each class
   compute its 3D shape (corners, edges, faces by sides) and the walls it carries (between two surviving cells aa, a surviving and a cut
   cell ac, two cut cells cc). Does the combinatorial slice type separate cut from surviving cells (types carrying ac or cc walls
   disjoint from types carrying only aa walls)?

## Method (one engine for every solid)
- `scripts/vac4.py`: a 4D polytope given by facets n_f·x ≤ h_f with EXACT coefficients (class R5 = a + b√5, gmpy2 rationals; integers
  are the case b = 0). Vertices and incidences from a float halfspace intersection (tolerance 1e-9, the gap to the next facet printed);
  f-vector with Euler V − E + F2 − F3 = 0; walls = facet pairs whose common corners span a plane.
- Central slice of wall (f, g) through c: normal ν = (h_g − n_g·c) n_f − (h_f − n_f·c) n_g, EXACT; slices counted by exact equality of
  normalised normals.
- Special heights on the line c(t) = c0 + t u: ν(t) is linear in t, two walls share a slice ⇔ all 2×2 minors of (ν1(t), ν2(t)) vanish;
  candidates from a float prefilter (minors below 1e-7 relative), each confirmed EXACTLY by the gcd of the six minor polynomials over
  Q(√5) (degree 1: an exact height in Q(√5); degree 2: both roots). N at each special height by union of the confirmed pairs.
  NUMERICAL: the prefilter (a pair it rejects is decided in float, smallest rejected value printed); slice shapes and classes (float,
  tolerance 1e-9, gaps printed).
- Positive controls: (i) the 4D permutohedron (30 facets, integer): the engine must find 150 two-faces, f-vector (120, 240, 150, 30),
  N = 65 at its centre with corner/face counts of the four classes as #105 (32/22, 24/14, 24/20, 24/14), and the centre as the deepest
  drop of a scan along a generic line through it; (ii) on the sweep, the wall counts of §31a (750, 930, 1170, 1410, 2310, 2040, 2040
  for k = 5 … 11) and the cut set = cells missing from the floor λ = 0.
- Negative controls: (i) the permutohedron with its 30 facet offsets moved by small random rationals (same f-vector): no lining up at
  its centre (N = 150); (ii) the sweep with every b_j moved by a small random rational factor: no mirror sheets, no non-trivial special
  height; (iii) for test 2, random cut labels on whole orbits (20 draws, same number of cut cells ± one orbit): how often a random
  labelling separates.
- Runs on the compute machine only (2 cores, 6 GB cage), pilot k = 5–6 first; k = 5 … 11 as §31a.

## Results (run 12 Nov 2026 on the compute machine, 2 cores; data/hop-vacuus4d.{json,log}, FINAL ok; figures/hop-vacuus4d-scan.png)
Scripts: scripts/vac4.py (the engine), scripts/hop_vacuus4d.py (controls + sweep), scripts/fig_scan.py.

**Controls, all PASS.**
- Positive, the 4D permutohedron through the SAME engine: f-vector (120, 240, 150, 30); 65 central slices at its centre; four classes
  30 × (32 corners, 52 edges, 22 faces), 20 × (24, 36, 14), 10 × (24, 42, 20), 5 × (24, 36, 14) = #105. Along a generic line through the
  centre the scan finds 43 special heights inside; the centre is the deepest (N = 65); every other drop is 1 to 8 (parallel 2-faces).
- Negative, the permutohedron with its 30 facet offsets moved by random rationals (same f-vector): 150 slices at the old centre (nothing
  lines up); largest inside drop 1.
- Negative, the sweep at k = 5 with every b_j moved by a random rational factor: 1001 walls, 1001 slices at every generic height (no
  mirror sheets), no non-trivial special height at all.
- On the sweep, k = 5, 6, 7: cells, cut cells and walls = og-margin §31a ((252, 60, 750), (320, 60, 930), (402, 90, 1170)); generic N
  = 465, 615, 1035 = §31a, exact and equal at three generic heights; every special height confirmed EXACTLY (gcd of the six minor
  polynomials over Q(√5)); smallest float value the prefilter rejected 1.1e-7, 1.6e-7, 6.9e-6 (k = 7: 1176 float candidates rejected
  exactly).

**Question 1, heights where the walls line up.** Exact, k = 5 / 6 / 7:
| k | walls | generic N | special heights (trivial) | inside the solid | drops inside | largest inside drop / N |
|---|------|-----------|---------------------------|------------------|--------------|--------------------------|
| 5 | 750 | 465 | 46 (4) | 3 | 60, 60, 48 | 0.129 (t = 0.473 max b) |
| 6 | 930 | 615 | 71 (5) | 8 | 12 (all eight) | 0.020 |
| 7 | 1170 | 1035 | 112 (7) | 8 | 36, 30, 12 ×5, 6 | 0.035 (t = 0.155 max b) |
Every inside special height merges one or two symmetry orbits of walls; no inside pair is a pair of parallel walls (all genuine
crossings). Most special heights lie BELOW the floor (centre outside the solid), as §31a found. Against the permutohedron's centre
(85 of 150 slices merged, 57 %) the hop's sweep has no centre where its walls collapse. (k = 7: §31a listed a drop 48 near t = 0.155;
the exact count here gives 36 at that height; the float prefilter can only miss merges, so 36 is exact for the pairs it found and a lower
bound in principle; the difference is noted, not resolved.)

**Question 2, cut against surviving cells by slice class.**
- k = 5 (EXACT slice shapes: corners recomputed in Q(√5) from three facets each, incidences exact, Euler 2 for every class at five heights):
  10–11 classes per height (orbits of 120, 72, 60, 48, 36, … slices; 94–143 corners each, two big cap faces). Every class carries walls of
  one type only. T1: the slice types carrying a cut cell's wall (2) and those carrying only survivor walls (5) are disjoint, BUT random
  whole-orbit labels separate in 20 of 20 draws (every class has its own type), so T1 carries no information.
- k = 5–7, T2 (no shapes needed): slices merged at an inside special height never mix wall types (aa with ac or cc), and random orbit
  labels never do either (0 of 20 draws): the merges join walls of matching orbit pairs, so T2 carries no information either.
- k = 6, 7: slice shapes NOT computed (pilot: the float corner proposals of these near-degenerate slices broke Euler even after exact
  repair); only T2 there.

**Plainly numerical:** the wall lists (float 4D enumeration, incidence gap ≥ 1.5e-6 at k = 5–7, checked against §31a and Euler 0); the
float prefilter for special heights; the I_h classes of slices (normals rounded to 1e-7). Exact: every slice count, every special height,
the k = 5 slice shapes.

**Reading for #43 step A1.** DICTO's guess that a sophisticated 4D Vacuus would narrow the cut down is tested the permutohedron's way and
does not hold in this form: the sweep's walls do not gather on a few central slices at any inside height, and the slice classes that
exist sort cut and surviving cells no better than chance. The border sheets of §31a (centre-free) remain the open form of the idea.

## LEADS
1. k = 8–11: the float 4D enumeration of the sweep fails Euler (symmetric corners where 5–15 cells meet split or merge wrongly; k = 8
   gives 1490 walls against §31a's 1410). Next method, decided: EXACT 4D corner enumeration (corners as exact solutions of four cell
   planes, proposed by the float run), then rerun this scan for k = 8–11.
2. The k = 7 drop near t = 0.155 max b: 36 here, 48 in §31a; recompute that one height with all pairs exactly (no prefilter).
3. Slice shapes at k ≥ 6: build them from the exact 4D corners of lead 1 (cut each exact edge by the slice) instead of a float 3D hull.
4. Centre-free sheets (§31a, P2 of §35): count the border sheets (circles through two surviving and two cut candidates) per level.
5. A slice-type test with information needs a coarser invariant than the full combinatorial type (e.g. which cells a slice meets); fix it
   in advance and keep the random-label control.

## Concordance line (ready)
2026-11-12 · #43 Conj. 1 step (A1) · DICTO 11-11 'c the permutahedron 4D vacuus': the hop sweep's 4D Vacuus built like the
permutohedron's, k = 5–7 · one engine reproduces the permutohedron (65 slices, four classes) and fails its negatives · inside the solid
the walls line up at most one or two orbits (drop ≤ 12.9 % vs 57 % at the permutohedron centre) · slice types and wall mixing do not sort
cut from surviving cells better than random orbit labels · k = 8–11 skipped (float enumeration fails Euler; next: exact 4D corners) ·
studies/2026-11-12-hop-4d-vacuus.
