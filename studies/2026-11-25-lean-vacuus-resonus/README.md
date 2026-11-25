# Lean: the polar link, Aequus = equal fin regions, and the factor 3 (25 Nov 2026)

DICTO · Lean 4 formalisation of three short results of the Vacuus–Resonus–Aequus project, with Claude (Anthropic).

> **Status box.** Study note, not published. All three milestones build with Lean 4 `v4.35.0-rc2` and Mathlib `v4.35.0-rc2`:
> no `sorry`, no `native_decide`, and every theorem listed below depends only on the standard axioms
> `[propext, Classical.choice, Quot.sound]` (`logs/build-ALL.log`, `FINAL ok`). 504 lines of Lean. Resume: everything committed;
> nothing running.

**Conclusion.**
1. **Polar link (M1, formalised).** The Resonus plane of the facet plane a·x = 1 is the orthogonal complement of the line from O to
   the polar corner a. In 3-space, the Vacuus plate through O and an edge [u, v] lying on the facet planes a·x = 1 and b·x = 1 is the
   orthogonal complement of the polar edge direction a − b.
2. **Aequus = equal fin regions (M2, formalised, measure-theoretic).** For a die (unit distinct face normals not in one closed
   hemisphere, positive face distances), the radial projection of each face to the unit sphere has Mathlib surface measure equal to the
   solid angle of the face. The projections cover the sphere, two distinct ones overlap in a null set, and the areas sum to 4π. Hence
   all faces have equal solid angle ⇔ all fin regions have equal area ⇔ every fin region has area 4π/N (fair).
3. **The factor 3 (M3, formalised).** φ^k ≠ 3 for every integer k. Stronger, and what gap (b) needs: if φ²r² = 3 then r ≠ q·φ^k
   for every rational q and integer k, so no φ-step (even rescaled by a rational) reaches the station-die depth ratio √3/φ.

