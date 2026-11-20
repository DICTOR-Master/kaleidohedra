**Verdict: stop. Do not build Version 2.** In the re-score, both blind scorers give notability 4 and literature 4, so the literature gap of the first pre-score is closed. Both still return outcome `warning` with one finding, and it is the same finding from each: the golden-product theorem has no research interest of its own apart from Kulaichev's theorem. The build rule set on 20 Nov was a clean 4 / 4 from both scorers with no finding, and that rule is not met. **What blocks it:** a theorem that singles out the Cleo-Antonius condition among the fourth conditions in Table 3, or the 43 / 24 counts proved in Lean. Neither exists, and no wording can supply them.

# Yantra Version 2: Bolton–Macleod and Fonseca, the #103 gap, and a re-score (20 November 2026)

DICTO, 20 Nov 2026, decided to pursue Version 2 of the Yantra Palomar entry, Theorem 14 plus Theorem 15 (the DICTO Yantra), against the pre-score's advice, and to close the gap that the pre-score found in #103. This study follows the order that study 2026-11-20-palomar-yantra-v2-prescore set:

1. read the sources;
2. write a paragraph for #103;
3. say why this condition was chosen;
4. rewrite the input and re-score once;
5. give the verdict.

Nothing was built. The entry repository and the published #103 were not touched.

## 1. Sources read (free routes only)

**The two papers themselves were not read in full.**
- N. J. Bolton, D. N. G. Macleod, "The geometry of the Śrī-yantra", *Religion* 7(1) (1977) 66–85, doi:10.1016/0048-721X(77)90008-2.
- R. Fonseca, "Constructive geometry and the Śrī-cakra diagram", *Religion* 16(1) (1986) 33–49, doi:10.1016/0048-721X(86)90004-7.

Both are closed access:
- OpenAlex and Semantic Scholar both mark them closed.
- The publisher pages (Taylor & Francis, ScienceDirect) refused the fetch with HTTP 403.
- The Internet Archive holds only the journal's annual indexes (sim_religion_1978_7-8_index and others), not the volumes.
- Searches for an author copy or repository copy found none.
- Google Books gave citations only (Joseph, *The Crest of the Peacock* 1992; Klostermaier, *A Survey of Hinduism* 1994).

The free route left is a library. CiNii lists the journal *Religion* (NCID AA00390749) in **35 libraries in Japan**, so DICTO could read both papers in a library (see LEADS).

**What was read about them:**

| Source | How read | What it says about Bolton–Macleod / Fonseca |
|---|---|---|
| A. Chiodo, *C. R. Math.* 359 (2021) 377–397 | library copy (CC BY), full text | p. 381 (French): "Bolton et al [2] et puis Fonseca [5] proposent également des constructions à la règle et au compas basées sur celle du nombre d'or. Elles échouent de façon invisible à l'œil nu : cela a motivé l'hypothèse [2, p. 75] … qu'une construction analogue du śrīyantra remonterait à l'Égypte ancienne." p. 386 (§1.2.2): "Nicolas J. Bolton and D. Nicol G. Macleod [2] and Fonseca [5] propose a straightedge and compass construction based on the golden ratio. These approaches fail to meet concurrency conditions in a way that is not visible to the eye." **n. 15:** "The first construction is approached by replacing at a first stage the circumscribed circle by a square. The second construction is inscribed in a circle and appears as a refinement of the first." Also from p. 386: both list Method A's vertex coordinates (B–M pp. 68–69; Fonseca pp. 35–36). B–M Table 2 and Fig. 2 give A. West's scheme, which meets all the concurrencies but not the circle condition (i). |
| A. P. Kulaichev, *IJHS* 19.3 (1984) 279–292 | library copy (INSA scan), page images | p. 292, n. 12, on "any required value of a ratio between the chosen sides of triangles would be achieved": "Similar attempts (in respect to golden proportion and number π) have been undertaken in: Bolton and Macleod, op. cit., which is the only, we know, research of the Śrīyantra as a mathematical object." |
| R. C. Gupta, "Yantras or mystic diagrams", *IJHS* 42.2 (2007) 163–204 | INSA free scan (new to the library), pp. 180–181 and notes pp. 201–203 as page images | p. 181: "A technique for drawing a nearly perfect Śrīyantra within a square has been given by Bolton and Macleod who also mention that Alan West of the University of Leeds has produced a scheme to construct the yantra without any error." Gupta also mentions a Nepalese version with the pyramid angle 51°51′ (notes 61–62: B–M pp. 71–79, 74). |
| G. Heil, Indology mailing list, 16 Apr 1994 | web archive | Informal: "the citation I gave earlier to the architect Rory Fonseca is the most accurate I have seen printed. Two very small extra triangles. While the earlier work by Nicholas J Bolton and D. Nicol G. Macleod showed it could be done exactly if the outline was a square rather than a circle." Recorded here only, and not used in #103. |
| sriyantrageometry.com/sources | web page | An unattributed site claims a measured concurrency miss of 0.2229 % for a "seven-by-seven grid" construction by B–M. It is not used: its source and method are not stated. |

