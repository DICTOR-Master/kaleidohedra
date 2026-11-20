# New tools from recent papers, for the Concordance gaps

Study 2026-11-21-new-tools. Network reading only, nothing computed. Gaps as listed in
`papers/dicto-concordance/concordance.json` → `gaps` (grid, ranked, weak, loose with status open)
and the three aims (bridge, laws, one piece).

Rules kept: every line below comes from a page I opened (arXiv abstract page, GitHub/Reservoir page,
project page) or is marked **[unverified]** (from a search-result snippet or the library index only).
"In library" means the entry is already in the reference library's INDEX.pdf (Pi copy, read 21 Nov).
Nothing was added to the library. Candidates to add are listed at the end.

Effort: small = cite, or one script; medium = one study; large = several studies or a new framework.

---

## Top 10 (ranked by how directly each one settles or moves a named gap)

### 1. Normaliz: exact polyhedra over real algebraic number fields (with e-antic)
- **Source:** Normaliz, W. Bruns, C. Söger and others; https://github.com/Normaliz/Normaliz (opened).
  README: "Normaliz now computes rational and algebraic polyhedra, i.e., polyhedra defined over real
  algebraic extensions of QQ"; algebraic polyhedra need FLINT and e-antic. Latest stable 3.11.0,
  18 Oct 2025 **[unverified: from a Wikipedia mirror snippet]**.
- **What it does:** exact convex hulls, facets, face lattices, volumes and lattice points of polyhedra
  whose coordinates lie in a number field such as Q(√5), with no floating-point step.
- **Gaps served:** #76 "exact atlas in Q(√5)"; #91 Lemma 6 in general and the exact stations of the
  tilted slice; #62 the all-triangle 600-cell slices and #89/#91 sections of the Schläfli–Hess star
  polytopes (queued); GC column (golden cuts of every row). One exact engine for every golden
  section instead of per-study scripts.
- **Effort:** small to medium (install, port one existing study as control).
- **Our hosts:** yes, open source (GPL), builds on Linux; no network needed once built.

