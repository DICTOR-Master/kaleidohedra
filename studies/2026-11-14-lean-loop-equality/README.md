**Status (19 November 2026): set aside by DICTO as not viable for Palomar for now (pre-score 3). Not submitted.**

# Palomar preparation (2026-11-14)

DICTO said yes to preparing a Palomar submission on 14 November 2026. This study covers steps 1–3 only: the rules, a working Lean workspace, and the choice of a first entry. **Nothing has been submitted.** No issue or pull request was opened anywhere. Submission needs DICTO's word.

**Conclusion.** The first entry should be **#43 Theorem 4, the octahedral constant 3**, with the covering lemma and sharpness in the same Challenge. The second should be **#102, the Loop Equality**: it is the most notable result, but it is a much larger formalisation. The Challenge statements of both compile against Palomar's toolchain (`lean/`, every proof `sorry`).

**Status:** rules read; workspace built (FINAL ok); statements typecheck. **15 Nov: #43 Theorem 4 is fully proved in Lean** (`lean/OctahedralNestingProof.lean`, no `sorry`, only the three allowed axioms; §5). On 15 Nov DICTO decided that it will **not** be the first Palomar entry, because the covering lemma is known (LITERATURE.md). No Palomar repository was prepared.

## 1. Rules (read 14 Nov 2026)

**Sources read.** The URL in the brief, `github.com/PalomarRegistry/PalomarDatabase`, returns 404. The registry's repositories are under the `PalomarRegistry` organisation, and the database repository is `henriqueheine/PalomarDatabase`, which the policy repository links to. Files read, at these commits:

- PalomarRegistry/PalomarPolicy @ 28bd48b: `README.md`, `CONTRIBUTING.md` (the binding submitter standard; sections 1–5, 7 and 9 in full), `LICENSE`
- PalomarRegistry/PalomarTemplate @ 2891de4: `README.md`, `CONTRIBUTING.md`, `lean-toolchain`, `lakefile.toml`, `lake-manifest.json`, `formalization.yaml`, `comparator.json`, `Challenge.lean`, `Solution.lean`, `PalomarTemplate.lean`, `PalomarTemplate/Basic.lean`, `LICENSE`
- PalomarRegistry/PalomarSubmission @ 14aa8d6: `README.md`, `toolchains.json`, `verification-profile.json`, `LICENSE`
- henriqueheine/PalomarDatabase @ 23da4f1: `README.md`, `LICENSE`
- https://submit.palomar-registry.org/llms.txt

**Lean and mathlib versions.** Palomar sets a **floor, not a pin**. `toolchains.json` says `"minimum": "v4.35.0-rc2"`: this is the first release with `lake comparator`. A submission is judged with the toolchain in its own `lean-toolchain`, which must match the `lean-toolchain` of the resolved Mathlib revision exactly. The official template pins `leanprover/lean4:v4.35.0-rc2` and Mathlib tag `v4.35.0-rc2`, which is commit `065356127b1dc0016f66b7283ce0ce2c4055aa55`. This workspace uses that same pair. Later pairs, such as v4.35.0 with Mathlib `v4.35.0` (56a0058), would also be accepted.

**Axioms.** `comparator.json` may permit only `propext`, `Quot.sound` and `Classical.choice`. Comparator rejects any proved declaration that depends on `sorryAx`, `Lean.ofReduceBool` or a custom axiom. **`sorry` and `native_decide` are therefore banned in proofs** (`native_decide` uses `Lean.ofReduceBool`). The proof is checked by Lean's kernel and by the independent NanoDa kernel, and a con-ron replay is also attempted. Plain `decide`, `norm_num` and `ring` are allowed.

**Entry format.** The entry is a public GitHub repository at a fixed 40-character commit. It contains:
- `lean-toolchain`
- `lakefile.toml` or `lakefile.lean`
- a committed `lake-manifest.json`
- exactly one root licence file
- `formalization.yaml`, in the upstream v0.4 self-reporting format
- `comparator.json`, which lists `challenge_module`, `solution_module`, `theorem_names`, optionally `definition_names`, and `permitted_axioms`
- `Challenge.lean`: the small, auditable statement, with one `sorry` per advertised theorem. It may import only Lean core, Mathlib, Tau Ceti or CSLib, and is limited to 1,000 lines and 100 KiB.
- `Solution.lean`: the same declarations with proofs. It may import any pinned public GitHub dependency.

Further rules:
- Every `.lean` file must use the module system (`module`, `public import`) and have at most 10,000 lines.
- No build output may be committed.
- One Comparator configuration makes one entry.
- Identifiers have the form `PALOMAR-YYYY-MM-DD-NNNNNN-vN`. A later commit of the same configuration becomes the next version.
- Before submitting, run the reusable PalomarSubmission workflow as a preflight (`execution_profile: palomar-standard-v1`). The only way in is the form at submit.palomar-registry.org.

**Review and what is acceptable.** Two gates:
1. Mechanical verification, as above.
2. An automated AI editorial review. A language model works through fixed prompts, and no person reads the submission before the outcome. It checks classification, metadata and provenance, alignment between the statement and the informal account, fidelity of definitions, and literature and notability.

Each check is scored from 1 to 5, and the minimum is 4. **A notability score below 4 means rejection.** The result must "plausibly warrant a research paper or a serious research note", and the reviewer must be able to name a credible research audience. Being proven, novel or large is not enough on its own. Trivial results, definitions built to manufacture a conclusion, and repackaged work are not indexed. Novelty may be claimed only after a credible literature search; otherwise the metadata must say novelty is unknown. The outcomes are neutral (may register), revision_required or rejected. There is no appeal: a submitter resubmits a corrected commit.

**Authorship and AI disclosure.** `project.authors` and `responsible_maintainers` must be humans: here, DICTO. They must not name an AI model, agent or tool, following the Leiden Declaration's human-authorship principle. AI contributions are declared in `automation.methods` (method `agent`, models, tool setup, and optionally cost) and in the narrative account of the work, including human review. `review.status` must be honest, for example `self-assessed` or `agent-reviewed`. The submitter declares that they are a responsible author or maintainer. A false declaration counts as material misrepresentation. Write access is proved separately, either by browser sign-in or by a tag plus a gist.

**Licence.** The submitted repository needs exactly one standard SPDX licence, which must match `project.license`. The template supports Apache-2.0, and other licences permitted by Palomar policy are possible. Papers that are cited, such as DICTO's papers under CC BY-SA 4.0, keep their own licences. Palomar's own policy and database metadata are released under CC0 1.0, and its submission tooling under MIT.

## 2. Workspace

A Lake project on the compute host, outside this repository. Its `.lake` folder (7.5 GB) is not committed.
- `lean-toolchain`: `leanprover/lean4:v4.35.0-rc2` (Lean 4.35.0-rc2, commit 11acb17)
- `lakefile.toml`: Mathlib `rev = "v4.35.0-rc2"`
- `lake-manifest.json`: the template's manifest, copied unchanged. Mathlib resolves to `065356127b1dc0016f66b7283ce0ce2c4055aa55`. After `lake update`, the manifest was byte-identical to the template's.
- Mathlib cache: `lake exe cache get` completed; 8,723 files were decompressed.
- Smoke module: imports Mathlib and proves `0 ≤ x^2` and `√5·√5 = 5`. `lake build` finished with "Build completed successfully (8933 jobs)" and the job ended with **FINAL ok**.
- The two statement files below build in the same project (only `sorry` warnings). A sanity module checks by `decide` that `IsOctahedralRotation` selects exactly 24 of the 48 signed permutations, and that diamond is a stacking.

## 3. Candidates

