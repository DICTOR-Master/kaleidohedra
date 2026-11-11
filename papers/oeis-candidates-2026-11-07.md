# OEIS candidates from DICTO's research (7 November 2026)

Working list, not submitted. Nothing was sent to the OEIS. Every term below was recomputed with exact integers by
`studies/2026-11-07-oeis-candidates/oeis_checks.py` (output `data-oeis-terms.txt`, runs in about 30 s on the Pi, `FINAL ok`).
OEIS searches: 35 queries of the form `https://oeis.org/search?q=<terms>&fmt=json`, at most one every 3.5 s (list at the end).
"No hits" means no hits for those terms on 7 November 2026.

Ranking: new + well defined + many terms first, then comments/cross-references to existing entries, then finite or weak ones.

---

## 1. NEW. Closed non-backtracking walks per vertex of the diamond net (DICTO's Loop Equality)

**Definition.** a(n) = number of closed, cyclically non-backtracking (tailless) walks of length 2n that start and end at a
fixed vertex of the diamond net, i.e. (1/|V|) tr B^(2n) for the Hashimoto edge matrix B. Odd lengths give 0 (the net is bipartite).

**Terms, n = 1..30:** 0, 0, 24, 48, 480, 3432, 25704, 194256, 1509072, 11820000, 93722376, 750276792, 6056400480,
49241424120, 402912569544, 3315331754256, 27416593190640, 227742362372496, 1899436965599880, 15899758239277008,
133535586308211888, 1124913591689189016, 9502705513658774712, 80479398557955246744, 683197069729669127280,
5812393836160495572768, 49550028744917267304936, 423205902089422578373512, 3620959145374601760171744,
31032025217056871607341592

**OEIS:** no hits for 24,48,480,3432,25704,194256,1509072, nor for 24,48,480,3432,25704, nor for the halved form
12,24,240,1716,12852,97128. **New.**

**Source.** Study 2026-10-28-pyrochlore-kagome (loops2.py, loops2.out); paper #74 *Halves and Loops in Magnets*
(papers/magnets, DICTO DOI 10.5281/zenodo.23730421), §3 "The Loop Equality"; book *Laws of Stacking*
(DICTO DOI 10.5281/zenodo.23731359).

**How checked.** Two independent ways that agree term by term for lengths 6..34:
(a) DICTO's direct count (loops2.py: sparse propagation on a 36 x 36 x 36+ cell, five stackings 3C, 2H, 4H, 6H, 9R);
(b) the Ihara–Bass formula for a 4-regular graph, per vertex
Σ N_m u^m/m = −log(1−u²) − E[log(1 − λu + 3u²)], with the moments E[λ^(2k)] = the Domb numbers A002895
(closed walks on diamond). (b) gives the terms beyond 34.

**Formula for the entry:** from A002895 by the Ihara–Bass transform above.

**What arose on the way (for DICTO; changes the status of the Loop Equality).**
- Ordinary closed walks are also identical: at **every site** of 3C, 2H, 4H and 6H the number of closed walks of length
  0..30 equals the Domb numbers (computed). Through Ihara–Bass this is equivalent to the Loop Equality (per site averaged).
- A short argument seems to prove it for **every** close-packed tetrahedral stacking and every length: in Fourier space over the
  shared in-plane lattice, each crossing of the bond layer between bilayers k and k+1 contributes g(θ) going up and its complex
  conjugate going down; the stacking only decides whether g(θ) or g(−θ) = conj g(θ) is used, so a closed walk, which crosses
  each bond layer equally often both ways, carries |g(θ)|^(2m) whatever the stacking. The vertical part is the same walk on a
  line for every site. Hence closed-walk counts, and by Ihara–Bass the non-backtracking loop counts, do not depend on the stacking.
  Status: argument written here only; to be checked and written out as a proof before #74 / *Laws of Stacking* changes
  "conjecture" to "theorem". Prior art not yet searched for this exact statement.
- The same argument applies to close-packed spheres; see candidate 2b.

**Possible companion (NEW):** the same count on the fcc net (12-regular, Ihara–Bass with q = 11 from A002899), lengths 3..24:
48, 264, 1680, 17016, 151872, 1401720, 13238400, 126357120, 1221557040, 11927724720, 117462513168, 1165493695464, ...
(no hits for 48,264,1680,17016,151872,1401720). By 2b the same holds for hcp and every close-packed stacking. This one is an
extension, not yet in a DICTO paper.

---

## 2. COMMENTS on existing entries: closed walks do not see the stacking