**What each construction does, as far as the sources support:**
- **Bolton–Macleod.** A straightedge-and-compass construction based on the golden ratio. It is drawn first in a square in place of the circle, and the meetings are nearly exact. They relate the yantra to the golden proportion and π, and they float an ancient Egyptian origin (p. 75).
- **Fonseca.** A golden-ratio construction inscribed in the circle, a refinement of Bolton–Macleod's.

Both miss the concurrencies by amounts too small to see. **How far they miss is not known from any source read.** Chiodo gives no number. The 0.2229 % figure above is unverified, and Heil's "two very small extra triangles" is informal.

**Library.** Added on the compute host (commit f14b1fe):
- Bolton–Macleod 1977 and Fonseca 1986 as link entries, NOT READ in full, with reading notes giving the pages above.
- Gupta 2007 as a copy, sha256 5f98556e….
- Kulaichev 1984 p. 292 n. 12 added to his reading notes.

INDEX.html was rebuilt. INDEX.pdf needs Playwright and was not rebuilt here (LEADS).

## 2. The paragraph for #103 Version 7 (text only; the published #103 is untouched)

For §2 (sources) or the end of §10.1, with DICTO's names:

> **Golden-ratio drawings before this paper.** N. J. Bolton and D. N. G. Macleod (*Religion* 7, 1977) and R. Fonseca (*Religion* 16, 1986) gave straightedge-and-compass constructions of the Śrī Yantra based on the golden ratio. The first is drawn at first in a square in place of the circle; the second is inscribed in the circle as a refinement of the first; both fail the concurrency conditions by amounts invisible to the eye (Chiodo [2], pp. 381 and 386, n. 15). Kulaichev names Bolton and Macleod's attempts "in respect to golden proportion and number π" (p. 292, n. 12). Those drawings use the golden ratio as a rule for placing points and accept meetings that are only nearly exact. The Cleo-Antonius condition is different in kind: it is one exact equation, uv = 2/φ³, imposed on a yantra in which Huet's 18 marmas, the corner touches and the apexes on bases already hold exactly (Theorem 1); with (b), (c) and (d) it fixes one yantra (Theorem 15), whose slope u has a minimal polynomial of degree 160 (Theorem 9). Since 160 is not a power of 2, u is not a constructible number (Wantzel, 1837), so no straightedge-and-compass construction, golden or otherwise, draws the DICTO Yantra exactly; the same holds for Kulaichev's yantra (degree 348, Theorem 10). The golden ratio enters only through the slopes of the two solids of §9.1, and we make no claim about how the yantra was drawn in the past.

For the Sources checked, the line "Named in Chiodo's bibliography and not read: Bolton–Macleod 1977, Fonseca 1986, …" becomes:

> Bolton–Macleod 1977 and Fonseca 1986: closed access, no free copy found (20 November 2026); described from Chiodo 2021 (pp. 381, 386, n. 15), Kulaichev 1984 (p. 292, n. 12) and R. C. Gupta, *IJHS* 42.2 (2007), p. 181, which were read.

Notes for DICTO:
1. The Wantzel sentence is new to #103. It is a one-line consequence of Theorems 9 and 10, which are certified, and of Wantzel's theorem. It is not a new computation. Both blind scorers called it correct ("correct as stated, given #103's irreducibility theorem").
2. Add Gupta 2007 and Wantzel 1837 to the references.

## 3. Why the Cleo-Antonius and not the other fourth conditions in Table 3

**What #103 says.** The reasons #103 gives are constructive. None of them is a theorem that singles the Cleo-Antonius out.

The conditions in Table 3 that, with (b), (c) and (d), give a yantra meeting every condition:

| Fourth condition | Yantra | Regions / sandhis | Status |
|---|---|---|---|
| uv = 2/φ³ (Cleo-Antonius) | DICTO Yantra | 43 / 24 | exact, Theorem 9; unique, Theorem 15 |
| uv = (2/φ²)(1/√2) (Cleo-Octangula, from a viewpoint) | V1 | 43 / 24 | 60 digits, computed |
| v = 1/√2, u free | PF2 | 43 / 24 | 60 digits, computed |
| u = 2/φ², v free | PF1 | 45 / 28 | 60 digits, computed |
| u = v (Kulaichev) | Kulaichev's yantra | 45 / 28 | exact, Theorem 10; unique, Theorem 14 |

The reasons #103 gives:
1. **Partners.** "Antonius … is the Cleo-Icos's own partner: Cleo + Antonius + Cleo make the golden rhombohedron" (§9.1). PF2's upper slope "has no parent solid" (Proposition 8, Figure 9).
2. **One field.** The Cleo-Antonius lies "all in ℚ(√5)" (§9.1). The Cleo-Octangula "needs both √5 … and √2" (§9.2).
3. **Exactness and proof.** The DICTO Yantra is solved exactly and proved unique (Theorems 9 and 15). V1, PF1 and PF2 are computed only (Table 5).

**What #103 does not say.** #103 states the opposite of a selection theorem (§10.1): "Equal great triangles (Kulaichev) and the Cleo-Antonius product uv = 2/φ³ (DICTO) are two choices of that fourth condition, and the family cannot single out 'the' yantra by itself." The only general statement nearby is an observation: in Table 3, the two extra triangles appear exactly when the two great slopes add up to about 1.49 or more. #103 itself calls this "an observation from these cases, not yet a theorem" (§10.1). Even proved, it would not single out the Cleo-Antonius, because V1 (1.470) and PF2 (1.403) are also below 1.49.

**No theorem singling out the Cleo-Antonius exists in #103 or in its studies.** These were searched:
- 2026-11-08-sri-yantra
- 2026-11-15-dicto-yantra-uniqueness
- 2026-11-20-yantra-thm15-scope
- 2026-11-20-palomar-yantra-v2-prescore
- the canonical regions and cones studies

The sri-yantra study records the order of events on 8 Nov:
- K1, V1 and PF2 already had 43 / 24.
- DICTO then asked for "a side of Antonius instead of stella", which gave GF1.
- GF1 was named the DICTO Yantra.

This is recorded as history. It is not offered as a reason.

## 4. Re-score (palomar-kit/prescore protocol, one run)

**Input.** `blind/inputs/V2b-kulaichev-and-golden.md`: the first pre-score's V2 input with four changes and nothing else.
1. **A new bullet in "prior work"** for Bolton–Macleod and Fonseca. It says what was read and what was not, and how the golden product differs from those drawings, including the Wantzel sentence.
2. **A new paragraph, "Why this fourth condition and not the others"**, with the reasons from §3 and the plain statement that no theorem singles the condition out.
3. **Challenge header:** a new paragraph, "The golden product is one choice among several", lists Table 3's alternatives and says the file proves uniqueness for the stated condition only. The first scorer B asked for this.
4. **Challenge header, Sources:** two sentences on Bolton–Macleod and Fonseca.

The candidate is labelled V2b. Blindness: the submitter is never named. A check for leaked names found only "Macleod". Note that the file was edited by hand: `make_challenge.py` was not re-run, and the new header text is given here for the build if Version 2 is ever built.

**Policy and prompt.** `blind/policy/` and `blind/scorer-prompt.md` were copied from the kit. `cmp` shows both are byte-identical to `palomar-kit/prescore` (PalomarPolicy @ 28bd48b).

**Scorers.** Two fresh general-purpose agents ran in parallel:
- Each received only the kit's prompt, with POLICY, INPUT and CAND = V2b filled in.
- They read the web only, wrote no files and started no background work.
- Each hand-back was saved verbatim in `blind/raw/` as `blind-A-V2b.json` and `blind-B-V2b.json`. Each was extracted straight from the scorer's hand-back call, not retyped.

**Tally** (`tally.py`): `V2b: A: 4 / 4, warning, 1 finding(s) | B: 4 / 4, warning, 1 finding(s) -> notability clears`.

| Candidate | Scorer | Notability | Literature | Outcome | Finding |
|---|---|---|---|---|---|
| V2 (first pre-score) | A | 4 | 4 | warning | the second theorem has no research audience of its own |
| V2 (first pre-score) | B | 4 | **3** | warning | Bolton–Macleod and Fonseca missing |
| **V2b (this study)** | A | **4** | **4** | warning | the golden-product theorem's interest is "not established independently of the Kulaichev theorems" |
| **V2b (this study)** | B | **4** | **4** | warning | "its research interest is not shown on its own terms"; present it as a companion, or give "a proved statement that separates it from the other conditions in Table 3" |

