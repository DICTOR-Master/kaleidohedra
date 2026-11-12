# The balance law for rosette tissues (13 Nov 2026; The Permutohedron Paradigm, Open question 8.2)

**Conclusion (13 Nov 2026): every rosette tissue of the Atlas balances exactly, class by class and in every direction (Theorem 2,
PROVED for every Wythoff polytope of every finite reflection group); for rosette tissues without that symmetry the balance law is
FALSE (exact counterexample: a moved 16-cell, Section 4), and no face-lattice invariant (toric h-vector, cd-index, flag vector)
can restore it. What every rosette tissue keeps is the conservation law of Proposition 3.**

Script `scripts/rosette_balance.py` (logs `data/rosette-pilot.log`, `data/rosette-full.log`; data `data/rosette-pilot.json`,
`data/rosette-full.json`), invariants `scripts/invariants.py` (log `data/invariants.log`). Compute node through the job gate
(jobs rosette-pilot, rosette), 6 worker processes, about 1 min, FINAL ok. **Exact arithmetic throughout** (rationals; Q(sqrt5) for
H4); no floating point decides anything.

## 1. The question (Chapter 8, Section 8.2, as drafted)
"A rosette at a corner with e edges is a bistellar move on more than four cells at once. Which of its exchanges balance, and whether
a rosette tissue has a balance law of its own, is open; the Atlas gives the ledger of every clean tissue, and the same sweeps on the
rosette tissues are the next computation."

Cited there: Chapter 7 (Theorem 7.1, the balance law Theorem 7.4, Lemma 7.3), #104 (Lemma 5), #108 Theorem 1 and Section 4
(study `studies/2026-11-11-orbit-polytopes`, `balance_formula.py`), Chapter 8 check `studies/2026-11-11-paradigm-ch8`
(`simple_rule.py`).

## 2. Words
Sweep a 4-polytope P by a height u that is generic (no edge horizontal). At a corner v let D be its edges going down and U those
going up. Faces through v are read on the corner figure (vertices = edges at v, edges = 2-faces at v, faces = cells at v):
a 2-face (contact) is **lost** at v iff both its edges at v are in D, **made** iff both are in U; a cell **dies** at v iff all its
edges at v are in D, is **born** iff all are in U. The **event** at v is (|D|; kinds of contacts lost; kinds made; types of cells
dying; types born), kinds and types as in #108 (a cell's type = the node of its fundamental weight; a contact's kind = the pair of
types of its two cells). Its **reverse** swaps D and U (lost with made, dying with born). The **fine class** of an event is the
orbit of D under the corner's stabiliser. The **ledger** of a sweep is the multiset of the events at all corners. A **rosette
tissue** is a sweep of a non-simple polytope (more than four edges at a corner). For a simple polytope the events are births (i = 1),
swaps (i = 2) and deaths (i = 3) of Chapter 7, and "balanced" is #108 Theorem 1.

## 3. Results

**Lemma 1 (one ledger per polytope; PROVED).** Let P be the Wythoff polytope of a finite reflection group W (any seed, any
dimension). Every edge of P is parallel to a root. Hence the down-set at every corner depends only on the Weyl chamber of u, and
every generic sweep of P has the same ledger.

*Proof.* The edges at the corner wx are w[x, s_i x] for ringed i (and their W_U-images), and s_i x - x is a multiple of the root
alpha_i; so every edge direction is a multiple of a root. Two heights in the same chamber give every edge the same sign. For g in W,
the event at gv for gu is the image under g of the event at v for u, and g keeps cell types and contact kinds (they are W-orbits);
so ledger(gu) = ledger(u). W is transitive on chambers. (A height orthogonal to some root but to no edge is moved slightly
without changing any edge sign.) ∎

**Theorem 2 (the rosette balance law; PROVED).** In every generic sweep of a Wythoff polytope of a finite reflection group, every
event is matched by its reverse: for every class tau (coarse or fine), the corners with event tau are exactly as many as the corners
with the reverse event. In particular every rosette tissue of the Atlas (all 34 non-simple rows of A4, B4, F4, H4 in Section 5)
balances: each contact lost of kind X with Y made at a rosette corner is matched by a corner that loses Y and makes X with the same
births and deaths reversed.

