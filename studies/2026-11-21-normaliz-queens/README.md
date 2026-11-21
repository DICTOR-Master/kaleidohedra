# The golden stations of the Queens, exactly (gap study, direction 5)

Study 2026-11-21. Gap study 2026-11-21-gap-study, direction 5; rows R4, L26, L33, L34, L37.
Engine: Normaliz with e-antic, exact polyhedral computation over Q(√5). All numbers below are exact (a + b√5).
The 600-cell and the 120-cell are DICTO's White Queen and Red Queen.

## 1. Engine (how to rerun)

On the compute host, without root:

    mkdir -p ~/opt && cd ~/opt
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj bin/micromamba
    MAMBA_ROOT_PREFIX=~/opt/mamba ~/opt/bin/micromamba create -y -p ~/opt/mamba/envs/normaliz \
        -c conda-forge python=3.12 normaliz pynormaliz
    ~/opt/mamba/envs/normaliz/bin/normaliz --version   # Normaliz 3.11.0, with Flint e-antic nauty

Python: `~/opt/mamba/envs/normaliz/bin/python` (PyNormaliz 2.24, libeantic 2.1.1, FLINT 3.5).
Field: Q(a), a² = a + 1 (a = φ), entered as strings such as `1/2*a+1`.

Scripts (`scripts/`, run from that folder):

