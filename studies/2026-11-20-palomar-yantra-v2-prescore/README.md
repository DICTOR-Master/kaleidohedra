**Verdict: do not build Version 2 as it stands.** Version 2 (Theorem 14 plus Theorem 15) scores notability 4 and 4, which clears the floor, but only because Kulaichev's question carries it. Both scorers say the second theorem adds nothing to notability. Both change the outcome from Version 1's clean `neutral` to `warning`, each with one finding, and one of them drops literature to 3. Theorem 15 alone (V2-alt) scores 3 and 3, outcome `failure`. Kulaichev's anchor is worth exactly one point. No scorer made a "manufactured definition" finding under CONTRIBUTING §1, and two said in so many words that they do not assert one. So the honest gain from building is visibility of a theorem the reviewers read as the submitter's own choice of condition. The cost is a medium-to-large build, and the risk falls on the whole entry. The case changes only if the fixes listed under LEADS are made first.

# Palomar pre-score: Version 2 of the Yantra entry (20 November 2026)

DICTO, 20 Nov 2026: "pre-score first", with no Lean building yet. The entry is PALOMAR-2026-11-17-000006, Kulaichev's uniqueness (#103 Theorem 14), registered as Version 1. The plan for Version 2 is to add #103 Theorem 15: Huet's conditions, Kulaichev's (b), (c), (d), the Cleo-Antonius product uv = 2/φ³ in place of (a), and admissibility admit exactly one Śrī Yantra, the DICTO Yantra. Its traditional-form counts (43 triangles, 24 sandhis) stay certified in #103 (Proposition 11) and are not formalised. Scope and feasibility are in study 2026-11-20-yantra-thm15-scope. **Status:** estimate only. Nothing was built or submitted, and the entry repository and #103 were not touched.

## Method (palomar-kit/prescore README)

1. **Policy.** `blind/policy/` is copied from the kit unchanged (PalomarPolicy @ 28bd48b). `cmp` shows it is byte-identical to the kit and to the Version 1 pre-score (study 2026-11-16-palomar-yantra).
2. **Inputs.** Both are built from `input-template.md`. The submitter is never named, and the input says which names were replaced: Cleo-Antonius becomes "golden slope product" / `GoldenProduct`; the DICTO Yantra becomes "golden-product yantra"; `dicto_unique` / `dicto_slope` become `golden_unique` / `golden_slope`; the Cleo-Icos becomes "face pyramid of the icosahedron"; Antonius becomes "golden antiprism". #103's title is left out, and its DOI is given.
   - `blind/inputs/V2-kulaichev-and-golden.md`: **V2**, one entry with both theorems. It contains the proposed Version 2 Challenge in full: Version 1's Challenge, a second-theorem paragraph in the header, the pilot's two definitions and the pilot's two theorems.
   - `blind/inputs/V2-alt-golden-alone.md`: **V2-alt**, the control. It is the same result framed as a separate entry with Theorem 15 alone. It says that Theorem 14 exists as a separate entry.
   - The Challenge texts were generated from Version 1's Challenge file by `blind/make_challenge.py`. The new definitions and statements are those of the compiled pilot. The two generated Challenge files were not themselves compiled: nothing heavy runs on this machine.
3. **What the inputs say about the condition's origin.** They state only what #103 says (§§4–5, §9.1, §10.1, Table 3):
   - the slopes come from a pair of solids: the icosahedron's face pyramid, which sweeps a cone of slope 2/φ², and its golden-antiprism partner, with side slope 1/φ;
   - the viewpoint maps keep the product uv;
   - the undistorted pair fails (d), so the condition is the product;
   - #103 calls it one of two choices of a fourth condition;
   - Table 3 lists other solid-derived fourth conditions that also give 43 (computed, not certified).

   The inputs also say that #103 does not state the condition was chosen for the counts, and that the inputs make no claim either way. Both inputs disclose that the counts are not formalised.
4. **Scorers.** Four fresh general-purpose agents ran in parallel, two per input, one run each. Each received only the kit's scorer prompt with POLICY, INPUT and CAND filled in. They read the web only, wrote no files and started no background work. Each hand-back was saved verbatim in `blind/raw/`, extracted straight from the scorer's hand-back call, not retyped.
5. **Tally.** Made with `palomar-kit/prescore/tally.py`. The judgement below is mine.

## Blind scores