*Proof.* Sweeping by -u turns D into U at every corner, so ledger(-u) = reverse of ledger(u). By Lemma 1, ledger(-u) = ledger(u). ∎

For the simple Wythoff rows this is a second proof of #108 Theorem 1 (the flow argument of #108 is still needed for simple polytopes
without symmetry, which Theorem 1 of #108 covers). Lemma 1 also explains why #104 and #108 found the same counts in every direction.

**Proposition 3 (what every rosette tissue keeps: the conservation law; PROVED).** For every 4-polytope (simple or not, any
symmetry) and every generic sweep: one corner has D empty and one has U empty; summed over the corners, the contacts of each kind X
made = the contacts of kind X lost = N_X (the 2-faces of kind X); the cells of each type t born = those dying = n_t; the up edges =
the down edges = f_1. In the toric form: with phi_v(x) = sum over the faces G with lowest corner v of g((P/G)*; x)(x - 1)^dim G,
sum_v phi_v(x) = h(P*; x), the toric h-vector of the dual (Stanley), the same in every direction and palindromic.

*Proof.* Every face has exactly one lowest and one highest corner; a face G has lowest corner v iff all its edges at v go up. The
toric sum is the toric h of the boundary complex of P* written face by face (face G of P = face of P* with lattice (P/G)*), grouped
by lowest corner; this is the decomposition by the line shelling of P* (Bruggesser-Mani), which Lee (2011) uses for his sweep
formulas. For a simple corner phi_v = x^|U|, the h-vector of Chapter 7. ∎ In four dimensions g((P/G)*) is 1 + (c_v - 4)x at a
corner (c_v cells at it), 1 + (n_e - 3)x at an edge in n_e cells, and 1 above; so the toric sum is a combination of the counts above:
it says nothing beyond them.

**Theorem 4 (no balance law for rosette tissues in general; EXACT COUNTEREXAMPLE).** The 16-cell with its corners moved to

    (10, 2, -1, 0), (-10, 1, 0, 1), (1, 8, -2, 0), (1, -10, 1, -1), (0, -2, 10, 2), (-1, 2, -9, -2), (-1, -2, 1, 9), (-2, -1, 1, -8)

has the face lattice of the 16-cell (each of the 16 sign-choice tetrahedra checked to be a facet exactly: the other four corners
strictly on one side), every corner a rosette (6 edges, 8 tetrahedra; one cell type). Swept
by the height -3x_1 + x_4, the corners stand at -30, -4, -3, -2, 1, 2, 12, 31 and the ledger is

| down edges | contacts lost | made | cells die | born | corners | reverse | corners with the reverse |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 12 | 0 | 8 | 1 | 6 down | 1 |
| 1 | 0 | 8 | 0 | 4 | **2** | 5 down | **1** |
| 2 | 1 | 5 | 0 | 2 | **0** | 4 down | **2** |
| 3 (a path) | 2 | 2 | 0 | 0 | 1 | itself | 1 |

Two corners give birth to four cells at once (one edge down; the corners at -4 and -3), but only one corner (at 12) lets four die;
no corner exchanges one contact for five (two down), but two corners (at 1 and 2) exchange five for one. The balance law fails.
(Hand check: the neighbours of a corner are all corners but its opposite; count the lower neighbours.)

In 8000 exact sweeps (40 moved 16-cells x 200 random directions) 4 were unbalanced; in 60 sweeps of 6 moved 600-cells (every corner
a rosette of 12 edges) 8 were unbalanced. The regular 16-cell and the regular 600-cell are balanced in every direction (Theorem 2).