| script | what | log |
|---|---|---|
| `qphi.py` | own exact Q(φ) numbers; parses Normaliz output; used to re-check every result independently | |
| `polys.py` | exact corners of the 600-cell (radius 2, as in #62) and the 120-cell (radius √8) | |
| `nz.py` | thin PyNormaliz wrapper (hull of points; polytope from inequalities and equations) | |
| `controls.py` | target 1 controls | `logs/controls.log` |
| `slices600.py` | target 2 (#62) | `logs/slices600.log` |
| `stations.py` | target 3: Lemma 6 of #91 for all μ; eleven stations; #76's builds | `logs/stations.log` |
| `atlas76.py` | target 3: #76's atlas, exact (spawn pool; forked workers deadlock in Normaliz) | `logs/atlas76.log` |

Engine caveat found: on a two-dimensional section (the pentagon at the tip of the 120-cell, pentagon direction)
`VerticesOfPolyhedron` returned 11 rows for a pentagon while the f-vector correctly said 5. Three-dimensional and
four-dimensional results were always consistent (vertex rows = f₀, Euler, independent recomputation). The atlas
therefore reads tip polygons from the f-vector, and every three-dimensional slice is checked for vertex rows = f₀.

## 2. Target 1: controls (FINAL ok)

| | corners | facets | corners per facet | f-vector | time |
|---|---|---|---|---|---|
| 600-cell | 120 | 600 | 4 (all) | 120, 720, 1200, 600 | 3 s |
| 120-cell | 600 | 120 | 20 (all) | 600, 1200, 720, 120 | 3 s |

Also exact: Normaliz returns exactly the input corner set; every corner lies inside every facet; the polar points of
each solid's facets lie on one sphere with the cosine pattern of the other solid's corners (duality);
inradius² = (7 + 3√5)/4 (600-cell, radius 2) and (7 + 3√5)/2 (120-cell, radius √8): the same ratio r²/R² = (7 + 3√5)/16.

## 3. Target 2: #62, the all-triangle slices of the 600-cell (gap L37)

Method. The slice x·d = h can change pattern only where the hyperplane passes a corner (an incidence event). Slicing
at every corner height and at the midpoint of every interval between neighbouring heights therefore gives every
pattern that occurs. d is the centroid of a corner, an edge, a triangle or a cell (#62's convention, so heights compare
directly). 58 slices from the centre to the tip (8 + 16 + 20 + 14), each from the 600 facet inequalities and one
equation, each re-checked: Normaliz's corners equal an independent construction (corners at height h plus the
crossings of edges strictly across h); Euler V − E + F = 2. 25 s in all.

Result (exact; −h gives the mirror slice; h/(d·d) is the fraction of the way from the centre to the element's centroid):

| direction | h | h/(d·d) | corners, edges, triangles | in #62 |
|---|---|---|---|---|
| vertex-first | −(1 + √5) | −φ/2 | 12, 30, 20 | icosahedron (corner layer) |
| vertex-first | −2 | −1/2 | 32, 90, 60 | dodecahedron height (32, 60) |
| vertex-first | 1 − √5 | −1/(2φ) | **72, 210, 140** | V72 at ±(√5 − 1) |
| vertex-first | 0 | 0 | 42, 120, 80 | central slice (42, 80) |
| edge-first | −(1 + √5) | −2/√5 | 17, 45, 30 | Shadow-17 |
| edge-first | −(3 + √5)/2 | −(5 + √5)/10 | **32, 90, 60** | V32 at ±(3 + √5)/2 |
| face-first | −(4 + 2√5)/3 | −φ/2 | **30, 84, 56** | V30 at ±(4 + 2√5)/3 |
| cell-first | −(5 + 3√5)/4 | −(3√5 − 5)/2 | **28, 78, 52** | V28 at ±(5 + 3√5)/4 |
| cell-first | −(3 + √5)/2 | −2/φ² | **42, 120, 80** | V42 at ±(3 + √5)/2 |
| cell-first | −(2 + √5)/2 | −1/φ | **48, 138, 92** | V48 (Slice-48) at ±(2 + √5)/2 |

plus, in every interval next to a vertex-first tip, the vertex figure (an icosahedron). Every other slice in the four
directions has four-sided faces (data/slices600.json lists all 58 with their faces by sides).

Verdict L37: CLOSED. The six large all-triangle slices (bold) have exactly the heights and counts of #62 §6, now
confirmed by a second, independent exact engine, and the full event sweep shows that in the four main directions
all-triangle slices occur ONLY at corner heights: no interval between two incidence events is all-triangle except the
vertex-figure caps. In units of the distance to the element's centroid the heights are golden: the 42- and 48-corner
cell-first slices sit at 2/φ² and 1/φ, the 72-corner slice at 1/(2φ), the 30-corner slice at φ/2.
Proposed home: #62 next version, one sentence in §6 (the event sweep and the golden fractions; "the list is complete in
the four directions").
Prior art: Dutour Sikirić and Myrvold, "The special cuts of 600-cell" (arXiv:0708.3443, abstract read freely)
enumerate the 314,248,344 polytopes obtained by removing independent sets of corners from the 600-cell (Blind and
Blind's last class of regular-faced polytopes). They do not treat hyperplane slices; no overlap with #62's slices.

## 4. Target 3: #91 Lemma 6 and the #76 stations (gaps R4, L33, L26)

Frame: the 600-cell P with circumradius 1 (corners V/2), P = {N·x ≤ 1} over its 600 face poles N, P* = conv(N) the
120-cell, and the sweep S(μ) = P ∩ μP*, r² = (7 + 3√5)/16 ≤ μ ≤ 1 (#91, Section 6).

### 4A. Lemma 6, proved for every μ (no longer "checked at three points")

Cell rule (identity in the facet frame).
- On a facet N·x = 1 of P (a tetrahedron T, centre c = N/|N|², |c|² = r²): with x = c + y, v·x = r² + (v − c)·y,
  so the corner constraints of T's own four corners give T ∩ (μ − r²)·T*: the T·T sweep with μ₃ = μ − r² (linear in μ).
- On a facet v·x = μ of μP* (a dodecahedron μD, centre μv): with x = μ(v + z), N·x = μ(1 + (N − v)·z), so the
  constraints of D's own 20 poles give μ·(D ∩ (1/μ − 1)·D*): the D·I sweep with parameter 1/μ − 1 (linear in 1/μ).

This is the whole of Lemma 6 provided no other constraint cuts the cell. That proviso is settled for all μ at once:
lift μ to a fifth coordinate. Q = {(x, μ): x on the facet, own cuts, r² ≤ μ ≤ 1} is a polytope; a foreign
constraint is redundant for every μ iff it holds at every corner of Q (exact, Normaliz):

| cells | corners of the lifted Q | max of the foreign constraints over Q | verdict |
|---|---|---|---|
| tetrahedral (facets of P) | 15 | w·x − μ ≤ −1/4 + √5/12 ≈ −0.0637 | redundant, never touching |
| dodecahedral (facets of μP*) | 63 | N·x − 1 ≤ −7/8 + 3√5/8 ≈ −0.0365 | redundant, never touching |

Theorem (Lemma 6 for the 600-cell × 120-cell family, exact). For every μ in [r², 1] each cell of S(μ) on a facet of
P is the T·T-sweep member T ∩ (μ − r²)T*, and each cell on a facet of μP* is μ times the D·I-sweep member
D ∩ (1/μ − 1)D*. Consequently Proposition 7 of #91 (the two DICTO All-Golden Polytopes at μ = 2 − √5/2 and
(19 + 9√5)/44) is proved exactly, not only from a rule checked at three points.

### 4B. The stations, built exactly

Each station: S(μ) from its 720 inequalities by Normaliz; f-vector; cells by corner count; all edge lengths (edges
found as pairs of corners on three common facets, count = f₁); all corners on one sphere; the cell on one facet of P
and on one facet of μP* recomputed from the facet's OWN constraints only and compared corner for corner (Lemma 6,
directly); each cell's three-dimensional sweep value ν₃ = μ₃/r₃² read against #91's T·T and D·I tables
(ν = 1 dual end; T·T: −T 1, Lesser GCT 15 − 6√5, truncated 9/5, Greater GCT (9 + 6√5)/11, octahedron 3,
Greater GCT 6√5 − 9, truncated 5, Lesser GCT 3 + 6/√5, T 9; D·I as #91 Table 1). ν₃ below 1 means the cell is a
scaled copy of the dual end (an icosahedron, or a tetrahedron −T). 411 s for all eleven.

| station | μ (R = 1) | f-vector | tetrahedral-facet cell (ν₃) | dodecahedral-facet cell (ν₃) | edges |
|---|---|---|---|---|---|
| truncated 600-cell, uniform | (9 + √5)/12 | 1440, 4320, 3600, 720 | truncated tetrahedron (5) | icosahedron ((10 + √5)/19 < 1) | one length |
| rectified 600-cell | (5 + √5)/8 | 720, 3600, 3600, 720 | octahedron (3) | icosahedron (1) | one length |
| bitruncated, uniform midpoint | (11 + 3√5)/20 | 3600, 7200, 4320, 720 | truncated tetrahedron (9/5) | truncated icosahedron ((30 − 3√5)/19) | one length |
| rectified 120-cell | (3 + √5)/6 | 1200, 3600, 3120, 720 | tetrahedron (1) | icosidodecahedron (3 − φ) | one length |
| truncated 120-cell, uniform | (15 + 8√5)/38 | 2400, 4800, 3120, 720 | tetrahedron ((6√5 − 3)/19 < 1) | truncated dodecahedron (2√5 − 3) | one length |
| golden | (13 + 5√5)/28 | 2400, 4800, 3120, 720 | tetrahedron (3/7) | **Lesser GCD** ((50 − 15√5)/11) | two, ratio φ |
| golden | (111 + 45√5)/244 | 2400, 4800, 3120, 720 | tetrahedron | **Greater GCD** ((20 − 7√5)/3) | two, ratio φ |
| golden, Prop 7 | 2 − √5/2 | 3600, 7200, 4320, 720 | **Lesser GCT** (15 − 6√5) | **Greater GCI** ((5 + 4√5)/11) | two, ratio φ |
| golden, Prop 7 | (19 + 9√5)/44 | 3600, 7200, 4320, 720 | **Greater GCT** ((9 + 6√5)/11) | **Lesser GCI** (5√5 − 10) | two, ratio φ |
| golden | 3(√5 − 1)/4 | 1440, 4320, 3600, 720 | **Greater GCT** (6√5 − 9) | icosahedron (√5/3 < 1) | two, ratio φ |
| golden | (5 + 2√5)/10 | 1440, 4320, 3600, 720 | **Lesser GCT** (3 + 6/√5) | icosahedron (5 − 2√5 < 1) | two, ratio φ |

All eleven: corners on one sphere; Lemma 6 direct check true at both facets. Cells: 720 at every station
(600 + 120). #91 Table 2's six golden values and their cell names are all confirmed exactly (the
"floating point" in that table's caption can go), and at each golden station the solid has exactly two edge lengths in
the ratio φ.

#76 Table 1 against the sweep (corner for corner, exact): the truncated 600-cell built 1/3 along each edge (1440
corners), the bitruncated midpoint built 3/5 from each triangle edge's middle to its centre (3600) and the truncated
120-cell built (5 − √5)/10 along each 120-cell edge (2400) are IDENTICAL to S((9 + √5)/12), S((11 + 3√5)/20) and
S((15 + 8√5)/38) (the first two at scale 1, the third at scale (22√5 − 30)/19, because #76 builds the 120-cell from cell
centres). So the "exact, cross-links study" statement of #91 Section 6 now has its corner-for-corner proof.

### 4C. #76's atlas, exact (gap L26)

Every stage S(μ) (§4B shows they are #76's solids), the four directions of #76, slices at every corner height and
halfway between, from the centre to the tip; each three-dimensional slice from 720 inequalities and one equation;
corners, edges, faces by sides; Euler and "vertex rows = f₀" on every slice; shadows as exact hulls of the projected
corners. 1587 slices (ends included) and 28 shadows in 314 s on 8 workers; 0 failing checks
(data/atlas76.json, logs/atlas76.log).

| solid | slices v·e·f·c | all | patterns v·e·f·c | shadows corners/faces v·e·f·c |
|---|---|---|---|---|
| 600-cell | 9·17·21·15 | 62 | 7·15·19·14 | 42/80 · 52/80 · 56/96 · 44/78 |
| truncated 600-cell | 29·85·103·**72** | **289** | 21·77·98·**63** | 192/110 · 280/232 · 312/272 · 240/194 |
| rectified 600-cell | 17·**37**·49·33 | **136** | 16·35·49·33 | 132/110 · 150/232 · 168/272 · 144/194 |
| bitruncated | 43·135·175·125 | 478 | 23·110·151·97 | 240/122 · 580/312 · 636/368 · 504/266 |
| rectified 120-cell | 21·49·65·45 | 180 | 14·46·60·41 | 140/102 · 260/252 · 282/296 · 240/242 |
| truncated 120-cell | 33·87·117·81 | 318 | 12·69·96·62 | 200/102 · 500/252 · 564/296 · 480/242 |
| 120-cell | 15·33·45·31 | 124 | 8·29·40·24 | 80/42 · 160/92 · 180/104 · 158/84 |

Against #76 Table 2: every shadow (28) and every entry agree except two (bold), both traced to the float atlas
(study 2026-10-30-queen-stages, stages_atlas.json):
- rectified 600-cell, edge-first: 37, not 39. The float list holds the corner height 0.447214 (normalised) three
  times; the exact list has it once. Patterns unchanged (35).
- truncated 600-cell, cell-first: 72, not 71, and 63 patterns, not 62. 0 is not a corner height there, and the float
  list starts at the first corner height 0.029083, so it lacks the central slice (halfway between ±0.029): 240
  corners, 408 edges, 170 faces (24 triangles, 78 four-sided, 48 five-sided, 8 nine-sided, 12 ten-sided), a pattern
  of its own.
So Theorem part (1) of #76 reads, exactly: 289, 136, 478, 180 and 318 slices from the centre to the tips, 1401 in all
(not 1402). Part (2) is confirmed (62 and 124). Part (3) is confirmed with exact shadows: 110, 232, 272, 194 and
102, 252, 296, 242.

## 5. Target 4: #89's "no section" claim for the ten Schläfli–Hess star polytopes (gap L34)

Not run tonight (the night's budget went to targets 1 to 3). Method ready, see LEADS 1. Verdict L34: OPEN.

## 6. Verdicts and proposed homes

| gap | verdict | numbers | proposed home |
|---|---|---|---|
| L37 (#62) | CLOSED | the six large all-triangle slices at exactly #62's heights, confirmed by a second exact engine; full event sweep: no other all-triangle slice in the four directions (§3) | #62 next version, §6: one sentence and the golden fractions 1/(2φ), φ/2, 2/φ², 1/φ |
| R4 / L33 (#91 Lemma 6) | CLOSED | Lemma 6 proved for every μ in the 600-cell × 120-cell family (lifted-polytope redundancy, margins −1/4 + √5/12 and −7/8 + 3√5/8); Proposition 7 now exact; all six golden values and their cells exact; the three uniform members equal #76's builds corner for corner (§4A, §4B) | #91 next version: Lemma 6 becomes a theorem for this family (proof as §4A, about six lines); Table 2 caption drops "floating point" for this row; Proposition 7 "from Lemma 6" becomes "by Theorem 6" |
| L33, other parts (tilted slice, off-base prism sections, TRD outside the cubic sweep, 342/171) | OPEN | not touched tonight | #91 |
| L26 (#76) | CLOSED, with a correction | exact atlas in Q(√5); 1401 slices, not 1402 (rectified 600-cell edge-first 37; truncated 600-cell cell-first 72 and 63 patterns); shadows and part (3) confirmed exactly (§4C) | #76 Version 3: Table 2 two cells, the total, the patterns count, "exact in Q(√5) (Normaliz with e-antic)" in the proof; "Next: an exact version" can go. Part (3)'s proof stays open (LEADS 4) |
| L34 (#89, #91) | OPEN | not run (§5) | #89 next version once done |

## 7. LEADS

1. L34 exactly. Along the 600-cell corner axis (the only direction whose stabiliser contains the icosahedral group),
   for each of the 38 chord classes the corners of a section are chord crossings, each affine in the height h, so they
   fall into icosahedral orbits whose positions are affine in h between incidence events. Matching a golden
   Kepler–Poinsot cut (Proposition 4 of #89; 60 or 12 + 60 corners) scale-free is then one polynomial equation per
   orbit parameter in h over Q(√5): solve per interval and per event height, exactly. The star polytopes' flags are
   exact in study 2026-11-09-regular-stars-census (data/flags.json).
2. Lemma 6 for the other pairs. The lifted-polytope test of §4A is general: it proves the cell rule of any regular
   pair P ∩ μP* in one Normaliz run per cell type (tesseract × 16-cell and 24-cell × 24-cell are rational: two more
   runs close "checked exactly at stations" for them too).
3. The 5-cell × 5-cell and the 16-cell × tesseract sweeps' golden stations exactly, the same way (§4B), to complete
   #91 Table 2 with exact cell names.
4. #76 Theorem part (3), a proof: with the atlas exact, the equal face counts of the paired shadows (truncated and
   rectified 600-cell; rectified and truncated 120-cell) can be read face by face; the cells on facets of P go from
   truncated tetrahedra to octahedra while the outline's faces keep their number; check whether each shadow face of
   the one maps to a face of the other along the sweep (shadow faces as functions of μ between events).
5. The full event sweep of #62 in non-principal directions (for example the 2-fold axes of the cell-first frame):
   the exact engine now makes a direction scan cheap (25 s for the four main ones).