| Candidate | Scorer | Notability | Literature | Outcome | Findings |
|---|---|---|---|---|---|
| V2 (Thm 14 + Thm 15) | A | **4** | 4 | warning | 1: the second theorem has no research audience of its own |
| V2 | B | **4** | **3** | warning | 1: the earlier golden-ratio constructions (Bolton–Macleod 1977, Fonseca 1986) are missing |
| V2-alt (Thm 15 alone) | A | **3** | 4 | failure | 1: research interest not shown |
| V2-alt | B | **3** | 4 | failure | 1: research interest not shown |

Tally: V2 clears the notability floor, but its literature is below the floor, so the finding must be fixed first. V2-alt fails. For comparison, Version 1 scored 4 / 4 `neutral` with no findings in both blind scores (16 Nov). The DICTO Yantra alone scored 2 / 3 in the 15 Nov replay (Y3, "chosen to get the count").

**Manufactured definition (CONTRIBUTING §1): none.**
- B on V2: the added theorem "does not manufacture its own advertised conclusion (uniqueness under a stated condition is a substantive claim)".
- A on V2-alt: "The section-1 concern about 'definitions designed to manufacture the advertised conclusions' is not asserted". The same scorer adds that the condition "can be read as chosen to produce a figure with the traditional counts" and that it "found no evidence either way".
- The honest account of the condition's origin moved Theorem 15 alone from 2 (Y3) to 3, but not to 4.