4. **Lattice webs (M4, formalised, 25 Nov).** `VacuusResonus/LatticeWebs.lean`, `logs/build-M4.log` (`FINAL ok`, standard axioms only).
   For a convex, centrally symmetric cell P with interior points, a nonzero functional f and h the least upper bound of f on P:
   `plane_meets_interior_iff` (the plane f x = t meets the interior of P iff |t| < h); `plane_meets_cell_iff` (the copy through λ meets
   the interior of the cell P + μ iff |f(λ − μ)| < h); `web_iff` (Theorem 0 of the lattice-webs study: every copy meeting a cell's
   interior is that cell's own central plane iff every lattice vector ν has f ν = 0 or h ≤ |f ν|), in any finite dimension.
   Concrete: `cube_resonus_web` (ℤ³, eᵢ, h = 1/2), `cube_vacuus_web` (ℤ³, eᵢ ± eⱼ, h = 1), `rd_web` (D₃, eᵢ ± eⱼ, h = 1),
   `same_web` (for eᵢ ± eⱼ both lattices give the planes f x ∈ ℤ). Not formalised: that these normals are exactly the cube's and the
   rhombic dodecahedron's Vacuus and Resonus planes (taken from the catalogue study), and the families that break.

## Files and build

- `VacuusResonus/PolarLink.lean` (M1), `VacuusResonus/Fins.lean` (M2), `VacuusResonus/GoldenThree.lean` (M3), `VacuusResonus/LatticeWebs.lean` (M4); root `VacuusResonus.lean`.
- `check.sh TAG MODULE thm…`: builds the module, prints `#print axioms` for each theorem, counts `sorry`/`admit`/`axiom`/
  `native_decide`, and writes `FINAL ok` only if the build succeeded, there is no warning or error, every axiom list is the standard
  one, and the count is 0.
- Built on the compute host, not on this machine: `rsync -a ./ <host>:lean/vacuus-resonus/`, Mathlib packages hard-linked from the
  rolling-law study's checkout of the same revision, then `check.sh` over ssh (each build under 30 s, so no long-job wrapper was needed).

**Build log.**

| milestone | log | result |
|---|---|---|
| M1 polar link | `logs/build-M1.log` | built at the 2nd attempt (deprecated name; an instance `Fact (finrank = n + 1)` needed `n := 2`). `FINAL ok` |
| M3 factor 3 | `logs/build-M3.log` | 3rd attempt (the φ notation needs `open scoped goldenRatio`; `√3` irrational via `Nat.Prime.irrational_sqrt`; exponent rewrite). `FINAL ok` |
| M2 fin regions | `logs/build-M2.log` | 3rd attempt (`Pointwise` scope; plane-volume lemma); `aequus_iff_isFair` then added and built first time. `FINAL ok` |
| all | `logs/build-ALL.log` | whole library, 18 theorems' axioms printed. `FINAL ok` |

## M1. The polar link (source: study 2026-11-24-resonus, Theorem 1)

Setting: a real inner-product space `E` for (a), Euclidean 3-space `E3 = EuclideanSpace ℝ (Fin 3)` for (b). A facet of P lies on
`facetPlane a = {x | ⟪a, x⟫ = 1}` (O = 0 inside P makes this normalisation possible); `polar P = {y | ∀ x ∈ P, ⟪y, x⟫ ≤ 1}`.

- `mem_polar : (∀ x ∈ P, ⟪a, x⟫ ≤ 1) → a ∈ polar P` — the facet vector lies in P\*.
- `resonusPlane a := {v | ∀ p ∈ facetPlane a, p + v ∈ facetPlane a}` — the plane through O parallel to the facet plane (its
  translation directions).
- `resonusPlane_eq (ha : a ≠ 0) : resonusPlane a = {x | ⟪a, x⟫ = 0}` and
  `resonusPlane_eq_orthogonal (ha : a ≠ 0) : resonusPlane a = ((ℝ ∙ a)ᗮ : Submodule ℝ E)` — **Theorem 1 (a)**.
- `vacuusPlate u v := Submodule.span ℝ {u, v}` — the plane through O and the edge; `segment_subset_vacuusPlate` — it contains the edge.
- `vacuusPlate_eq (hab : a ≠ b) (huv : u ≠ v) (hua : ⟪a, u⟫ = 1) (hva : ⟪a, v⟫ = 1) (hub : ⟪b, u⟫ = 1) (hvb : ⟪b, v⟫ = 1) :
  vacuusPlate u v = (ℝ ∙ (a - b))ᗮ` — **Theorem 1 (b)**.

*Maps to the paper statement:* (a) is exactly "the Resonus plane of F is {a_F·x = 0}, at right angles to O→a_F". (b) is "the Vacuus
plate of F∩G is {(a_F − a_G)·x = 0}, at right angles to the polar edge [a_F, a_G]" for d = 3, where the ridge is an edge [u, v]. The
proof that u, v are linearly independent (they lie on a·x = 1, which misses O) is the paper's "O and R span exactly one hyperplane".
*Not formalised:* that a_F is a vertex and [a_F, a_G] an edge of P\* (face duality, Ziegler Thm 2.11); this is input, not part of the
claim. The general-d ridge version is not formalised (only d = 3, the paper's case).

## M2. Aequus = equal fin regions (source: study 2026-11-25-one-structure, Theorem A1 (a))

Setting, copied from the Lean Alexandrov study (2026-11-22-lean-alexandrov, `Alexandrov/Dice.lean`, the same definitions verbatim):
face normals `n : Fin N → E3`, distances `d : Fin N → ℝ`, `die n d = {x | ∀ j, ⟪n j, x⟫ ≤ d j}`,
`face n d k = die n d ∩ {x | ⟪n k, x⟫ = d k}`, `faceCone n d k = {x | ∃ t > 0, t • x ∈ die n d ∧ ⟪n k, t • x⟫ = d k}`,
`solidAngle n d k = 3 * volume (faceCone n d k ∩ ball 0 1)`, `IsFair n d = ∀ k, solidAngle n d k = ofReal (4π / N)`. The hypotheses
are `hn : ∀ i, ‖n i‖ = 1`, `hinj : Injective n`, `hspan : ∀ x ≠ 0, ∃ i, 0 < ⟪n i, x⟫` (so the die is bounded with O inside),
`hd : ∀ j, 0 < d j`.

- `finRegion n d k : Set (sphere 0 1) := {u | ∃ t > 0, t • u ∈ face n d k}` — the radial projection of face k to the unit sphere,
  i.e. the region the fins cut out over face k.
- `toSphere_finRegion hspan hd k : volume.toSphere (finRegion n d k) = solidAngle n d k` — area of the fin region = solid angle
  (`volume.toSphere` is Mathlib's surface measure on the sphere, `Measure.toSphere`).
- `iUnion_finRegion hspan hd : ⋃ k, finRegion n d k = univ` — the regions cover the sphere.
- `finRegion_inter_subset` — two regions meet only on the great circle `⟪d k • n j − d j • n k, x⟫ = 0` (the plane through O and
  the common edge); `toSphere_finRegion_inter hn hinj hspan hd (hjk : j ≠ k) : volume.toSphere (finRegion j ∩ finRegion k) = 0`.
- `toSphere_univ : volume.toSphere univ = ofReal (4π)`; `sum_toSphere_finRegion : ∑ k, volume.toSphere (finRegion n d k) = ofReal (4π)`.
- `aequus_iff_finRegions hspan hd : (∀ j k, solidAngle j = solidAngle k) ↔ ∀ j k, toSphere (finRegion j) = toSphere (finRegion k)`.
- `isFair_iff_finRegions hspan hd : IsFair n d ↔ ∀ k, toSphere (finRegion n d k) = ofReal (4π / N)`.
- `aequus_iff_isFair [NeZero N] hn hinj hspan hd : (∀ j k, solidAngle j = solidAngle k) ↔ IsFair n d`.

*Maps to the paper statement:* A1 (a) says "S \ Γ has exactly F components, one per face, namely π(relint f), with area Ω_f; hence P is
an Aequus about O ⇔ all fin regions have equal area (each then 4π/F)". Formalised: the regions as the closed projections π(f), their
area Ω_f, their covering of S, null pairwise overlaps (so they partition S up to boundaries), the equivalence, and the value 4π/F.
*Not formalised:* that the open regions π(relint f) are exactly the connected components of S \ Γ (topology). In the paper, π(f) \ π(relint f) lies in Γ,
which has area 0, so the two readings give the same areas; that step is also not formalised. A1 (b) (O on the boundary) and (c) are
not formalised. The die is given by its face planes; that every face plane carries a face of positive area is not assumed or needed.

## M3. The factor 3 (source: study 2026-11-25-stellation-cycle, gap (b); Theorem 8)

Gap (b) states that Double Vision's factor 3 cannot be closed by φ-steps, and Theorem 8 gives the depth ratio r = d(B)/d(S) = √3/φ of
the 41 three-fold station dice, i.e. φ²r² = 3; `scripts/factor3.py` there tested r² = 3φ^k and φ^k/3 numerically for |k| ≤ 12.
With `φ = Real.goldenRatio = (1 + √5)/2`:

- `goldenRatio_zpow_irrational {k : ℤ} (hk : k ≠ 0) : Irrational (φ ^ k)` — via φ^(n+1) = F(n+1)·φ + F(n) and the irrationality of φ.
- `goldenRatio_zpow_ne_three (k : ℤ) : φ ^ k ≠ 3`.
- `three_eq_rat_mul_zpow_iff (q : ℚ) (k : ℤ) : (3 : ℝ) = q * φ ^ k ↔ k = 0 ∧ q = 3`.
- `ratio_ne_rat_mul_zpow (hr : φ ^ 2 * r ^ 2 = 3) (q : ℚ) (k : ℤ) : r ≠ q * φ ^ k` — **gap (b)**.
- `ratio_ne_zpow (hr) (k) : r ≠ φ ^ k` and `ratio_sq_ne_zpow (hr) (k) : r ^ 2 ≠ φ ^ k` (the form `factor3.py` tested, now for all k).

*Maps to the paper statement:* "3 ≠ φ^k for every k" is `goldenRatio_zpow_ne_three` (for all k, including k = 0 trivially). The step
gap (b) uses, that the ratio √3/φ is no φ-step, is `ratio_ne_zpow`; `ratio_ne_rat_mul_zpow` is stronger: no rational rescaling of a
φ-step reaches it either (because q² = 3 has no rational solution). The paper's proof in #33 is not reread here; this is an independent
proof by irrationality (the hint's norm route is not needed).

## Sources checked

Studies 2026-11-24-resonus (Theorem 1), 2026-11-25-one-structure (A1), 2026-11-25-stellation-cycle (gap (b), Theorem 8),
2026-11-22-lean-alexandrov (`Dice.lean` definitions and the face-cone/cell argument of `solidAngle_eq_curvature`, reused in
`faceCone_eq`; `volume_plane` from `Comparison.lean`), 2026-11-24-lean-rolling-law-a4 (build setup). Mathlib: `Measure.toSphere`
(`HaarToSphere.lean`), `EuclideanSpace.volume_ball_fin_three`, `Real.goldenRatio_mul_fib_succ_add_fib`, `Real.goldenRatio_irrational`,
`Nat.Prime.irrational_sqrt`, `Submodule.finrank_orthogonal_span_singleton`. Ziegler, *Lectures on Polytopes*, Thm 2.11 (face duality).

## LEADS

1. M2: the components of S \ Γ (the open regions π(relint f)) as a topological statement, to formalise A1 (a) word for word.
2. M2 (b): O on the boundary (both sides false), to complete A1.
3. M1: link to the Alexandrov `rayPolytope` (polar corners n j / d j) so that a_F is formally a corner of the polar.
