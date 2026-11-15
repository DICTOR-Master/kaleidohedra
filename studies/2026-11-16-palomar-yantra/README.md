**Verdict: notability 4 (estimate), at the floor and not above it; literature 4 once one page number is corrected.** Both fresh blind scorers gave the finished Lean entry (`kulaichev_unique`, `kulaichev_slope`) notability 4 / literature 4, outcome `neutral`, with no findings. I agree with 4. The reason is the one the landscape study predicted: the entry settles a question someone else put in print (Kulaichev 1984), and a peer-reviewed paper calls that question still open (Chiodo 2021). That makes this the first DICTO entry whose finished form, not only a planned target, reaches 4 in our replays. It is still only at the floor, and production scores vary by about one point between runs, so 4 is likely but not guaranteed. **Nothing was submitted. Submission happens only on DICTO's word.**

# Palomar pre-score: the Lean entry for Kulaichev's Śrī Yantra (16 November 2026)

**Status:** estimate only. No account was used, no repository was created and no contact was made. The production reviewer (`palomar-review`, `codex:gpt-6-sol`) cannot be run outside Palomar's broker, as the earlier studies explain (2026-11-14-lean-loop-equality/SCORE.md, Method).

## The entry scored

- **Package.** studies/2026-11-15-yantra-box-certificate, §7, milestone 11.
- **Challenge.** `lean/Challenge/KulaichevYantra.lean`: 116 lines, Mathlib only.
- **Theorems.**
  - `kulaichev_unique : ∃! y : Yantra, y.Huet ∧ y.Kulaichev ∧ y.Admissible`;
  - `kulaichev_slope`: w7/b7 lies in an interval of width 2⁻²¹ around 0.75043851602221….
- **Proof.** Fully kernel-checked, with no `sorry` and no `native_decide`. The axioms are propext, Classical.choice and Quot.sound. The comparator accepts it with all three kernels, and all three negative controls are rejected.
- **Metadata.** `lean/palomar/formalization.yaml`.

## Method (copied from 2026-11-15-palomar-permutohedron)

1. **Blind input.** `blind/inputs/K-kulaichev-unique.md` holds:
   - a neutral abstract, including the method of proof and the author's prior non-Lean work;
   - the problem's published sources with exact citations;
   - the Challenge definitions and theorems, verbatim.
   It says plainly that the Kulaichev scan has no text layer, that his page numbers come through Chiodo, that Rao 1998 was not read, and that admissibility is the submitter's own formalisation.
