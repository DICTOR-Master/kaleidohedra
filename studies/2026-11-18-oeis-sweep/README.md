# OEIS sweep: every possible new entry from DICTO's published work (18 November 2026)

DICTO, 18 Nov 2026: "Queue all possible sequences." Occam's razor applied: only genuine candidates are listed; the rest are
in "Considered and rejected" with a one-line reason. Nothing here was written to ENTRIES.md, concordance.json or any paper.
Nothing was committed. "Not found" means the OEIS search returned no match on 18 Nov 2026; it does not mean new.

**Conclusion.** Four entries can be queued from published papers: two pyrochlore walk sequences (#102 Corollary 2), the
mode counts of the Poincaré dodecahedral space (*Alicia*/Queens book, Chapter 9, Theorem 3) and the slope constant of
Kulaichev's Śrī Yantra (#103 Theorem 10). Two more need a published home first, and five comments on existing entries are
possible. Every term was computed two independent ways and agrees (FINAL ok in all three scripts).

Already handled, not re-proposed: A400949, entries 2-5 (4H/6H coordination sequences), entry 6 (Fibonacci stacking word),
A402231, entry 8 (cot(2π/7)), A402191, ENTRIES.md section B comments (A002895, A002899, A008264, A085002).

## Method

- Read: ENTRIES.md (rules 0, 0b, 11-15), papers/oeis-candidates-2026-11-07.md, studies 2026-11-07-oeis-candidates,
  2026-11-08-oeis-matcher (96 lists, 72 not found), 2026-11-08-sequences, 2026-11-08-pyrochlore-walks, 2026-11-04-pds-modes,
  2026-11-15-ring-counts-stackings, 2026-11-17-yantra-sequence; concordance.json (ledger: 312 entries, grepped for sequence,
  coordination, generating, OEIS, a(n), N(n), recurrence, decimal, walks, polygons, shell; papers; oeis section); and the
  text of every published paper/book folder with a zenodo-state.json (grepped for "for every n", "every dimension",
  "OEIS", A-numbers, "irreducible", "root of", "minimal polynomial", and specific term runs).
- Computed on the compute host (venv with mpmath/sympy), nothing on the Pi. Scripts in `scripts/`, raw output in `data/`.
- OEIS: `scripts/oeis_search.sh` with `scripts/queries.txt` (23 queries, `search?q=...&fmt=short`, 4 s apart), log
  `data/oeis-searches.txt`; follow-up lookups (fmt=text) in `data/oeis-searches-followup.txt`.

---

## Ranked candidates

### 1. Closed walks per site of the pyrochlore network: READY

- **What it is.** The pyrochlore network is the net of corner-sharing tetrahedra (the spin-ice lattice): each site joins
  6 others. a(n) = number of closed walks of n steps that start and end at a fixed site.
- **Terms, n = 0..40:** 1, 0, 6, 12, 78, 300, 1512, 7056, 35214, 176124, 902496, 4679136, 24590208, 130560768, 699729792,
  3779987712, 20562988878, 112547448924, 619346672208, 3424664011776, 19018122975768, 106021551258096, 593110987716000,
  3328539189498432, 18733818892838688, 105717847936756800, 598035541490454528, 3390631479921169920, 19263561414031164672,
  109655484361799852544, 625322550966187133952, 3571953658400419952640, 20435659252041239298894, 117087398683785978894876,
  671787276431394873967152, 3859387337202726501074496, 22199225704355895681486216, 127838222555470581305464656,
  736987326087592547111811936, 4253151084873620038937290176, 24569148624255854101508131704
- **How computed, two ways (agree for n = 0..30):**
  (A) new, `scripts/pyrochlore.py`: the pyrochlore network is the line graph of diamond, so its spectrum is diamond's
  shifted by +2 plus the eigenvalue -2; per site a(n) = (1/2) Sum_{i} C(n,i) 2^(n-i) D(i) + (1/2)(-2)^n, where D(i) is the
  Domb number A002895(i/2) for even i and 0 for odd i. A clean closed formula for the entry.
  (B) independent, study 2026-11-08-pyrochlore-walks/walks.py: direct dynamic programming on the network (no formula), L <= 30.
- **OEIS:** 6,12,78,300,1512,7056,35214,176124,902496,4679136 not found; 78,300,1512,7056,35214,176124 not found;
  halved 3,6,39,150,... not found; keyword "pyrochlore" not found (the word appears nowhere in the OEIS).
- **Source:** #102 *Every Site Hears the Same: the Loop Equality Is a Theorem*, DICTO DOI 10.5281/zenodo.24037664 (v6
  published), **Corollary 2** (spin ice): the counts are the same at every site of every stacking; lengths 1..6 printed
  (0, 6, 12, 78, 300, 1512, ...). The A002899 comment pattern (same counts on every stacking) applies here too.
