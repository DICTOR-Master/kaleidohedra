# Fresh referee report: #118 draft Version 2 (24 November 2026)

Paper: "Icosahedral Cores in Golden Rhombohedra: Scutoid-Frusta Cells for the Ammann–Kramer–Neri Tiling", `paper.html`, draft Version 2, and its PDF (15 pages, same build time as the HTML).

Read independently: the paper, the study folder `2026-11-21-amber-ammann` (scripts, logs, data), the Lean study `2026-11-24-lean-amber-mirror`, #117, and the open sources [1], [9], [10], [11], [12]. Not read: the audit note, any other referee file, the commit messages.

## Verdict

**Ready after minor fixes.** No main result is wrong. Every count in the text, tables and captions that I recomputed agrees with the logs and with an independent rebuild of the patch. Two statements are false or unsupported as written (findings 1 and 2), three are stronger than what is proved (3, 4, 6), and the proof of Theorem 1 (c) leaves out two steps that the script relies on (5). All can be fixed in the text; finding 2 also needs one added exact comparison, and finding 7 one re-rendered figure label.

## Findings, in order of severity

### 1. Theorem 1 (b): the stated bound is false by rounding

- **Where:** Theorem 1 (b), "by at least 0.0806".
- **Problem:** The smallest prolate–oblate volume gap is 0.080553, which is less than 0.0806, so "at least 0.0806" is not true.
- **Evidence:** `logs/exact/summary/C2_S0_cen.txt`: closest pair 7.571397 and 7.490844, "exact difference … = 0.080553". The proof's "≈ 0.0806" is a correct rounding; the statement turned a rounded value into a lower bound.
- **Fix:** "by more than 0.0805" (or "by at least 0.08055").

### 2. Theorem 1, last sentence, and Proposition 4 / Table 2: the "own" settings

- **Where:** Theorem 1 "The same holds … with each cell at its own s0 (centroid seeds) … none shared"; Table 2 rows with "own" (Rollerball, icosahedron, dodecahedron).
- **Problem:** With each cell at its own s0 the cores in one tiling have two sizes (ratio φ), which contradicts the theorem's "all of one size" and is not said; and the "none shared" check for these rows compares piece volumes with a core of edge 1 in both cells, which is not the pair of sizes that occurs in one tiling.
- **Evidence:** The study README defines "own" as "each cell at its own s0 (two core sizes)". `exact_summary.py` (scale `1`) takes each run at its own s0 with core edge 1 and tests the two volume lists for disjointness as they stand. In a tiling the cell edges are equal, so the oblate pieces are smaller by the factor 1/φ and their volumes by φ⁻³ = √5 − 2. I redid the comparison with that factor, exactly in ℚ(√5), from the logged exact volumes: Rollerball 8 × 8, icosahedron 3 × 3, dodecahedron 2 × 2 pairs, no coincidence (smallest gaps: Rollerball 9.376035 against 9.186339; icosahedron 0.224249 against 0.218169). So the claim is true, but the logged check does not prove it.
- **Fix:** Say in the theorem and under Table 2 that "own" means two core sizes in the ratio φ (prolate core larger). Add the rescaled comparison to `exact_summary.py` for scale `1` and cite it. Theorem 3 (v) already excludes the own-scale settings; keep that.

### 3. Abstract: "The tiling has no symmetry other than the identity" is proved for one tiling only

- **Where:** Abstract, sentence beginning "The tiling has no symmetry other than the identity"; also the inside text of Figure 2 (finding 7).
- **Problem:** In the abstract "the tiling" reads as the Ammann–Kramer–Neri tiling in general, but Theorem 1 (c) proves "no rotation or mirror" only for the tiling of Lemma 2 (one value of γ); for the class only "no period" is proved.
- **Evidence:** Theorem 1 (c): "for the tiling of Lemma 2 both have no symmetry other than the identity". `sym_check.py` part A4 tests the 120 elements for this γ only. Whether other tilings of the class have a rotation or mirror symmetry is not examined.
- **Fix:** "The tiling built here has no symmetry other than the identity …; no tiling of the class has a period."

