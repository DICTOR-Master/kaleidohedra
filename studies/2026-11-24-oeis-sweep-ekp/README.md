# OEIS sweep: the EKP cell, the Kaleidohedra and the Double Vision / Vajrayana shells (24 November 2026)

Purpose: the 18 November sweep (studies/2026-11-18-oeis-sweep) never looked at the Euclid–Kepler–Pacioli (EKP) cell or at the
Kaleidohedra record (DICTO DOI 10.5281/zenodo.23173809, "shearable lattices, new space-fillers and the EKP cell"). On 24 Nov
DICTO extended the sweep to the shells of the Double Vision (Dual Vision) and Vajrayana worlds. Pass condition: an entry is
queued only if it is printed in a released paper with a DOI (or follows from a stated theorem there), new to the OEIS, has
at least about 20 exact terms computed two ways, is not an artefact of a chosen parametrisation, and is not a trivial
multiple or transform of an existing entry (ENTRIES.md rules 0–15 and the 18 Nov filters). Nothing was submitted, and nothing
was written to ENTRIES.md, concordance.json or any paper.

**Conclusion.** No new entry can be queued from this work. The EKP and Kaleidohedra papers print no sequence indexed by n.
The golden-cycle shells (Double Vision, Vajrayana, Universal PiTet) repeat exactly every turn, so their per-shell counts are
periodic and their running totals are linear. The two growth counts that are printed (Chain of Karma, dodecahedral Chain)
are of the form c·13^n + d. One comment on an existing entry is possible: A001400, from #100 / *Space-Fillers* Chapter 2.
All near-misses were computed two ways and agree for n = 0..24 (FINAL ok).

## Method

