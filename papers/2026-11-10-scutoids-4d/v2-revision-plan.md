# DICTO Paper #104 — Revision plan for Version 2

**Paper:** Scutoid Tissues in Four Dimensions, v1 (10 Nov 2026)
**Input:** one external AI review of v1
**Audience for this file:** Claude Code, working in the paper's repo

---

## 0. Read this first

- This plan was written from the review only. The author of this plan did not see the paper, and the pasted review had lost its inline maths (thresholds, parameter names, table counts). Wherever this plan says "check", open the paper and confirm before editing.
- Scope is small. No theorem, proof, count or figure changes unless a check below fails. If a check fails, stop and report; do not patch the maths silently.
- Work in one consolidated pass: collect every edit, apply them together, rebuild the PDF once. Do not rebuild or re-send after each small change.
- Bump to Version 2, add a short changelog line listing the edits.

---

## 1. Assessment of the review

### 1.1 What it gets right (act on these)

| Review point | Verdict | Task |
|---|---|---|
| Two meanings of "scutoid" are blurred | Correct, worth fixing | T1 |
| Theorem 1' needs a stated dimension range | Correct | T2 |
| References are a "sources checked" list, not a bibliography | Correct | T4 |
| Theorem 3 needs reproducibility detail | Correct, and the most substantive item | T5 |
| "Fixed four-layer context" condition is under-defined | Plausible, check the wording | T6 |
| Keep Queens interpretation labelled as interpretation | Correct | T7 |

### 1.2 Numbers independently re-derived (all agree)

For a simple 4-polytope, h = (1, h1, h2, h1, 1) with h1 = f3 − 4 and h2 = f0 − 2 − 2·h1.

| Polytope | f3 | f0 | h1 (births = deaths) | h2 (swaps) |
|---|---|---|---|---|
| 120-cell | 120 | 600 | 116 | 366 |
| Truncated 120-cell | 720 | 2400 | 716 | 966 |
| Bitruncated 600-cell | 720 | 3600 | 716 | 2166 |

Balance law: 601 + 601 + 964 = 2166. Consistent.

The review's d = 3 remark is also right, and can be stated more completely. In a simple d-polytope with a generic sweep:

- index 1: facet birth
- index 2: contact gain (a ridge appears)
- index d−2: contact loss
- index d−1: facet death

So d = 4 is the only dimension where gain and loss share an index (2). At d = 5 they separate (2 and 3). At d ≥ 6 indices 3 … d−3 touch only lower-dimensional faces. At d = 3 birth coincides with contact loss (index 1) and death with contact gain (index 2); the review mentions only the first half.

### 1.3 What the review misses or overstates

1. **Classical content is praised as new.** That the number of index-k vertices is independent of the generic direction is the standard definition of the h-vector (McMullen 1970; Ziegler, Lectures on Polytopes, §8.3; line shellings, Brüggesser–Mani 1971). Passing a vertex acting as a bistellar move on the dual of the section is also known. The review calls the direction-independence the paper's strongest contribution. A referee would not. What is DICTO's: reading the three indices as birth / swap / death of tissue cells, the Queens counts, the balance law, and the Section 2 material. See T3.
2. **The MathOverflow citation could not be confirmed.** Two web searches for a 2018 thread titled "Higher dimensional scutoids?" did not surface it. The review may be right, but it is unverified. See T4.
3. **Boundary vertices.** "116 births" excludes the four cells already present at the bottom vertex (120 = 116 + 4), and four cells survive to the top vertex. Check that the paper says this where the counts are first stated. See T2.
4. **Section 7's ratings table** ("strong", "very strong") carries no information. Ignore it.
5. **The review's closing question** (classifying tissues by h-vector) is future work. The h-vector gives counts, not arrangement. One cheap corollary may be worth a remark; see T8.

### 1.4 Not actioned

- "Don't rush Version 2": agreed in spirit; this plan is deliberately small.
- No change to the proofs of Theorems 1, 2, 4, the defect expressions, or the disclosed open regions.

---

## 2. Tasks

Priority: T5 > T1 > T3 > T2 > T4 > T6 > T7 > T8.

### T1. Separate the two scutoid constructions

Where: abstract, introduction, a new short "Terminology" paragraph, and the opening of each section.

- Construction A (Section 1): the cells are the 3-dimensional facets of a simple 4-polytope. Their 2-dimensional sections are polygons that exchange neighbours. This is the direct analogue of a biological scutoid. Suggested fixed term: **scutoid tissue** (on ∂P).
- Construction B (Section 2): the cell is the 4-dimensional polytope Q obtained by stacking a power cell over the weight parameter. Its 3-dimensional sections exchange neighbours. Suggested fixed term: **4D scutoid**.
- State once that both are convex with flat faces, unlike biological scutoids, which have curved faces and need not be convex.
- Then grep the paper for every use of "scutoid" and make each one unambiguously A or B.