### 4. After Figure 4: "(iv) holds for every infinite tiling of the class" rests on the wrong fact

- **Where:** §5, paragraph after Figure 4: "cut-and-project tilings are repetitive, so a translate of the patch occurs in each one (Moody [9], §3)".
- **Problem:** Repetitivity says a patch of one tiling recurs in that same tiling; that it occurs in every other tiling of the class needs local isomorphism of the class, which is a different statement.
- **Evidence:** Moody §3 says only "Λ is repetitive if it is generic". The statement needed is in Moody §6 (Theorems 8 to 10: the generic model sets of one window are parametrised by one minimal system, each with a unique preimage in the hull, so they are locally isomorphic), or it follows directly from the density of π′(ℤ⁶), which `sym_check.py` A2 proves exactly (the set of γ at which the patch occurs is open and non-empty, and every generic γ′ meets it after a shift by π′(k)).
- **Fix:** Cite Moody §6 (Theorems 8 to 10) or give the two-line density argument, and say "every generic tiling of the class".

### 5. Theorem 1 (c): three steps of the proof are missing from the paper

- **Where:** Proof of Theorem 1 (c), from "The same argument carries an isometry of the layer" to "ending FINAL ok".
- **Problem:** (a) The reduction of "symmetry of the infinite tiling" to a finite test is not stated; (b) "the tiling of Lemma 2" does not say whether the 402-cell patch or the infinite tiling is meant; (c) for a general face-to-face T the proof that every symmetry of T is a symmetry of the layer uses a linear part in I_h, which is shown only for the tiling of Lemma 2.
- **Evidence:** (a) `sym_check.py` A4 uses: x ↦ gx + t is a symmetry of T_γ exactly when t = π(k) with π′(k) = γ − g′γ. Its docstring refers to a lemma in a private note; the paper gives neither statement nor proof. I checked the criterion: g acts on ℤ⁶ as a signed permutation with gπ = πσ and g′π′ = π′σ, so gT_γ + π(k) = T_{g′γ + π′(k)}, and T_γ determines γ because π′(ℤ⁶) is dense. It is correct, but it must be in the paper. (b) The script checks both (A4 the infinite tiling, B the patch); the theorem should say "the infinite tiling T_γ of §2". (c) The statement "a translation, rotation or mirror maps the layer onto itself exactly when it maps T onto itself" is made for every T of the theorem, including tilings that use fewer than six axes.
- **Fix:** Add the criterion with its three-line proof. Name the infinite tiling. For (c) add: an isometry that carries three independent axes of the star to axes of the star lies in I_h, because I_h is transitive on the triples of each type and the stabiliser D3d is the full symmetry group of the three lines.

### 6. §5, opening sentence: "moving the cores cannot make them" is stronger than Theorem 3

- **Where:** §5, the lead under the heading: "Where a prolate cell meets an oblate one, they never do, and moving the cores cannot make them."
- **Problem:** Theorem 3 (iv) proves only that the cores cannot all be mirror images of their neighbours; that no other placement lines up a prolate–oblate wall is Remark 5, which is marked argued, not proved.
- **Evidence:** Abstract and §1 word this correctly ("forced within the mechanism that closes the same-type walls"; "argued, not proved"). The §5 lead does not.
- **Fix:** "…they never do, and the cores cannot all be placed as mirror images of their neighbours."

### 7. Figure 2: the label inside the figure gives the argument that Version 2 withdrew

- **Where:** Figure 2, text inside the image: "prolate : oblate = golden ratio, so no period".
- **Problem:** An irrational ratio of frequencies rules out a full lattice of periods, not a single period; the Version 2 proof rightly uses the injectivity of the star map instead, and the figure still shows the old reason.
- **Evidence:** Status box: "The proof of Theorem 1 (c) now uses the cut-and-project fact for 'no period' (Moody) in place of the frequency argument". The image was not re-rendered (its file date is 22 November; Figures 3 and 4 are 24 November).
- **Fix:** Re-render with "prolate : oblate = golden ratio · no period".

### 8. Proof of Theorem 3 (v) cites a private file