2. **Policy given to the scorers.** These are in `blind/policy/`: CONTRIBUTING §1 (lines 63–94) and §7 (lines 831–981), prompt 04 and rubric.json. They come from PalomarPolicy @ 28bd48b and are byte-identical to the copies used in the earlier replays.
3. **Two fresh scorers in parallel.** Both were general-purpose agents (Claude Opus 5.5). Each got only the policy files and the blind input: none of our notes, none of the earlier scores, and no studies. Each searched the web on its own (reading only) and returned prompt 04's JSON: `blind/blind-A-K1.json` and `blind/blind-B-K1.json`. Neither started background work or wrote files.
4. **Citation check (my own, step 1).**
   - **Reference library.** The reference library (its INDEX, MANIFEST and file names) hold no Kulaichev, Chiodo, Pustynski or Huet. The only yantra item is Chapati–Chapati 2026 (#189). So none of the problem's sources is in the library.
   - **Papers and studies.** #103 (paper.html, §10.1 and §14) and the studies yantra-uniqueness, dicto-yantra-uniqueness and open-problems-to-close give the same citations. #103 §14 records that Chiodo and Pustynski were read in full, that the Kulaichev scan has no text layer, and that Huet was not reachable.
   - **Chiodo, re-read for this study.** I read the open-access C. R. Math. PDF and found the page of each quotation:
     - "il se pose la question (toujours ouverte) de l'unicité" is on journal **p. 381** (French section "La recherche d'un unique śrīyantra"), **not p. 384** as our files say;
     - the English §1.2.4, "This problem is not considered here", is on p. 387, which is correct.
   - **Pustynski.** No copy is held. The INSA URL in #103 §14 was the source of the earlier reading; the scorers got HTTP 404 on the other link.
   - **Kulaichev.** Not read directly. Page 285 for the question comes from Chiodo's citation.
   - No citation was invented. The open question has a real, checkable printed source: Chiodo 2021, p. 381 (French) and p. 387 (English).
5. **Review of the reviews.** This is my own judgement, below.

## Blind scores

| Scorer | Notability | Literature | Outcome | Findings |
|---|---|---|---|---|
| A | **4** | 4 | neutral | none |
| B | **4** | 4 | neutral | none |

**Reasons both gave:**
- The question was posed in print by someone else (Kulaichev 1984).
- It is called "still open" in a peer-reviewed venue (C. R. Math. 2021).
- Chiodo's own English text says the answer was argued to be "out of reach".
- Neither found any later work that settles it.
- They name three audiences:
  - the Śrī Yantra geometry literature (IJHS, Math. Gazette, CRAS);
  - certified computation and real algebraic geometry;
  - formally verified computer-assisted proof.
- Both say 5 is not justified, because the audience is specialist. B calls the 4 "earned but borderline".

## Review of the reviews

**Where they are right:**
1. **The anchor.** The reason for 4 is the right one, and it is the pattern of the 134 registered original entries (landscape study §3): an owner of the question in the literature. Our replays reached 4 only for this problem, and never for questions DICTO posed himself (Loop Equality 3, Kyushindo 2, permutohedron ≤ 3).
2. **Borderline, not 5 (B).** Right. The interest is specialist. The cultural fame of the figure is rightly not counted (A).
3. **Rao 1998, Tahta 1992, Santhi et al. 2012, Tularam 2012 and Kulaichev's own "Addition" are unread or uncited** (A and B). Right, and it is our real weakness in the literature account. Chiodo's "still open" postdates them all, so it is unlikely that any of them settles the question. But an editor would want each named, with one line on what it says.
4. **The Chiodo page (B).** Right. B said the French passage sits earlier than p. 384, and the PDF puts it on p. 381. Our files carry p. 384 in:
   - `formalization.yaml`;
   - #103 paper.html (§10.1, §14);
   - studies yantra-uniqueness and open-problems-to-close;
   - concordance.json;
   - this study's blind input (left as the scorers saw it).
   This is a minor bibliographic slip under prompt 04 (an internal note, not a finding). It must be corrected before any submission.
5. **The Synapse pre-registration (A and B).** A search snippet describes a planned certified Krawczyk enumeration of "well-posed subsets of the Rao 1998 constraint system". Neither scorer could open it (HTTP 429), and I did not try. It is not a prior settlement (A: "a planned study with no reported results"). It must be read and, if it is independent, cited before submission. A prior result there would change the account.

**Where they are mistaken or overstate:**
1. **A's claim that p. 384 is accurate.** This is mistaken: A echoed the input's page. The quotation itself is correct.
2. **Admissibility, "say whether real solutions exist outside the admissible set" (B).** This is already answered in our work, though not in the blind input. Study 2026-11-15-yantra-uniqueness found exactly one other real solution with 0 < u < 1, at u = 0.66866. In it t4 turns over, b6 > b7 and w5, w6 < 0, so it is not a Śrī Yantra. A real package should say this in one line. It answers the "narrowed to manufacture uniqueness" worry and belongs to statement alignment.
3. **B's reading of Kulaichev (b) via Chiodo's footnote ("circumcircle of t1").** The entry's reading, base corners on the circle, is the one Pustynski and #103 use, and B accepts it. This is not a defect.
4. **LeanCert (B).** It was not used, so no citation is needed. Nothing to change.
5. **"Formalise the minimal polynomial or get peer review" (A and B).** These would add outside evidence, but they are not needed for 4. Prompt 04 does not reward more formalisation.

**Final estimate: notability 4, literature 4 after the fixes below. Outcome `neutral`, at the floor.** The risk is the one-point run-to-run noise. A production run could give 3 if its reviewer weighs the specialist audience more heavily. Two independent blind 4s, and the earlier blind 4 for the target (2026-11-15-open-problems-to-close, Y2), make 4 the honest central estimate. A 5 cannot be claimed truthfully.

## What would raise it, or make the 4 safer

1. **Fix the citation: Chiodo p. 381, not p. 384**, in formalization.yaml and wherever else it appears (#103 v5 through the Concordance errata route). Add a source entry for Chiodo's English §1.2.4, p. 387.
2. **Name the missing comparisons** in formalization.yaml's notes: Rao 1998 (IJHS 33, 203–227), Kulaichev's "Addition", Tahta 1992, Santhi et al. 2012 and Tularam 2012. Read them through free routes (NDL copy or library) and give one line each on what they say about uniqueness; never buy them. Read the Synapse pre-registration.
3. **One line on scope.** The only other real solution of the equations in the box is not admissible (u = 0.66866; see the census). Admissibility excludes only degenerate figures.
4. **Name the audience in the account:** the Śrī Yantra geometry line (Huet, Kulaichev, Rao, Pustynski, Chiodo, Chapati–Chapati), certified real-root computation, and formal proof.
5. **Pairing with the DICTO Yantra (Theorem 15).** This is not recommended for the score. The earlier blind replay put the golden condition at 2 ("chosen to get the count"; no outside source asks for it), and bundling would not lift the Kulaichev result. If it were added, it should be a separate corollary in the same Challenge. It could only dilute the entry. Keep it for #103.
6. **A better Challenge statement.** None is needed for notability. If DICTO wants the exact algebraic identification, formalising f348 as the slope's minimal polynomial is extra work that adds outside checkability, not notability.

## LEADS

1. Correct Chiodo's page to 381 in formalization.yaml and in the other files listed above, through the errata route for #103 (DICTO's call on the paper text).
2. Read the Synapse pre-registration (Rao system, Krawczyk enumeration). It is the only item that might touch priority.
3. Read Rao 1998 and Kulaichev's "Addition" by a free route, then Tahta, Santhi et al. and Tularam. Add each to formalization.yaml.
4. Add the one-line scope statement (u = 0.66866 not admissible) to formalization.yaml `fidelity`.
5. Then DICTO decides on submission. The estimate meets his rule of 4 or more, but only at the floor.

## Files

- `blind/inputs/K-kulaichev-unique.md`: what the scorers saw.
- `blind/policy/`: CONTRIBUTING-s1.md, CONTRIBUTING-s7.md, 04-literature-notability.md, rubric.json (PalomarPolicy @ 28bd48b).
- `blind/blind-A-K1.json`, `blind/blind-B-K1.json`: their replies, in prompt 04's shape, with `what_would_reach_higher`.
