# #110 Walls of Silence, Version 2: review actions and outcomes (17 November 2026)

Sources:
- the external review (review-actions-109-110.md, items 1–7);
- DICTO's ruling of 16 November: Nansen is removed (kept in Alicia and the Brief Geometry chapter).

The referee review of Version 1 (22 findings) was applied before Version 1 was released.

| # | item | outcome |
|---|---|---|
| 1 | Cross walls justified up front | **Done.** §2 gives three reasons that do not depend on B: they are cell-parallel sections, dual to the mirrors; they are the middle walls of the 25 inscribed 24-cells (now **exact**; it was floating point in Version 1); and they are the 120-cell Kochen–Specker rays. The order in which the cross walls were found is still stated. |
| 2 | Verification language | **Done.** The two "by the review" and "independently" phrases are reworded. A Reproduction paragraph says "reproducible, not independently refereed". |
| 3 | Reproducibility | **Done.** studies/2026-11-17-independent-checks/110-exact has one rerun script (run_all.sh); 110-chambers has rerun commands. Both are named in the meta line. |
| 4 | Optimality of the 16/16/22 covers | **Partly.** Two solvers, run without symmetry breaking: HiGHS gives optima 16, 16 and 22, and CP-SAT finds 15, 15 and 21 infeasible. The covers and the instance are written as data. There is **no checkable proof certificate**: CaDiCaL gave no answer within the 300 s host limit, and no DRAT check was run. No short hand-checkable bound reaches the optimum: the linear relaxation gives 12, and counting over mirrors gives 12, 12 and 18. The paper says this. |
| 5 | Theorem C auditable | **Done.** The new Appendix B has the 360-wall lattice by rank: flat counts by walls through them, Σμ and χ. It also gives the in-chamber terms (1+25+138+134 = 298), and for the 1560 walls χ(t) and the in-chamber terms (1+174+5981+35041). Every claimed number was matched by two methods. The 1560-wall χ(t) is new and appears only in the appendix. |
| 6 | Proposition 5 data | **Done.** prop5_cases.csv.gz (90,000 cases) and prop5_patterns.txt (18 patterns, 1500 matched cases) are named in the statement. |
| 7 | Independent implementation | **Done for:** cross walls, Theorem A, Lemma 3 (b, c), Theorem B (a–d), Proposition 5, Theorem B′ (d) and the exact-cover claim, and Theorem C. **Not covered:** Theorem B′ (a), (e), (f); Proposition 6; Tables 1 and 4; the 15 piece types of Theorem C (a). One step of B′ (d) is floating point (zero-area remainders), and the paper says so. |

## Corrections found by the second implementation

- **Proposition 5:** "copies from the two states share at most 6 corners" holds for A and B copies only. Two C3 copies can share 12 corners and no wall. The text is corrected.
- **Theorem B′ (d):** "covers a pentagon whole" means by the union of one copy's fins on that plate. A single fin of B* holds only some of them, and a single fin of C3* holds none. The text is clarified.

## Left as it is (per the review)

- §8 on "hidden" not explaining silence;
- A and B as unions of chambers;
- Theorems B(d) and B′.

## Changed per DICTO

- Nansen's cat and its reference are removed. The Red Queen keeps Schrödinger's cat (two states).
- The references are renumbered, and two wrong appendix citation numbers are corrected.