**Corollary 5 (balance is not governed by the face lattice; PROVED).** The moved 16-cell above and the regular 16-cell have the
same face lattice, hence the same toric h-vector (1, 12, 14, 12, 1), the same flag vector and the same cd-index (Bayer-Klapper);
one is balanced in every direction, the other is not. So no combinatorial invariant (toric h-vector, cd-index, flag vector, or
anything else read from the face lattice) can force a non-simple sweep to balance. What governs the balance of a rosette tissue is
geometric: the symmetry of Theorem 2. The answer to "a non-simple sweep may be governed by the toric h-vector or the cd-index" is:
the toric h-vector governs the sweep's totals (Proposition 3), and nothing combinatorial governs its pairwise balance.

**Proposition 6 (the complete law of a 16-cell tissue; PROVED).** A corner figure of the 16-cell is an octahedron; a generic plane
splits it in one of 8 ways (each side connected): down edges 0, 1, 2, 3 as a triangle (T), 3 as a path (Q), 4, 5, 6, counts
N0..N6, NT, NQ. In every generic sweep of every polytope with the face lattice of the 16-cell:
N0 = N6 = 1, 4 N1 + 2 N2 + NT = 8 (births), NT + 2 N4 + 4 N5 = 8 (deaths), N1 + N2 + NT + NQ + N4 + N5 = 6, and
**N1 + N5 = NQ + 2** (corners where four cells are born or four die = pure double exchanges + 2). Such a sweep balances iff N1 = N5
(then N2 = N4). These are all the linear laws: the 8000 sweeps span the remaining 3 dimensions (`data/invariants.log`: nullspace
dimension 5 = rank of the counting laws).
*Proof.* Proposition 3 with f = (8, 24, 32, 16) and the 8 classes; the last law is (births + deaths)/2 - corners. ∎

**Observation 7 (computed, every Atlas rosette).** In the 600-cell, the 16-cell and the runcinated rows (1001) of A4, B4, F4, H4
no corner is a pure exchange (contacts lost and made with no cell born or dying). The truncated 600-cell (Lemma 7.3) has five
balanced pairs of classes: 119 / 2 corners where one icosahedron / three truncated tetrahedra are born (as many where they die),
118 corners trading one contact between truncated tetrahedra for three truncated-tetrahedron-icosahedron contacts and 118 the reverse, 109 and 109, 371 and 371.

## 4. The rosette ledgers (exact; full ledgers in `data/rosette-full.json`)

