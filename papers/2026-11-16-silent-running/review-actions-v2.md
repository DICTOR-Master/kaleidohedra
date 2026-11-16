# #109 Silent Running, Version 2: review actions and outcomes (17 November 2026)

Sources:
- the external review (review-actions-109-110.md, items 1–12);
- the referee attack (second-implementation/REPORT.md, findings 1–17; judged in JUDGEMENT.md).

## External review

| # | item | outcome |
|---|---|---|
| 1 | Crystallography: theorem vs analogy | **Done.** §8 is renamed "A crystallographic analogy" and opens by stating that the result is representation theory, not a diffraction result. The negative Bragg-peak pilot now comes first. Proposition 8 is renamed "a group-theoretic analogue of systematic absences", and its label covers only the proved sentences. The abstract was rewritten in the same terms. |
| 2 | Census scope early | **Done.** The scope sentence is in the abstract and after the method. The method now states the exact union rule (two-orbit unions for subgroups with ≤ 8 orbits; twisted unions all if ≤ 9 classes, else up to 3). |
| 3 | Three views of Prop 3 | **Done.** They are stated as "complementary explanations, not independent proofs". A paragraph says which part each covers, and it is moved from the proofs to directly after the statement. |
| 4 | Moment rigidity in words | **Done**: text and new Figure 3 (X against an ordinary orbit; DICTO asked for it 17 Nov). |
| 5 | Ordinary vs twisted symmetry in the introduction | **Done.** New paragraph in §1. |
| 6 | 16-dimensional candidates: make the open status visible | **Superseded.** Referee finding 1 proves these silences follow from the Main theorem: the classes are products of 2I classes. So they are no longer open. Table 3b, Figure 6 (regenerated) and §6 now say so, and open problem 3 is removed. |
| 7 | (T) within the scope of the census | **Done** (§9). |
| 8 | All-degrees step for non-specialists | **Done.** The Klein-form argument is in plain steps, with the witness degrees. These were checked against an exact decomposition of V_k for k ≤ 30. |
| 9 | Second-hand sources | **Listed** in the status box (13 sources to obtain). Appendix A is unchanged until they are read. |
| 10 | Theorem 1 re-audit | **Done.** second-implementation/THEOREM1-AUDIT.md audits 9 steps and finds no gap. The hypotheses are corrected (any finite-dimensional representation of a finite G), and the proof gains the isotypic-multiplicity and invertibility steps. |
| 11 | Prop 6 vs the classification | **Done:** studies/2026-11-17-independent-checks/109-prop6. Every automorphism of I2(n) (n ≤ 40), H3, H4, A3–A5, B3, B4, D4 and F4 was computed with exact characters. **Mismatch in Version 1:** "n = 5 or n ≥ 7" wrongly includes n = 8 and 12; Version 2 says n = 5, 7, 9, 10, 11, n ≥ 13. The general step "reflection representation ⇒ Galois conjugate" is still unproved and is now stated as checked case by case. |
| 12 | Independent implementation | **Done for the core; partly for the census.** The second implementation reproduces the core. A third program reproduces the census: all zero lists of the 600-cell, 24-cell, snub and E8 sets, the 120-cell sets by invariants, and Table 3a. The count 3232 is not independently reproduced. The paper says "reproducible, not independently refereed"; nowhere does it say "independently verified". |

## Referee findings

All 17 are applied:

- **1:** the W(H4) products.
- **2:** spin values ±i√3, ±i√2, with moduli in the proof and the double cover named.
- **3:** the Chebyshev condition, plus defect zero.
- **4:** the Prop 6 n list, the scope and the unproved step stated.
- **5:** Table 3b columns renamed.
- **6:** the dial claim in the abstract.
- **7:** Koca credit.
- **8:** Frobenius/Shintani credit and the hypotheses.
- **9:** Prop 5 for all k, with the open problem trimmed.
- **10–17:**
  - the Prop 6(b) proof;
  - Theorem 4 defined, with real versus rational weightings;
  - "C ∪ −C also kills 4";
  - "generic orbit";
  - the Prop 8 label;
  - the lift step;
  - the Franzsen numbering;
  - Schur is now in the to-obtain list.

## For DICTO

The 16 November study 2026-11-16-remaining-silences explains the three census rows that Table 3a still lists as unexplained. The review says to add no new results in this pass, so Version 2 leaves them as they are. Adding one sentence is DICTO's call.
