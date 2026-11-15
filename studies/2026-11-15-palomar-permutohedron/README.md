# Palomar pre-score: the permutohedron work (15 November 2026)

**Verdict. No candidate reaches notability 4. Do not start any Lean work for these.** Nineteen statements from #104, #105, #107, #108 and *The Permutohedron Paradigm* were scored blind. The best are at 3: #105 Theorem 3 (the Vacuus count N(n)), #104 Theorem 3 (the Swap defect, computer-assisted), and book Theorems 12.1–12.2 (the golden slice) and 14.3 (the equal-edged members). Everything else scored 2. Palomar rejects below 4, so each of these would come back `rejected`, the same as the two earlier entries: Loop Equality scored 3 and the Kyushindo Theorem 4 entry scored 2. Our own reading agrees with the blind replies on every row. The one with a real chance after **new mathematics** is #105 Theorem 3, taken from one polytope to a theory (see "What would reach 4").

**Status:** estimate only. Nothing was built or submitted. The production reviewer (`palomar-review`, model `codex:gpt-6-sol`) cannot be run outside Palomar's broker; see the method of the two earlier studies (2026-11-14-lean-loop-equality/SCORE.md, 2026-11-15-palomar-kyushindo/SCORE.md).

## How notability is judged (PalomarPolicy @ 28bd48b)

- **The two tests** (CONTRIBUTING §1). The result "could plausibly warrant a research paper or a serious research note", and the reviewer can name "a credible research area and a plausible kind of mathematician" who would care. Both tests are needed.
- **Anchors** (§7):
  - 2: trivial, routine or lightly repackaged;
  - 3: paper-worthiness or audience "not affirmatively established";
  - 4: "plausibly paper-worthy, with a specifically identified credible research audience".
- **Floor.** Notability below 4 means `rejected`.
- **What does not count** (prompt 04): "Formal verification, effort, length, and polish do not by themselves establish research interest."
- **What the earlier reviewer penalised:** short corollaries of known theorems (Kyushindo: "a short routine corollary of the known orbit-space diameter"); single-polytope or single-dimension results; and unrefereed sole sources with no outside reception.

## Method