| group seed | polytope | corners | edges at a corner | cells at a corner (types) | toric h of the dual | event classes | pure-exchange corners |
|---|---|---|---|---|---|---|---|
| A4 0100 / 0010 | rectified 5-cell | 10 | 6 | 2+3 | 1, 6, 6, 6, 1 | 10 | 1 |
| A4 1010 / 0101 | cantellated 5-cell | 30 | 6 | 1+2+2 | 1, 16, 26, 16, 1 | 18 | 5 |
| A4 1001 | runcinated 5-cell | 20 | 6 | 1+3+3+1 | 1, 26, 46, 26, 1 | 16 | 0 |
| A4 1101 / 1011 | runcitruncated 5-cell | 60 | 5 | 1+1+2+1 | 1, 26, 66, 26, 1 | 18 | 14 |
| B4 0001 | 16-cell | 8 | 6 | 8 | 1, 12, 14, 12, 1 | 7 | 0 |
| B4 0010 | 24-cell (rectified 16-cell) | 24 | 8 | 4+2 | 1, 20, 30, 20, 1 | 15 | 2 |
| B4 0011 | truncated 16-cell | 48 | 5 | 4+1 | 1, 20, 54, 20, 1 | 10 | 12 |
| B4 0100 | rectified tesseract | 32 | 6 | 2+3 | 1, 20, 22, 20, 1 | 10 | 4 |
| B4 0101 | cantellated 16-cell | 96 | 6 | 2+2+1 | 1, 44, 102, 44, 1 | 18 | 24 |
| B4 1001 | runcinated tesseract | 64 | 6 | 1+3+3+1 | 1, 76, 166, 76, 1 | 16 | 0 |
| B4 1010 | cantellated tesseract | 96 | 6 | 1+2+2 | 1, 52, 86, 52, 1 | 18 | 16 |
| B4 1011 / 1101 | runcitruncated 16-cell / tesseract | 192 | 5 | 1+2+1+1 / 1+1+2+1 | 1, 76, 230, 76, 1 | 18 | 52 |
| F4 1000 / 0001 | 24-cell | 24 | 8 | 6 | 1, 20, 30, 20, 1 | 10 | 2 |
| F4 0100 / 0010 | rectified 24-cell | 96 | 6 | 2+3 | 1, 44, 102, 44, 1 | 10 | 24 |
| F4 1010 / 0101 | cantellated 24-cell | 288 | 6 | 1+2+2 | 1, 140, 294, 140, 1 | 18 | 76 |
| F4 1001 | runcinated 24-cell | 144 | 8 | 1+4+4+1 | 1, 236, 534, 236, 1 | 25 | 0 |
| F4 1011 / 1101 | runcitruncated 24-cell | 576 | 5 | 1+2+1+1 | 1, 236, 678, 236, 1 | 18 | 148 |
| H4 0001 | 600-cell | 120 | 12 | 20 | 1, 596, 846, 596, 1 | 14 | 0 |
| H4 0010 | rectified 600-cell | 720 | 10 | 5+2 | 1, 716, 1446, 716, 1 | 21 | 22 |
| H4 0011 | truncated 600-cell | 1440 | 6 | 5+1 | 1, 716, 2886, 716, 1 | 12 | 236 |
| H4 0100 | rectified 120-cell | 1200 | 6 | 2+3 | 1, 716, 966, 716, 1 | 10 | 272 |
| H4 0101 | cantellated 600-cell | 3600 | 6 | 2+2+1 | 1, 1436, 4326, 1436, 1 | 18 | 1236 |
| H4 1001 | runcinated 120-cell | 2400 | 6 | 1+3+3+1 | 1, 2636, 6726, 2636, 1 | 16 | 0 |
| H4 1010 | cantellated 120-cell | 3600 | 6 | 1+2+2 | 1, 1916, 3366, 1916, 1 | 18 | 600 |
| H4 1011 / 1101 | runcitruncated 600-cell / 120-cell | 7200 | 5 | 1+2+1+1 / 1+1+2+1 | 1, 2636, 9126, 2636, 1 | 18 | 2164 |

Every row: the ledger is identical in all directions tried (3; H4 2), every class and every fine class is matched by its reverse,
and the corner-by-corner toric sum equals the global formula. (Pure exchange: contacts both lost and made, no birth or death.)
Example, the rectified 5-cell (10 corners, one in each of its 10 classes; tetrahedra type 1, octahedra type 4): the two classes
with three edges down are their own reverses: "lose 3 tetrahedron-octahedron contacts, make 3, one tetrahedron dies and one is
born" and the pure exchange "lose a tetrahedron-octahedron and an octahedron-octahedron contact, make the same kinds".