- **Where:** Proof of (v): "which reproduces the referee check of 24 November 2026, REFEREE-120-2026-11-24.md §4" and "the referee's exact check, §5 of the same report".
- **Problem:** A reader cannot open that file and is not told who "the referee" is; the two scripts and logs named beside it already carry the proof.
- **Fix:** Drop both clauses, or say "an independent exact check" and put the report in the public data folder.

### 9. Remark 5: credit for the power-diagram fact

- **Where:** Remark 5: "the fact goes back to Aurenhammer 1987 [13]", with [13] "not opened; cited through [12]".
- **Problem:** The opened source [12] does not give that credit at the place cited.
- **Evidence:** Aurenhammer's survey §3.1.5 opens "the observations described below [Aurenhammer and Imai 1988]" and concludes "any Voronoi diagram whose separators are hyperplanes is a power diagram". Aurenhammer 1987 is cited in §3.1.1 for the correspondence between power diagrams and polyhedra one dimension up. §3.1.1 (definition of power, power cell, power diagram) and §3.1.5 are otherwise as the paper says.
- **Fix:** "(… §3.1.5, credited there to Aurenhammer and Imai 1988; power diagrams themselves: Aurenhammer 1987 [13], cited through [12], §3.1.1)". The two-line identity in the remark already proves the step used.

### 10. Remark 5: one sentence is imprecise

- **Where:** "Two weighted sets give the same diagram only when their power functions differ by a common positive factor and a common affine function."
- **Problem:** What must agree up to a common positive factor λ are the differences pow_i − pow_j; pow_i − λ pow′_i is then common to all i but is affine only when λ = 1.
- **Fix:** "…only when the differences of their power functions agree up to one common positive factor (for neighbouring regions; equal round a vertex where three meet)". The remark stays "argued".

### 11. Release items the status box does not list

- **Where:** Meta line and status box ("At release … moves to a commit that holds odd_edges.py, sym_check.py, buried_hex.py and the Lean study").
- **Problem:** The linked commit 8d5653d7 also lacks `wall_configs.py`, `wall_disjoint.py` and `stacked_pairs.py`, which Theorem 3 (v) cites; and `zenodo-metadata.json` beside the paper still has the Version 1 title ("Scutoid Cells"), abstract ("true scutoids") and version.
- **Evidence:** `git ls-tree 8d5653d7` of the study's scripts folder shows 16 files, none of the six. The public link itself answers (HTTP 200); the three DICTO DOIs [5], [6], [7] resolve to the titles given.
- **Fix:** Add the three scripts and their logs to the release list; update the metadata file at release.

### 12. Clarity (small)

- **Index labels:** the vectors are e1 … e6 but the orientations are called 023 and 012 (counting from 0) in the proof of Theorem 1 (a) and in Figure 3's caption. Say once that orientations are labelled by indices 0 to 5, or write 134 and 123.
- **"Y-corners"** appears once (Figure 3 caption); everywhere else "Y-vertices". Use one.
- **Numbering:** Lemma 2 comes before Theorem 1 and Proposition 4 before Theorem 3 in reading order. Acceptable if deliberate (the theorems carry the low numbers); a reader will look twice.
- **§2, "The division":** "unchanged except for the mould (the rhombohedron), the symmetry group used to sort the pieces into orbits" lacks "and"; a reader expects a third item.
- **Remark 6** does not give the scale and seed rule of the 30 runs (S0, centroid seeds, per the logs).
- **Figure 4, left panel:** where a pale blue line runs on top of a yellow one the two patterns share that segment, and it reads as a third colour that the legend does not explain. Add to the caption: "where both cells draw the same segment the pale blue line lies on the yellow". This also heads off a misreading of (v): the patterns share no region, but they do share segments.
- **Term in the earlier papers:** #104, #114 and #117 call the same pieces "scutoids" (their titles say so). One clause at the definition in §2 ("called scutoids in #104, #114 and #117") would stop a reader thinking a different object is meant.

## The seven checks