1. **Statements.** Each candidate is stated precisely in `blind/inputs/` (four files: A = #105, B = #104, C = #107 + #108, D = book-only theorems).
2. **Blind replay.** Four fresh agents (Claude Opus 5.5), one per file. Each was given only the policy (CONTRIBUTING §1 and §7, prompt 04, rubric.json) and that file (the bare statements and the paper's abstract). They were not given our notes, earlier scores or these papers. Each searched the web on its own and returned prompt 04's JSON for every statement: `blind/blind-A-105.json`, `blind-B-104.json`, `blind-C-107-108.json`, `blind-D-book.json`.
3. **Own reading** against the papers' full texts and their own "classical / new" notes (below).
4. **Mathlib check.** Read on GitHub (mathlib4 master, 15 November 2026). Code search finds no `permutohedron`, no hyperplane arrangements and no face lattice of polytopes.
   - **What exists:** `convexHull`, `IsExtreme` / `IsExposed`, `Equiv.Perm` and `Finset` counting, Birkhoff's theorem (`doublyStochastic_eq_convexHull_permMatrix`), `CoxeterMatrix` / `CoxeterSystem` (A–H types), and root pairings.
   - **What is missing:** majorization ⇔ membership in the permutohedron (Rado's theorem) is listed as a TODO in `Analysis/Convex/Birkhoff.lean`, not proved. There is no h-vector, no Dehn–Sommerville and no Wythoff construction.

The blind input for A1 left out the paper's own citation of the resonance arrangement (Kamiya–Takemura–Terao 2011; Billera et al. 2012; Kühne 2023). So the blind literature score of 3 for A1 is low by a point; a real package would cite it, as #105 does. Notability is not affected.

## Table

| # | Candidate | Known? | Blind pre-score (notab. / lit.) | Own | Lean feasibility and size | Recommendation |
|---|---|---|---|---|---|---|
| A1 | #105 Thm 3: ridges of Π_n span N(n) central hyperplanes, N(n) = Σ_{a<c} n!/(a!b!c!) + T(n) | Count not found stated (OEIS: no match for 3, 15, 65, 225, 770, 2443; A402191 is only allocated, no terms yet). Two-valued part = resonance hyperplanes; the proof is a count of normals. | **3** / 3 | 3 | **Geometric:** ridges as faces of conv(perms) needs the face lattice of Π_n, which Mathlib lacks: very large. **Combinatorial:** ridges *defined* as ordered 3-partitions, slices by explicit normals, closed form for all n: medium (roughly 1–2k lines), but risks "definitions designed to manufacture the conclusion". | Best of the set; not enough alone. Basis for the route below. |
| A2 | #105 Thm 1: 150 faces of Π_5 on 65 slices, 4 classes | n = 5 case of A1 plus exact shapes | 2 / 3 | 2 | Finite check, `decide`-style: small–medium | No |
| A3 | #105 Lemma 2a, Thm 2, Thm 2b (heart in every odd dimension) | A few lines from Rado's majorization theorem; Thm 2b iterates the lemma | 2 / 3 | 2 | Needs Rado (not in Mathlib): large; with membership defined by majorization: small, but then trivial | No |
| A4 | #105 Thm 4: T(x) is the permutohedron of −q, −p, p, q | One-line change of coordinates (A₃ = D₃) | 2 / 2 | 2 | Small–medium (explicit isometry; hull equality) | No |
| B1, B1′ | #104 Thms 1, 1′: sweep events counted by h_i | Classical (McMullen; Bruggesser–Mani; Ziegler Lect. 8; C. W. Lee 2011); #104 says so | 2 / 3 | 2 | h-vector of simple polytopes absent: very large | No |
| B2 | #104 Thm 2: (116, 366, 116), (716, 966, 716), (716, 2166, 716) | Evaluation from known f-vectors | 2 / 3 | 2 | Arithmetic small; meaning needs B1 | No |
| B3 | #104 Thm 3: Swap defect of close-packed stackings, s ∈ [1/8, 1/4] | Self-defined quantity; computer-assisted (35.5 M exact sign checks) | 3 / 2 | 2–3 | Out of reach for a kernel-checked proof: very large | No |
| B4 | #104 Thm 4: balance law, 601 each way | In substance Stanley 1979 (a-balanced spheres, fine h-numbers; Bayer–Billera 1985) | 2 / 3 | 2 | Combinatorial model: medium–large; geometric: very large | No |
| B5 | #104 Lemma 5: truncated 600-cell has no pure swap | Max cut of W₅ | 2 / 3 | 2 | Small | No |
| C1 | #107 Thm 1, the Mirror Law | A few lines from parabolic stabilisers (Bourbaki V.3.3; Humphreys 1.12) plus the Wythoff face description (Champagne–Kjiri–Patera–Sharp 1995); #107 says "may be known" | 2 / 2 | 2 | Root pairings exist; Wythoff faces and root positivity in the needed form do not: medium–large | No |
| C2 | #108 Thm 1, balance law for any type multiset | Stanley 1979 Prop. 3.6 (fine h-numbers of a-balanced spheres; symmetry h_b = h_{a−b}); Book Ch. 9 already says so | 2 / 2 | 2 | As B4 | No |
| C3 | #108 Thm 3: 6, 17, 73, 601 = E − V + 1 | Evaluation; dual pairs give the same value by Euler | 2 / 2 | 2 | Arithmetic small; meaning needs C2 | No |
| D1 | Book Ch. 10: vertex degree from the diagram; rosette balance law | Vertex-figure count classical; balance immediate from chamber transitivity; book: "elementary, likely folklore" | 2 / 2 | 2 | Medium–large | No |
| D2 | Book Ch. 13: golden slice, 35 types, rank-2 periods | Rank-2 period lattice immediate; rest a census for one slope; no comparison with model-set work | 3 / 2 | 3 | Very large (cut-and-project, volumes) | No |
| D3 | Book Ch. 14 Thm 14.3: equal-edged members 17 / 101 / 4427 | Characterisation direct from edge-length coordinates of deformation cones; counts unstructured | 3 / 2 | 3 | Large | No |
| D4 | Book Prop. 14.4: graphical zonotopes tile | Shephard / McMullen: zonotopes of regular (hence graphic) matroids tile | 2 / 2 | 2 | Large | No (see note 1) |
| D5 | Book Thm 14.1: the Postnikov line | From convexity of the deformation cone; Hohlweg–Lange | 2 / 2 | 2 | Large | No |
| D6 | Book Ch. 15: 44 and 5396 Hamiltonian cycles, symmetry classes | 44 in OEIS A343433; 10 792 Minimus extents (Polster–Ross) = 2 × 5396 | 2 / 2 | 2 | `decide` on finite graphs: feasible but heavy | No (see note 2) |

## Own reading

- **The pattern is the same as in the earlier entries.** Each proof is short once a classical tool is named: Rado for the heart, McMullen's h-vector for the sweeps, Stanley's balanced spheres for the balance law, parabolic stabilisers for the Mirror Law. What is new is DICTO's reading (Vacuus, scutoid tissue, the Queens) and exact data for named polytopes. Palomar scores the theorem as it would be stated in a Challenge, not the reading. Prompt 04 sends a short consequence of a classical theorem to 2.
- **A1 is different in kind.** It holds for every n, the sequence is new, and the three-valued slices (normal bc(b+c), −ac(a+2b+c), ab(a+b) on the blocks) are not members of any standard arrangement we or the blind reviewer found. It still sits at 3, for two reasons:
  - the proof is a routine count;
  - "the central hyperplanes spanned by the ridges" has no role in known theory yet, so no audience is affirmatively identified.
- **Lean would not help** (prompt 04), and every geometric version is large: Mathlib has no face lattice of polytopes and no Rado's theorem.

## What would reach 4 (new mathematics, not packaging)

In order of best chance:

1. **The Vacuus arrangement as an arrangement.**
   - Let V_n be the arrangement of all N(n) central hyperplanes. Determine its intersection lattice, characteristic polynomial or number of regions, at least in closed form for its three-valued part.
   - Relate it to the resonance arrangement, whose region count is a known open problem with an active audience (Billera–Tatch Moore–Moraites–Wang–Williams; Kühne; Gutekunst–Mészáros–Petersen). V_n contains the half of the resonance hyperplanes that come from the two-valued slices.
   - A theorem of the form "V_n ∩ (resonance) = …, and V_n has χ(t) = …", or a bound on regions that improves a known one, would give a named audience (hyperplane arrangements, Coxeter combinatorics).
2. **All Coxeter permutohedra and all face dimensions.**
   - Replace Π_n by the Wythoff polytope of any finite reflection group, and ridges by k-faces.
   - Prove a uniform formula for the number of central hyperplanes, with the Mirror Law (C1) as the "on a mirror" part and A1 as type A.
   - Classify when off-mirror slices carry three or more faces. #108 Observation 4 found only the runcinated 5-cell and the permutohedron in rank 4; a proof for every rank and type, D_n and E_n included, would be a real theorem.
3. **Value-space walls.**
   - For the permutohedron of generic values v the slices are all distinct; coincidences happen on walls in v-space.
   - Describe this wall arrangement and show that the equally spaced case is its most degenerate point. This links to deformation cones (Postnikov; Padrol–Pilaud–Ritter).
4. **Not recommended.** More single-polytope counts, more chains, or Lean formalisation of the existing statements. The blind reviewers say each of these stays at 2 or 3.

## Points to pass on (no change made here)

1. **Book Prop. 14.4 (ii)** says "the five such graphs". There are six connected graphs on four vertices; the path and the star both give the parallelepiped (five solids, six graphs). This goes through the Concordance errata route. The Shephard–McMullen credit for (i) should be added at the next version (credit at point of use).
2. **Book Ch. 15** should credit OEIS A343433 (the truncated octahedron's 44 Hamiltonian cycles) and Polster–Ross's Minimus extent count at the point of use.
3. **#105 Theorem 3 / A402191:** the OEIS page shows the number allocated with no terms yet (draft not yet live on 15 November 2026).

## Files

- `blind/inputs/A-105.md`, `B-104.md`, `C-107-108.md`, `D-book.md`: the statements and abstracts the blind reviewers saw.
- `blind/blind-A-105.json`, `blind-B-104.json`, `blind-C-107-108.json`, `blind-D-book.json`: their replies, prompt 04 shape, one object per statement, with `what_would_reach_4`.