**The reasons all four gave:**
- The golden product is the submitter's own condition. Its only motivation is the submitter's unreviewed preprints (#29, #44, #103).
- No published question asks for it.
- #103 itself calls it one of several choices (Table 3).
- The property that would make it matter, the traditional 43 / 24, is outside Lean.
- In V2, notability "rests on the Kulaichev theorem" (A), and the golden theorems "do not raise notability" (B).
- A on V2-alt: "a lighter repackaging of the same method under an invented condition".

## What would raise the score (the scorers' lists, merged)

1. **Formalise the counts** (45 / 28 against 43 / 24) for both figures, so the contrast "Kulaichev's figure is not traditional, the golden one is" becomes part of what is checked. All four scorers name this. The scope study rates it a separate **large** project.
2. **Say why this fourth condition and not the others.** This could be a classification theorem over slope-product conditions that give the traditional counts, or a certified uniqueness for Table 3's alternatives (V1, PF2). Named by A on V2, and by A and B on V2-alt.
3. **Cite the golden-ratio constructions** of Bolton–Macleod (*Religion* 7, 1977, 66–85) and Fonseca (*Religion* 16, 1986, 33–49), and state how the exact condition differs from them. They are approximate drawings that miss the concurrencies, and no historical claim is made. Named by B on V2, the literature finding. Also name Kulaichev and Ramendic 1989 (A).
4. **Outside reception.** Peer review of #103, or a citation by a specialist, so the condition does not rest only on self-citation. Named by all four.
5. **Put the Table 3 alternatives in the Challenge header too**, so the Lean side does not suggest that the golden product is the distinguished choice. Named by B on V2.
6. **Do not file it alone.** Named by both V2-alt scorers, which agrees with the scope study.

## Review of the reviews

**Where they are right:**
1. **The anchor (all four).** Kulaichev's published question carries the 4, as the kit's README predicts. Without it, Theorem 15 is a 3. *Action:* if Theorem 15 ever goes on Palomar, it goes only inside this entry.
2. **The literature finding (B on V2): checked and confirmed.** Chiodo 2021 (open-access PDF, text checked) reviews them twice:
   - p. 381 (French): "Bolton et al [2] et puis Fonseca [5] proposent également des constructions à la règle et au compas basées sur celle du nombre d'or. Elles échouent de façon invisible à l'œil nu".
   - p. 386 (§1.2.2, English): "a straightedge and compass construction based on the golden ratio. These approaches fail to meet concurrency conditions in a way that is not visible to the eye", followed by the hypothesis of an ancient "perhaps perfect" construction and "numerous attempts of this kind … on the internet".

   #103's Sources list names Bolton–Macleod and Fonseca only as "named in Chiodo's bibliography and not read". It does not mention that they are golden-ratio constructions. A golden condition placed beside that history, without the distinction, invites the "baseless numerology" reading. *Action:* read both by free routes, then add one paragraph to #103 (via the errata route) and to any Version 2 `formalization.yaml`. Page numbers here come from the PDF's own page sequence, starting at 377; the 381 for "toujours ouverte" matches Version 1's corrected citation.
3. **The second theorem adds no notability (A and B on V2).** This is right, and it is the kit's own rule: "A wider scope that does not raise notability stays in the paper" (Dehn D2, Grünbaum G2).
4. **Table 3 weakens the choice.** This is right, and our own input said so honestly. An honest account cannot avoid it. Only a theorem can remove it (item 2 above).

**Where they are mistaken or overstate:**
1. **"A lighter repackaging of the same method" (A on V2-alt).** This overstates the case. The proof needs √5 coefficients, a box unbounded in u and a new corner analysis (scope study §3). It is not lighter as mathematics. For notability, though, the point stands: difficulty is not research interest, and B on V2-alt says the same.
2. **"Build and register before claiming Version 2" (B on V2).** This is already the plan. We scored a proposal, and it is not a defect.
3. **The Pustynski link returned 404 (A and B on V2).** This was the cahc link. Both inputs cite Pustynski without a URL, and the INSA copy was read on 16 Nov. No action.
4. **Kulaichev and Ramendic 1989 (A on V2).** A itself says it is psychophysiological, not mathematical. Name it in one line, nothing more.

**Final estimate.**
- **V2:** notability 4 at the floor, outcome `warning`. With the Bolton–Macleod / Fonseca paragraph added, the literature score should be 4. Production scores vary by about one point between runs, and Version 2 is reviewed as a whole. A reviewer who weighs A's finding more heavily could give 3, and that would be a `failure` of the whole resubmission.
- **Theorem 15 alone:** 3, `failure`.
- 5 cannot be claimed for either.

## Recommendation

**Do not build Version 2 now.** It does not raise notability, it changes the entry's outcome from `neutral` to `warning`, and it puts the whole entry at the floor with a live finding. That spends a medium-to-large build (scope study §5) for a theorem the reviewers see as one choice among several. The DICTO Yantra's visibility is better served in #103 itself (v6 leading with Theorems 14 and 15 together), where Theorem 15 is already certified.

If DICTO wants it on Palomar anyway, these steps come first, in this order:
1. Read Bolton–Macleod and Fonseca by free routes, and add the paragraph that distinguishes the exact condition from them.
2. Put the Table 3 alternatives in the Challenge header.
3. Re-score V2 once.
4. Build only if both scorers give 4 / 4 with no finding.

The one change that could really lift Theorem 15 is a theorem: either Lean counts of 43 / 24 against 45 / 28 (large), or a result that singles the golden product out among the fourth conditions that give the traditional form.

## LEADS

1. Bolton–Macleod 1977 and Fonseca 1986 (*Religion*): read by a free route (NDL or library), then add a distinguishing paragraph to #103 through the errata route. This is a real gap in #103's account, whatever happens to Version 2.
2. Name Kulaichev and Ramendic 1989 in #103's sources checked (one line: not mathematical).
3. A selection theorem for the fourth condition: which slope products uv, with (b), (c), (d), give the traditional 43 / 24? #103 §10.1 already has the observation (sum of slopes below about 1.49). A proof would answer "why this condition" and would serve #103 whether or not Palomar follows. Its home is #103.
4. The ORCID commit (6bf9e04) still waits for a resubmission. If Version 2 is not built, decide separately whether the ORCID alone is worth one resubmission (checklist §E: avoid resubmissions).
5. If Version 2 is wanted after leads 1–3, re-score once with the fixed input before any build. Next, the face analysis of the new box (scope study §5, step 2).

## Files

- `blind/policy/`: CONTRIBUTING-s1.md, CONTRIBUTING-s7.md, 04-literature-notability.md, rubric.json (PalomarPolicy @ 28bd48b, byte-identical to the kit).
- `blind/scorer-prompt.md`: the kit's prompt (byte-identical), given to each scorer with POLICY, INPUT and CAND filled in.
- `blind/inputs/V2-kulaichev-and-golden.md`, `blind/inputs/V2-alt-golden-alone.md`: what the scorers saw.
- `blind/make_challenge.py`: builds the two proposed Challenge texts from Version 1's Challenge (`python3 -I make_challenge.py <KulaichevYantra.lean> v2|alt`).
- `blind/raw/blind-A-V2.json`, `blind-B-V2.json`, `blind-A-V2-alt.json`, `blind-B-V2-alt.json`: the four hand-backs, verbatim.

FINAL ok