1. **Theorems.** Theorem 1 (a), (b): true; (b)'s bound to correct (finding 1); own-scale clause (finding 2). Theorem 1 (c): true; proof gaps (finding 5). Lemma 2: true and complete; all its numbers reproduced. Proposition 4: true; own rows as finding 2. Theorem 3 (i) to (v): true. For (v) I checked the count by hand (24 isometries, orbits of 12, 2 placements per side and type; 8 prolate–oblate, 4 + 4 same-type per rhombus; half mirror, half stacked), the induction to one six-axis star, and the stacked-pair exclusion (a coefficient of absolute value exactly 1, so on the window boundary). Scope is stated correctly: same-type agreement only in the cut-and-project tilings, prolate–oblate disagreement in every face-to-face tiling, common-scale settings only. The Lean theorem `no_mirror_placement` states what the paper says it does, builds clean, and depends only on the three standard axioms; its three planes are the ones in `logs/odd_edges.log`, and the paper's "z = 0" and "z = −(1 + √5)/2" match `plane1_plane3_z` and `plane2_z`.
2. **Numbers.** Rebuilt the patch independently from the definition in §2 (not from the study's code): 402 tiles, 278 + 124, identical tile set to `data/patch.json`; 1414 faces = 998 shared + 416 boundary; walls 319 / 61 / 618; 0 stacked; 814 interior edges with 364, 239, 156, 13, 30, 10, 2 cells round them, 552 odd; window ratio φ; 120 of 120 prolate–oblate configurations present. 1856.899327 = 958 + 402√5. Table 1: all five products s0(prolate)·φ = s0(oblate) by hand; the icosahedron and Rollerball values rederived from the half-width along a two-fold axis. Table A1: the pieces per cell sum to 72, the Y incidences to 180 = 30 × 6 in both cells, and the volumes sum to cell minus Rollerball (1598.78 and 954.78). Table 2: every row against `logs/exact/summary/`. 597 = 27 + 368 + 202; 96 planes; 30 wall-cast failures; (−83 + 55√5)/4 < (15 + 3√5)/2. `scripts/audit.py` prints AUDIT OK. Only finding 1 is a wrong number.
3. **Citations.** Moody: §3 "Lack of periodicity is automatic … as long as the mapping ∗ is injective" and §5 Theorem 2 (credited to Schlottmann and Hof) are there as cited; the repetitivity citation does not carry the step it is used for (finding 4). Baake and Grimm: "pioneered by Kramer and Neri … Ammann described the tiling earlier … Mackay's early paper", as cited. Frettlöh: history and ℤ⁶, as cited. Senechal: Ammann's letters to Gardner, April 1976, with marked nets, as cited. Aurenhammer: finding 9. Kramer–Neri and Mackay are honestly marked not opened. #117: Theorem 15, Proposition 17 (Rollerball: 4 kinds, 72 of 72, 30), Figure 4, §6 and §8 are as cited; projected seeds are mentioned there. No missing credit for a borrowed method found.
4. **Figures.** Figure 1 matches. Figure 2: 19 + 11 per the scene log; inside text as finding 7. Figure 3: orientations, 72 pieces, 8 kinds per cell as captioned; the 180 dots follow from the drawing code (each Y dot drawn on each piece that has it). Figure 4: 16 + 16 and 16 regions per the scene log; colours match the caption; see the clarity note.
5. **Abstract and contributions against the body.** Findings 3 and 6. The rest is no stronger than proved; "argued, not proved" is said where it applies.
6. **Terminology.** "Scutoid-Frusta" 41 times, "Scutoid-Frustum" 6 times, always hyphenated and capitalised; no unhyphenated form; bare "scutoids" only for the biological ones, for prior art and in titles of earlier papers. The first-use sentence in the abstract is correct and credits Gómez-Gálvez et al.; the definition follows in §2. The figures' inside text uses the term too.
7. **Clarity.** Finding 12.

## A strengthening, not a fault

Lemma 2 (iii) and the contributions present s0(oblate) = φ·s0(prolate) as a computed fact for five cores. It holds by hand for every core with the symmetry I_h: by Theorem 3 (i) every wall is perpendicular to a two-fold axis, the core's half-width w is the same along all 15 of them, and the walls of the two cells at scale s lie at distances s·φ/6 and s/6 from the centre, so s0 = 6w/φ and 6w. One sentence would turn five checks into a rule.
