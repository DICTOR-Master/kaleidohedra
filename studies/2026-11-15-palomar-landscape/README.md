# What Palomar has accepted so far, and why (15 November 2026)

**Verdict.** Palomar has registered **1,124 results (869 projects; 1,279 versions)** since 8 August 2026. That is far more than our earlier notes said: they found one entry, because the old public database repository stopped updating on 1 August. The data now comes from the registry's public API.

- **Novelty is not the bar.** 88% of entries (990) formalise results that are already in the literature. They include classical theorems such as Kotzig 1955, Sauer–Spencer 1978 and Edmonds' matching polytope. One registered entry formalises a permutohedron theorem that its own authors say was already known.
- **What the bar is.** The result must be the kind of thing a research paper is written about, and it must have an audience that already exists.
- **Original results that passed (134 of them).** Almost all answer a question that **someone else had already put in print**. They close a stated open case or conjecture, beat a published record, or settle a count that the literature had left open. Examples:
  - the one open case of geometric (n₄) configurations, n = 23 (35-line Challenge, single author);
  - "at least 10" minimum universal sets of MacMahon cubes, proved to be exactly 10;
  - Kurz's 2008 polyhex conjecture;
  - Tabachnikov's Problem 2.
- **Why DICTO's results stalled at 2–3.** They answer questions that DICTO posed himself, so the reviewer finds no existing audience.
- **What should clear 4.** A geometric result that settles a problem stated by someone else, with the problem's source cited, packaged as a short Mathlib-only Challenge.

**Status:** desk study from public sources only. No account, repository, issue, pull request or contact was made.

**Scores are not public.** The registry publishes no notability scores and no reviewer reasons. Each record holds only the review's SHA-256 digest and its public `warnings`. Every registered entry has outcome `neutral`, which implies notability of at least 4 at review. Rejected submissions are never published.

## 1. The registry in numbers (all 1,124 records, read 15 Nov 2026)

These figures come from every full record at `data.palomar-registry.org/entries/…`, downloaded and tallied here. The per-entry table is in `registry-entries-2026-11-15.tsv`.

| Measure | Value |
|---|---|
| Registered results / projects / versions | 1,124 / 869 / 1,279 |
| Registered by month | Aug 140 · Sep 243 · Oct 497 · Nov (to 15th) 244 |
| Review outcome | `neutral` for all 1,124 (rejections are not published) |
| Reviewer model | `codex:gpt-6-sol` 817 · `codex:gpt-5.6-sol` 307 (earlier) |
| Entries with public review warnings | 101 (108 warnings) |
| `result_origin` | source-based 990 (88%) · **original 134 (12%)** |
| Main source relationship (all sources) | formalizes 1,212 · adapts 473 · independently-proves 114 · background 2,235 · other 406 |
| Challenge size (lines) | median 156; quartiles 79 / 156 / 304; min 8; max 1,000 (the cap). Original results: median 145 |
| Trust level | high 1,123 · qualified 1 |
| Authors per entry | 1: 895 (80%) · 2: 81 · 3: 124 · 4+: 24 |
| Distinct submitting repository owners | 282 (heavily concentrated: the top three author names appear on about 330 entries) |
| Entries where an author is also an author of the main source | 403 (people formalising their own papers) |
| Primary arXiv class | math.CO 303 · math.NT 212 · math.PR 70 · math.LO 57 · math.GN 43 · math.DS 41 · math.CA 37 · **math.MG 25** · math.GR 24 … |
| Geometry (math.MG anywhere or MSC 52) | 81 entries; polytope/tiling/polyhedron keyword: 13 |
| Keyword tags (title + abstract; rough) | "conjecture" 192 · Erdős 108 · counterexample/"is false" 83 · improved bound/record ≈189 · OEIS 18 · "open problem" 9 · competition/olympiad/IMO/Putnam **0** |