- **Notes for the entry:** the line-graph formula is standard (Sachs); the entry needs it stated with that credit. Natural
  crossrefs: A002895, A400949, A002899.

### 2. Closed non-backtracking (tailless) walks per site of the pyrochlore network: READY

- **What it is.** The pyrochlore analog of A400949 (diamond) and A402231 (fcc): closed walks that never step straight back,
  including across the start/end, counted per site.
- **Terms, n = 1..40:** 0, 0, 12, 12, 0, 276, 756, 2988, 16104, 64800, 278916, 1286352, 5738928, 25845036, 118098612,
  540178572, 2482501704, 11470845192, 53186644596, 247472898972, 1155354197016, 5409675441324, 25398322598892,
  119545910744592, 563987677987800, 2666471876270592, 12632008967689620, 59953672872323256, 285045170715444144,
  1357431489995004156, 6474176318410052820, 30922424530670606028, 147893306022431788776, 708232870196593822776,
  3395670991492234406196, 16299299509844030074260, 78321345087212812535496, 376734359371710607989900,
  1813894583642795071754556, 8741581552714202942840508
  (a(3) = 12: each site lies on 2 tetrahedra, 3 triangles through it in each, 2 directions; a(5) = 0: no 5-cycles and no
  tailless 5-walks.)
- **How computed, two ways (agree for n = 1..30):** (A) Ihara-Bass for a 6-regular net (q = 5, the A400949 program's
  transform) applied to the closed walks of candidate 1; (B) direct count of Hashimoto edge walks on the network
  (walks.py, independent of any formula).
- **OEIS:** 12,12,0,276,756,2988,16104,64800,278916 not found; 276,756,2988,16104,64800,278916,1286352 not found; halved
  6,6,0,138,... not found.
