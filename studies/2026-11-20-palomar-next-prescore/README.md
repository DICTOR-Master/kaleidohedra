# Palomar pre-score: explicit scissors congruences (E1) and the Dehn invariant in four dimensions (E2) (20 November 2026)

**Verdict: E1 falls below the floor. Both scorers give notability 3, outcome `failure`. The reason is that a hand-picked list of instances of a classical existence theorem shows no research interest. E2 holds notability 4, at the floor, in both scores: A gives 4 / 4, `neutral`; B gives 4 / 3, `warning`. B's single finding is that Hadwiger is not cited. The dihedral-angle check left four of the six regular 4-polytopes with invariant zero, so E2 was framed on the pairs that actually differ, and both scorers accepted that framing. Nothing was submitted, and nothing is built yet: both candidates are proposals.**

DICTO approved the pre-score on 20 November. The method is the same as in the Grünbaum pre-score (studies/2026-11-20-palomar-grunbaum-prescore) and the Dehn pre-score (studies/2026-11-19-palomar-dehn/blind).

## Method

- **Policy.** `blind/policy/` holds CONTRIBUTING §1 and §7, prompt 04 (literature and notability) and rubric.json. They are byte-identical to the Dehn and Grünbaum copies (checked with `cmp`).
- **Inputs.** `blind/inputs/` holds two neutral descriptions. DICTO is not named. Each input states only claims that the entry would prove, and says that the proof is not yet built. Each says that it builds on the registered entry "PALOMAR-2026-11-20-000003, the Dehn invariant read from the solid, with the bridge from convex dissections".
  - **E1** (`E1-explicit-scissors-congruences.md`): `ScissorsCongruent P (cube of side (volume P)^(1/3))`, using the registered entry's definition, with exact pieces. P runs over the rhombic dodecahedron, the truncated octahedron, both golden rhombohedra, the cube ∩ rhombic dodecahedron family, and the nine most regular space-fillers. It is framed honestly: the individual dissections are classical or follow from Sydler or Debrunner, and what is new is the machine check.
  - **E2** (`E2-dehn-invariant-4d.md`): it has five parts:
    - the set-defined 4D invariant, using 2-dimensional Hausdorff measure on the points whose cone has a plane as lineality space;
    - the ridge-sum identity;
    - the bridge;
    - the table of the six regular invariants;
    - non-congruence of the pairs that differ.

    Jessen (1968, 1972) and Dupont are credited.
- **Dihedral-angle check, done before writing E2** (`checks/`, all FINAL ok):

  | polytope | dihedral angle | in ℚπ | 4D invariant |
  |---|---|---|---|
  | 5-cell | arccos(1/4) ≈ 75.52° | no | nonzero |
  | tesseract | π/2 | yes | 0 |
  | 16-cell | 2π/3 | yes | 0 |
  | 24-cell | 2π/3 | yes | 0 |
  | 120-cell | 4π/5 | yes | 0 |
  | 600-cell | arccos(−(1+3√5)/8) = π/3 + arccos(−1/4) ≈ 164.48° | no | nonzero |

  The angles were computed from coordinates (`dihedral4d.py`) and checked against Wikipedia's wikitext, which cites Coxeter's Table I(ii). The 24-cell value rests on the coordinates together with Coxeter as cited. Two angles are not in ℚπ, by the algebraic-integer test (`rational_pi.py`). The 600-cell angle is θ₆₀₀ = 4π/3 − θ₅ exactly (`relation_600_5.py`), so θ₆₀₀ ≡ −θ₅ (mod ℚπ). The two nonzero invariants are A₅⊗[θ₅] and −A₆₀₀⊗[θ₅], so they differ at every scale.

  **Four of the six vanish, so E2 was re-framed.** It now claims only the following: the 5-cell and the 600-cell are each not scissors congruent to any of the four zero-invariant polytopes, and they are not scissors congruent to each other. It says outright that the tesseract, 16-cell, 24-cell and 120-cell are not separated by the invariant. By Jessen's theorem, any two of them with equal volume are scissors congruent.