**Annual workload** (Palomar's public cost page, window 10 Oct – 9 Nov 2026): about 13,030 submissions, 10,828 completed reviews and 7,276 registrations a year. So roughly one completed review in three does not end in registration. That third mixes rejection, revision requested, withdrawal and reviews not yet registered; the split is not published.

**AI use** (`automation.methods` in each repository's `formalization.yaml`; random sample of 150 plus 7 named entries, 157 files read):
- 133 of 157 (85%) declare an AI agent; 27 list `manual`, often alongside an agent; 8 say `autonomous`; 21 give no method.
- Model mentions: Claude 71, GPT/Codex 60, Aristotle 8, others 1–6 each.
- `review.status`: self-assessed 63, agent-reviewed 54, author-verified 8, unchecked 4.
- The review **warns** when AI review roles are unclear: 6 of the 108 warnings are about this. It does not penalise AI use itself.

**Independents versus academics.** Records carry only a name, plus an optional ORCID (53 authors) or GitHub handle (35); there is **no affiliation field**. So the number of accepted entries from independent researchers **cannot be read from the registry**. What can be said:
- At least the 134 `original` entries are mostly single-author (114), and many name only the submitter's own repository or manuscript as the source.
- The rows in §2 show independents with no institution listed alongside university groups.

## 2. Representative entries, with outside profile

The full list of 1,124 is in the TSV. This table picks entries for spread: famous, classical, original by single authors, and geometry close to DICTO's work.

How to read the columns:
- "Notability / reasons": **not public** for every row. Registration implies ≥ 4.
- Citations: OpenAlex, 15 Nov 2026, for the formalised or background paper. "n/r" means not retrieved: the OpenAlex rate limit was hit and no figure is claimed.
- Coverage and prizes were **not searched** row by row. "None checked" means no claim either way.
- Standing: only what a public source states; otherwise "not stated".

| Entry | Title (short) | Area | Submitter(s), as listed | Origin · Challenge lines | Underlying work: where | Citations | Open-problem status | Submitter standing (public) |
|---|---|---|---|---|---|---|---|---|
| [PALOMAR-2026-08-08-000001](https://palomar-registry.org/entry?id=PALOMAR-2026-08-08-000001&version=1) | Uniform-constant Erdős unit-distance conjecture is false | math.MG / 52C10 | Kim Morrison | source-based · 43 | Alpöge, "Integral points on norm-one tori…" (cited via an X post and a PDF; no journal) | n/r | **Famous conjecture** (Erdős unit distance, uniform-constant form) | Not stated in the record (the repository is `kim-em`) |
| [PALOMAR-2026-09-08-000004](https://palomar-registry.org/entry?id=PALOMAR-2026-09-08-000004&version=1) | A real affine (23₄) configuration | math.CO, math.MG | Will Strinz | **original** · **35** | Own repository only; agent (Codex) disclosed | Cuntz (Art Discrete Appl. Math.): n/r; Berman–Gévay–Pisanski: 1 | **Stated open case**: Cuntz's abstract says "only the case n = 23 remains open" ([AMC](https://amc-journal.eu/index.php/amc/article/view/1402)) | Not stated; no public profile found by one search |
| [PALOMAR-2026-11-01-000019](https://palomar-registry.org/entry?id=PALOMAR-2026-11-01-000019&version=1) | The ten minimum universal sets of MacMahon cubes | math.CO | Jason Davies | **original** · 105 | Own repository | Johnson–Roldán arXiv:2407.13208: 0 | **Stated count left open**: Johnson–Roldán found "at least 10" minimum universal sets; Haraguchi proved the minimum is 12 ([arXiv](https://arxiv.org/abs/2407.13208)) | Not stated |
| [PALOMAR-2026-10-27-000022](https://palomar-registry.org/entry?id=PALOMAR-2026-10-27-000022&version=1) | Kurz's conjecture on the convex hull of a polyhex | math.MG | Pragyaan Gaur | source-based (own arXiv:2609.30310) · 89 | arXiv only | 0 | **Stated conjecture** (Kurz 2008, Conjecture 2) | Not stated |
| [PALOMAR-2026-10-17-000001](https://palomar-registry.org/entry?id=PALOMAR-2026-10-17-000001&version=1) | A converse to the discrete four-vertex theorem | math.MG, math.DG | Kristoffer Josefsson | **original** · 517 | Own paper in the repository | Tabachnikov 2008 (J. Fixed Point Th. Appl.): 0 | **Stated problem**: Tabachnikov's Problem 2 | Not stated |
| [PALOMAR-2026-08-24-000004](https://palomar-registry.org/entry?id=PALOMAR-2026-08-24-000004&version=1) | Three sharp bounds for Hansen polytopes of cographs | math.MG, math.CO | Jeremy P Parker | **original** · 243 | Own proofs; context Freij–Henze–Schmitt–Ziegler (Electron. J. Combin. 2013) | FHSZ: 10 | Extends a studied family (Mahler volume, 3^d face count) with **equality classification** | Not stated |
| [PALOMAR-2026-09-14-000004](https://palomar-registry.org/entry?id=PALOMAR-2026-09-14-000004&version=1) | To cover a permutohedron | math.MG, math.CO | Bochao Kong | source-based · 261 | Kong–Zeng arXiv:2509.13877. arXiv v3 says the main result follows from Pawlowski's earlier work and that the authors will not seek journal publication ([arXiv](https://arxiv.org/abs/2509.13877)) | 1 | Covering question from Hegedüs–Károlyi (Acta Math. Hungar. 2024) | Michigan State University (per arXiv paper) |
| [PALOMAR-2026-10-07-000006](https://palomar-registry.org/entry?id=PALOMAR-2026-10-07-000006&version=1) | The CLARK tile: an aperiodic monotile in five dimensions | math.MG | Conor Grogan | source-based (own manuscripts) · 291 | Unpublished manuscripts; background Smith–Myers–Kaplan–Goodman-Strauss | n/r | Einstein problem in higher dimension | Not stated |
| [PALOMAR-2026-10-02-000008](https://palomar-registry.org/entry?id=PALOMAR-2026-10-02-000008&version=1) | Optimality, uniqueness, stability of Gerver's sofa | math.MG | The-Anh Vu-Le | source-based · 770 | Baek arXiv:2411.19826 | 12 | **Famous problem** (moving sofa) | Not stated |
| [PALOMAR-2026-11-09-000008](https://palomar-registry.org/entry?id=PALOMAR-2026-11-09-000008&version=1) | The Reinhardt conjecture, formalized | math.MG, math.OC | The-Anh Vu-Le | **original** · 173 | No external source for the proof | (Hales 2011 background: n/r) | **Famous conjecture** (Reinhardt 1934). The record claims a proof. **Not verified by us**, and no outside reception was checked | Not stated |
| [PALOMAR-2026-11-04-000007](https://palomar-registry.org/entry?id=PALOMAR-2026-11-04-000007&version=1) | A Schur 6-colouring of [1, 538] | math.CO | Adam McKenna | **original** · **29** | Own Zenodo preprint | Chen–Zhu–Long arXiv:2610.31362 (S(6) ≥ 537): 1 | **Beats a published record** by one | Not stated |
| [PALOMAR-2026-11-13-000005](https://palomar-registry.org/entry?id=PALOMAR-2026-11-13-000005&version=1) | Exact Gallai–van der Waerden numbers GW(r;3,4) = 53 | math.CO | Arhan Canli | **original** · 94 | SAT + LRAT certificate; own | Mao–Ozeki–Robertson–Wang (JCTA 2023): n/r | **Values asked for** in the defining paper | Not stated |
| [PALOMAR-2026-09-25-000017](https://palomar-registry.org/entry?id=PALOMAR-2026-09-25-000017&version=1) | Pascal minus-one GCD | math.NT | John Fairfax-Ball | **original** · 67 | Own; context McTague (Amer. Math. Monthly 2017) | n/r | Completes a valuation classification in a studied family | Not stated |
| [PALOMAR-2026-10-30-000006](https://palomar-registry.org/entry?id=PALOMAR-2026-10-30-000006&version=1) | Proof of WOWII Conjecture 96 (Graffiti.pc) | math.CO | Rhett (@v3ai) | **original** · 53 | Own repository | — | **Stated conjecture** (computer-generated, DeLaVina's list; in the Formal Conjectures repo) | Not stated |
| [PALOMAR-2026-10-19-000008](https://palomar-registry.org/entry?id=PALOMAR-2026-10-19-000008&version=1) | Erdős Problem 173: monochromatic triangles in 2-colourings of the plane | math.CO, math.MG | Jacob Parish | **original** · 121 | Own blueprint (repository `plasma-ai/erdos-173`) | Erdős–Graham et al. 1973: n/r | **Listed Erdős problem** ([erdosproblems.com/173](https://www.erdosproblems.com/173)) | Not stated |
| [PALOMAR-2026-10-04-000008](https://palomar-registry.org/entry?id=PALOMAR-2026-10-04-000008&version=1) | Erdős 956: unit distances between disjoint convex translates | math.MG | Linmiao Xu | source-based · 102 | Adapts Chojecki (web PDF) and Valtr 2005 | n/r | Listed Erdős problem | Not stated |
| [PALOMAR-2026-11-01-000023](https://palomar-registry.org/entry?id=PALOMAR-2026-11-01-000023&version=1) | Kotzig's theorem on light edges of planar graphs | math.CO | Juan Pablo Traverso Gianini | source-based · 139 | Kotzig 1955 (Mat.-Fyz. Časopis); Borodin 1989 (Crelle) | n/r | **Classical theorem** (no open problem) | Not stated (109 entries under the same name) |
| [PALOMAR-2026-11-14-000010](https://palomar-registry.org/entry?id=PALOMAR-2026-11-14-000010&version=1) | The Sauer–Spencer packing theorem | math.CO | Wentao Li | source-based · 56 | JCTB 1978 | n/r | **Classical theorem** | Not stated |
| [PALOMAR-2026-11-14-000014](https://palomar-registry.org/entry?id=PALOMAR-2026-11-14-000014&version=1) | Sun's determinants for m = 1, 2, 3 | math.CO, math.NT | Wentao Li | source-based · 55 | Fried arXiv:2606.09913; Wang–Sun arXiv:2206.12317 | 1; 2 | OEIS conjectures of Z.-W. Sun, proved by Fried | Not stated |
| [PALOMAR-2026-11-02-000017](https://palomar-registry.org/entry?id=PALOMAR-2026-11-02-000017&version=1) | Exact directed L/X diameter of the symmetric group | math.CO, math.GR | S. Uskov, A. Chervov, F. Levkovich-Maslyuk, I. Litvak, A. Smolensky, A. Soibelman | **original** · 68 | Own; context CayleyPy arXiv:2509.19162 | CayleyPy: 8 | Glushkov's problem (1973); conjectures from the CayleyPy list | Not stated (team of six) |
| [PALOMAR-2026-10-07-000007](https://palomar-registry.org/entry?id=PALOMAR-2026-10-07-000007&version=1) | Matrix multiplication exponent ω < 2.3710449 | cs.CC | Oliver Proudfoot, Andrew Perrault | **original** · 137 | Own; previous record Dupont et al. arXiv:2608.16884 | Dupont et al.: 23 | **Beats a published record** on a famous constant | Not stated |
| [PALOMAR-2026-10-22-000013](https://palomar-registry.org/entry?id=PALOMAR-2026-10-22-000013&version=1) | Fixed-force anomalous dissipation | math.AP | Tao Tao, Baishu Zeng, Haiqi Zhang | **original** · 189 | Own simplified proof; context Bruè–De Lellis (Comm. Math. Phys. 2023) | Bruè–De Lellis: 40 | Active research line | Not stated |

**What these rows show.**
1. Every `original` row is framed against a problem, conjecture, record or classification that others set: Cuntz, Johnson–Roldán, Kurz, Tabachnikov, Erdős, Graffiti, Schur records, Glushkov.
2. The audience is supplied by the problem's own literature, even when citations are low (0–1 for several). Low citation counts and arXiv-only status did not block registration.
3. Size is no obstacle. The configuration and Schur entries have Challenges of 35 and 29 lines.

**Public review warnings** (all 108 read) concern metadata only:
- novelty or priority claimed without a documented search, about 10, e.g. *"Qualify novelty as unknown or document the literature search supporting the claim"* (PALOMAR-2026-09-21-000006);
- unclear AI review roles;
- missing `related_formalizations`;
- wrong toolchain versions in READMEs;
- abstracts that overstate the Lean statement.

None discusses notability, because notability findings would have blocked registration.

## 3. What the rubric rewards in practice

Binding text (PalomarPolicy @ 28bd48b):
- CONTRIBUTING §1: the result "could plausibly warrant a research paper or a serious research note", and the reviewer "can identify a credible research area and a plausible kind of mathematician in a research department".
- "Formal correctness, the difficulty or size of the Lean development, polished prose, and novelty do not by themselves establish research interest."
- Prompt 04: "Novelty is not required." Also: "Do not … penalize an original result merely for lacking a prior mathematical source."
- Anchor 4: "plausibly paper-worthy, with a specifically identified credible research audience". Anchor 3: "paper-worthiness or a credible research audience has not been affirmatively established".

In practice, read from the registered set:

1. **Known theorems pass freely when they were paper-worthy in their day.** Examples: Kotzig, Sauer–Spencer, Kelly's reconstruction cases (PALOMAR-2026-11-14-000007), Edmonds' polytope, Gibbard–Satterthwaite. The test is whether the result was paper-worthy, not whether it is new.
2. **Original results pass when the question has an owner in the literature:**
   - a stated open case (23₄);
   - a stated conjecture (Kurz, Graffiti 96, Sun);
   - an Erdős problem (108 entries);
   - a record (Schur, ω, tensor ranks);
   - a count or classification the literature left open (MacMahon "at least 10" became exactly 10; equality cases for Hansen polytopes).
3. **"Affirmatively established" is the hinge.** Our three blind replays all failed there: Loop Equality 3, Kyushindo Theorem 4 at 2, permutohedron statements ≤ 3. The reviewer had to invent the audience. In every accepted original above, the audience is the people who stated the problem.
4. **Competition problems:** none found by keyword. **Formalisations of the submitter's own paper:** common (403).

A caution: production scores have about one point of run-to-run noise (policy text). In Palomar's own August audit, model tiers disagreed on outcome in 2–3 of 5 cases. Our replays are estimates made with a different model.

## 4. What this means for DICTO

**Why our candidates score 2–3.** Each answers a question DICTO posed (Loop Equality across stackings, foot-point hulls, Vacuus slices). Each is also a short consequence of a classical tool (Thorpe, orbit-space diameter, Rado/McMullen/Stanley). Nobody outside DICTO's papers has asked these questions, so no audience is "affirmatively established". The accepted set shows this, not the topic, is the obstacle: geometry passes (81 entries), polytopes pass, and small Challenges pass.

**Result types likely to clear 4, in order of fit with DICTO's work:**

1. **Close a stated open case in configurations, tilings or polyhedra.** The (23₄) entry is the model: one explicit construction, exact rational coordinates, 35 lines, an independent author, a one-line citation of the paper that called the case open. Places where such cases are stated:
   - Grünbaum, *Configurations of Points and Lines* (open existence and realisability cases);
   - Croft–Falconer–Guy, *Unsolved Problems in Geometry* (tiling, packing and polyhedra sections);
   - erdosproblems.com, geometry tag;
   - the Formal Conjectures repository (google-deepmind), which the accepted entries cite;
   - OEIS entries carrying "Conjecture" lines on polyhedra or polyforms.

   **First step (ready):** list stated open cases on space-filling polyhedra, stereohedra and polyform hulls from these sources. Check each against DICTO's existing constructions before any new work.
2. **Settle a count that someone else left as a bound.** Like "at least 10" to "exactly 10" for MacMahon cubes, or exact GW numbers. If DICTO's enumerations (space-fillers, Hamiltonian cycles, slices) match a quantity someone published only as a bound, the exact value with a classification is a 4-type result. Book Ch. 15's 44/5396 counts are already in OEIS and Polster–Ross, so those are known, not open.
3. **Attach the Vacuus count to the permutohedron covering line.** "To cover a permutohedron" (Kong–Zeng; Hegedüs–Károlyi; Pawlowski) was registered *although its main result was already known*. That literature asks how many hyperplanes cover the vertices. #105's N(n) counts the central hyperplanes spanned by the ridges, which is a neighbouring question.
   - A theorem answering a covering-type question for faces or ridges, posed in those papers, would inherit their audience.
   - So would one that relates V_n to the resonance arrangement, as the permutohedron study's route 1 proposed.
   - This is the best upgrade route for A1.
4. **A record or sharp constant on a named problem.** For example, a Reinhardt- or Kurz-type extremal value for a polyhedral packing or covering question stated by others. The Kyushindo route 1 table, t(G) for every finite group, becomes 4-type only if a published question asks for it. Search for one first.
5. **Aim 3 (one piece, any stacking).** A 3D monotile that forces non-periodicity, with a Lean-checked core, sits next to the registered 5D CLARK tile and the Einstein-problem literature. It would clear 4 easily if achieved. It is research, not packaging.

**What will not help:** more Lean polish, bundling more corollaries, or better prose (prompt 04). The Loop Equality and Kyushindo packages should stay local unless one of routes 1–4 is added.

## 5. Sources checked

Registry data (public API, CC0):
- https://data.palomar-registry.org/api/v1/results?order=registered: all 45 pages, 1,124 rows.
- https://data.palomar-registry.org/entries/PALOMAR-…-vN.json: all 1,124 full records.
- https://data.palomar-registry.org/browse/index.json

Registry site and its llms.txt files:
- https://palomar-registry.org/costs (refreshed 9 Nov 2026)
- PalomarWeb `llms.txt`
- https://submit.palomar-registry.org/llms.txt

GitHub, organisation PalomarRegistry:
- repository list;
- PalomarPolicy @ 28bd48b: README, CONTRIBUTING.md, prompts/04-literature-notability.md;
- PalomarReviewer @ ba9b26c: docs/audits/2026-08-20-reviewer/REPORT.md;
- PalomarWeb @ b3a4a5e: README, llms.txt, AGENTS.md;
- PalomarDatabaseTools @ 0b44879: README;
- commit logs of PalomarServer, PalomarPolicy, PalomarReviewer, PalomarWeb, PalomarDatabaseTools;
- henriqueheine/PalomarDatabase @ 23da4f1 (commit log; last update 1 Aug 2026, superseded by a private canonical repository plus the public API).

`formalization.yaml` files: 157 files from the submitted repositories at their registered commits (raw.githubusercontent.com).

OpenAlex works API: the DOIs and arXiv IDs in the table. Several lookups were refused (HTTP 429) and are marked n/r.

Web pages:
- Cuntz, AMC article page: https://amc-journal.eu/index.php/amc/article/view/1402
- Kong–Zeng arXiv:2509.13877 (via search)
- Johnson–Roldán arXiv:2407.13208 (via search)
- launch coverage: letsdatascience.com, zeli.app story 49355968, runtimewire.com (paywalled; headline only)

Web searches:
- "Palomar registry Lean formalization accepted entries"
- "Palomar registry … Sendov notability review rejected"
- "Bochao Kong Ji Zeng To cover a permutohedron"
- "Jason Davies MacMahon cubes minimum universal sets"
- "Will Strinz configuration (23_4)" (no relevant result)

Earlier studies:
- 2026-11-14-lean-loop-equality (README, LITERATURE, SCORE)
- 2026-11-15-palomar-kyushindo (SCORE)
- 2026-11-15-palomar-permutohedron (README)

**Not verified or not available:**
- notability scores and reasons (not public);
- rejected submissions (never published);
- affiliations (not in records);
- row-by-row press coverage and prizes (not searched);
- the mathematical correctness of extraordinary claims in some records (e.g. Reinhardt, deterministic factoring in N^{o(1)}, the KLS bound): Lean-checked statements, but not checked by us against their informal accounts.

The launch-era entry PALOMAR-2026-07-29-000001 cited in our earlier notes is not in the current registry. Its content appears as PALOMAR-2026-08-08-000001.

## Files

- `registry-entries-2026-11-15.tsv`: all 1,124 registered results, one row each. Columns: id, version, date, title, authors, classes, origin, Challenge lines, main source and its relationship, endorsement, repository, reviewer model, keyword tags, permalink. The data is Palomar's CC0 metadata.
