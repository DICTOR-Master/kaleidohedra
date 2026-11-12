# Aim 2, chunk 5c: canonical forms of the 43 regions of the flat DICTO Yantra (12 Nov 2026; `scripts/yantra_regions.py`, log `data/yantra-regions.log`, 62 checks, FINAL ok)

**Conclusion.** Each of the 43 regions of the DICTO Yantra is a positive geometry (all 43 are triangles; no region is four-sided); no
two regions share a wall, so their forms never cancel each other; walls cancel only against the 31 even faces between them (10 triangles,
21 four-sided), and the whole yantra's form, the sum of the 43, has degree-24 numerator N over the 27 side lines. The 18 marmas are exactly
where N gains an extra zero: it vanishes there to order 2, so the marmas carry no point residue, while each of the 24 sandhis carries
residue 2. Because of those 2s the whole yantra is a signed sum of positive geometries, not one itself.

**Question.** Chunk 5b (studies/2026-11-12-yantra-cones-canonical, commit 357d1255) showed that the half-spun DICTO Yantra cones are
positive geometries whose residue on the yantra plane is the flat yantra triangle, and left the lead: the canonical forms of the flat
DICTO Yantra's 43 regions, where the degree-160 marma points enter. Three questions:
1. Is each of the 43 regions a positive geometry (and which are triangles, which four-sided)?
2. Do the forms of adjacent regions cancel along shared walls, so that the whole yantra's form is the sum of the regions' forms?
3. Do the marma points (three sides meeting) show special structure in the whole yantra's form: cancelling poles, extra zeros?

**Yantras.** The DICTO Yantra = GF1 of the sri-yantra study (perfect Cleo-Antonius yantra, u·v = 2/φ³). Its great slope u is a root of
an irreducible integer polynomial of degree 160 (figures/dicto-yantra-exact-u.txt of that study), so every vertex and marma is algebraic
of degree up to 160. Second, exact instance: R1, the rational Śrī Yantra of the same study (all coordinates in Q, all 18 marmas exact,
regions 14 + 10 + 10 + 8 + 1 = 43).

## Method (chosen before computing)

**Precision, stated plainly.** Fully exact algebra in the degree-160 field is not attempted (one multiplication there is a reduction
modulo a polynomial with 226-digit coefficients; the arrangement needs thousands). Instead:
- *Exact, proved:* (a) the local lemmas below, as sympy identities with symbolic slopes; (b) everything for R1, in exact rational
  arithmetic, with polynomial identities proved by the grid lemma (a polynomial in x, y of degree ≤ d that vanishes on an
  (d+1) × (d+1) grid is zero).
- *DICTO Yantra, certified high precision:* u is isolated EXACTLY (integer arithmetic) by a sign change of the degree-160 polynomial
  across an interval of width 10⁻²⁸⁰ around the Newton root; v = (2/φ³)/u; Q and S solved by Newton from the two corner conditions
  (t1, t9 corners on the circle), as in the study's backwards check; the third condition (bindu centred), never imposed, and all 18
  marmas, tips on bases and corner touches must then hold below 10⁻²⁵⁰. The whole computation runs at 300 digits and again at 600
  digits; a quantity is called zero only if it is below 10⁻²⁰⁰ times its scale at both, and every nonzero value must agree between the
  two to 10⁻²⁰⁰. The point positions are not interval-certified; the claim for the DICTO Yantra is "holds to 200+ digits at two
  precisions", and its structural part is proved exactly through R1 when the two crossing patterns are identical (checked).

**Arrangement.** 27 sides (base and two legs of each of the nine triangles); all side crossings; planar graph; faces by the half-edge
walk (as in figure.py); containment count c(F) = number of triangles containing the face; the 43 regions are the faces with c odd.
For each face: number of sides after dropping straight-through vertices (triangle / four-sided / more), convexity, and the line of
each edge (one of the 27). The crossing pattern of a yantra = the set of faces, each written as (containing triangles, edge lines in
order); R1 and GF1 are compared on it.