Acceptance: no bare "scutoid" whose dimension a reader has to infer.

### T2. Scope Theorem 1'

- State the theorem for d ≥ 4.
- Add a remark with the index table from 1.2, including both d = 3 coincidences.
- Check the theorem statement and proof against that table. If the paper's indices differ, stop and report.
- Where the Queens counts are first given, add one sentence on the 4 initial and 4 final cells (item 1.3.3), if not already there.

### T3. Mark classical versus new

Add a short paragraph before or after Theorem 1 (and mirror it in the introduction):

- Classical: h_k counts index-k vertices for any generic linear functional; Dehn–Sommerville; the sweep as a shelling of the dual; bistellar moves. Cite.
- New here: the tissue reading of indices 1, 2, 3; Theorem 2; Theorem 4; Section 2.

Also soften any priority language about "higher-dimensional scutoids" to the specific claims: this construction, and its link to the h-vector and the Swap Rule.

### T4. Bibliography

Replace the "sources checked" list with a conventional bibliography. Verify every entry against the publisher or DOI before committing. Starting points, from memory and unverified:

- P. McMullen, The maximum numbers of faces of a convex polytope, Mathematika 17 (1970).
- H. Brüggesser, P. Mani, Shellable decompositions of cells and spheres, Math. Scand. 29 (1971).
- G. M. Ziegler, Lectures on Polytopes, GTM 152, Springer (1995).
- V. M. Buchstaber, T. E. Panov, Toric Topology, AMS Math. Surveys and Monographs 204 (2015).
- U. Pachner, P.L. homeomorphic manifolds are equivalent by elementary shellings, European J. Combin. 12 (1991).
- W. B. R. Lickorish, Simplicial moves on complexes and manifolds, Geom. Topol. Monogr. 2 (1999).
- F. Aurenhammer, Power diagrams: properties, algorithms and applications, SIAM J. Comput. 16 (1987).
- P. Gómez-Gálvez et al., Scutoids are a geometrical solution to three-dimensional packing of epithelia, Nature Commun. 9, 2960 (2018), doi:10.1038/s41467-018-05376-1. (Confirmed.)

MathOverflow thread: search for it. If found, cite with URL and access date, and add two sentences contrasting it (shape of a single generalised cell, by truncating a prism) with Construction B (parameterised power cells with exchanges at walls). If not found, do not cite it and do not mention it; report that it could not be located.

Prefer the Nature Communications paper over MathWorld for the biological definition.

### T5. Reproducibility of Theorem 3

Add a "Verification" subsection or appendix, and a matching README in the study folder. It must answer:

1. Environment: language, library names and pinned versions, OS.
2. Which steps are exact (rational or algebraic arithmetic) and which are floating point. Any floating-point step must be labelled as evidence only, not as part of the proof.
3. Certificates: which output files constitute the proof (symbolic resolutions, rational identities, Bernstein sign certificates), with file names and hashes at the cited commit.
4. One command that re-runs the roughly 11 million sign checks from a clean checkout, with expected runtime and expected summary output.
5. The exact domain covered: the six stackings, the local-context condition, the parameter range. The open regions restated next to it.

Then actually run the command from a clean clone and confirm it reproduces. If any step in the proof chain turns out to be floating point, stop and report; that changes the status of the theorem.

In the theorem statement, use the phrase "computer-assisted proof" and state the domain in the statement itself, not only in the discussion.

### T6. Define the four-layer condition

Check Theorem 3's wording on stackings "whose pieces are fixed by the four layers around their gap". If it is not already a formal definition, add one before the theorem: what a context is, what "fixed by" means, and which of the six stackings satisfy it.

### T7. Label interpretation

Put the Queens channel analogy and similar readings under an explicit "Interpretation" or "Remark" heading so they are not read as part of a theorem.

### T8. Optional, only if the author approves

A possible remark after Theorem 1. For a simple 4-polytope the g-theorem gives g2 = h2 − h1 ≥ 0 and g2 ≤ C(h1, 2). In tissue terms: every generic sweep has at least as many swaps as births, and at most births + C(births, 2). Check against the three Queens rows (366 ≥ 116, 966 ≥ 716, 2166 ≥ 716) and against Ziegler §8.6 before including. Do not add without sign-off.

---

## 3. Final checklist

- [ ] Checks in T2, T5, T6 passed, or failures reported and work stopped
- [ ] Every "scutoid" is A or B
- [ ] Classical / new paragraph present
- [ ] Bibliography entries verified; MathOverflow item cited or reported missing
- [ ] Verification appendix and README written; clean-clone run reproduced
- [ ] Version, date and changelog updated
- [ ] Single rebuild; page count and figure numbering still correct
- [ ] Short report to the author: what changed, what was checked, what could not be verified