### 2. Rational-angle tetrahedra: the Kedlaya–Kolpakov–Poonen–Rubinstein classification and code, with the Chentouf–Sun tiling test
- **Sources:** K. S. Kedlaya, A. Kolpakov, B. Poonen, M. Rubinstein, "Space vectors forming rational
  angles", arXiv:2011.14232 (2020), code https://github.com/kedlaya/tetrahedra (opened);
  A. A. Chentouf, Y. Sun, "Tetrahedra tiling problem", arXiv:2312.01654 (2023, opened; in library #470,
  with their "Dehn invariant zero tetrahedra" arXiv:2312.01282, #469).
- **What it does:** KKPR classify every set of vectors in R³ with all pairwise angles rational multiples
  of π; for tetrahedra: two one-parameter families and 59 sporadic cases. The repository holds the C++
  enumeration (README: rigorous analysis shows it "produces no false negatives"), SageMath notebooks
  for the algebra, and Magma code for larger configurations. Chentouf–Sun decide which of these
  tetrahedra tile space: all of the Hill family, exactly one of the new family, at most 40 sporadic;
  corollary: the converse of Debrunner's theorem is false (Dehn invariant zero does not imply tiling).
- **Gaps served:** ranked gap "Dehn counts of the RD, CO, RT and ID pyramids: which pyramids can fill
  space beyond Plato" — the DEHN column rows marked —; #92/#93 TRD centre pyramids; #113 "does the
  fair 18-face die fill space (Debrunner in Lean)": Chentouf–Sun show a zero Dehn count is necessary
  only, so the fill question needs a construction, not the invariant. Any of our pyramids or
  tetrahedral pieces with rational dihedral angles can be looked up in the KKPR list directly.
- **Effort:** medium (dihedral angles of each pyramid → look-up; tiling test per Chentouf–Sun).
- **Our hosts:** yes for the C++ and SageMath parts; the Magma part needs a paid licence, so skip it
  (it covers only configurations of more than 4 lines).

### 3. The Mahler conjecture in three dimensions (shadow flow)
- **Source:** S. Chen, Y. Li, D. Xi, Z.-F. Xu, "The Mahler Conjecture in Three Dimensions",
  arXiv:2605.09334 (v1 10 May 2026, v3 15 Jun 2026; opened; in library #373). Unrefereed preprint.
- **What it does:** claims the full non-symmetric Mahler conjecture in R³ with the equality cases, by a
  "shadow flow", and a new proof of the symmetric case (Iriyeh–Shibata).
- **Gaps served:** SWP column and the waiting result "Mahler volume product on the cube–octahedron
  sweep: exact formula; 32/3 at the ends; maximum at 2μ³ − 9μ + 6 = 0": the ends of the sweep are
  then the proved symmetric minimum, so the sweep runs from a proved floor to our exact maximum; the
  laws aim (chunk 5 Mahler values of OG, Covenant, Narcissus at the Santaló point) gets a proved
  lower bound to quote beside each value.
- **Effort:** small (cite and state; the symmetric floor 32/3 should be checked against the paper's
  normalisation before quoting).
- **Our hosts:** nothing to run.

### 4. LeanCert: verified interval arithmetic in Lean 4
- **Source:** LeanCert, https://github.com/alerad/leancert, Reservoir page
  https://reservoir.lean-lang.org/@alerad/LeanCert (opened): version 0.1.0, updated 10 Nov 2026,
  Apache 2.0, Lean v4.35.0. Tactic list (`leancert`, `interval_bound`; point inequalities, bounds on
  boxes, root existence and uniqueness, finite sums, integrals, exp/log/sin/cos) **[unverified: from a
  search snippet of its docs]**.
- **What it does:** proves numerical inequalities and root isolation inside Lean, machine-checked.
- **Gaps served:** #113 (the ten other fair dice in Lean; an exact t for Lucky 7); #43 Conjecture 1
  "reduced to an inradius bound beyond k = 40 (Proposition 6)" — the bound is a real inequality, the
  kind this proves; #80/#81 exact edges of the open windows; #86 proof over whole stretches (exact at
  402 weights → an interval proof over the stretch).
- **Effort:** medium; version 0.1.0, so pin the toolchain and treat as young software.
- **Our hosts:** yes (Lean + Lake; Mathlib build is heavy, run on a compute host).

### 5. Frame-marking certificates for aperiodic monotiles (Monotile-RN)
- **Source:** D. Kamenetsky, "Towards Strongly Aperiodic Monotiles in Higher Dimensions",
  arXiv:2610.00916 (1 Oct 2026; opened; in library #375); code https://github.com/dimkadimon/Monotile-RN.
  Context: I. Tsiokos, arXiv:2609.19214 (Chair44; finite parts checked in Lean 4, no repository URL
  on the abstract page); F. Flicker, arXiv:2609.23783; C. Goodman-Strauss, arXiv:2609.24779 (all in
  library).
- **What it does:** treats each tile's orientation as part of its marking so the search for matching
  rules is finite; outputs a finite certificate that, if valid, forces a unique hierarchy (strong
  aperiodicity). Reproduces Chair44 in 3D; 4D markings tested all failed.
- **Gaps served:** aim 3 (one piece, any stacking). Keying and the RD hunt are paused until "a hopeful
  piece or new applicable mathematics"; this is the nearest thing to new applicable mathematics found:
  a finite certificate a marked RD/half-RD regrouping of the chair could be tested against. Restart
  only on DICTO's word.
- **Effort:** large.
- **Our hosts:** yes (public code) — not started; listed only.

### 6. The canonical form as a scissors-congruence valuation
- **Sources:** T. Baumbach, A. Freyer, J. Weigert, M. Winter, "The canonical form, scissors congruence
  and adjoint degrees of polytopes", arXiv:2508.04275 (Aug 2025; opened; in library #371/#490);
  C. Gaetz, "Canonical forms of polytopes from adjoints", arXiv:2504.07272 (Apr 2025; opened; not in
  library).
- **What it does:** Baumbach et al. treat the canonical form as a valuation, define the adjoint
  "degree drop", a reduced canonical form that is a translation-invariant 1-homogeneous valuation
  vanishing exactly when the drop is positive, and characterise zonotopes as maximal drop d − 1.
  Gaetz: the numerator of a cone's canonical form is the adjoint (Warren) of the dual cone.
  A search snippet of 2508.04275 says the 24-cell is translation scissors congruent to the cube but not
  a zonotope **[unverified: not on the abstract page]**.
- **Gaps served:** laws aim (canonical form = volume of the polar) joined to the DEHN column: one
  object that is both a law-giving form and a scissors invariant; the "weak" note that the fill thread
  is isolated (zonotopes = parallelohedra side); 4D column for the 24-cell.
- **Effort:** medium.
- **Our hosts:** yes (adjoints are linear algebra; existing canonical-form scripts extend).

### 7. FLINT 3 exact real algebraic numbers (former Calcium and Arb)
- **Source:** F. Johansson, "Calcium: computing in exact real and complex fields", arXiv:2011.01728;
  docs https://flintlib.org/doc/introduction_calcium.html and https://flintlib.org/doc/qqbar.html
  **[unverified: from search snippets of these pages; not opened]**.
- **What it does:** `qqbar` stores an algebraic number by its minimal polynomial and an isolating
  interval, so equality and sign tests are exact; Arb ball arithmetic for fast certified bounds.
- **Gaps served:** #90 structure over Q(√2, √5); #111 the fields of the radii of T ∩ D and of the 42-
  and 50-face dice; #6 lead (the 19-design station μ* of degree 20 over Q) — exact root isolation of
  high-degree stations; #80/#81 windows. Also the e-antic back end of item 1.
- **Effort:** small (python-flint bindings).
- **Our hosts:** yes (LGPL, packaged on Linux).

### 8. Dehn–Sydler–Jessen by homological algebra, and the tiling theorem in every dimension
- **Sources:** A. Nanavaty, "Dehn–Sydler–Jessen via Homological Algebra", arXiv:2502.03380 (Feb 2025;
  in library #479; seen via search, abstract not reopened); J. C. Lagarias, D. Moews, "Polytopes that
  fill Rⁿ and scissors congruence", DCG 1995 (in library #263); A. Garber, "Voronoi conjecture for
  five-dimensional parallelohedra", arXiv:1906.05193, Invent. Math. 2025 **[journal data from a search
  snippet]** (in library #99).
- **What it does:** a self-contained review of the group-homology proof of Sydler–Jessen (the route
  Dupont–Sah took); Lagarias–Moews: a polytope that tiles Rⁿ has all classical Dehn invariants zero
  and, in dimensions ≤ 4, is scissors congruent to a cube **[from search snippet]**.
- **Gaps served:** study 2026-11-20-palomar-next-prescore: Sydler's converse in Lean and E2, the
  Dehn–Hadwiger invariant in four dimensions; #113 Sydler's converse in Lean; 4D column ("a 4D union
  that fills space; an actual dissection to the 4-cube", study 2026-11-20-600cell-5cell-zero).
  Searches found **no** Lean, Isabelle or Coq formalization of the Dehn invariant, Hilbert's third
  problem, Sydler or Wallace–Bolyai–Gerwien (see Sources checked) — so a Lean development there would
  be first, as far as these searches reach.
- **Effort:** large (the homological route is long in Lean).
- **Our hosts:** yes (Lean).

### 9. PyQCstrc: 6D models of icosahedral quasicrystals
- **Source:** T. Yamada, "PyQCstrc.ico: a computing package for structural modelling of icosahedral
  quasicrystals", J. Appl. Cryst. 2021; https://github.com/ttyamada/PyQCstrc (MIT, PyPI)
  **[unverified: from search snippets; pages not opened]**. Older than 2023, but the only maintained
  open tool found.
- **What it does:** builds occupation domains in the 6D icosahedral lattice and projects them, the
  cut-and-project step done as a library.
- **Gaps served:** bridge aim; #30 "spine = thinned cut-and-project chain; seams as model sets";
  #40 "OG on aperiodic stackings with diffraction"; #43 "shell ratios against Tsai clusters" (queued).
- **Effort:** medium.
- **Our hosts:** yes (Python).

### 10. Space-filling stereohedra: Schmitt's classification as data, with the facet bounds
- **Sources:** E. Pegg, "Spacefilling polyhedra: Voronoi cell tessellation & stereohedra classification
  in 3D Euclidean space", Wolfram Community, 15 Apr 2026, 14.3 MB notebook (opened; the page itself
  gives no count and no source); a seqfan post says 3903 space-filling polyhedra compiled from
  M. W. Schmitt, "On Space Groups and Dirichlet–Voronoi Stereohedra" **[unverified: forum snippet]**;
  Sabariego–Santos facet bounds, arXiv:math/0608039 and 0708.2114 (≤ 92 facets for any 3D Dirichlet
  stereohedron; in library) **[bounds from snippets]**.
- **What it does:** a machine-readable list of isohedral space-fillers by space group.
- **Gaps served:** fill thread ("Joining the fill thread to the cuts and the sweep", #47 questions 1
  and 3); #51 "one solid per bond that fills alone"; #50 "which dissection fillers the moves reach";
  #87 other centres for solids of low symmetry. A lookup table to test our pieces against.
- **Effort:** medium (convert the notebook once).
- **Our hosts:** needs the Wolfram Engine (free licence for personal non-commercial use
  **[unverified]**); after one export, plain data.

---

## Further tools found (not top 10)

| Tool | Source (opened unless marked) | Gap it touches | Effort | Hosts |
|---|---|---|---|---|
| Mahler volume ≤ flags/(d!)²·… | M. Winter, arXiv:2610.09990 (Oct 2026), in library #372 | SWP, laws: Mahler values against flag counts of our solids | small | nothing to run |
| Floating bodies and Mahler minimizers | A. Guberman, arXiv:2608.10994 (Aug 2026) | SWP (structure of minimizers) | small | — |
| Valuations and hyperplane arrangements | A. Khovanskii, V. Kiritchenko, V. Timorin, arXiv:2601.03176 (Jan 2026), in library #491 | DEHN (valuations for arrangements of cut planes, e.g. golden cuts) | medium | — |
| SAT detection of isohedral polyforms | C. S. Kaplan, arXiv:2406.16407 (2024) **[snippet]**; Heesch numbers by SAT, arXiv:2105.09438 **[snippet]** | #47 smallest kit; aim 3 (paused) | medium | yes |
| Enumerating polyforms on 3D tilings | B. Dobbelaere, P. Kagey, D. Thomas, A. R. Vindas-Meléndez, arXiv:2602.23301 (Feb 2026); code not linked | #41 third level of Hexas; poly-RD counts | medium | yes if code found |
| Undecidability of tiling R³ by 3 polycubes | C. Yang, Z. Zhang, arXiv:2508.00192 (Jul 2025), in library #1029 | aim 3: limit on general search; argues for targeted keys | — | — |
| Translational tilings survey | R. Greenfeld, arXiv:2509.25576 (Sep 2025) | aim 3 background | small | — |
| Minkowski reconstruction (normals + areas → polyhedron) | M. Sellaroli, arXiv:1712.00825, "polyhedrec", Python **[snippet]** | #112 Aequi as Wulff shapes; fair dice from face areas | small | yes |
| Adjoints of tree amplituhedra | K. Ranestad, R. Sinn, S. Telen, arXiv:2402.06527 (2024) **[snippet]** | laws aim | small | — |
| polymake 4.15 (30 Sep 2025) | https://polymake.org/doku.php/news (opened; features not listed there) | general polytope work | small | yes |
| Lean polyhedral geometry | https://github.com/uw-math-ai/lean-polyhedral-geometry (opened: Lean 4, GPL-3.0, 125 commits; goal H/V equivalence, proved content not listed) | #113, E1 formal Wallace–Bolyai–Gerwien (definitions to reuse) | medium | yes |
| Special cuts of the 600-cell | M. Dutour Sikirić, W. Myrvold, Beitr. Alg. Geom. 49 (2008) **[snippet]**, in library | #62 600-cell slices | small | — |
| Markov description of stacking disorder | Hart, Hansen, Kuhs, arXiv:2102.08418 (2021) **[snippet]**, in library | CH column, #40 diffraction of mixed stackings | medium | yes |

## Searched, nothing new found (2023–2026)
- A Lean, Isabelle or Coq formalization of the Dehn invariant, Hilbert's third problem, Sydler's theorem
  or Wallace–Bolyai–Gerwien: none found (three searches + Lean Zulip archive). Myers's hat
  formalization: only a 2023 Zulip intention found.
- Mathlib polytope theory: the 2020 Zulip thread "convex polytopes" (opened) shows none then; a 2025
  proposal by Berlin/Leipzig geometers is reported in a search snippet **[unverified]**.
- Fair dice: no 2023–2026 arXiv paper found (two searches); newest is Taniguchi–Uehara arXiv:1810.12108.
- Discrete Minkowski/Alexandrov algorithms: nothing newer than polyhedrec (2017).
- Stacking-fault / polytype theory 2024–2025: nothing new beyond what the library holds.
- Hyperplane sections of the 600-cell 2024–2025: none.
- Frank–Kasper enumeration 2024–2025: none (newest Dutour Sikirić–Delgado-Friedrichs–Deza 2010).
- Dirichlet stereohedra 2023–2025: none.
- Scutoids 2024–2025 on arXiv: none found (only 2018–2020 work).
- 3D isohedral tilings by convex polyhedra 2025: none.

## Candidates to add to the reference library (not in INDEX.pdf, checked by grep)
Kedlaya–Kolpakov–Poonen–Rubinstein arXiv:2011.14232 (+ code link); Johansson, Calcium arXiv:2011.01728;
Gaetz arXiv:2504.07272; Ranestad–Sinn–Telen arXiv:2402.06527; Fradelizi–Meyer–Zvavitch, "Volume
product" survey arXiv:2301.06131; Kaplan arXiv:2406.16407 and arXiv:2105.09438; Sellaroli
arXiv:1712.00825; Greenfeld arXiv:2509.25576; Dobbelaere–Kagey–Thomas–Vindas-Meléndez arXiv:2602.23301;
Taniguchi–Uehara arXiv:1810.12108; Yamada, PyQCstrc.ico (J. Appl. Cryst. 2021); software links:
Normaliz + e-antic, LeanCert, Monotile-RN, polymake.

## Sources checked
Web searches (all standard mode):
1. Lean Mathlib Dehn invariant Hilbert third problem formalization — nothing on formalization.
2. arXiv 2024 scissors congruence four dimensions Dehn–Hadwiger Jessen Sydler new proof — older work only.
3. arXiv fair dice polyhedra isohedral 2024 2025 — nothing new.
4. arXiv 2025 space-filling convex polyhedra stereohedra Voronoi parallelohedra — Pegg post, seqfan thread.
5. arXiv aperiodic monotile three dimensions 2025 — Tsiokos, Flicker, Goodman-Strauss, Kaplan 2509.12216.
6. Lean 4 formalization scissors congruence Dehn invariant 2025 — Nanavaty 2502.03380 only.
7. Mahler conjecture recent progress 2025 — Chen–Li–Xi–Xu, Guberman, Winter.
8. arXiv discrete Minkowski problem polytope algorithm 2024 — Sellaroli 1712.00825.
9. arXiv Fibonacci stacking close-packed polytypes matching rules — nothing new.
10. Isabelle AFP or Lean "Hilbert's third problem" — nothing.
11. "Dehn invariant" Lean github — nothing (Zulip Proofs-from-the-Book thread).
12. Mathlib convex polytope definition 2025 — UW project, Zulip threads.
13. arXiv 2025 tilings by congruent copies Dehn invariant zero — Chentouf–Sun, Garber–Pak 2003.04667.
14. arXiv 2025 Voronoi conjecture parallelohedra dimension five — Garber 1906.05193.
15. arXiv 2024 positive geometry canonical form adjoint software — Gaetz, Ranestad–Sinn–Telen, others.
16. arXiv sections of the 600-cell 2024 2025 — Dutour Sikirić–Myrvold 2008 only.
17. Lean formalization aperiodic hat spectre 2025 — none.
18. Wallace–Bolyai–Gerwien formalized Lean/Isabelle/Coq — none.
19. Myers formalization hat Lean — 2023 Zulip only.
20. arXiv 2024 SAT solver tiling Heesch Kaplan — 2406.16407, 2105.09438.
21. Kedlaya Kolpakov Poonen Rubinstein rational angles — 2011.14232, GitHub.
22. arXiv fair dice Alexandrov/Minkowski 2023 2024 — nothing new.
23. arXiv Sydler new elementary proof 2023 2024 — Nanavaty, Schwartz notes.
24. Normaliz / polymake / SageMath new features 2024 2025 — release data only.
25. arXiv Frank–Kasper enumeration 2024 2025 — nothing new.
26. arXiv 2025 isohedral tilings of three-space enumeration — 2602.23301, 2606.26140 (face tilings, not relevant).
27. Lean 4 verified interval arithmetic 2025 — LeanCert, FloatLib 2609.19352, Gappa tactic.
28. arXiv 2024 2025 aperiodic stacking diffraction Baake Grimm — Hart et al. 2021 only.
29. arXiv 2024 2025 scutoids — nothing new.
30. FLINT 3 Calcium qqbar — FLINT docs.
31. Greenfeld Tao undecidability periodic tiling — Greenfeld 2509.25576, Yang–Zhang papers.
32. cut-and-project software icosahedral Python — PyQCstrc, quacry, 2609.33863 (1D Fibonacci tool).
33. Dirichlet stereohedra 2023–2025 Bochiş Santos — older papers only.
34. Hadwiger invariants 4D 24-cell tesseract — 2508.04275, 2601.03176.
35. arXiv 2025 2026 fair die not isohedral — nothing new.

Pages opened (WebFetch): arxiv.org/abs/ 2609.24779, 2605.09334, 2610.09990, 2608.10994, 2312.01654,
2504.07272, 2509.12216, 2602.23301, 2508.00192, 2509.25576, 2609.19214, 2601.03176, 2508.04275,
2610.00916; community.wolfram.com/groups/-/m/t/3688732; reservoir.lean-lang.org/@alerad/LeanCert;
leanprover-community Zulip archive "convex polytopes"; github.com/uw-math-ai/lean-polyhedral-geometry;
github.com/kedlaya/tetrahedra; github.com/Normaliz/Normaliz; polymake.org/doku.php/news.
Local: concordance.json gaps; aims (bridge, laws, one piece); reference library INDEX.pdf (Pi copy).