| | Statement | Mathlib pieces | Missing from Mathlib | Size | Risks | Whose |
|---|---|---|---|---|---|---|
| **A. #43 Theorem 4** (octahedral constant 3), with the covering lemma and sharpness | `lean/OctahedralNesting.lean` | `EuclideanSpace ℝ (Fin 3)`, inner product, `convexHull`, pointwise `•` on sets, finite-dimensional separation (`geometric_hahn_banach_*`), `Equiv.Perm.sign`, `Fintype` sums, `Real.sqrt` | an octahedral group (defined here as 24 signed permutations); polytopes and facets (avoided: the body is given by half-spaces) | 600–1,000 lines; 1–2 weeks | no floating point. Only √3 appears. The 24 rotations are a finite case split (`fin_cases`/`decide`). The moment identities Σt = 0, Σt² = 8, Σt³ = 0 are polynomial identities (`ring`). Main risk: notability. | DICTO's: Conjecture 2 in #43 v1, proved in v2 (proof with Claude). The moment/3-design method is classical (Delsarte–Goethals–Seidel). A literature search is needed before any novelty claim. |
| **B. #102 Loop Equality** (closed non-backtracking loops at every site of every close-packed stacking equal diamond's) | `lean/LoopEquality.lean` | `ZMod 3`, `Finset`, `Set.ncard`/`Set.Finite`, `Fin m` cyclic indices | non-backtracking walks; Ihara–Bass; the Fourier step over the layers (needs either torus integration or a group-ring/Laurent-polynomial replacement); walks on infinite locally finite graphs | 2,000–4,000 lines; 4–8 weeks | no floating point, no transcendental functions. Hard parts: the cancellation argument (each bond layer crossed equally often upwards and downwards), the reduction of NB loops to walks between bond ends, and finiteness. | Conjecture DICTO's (#74); proof with Claude. Known and credited: closed walks (Nagle 1966, Thorpe 1972) and site-averaged periodic loops (Guido–Isola–Lapidus 2008). New: every site, aperiodic stackings, and the corollaries. |
| C. #103 yantra, Theorem 2 (R1 in whole-number fractions) | explicit rational depths, half-widths and apices; 18 marmas (three lines concurrent), 6 corner touches, 7 apex-on-base points, great-triangle corners on the circle, admissibility inequalities | `ℚ`, `Matrix.det` or explicit line equations, `norm_num`, `decide` | a "Śrī Yantra" definition (bespoke; fidelity must be argued) | 200–400 lines; 2–4 days | exact over ℚ, no risk in the proof. Risk is in the Challenge definitions and in notability: one rational configuration is likely to be judged a computation. | R1 is DICTO's. |
| C′. #103 Theorem 1 (quadratic family) or Theorem 5 (viewpoint, β* = −y_H) | Theorem 1: 31 condition polynomials vanish or are multiples of the closing polynomial over ℚ(u, v, Q, S, b₁). Theorem 5: T_β fixes the circle, keeps incidences, and centres the bindu only at β = −y_H | `Polynomial`/`MvPolynomial`, `ring`, `field_simp` | nothing essential | Theorem 1: 1–3 weeks (large polynomials; `ring` may time out). Theorem 5: 2–4 days. | Theorems 9 and 10 (degrees 160 and 348) are out of reach without `native_decide`. Theorem 5 is largely classical (translations of the Klein model). | Theorem 1 and the uniqueness of β* are DICTO's; the Klein map is classical. |
| D. Switch theorem (#52/#53; study 2026-11-08-switch-theorem) | Theorem A: det[pᵢ, \|pᵢ\|² − wᵢ, 1] = c·(S₀ − λS_A). Theorem B: at a switch point, every like bond on one side is A–A and on the other B–B (a single switch). | `Matrix.det`, cofactor expansion, `affineIndependent` | regular (weighted Delaunay) subdivisions, lower hulls, pushing | A: 200–400 lines, 2–4 days. B: 1–3 months. | A on its own is the classical lifted test (Edelsbrunner–Shah), so it fails the notability floor. B needs a large theory. | The question (the DICTONIC loops, the web of bonds) is DICTO's; proofs with Claude; pushing is classical. |
| E. Delian walk, #93 Theorem B (for t ∈ (0, 1/3) ∪ (1/3, 1), every tiling by T(t), O(t) is #51's) | tilings of ℝ³ by congruent copies, face to face or not | almost none: Mathlib has no polyhedral tilings, dihedral angles at edges, or Dehn invariant | over 10,000 lines; months | angle sums use the irrationality of arccos(1/3)/π, which is not in Mathlib. Every case analysis is geometric. | The walk is DICTO's (#51); the theorem is DICTO's (#93, proofs with Claude). |

**Ranking for a first entry:** A, B, C/C′, D, E.
- **A** is small and exact, makes a general and sharp claim, and the trusted Challenge is short and uses only standard Mathlib notions.
- **B** has the clearest research audience (polytypes, spin ice, Ihara zeta functions) and is already checked on aiXiv, but it is about four times larger.
- **C** risks rejection on notability unless Theorem 1 carries it.
- **D** and **E** need theory Mathlib does not have.

**Short series:**
1. #43 Theorem 4, with the covering lemma and sharpness.
2. #43 Corollary 7 (pyritohedral 3, tetrahedral 9) and Lemma 3 (polar(P(S)) = T(polar S)), as a second configuration in the same repository.
3. #43 Theorem 2, the icosahedral constant 15 − 6√5. It needs 60 rotations in ℚ(√5); the exact proof by averaging three mirror images (study 2026-11-08-octahedral-constant) is the better route.
4. #102 Loop Equality.

## 4. Recommended first entry: the Lean statement

`lean/OctahedralNesting.lean` (compiles; four `sorry`s, one for each advertised declaration). Its main theorem:

```lean
theorem octahedral_nesting {ι : Type*} [Fintype ι] [Nonempty ι]
    (n : ι → E3) (h : ι → ℝ) (hn : ∀ i, ‖n i‖ = 1) (hh : ∀ i, 0 < h i)
    (hsym : OctahedrallySymmetric n h) :
    halfspaceBody n h ⊆ (3 : ℝ) • footHull n h
```

It is accompanied by `covering` (∀ unit u, w, ∃ an octahedral rotation g with 1/√3 ≤ ⟪g u, w⟫), `cube_admissible` and `octahedral_nesting_sharp` (for 0 ≤ c < 3 the cube is not inside c·P; the hypothesis 0 ≤ c was added on 15 Nov, §5).

**Fidelity notes for the informal account:**
1. The statement is made in the standard frame (symmetry axes along the coordinate axes). The paper's statement for any frame follows by rotating S.
2. The body is given by finitely many half-spaces, and P is the hull of their foot points. Applied to the facets of S, this is Theorem 4 exactly. It is slightly more general, because redundant half-spaces are allowed: they only enlarge P.
3. The hypothesis requires octahedral symmetry of the half-space family. For the facet family of a symmetric S this holds automatically.
4. Boundedness is not assumed. It follows, because every octahedral orbit of a normal positively spans ℝ³.

**Proof plan.** Take x in S.
1. By the covering lemma, every hᵢ ≥ |x|/√3, because the rotated copies of x lie in S.
2. For any unit v, the covering lemma also gives a face normal with ⟪nⱼ, v⟫ ≥ 1/√3, so the foot points reach ⟪hⱼnⱼ, v⟫ ≥ |x|/3 ≥ ⟪x/3, v⟫.
3. Separation then puts x/3 in P.

The covering lemma uses the moments over the 24 rotations and the cubic (t − m)(t + 1/(3m))² (#43 v2). This route is shorter than the one through Theorem 1.

`lean/LoopEquality.lean` (compiles; two `sorry`s) is the Challenge for the second entry.

## Before any submission (DICTO's word needed)

- Make a literature search for Theorem 4 and the covering lemma (foot-point hulls, pedal polytopes, covering radii of the orbits of finite rotation groups) and record it. If nothing is found, say "novelty unknown".
- Choose the repository: a new public repository under DICTO's account.
- Licence: Apache-2.0, as in the template.
- `formalization.yaml`:
  - authors: DICTO
  - automation: `agent`, Claude Code (Opus)
  - review: self-assessed
  - sources: #43 (DOI) with relationship `formalizes`. Since #43 already presents the result, this is not `original-proof`.
- Run the PalomarSubmission reusable-workflow preflight.

## 5. Formal proof of #43 Theorem 4 (15 Nov 2026)

DICTO approved the formalisation on 15 Nov 2026. Files:
- `lean/OctahedralNesting.lean`: the statement (Challenge form, four `sorry`s). Changed from 14 Nov in one place: `octahedral_nesting_sharp` now has the hypothesis `0 ≤ c` (see note 6 below).
- `lean/OctahedralNestingProof.lean`: the same definitions and theorems, all proved (274 lines). It ends with four `#print axioms` lines.

**Proof route.** This is the shorter route from §4: it does not use Theorem 1.
- (a) The 24 rotations are an explicit list `rot : Fin 24 → …` of signed permutations. `decide` checks that each has determinant `sign σ · ∏ sᵢ = 1`, that the list has no repeats, and that it contains every rotation of the group.
- (b) Covering lemma, in a general form: `‖u‖‖w‖/√3 ≤ ⟪g u, w⟫` for some g. Write t_g = ⟪g u, w⟫. The identities Σt = 0, Σt² = 8‖u‖²‖w‖² and Σt³ = 0 over the list are `ring` identities. Then use the cubic (M − t)(t + M)² with M = ‖u‖‖w‖/√3: it is the paper's cubic, since 1/(3m) = m at m = 1/√3.
- (c) Separation: a point outside the finite foot-point hull is strictly separated from it (`geometric_hahn_banach_closed_point`, then the Riesz vector `InnerProductSpace.toDual`).
- (d) Theorem 4. For x in the body, every hᵢ ≥ ‖x‖/√3, by covering with u = nᵢ, w = x and the symmetry. Every direction v has a normal with ⟪v, nⱼ⟫ ≥ ‖v‖/√3, so ⟪v, hⱼnⱼ⟫ ≥ ‖x‖‖v‖/3 ≥ ⟪v, x⟫/3. Hence x/3 cannot be separated from P.
- (e) Sharpness: the point (1, 1, 1) of the cube, against the half-space Σyᵢ ≤ 1, which contains the octahedron P.

**Informal ↔ formal correspondence** (paper v3, Theorem 4: "Every convex polytope S with octahedral rotational symmetry about O satisfies S ⊂ 3·P(S), and the constant is sharp (cube, octahedron).")
1. *Frame.* Formally, the symmetry axes lie along the coordinate axes, and O is the 24 signed permutation matrices of determinant 1 in `EuclideanSpace ℝ (Fin 3)`. The paper's statement in any frame follows by a rotation, which preserves S, P(S) and scaling.
2. *What "body" means.* S is given as `halfspaceBody n h` = {x : ⟪nᵢ, x⟫ ≤ hᵢ for all i}, for a nonempty finite family of unit normals nᵢ. P(S) is `footHull n h`, the convex hull of the foot points hᵢnᵢ. With the facet planes of S as the family, this is the paper's S and P(S). Redundant half-spaces are allowed, so the formal theorem is slightly more general: extra foot points can only enlarge P.
3. *Symmetry hypothesis.* `OctahedrallySymmetric n h`: every rotation carries each plane of the family to a plane of the family. This holds for the facet family of an octahedrally symmetric S.
4. *Strengthenings.* (i) Boundedness of S is not assumed. (ii) The hypothesis hᵢ > 0 (O inside S) stays in the statement to match the paper, but the proof does not use it: for a symmetric family, the covering step already forces hᵢ ≥ ‖x‖/√3 ≥ 0 whenever S is nonempty. (iii) The covering lemma is proved for all u, w with the bound ‖u‖‖w‖/√3. The stated `covering` is the unit case.
5. *Covering lemma, credit.* That every O-orbit on the unit sphere comes within angle arccos(1/√3) of every direction is the statement that S²/O has diameter arccos(1/√3). This is **known**: S. Greenwald, Indiana Univ. Math. J. 49 (2000) 1449–1479; W. D. Dunbar, S. J. Greenwald, J. McGowan, C. Searle, Differential Geom. Appl. 27 (2009) 307–319, Table 2; see also J. McGowan, Compositio Math. 87 (1993) 79–98 (LITERATURE.md). The moment proof used here is the one in #43 v2. The containment S ⊂ 3·P(S) for the foot-point hull was not found in print (LITERATURE.md), but it is close to the known diameter.
6. *Sharpness.* The formal statement covers the cube only (the octahedron is not formalised). It needs **0 ≤ c**: the 14 Nov draft said "for every c < 3", which is false for c ≤ −3, since c·P is then |c| times the centrally symmetric octahedron, which contains the cube for |c| ≥ 3. With 0 ≤ c < 3 it matches the paper's meaning of "sharp".

**Milestone log (15 Nov 2026).** Every check was run on the compute host, in the workspace pinned to Lean v4.35.0-rc2 and Mathlib v4.35.0-rc2.
- (a) Group lemma (`rot_isOctahedralRotation`, `rot_injective`, `rot_surjective`) compiles.
- (b) Covering lemma (`exists_ge_of_moments`, `covering_general`, `covering`) compiles.
- (c) Separation (`separation`, `le_dist`, `exists_foot`) compiles.
- (d) Main theorem `octahedral_nesting` compiles.
- (e) `cube_admissible` and `octahedral_nesting_sharp` (with `0 ≤ c`) compile. The draft's sharpness statement without `0 ≤ c` was found to be false.
- (f) Full build (job `kyushindo-t4-lean`): `lake build PalomarDicto.OctahedralNesting PalomarDicto.OctahedralNestingProof` gave "Build completed successfully (8932 jobs)". The proof file contains no `sorry` and no `native_decide`, and the only warning is the unused `hh`. **FINAL ok.**
- (g) Axioms output:

```
'DictoKyushindo.covering' depends on axioms: [propext, Classical.choice, Quot.sound]
'DictoKyushindo.octahedral_nesting' depends on axioms: [propext, Classical.choice, Quot.sound]
'DictoKyushindo.cube_admissible' depends on axioms: [propext, Classical.choice, Quot.sound]
'DictoKyushindo.octahedral_nesting_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
```

**Not done, on DICTO's decision (15 Nov):** no Palomar repository and no submission. The notability estimate is 2 out of 5 (LITERATURE.md). The proof stays here as a checked formalisation of #43 Theorem 4.

## Loop Equality (#102): formal proof (15 November 2026)

DICTO approved formalising #102 Theorem 1 on 15 November 2026. **Nothing has been submitted, and no Palomar repository has been created.**

**Status:** proved in Lean (Lean v4.35.0-rc2, Mathlib v4.35.0-rc2). There is no `sorry` and no `native_decide`, and the axioms are only `propext`, `Classical.choice` and `Quot.sound`.

**Files:**
- `lean/LoopEquality/`: Defs, Graph, Levels, Network, Counts, Main and Axioms, 1,488 lines in all.
- `loop-equality-outline.md`: the proof outline and the correspondence notes.
- `LITERATURE.md`, second part: the literature search and a notability estimate of 3 out of 5.

The statement is `lean/LoopEquality.lean` (the Challenge) unchanged, and it needed no extra hypothesis.

**Milestone log:**
| Milestone | Content |
|---|---|
| (a) | definitions and statement typecheck; generic graph part (`Graph.lean`), gauge lemma (`Levels.lean`), network (`Network.lean`) |
| (b) | key local lemma: walk counts at a site and along a bond do not depend on the stacking (`Counts.lean`) |
| (c) | counting lemma: #102 Lemma 3 transfer and loops as edge sequences (`Graph.transfer`, `Graph.loops_ncard`) |
| (d) | main theorems `loop_equality` and `nbLoops_finite` with no `sorry` (`Main.lean`) |
| (e) | clean build of all modules through the job wrapper on the compute host: FINAL ok; `#print axioms` for both theorems gives `[propext, Classical.choice, Quot.sound]` |

**Before any submission (DICTO's word needed):**
- Package the proof as Challenge.lean (the statement file) plus Solution.lean, which re-exports `LoopEquality.Main`.
- Check with the PalomarSubmission preflight that the comparator accepts declarations proved in imported modules; otherwise inline them.
- Write formalization.yaml v0.4: source #102 with relationship `formalizes`, authors DICTO, automation `agent`, Claude Code (Opus), review `self-assessed`.
- Note that the notability estimate (3 out of 5) is below the floor of 4.

## Loop Equality strengthened: explicit count and the Fibonacci companion (15 November 2026)

On 15 November DICTO chose "b and possibly c": strengthen #102 with its explicit count, then scout a companion. He then chose the **aperiodic Fibonacci stacking** as the companion, to be formalised in full. **Nothing has been submitted, and no repository has been created.**

**Conclusion.** The formal development now proves the count itself, not only the equality with diamond:

```lean
theorem loop_count_eq (σ : ℤ → ZMod 3) (hσ : IsStacking σ) (v : Atom) (hv : IsSite σ v)
    (m : ℕ) [NeZero m] : ((nbLoops σ v m).ncard : ℤ) = loopCount m
```

Here `loopCount` is an explicit, computable integer function: the local loop formula applied to the closed-walk counts, which come in closed form (#102 Proposition; the Domb numbers in Bala's chain form). All fifteen values in #102 (m = 6, 8, …, 34: 24, 48, 480, …, 27416593190640) are proved from it. The Fibonacci stacking is proved to be a stacking, aperiodic, and to satisfy the Loop Equality with the same explicit count.

**Status:**
- 11 modules, 2,372 lines, no `sorry` and no `native_decide`.
- `#print axioms` gives `[propext, Classical.choice, Quot.sound]` for all 15 theorems.
- Clean build FINAL ok.
- Notability estimate: 3.5 out of 5, still below the floor of 4 (LITERATURE.md, last part).

**New files** (in `lean/LoopEquality/`; the files from the first proof are unchanged except `Axioms.lean`):

| File | Lines | Content |
|---|---|---|
| `ClosedWalks.lean` | 269 | `W_closed`: closed walks at every atom of every stacking = `closedWalks i` (0 for odd i; Σ_a C(n,a)² H(a) for i = 2n). `chain_eq_domb_small`: equals Domb's closed form for n < 10 |
| `LocalFormula.lean` | 218 | `cA`, `A_eq_sum` (non-backtracking walks as explicit combinations of walks); `nbD`, `FD`, `F_eq_FD`, `FD_sum`; `sum_F_eq`, the local loop formula for graphs with q + 1 neighbours and equal closed-walk counts |
| `Explicit.lean` | 80 | `loopCount`, `loop_count_eq`, `loopCount_values`, `loopCount_values_34`, `iharaBass`, `loopCount_eq_iharaBass_small` (m ≤ 12), `closedWalks_domb_small` |
| `Fibonacci.lean` | 303 | `fibonacci`, `fibonacci_isStacking`, `fibonacci_layer_type`, `isH_eq_word` (k < 100), `isH_not_periodic`, `fibonacci_not_periodic`, `fibonacci_loop_equality` |
| `Axioms.lean` | 23 | `#print axioms` for the 15 theorems |
| `../SphereLoops.lean` | 50 | companion statement only (#102 Corollary 3, proof `sorry`; not in the library) |

**Correspondence notes:** `loop-equality-outline.md`, Section 7. **Companions:** `COMPANIONS.md`.

**What is not formalised:**
- the Ihara–Bass series for all m (checked for m ≤ 12);
- Bala's identity, chain form = Domb's closed form, for all n (checked for n < 10);
- the equality of the cut-and-project and substitution forms of the Fibonacci word at every position (checked for k < 100; this is the classical Sturmian characterisation).

**Milestone log (15 November 2026).** Quick checks used `lake env lean` on the compute host; the full build ran through the job wrapper. Lean v4.35.0-rc2, Mathlib v4.35.0-rc2.

| Milestone | Content |
|---|---|
| (b1) | `ClosedWalks.lean` compiles: `W_closed` (#102 Proposition, closed walks in chain form) |
| (b2) | `LocalFormula.lean` compiles: `sum_F_eq` (Lemma 3 summed over the bonds, linear in the walk data) |
| (b3) | `Explicit.lean` compiles: `loop_count_eq`; #102's 15 values by `decide` and `decide +kernel`; Ihara–Bass coefficients agree for m ≤ 12. Control: a deliberately wrong value (`loopCount 24 = 750276793`) is rejected |
| (f) | `Fibonacci.lean` compiles: stacking, Jagodzinski types, word check, aperiodicity, loop corollary |
| (g) | full clean rebuild of the `LoopEquality` library (job `loop-explicit-lean`): "Build completed successfully (8942 jobs)". Negative control: no `sorry` or `native_decide` in the sources. Positive control: 15 axiom lines, all `[propext, Classical.choice, Quot.sound]`. **FINAL ok** |
| (c) | `SphereLoops.lean` (#102 Corollary 3 statement) typechecks with `sorry` |

## Palomar entry packaged and scored (15 November 2026)

DICTO (15 Nov): "move forward with Palomar, if score guaranteed". **Nothing submitted, and no repository created or pushed.**

- **Package:** `entry/` (text files; the build cache is not included). One Comparator configuration with 17 theorems. `Solution.lean` is the Challenge with proofs, transferred from the library (namespace `LoopEqualityProof`).
- **Preflight:** `PREFLIGHT.md`. `lake comparator` accepts the Solution: Lean kernel, NanoDa and con-ron. The axioms are the three standard ones, and a wrong Challenge is rejected.
- **Score:** `SCORE.md`, with the blind replay in `replay-review.json`. **Notability 3 out of 5, below the floor, so the outcome would be `rejected`.** The condition "score guaranteed" is not met, and the entry stays local.

## Version (Palomar-ready) (16 November 2026)

Palomar now requires every committed Lean file of a submitted repository to use the module system (`module` first, module doc comments after it), with at most 10,000 physical lines per file and the Challenge within 1,000 lines and 100 KiB. DICTO approved making the work ready in this repository (16 Nov: "count them and do whichever fits").

- **Module form.** All 29 Lean files of this study, `entry/` (14) and the workspace `lean/` (15), already start with `module` and use `public import` and `@[expose] public section`, so no file changed. The longest file has well under 10,000 lines; `entry/Challenge.lean` has 363 lines and 15,825 bytes.
- **Rebuild from the repository copies (job ymod-small2, FINAL ok).** `entry/`: Palomar's source check passes; the clean `lake build` completes (8,947 jobs); the comparator accepts the solution with con-ron (4 workers), NanoDa and Lean's kernel ("Your solution is okay!"). `lean/`: the library `LoopEquality.*` builds clean (8,942 jobs); `LoopEquality.lean` (2 `sorry`, the statement), `OctahedralNesting.lean` (4 `sorry`, the statement), `SphereLoops.lean` (1 `sorry`, the statement) and `OctahedralNestingProof.lean` typecheck, and the four proved theorems depend only on `propext`, `Classical.choice` and `Quot.sound`.
- **Whole repository.** `scripts/palomar_source_check.py` (repository root) checks every committed `.lean` file against these rules; it ends FINAL ok.
- Nothing was submitted, and no workflow or runner was added.

## 28 Nov 2026: a paper with all the Lean mathematics (DICTO: "3... we do a paper anyway with all the lean math"; 1 and 2 yes)
Paper regardless of the Palomar score; Palomar only if an honest re-score reaches 4. Content: #102 Theorem 1 (formal, done) + Theorem 5's
local laws: Theorem A (twist bijection, all lengths) and the l = 18 law via Theorem B with its finite tables (plan:
studies/2026-11-15-polygon-bijection §7: parts 1-4 about 2,900-5,000 lines; l = 18 tables (1038 arcs, 7713 meeting pairs) plausible for
kernel decide as checked certificates; l = 20 beyond the kernel without native_decide, so stated as checked, not formal). Others' work
(Thorpe 1972, Herrero 2014, Joyce/Guttmann, Nagle, Grigorchuk-Zuk, Lenz-Pogorzelski-Schmidt, Guttmann-Jensen) enters as credited
literature; Guttmann-Jensen's absolute diamond counts enter as a stated hypothesis. Milestones, each self-contained:
 M1 plane lattice, Gamma+, Tog, Lemma 1 (flip = twist of the far half), Lemma 2.   M2 cut lemma, arcs, Theorem A.
 M3 product structure and Theorem B.   M4 six-crossing vanishing, reach lemma.   M5 l = 18 tables by decide.   Then the paper.

### Open questions drawn from others' work (DICTO 28 Nov: "we can phrase some of others work as asked or open questions")
Candidates for the paper's last section; each to be checked against its source before it is printed (stated exactly, credited):
 Q1 (Herrero 2014): open self-avoiding walks on ice Ih and Ic differ from length 15. Is there an exact local law for open walks, as
    Theorem B gives for polygons?
 Q2 (Benito et al. 2023): self-avoiding walks on hcp and fcc differ beyond some length. Does a twist argument give the sphere-packing law?
 Q3 (Nagle's ice series; #102 v5: first difference at 16 bonds): does the local law determine the residual-entropy difference between
    ice Ih and Ic to all orders?
 Q4 (Guttmann-Jensen 2009): can diamond's polygon counts, the constants of Theorem 5, be certified formally?
 Q5 (Joyce; Guttmann 2010): the escape probability is the same at every site of every stacking (Theorem 1); can Joyce's closed form for
    diamond's Green function be formalised?
 Q6 (Grigorchuk-Zuk 2004; Lenz-Pogorzelski-Schmidt 2019): the per-site Ihara zeta function is the same at every site of every stacking;
    which of their analytic results for infinite graphs (radius of convergence, spectral bounds) then hold uniformly over all stackings?
 Q7 (Xu, Lin and Zhang, as in #102): the open question on S_h and S_c, which #102 does not decide.
Refined (DICTO 28 Nov: "some of those questions though closed will not have been formalized in Lean"): three kinds, stated as such.
 (a) Closed and now formalised here: Thorpe 1972 (closed-walk equality on periodic polytypes, the periodic case of Theorem 1; confirm
     the closed-walk theorem name in the package before saying so); the rooted Hashimoto-Bass local formula as used.
 (b) Closed, not formalised (the formalisation is the open part): Guttmann-Jensen's diamond polygon counts (Q4); Joyce's closed form for
     diamond's Green function (Q5); Herrero's and Benito et al.'s enumerations (the counts of Q1, Q2); the infinite-graph zeta results
     of Grigorchuk-Zuk and Lenz-Pogorzelski-Schmidt for each stacking (Q6).
 (c) Open mathematics: local laws for open walks (Q1, Q2); Nagle's entropy difference to all orders (Q3); uniform statements over all
     stackings (Q6, beyond what Theorem 1 gives at once); Xu-Lin-Zhang (Q7).
 (d) (DICTO 28 Nov: "and truly still open questions"): long-standing problems open in the literature itself, which our setting touches
     but does not claim to close. Candidates, each to be confirmed open from a current source before printing: the exact connective
     constant of the diamond lattice (known exactly only for the honeycomb, Duminil-Copin and Smirnov); the exact residual entropy of
     ice (Pauling's estimate, Nagle's series; no closed form); Xu-Lin-Zhang's question on S_h and S_c (moved here from (c)).
     (c) keeps only the new questions our own results raise (Q1-Q3 laws, Q6 uniform statements).

### Milestone 1 DONE (28 Nov 2026): one flip is one twist (lean/LoopEquality/Twist.lean, 230 lines)
Built in the entry workspace (Lean v4.35.0-rc2, Mathlib v4.35.0-rc2): `lake build LoopEquality.Twist` completed, no errors, no
warnings; axioms of every main theorem: propext, Classical.choice, Quot.sound only. Proved: `flipAt_isStacking` (the flipped
stacking is a stacking), `flipAt_hex` (the c/h letter changes at bilayer k and nowhere else), `flip_is_twist` (Lemma 1: the half-turn
p -> c - p of the far half, c = 2 sigma(k) mod 3, carries sites onto sites of the flipped network, fixes the root half, and within each
half preserves bonds and non-bonds), `halfturn_two_points` (Lemma 2). Uses the published definitions (namespace LoopEqualityProof).
The file sits in the entry workspace as an extra module only; the Palomar entry's own files are unchanged.
Next: Milestone 2 (cut lemma: the vertical bonds of bilayer k are the only bonds between the halves; arcs, crossing sets; Theorem A).

### Milestone 2 DONE (28 Nov 2026): the cut, the surgery and Theorem A for at most two crossings
Files (built, no errors or warnings; axioms propext, Classical.choice, Quot.sound only):
- Surgery.lean (2a): `bond_symm`; the cut lemma `cut` (a far-root bond is the vertical bond of bilayer k); `crossing_bond_flip`;
  the surgery `surg` on ordered edges with `surg_bond_iff` (bonds before iff after) and `surg_surg`.
- Polygons.lean (2c part 1, replaces the ordered-edge Degrees.lean of 2b): the surgery `surgS` on unordered edges (`Sym2 Atom`),
  `degS_surg_root`, `degS_surg_far` (degrees kept when the half-turn keeps the crossing edges).
- TheoremA.lean (2c part 2): polygon = minimal nonempty closed (even-degree) set of bonds; `even_card_cross` (parity: a closed
  loopless edge set crosses the cut an even number of times); `surgery_polygon` (Theorem A for polygons crossing bilayer k at most
  twice: the surgered set is a polygon of the flipped network, same number of edges, same crossing edges).
Scope (stated exactly): the formal Theorem A is the n <= 2 case, which is all that Corollary A1 uses; the n = 4 symmetric cases
(parallelogram, toggle mirror) of the paper are not formalised.
Milestone 2d DONE (28 Nov): `bijOn_surgery` (Corollary A1 at one flip: for a set S of at most two crossing edges kept by the
G (flipAt sigma k), and equal counts for every length and crossing profile).
  half-turn and v in the root half, the surgery is a bijection between the polygons through v with crossing edges S in G sigma and in
  G (flipAt sigma k), keeping the number of edges) and `bijOn_two_crossings` (S = the vertical bonds at p != q, centre p + q by
  Lemma 2). Built, standard axioms only. The case S = {} (no crossing) is `bijOn_surgery` with any centre c = 2 sigma(k).
Next: Milestone 2e: all bilayers at once (Corollary A1 in full: change the letters one at a time; a polygon of length l meets only
finitely many bilayers, #102 Lemma 4) -- then Milestone 3 (Theorem B).
Milestone 2e DONE (28 Nov): CorollaryA1.lean. `ncard_polysA1_flip`: for an atom v in the root half of bilayer k and every length l,
G sigma and G (flipAt sigma k) have the same number of polygons through v with l edges crossing every bilayer at most twice. The
half-turn centre is read from each polygon's own crossing set (`centreOf`: p + q for the vertical bonds at p != q; polygons not crossing
k are unchanged); `crossN_surg` (the surgery keeps the crossing number at every bilayer); `cross_eq_vert`; `flipMap_flipMap`. Built,
standard axioms only. Counts as Set.ncard (equal also when infinite; finiteness is not needed for the equality).
Next: Milestone 2f: from one flip to every stacking (flips below v by the mirror k -> -k; finitely many flips; locality).
Milestone 2f-1 DONE (28 Nov): Relabel.lean. `ncard_polysA1_relabel` (the whole-network half-turn p -> c - p, c = 2a, maps G sigma
at v onto G (tog a o sigma) at htA c v: equal counts); `ncard_polysA1_mirror` (bilayer j -> -j with lower/upper exchanged: equal
counts); `ncard_polysA1_flipBelow` (a flip below v keeps the counts at v: mirror + the flip above, `mirS_flipBelow`). Built, no sorry,
standard axioms only. (A first attempt via relabelling alone did not close; replaced by the mirror before any build was claimed.)
Next: 2f-2 (any finite run of c/h flips keeps the counts; stackings with the same c/h word near v) and 2f-3 (locality).
Milestone 2f-2 DONE (28 Nov): FlipRuns.lean. `flipFor v sigma k` flips the c/h letter of bilayer k keeping the positions on v's
side (above by flipAt when v is in the root half, below by flipBelow otherwise); `flipBelow_hex`, `flipFor_hex` (the c/h letter
changes at k only); `ncard_polysA1_flipRun` (any finite run of such flips keeps the counts at v, every length); `flipRun_hex` (after a
run, the letter at j is sigma's flipped once per occurrence of j). Built, no sorry, standard axioms only.
Next: 2f-3, locality (a polygon of length l through v stays within bilayers |j - v.1| <= l; stackings agreeing there have the same
polygons), which together with 2f-2 gives Corollary A1 for every stacking.
Milestone 2f-3 DONE (28 Nov): Locality.lean. `must_cross` (a polygon through v that reaches the far side of a cut with v on the root
side crosses it, by minimality); `reach_bound`, `reach_bound_below` (every atom of a polygon through v with l edges lies within
bilayers v.1 - l - 1 .. v.1 + l + 1; different cuts are crossed by different edges); `polysA1_local` (stackings agreeing on those
bilayers have exactly the same polygons). Built, no sorry, standard axioms only.
Next: 2f-4, the assembly: Corollary A1 for every pair of stackings with v a site of both (flip run on the window from 2f-2, locality,
a relabel fixing v's letter when the next letter differs, and a lattice translation).
Milestone 2f-4 DONE (28 Nov): Assembly.lean. Lattice translations (`ncard_polysA1_translate`); positions from the c/h word
(`eq_up`, `eq_down`, `eq_window`); `flipRun_at_v`; and **`corollaryA1`: for any two stackings sigma, tau and any atom v that is a site
of both, and every l, the polygons through v with l edges crossing every bilayer at most twice are equally many** (flip the differing
c/h letters on the window, relabel by tog of v's letter if the next letter differs, translate back to v, locality). Built
(lake build LoopEquality.Assembly, 8940 jobs), no sorry in any file, axioms propext, Classical.choice, Quot.sound only.
MILESTONE 2 COMPLETE. Scope, stated exactly: the count is over all such polygons (every bilayer crossed at most twice), not split by
crossing profile; the n = 4 symmetric cases of Theorem A are not formalised.
Next: Milestone 3, Theorem B (the exact local formula for the rest: product structure, symmetrisation, locality f = all - bad).

### Milestone 3 design (28 Nov): Theorem B in Lean
Theorem B (study 2026-11-15-polygon-bijection §3): p_l(v; G') - p_l(v; G) = -1/2 sum A_w A_f. Formal route, each step built and committed:
- 3a Linkages: `LAdj L a b := s(a,b) in L and a != b`; `Conn L := ReflTransGen (LAdj L)`; `IsLinkage L B` (ends B of degree 1, other
  atoms degree 0 or 2, no nonempty closed subset, no loops); the PATH LEMMA: in a linkage each end is connected to exactly one other
  end (degree <= 2 and acyclic => components are paths). Mathlib has Reachable / ReflTransGen but, as far as found, not this lemma: it
  is the main new work of Milestone 3.
- 3b Product structure: a polygon crossing k at the points S is a root linkage plus a far linkage with ends at S whose pairings join
  into one cycle on S, and conversely (both directions).
- 3c Flip transfer: by Lemma 1 the twist maps far linkages of G with ends gS and pairing gM onto far linkages of G' with ends S and
  pairing M (bijection, sizes kept).
- 3d Counting: finiteness of linkages of a given size near S (locality as in 2f-3), the translation-weighted root counts w, and the
  symmetrisation algebra -> Theorem B.
- 3e Locality of A: f = all - bad for n = 4 (needed before the l = 18 tables of Milestone 5).
Compute: all Lean checks and builds on the compute host (entry workspace), as for Milestones 1-2.

### Palomar-ready (28 Nov 2026; DICTO: "make sure all parts are engineered for running on Palomar register without further work")
The new modules now live in the entry itself (entry/LoopEquality/*.lean, the canonical copy; the duplicates under lean/ were removed)
and the entry carries the new theorem in Palomar's layout:
- Challenge.lean: plain definitions (edgeDeg, IsPolygon, IsAbove, Crosses, crossings, polysAtMostTwice) and `corollaryA1` with sorry;
  Solution.lean: the same definitions word for word, transfer lemmas, and the proof from `LoopEqualityProof.corollaryA1`;
  comparator.json: 18 theorems; formalization.yaml describes Corollary A.
- Preflight on the compute host (entry branch `stackings`, commits 60150fe, 4a9ce3b): source checker pass (module headers, file sizes);
  18 proof sorries in Challenge = 18 compared theorems; no sorry/native_decide in proofs (mentions only in comments); clean build
  8955 jobs; comparator (job palomar-loop-v2-comparator): con-ron accepted 17395 declarations (--verified), nanoda accepts, Lean
  kernel accepts, "Your solution is okay!"; negative control (job palomar-loop-v2-negctl): statement changed l -> l + 1 rejected
  ("Challenge and solution theorem statement do not match: 'DictoLoopEquality.corollaryA1'"), Challenge restored.
- Not run here (as on 15 Nov): Palomar's GitHub workflow itself (needs a public repository at a fixed commit), Ruby metadata validator.
Rule for every later milestone: each new theorem goes into the entry the same way (Challenge + Solution + comparator) and the
comparator plus a negative control are rerun before the milestone counts as done.
PUBLISHED (28 Nov 2026, DICTO "publish repository"): https://github.com/DICTOR-Master/loop-equality-lean (public), main = efd98a2
(the entry branch `stackings`: Theorem 1 + Corollary A, 18 compared theorems). History checked before publishing: authors "DICTO"
with a local placeholder address, no machine names, paths or personal e-mail. The compute-host repository keeps its old main
(26fc584) untouched; its branch `stackings` is what was published. Palomar submission itself is DICTO's (fixed commit efd98a2...).
Milestone 3a DONE (28 Nov): entry/LoopEquality/Linkage.lean. `handshake`; `partner_exists` (an end is joined to another end, by
parity); `compGraph` (the component as a connected Mathlib SimpleGraph), `degree_compGraph`, `ends_le_two` (a component holds at most
two ends, by Mathlib's Connected.card_vert_le_card_edgeSet_add_one), `partner_unique`. So in an edge set with degrees <= 2, each end
has exactly one partner: the pairing of a linkage is well defined. Built, standard axioms only.
Next: 3b product structure. After Theorem B: Milestone 4 (f = all - bad; six-crossing terms vanish to l = 20) and Milestone 5
(length-18 tables by kernel decide as certificates), each Palomar-ready (DICTO 28 Nov: "and length-18 milestones").
Milestone 3b part 1 DONE (28 Nov): entry/LoopEquality/Product.lean `all_edges_of_touched`, `propagate` (a subset with even degree at
every degree-2 atom of K contains all of a path of K once it contains one edge of it). Built, standard axioms.
3b part 2 NEEDS FIRST (found 28 Nov): `polygon_deg_le_two`: a minimal even edge set (our IsPolygon) has every degree <= 2. Standard
(a circuit is a cycle) but not yet proved. Route: if deg_E x >= 4, take e = s(x,y) in E; in E \ {e}, x and y are joined (parity, as in
`partner_exists`); a Mathlib walk between them -> `Walk.bypass` (a path, `bypass_isPath`) -> cycle `cons e path`; its edge set F is
even (`Walk.IsTrail.even_countP_edges_iff` with u = v) and has degree 2 at x (path endpoint: `neighborSet_toSubgraph_endpoint`), so
F is a proper even subset of E: contradiction. Bridge needed: Walk.edges (nodup for trails) <-> our Finset (Sym2 Atom) and degS.
Then 3b part 2: polygon -> (root part, far part) are linkages ending at the crossing points, and no proper set of crossing points is
closed under both pairings (else the paths through it + their vertical bonds form a smaller closed set); 3b part 3: the converse by
`propagate` (a closed subset contains a whole path once it meets it, hence closes up a set of crossing points under both pairings).
Better route for `polygon_deg_le_two` (chosen 28 Nov; avoids counting at a vertex of a walk): E minimal even, e = s(x,y) in E,
E' = E \ {e}. (1) x, y joined in E' (parity). (2) K := (edges of E' inside the component of x) + e is even and inside E, so K = E:
E' is connected on the atoms of E. (3) E' has no cycle: a Mathlib cycle walk in it gives an even nonempty edge set (via
`Walk.IsTrail.even_countP_edges_iff`, edges nodup) strictly inside E. (4) So E' is a tree on the atoms of E: |E'| = |V| - 1
(`IsTree.card_edgeFinset`), |E| = |V|. (5) Handshake: degrees >= 2 summing to 2|V| are all 2.

## READINESS COUNTDOWN (DICTO 28 Nov: "count down readiness as we go ... till Palomar paper is fully ready with all requirements")
Done on 28 Nov: Corollary A in the entry; finiteness (`polysAtMostTwice_finite`); every site counts the same
(`corollaryA_everySite`, vs diamond's site); 20 compared theorems; comparator accepted (con-ron 17,765 declarations, nanoda, Lean);
negative controls rejected; repository public.
Remaining (22), struck off as they pass:
Lean / Palomar entry: 1 degree lemma `polygon_deg_le_two` · 2 product structure (3b) · 3 flip transfer (3c) · 4 counting and
Theorem B (3d) · 5 Theorem B in the entry (Challenge/Solution/comparator + negative control) · 6 Corollary A profile by profile ·
7 non-emptiness witness (a hexagon at l = 6) · 8 Challenge header, results list, naming, #102 Version 6 source · 9 README and
formalization.yaml for all theorems; new public commit · 10 length-18 law (Milestones 4, 5) · 11 notability re-score.
Paper #125: 12 title (DICTO) · 13 Theorem B section · 14 two figures · 15 correlation table and OEIS trail · 16 compared vs library
statements; Fable wording fixes · 17 general OEIS acknowledgement · 18 Thorpe "first formal proof" check · 19 open problems confirmed
open · 20 Benito et al. opened · 21 second Fable attack after Theorem B · 22 DICTO's final read ok (then Zenodo release; Palomar
submission is DICTO's).
Item 1 DONE (28 Nov): entry/LoopEquality/Degree.lean `polygon_deg_le_two` (tree route), built, standard axioms. Countdown 21.
Item 2 (product structure) formal shape: `IsLinkageOn L B` (degree 1 on B, 0 or 2 elsewhere, no nonempty closed subset, no loops);
`SingleCycle P R F` (no nonempty proper Q of crossing points closed under both pairings Conn R (low p) (low q), Conn F (up p) (up q));
`parts_to_polygon` (root linkage + vertical bonds + far linkage + SingleCycle = polygon; proof by `propagate`) and `polygon_to_parts`.
Item 2 DONE (28 Nov): Parts.lean `parts_to_polygon`, `polygon_to_parts` (both directions of the product structure), whole library
builds, standard axioms. Countdown 20 (items 18-20 literature checks also done: papers/2026-11-28-loop-equality-lean/literature-checks).
Item 3 DONE (28 Nov): Transfer.lean flip_transfer (involution lemmas linkage_image, conn_image), built, standard axioms. Countdown 16.
Item 4 design (28 Nov, decision 1 given to DICTO): Theorem B in Lean in PER-SITE form: for v on the root side of k, polygons of G'
through v = sum over crossing sets S (finite: inside box v (2l)), pairings M, M' (single cycle) of w_v(S, M) * f(c - S, c - M'),
w_v = root linkages of G through v, f = far linkages of G (flip transfer). Then Delta = -1/2 sum A_w A_f by finite-sum algebra.
Equivalent to the paper's translate-weighted form; the paper will quote the Lean form.
Step 4a: root bonds unchanged by the flip (`bond_root_flip`).
DICTO 28 Nov on decision 1: "lets do it your way first and by sites if further proof is required after next attack" -> per-site
form now; revisit after the second Fable attack.
Item 4 progress: Counting.lean `ncard_polysCross` (product structure as a count), `ncard_partsCross_flip`, `theoremB_count`
(polygons of the flipped stacking crossing at P = pairs of G-parts with far ends at c - P, half-turned far part closing one cycle),
built, standard axioms. Remaining for item 4: sum over P (finite, in the box) and the -1/2 sum A_w A_f algebra.
Item 12 DONE (28 Nov): title = option 1, DICTO: "1 with proviso of possible slight change later if prudent otherwise ok". Countdown 15.
Item 4 DONE (28 Nov): TheoremB.lean `theoremB` (flip formula: #polys(flipAt sigma k) = #polys(sigma) + sum over nonempty crossing
sets P in the window with vertical bonds of (#FlipParts - #PartsCross), all counted in G sigma), with ncard_polys_sum,
polysCross_empty_flip, root_of_no_cross. Built, standard axioms. The -1/2 sum A_w A_f symmetrisation is finite algebra on top, needed
only for the locality tables (item 10). Countdown 14.
Item 5 DONE (28 Nov): Theorem B in the entry (Challenge/Solution, comparator 21 theorems: con-ron, nanoda, Lean accept; negative control l -> l+1 rejected 'do not match: theoremB'). Countdown 13.
Item 7 DONE (28 Nov): Witness.lean hexagon through diamond's (0,(0,0),0), polysA1_diamond_six_pos; entry theorem polysAtMostTwice_diamond_six_pos (22 theorems): comparator accepts, negative control (6 -> 7) rejected. Countdown 12.
Item 8 DONE (28 Nov): Challenge header lists Corollary A, the witness and the flip formula, names them (Corollary A of #102; Theorem B), sources #125 (its DOI is written in at release, with item 9).
Paper items 13 (Theorem B section), 15 (correlation table + OEIS trail), 17 (OEIS acknowledgement) DONE (28 Nov); #102 v6 cited for Corollary A/Theorem B; draft PDF rebuilt. Countdown 8: Lean 6, 9, 10, 11; paper 14 figures, 16 library comparison (incl. A038515 factor), 21 second Fable, 22 read ok.
Item 6 DONE (28 Nov): every step generalised to a crossing condition Q (PolysQ); corollaryA_profile in the entry (23 theorems; con-ron accepted 18893 declarations; nanoda, Lean accept; negative control bound 2 -> 3 rejected). DICTO 28 Nov: full #102 §5 scope before release (new items: Theorem 8 per profile; -1/2 sum A A algebra; locality + Lemma 7; Theorem 5(a),(b) tables).
Countdown item 1 (Theorem 8 per profile) DONE 28 Nov: entry 24 theorems, con-ron 18903 declarations, negative control rejected.
Item 2 design (28 Nov): Theorem B, -1/2 sum A_w A_f form, per site. 2a pairR/pairF (relations on P from Conn R / Conn F),
OneCycleRel P M M' (SingleCycle iff OneCycleRel of the pairings). 2b linkages with r edges ending at P lie within 2r of P (finite).
2c #PartsCross = sum over M, M' (subsets of P x P), r + |P| + s = l, OneCycleRel: W(P,M,r) * Fc(P,M',s). 2d Fc in the flipped
stacking = Fc(c - P, c - M') before (flip_transfer). 2e symmetrisation over a g-invariant finite family of crossing sets.
Countdown item 2 (Theorem B in #102's form) DONE in library 28 Nov: Pairings.lean + BSym.lean theoremB_sym (2*Delta = - sum A_w A_f over a half-turn-closed family of crossing sets), built, standard axioms. Next: into the entry.
Item 2 in the entry 28 Nov: theoremB_symmetric (25 theorems; con-ron 19027 declarations; negative control 2* -> 3* rejected).
Item 3: Lemma7.lean term_zero_of_large (terms with 3|P| > l vanish: only |P| <= 6 for l <= 20), built, standard axioms. NOTE: per site, the 6-crossing terms vanish only after summing over translates of P when the 6-bond side is the root side (#102 weights the root side over translates); the far 6-bond side vanishes termwise.

## Theorem 5 plan (Fable review, 28 Nov; advisory, unmeasured timings)
Feasible. Shortcuts: (1) minimal-size lemma L5 (a side with s = |P| edges is all 2-bond arcs, unique and disjoint; A = 0 there;
gives Lemma 7) -> tables only to F <= l - 10: 48 meeting pairs (l = 16), 720 (l = 18), 7713 (l = 20), not 74,493; (2) one c/h
letter per half; (3) Delta = Y - X as a join of two short lists of meeting pairs (no table in the kernel). Transfer matrices /
generating functions NOT sound for self-avoiding polygons. Per-site sums need translation regrouping (L4) for the root weight.
Statement (b) as differences from diamond, no absolute constants: p18(v;sigma) + 12h(k-2) + 30h(k-1) + 42h(k) + 24h(k+1) =
p18(v0; diamond); p20: 30, 114, 204, 12. Diamond's 349236 / 2362200 only as a labelled hypothesis. Lemma list L0-L10 (~2500-3500
lines), milestones: M0 kernel pilot (Nat-coded half, arc search, meeting pairs, join; #eval vs halves.py, then decide +kernel timing)
-> M1 far flips (a) l <= 10 -> M2 single arcs, linkage = arcs, (a) l <= 12 -> M3 locality, regrouping, L5, (a) l <= 14, Lemma 7
-> M4 enumerators, (a) l <= 16 -> M5 l = 18 law -> M6 l = 20 law. Fallback if slow at l = 20: chunk, pack paths, 3-fold turn,
toggle identity; else release l <= 18 machine-checked, l = 20 checked outside Lean.
M0 PILOT (28 Nov): Nat-coded half (pilot/Pilot.lean in the entry workspace, not in the library) reproduces Python exactly (30/168 arcs, 384/5760 raw meeting triples); kernel decide: fmax 6 in 3 s, fmax 8 in 17 s (incl. ~1 s start). fmax 10 running.
M0 fmax 10: kernel 231 s (61704 raw triples) -> brute force feasible for all Theorem 5 tables. M1 DONE: Short.lean theorem5a_short (l <= 11: every site = diamond, all polygons), built, standard axioms.
Entry 26 theorems (theorem5a_short), con-ron 19043; pilot moved out of the entry to studies/.../pilot (it broke the source rules: 'must use the module header keyword'; caught by check-lean-sources, fixed same session).
M2 progress: Parity.lean theorem5a_odd (no polygon of odd length); SingleArc.lean Fc_two (two-point far counts unchanged by the half-turn: flip transfer about c, then about the midpoint). Built, standard axioms.
L5 (far, minimal size) design (28 Nov): with |F| = |Q| every edge holds exactly one end (end -> edge injective, card equal);
each non-end atom is a lower atom (k+1, m, 0) of degree 2 joined to two ends p, q (an arc p - m - q). Mid-swap m -> p + q - m
(the centre of the other triangle on p, q) maps minimal far linkages of tau onto those of any tau' with tau' k = tau k and
tau' (k+1) the other letter: so Fc_tau(Q, M, |Q|) = Fc_tau'(Q, M, |Q|); with fc_transfer: Af(P, N, |P|) = 0.
L5 far DONE: Minimal.lean Af_min (far asymmetry at size |P| is 0: middle-atom swap m -> p+q-m is a bijection of minimal far linkages between tau and flipAt tau k, then fc_transfer). Built, standard axioms.
Theorem 5 (a) at l = 12 DONE (theorem5a_12; Twelve.lean term_zero_12, flip_keeps_12; Theorem5.lean FlipLaw, corollaryFL). With theorem5a_short (<= 11) and theorem5a_odd: (a) holds for all l <= 13. Next: l = 14 (needs the root side at minimal size with translation regrouping, L4).
l = 14 plan (28 Nov): terms have |P| in {2, 4}; |P| = 2 vanish (Fc_two); |P| = 4 with sizes even (rootL_card_even, farL_card_even):
(6,4) vanish (Af_min); (4,6) root minimal: per site, cancel in pairs by an involution on (P, M, R) with v in R: half-turn about
v's own crossing point (v an end) or about the midpoint of v's arc (v a middle), then the middle swap; it fixes v and turns
A_f into -A_f (A_f antisymmetric under every good half-turn: far counts are translation-invariant). Steps: Fc translation
invariance; the root side through the mirror (root linkages of sigma at k = far linkages of the mirrored stacking at -k).
l = 14 progress (28 Nov): Pairing14.lean: farSet_htS, swapF_htS (swap commutes with the half-turn), pairMap (half-turn then
swap: lands in the half-turned set, involutive), count_sym (equal counts for conditions it keeps), cond_end, cond_mid, mirror
transport Wc_mir. Remaining for l = 14: (i) support: W(P,M)*Af != 0 -> P in the window (polygon); (ii) the arc at v is unique
(mid uniqueness: decide over shortVecs); (iii) Finset.sum_involution on (P, M) with centre 2 p0 (v an end) or p + q (v a middle);
(iv) flip_keeps_14, FlipLaw 14, theorem5a_14, entry.
Theorem 5 (a) at l = 14 DONE (28 Nov): Fourteen.lean. window_of_term (a non-zero term lives in the window: its parts close
into a polygon, of sigma or of the flipped stacking); minFar_finite; cenAt / cenSet (centre of the arc at v); Wc_cen (the
minimal root count through v split by centre, via the mirror); Wcen_g (count kept by the pairing map about that centre);
f14_g (each centre's part changes sign under its half-turn), f14_sum (Finset.sum_involution), term14 (every other term is 0),
sumWc_14, flip_keeps_14, theorem5a_of_law (the l = 12 assembly for any l), theorem5a_14, theorem5a_upto15.
Axioms: propext, Classical.choice, Quot.sound. Entry: theorem5a_upto13 -> theorem5a_upto15 (27 theorems); comparator v12
and negative control (l <= 15 -> l <= 16) running.
Comparator v12 (28 Nov): "Your solution is okay!", 19321 declarations, three kernels; negative control (l <= 15 -> l <= 16)
rejected ("do not match: theorem5a_upto15"). Next for l = 16: the minimal-root cancellation for any l (removes the (4, 8)
terms); the (6, 6) terms with |P| = 4 need locality (item 3) and the counting tables (item 4, 48 meeting pairs).
minRoot_zero DONE (28 Nov, MinRoot.lean): the minimal-root terms of Theorem B sum to zero at EVERY length (the l = 14 argument
for any l). At l = 16 only the (6, 6) terms with |P| = 4 remain; all such linkages are flat (two sublayers next to the cut).
l16/l16_terms.py (dbb): sum over P, M != N of W(P,M,6) * A_f(P,N,6) = 0 for all 4 letter patterns x 2 site kinds (FINAL ok);
60 / 36 (P, M) carry non-zero products that cancel only across translates of P (#102's weighted root side, probe16.py:
both asymmetries sit on one pairing per shape). First run had a bug of mine (disjoint 2-arc + 4-arc = 8 atoms, tested 7, so
it counted pairs meeting in one atom); found by comparing shape by shape with #102's probe16 (12 shapes, +-1 / -+5).
Lean route for l = 16: (i) A_f(P,N,6) = meet(gP,gN) - meet(P,N) (single-arc products are half-turn symmetric, Fc_two);
(ii) translation regrouping of the root count (atoms of v's kind on a 6-edge linkage: always 5 ends-sublayer, 3 lower);
(iii) support: A_f(S,N,6) != 0 only on the pairing of S that holds the meeting shape; root likewise via the mirror.
Items 2-3 (28 Nov): Split.lean (compPart / restPart of a linkage are linkages on the ends joined / not joined to x0, no common
atom; linkage_union joins atom-disjoint linkages; conn_union_left; conn_level_bound + farL_in_box: every atom of a linkage
lies within 2|L| of an end; farSet_finite). FourPoint.lean fc_four: far linkages on {a,b,c,d} paired a b | c d = pairs of
atom-disjoint arcs. Meet.lean: fc_four_meet (count = sum_i Fc(ab,i) Fc(cd,s-i) - #meeting pairs) and Af_four (far
asymmetry = #meeting pairs at gP - #meeting pairs at P, via Fc_two). Standard axioms.
Next: pairing relations of 4-end linkages are matchings; verified arc enumeration (arcs of length <= 4 for l = 16); the
root side by the mirror; regrouping over translates; the finite check.
Item 4, verified arc search (28 Nov): Path.lean (path_linkage: a simple path is an arc; arc_to_path: every arc is a simple
path; conn_two_ends; path_unique; fc_two_paths: Fc({a,b}, i) = number of simple far paths). Enum.lean (computable nbrs /
ext with mem_ext = exact specification, ext_nodup, fc_two_enum: arc counts are list lengths). Kernel test on diamond: 63 far
paths of 4 edges from an end atom, 24 of them arcs (= #102's 30 arcs of length <= 4 minus the 6 of length 2); decide ~3 s.
Next: meeting pairs and root counts through v from the enumeration; reduction of the sum over crossing sets to a finite
candidate list; normalisation of the stacking (only the letters near k matter) and of v; the l = 16 check by decide.
l = 16 assembly (28 Nov): Matching.lean (linkage_four, pairF_four: a 4-end linkage pairs its ends by a matching).
Regroup.lean: Wc_translate, Af_translate (lattice translations), class normalisation nrm by coordinate sum (shift,
nrm_trP, shift_nrm), regroup: sum over crossing sets of G v = sum over class representatives S and lattice translates of v
(G invariant under joint translation). Next: G for l = 16 and its invariance; Z = normalised meeting shapes from the arc
enumeration with a completeness proof; T(S); stacking normalisation; decide.
Full local preflight v12 (28 Nov): clean build, source rules, 0 sorry/native_decide, 27 compared theorems all with standard
axioms, comparator ok on con-ron / nanoda / Lean kernels, metadata parses, git clean: FINAL ok. Entry README and
formalization.yaml updated to 27 theorems and Theorem 5 (a) to l = 15 (l = 16 and the laws at 18, 20 listed as not formalised).
l = 16 (28 Nov, cont.): Sixteen.lean (G16, G16_translate, bonds_of_Wc, G16_support, term16, sumWc_16_iff: the change at
l = 16 is minus the sum of the (6,6) terms; T16, near_of_Wc, mem_T16, sum16_regroup). FourPoint.fc_four_pred. PathPairs.lean
(arcList, ncard_arcPairs_cond: arc pairs with an atom condition = filtered products of enumerated path lists). Counts.lean
(meetCountL, throughCountL; ncard_meetPairs, Wc_four via the mirror, Af_four_enum). Mt.lean (the three matchings; root and far
pairings carrying linkages are matchings; G16_mt). Remaining: the shape list Z with completeness, stacking normalisation,
the kernel check.