- **Sources found.** Searched papers/*/paper.html (in k-research and in the Kaleidohedra repo's papers/) and the memory index
  for EKP, Euclid–Kepler–Pacioli, Kaleidohedra, shearable, shear, Vajrayana, Double/Dual Vision. Read the Kaleidohedra
  DISCOVERIES.md (F1–F38) and the app worlds (world-double-vision.js, world-vajrayana.js) to see what the films unwrap.
- **Released status.** Checked against each folder's zenodo-state.json and the Concordance's papers table:
  - #8 *The Euclid–Kepler–Pacioli Cell*, DICTO DOI 10.5281/zenodo.23284106 (v2; first in Kaleidohedra v2026.10.11-octet).
  - Kaleidohedra findings F1, F2, F5–F7, F9–F12, F15, F16 (skewed RD, equal-edge rule, the nine regular space-fillers,
    skewed ED, EKP windows, stretched dodecahedron, Star Chain Reaction, Jewel and Sunstar clusters): DOI 10.5281/zenodo.23173809.
  - #13 Dodeca-13 (23284281), #17 Kagome Hulls (23376317), #18 The DICTO Hexa (23376320), #41 Jewel (23496353),
    #42 Sunstar (23497702), #50 *One Move Each* (23606894), #59 Icosaxes Hexa (23677485).
  - *Space-Fillers and Lattice Moves* (book), 10.5281/zenodo.24221379, published; Chapter 2 = #100 (concept 24030326, published).
  - #33 *Double Vision – Both Cycles in One Space*, 10.5281/zenodo.23407106; #35 *Vajrayana*, concept 10.5281/zenodo.23429911
    (its zenodo-state.json has no "published" flag; the Concordance lists the DOI); #38 *Universal PiTet*, 10.5281/zenodo.23463305
    (published); *The Golden Cycle* (book), concept 10.5281/zenodo.23752452, published.
- **Sequences sought.** Counts per layer, stage, turn or step; tilings by size; cells, faces, corners; coordination and growth
  series; looked for in the printed text, tables and theorems only.
- **Computed.** `scripts/near_misses.py` (exact integers, two ways each, n = 0..24, under one second; no heavy run was needed,
  so nothing went to the compute host). Output `data/out-near-misses.txt`, ends FINAL ok.
- **OEIS.** `scripts/oeis_search.sh` with `scripts/queries.txt` (13 queries, `search?q=...&fmt=short`, 4 s apart), log
  `data/oeis-searches.txt`; id lookups of A001400 and A091030 (fmt=text) in `data/oeis-lookups.txt`. "Not found" means no
  match on 24 Nov 2026; it does not mean new.

---

## Ranked candidates

None. Every sequence found fails at least one filter; see the table below.

---

## Considered and rejected

| Item | Source | Reason |
|---|---|---|
| Any count indexed by n in the EKP cell: nodes 13 per cell, 31 aligned axes, the Pm-3 / Fm-3 / Cmmm / Pmmm colourings | #8 (23284106) | single numbers, not sequences; the paper prints no n-indexed count |
| Coordination sequence of the EKP 13-node set | #8 data (ekp-cell.json) | not printed, and the paper defines no graph on the nodes: the edge set (icosahedron, dodecahedron, star or cube edges) would be our choice, an artefact. LEAD below |
| Nodes in a k × k × k block of EKP cells | — | not printed; depends on how the block's boundary is counted |
| The nine most regular space-fillers (F6); the 24 sheared-FCC RD targets (F9); the skewed ED's two forms (F7) | Kaleidohedra (23173809) | finite lists |
| Star Chain Reaction / Jewel chain, nesting without end by 1/φ³ | F12, F12a (23173809), #42 | one solid per step: the counts are constant; the sizes are not integers |
| Hexa levels: 8 Jewels per Hexa, Hexas on a 2 × 2 × 2 block of blocks | #18, #41, *Space-Fillers* ch. 7 | 8^n (A001018); the third level is an open gap, not printed as a sequence |
| Index-13 sublattices: 183, 8 | *Space-Fillers* ch. 4 (#25) | single numbers; the tiling is known (Kovačević–Tan; Singer's difference set) |
| Thirteen octet tilings of Table 2.1 (octahedra, tetrahedra, index N) | *Space-Fillers* ch. 2 (#100) | finite table of solver results |
| Chain of Karma, pieces after n steps: 1, 113, 1569, 20497, 266561, ... = 13^n + 100(13^n − 1)/12 = (28·13^n − 25)/3 | *Golden Cycle* ch. 1 §2 (formula printed; 113, 1569, 20497 printed) | not found in the OEIS, but an affine transform of 13^n (A001022): a(n) = 13 a(n−1) + 100. Trivial transform |
| Chain of Karma, gap pieces after n steps: 0, 100, 1400, 18300, ... = 100(13^n − 1)/12 | *Golden Cycle* ch. 1 §2 | 100 × A091030 (partial sums of powers of 13). Trivial multiple; a comment on A091030 would carry no information beyond the factor 100 (Occam) |
| Dodecahedral Chain, pieces of D(φ^(2n)): 63, 175, 1631, 20559, ... = (28·13^n + 161)/3 | *Golden Cycle* ch. 1 §5 (63, 175, 1631 printed) | the Chain of Karma count plus 62; same affine transform of 13^n |
| Bodhi chain, 13^n triacontahedra | *Golden Cycle* (Bodhi Seed) | 13^n itself, A001022 |
| Spheres of Dharma, 237 pieces per cycle | *Golden Cycle*, #23 | 237 n, linear |
| Double Vision interlock pieces per layer: ends 80, 60, 12, 60, 84, 240; middle 120, 20, 132, 20, 180, 30 (per turn 536 and 502; original cycle 174) | #33 Table 3 | the paper states the nest repeats by φ³ with the same pieces ("the same pieces scaled by φ⁻³"), so per-layer counts are periodic of period 6 and running totals are 536 per turn plus a partial turn: a finite table, not a sequence. Not found in the OEIS as a period |
| Vajrayana stations and pieces: 12 stations per turn (I, Cleo star, D′, ID, O, rTI, TI, H, jtI, RT, M, I·φ³); 82 pieces in D′, 30 in RT → M, 60 in M → I·φ³ | #35 | the film loops "without a seam" because each turn is the last scaled by φ³: periodic counts again; the faces and corners per station are fixed solids |
| Universal PiTet shell pieces: 32, 30, 32, 60 per turn (ID → RT → GTI → FPD → ID·10/φ⁴) | #38 Table 2 | the Proposition gives T^(4n)(ID) = (10/φ⁴)^n ID, so the counts are periodic of period 4; running totals 154 per turn, linear. Not found in the OEIS |
| Lotus seed shells 12, 30, 20 | *Golden Cycle* ch. 1 | the icosahedron's corner, edge and face counts |

## Comments on existing entries

| Entry | Comment (facts only; DICTO writes the text, rule 0b) | Source | Readiness |
|---|---|---|---|
| A001400 (partitions of n into at most 4 parts) | a(n) − 1 is the number of Dehn-zero truncations of the tetrahedron of edge n by whole layers of the octet (four corner cuts k_i ≥ 0 up to order, Σ k_i = n, the whole tetrahedron not cut away); equivalently, those that keep the octet's ratio of two tetrahedra to one octahedron. Terms checked two ways (brute enumeration of the cuts; the g.f. 1/((1−x)(1−x²)(1−x³)(1−x⁴)) minus 1) for n = 1..25: 0, 1, 2, 4, 5, 8, 10, 14, 17, 22, ... (this shifted form is not in the OEIS) | #100 (concept 10.5281/zenodo.24030326) and *Space-Fillers and Lattice Moves* (10.5281/zenodo.24221379) Chapter 2, Propositions 2.1 and 2.3; the twelve pieces for n ≤ 5 are printed as "the twelve partitions of n into two to four parts" | the count for general n is not printed, only the rule and the list for n ≤ 5; the book's wording ("partitions of n into two to four parts") makes the link one line. Ask DICTO; rule 14 (one comment in, one out) |

## LEADS

- **EKP network coordination sequence (outside the plan).** The EKP network (#8 §5(b): great stellated dodecahedra on even
  cells, icosahedra on odd cells, sharing corners only) has a natural skeleton graph, the edges of its pieces. Its coordination
  sequence would be a genuine candidate if a released paper defines that graph and prints the sequence; today it is neither.
  Its home would be #8's next version. DICTO's call.
- **Dehn-zero truncations, rational cuts.** Conjecture 2.5 (*Space-Fillers*) is about tiling, not counting; no sequence in it.

## Files

- `scripts/near_misses.py`, `data/out-near-misses.txt` (all near-misses two ways, n = 0..24; FINAL ok)
- `scripts/oeis_search.sh`, `scripts/queries.txt`, `data/oeis-searches.txt`, `data/oeis-lookups.txt`

Sources checked: the papers listed under Method (text, tables, theorems); Kaleidohedra DISCOVERIES.md F1–F38; the Concordance
(papers, names, ledger); the OEIS (13 searches, 2 id lookups, 24 Nov 2026).
