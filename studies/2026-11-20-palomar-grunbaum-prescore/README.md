# Palomar pre-score: Grünbaum's zone question at k = 10 (20 November 2026)

**Verdict: both candidates hold notability 4, at the floor, in all four blind scores. Literature is 3 in three of the four (outcome `warning`), because all three scorers who found it say the earliest known solid of this family is D. Hall's dimpled rhombic triacontahedron (Sketchfab, 28 June 2016), not Inchbald (by March 2023). Adding the classification (G2) does not raise notability. Literature can be put right by citing Hall 2016 (and Kostick 2022). Nothing was submitted.**

DICTO approved the pre-score on 20 November. The method is the same as the Dehn pre-score (studies/2026-11-19-palomar-dehn/blind) and the Yantra pre-score (studies/2026-11-16-palomar-yantra).

## Method

- **Policy.** `blind/policy/` holds CONTRIBUTING §1 and §7, prompt 04 (literature and notability) and rubric.json. They are byte-identical to the Yantra and Dehn copies (PalomarPolicy @ 28bd48b; checked with `cmp`).
- **Inputs.** `blind/inputs/` holds two neutral descriptions in the D1 format: a neutral abstract with the facts of the proof and its stated limits, the sources with exact citations and what was read, prior formalizations, prior work by the same author, what is claimed, the Challenge file quoted in full, and the statements to score. DICTO is not named; the submitter is "the submitter". One word in the Challenge docstring was changed, as the inputs say: the witness's name.
  - **G1** (`G1-grunbaum-k10-example.md`): the built Challenge of studies/2026-11-17-get-palomar, which is `grunbaum_k10`, `grunbaum_k10_parallelohedron` and the two calibration theorems, with GET A as the witness. GET B and the non-congruence of A and B appear in the informal account only, because they are not in Lean.
  - **G2** (`G2-grunbaum-k10-classification.md`): G1 together with the classification theorem of studies/2026-11-15-grunbaum-k10. Its scope is stated exactly: class C(6) only; face-to-face lattice tilings only; unions of golden rhombohedra only; exact computation outside Lean; the five non-sign-coherent surfaces are undecided.
  - Both inputs disclose three things. Inchbald's dimpled triacontahedron (web, by March 2023) is an earlier k = 10 example of the same family. Senechal–Taylor 2023 has not been read. Senechal's reply of 20 November is disclosed as correspondence that cannot be checked, and no priority is claimed from it.
  - **G3 dropped.** G3 was the worst case, in which GET is among Senechal–Taylor's solids. Senechal replied (20 Nov, as DICTO reports it) that GET and her solids only share similarities.
- **Scorers.** Four fresh general-purpose agents ran in parallel, two per candidate. Each was given only the four policy files and one input. Each could search the web and read pages, and wrote no files. The prompt is in `blind/scorer-prompt.md`. Each returned prompt 04's JSON with `what_would_reach_higher`. Each scorer ran once, as in the Dehn pre-score.
- **Raw outputs.** `blind/raw/blind-{A,B}-{G1,G2}.json` hold each scorer's final JSON verbatim, taken directly from its hand-back.

## Scores

| candidate | scorer A | scorer B |
|---|---|---|
| G1 (example for k = 10, Lean) | 4 / 3, warning, 1 finding | 4 / 3, warning, 1 finding |
| G2 (G1 + C(6) classification, outside Lean) | 4 / 3, warning, 1 finding | 4 / 4, neutral, no finding |

(notability / literature; the floor is 4; notability is mandatory, and literature at 3 with a `warning` does not block.)