- **Scorers.** Four fresh general-purpose agents ran in parallel, two per candidate, and each ran once. Each was given only the four policy files and one input. Each could search the web and read pages, and none wrote files. The prompt is `blind/scorer-prompt.md`, the same text as before with CAND set to E1 or E2.
- **Raw outputs.** `blind/raw/blind-{A,B}-{E1,E2}.json` hold each scorer's final JSON verbatim.

## Scores

| candidate | scorer A | scorer B |
|---|---|---|
| E1: explicit scissors congruences | **3** / 3, failure, 2 findings | **3** / 4, failure, 2 findings |
| E2: Dehn invariant in 4D | 4 / 4, neutral, no finding | 4 / 3, warning, 1 finding |

(notability / literature; the floor is 4; notability is mandatory.)

**E1: why 3.** Both scorers give the same two findings:
1. **No research interest shown.** The entry is a finite list of instances of Debrunner (1980) and Dehn–Sydler. Several of them are already in the recreational literature (Frederickson; Hanegraaf; Theobald 11 pieces; Paterson). Only the machine check is claimed, and §1 says formal correctness alone does not count. No audience is named, and nothing says why this list matters.
2. **"The nine most regular space-fillers" and "Bain rhombic dodecahedron" have no source.** The count of nine has neither a citation nor a proof of completeness, and "Bain" is not a standard name.

B adds a note that Debrunner's theorem covers periodic tilings, and that the general case is Lagarias–Moews. This does not matter here, because every listed solid tiles periodically.

**E2: why 4 and not more.** Both scorers rest notability on items 2 and 3, the ridge-sum identity and the bridge in 4D with 2-dimensional strata. These are classical theory at paper level (Hadwiger, Jessen), and a set-based definition with a new geometric-measure argument adds to that. The table and the non-congruence results "alone would be routine exercises". The risk both name is that a reviewer reads the entry as the 3D entry "one dimension up".

**B's finding (E2): Hadwiger is not cited.** Hadwiger introduced the codimension-2 invariant in Eⁿ and proved it invariant (Math. Ann. 127 (1954) 170–174; *Vorlesungen über Inhalt, Oberfläche und Isoperimetrie*, 1957). It is usually called the Dehn–Hadwiger invariant. A saw the same omission but recorded it as a note, not a finding.

**Accuracy.** All the arithmetic was checked independently by both E2 scorers: the angles, the irrationality argument, θ₆₀₀ = 4π/3 − θ₅, and the claim that the two nonzero invariants are opposite multiples. The E1 scorers both checked the cube ∩ RD angles (90°, 120°, 135°).

## Prior art (`prior-art.md`)

No formal versions of any of the following were found in Lean or Mathlib, Isabelle AFP, Coq/Rocq, HOL Light, Metamath or Mizar:
- an explicit polyhedral dissection into a cube;
- Sydler's theorem;
- the Wallace–Bolyai–Gerwien theorem;
- any Dehn invariant in dimension 4.

The 19 Nov Dehn prior-art record is reused, and today's GitHub code searches and web searches are added. All four scorers searched independently and found nothing either. **Priority:** I found no source with a table of the six regular 4D invariants, and none with θ₆₀₀ ≡ −θ₅ (mod ℚπ). Both follow at once from classical angles, so no discovery is claimed. A cites a valuations survey (arXiv:2302.00416, snippet only) that gives a dimension-general argument that the regular simplex is not scissors congruent to the cube. The 5-cell part of item 5 is therefore known.

## Review of the reviews

**Correct, and to act on:**
1. E1 as stated should not go forward. Both scorers are right that a list of instances does not meet §1. Better prose will not fix it.
2. E2 needs these citations:
   - Hadwiger 1954 and 1957 for the invariant and its invariance, crediting it as the Dehn–Hadwiger invariant;
   - Dupont–Sah, Acta Math. 164 (1990) 1–27, for the group-homology proofs;
   - a statement that the simplex-versus-cube non-congruence is classical in dimension 4.

   The input is mine, and the Hadwiger omission was mine.