**What the changes achieved:**
- **Literature 3 → 4.** The Bolton–Macleod / Fonseca finding is gone. A checked Chiodo's §1.2.2 and n. 15 word for word: "The account separates the golden product from the Bolton–Macleod and Fonseca drawings fairly … The non-constructibility argument … is correct as stated."
- **No manufactured-definition finding** under CONTRIBUTING §1. A: "The entry passes as a whole because the account is honest about the choice". B: the honesty "keeps the second theorem clear of the 'definitions designed to manufacture conclusions' concern."
- **The remaining finding is the one no wording can remove.** It is the first pre-score's A finding, now raised by both scorers.

## 5. Review of the reviews

**Where they are right:**
1. **The finding (both scorers).** As formalised, Theorem 15 is uniqueness for one chosen condition. Its outside interest, the traditional counts, is outside Lean, and #103 says no theorem singles the condition out. This is exactly §3's answer, so the finding is accurate. *Action:* none in wording. Only the two theorems in LEADS 1–2 can remove it.
2. **Cite #103's current version (both, internal notes).** The Zenodo record shows a version newer than v5: v6 is published and adds no mathematics. *Action:* if Version 2 is built, cite the concept DOI or the version whose theorem numbers match.
3. **Bolton–Macleod and Fonseca should be confirmed first-hand (both).** This is right: the paragraph rests on Chiodo, Kulaichev and Gupta. *Action:* the library route (LEADS 3).

**Where they are mistaken or overstate:**
1. **"Kulaichev's Addition has accessible text: a Scribd copy exists" (B).** The Scribd page shows no text without an account (library entry, 16 Nov). That is not a free route, so no action.
2. **Pustynski "404" (both).** The cahc mirror is dead. The INSA copy is in the library and was read on 16 Nov. A tooling limit, not an error.
3. **A's "a family the account calls arbitrary".** The account says "one choice among several", not arbitrary. A slight overstatement, with no effect on the score.
4. **A's suggestion "generalise to uv = c over an interval of c".** This is a real idea, but it is the same as LEADS 1, and it is a new theorem.

## 6. Verdict

The rule (DICTO, 20 Nov, from the pre-score study): build only on a clean notability 4 / literature 4 from both scorers with no finding.

**Result:** 4 / 4 from both scorers, outcome `warning`, one finding each, the same one. **Not met: stop.**

**What blocks it:** the golden-product theorem's independent interest. Wording cannot fix this, since the account is already as honest as it can be. Only a theorem can:
- (a) a selection theorem that separates uv = 2/φ³ from the Table 3 conditions, or classifies the fourth conditions that give 43 / 24; or
- (b) the region counts (43 / 24 against 45 / 28) proved in Lean, which the scope study rates as **large**.

The #103 gap that the pre-score found (Bolton–Macleod and Fonseca) is closed in text: the paragraph in §2 is ready for #103 v7, and it is recorded in the Concordance (gaps.waiting, home #103 v7).

## LEADS

1. **Selection theorem for the fourth condition (home: #103).** Over the family uv = c with (b), (c), (d), find which c give 43 / 24. If the boundary is the extra-triangle wall (Proposition 13's u* in general), the Cleo-Antonius is one point of an interval and is still not singled out. That would answer the question honestly either way. This is token-free compute and needs DICTO's word.
2. **Lean counts (large).** See the scope study §5.
3. **Bolton–Macleod and Fonseca first-hand.** The journal *Religion* is held by 35 libraries in Japan (CiNii AA00390749). DICTO could read both papers in a library. Copying fees may apply, and that is DICTO's choice. Then check the paragraph's wording against them and record how far each construction misses.
4. **#103 v7.** Add the §2 paragraph, the Sources-checked line, and Gupta 2007 and Wantzel 1837 to the references, when DICTO approves a v7.
5. **Library INDEX.pdf.** Rebuild it with Playwright on the node. INDEX.html is already rebuilt.
6. **ORCID resubmission (unchanged from the pre-score's LEAD 4).** If Version 2 is not built, decide whether the ORCID commit alone is worth one resubmission.

## Files

- `blind/policy/` (4 files) and `blind/scorer-prompt.md`: byte-identical to the kit.
- `blind/inputs/V2b-kulaichev-and-golden.md`: what the scorers saw.
- `blind/raw/blind-A-V2b.json`, `blind/raw/blind-B-V2b.json`: the two hand-backs, verbatim.

FINAL ok