**Forms.** A convex polygon with inward edge functions ℓ_i ≥ 0 (in cyclic order) has Ω = Σ_i det(a_i, a_{i+1})/(ℓ_i ℓ_{i+1}) (vertex
formula; a_i the gradient of ℓ_i). Independent second formula: fan triangulation into triangle forms D²/(⟨X12⟩⟨0X2⟩⟨01X⟩). Bridge
check (chunk 2): inside each region, Ω(X) = 2!·area of the polar of (region − X). The whole yantra's form is Ω_Y = Σ over the 43
regions; its numerator N = Ω_Y · Π_{27 sides} L_j is a polynomial of degree ≤ 25 (≤ 24 expected), built by exact interpolation on a
26 × 26 grid (for R1; at 300/600 digits for GF1).

**Q1 (each region).** Residue test is automatic for convex polygons; checked here: vertex formula = fan formula (grid identity),
Ω > 0 inside, Ω = 2·polar area at an inside point.

**Q2 (walls).** Parity lemma: crossing one side changes c by exactly 1 (no two sides of different triangles on one line: checked), so
two regions of the 43 never share a wall; they meet only at points. Walls are shared between a region (odd) and an even face. Checks:
(i) inside each triangle T_i, the faces (odd and even) sum to Ω(T_i) (all inner walls cancel); (ii) valuation identity
Ω_Y = Σ_{I ≠ ∅} (−2)^{|I|−1} Ω(∩_{i∈I} T_i) (parity form of inclusion-exclusion, 1_odd = Σ (−2)^{k−1} e_k), proved for R1 by the grid
lemma; (iii) the residue of Ω_Y on each side line, and whether Ω_Y is a positive geometry in the strict sense of Arkani-Hamed, Bai and
Lam (2017) (point residues only ±1 or 0).

**Q3 (marmas).** Every point where two or more of the 27 side lines meet (inside or outside the segments) is classified: marma (three
sides through it, inside all three), sandhi (two sides crossing), triangle corner, corner touch, tip on a base, or a crossing of the
extended lines outside the drawn sides. At each: m = number of lines through it, k = order of vanishing of N there (exact derivatives
for R1, up to order 3), and at m = 2 points the point residue N(p)/(R(p)·det(n1, n2)). The local lemma (symbolic): for k lines through
one point and the 2k sectors alternately in and out, the sum of the "in" sectors' forms is 0 when k is odd and 2·(alternate sum) when
k is even; so at a marma (k = 3) the point residue should vanish and N vanish to order 2, at a sandhi (k = 2) the residue should be ±2.

**Controls.** Positive: a plain triangle (standard simplex: vertex = fan = 1/(xy(1 − x − y)), polar area at (1/3, 1/3) = 27/2);
a triangle cut into 4 by its midlines sums back (known region sum); the nine faces-in-triangle sums. Negative: a mis-joined wall (an
odd region plus its even neighbour moved 1/1000 off the shared wall) must leave a pole on that wall (scaling exponent 1 instead of 0);
a broken marma (R1 with one base moved 1/1000 so its three sides no longer meet) must turn the order-2 zero into ordinary sandhis with
residue ±2; one region's sign flipped must break the valuation identity; one flipped normal must break vertex = fan.

**Compute.** The compute machine, 4 cores (lemmas + R1 exact, GF1 at 300 digits, GF1 at 600
digits, broken-marma control in parallel), memory cage 12 GB, through the job gate; pilot (R1 + GF1 at 80 digits) under 5 minutes first.

## Checks (62, all held; asserted lines only)

- Positive controls: lemmas and plain cases (symbolic, sympy): plain triangle (vertex = fan = 1/(xy(1 − x − y)); 2 × polar area at
  (1/3, 1/3) = 27 = Ω); triangle cut in four by its midlines sums back; alternate sectors of k lines through one point: sum 0 for k = 3, 5,
  2 × (alternate sectors of a half-turn) ≠ 0 for k = 2, 4; sectors add (Plücker).