- **Source:** #102, **Corollary 2**; lengths 1..8 printed (0, 0, 12, 12, 0, 276, 756, 2988, ...).
- **Note:** completes a family of three (A400949, A402231, this). Rule 14 means one at a time; 1 and 2 are a natural pair,
  1 first (2's formula uses 1).

### 3. Mode counts of the Poincaré dodecahedral space: READY (classical mathematics; new only as an entry)

- **What it is.** The Poincaré dodecahedral space is the 3-sphere divided by the 120 icosians (the corners of the 600-cell,
  DICTO's White Queen). a(n) = number of independent vibration modes of degree k = 2n there (multiplicity of the Laplace
  eigenvalue k(k+2)); odd degrees have none. Its gaps (nothing in degrees 1 to 11) are why the space was proposed for the
  missing large-scale patterns of the microwave sky.
- **Terms, n = 0..100 (k = 2n):** 1, 0, 0, 0, 0, 0, 13, 0, 0, 0, 21, 0, 25, 0, 0, 31, 33, 0, 37, 0, 41, 43, 45, 0, 49, 51,
  53, 55, 57, 0, 122, 63, 65, 67, 69, 71, 146, 75, 77, 79, 162, 83, 170, 87, 89, 182, 186, 95, 194, 99, 202, 206, 210, 107,
  218, 222, 226, 230, 234, 119, 363, 246, 250, 254, 258, 262, 399, 270, 274, 278, 423, 286, 435, 294, 298, 453, 459, 310,
  471, 318, 483, 489, 495, 334, 507, 513, 519, 525, 531, 358, 724, 549, 555, 561, 567, 573, 772, 585, 591, 597, 804
- **How computed, three ways (agree for k = 0..200), `scripts/pds.py`:** (A) (k+1) x [t^k] (1+t^30)/((1-t^12)(1-t^20))
  (the Molien series A008651); (B) Aurich, Lustig and Steiner's closed formula r(β), β = k+1 (their eqs. 26-27, as printed
  in the book's Theorem 3); (C) character average over the 9 conjugacy classes of the icosians in mpmath at 60 digits.
  The earlier study (2026-11-04-pds-modes) did (C) from DICTO's own 120 corners and matched (B) for k <= 120.
- **OEIS:** with zeros (1,0,0,0,0,0,13,0,0,0,21,0,25,...) not found; zeros removed (1,13,21,25,31,...,122,63) not found;
  122,63,65,67,69,71,146,75 not found; indexed by every k (1, eleven 0s, 13, ...) not found; keywords "Poincare dodecahedral",
  "dodecahedral space", "Poincare sphere" give no spectrum entry. A008651 (the Molien series) has no comment on it.
- **Source:** *Alicia in Wonderland: The Red & White Queens* (book), concept DOI 10.5281/zenodo.23753305, **Chapter 9
  "The Silent Queens", Theorem 3** (with the ALS formula; first published in v4, 7 Nov 2026; confirm the wording in the
  published version before drafting). Studies 2026-11-04-pds-modes, 2026-11-12-pds-hopscotch-line.
- **Fairness note:** the mathematics is classical (Klein's invariants; Ikeda's spectra of spherical space forms; Aurich,
  Lustig and Steiner 2005; Lachièze-Rey and Weeks). DICTO's part is the check from his own corners and the reading of the
  White Queen as the space's group. The entry should say so; prior art for the exact sequence (Ikeda 1980 and ALS) must be
  read before submission (not read in this sweep).

### 4. Slope of the great triangles of Kulaichev's Śrī Yantra (constant): READY, DICTO's call

- **What it is.** Under Kulaichev's conditions the Śrī Yantra is one exact figure (#103). Its two great triangles have equal
  leg slope u (half-width per depth from the apex, i.e. tan of the half apex angle), u = 0.75043851602221402440...,
  a root of an irreducible integer polynomial of degree 348.
- **Digits (offset 0):** 7, 5, 0, 4, 3, 8, 5, 1, 6, 0, 2, 2, 2, 1, 4, 0, 2, 4, 4, 0, 6, 0, 8, 4, 6, 5, 7, 0, 5, 1, 2, 3, 4,
  5, 1, 0, 3, 4, 0, 8, 9, 1, 0, 0, 3, 6, 3, 9, 7, 9, 0, 3, 1, 5, 4, 1, 5, 3, 1, 4, 3, 9, 1, 2, 5, 2, 1, 4, 6, 4, 4, 2, 3, 8,
  8, 1, 5, 4, 1, 4, 4, 6, 1, 8, 7, 3, 9, 4, 2, 9, 4, 2, 1, 9, 1, 1, 3, 8, 8, 1, 7, 7, 2, 2, 0 (105 digits)
- **How computed, two ways:** (A) `scripts/kulaichev_slope.py`: Newton on the degree-348 polynomial (paper data file
  kulaichev-minpoly-u.txt) at 160 digits from the paper's 40-digit isolating interval, then a strict sign change at
  u -/+ 10^-125; (B) independent earlier results: the yantra audit's exact rational sign-change refinement to width
  3·10^-1000 (study 2026-11-09-yantra-audit, stage1-K.json) agrees to 120 digits, and the 260-digit Newton solve of the
  geometric conditions without any polynomial (study 2026-11-08-sri-yantra, 60 stored digits) agrees to 60 digits.
- **OEIS:** 7,5,0,4,3,8,5,1,6,0,2,2,2,1,4,0,2,4 not found; keywords "Sri Yantra" and "yantra" match only A003401 (a passing
  mention, constructible polygons).
- **Source:** #103 *The DICTO Yantra: Two Exact Solutions*, concept DOI 10.5281/zenodo.24052633, **Theorem 10** (added in
  v2, published; the polynomial attached as kulaichev-minpoly-u.txt); uniqueness Theorem 14 is in the v5 draft.