**Why notability holds at 4.** All four scorers give the same reasons:
- Grünbaum published the question in print (*Math. Intelligencer* 2010), and his "no information is available for any k ≥ 10" is quoted accurately (all four checked his author's version).
- There is a specialist audience: parallelohedra and nonconvex space-fillers, the Venkov–McMullen and Senechal–Taylor circle, and golden-rhombohedron and quasicrystal polyhedra.
- A proved example of every property Grünbaum asks for is plausibly a research note.

**Why it is not 5.** The interest is specialist. A solid of the same family was already on the web without proof, so the existence statement at k = 10 is less new.

The classification (G2) is credited as "structural" and "the main lever toward broader interest", but only if it is formalized. As an informal computation it did not move notability.

**The literature finding (A-G1, B-G1, A-G2, each on its own).** D. Hall, "Dimpled Rhombic Triacontahedron – Construction", Sketchfab, 28 June 2016, with a companion model "DRT with Positive Tetrahedral Translation", 11 July 2016:
- one golden rhombohedron is removed at each of four vertices with tetrahedral symmetry;
- it is chiral;
- it is called "a delightful new space filling polyhedron", packing as a lattice in which 14 copies enclose one.

That is very likely Inchbald's solid (our candidate 2, with 12 rotations). It is not GET A or GET B. The scorers also name J. Kostick's vZome arrays of dimpled triacontahedra (3 April 2022). None of these sources mentions zones or Grünbaum's question, and none gives a proof. All three say GET A is not in them.

**My check.** I fetched the first Hall page myself. It confirms the title, the author, the date 28 June 2016, the tetrahedral four-dimple construction, "chiral" and the lattice packing. The finding is real. B-G2 also saw a Sketchfab hit but treated it as "further web presence" and not as a finding. That is the only difference between the 4 and the 3s.

## Review of the reviews

**Correct, and to act on:**
1. Hall 2016 must be cited as the earliest known appearance of the tetrahedrally dimpled triacontahedron as a space-filler, and the Inchbald-first wording must go. This also bears on the Concordance and DICTOnary entry "The indented rhombic triacontahedron (Inchbald / Senechal–Taylor, c. 2023)", which should become Hall 2016 first. DICTO decides the name.
2. Kostick's vZome pages (April 2022) should be checked: is any single-tile array GET A or GET B? Kabai's 54-faced space-filler should get a one-line comparison. It is not in class C(6), since it has 54 faces.
3. Say outright that GET A, GET B and the Hall/Inchbald solid contradict Grünbaum's remark that "none of the other isozonohedra obtainable by indentation of F or T seem to be parallelohedra" (all four scorers).
4. Cite Grünbaum's web "Supplement to Bilinski" (the P_n family; "multiple indentations of T not examined in detail") with one line on why P_n does not give uniform zones of 10 (three scorers).
5. Search the other proof libraries (AFP, Rocq, HOL Light, Mizar) and record the search (all four).

**Not needed for the floor, but useful:**
- Read Senechal–Taylor 2023 in full and quote her reply word for word. This replaces the private correspondence with a checkable source.
- Bring GET B and the non-congruence into Lean (two scorers).
- Formalize the C(6) classification (two scorers). This was the only route the scorers named toward a higher notability, and it is a large job.

**Over-reaching:** k ≥ 12 is named as a way to broaden interest. A separate study (2026-11-16-echo-shapes) already argues that k ≥ 12 is impossible in the class where every two zones cross. That would answer it, but it is not part of this entry. I keep it as a lead, not a change.

**Final estimate:** notability 4 (four of four), literature 4 once Hall 2016 is cited. The outcome would then be `neutral`, at the floor. As with Yantra and Dehn, production runs can vary by about one point. G1 is enough. G2's informal classification adds no score, and it carries the risk that a reviewer treats an unformalized claim as part of the checked result. It fits better in the informal account than as a scored group.

## LEADS

1. Cite Hall 2016 (both Sketchfab models) in the GET entry metadata, the GET paper and the Concordance. Rename the known atom's attribution (Hall 2016; Inchbald 2023; Senechal–Taylor if confirmed), with DICTO's word on the name.
2. Run an exact congruence check: Hall's chiral DRT against our candidate 2. Both hands are needed, because Hall says it is chiral and candidate 2 has 12 rotations.
3. Check Kostick's vZome arrays (2022) for GET A or GET B, and for any other single-tile k = 10 solid.
4. Write the GET entry's `formalization.yaml` literature section with Hall, Kostick, Inchbald, Grünbaum's Supplement, the "indentation remark contradicted" sentence, and a recorded search of the proof libraries.
5. Get Senechal's exact words (DICTO), and the full text of Senechal–Taylor 2023 by a free route.
6. Optional, after DICTO's word: bring GET B and the non-congruence into Lean. Then consider the C(6) classification in Lean, the only notability lever the scorers named.
7. Re-score blind once with the corrected literature (one pair, G1 only) before any submission.

## Files

- `blind/policy/`: the policy files (byte-identical copies).
- `blind/inputs/G1-grunbaum-k10-example.md`, `blind/inputs/G2-grunbaum-k10-classification.md`: what the scorers saw.
- `blind/scorer-prompt.md`: the scorer prompt (INPUT, POLICY and CAND were filled in per scorer).
- `blind/raw/blind-A-G1.json`, `blind-B-G1.json`, `blind-A-G2.json`, `blind-B-G2.json`: the raw scorer outputs.

Nothing heavy was run on this machine, and nothing is left running.

FINAL ok