## 5. Controls (all ok)
POSITIVE: the classical h-vectors and the swap ledgers of Chapter 7 and #108 come out exactly: 4D permutohedron (A4 1111)
h = (1, 26, 66, 26, 1), swaps 6 / 16 / 11 each way; bitruncated 600-cell (H4 0110) (1, 716, 2166, 716, 1), 601 each way and 964
mixed (Theorem 7.4); truncated 120-cell 483 each way; 120-cell (1, 116, 366, 116, 1); bitruncated 24-cell 73 and 52; 5-cell
(1, 1, 1, 1, 1); tesseract (1, 4, 6, 4, 1) (these seven checked by the script; the other simple rows are in the log, and the A4
and B4 rows and the omnitruncated 120-cell agree with the #108 table, compared by eye). Every row: the edge count of Theorem 8.1
asserted; Euler for the corner figure and for the f-vector; each 2-face in exactly two cells; each cell's faces at the corner equal
its edges there. The toric h of the dual of the 16-cell, (1, 12, 14, 12, 1), was also computed by hand from the tesseract's faces.
NEGATIVE: the moved 16-cells and 600-cells, without symmetry, break balance (Theorem 4), while the toric sum still holds in every
one of their sweeps.
Faults on the way: the full run first stopped at the witness search (a function defined after the main block); moved, rerun, ok.

## 6. Proposed text for Chapter 8, Section 8.2 (for DICTO's read; the book itself is not edited here)
"8.2 The balance law of the rosettes. Every edge of a Wythoff polytope points along a root, so the height that sweeps it matters
only through its chamber, and every sweep has the same ledger of corner events (Lemma 8.2). Reversing the height reverses every
event; hence (Theorem 8.3) in every rosette tissue of the Atlas each rosette move is matched by its reverse, class by class, in every
direction: the truncated 600-cell trades one contact between truncated tetrahedra for three truncated-tetrahedron-icosahedron contacts at 118 corners and
back at 118.
The law needs the symmetry: a 16-cell with its corners moved slightly has a sweep with two corners where four cells are born at once
and only one where four die. Its face lattice, toric h-vector and cd-index are those of the regular 16-cell, so no combinatorial
invariant decides the balance; what every rosette tissue keeps is conservation: each contact is made once and lost once, each cell
born once and dies once, and the corner-by-corner sum of these is the toric h-vector of the dual (Stanley; Lee 2011)."

## LEADS
1. Closed formulas for the rosette ledgers (as in(X) of #108): a W-descent statistic over minimal coset representatives (D at the
   corner wW_U = the edge roots beta with w beta positive); the omnitruncated case is the Eulerian / W-Eulerian distribution.
2. Weaker symmetry: Theorem 2 needs only a type-keeping symmetry g with g(-u) in the edge-chamber of u; central symmetry suffices
   (all of B4, F4, H4). Which non-uniform polytopes (zonotopes, Minkowski sums of Wythoff polytopes) balance?
3. Observation 7 as a theorem: why the 600-cell, the 16-cell and the runcinated rows have no pure-exchange corner (every plane split
   of their corner figure leaves a whole face on one side).
4. Higher dimensions: Theorem 2 holds for every d; the rosette ledgers of the 5D Wythoff polytopes (Theorem 7.1' indices).
5. Lee's local cd-index terms per corner: compare with the event classes (they too can only constrain totals, by Corollary 5).

## Sources checked
Chapter 7 and Chapter 8 drafts (papers/paradigm-ch07, papers/paradigm-ch08); #104 (papers/2026-11-10-scutoids-4d) and #108
(papers/2026-11-11-atlas-chains, studies/2026-11-11-orbit-polytopes: balance_formula.py); studies/2026-11-11-paradigm-ch8
(simple_rule.py). Reference library queries: "toric h-vector cd-index sweeping hyperplane shelling nonsimple polytope" and "edges
of Wythoff polytope parallel to roots, Weyl chamber, descent statistics" (no matching source). Web: C. W. Lee, Sweeping the cd-index
and the toric h-vector, Electron. J. Combin. 18 (2011) P66, doi:10.37236/553 (abstract: formulas for the cd-index and toric
h-vector from a sweep, via an S-shelling of the dual; his local terms were not reproduced here); a web search for direction-
independent corner statistics of Wythoff polytopes (found only that permutohedra and M-convex polytopes have edges along roots,
arXiv math/0407527, 2608.16090, math/0609809; no statement of Lemma 1 or Theorem 2). Classical: R. P. Stanley, Generalized
h-vectors, intersection cohomology of toric varieties, and related results (1987) (toric h, its symmetry); M. M. Bayer and
A. Klapper, A new index for polytopes, Discrete Comput. Geom. 6 (1991) 33-47 (cd-index); H. Bruggesser and P. Mani (1971) (line
shellings); J. E. Humphreys, Reflection Groups and Coxeter Groups (1990) (chambers, parabolic subgroups); P. McMullen (1970).
Lemma 1 and Theorem 2 are elementary; we found them stated nowhere, and treat them as likely folklore for the permutohedron
(descents) and new in the tissue reading.

DICTO · dictospheres.com