- R1 exact (Fractions, grid lemma on 26 × 26 points) and the DICTO Yantra at 300 and at 600 digits, the same 23 checks each: 74 bounded faces,
  all convex; regions 14 + 10 + 10 + 8 + 1 = 43, all triangles; parity lemma (0 exceptions, 0 walls between two regions); vertex = fan
  for each region; Ω > 0 inside every face and Ω = 2 × polar area (chunk-2 bridge); faces in each of the nine triangles sum to its form
  (known region sum); valuation identity Σ43 = Σ_I (−2)^{|I|−1} Ω(∩T_I) over all 511 intersections (every subset of the nine triangles
  meets: 9, 36, 84, 126, 126, 84, 36, 9, 1); Σ nine triangles = Σ faces × c; N of degree 24; all 27 sides are pole lines; point table
  (below); 18 marmas, 24 sandhis; order 2 at every marma; residue 2 at every sandhi; zero residue at every crossing of extended lines;
  wall control.
- DICTO Yantra rebuilt: u isolated exactly by a sign change of its degree-160 polynomial on an interval of width 10⁻²⁸⁰ (10⁻⁵⁸⁰ in the
  600-digit run); bindu centring, never imposed, holds to 1.5·10⁻²⁹⁴ (1.9·10⁻⁵⁹³); worst Huet condition 4.7·10⁻³⁰² (3.5·10⁻⁶⁰²); stored
  40 digits agree. Merged points spread 1.9·10⁻³⁰¹ (tolerance 10⁻¹⁵⁰).
- R1 and the DICTO Yantra have the same crossing pattern: the same 74 faces (each with its triangles and side lines) and the same type,
  m and k at every point on the drawn sides. So the exact R1 results hold as structure for the DICTO Yantra too; only the crossings of
  extended lines far off the figure differ in number (R1 68 + 22 beyond the box, DICTO Yantra 74 + 16), all with zero residue.
- 300 against 600 digits: the same pattern and point table; values agree to 6.7·10⁻²⁹², residues to 5.7·10⁻²⁸².
- Negative controls (all caught): one region's sign flipped breaks the valuation identity; one flipped normal breaks vertex = fan; the
  middle piece subtracted from the four-piece triangle does not sum back; wall control: a region plus its even neighbour has pole exponent
  0.000 on the shared wall (cancels), the neighbour moved 1/1000 off the wall gives exponent 1.000 (a pole is left); broken marma: R1 with
  t2's base moved 1/1000 keeps 12 of the 18 marmas, and near the old marma (1,2,7) there are 3 separate crossings, each an ordinary sandhi
  with k = 0 and |Res| = 2: the order-2 zero needs exact concurrency.

## Results

1. **Each region (question 1).** All 43 regions are triangles (DICTO Yantra and R1). Every face of the arrangement is convex, so every
   region is a positive geometry with the triangle form; vertex formula = triangulation = 2 × polar area, the chunk-2 bridge. The 31 even
   faces inside the yantra (the gaps between regions) are 10 triangles and 21 four-sided; nothing has more sides.
2. **Walls (question 2).** Crossing any side changes the number of covering triangles by exactly one, so two regions never share a wall:
   the 43 regions meet only at points, like the black squares of a chessboard. Wall cancellation happens between a region and an even
   neighbour (control: exponent 0, and 1 when moved off), and inside each of the nine triangles all inner walls cancel. The whole yantra's
   form is the sum of the 43 regions' forms by definition of the canonical form as a valuation, and equals
   Ω_Y = Σ over nonempty I of (−2)^{|I|−1} Ω(∩_{i∈I} T_i) (all 511 intersections nonempty). It is not the sum of the nine triangles' forms,
   which is the residue of chunk 5b's half-cones; that sum weights each face by its count c instead of by c mod 2. Ω_Y = N/(product of the
   27 side lines), N of degree 24, every side a pole line.