**2a. A002895 (Domb numbers: 2n-step polygons on the diamond lattice).** Proposed comment: "Also the number of closed 2n-step
walks from any vertex of lonsdaleite (wurtzite net, A008264) and of every close-packed tetrahedral polytype (4H, 6H, ...)."
Checked: every site of 3C, 2H, 4H, 6H, lengths 0..30 (oeis_checks.py C2). The A002895 entry (fetched 7 Nov) has no such
comment and no lonsdaleite cross-reference. Proof sketch as in 1.

**2b. A002899 (n-step polygons on the f.c.c. lattice).** Proposed comment: "Also the number of closed n-step walks from any sphere
of the hexagonal close packing and of every close-packed stacking." Checked: every sphere of fcc, hcp and dhcp (ABAC), lengths
0..12 (C2b): 1, 0, 12, 48, 540, 4320, 42240, 403200, 4038300, 40958400, 423550512, 4434978240, 46982827584. The A002899 entry has
no hcp comment.

Source: as in 1 (the Loop Equality of #74 and *Laws of Stacking*). Both comments need the proof of 1 written out first; until then
they can only say "computed for n <= ...".

---

## 3. NEW. Coordination sequences of the 4H and 6H diamond polytypes (one sequence per site)

**Definition.** a(n) = number of atoms at graph distance n from a given atom of the tetrahedral (SiC-type) network on the
4H stacking ABAC (= ABCB) or the 6H stacking ABCACB; one sequence per inequivalent site. Site labels below: bilayer letter,
Jagodzinski type of that layer (h if its two neighbouring layers have the same letter), atom 0 = lower, 1 = upper of the bilayer.

| Site | Terms n = 0..30 (61 terms computed) | OEIS |
|---|---|---|
| 4H, A (c) | 1, 4, 12, 25, 44, 67, 96, 130, 170, 214, 264, 319, 380, 445, 516, 592, 674, 760, 852, 949, 1052, 1159, 1272, 1390, 1514, 1642, 1776, 1915, 2060, 2209, 2364 | **= A008264 (lonsdaleite) for all 61 terms** |
| 4H, B (h) | 1, 4, 12, 24, 42, 66, 96, 130, 170, 214, 264, 318, 378, 444, 516, 592, 674, 760, 852, 948, 1050, 1158, 1272, 1390, 1514, 1642, 1776, 1914, 2058, 2208, 2364 | no hits for 1,4,12,24,42,66,96,130,170,214,264,318,378: **new** |
| 6H, A (h) | 1, 4, 12, 24, 42, 64, 92, 127, 168, 213, 264, 319, 380, 445, 516, 591, 672, 757, 848, 946, 1050, 1158, 1272, 1390, 1514, 1642, 1776, 1914, 2058, 2206, 2360 | no hits for 1,4,12,24,42,64,92,127,168,213,264: **new** |
| 6H, B (c), atom 0 | 1, 4, 12, 25, 43, 66, 96, 129, 169, 214, 264, 319, 380, 445, 516, 592, 673, 759, 852, 948, 1051, 1159, 1272, 1390, 1514, 1642, 1776, 1915, 2059, 2208, 2364 | not searched separately (differs from all known above at n = 4); presumably new |
| 6H, B (c), atom 1 | 1, 4, 12, 24, 43, 67, 96, 130, 169, 213, 264, 319, 380, 445, 516, 591, 673, 760, 852, 949, 1051, 1158, 1272, 1390, 1514, 1642, 1776, 1914, 2059, 2209, 2364 | not searched separately; presumably new |

Terms to n = 60 are in data-oeis-terms.txt.

**Source.** Study 2026-10-28-pyrochlore-kagome (coordseq.py: 3C, 2H, 4H means to n = 5; "shell 3 = 24 + h, shell 4 = 42 + 2h");
paper #74 (DICTO DOI 10.5281/zenodo.23730421), Figure 1a; *Laws of Stacking*.

**How checked.** Breadth-first search on the exact bond rule of loops2.py (no distances, no rounding); the same code gives
A008253 (diamond) and A008264 (lonsdaleite) exactly for all 31 and 48 terms the OEIS lists (both fetched 7 Nov). Averages
per atom reproduce coordseq.out (4H: 24.5, 43, 66.5).

**Comment candidate on A008264:** "Also the coordination sequence of the c-layer atoms of the 4H polytype (computed n <= 60)."
Only as a computed observation; no proof.

Caveat for submission: OEIS has many per-site coordination sequences (tilings, zeolites), so the format fits; the editors will
want the structure named by its standard name (4H-SiC / 6H-SiC network) and the site defined unambiguously.

---

## 4. NEW (as an OEIS entry; classical in cosmology). Eigenmode multiplicities of the Poincaré dodecahedral space

**Definition.** a(n) = number of linearly independent degree-k harmonics on the 3-sphere invariant under the 120 icosians
(the 600-cell's corners), k = 2n; equivalently (k+1) * A008651(k), the multiplicity of the Laplace eigenvalue k(k+2) on the
Poincaré dodecahedral space S³/2I.

**Terms, k = 0, 2, ..., 120:** 1, 0, 0, 0, 0, 0, 13, 0, 0, 0, 21, 0, 25, 0, 0, 31, 33, 0, 37, 0, 41, 43, 45, 0, 49, 51, 53, 55,
57, 0, 122, 63, 65, 67, 69, 71, 146, 75, 77, 79, 162, 83, 170, 87, 89, 182, 186, 95, 194, 99, 202, 206, 210, 107, 218, 222, 226,
230, 234, 119, 363

**OEIS:** no hits with zeros (13,0,0,0,21,0,25,0,0,31,33,0,37,...), none without (1,13,21,25,31,33,...,122), none for the list of
degrees 0,12,20,24,30,32,36,... **New as an entry.** The Molien series itself is A008651; cross-reference it.

**Source.** Study 2026-11-04-pds-modes (scripts/pds_modes.py, data/pds-modes.json: character average over DICTO's 120 icosians,
all 121 degrees k = 0..120, equal to Aurich–Lustig–Steiner's r(β)); the link to the White Queen 600-cell (#63, DICTO DOI
10.5281/zenodo.23690856) and the harmonic fingerprint (#94, DICTO DOI 10.5281/zenodo.23934349). Not yet in a published paper of its own.

**How checked.** (k+1) x coefficient of (1 + t^30)/((1 − t^12)(1 − t^20)) equals DICTO's pds-modes.json at all 121 degrees (C4).

Caveat: the result is classical (Klein's invariants; Lachièze-Rey & Weeks; Aurich–Lustig–Steiner 2005); the entry would credit
them and cite DICTO's check. Our claim is only the OEIS entry, not the mathematics.

---

## 5. NEW. The Fibonacci stacking as a letter sequence (A, B, C = 0, 1, 2)

**Definition.** Layer types c, h follow the Fibonacci word (c → ch, h → c, from c); positions start 0, 1 and each next step
repeats the previous one at a c layer and reverses it at an h layer (Jagodzinski); a(n) = position of layer n mod 3.

**Terms, n = 0..104:** 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 1, 2, 0, 2, 1, 2, 0, 1, 0, 2, 0, 1, 2, 1, 0, 2, 0, 1, 0, 2, 1, 2, 0, 1, 0, 2,
0, 1, 2, 1, 0, 1, 2, 0, 2, 1, 0, 1, 2, 1, 0, 2, 0, 1, 0, 2, 1, 2, 0, 1, 0, 2, 0, 1, 2, 1, 0, 2, 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 1, 2,
0, 2, 1, 2, 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 1, 2, 1, 0, 2, 0, 1, 2, 1, 0, 1

**OEIS:** no hits for the first 30 terms. **New.**
**Related comment candidate on A085002** (floor(nφ) mod 2): the step sequence (+1 = forward A→B→C, −1 = backward) is
s(k) = 2·A085002(k+2) − 1 (checked k < 390); the 1/2 form 1,2,2,2,1,1,2,... has no hits, the 0/1 form matched only A085002.
So a(n) = Σ_{k<n} s(k) mod 3 = (2·Σ A085002(k+2) − n) mod 3, which can serve as the formula.

**Source.** Paper #69 *Fibonacci Stackings* (papers/fibonacci-stackings, DICTO DOI 10.5281/zenodo.23721038); study
2026-10-28-fibonacci-stackings (fib_words.py; same rule, extended to the infinite word).

**How checked.** Jagodzinski types recovered from the letters for 390 layers; the relation to A085002 checked for 390 steps.

Caveat: the convention (first layer A, first step forward) must be stated in the entry; the other choices give the same
sequence up to a permutation of 0, 1, 2.

---

## 6. NEW. Multiplet ladders of the Golden Ladder (Weyl dimension formula)

**Definitions** (F = Fibonacci, P = Pell A000129, Q = A001333):
- 6a. dim of the SU(4) multiplet (F(n+1), F(n), F(n+1)) → Icosaxes: 64, 300, 2156, 19200, 218700, 2877231, 42444864,
  671297550, 11134301360, 190155772800, 3309151031250, 58258240690455, 1033133038217280, 18403716735986400, 328751096163015084
- 6b. SU(4) (F(n), F(n+1), F(n)) → Unborn Axes: 64, 175, 1470, 11200, 127575, 1599696, 23284800, 362333895, 5964804300,
  101273168640, 1756672734375, 30858891591450, 546531849654336, 9727576651104039, 173679004122090090
- 6c. SO(7) (0, P(n), Q(n)) → truncated cube: 112, 4928, 905520, 411098688, 311548622112, 299636262953280,
  320240729382084000, 357903215135010881336, ...
- 6d. SO(9) (0, F(n), F(n+1), 0) → All-Golden Polytope (Icosaxes cells): 1650, 27027, 1527552, 142074933, 27491692800,
  8195406055200, 3539386118577375, ...
- 6e. SO(9) (0, F(n+1), F(n), 0) → All-Golden Polytope (Unborn Axes cells): 1650, 15444, 1005312, 77144760, 14642943744,
  4065095311200, 1708770292577205, ...

**OEIS:** no hits for 64,300,2156,19200,218700,2877231; 175,1470,11200,127575,1599696; 112,4928,905520,411098688;
1650,27027,1527552,142074933. **New.**

**Source.** *The Golden Ladder*, chapter 2 "Silence Is Golden" (papers/golden-ladder-ch2; book DICTO DOI 10.5281/zenodo.23966554);
study 2026-11-04-su4-weights.

**How checked.** Weyl dimension formula (SU(4) closed form; B3, B4 from the orthogonal basis), tested on 4, 6, 15, 7, 21, 8, 9, 16;
the printed terms of the chapter are reproduced exactly.

**Error found (exact details):** the chapter (and the book) write the Pell multiplets as (0, P_n, P_{n+1}). That gives
378, 19656, 5057325, ... and μ → (15 + 2√2)/7 = 2.547, not the truncated cube's 1 + √2. The printed dimensions 112, 4928, 905520, 411098688 and μ = 7/3, 17/7, 41/17, 99/41
belong to (b, c) = (1,1), (2,3), (5,7), (12,17) = (P_n, Q_n), as the study README says. Fix: "(0, P_n, Q_n), Q_n the numerators
of the convergents of √2" in golden-ladder-ch2 and book-golden-ladder.

Caveat for submission: OEIS editors may judge "irrep dimension at Fibonacci labels" an arbitrary composition; 6a is the strongest
of the five (it is the chapter's theorem (d)); submit at most 6a and 6b, citing the theorem.

---

## 7. COMMENT. Rhombohedra in the cubic approximants of the icosahedral tiling

**Statement.** In the F(n+1)/F(n) cubic approximant (n = 1: 1/1), the conventional cubic cell holds 4F(3n+2) prolate and
4F(3n+1) oblate golden rhombohedra, 4F(3n+3) tiles (and points) in all:
prolate 20, 84, 356, 1508, 6388, 27060, 114628, 485572, 2056916, 8713236, 36909860, 156352676;
oblate 12, 52, 220, 932, 3948, 16724, 70844, 300100, 1271244, 5385076, 22811548, 96631268;
total 32, 136, 576, 2440, 10336, 43784, 185472, 785672, 3328160, 14098312, 59721408, 252983944.
DICTO's primitive-cell counts (16, 136, 576, 1220, 10336, 43784, 92736, ...) are these, halved exactly on the rungs where
F(n) and F(n+1) are both odd (1/1, 5/3, 21/13, 89/55): there the cell is body-centred.

**OEIS:** none of the three ×4 sequences, nor the primitive-cell sequence, gives hits; the divided forms are A015448 (F(3n−1)),
A033887 (F(3n+1)) and A014445 (F(3n)). Multiples by 4 are not worth new entries; proposed comments on A015448 and A033887
("4·a(n) = number of prolate/oblate rhombohedra in the conventional cubic cell of the F(n+1)/F(n) approximant").

**Source.** Paper #99 *All Five in the Octet* (papers/2026-11-06-five-in-octet, DICTO DOI 10.5281/zenodo.24012439), Theorem 3
and its table; study 2026-11-06-approximant-ladder (scripts/exact_counts.py).

**How checked.** exact_counts.py extended to 11 rungs (1/1 .. 144/89) on compute-host, about 1 min; every count matches
the formula with the halving rule (C7).

**Lead:** this answers part of #99's open point "the body-centred and simple cubic alternation of the rungs as a theorem":
the alternation has period 3 and follows the parity of the Fibonacci numbers (F(m) is even exactly when 3 | m). The proof
(the index of Λ⊥ jumps by 2 when both entries are odd) is still to be written; probably known to Elser–Henley-type work, so
prior art first.

---

## 8. Finite sequences (weaker; OEIS takes them with keyword "fini,full")

- **8a. Vertices of the 600-cell by distance from one vertex:** 1, 12, 20, 12, 30, 12, 20, 12, 1. No hits. Source: *The Queens*
  (DICTO DOI 10.5281/zenodo.23753305), Red Queen 120-cell paper, study 2026-10-27-white-queen-polar. Classical (Coxeter); new
  only as an entry; may exist as a row of a table under another search form.
- **8b. Cells of the 600-cell by the height of their centres along a vertex axis (DICTO's Cleo Shells):** 20, 20, 30, 60, 60, 60,
  20, 60, 20, 60, 60, 60, 30, 20, 20. No hits. Source: study 2026-10-27-cleo-shells, White Queen 600-cell (#63, DICTO DOI
  10.5281/zenodo.23690856). Equals the 120-cell's vertices by layers along a cell-centre axis.
- **8c. Comment on A108997** (coordination sequence of the 120-cell): DICTO's 16 shells of the 600 cells by face-to-face steps,
  1, 4, 12, 24, 36, 52, 68, 76, 78, 72, 64, 56, 40, 12, 4, 1 (#63; *The Queens*), are exactly A108997 by duality. Comment
  "also the number of cells of the 600-cell n face-steps from a given cell" (trivial by duality; low value).

---

## Looked at and set aside

| Item | Source | Why not |
|---|---|---|
| Seam removals 5, 20, 60, 95, 145, 205, 275 (radius 3..9) | ocd-chorus; *DICTOnary* | float, depends on window and radius choice |
| Corner-radius kinds 3, 2, 4, 4, 6, 10, 14, 19, 24 along the OG chain | star-cores-c (#80) | float hull steps, 9 terms, one chain |
| Corners 26 → 552, 62 → 812, 452, 642, 1220, 1352, 2240 under the growth rule T | star-cores-c; star-chain census | float, few terms, tolerance-dependent |
| Lotus spheres 20, 80, 470, 770 per level | 2026-10-11-spheres-and-ripples | greedy float search, 4 terms |
| Hard-core fermion counts on chains | fibonacci-stackings, susy-fermions | known (Fendley et al.), DICTO only reproduced them |
| Degrees 0, 6, 10, 12, 16, 18, ... with icosahedral harmonics | #94 | support of A008651 (k even); known |
| Knitting row lists, bobble rows 1, 15, 29, ... | hexoct-knitting | periodic pattern instructions |
| Single numbers (62 slice patterns, 46 checks, ...) | various | not sequences |
| "1, 2, 3, ..." runs | book indexes | page/chapter lists |

Sources searched: all papers/*/paper.html and book-*/paper.html (integer runs of six or more, and every OEIS mention), all
studies/*/README.md (titles and integer lists), the .txt/.out/.log/.json data of the candidate studies, and
papers/dicto-concordance/concordance.json (keywords sequence, OEIS, per shell, growth).

## OEIS queries made (35)

24,48,480,3432,25704,194256,1509072 (none) · 1,4,12,24,42,64,92 (A008253) · 1,4,12,25,44,67,96 (A008264) · 24,48,480,3432,25704
(none) · 12,24,240,1716,12852,97128 (none) · 1,4,28,256,2716,31504,387136 (A002895) · 4H B-site (none) · 6H A-site (none) ·
id:A002895 · 64,300,... (none) · 175,1470,... (none) · 112,4928,... (none) · 1650,27027,... (none) · 120-cell shells (A108997) ·
1,12,20,12,30,12,20,12,1 (none) · 20,84,356,... (none) · 32,136,576,... (none) · 12,52,220,... (none) · 16,136,576,1220,...
(none) · 5,21,89,377,... (A015448) · 3,13,55,233,... (A033887) · PDS degrees (none) · I-harmonic degrees (none) · Molien
1,0,0,0,0,0,1,... (A008651) · PDS multiplicities with zeros (none) · without zeros (none) · Fibonacci letters (none) · steps 1/2
form (none) · steps 0/1 form (A085002) · id:A008253 · id:A008264 · fcc NB walks (none) · fcc closed walks (A002899) ·
id:A002899 · Cleo shells (none).

## Next steps (none taken)

1. Write out the proof of the Loop Equality (section 1) and search prior art for "closed walks identical on all stackings /
   polytypes"; then #74 and *Laws of Stacking* can say theorem, and candidates 1, 2a, 2b become strong submissions.
2. Fix the Pell notation in golden-ladder-ch2 and book-golden-ladder (section 6).
3. DICTO decides which to submit; strongest: 1, 3 (4H/6H), 4, 5; then comments 2a, 2b, 7.