3. The Zakharevich attribution in E2 ("complete in dimensions 3 and 4, open from 5") is not in the abstract of arXiv:1101.3833. Re-source it (both E2 scorers say so).
4. The E1 family, if it is ever used: source or derive "the nine most regular space-fillers", and use standard names or descriptions of how each solid is generated. "Bain rhombic dodecahedron" is DICTO's name, and in public text the known shapes need their regular names and discoverers.

**Not needed for the floor, but these are the levers the scorers named:**
- E2: make the bridge the headline, with the table and non-congruence as corollaries. Name the audience: scissors congruence, K-theory, valuations. A higher reach is the codimension-2 invariant in every dimension n ≥ 3, or one sufficiency instance in 4D, such as an explicit dissection of the 24-cell or the 16-cell into a 4-cube.
- E1 could be rebuilt as a general theorem: a formal Wallace–Bolyai–Gerwien in the plane plus box to cube, then every parallelepiped, zonotope or parallelohedron to a cube by one construction. The listed solids would then be corollaries. All three of these (WBG, box to cube, zonotope to cube) were found unformalized. That is a different, larger entry.

**Over-reaching:** B's suggestion of "an effective Sydler for all rational-dihedral polyhedra" is a research problem, not an entry change. I keep it as a lead only.

**Final estimate.** E2 is notability 4 in two of two. Literature would be 4 once Hadwiger and Dupont–Sah are cited, giving outcome `neutral` at the floor. As before, production runs can vary by about a point, and E2 carries the extra risk of being read as "3D one dimension up". E1 is notability 3 in two of two, below the floor.

**Recommendation.** Drop E1 in its present form. If DICTO wants the dissection direction, the version that could pass is the general one: formal WBG plus box to cube, then all parallelohedra. It needs his word, because it is a new project. E2 is the candidate to build. Before any build, fix the three citations, and pre-score again blind once (one pair) on the built Challenge.

## LEADS

1. E2 input: add Hadwiger 1954 and 1957 (Dehn–Hadwiger), Dupont–Sah 1990, Debrunner beside Lagarias–Moews, and a correct source for the dimension-≥5 remark. Read Hadwiger 1954 (EuDML 160370, free) and Dupont 2001 (author's free copy).
2. E2 Lean plan: carry the 3D modules (cones, wedge angles, plane cut, common refinement) to `finrank = 4` with μH[2]. Headline: the bridge. Then the six-polytope table and the non-congruence results as corollaries.
3. Outside the plan (one line, as a 4D echo of the tetrahedron and octahedron): since θ₆₀₀ ≡ −θ₅, a 600-cell together with 5-cells of the same total ridge area has invariant zero. By Jessen, such a union is scissors congruent to a 4-cube. Is there a natural 4D packing that realises this, as the octet truss does in 3D? Only if DICTO wants it.
4. E1 rebuilt (needs DICTO's word): formal Wallace–Bolyai–Gerwien, box to cube, and zonotope or parallelohedron to cube, with the listed solids as corollaries. Pre-score that general statement blind before any build.
5. The "nine most regular space-fillers" classification: write down its derivation, or find a source. Map each solid to its standard name (Fedorov parallelohedra; Bain for the RD form, if it is from a source).
6. Pre-score E2 again blind (one pair) once the citations are corrected and the Challenge is built.

## Files

- `blind/policy/`: the policy files (byte-identical copies).
- `blind/inputs/E1-explicit-scissors-congruences.md`, `blind/inputs/E2-dehn-invariant-4d.md`: what the scorers saw.
- `blind/scorer-prompt.md`: the scorer prompt template.
- `blind/raw/blind-A-E1.json`, `blind-B-E1.json`, `blind-A-E2.json`, `blind-B-E2.json`: the raw scorer outputs.
- `checks/dihedral4d.py`, `checks/rational_pi.py`, `checks/relation_600_5.py` with their `.log` files: the angle checks (light; at most 600 points).
- `prior-art.md`: the prior-art record.

Nothing heavy was run on this machine, and nothing is left running.

FINAL ok