- **Note:** DICTO dropped the yantra region *sequence* on 17 Nov ("thin ice"). This is a different object: one certified
  constant of a classical figure. Ask him whether he wants it queued. The OEIS field %F can only say "root of a degree-348
  polynomial (see link)".

### 5. Close-packed stackings by period and number of hexagonal layers (triangle): needs-home (and prior art)

- **What it is.** T(n,k) = number of close-packed stackings (polytypes) of exact period n with k hexagonal layers, up to
  shift and relabelling (rows sum to A011957); a second triangle with reversal (rows sum to A011768). k is always even.
- **Rows (without reversal), n = 2..14, k = 0, 2, 4, ...:** n=2: 0,1 · n=3: 1 · n=4: 0,1 · n=5: 0,1 · n=6: 0,1,1 ·
  n=7: 0,1,2 · n=8: 0,2,2,2 · n=9: 0,1,5,4 · n=10: 0,2,7,7,2 · n=11: 0,2,9,15,5 · n=12: 0,2,14,28,12,3 ·
  n=13: 0,2,19,42,35,7 · n=14: 0,3,22,76,70,24,3 (data: studies/2026-11-08-sequences/data-polytypes.txt).
- **How computed:** one way only (brute-force enumeration with canonical forms, polytypes.py); row sums reproduce A011957
  and A011768, which checks the enumeration. A second way (Burnside count weighted by h) is needed before submission, and
  more rows (20+ terms are there already, but the shape of the triangle must be fixed: rows from n = 1 or 2, which k).
- **OEIS:** flattened rows (1,1,1,1,1,1,1,2,2,2,2,1,5,4,2,7,7,2) not found; with reversal not found; row 14 (3,22,76,70,24,3)
  not found (also 8 Nov).
