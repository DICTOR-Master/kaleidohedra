# Open problems stated by others that DICTO's work can close (15 November 2026)

**Verdict.** One problem is already partly closed by DICTO's published work. One more short certified computation could close it fully. That problem is Kulaichev's question whether the Śrī Yantra with his four extra conditions is unique (1984). Chiodo, in Comptes Rendus Mathématique 2021, calls it "toujours ouverte" (still open).

#103 Theorem 10 already gives that yantra exactly: degree 348, against Kulaichev's published bound of 12544. Its existence is certified, and its region count is certified at 45. A blind Palomar pre-score gives Theorem 10 as it stands **notability 4 / literature 4** (`neutral`, at the floor). It gives the same 4 / 4 to the version with uniqueness proved. This is the first candidate of DICTO's to reach 4 in any of our replays. Earlier replays scored 2–3.

**Top five, ranked by (chance DICTO's work can close it) × (Palomar fit):**

| Rank | Stated problem (owner, place) | DICTO's handle | What closing needs | Chance × fit |
|---|---|---|---|---|
| 1 | **Uniqueness and exact form of Kulaichev's Śrī Yantra.** Kulaichev 1984, IJHS 19.3, p. 285 (degree bound 12544); "toujours ouverte": Chiodo 2021, C. R. Math. 359, p. 384 (English §1.2.4, p. 387); "probably impossible" analytically: Pustynski 2014, IJHS 49.3, p. 275 | #103 Thm 10 (degree 348, certified); audit certificates (2026-11-09-yantra-audit) | The exact form is **done**. Uniqueness: every real root of the full eliminant (degree 1744, already factored) tested for admissibility, plus the degenerate loci of the elimination | **high × high** |
| 2 | **Which of the 40 sporadic rational tetrahedra tile space.** Chentouf–Sun 2023, arXiv:2312.01654, Thm 1.2 ("at most 40"; "the goal … not fully attained", §1.1). The list comes from Kedlaya–Kolpakov–Poonen–Rubinstein 2020; the wider question is Senechal 1981 | #102 (Dehn test; exact-cover tiling checker, Thm 2.4); #92/#93 reversed-neighbour search proofs; #44 Aristotle's pyramid | For each case, either an explicit tiling or a certified obstruction. Several cases have π/5 angles, which is DICTO's icosahedral territory | medium × high |
| 3 | **Rhombic monohedral parallelohedron with every zone of exactly k faces, k ≥ 10.** Grünbaum 2010, Bilinski paper, p. 17 of v2/3/10 (Math. Intelligencer 32(4), 2010): "No information is available for any k ≥ 10" | Golden-rhombus solids (#29 Theaetetus/Cleo; #30–#38 OG family, Palintriacontahedron, Metaxyhexecontahedron); #1, #2 parallelohedra | One explicit sphere-like polyhedron of congruent rhombi, every zone with 10 (or 12, …) faces, tiling by translations. The proof is constructive | medium-low × high |
| 4 | **Goldberg's space-filling pentahedra: "It is still not known whether all the space-filling pentahedra have been found"** (Goldberg 1974, JCTA 17, p. 378, §6). Closable part: the quadrilateral pyramids | #44, #77, #92 (Aristotle's pyramid, square pyramids, face to face); #102 Dehn sweeps | Classify a named sub-family exactly, such as the square pyramids by apex height, with tilings and obstructions. A full classification is out of reach | medium-low × medium |
| 5 | **Tsiokos 2026, §10 Q8: "Does the same design yield einsteins … on other lattices?"** Q5 asks for the fewest faces of a strongly aperiodic monotile in ℝ³ (arXiv:2609.19214, pp. 46–47) | RD bridge (2026-11-12-rd-bridge: 118 marked RDs carry the chair hierarchy on fcc); repro-tsiokos; aim 3 | One rhombic dodecahedron with features that force the chair hierarchy on fcc. That is aim 3 itself | low × very high |

**Status:** desk study plus one blind replay. No new computation was run and no account or contact was made. Nothing was submitted.

---

## 1. Candidate 1 in full: Kulaichev's Śrī Yantra

### 1.1 The problem as stated in print

- **Kulaichev 1984.** A. P. Kulaichev, "Śrīyantra and its mathematical properties", *Indian J. History of Science* 19.3 (1984) 279–292.
  - He fixes one plain yantra by the classical conditions plus four more:
    - (a) the two great triangles t3 and t7 are congruent;
    - (b) t1's base corners lie on the circle;
    - (c) t9's base corners lie on the circle;
    - (d) the incircle of the innermost triangle is concentric with the circle.
  - With (a), (b), (c) and the inscribed great triangles, ten corners lie on the circle.
  - He argues for a solution by iterated approximation (p. 284) and asks whether it is unique (p. 285).
  - He reduces the system to one polynomial "of a single variable with a power not higher than 12544" (quoted by Pustynski, p. 269) and judges uniqueness beyond the computers of the time.
  - The scan we hold has no text layer, so pages 284 and 285 are as Chiodo cites them.
- **Pustynski 2014.** V.-V. Pustynski, *IJHS* 49.3 (2014) 268–277 (full text read).
  - He solves the system to 15 figures (Table 1, p. 274).
  - He argues uniqueness from residual plots on dense grids (pp. 273–274: "there is evidently no chance that local extrema could have been missed"). This is numerical evidence, not a proof.
  - He concludes (p. 275): "Unfortunately, purely analytical solution of the final two steps is probably impossible since the corresponding equations are too unwieldy."
  - He notes "two additional tiny triangles" (p. 275).
- **Chiodo 2021.** A. Chiodo, "On the construction of the Śrī Yantra", *C. R. Mathématique* 359 (2021) 377–397, doi:10.5802/crmath.163 (full text read).
  - French version, p. 384: Kulaichev "fournit un raisonnement qui indique l'existence d'une solution et il se pose la question (toujours ouverte) de l'unicité" (he gives an argument that indicates a solution exists, and asks the question of uniqueness, which is still open).
  - English §1.2.4 "The search for a unique Śrī Yantra", p. 387: "This problem is not considered here."
- **Chapati–Chapati 2026** (Zenodo 23188650) state that the system has no closed-form solution.

So, as stated in print:
- **existence** is "indicated", not proved (Chiodo);
- **uniqueness** is explicitly open (Chiodo);
- an **exact or analytic solution** was judged "probably impossible" (Pustynski);
- the **degree** was bounded by 12544 (Kulaichev).

### 1.2 What #103 proves (Version 4, DICTO DOI 10.5281/zenodo.24052633; certificates in studies/2026-11-09-yantra-audit)

**Theorem 10.**
- The slope u = v of Kulaichev's yantra is a root of an explicit irreducible integer polynomial f348 of degree 348:
  - even in u, so u² has degree 174;
  - 175 terms, coefficients of up to 33 digits;
  - leading coefficient 2²⁰·5², constant term −2⁸·3⁵;
  - 34 real roots.
- Certified as follows:
  - **Irreducibility:** degree patterns mod 7, 11, 13 and 19.
  - **Existence of the exact configuration:** a Krawczyk / interval-Newton box at 520 digits, with every dropped factor certified nonzero on the box and the root selected by exact Sturm counts. This is a rigorous existence proof, which Kulaichev and Pustynski did not have.
  - **Second derivation:** an elimination in other variables gives a degree-1744 resultant with factors 1^178, 1^274, 1^178, 2^185, **348**, 396.

**Proposition 11 (certified).**
- Kulaichev's yantra has 45 odd regions (41 of them triangles) and 28 sandhis, not the traditional 43 and 24.
- This proves Pustynski's remark about the "two additional tiny triangles", which have area about 10⁻⁷.

**Theorem 9 (the DICTO Yantra).** With uv = 2/φ³ in place of (a), the yantra meets (b), (c), (d) and the traditional 43 regions and 24 sandhis. Its slope has degree 160.

**What is not proved yet:**
- **Uniqueness.** It is open in #103 too.
- **The field of definition of Q, S, b1.** Whether these lie in ℚ(u²) is open (audit, "What remains"). No theorem claims it.

**Priority.** Searches by us and by the blind reviewer found no exact form and no proof of uniqueness after 2021. The sources are in §5.

### 1.3 Blind Palomar pre-score (method as in 2026-11-15-palomar-permutohedron)

- **Setup.** One fresh agent was given only:
  - PalomarPolicy @ 28bd48b9 (README, CONTRIBUTING §1 and §7, prompt 04, rubric.json);
  - a bare statement file, `blind/inputs/Y-sri-yantra.md`, holding the problem, its three published sources and four statements.
- **Search.** It searched the web on its own.
- **Output.** `blind/blind-Y-sri-yantra.json`.

| | Statement | Notability / literature | Outcome |
|---|---|---|---|
| Y1 | Theorem 10 with certified existence and the 45-region count (as published) | **4 / 4** | neutral |
| Y2 | Y1 plus uniqueness (target; scored as if proved) | **4 / 4** | neutral |
| Y3 | Theorem 9, the DICTO Yantra (uv = 2/φ³; 43 regions) | 2 / 3 | failure |
| Y4 | Theorems 1–2 (quadratic field; whole-number-fraction yantra) | 2 / 2 | failure |

**Reasons given:**
- **Y1.** It turns Kulaichev's 12544 bound into the exact 348, gives the first certified existence proof, and proves Pustynski's tiny triangles. The reviewer judged it a serious note with a named audience: history of Indian mathematics and computational algebraic geometry.
- **Y2.** It settles the uniqueness question that Chiodo calls still open. The reviewer warns that the admissibility conditions must be exactly Kulaichev's, so that uniqueness is not won by narrowing the set.
- **Y3.** The golden condition "reads as chosen to get the count". No source asks for it.
- **Y4.** It follows closely from Chiodo's straightedge-and-compass theorem. Our blind file cited Chiodo only for uniqueness and left out that theorem; #103 §14 does cite it. Any Palomar package must state Chiodo's theorem as the predecessor.

**Own reading.**
- I agree on all four.
- Y1 and Y2 are both at the floor, and production scores carry about one point of run-to-run noise (landscape study §3). So Y2, which answers the question Chiodo names as open, is the safer package. Y1 alone is a fair submission if uniqueness resists.
- The DICTO Yantra (Y3) is the artistic heart of #103, but it is not what Palomar rewards.

### 1.4 What closing uniqueness requires

1. **Admissible domain.** Fix it exactly as Kulaichev and Pustynski use it: the nine triangles non-degenerate, each apex on the correct side, corners in the closed disc, and the tangency and inscription conditions (b)–(d) with their sign branches.
2. **Projection.** Show that every admissible solution projects to a real root of the full eliminant Res (degree 1744, factors already listed).
   - This needs the elimination to be **complete**: no solution may be lost where a leading coefficient or a cleared denominator vanishes.
   - The degenerate loci (u = 0, v = 0, tu = ±1, t = ±v and the dropped factors) must be handled separately. Each is a lower-dimensional system and can be checked exactly.
3. **Root test.** For every real root of every factor, isolated exactly:
   - rebuild the configuration;
   - test admissibility in interval arithmetic;
   - expect exactly one survivor, the root of f348 near 0.750438516.
4. **Rival elimination.** As a check, redo the count with a second elimination order, as in the audit's stage4.

This is a certified computation of the kind the audit already ran (about 6 minutes for the full certificate rerun). It is token-free compute-host work. It should start with a pilot of 5 minutes or less, with a heartbeat and a FINAL line.

### 1.5 Lean feasibility

- **Challenge (the statement).** About 150–250 lines:
  - nine triangles given by depths and half-widths;
  - incidences and concurrences as polynomial equations over ℝ;
  - admissibility as inequalities;
  - the conclusion ∃! configuration, or ∃ configuration with `Polynomial.aeval u f348 = 0`.
  - f348 would be written out (175 terms; about 60–90 lines). This is well inside the 1,000-line cap.
- **Proof, Y1 (existence).** Hard but feasible.
  - The cleanest route needs Q, S, b1 written as explicit polynomials in u modulo f348, which is the audit's open point. Then every condition is a polynomial identity mod f348 (checkable by `ring_nf` / `decide` on ℚ[X] remainders, heavy at degree about 700 with 33-digit coefficients). The root comes from the intermediate value theorem on f348 at rational endpoints (`norm_num` evaluation), and the admissibility inequalities need rational bounds.
  - Without that route, a Krawczyk proof inside Lean is research-grade.
  - Mathlib's `polyrith` needs network access and does not scale to this. Use explicit cofactor certificates instead.
- **Proof, Y2 (uniqueness).** Very large: Gröbner or resultant cofactor certificates, plus real-root counting. Mathlib has no Sturm sequences.
- **Palomar note.** Palomar registers the Lean-checked Challenge. A Y2 Challenge whose proof cannot be completed is no use. The realistic Palomar package is therefore Y1, at about 4. Y2 should go as a paper (#103 v5) with certificates, and to Palomar only if the Lean uniqueness proof turns out tractable.
- **First Lean step:** settle whether Q, S, b1 ∈ ℚ(u²). It is one exact computation: reduce the rebuilt coordinates modulo f348 over ℚ.

---

## 2. The ranked list (all candidates found)

Chance is the chance that DICTO's existing results and tools close the problem. Fit is the Palomar fit: a problem stated by someone else, a named audience, and Challenge size.

| # | Problem, exact source | Status (checked 15 Nov 2026) | DICTO's handle | Needs | Difficulty | Lean | Palomar fit |
|---|---|---|---|---|---|---|---|
| 1 | Kulaichev's Śrī Yantra: uniqueness, exact form (§1) | Uniqueness open (Chiodo 2021). Exact form: #103 | #103 Thms 10, 11; audit | Certified root census | Computation (certified) | Y1 feasible with work; Y2 very large | **4 (blind)** |
| 2 | Rational tetrahedra that tile: 40 sporadic cases. Chentouf–Sun, arXiv:2312.01654 v1, Thm 1.2 (list A, p. 2); KKPR, arXiv:2011.14232; Senechal, *Math. Mag.* 54 (1981) 227–243 | Open for the 40, as far as found (Wolfram MathWorld "Rational Tetrahedron"; no later paper found). Some of A may be classical tilers (Sommerville, Goldberg); match them before any work | #102 exact-cover checker and Dehn tools; #92 search proofs | Per case: periodic tiling (exact cover) or a certified obstruction | Computation, then proof | A periodic tiling is checkable but irrational coordinates (π/5 angles) make it large; obstructions very large | High: a stated finite list, Kedlaya–Poonen audience |
| 3 | Grünbaum: rhombic monohedral parallelohedron with every zone of k faces, k ≥ 10 (Bilinski paper v2/3/10, p. 17; library copy) | Open in Grünbaum's text; his supplement adds nothing; no later answer found | Golden-rhombus solids; #1, #2 | One construction plus a translation-tiling proof | Construction search plus exact check | Large (nonconvex tiling) | High (Grünbaum's named problem) |
| 4 | Goldberg 1974 (JCTA 17, p. 378): are all space-filling pentahedra known? Closable part: quadrilateral pyramids | Open (MathWorld "Space-Filling Pentahedron": lists not claimed complete) | #44, #77, #92, #102 | Exact classification of a sub-family | Proof plus computation | Large | Medium (a part of a stated question) |
| 5 | Tsiokos §10 Q8 (other lattices) and Q5 (fewest faces); arXiv:2609.19214 pp. 46–47 | Open (posed September 2026; Flicker and Goodman-Strauss notes do not answer them) | RD bridge; repro-tsiokos; aim 3 | A single marked RD forcing the hierarchy | Research | Very large (Tsiokos's own Lean was huge) | Very high if achieved |
| 6 | Grünbaum's patch conjecture: sphere-like translation tilers have Fedorov patch structure (Bilinski paper pp. 21–22; Wikipedia "Parallelohedron": "remains unproven") | Open | HexOct, Narcissus (if any is a translation tiler) | A counterexample (one tiler) or a proof for a class | Search, then proof | Large | High if a counterexample is found; chance low |
| 7 | Tsiokos §10 Q3: a convex strongly aperiodic monotile in ℝ³ (also the Schmitt–Conway–Danzer line) | Open | Convex pieces throughout | — | Famous-hard | — | Very high; chance very low |
| 8 | Erdős #634: all n such that some triangle cuts into n congruent triangles (Soifer 2009; Beeson) | Open (erdosproblems.com/634) | #54 gnomon, Rule of Halves (weak) | Remaining n | Proof | Medium per case | High (Erdős list); fit low |
| 9 | Erdős #769: c(n) for cubes into homothetic cubes, c(3) | Open | Weak | — | — | — | Fit low |
| 10 | Rupert property for the remaining Archimedean and Catalan solids (Formal Conjectures `Paper/Rupert.lean`, which cites Jerrard–Wetzel–Yuan 2017 and arXiv:2112.13754, 2210.00601; the general case was disproved by Steininger–Yurkevich, arXiv:2508.18475) | Some cases open | Exact polyhedra only | Search plus certificate | Computation | Medium | High; fit to DICTO's themes low |
| — | Hegedüs–Károlyi permutohedron covering (Acta Math. Hungar. 174, 2024; Conjecture 6) | **Closed**: Pawlowski; Kong–Zeng arXiv:2509.13877 (Palomar 2026-09-14-000004). The almost-cover bound C(n,2) is sharp (Hegedüs–Károlyi) | #105 N(n) | No open question found that N(n) answers | — | — | Route 1 of the permutohedron study stays the only way (resonance arrangement) |
| — | 3D einstein (strongly aperiodic monotile) | **Closed**: Tsiokos 2026 (Chair44); CLARK in 5D (Palomar 2026-10-07-000006) | — | — | — | — | Only the follow-ups (rows 5, 7) remain |

**Not ranked (no fit found):**
- Grünbaum's configuration cases (n₄): settled up to the Palomar (23₄) entry. The (n₅) gaps lie outside DICTO's tools.
- Erdős geometry problems on distances, lines and circles (59 open, by tag); see §5.
- The Formal Conjectures geometry files: Borsuk, Hadwiger–Nelson, Kakeya, moving sofa, square packing, inscribed square, happy ending, no-three-in-line.
- OEIS: the searches found no sequence carrying a stated conjecture or missing terms that DICTO's work bears on. A071880 (parallelohedra in dimension ≥ 6) is far from his tools. A114438 (Barlow packings by period) is known in closed form.

## 3. Recommended order

1. **Kulaichev uniqueness.** Run the certified root census (§1.4), then #103 v5 with a "Theorem 10′: unique". In parallel, the one-shot ℚ(u²) check (§1.5), which decides whether a Lean Challenge for Y1 is practical. Ask DICTO before any Palomar step, and before writing to Chiodo or Pustynski (the audit already lists that as wanted).
2. **Sporadic tetrahedra.**
   - First, a desk match of list A against the known tilers (Sommerville 1923, Goldberg 1974, Baumgartner), so that only open cases go forward.
   - Then run #102's exact-cover tiler on the open cases with fifths angles. Each case it settles is a stated open case.
3. **Grünbaum k = 10.** A finite search over nonconvex polyhedra of golden rhombi in which every zone has 10 faces, with a translation-tiling test.

## 4. Concordance and library

- **Concordance "outside".** Goldberg's tetrahedral families (JCTA 16, 1974) are already paired with #92's face-to-face law ("test"). Sydler (scissors congruence) is paired with #50. Both support row 2.
- **Concordance "gaps".** These are DICTO's own open points. None is stated by others, so none qualifies here.
- **Library: searched.** The reference library (private repository, on the compute host) was searched:
  - all six MANIFEST.json files, for problem-list and source keywords;
  - the full text of Grünbaum 2010 (Bilinski; source of rows 3 and 6);
  - Goldberg 1972, 1974 and 1982 (source of row 4);
  - Tsiokos 2026, Goodman-Strauss 2026 and Flicker 2026 (row 5);
  - Senechal 2004 (scan, no text layer: not searchable).
- **Not in the library:** Croft–Falconer–Guy and Grünbaum's *Configurations*.

## 5. Sources checked

**Read in full or at the passages cited:**
- Pustynski 2014: insa.nic.in/writereaddata/UpLoadedFiles/IJHS/Vol49_3_5_Pustynski.pdf
- Chiodo 2021: comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.163.pdf
- #103 v4 (paper.html) and the study READMEs 2026-11-08-sri-yantra, 2026-11-09-yantra-audit, 2026-11-12-repro-tsiokos and 2026-11-12-rd-bridge
- Chentouf–Sun, arxiv.org/pdf/2312.01654 (v1)
- Kong–Zeng, arxiv.org/pdf/2509.13877 (v3)
- Grünbaum 2010 and Goldberg 1974 (library copies)
- Grünbaum's "Supplement to Bilinski": faculty.washington.edu/moishe/branko/Bilinski paper files/Supplement to Bilinski (first 100,000 characters)
- Tsiokos §10, Goodman-Strauss and Flicker (library copies)
- Formal Conjectures (github.com/google-deepmind/formal-conjectures, main, full tree of 2,428 paths): `Paper/Rupert.lean` read; geometry file names scanned
- erdosproblems.com: `data/problems.yaml` from github.com/teorth/erdosproblems (1,221 problems; 108 geometry, 59 still open). Pages fetched: 101, 102, 104, 107, 352, 506, 507, 528, 588, 589, 634, 669, 769, 827, 831, 838, 1070 and 1088
- Wikipedia "Parallelohedron" (API extract)

**Abstract or summary only:**
- Hegedüs–Károlyi, Acta Math. Hungar. 174 (2024) 453–461, via arXiv:2305.06202 and the Springer page
- KKPR, arXiv:2011.14232
- Wolfram MathWorld: "Space-Filling Tetrahedron", "Rational Tetrahedron", "Space-Filling Pentahedron"
- Quanta, 9 February 2021 (tetrahedra)

**OEIS JSON searches:** "space-filling polyhedra", "stereohedra", "tetrahedra tile space", "rhombic dodecahedron conjecture", "permutohedron conjecture", "polycubes tile space", "close-packed stacking".

**Web searches:**
- Sri Yantra exact or uniqueness (two queries)
- preprints.org 202509.1564
- "rhombic monohedral" parallelohedron zones
- Senechal–Taylor 2023 zonohedra
- "which tetrahedra fill space" status
- Chentouf–Sun
- Hegedüs–Károlyi almost cover
- the space-filling pentahedra classification

**Blind agent's own URLs:** listed in `blind/blind-Y-sri-yantra.json`.

**Not available or not read:**
- Croft–Falconer–Guy, *Unsolved Problems in Geometry*: no free copy; not purchased. Its problem numbers are not cited here.
- Grünbaum, *Configurations of Points and Lines* (2009): not held. Its status is taken from the Palomar landscape study (Cuntz).
- Schattschneider's open-problem lists, Senechal's *Quasicrystals and Geometry* problem list, Hirschhorn–Hunt (2D pentagons, outside the 3D scope) and Conway–Sloane on polytypes: no free text found in this session, so no claim is made from them.
- Kulaichev 1984: a scan with no text layer; pages 284–285 as cited by Chiodo.
- preprints.org 202509.1564: HTTP 403; its topic is unknown.
- Huet 2002: not reachable, as before.

## Files

- `blind/inputs/Y-sri-yantra.md`: the bare statements given to the blind reviewer.
- `blind/blind-Y-sri-yantra.json`: the blind reviewer's prompt-04 output for Y1–Y4.