3. **Points (question 3).** At every point where side lines meet (m lines, N vanishing to order k; DICTO Yantra counts, R1 the same except 68 fully-off crossings):

   | point | count | m | k | point residue |
   |---|---|---|---|---|
   | marma (three sides through it) | 18 | 3 | **2** | none (pole order 1 only) |
   | sandhi (two sides crossing) | 24 | 2 | 0 | **±2** |
   | triangle corner (free) | 14 | 2 | 0 | ±1 |
   | tip on a base | 7 | 3 | 1 | |
   | corner touch | 6 | 3 | 1 | |
   | crossing of extended lines, partly or fully off the drawn sides | 94 + 74 | 2 | 1 | 0 |

   The marmas are the special points: N has an extra zero of order 2 there (one more than a triple point forces), because the three
   regions round a marma sit in alternate sectors and alternate sectors of three lines cancel (the lemma; a sum over a half-turn).
   Along each side the residue of Ω_Y is a chain of its segments whose sign flips at every sandhi and runs straight through every marma.
   The sandhis are the opposite: the two regions meeting there add, residue 2. The degree-160 numbers enter only as positions: the pattern,
   the orders and the residues are those of the exact rational yantra R1.
4. **Positive geometry, whole yantra.** In the strict sense of Arkani-Hamed, Bai and Lam a 0-dimensional residue must be ±1; Ω_Y has 2 at
   all 24 sandhis, and at the DICTO Yantra's centre (0, 1/2), inside the bindu region, Ω_Y = −86.08 < 0 (R1: +1649.8). So the whole
   DICTO Yantra is a signed sum of 43 positive geometries, not a positive geometry itself.

**What this gives the aim.** In the flat yantra the "law" is a parity law: regions alternate, so poles never cancel between regions but
cancel exactly at the marmas, where three sides meet. The marmas are the zeros of the yantra's form (order 2), the sandhis its doubled
point poles. This is a statement about the crossing pattern, shared with every yantra of the traditional pattern tested (R1, the DICTO
Yantra); the exact degree-160 values only place the points.

**Faults fixed on the way.** (1) Pilot: the zero tolerance was 10^−(digits − 100), which is above 1 at 80 digits; now 10^−(2·digits/3).
(2) Pilot: crossings of nearly parallel extended lines far off the figure lost precision in the monomial form of N; these are now
classified only inside the box |x| ≤ 3, |y − 1/2| ≤ 3 and counted beyond it; the comparison of R1 with the DICTO Yantra uses the drawn
points. (3) Full run: in the broken-marma figure a broken corner touch makes a corner poke into a face (3 non-convex faces); the
containment test used the face centroid, which can fall outside a non-convex face, and reported false parity jumps; it now uses a point
just inside the longest edge (diagnostic `scripts/diag_broken.py`). The yantras themselves have only convex faces, so their results are
unchanged.

Launch: the compute machine, 4 cores, 12 GB cage, through the job gate; pilot 39 s, full run 62 s.

**LEADS.** (a) Kulaichev's yantra and Rh345 have 45 regions with two non-triangles (the sri-yantra study): does the extra pair change
the point table (a marma split into sandhis)? (b) The zero curve N = 0 (degree 24) of the DICTO Yantra: does it pass through anything
else traditional (the circle, the bindu centre)? (c) The 3D version: the alternating sum of chunk 5b's half-cones.

Credit: positive geometries and canonical forms: Arkani-Hamed, Bai, Lam (2017); the Śrī Yantra conditions: Huet (2002), Chiodo (2021);
the DICTO Yantra, its name and the Cleo-Antonius pair are DICTO's; R1 is from the sri-yantra study (8 Nov 2026).