- **Source:** none published. Natural home: the Hexagonality Law papers (#68 *Real Polytypes and the Hexagonality Law*,
  #69) or *Laws of Stacking*. Prior art to check first: McLarnan (1981) and Iglesias, who count polytypes by period; they
  may give the split by hexagonality.

### 6. The 19-design station on the Queens' line (constant): needs-home

- **What it is.** On the line from the White Queen (600-cell) to the Red Queen (120-cell), exactly one stage's 1440 corners
  form a spherical 19-design, at μ* = 0.9241386732... (algebraic of degree 20).
- **OEIS:** 9,2,4,1,3,8,6,7,3,2 not found.
- **Source:** study 2026-11-12-pds-hopscotch-line; listed in the Concordance as "Geometry Gives Laws (draft)"; the Queens
  book prints only the numerical grid value 0.924165 ("numerical only"). Not in a published paper with its exact form.
- Digits were not recomputed in this sweep (it needs its home first).

---

## Considered and rejected

| Item | Source | Reason |
|---|---|---|
| Coordination sequences of 9R and other polytype sites (42 stackings in the loop checks) | #74, #102 data | same family as entries 2-5, not yet sent; serial/bulk submissions are against the OEIS AI policy (rule 0); wait for how 2-5 are received |
| Multiplet ladders: SU(4)/SO(7)/SO(9) dimensions at Fibonacci or Pell labels (64, 300, 2156, ...) | *Golden Ladder* ch. 2 | an arbitrary composition (Weyl dimension at chosen labels); the chapter's theorem is about the limit shape, not these numbers |
| Rhombohedra per cell of the cubic approximants 4F(3n+2), 4F(3n+1), 4F(3n+3) | #99 Theorem 3 table | multiples by 4 of A015448, A033887, A014445; at most a comment (below) |
| Three-valued part of N(n): 0, 12, 50, 210, 707, 2380, 7506 | #105, Paradigm ch. 12 | a summand of A402191's own formula; belongs in A402191 (formula/comment), not a new entry (not found in OEIS) |
| Self-avoiding polygons through a site, per stacking | #102 Theorem 5 | computed only to length 24 (fewer than 20 terms) and depends on the stacking; the stacking-blindness to length 16 goes in a comment on A038515 (below) |
| Yantra odd regions 7, 16, 29, 43 | 2026-11-17-yantra-sequence | finite (no rule past nine); DICTO dropped it 17 Nov |
| Slope of the DICTO Yantra, 0.67931858870677465738... (degree 160; not found in OEIS) | #103 Theorem 9 | fixed by DICTO's own choice of slope product (Cleo-Antonius); Kulaichev's slope (candidate 4) is the canonical one. DICTO may still want it; his call |
| Golden Cut Cube depths 1/(1+√2φ), 1/(1+√2/φ) (z⁴ − 8z³ + 4z − 1) | #90, *Golden Ladder* | constants of DICTO's own named solids; nothing but the construction makes them notable |
| Equal-volume point λ = 3/8 − ∛4/4 (Sonsam and Lahdeli); Delian root 0.3747 (16u³ − 36u² + 18u − 1) | #56, #51 | values of a sweep parameter that depend on how the sweep is coordinatised; the 0.3747 one is a negative side remark |
| Mahler maximum on the tetrahedron sweep, μ* = (11 − √33)/4 | #100 remark | sweep-parameter value in a side remark the paper itself says is not its result |
| PDS mode degrees 0, 12, 20, 24, 30, ... | Queens book | the support of candidate 3; one entry is enough |
| Vertices of the 600-cell by distance (1, 12, 20, 12, 30, 12, 20, 12, 1); Cleo shells | Queens book, #63 | finite, classical (Coxeter) |
| Corner counts along the growth rule T (92, 180, 212, ...), lotus spheres, seam removals | #79, #80, studies | float or tolerance-dependent, few terms (11-07 note) |
| Fibonacci/Lucas readout of volumes (8 of 78 = q·φ^n) | 2026-11-08-sequences | single numbers, not a sequence |
| Hard-core fermion counts on chains | fibonacci-stackings | known (Fendley et al.) |
| Eulerian sweep counts, ridges of the permutohedron | Paradigm ch. 12 | Eulerian numbers and ridge counts are already in the OEIS |

## Comments on existing entries

| Entry | Comment (facts only; DICTO writes the text, rule 0b) | Source | Readiness |
|---|---|---|---|
| A008651 (Molien series of 2I) | (k+1)·a(k) is the multiplicity of the eigenvalue k(k+2) on the Poincaré dodecahedral space; crossref candidate 3 | Queens book ch. 9 Thm 3 | with candidate 3 |
| A038515 (closed self-avoiding walks, diamond) | twice a(n) is the number of polygons through an atom; the same count holds at every atom of lonsdaleite and every close-packed stacking up to length 16, and first differs at length 18 (diamond 349236 per site, lonsdaleite 349128) | #102 v6 Theorem 5 | READY (check #102's wording of the factor 2 first) |
| A015448, A033887 | 4·a(n): prolate / oblate golden rhombohedra in the conventional cubic cell of the F(n+1)/F(n) approximant | #99 Theorem 3 table (6 rungs only; formula not printed; 11 rungs checked in study 2026-11-06-approximant-ladder) | needs-proof (and prior art: Elser-Henley-type work) |
| A402191 (DICTO's, in review) | the three-valued part (3^n − 3·2^n + 3 − A_n)/2: 0, 12, 50, 210, 707, 2380, 7506 | #105 Thm 3, Paradigm ch. 12 | after approval |
| A011957, A011768 | crossref to the hexagonality triangle (candidate 5) | none yet | needs-home |

## Files

- `scripts/pyrochlore.py`, `data/out-pyrochlore.txt` (candidates 1, 2; FINAL ok)
- `scripts/pds.py`, `data/out-pds.txt` (candidate 3; FINAL ok)
- `scripts/kulaichev_slope.py`, `data/out-kulaichev.txt`, inputs `data/input-kulaichev-minpoly-u.txt` (copy of the paper's
  data file), `data/input-kulaichev-u-1000-audit.txt` (from the yantra audit) (candidate 4; FINAL ok)
- `scripts/oeis_search.sh`, `scripts/queries.txt`, `data/oeis-searches.txt`, `data/oeis-searches-followup.txt`

All computation ran on the compute host; outputs were copied back here.
