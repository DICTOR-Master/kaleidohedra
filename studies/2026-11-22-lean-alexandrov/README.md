# Lean study: Alexandrov's theorem on prescribed curvature, polyhedral case

DICTO, with Claude (Anthropic). Started 2026-11-22. Private study (no public repo).
Lean project: `~/lean/alexandrov` on the build host (Lean `v4.35.0-rc2`, Mathlib `v4.35.0-rc2`,
the same pin as the Dehn project). Sources mirrored here: `lakefile.toml`, `Alexandrov.lean`,
`Alexandrov/*.lean`; build logs in `logs/`.

## Why this theorem: how #112 (Aequi) uses it

#112 Theorem A (a): for distinct unit vectors n_1..n_N not all in one closed hemisphere, a die with
these face normals that is fair about 0 exists iff μ = (1/N) Σ δ_{n_k} satisfies Alexandrov's
condition, and it is then unique up to scale. The proof passes to the polar Q = P°, whose corners are
v_k = n_k / d_k on the rays through the n_k; Lemma 1 of #112 shows the solid angle of face k of P equals
the integral Gauss curvature of Q at v_k, that is the area of
{u ∈ S² : v_k·u ≥ v_j·u for all j}. So a fair die is a polytope with corners on given rays and equal
curvature 4π/N at every corner, and the uniqueness of the die is the uniqueness in Alexandrov's theorem
for such polytopes.

## The statement formalized (decided from the sources, before coding)

Sources opened:
* A. D. Aleksandrov, Doklady 35 (1942) 131-134: original; not opened (as in #112, cited via the next two).
* V. Oliker, Adv. Math. 213 (2007), arXiv:math/0701398: integral Gauss curvature, variational proof;
  Theorems 4 and 6 give the polytope case (abstract re-read 2026-11-22; full text read for #112).
* J. Bertrand, Geom. Dedicata 183 (2016), arXiv:1505.04821: prescription of Gauss curvature by optimal
  transport, Theorem 1.2, necessity at (3) of §1.1 (abstract re-read 2026-11-22; full text read for #112).
* A. I. Bobenko, I. Izmestiev, arXiv:math/0609447: checked and NOT the right theorem. It proves
  Alexandrov's gluing theorem (a convex polytope with a prescribed intrinsic metric on its boundary),
  not the prescribed-curvature theorem.

**Theorem (Alexandrov, polyhedral integral curvature).** Let n_1..n_N be distinct unit vectors in R³,
not all in one closed hemisphere, and κ_1..κ_N > 0 with Σ κ_i = 4π. For r ∈ (0,∞)^N let
Q(r) = conv{r_i n_i} and κ_i(r) = area{u ∈ S² : r_i n_i·u ≥ r_j n_j·u ∀ j}, the integral Gauss
curvature of Q(r) at its corner r_i n_i.
1. (Uniqueness) If κ_i(r) = κ_i(r') > 0 for all i, then r' = c r for some c > 0.
2. (Existence) There is r with κ_i(r) = κ_i for all i iff for every nonempty spherically convex
   ω ≠ S², Σ_{n_i ∈ ω} κ_i < area(ω^{π/2}) (ω^{π/2} = directions within π/2 of ω).
   For the dice: κ_i = 4π/N.

Formal choices (shortest honest route): `normalCone Q p = {x | ∀ q ∈ Q, ⟪q,x⟫ ≤ ⟪p,x⟫}`;
`curvature Q p = 3 · volume(normalCone Q p ∩ unit ball)` (the area of a spherical region is three times
the volume of its cone in the unit ball, so this is the Gauss-image area with no sphere measure needed);
`rayPolytope n r = convexHull ℝ (range (i ↦ r i • n i))`. The hemisphere condition is
`∀ x ≠ 0, ∃ i, 0 < ⟪n i, x⟫`.

Uniqueness proof (classical maximum principle): scale r' so that r' ≤ r with equality on a nonempty
set I of rays; if the complement J is nonempty, the cells of the I-corners only grow, and near a boundary
point between the I-cells and J-cells (found by connectedness of R³∖{0}) they grow by an open set, so
some I-corner gains curvature: contradiction. Hence J is empty and r' = c r.

## RESUME NOTES (kept current; power outage 2026-11-24 10:00 JST)

* Done and committed: M1-M8, M9a, M9b (see Milestones). Each milestone: `check.sh TAG thm...` on the
  build host (full build + axioms + sorry count, FINAL ok line), then README line + commit.
* Done: M9c part 1 (Margin.lean).
* Done: M9c part 2 (Coercive.lean).
* Done: M9d (Existence.lean), M6b (Hemisphere.lean). Done: `Main.lean` (M10). In progress:
  `Dice.lean` (fair-dice corollary with #112 Lemma 1); not in the Milestones list = not finished.
* Then M9c part 2 `Coercive.lean`: with a_j = −log r_j (0 < r ≤ 1, some r_j = 1), T = max a_j,
  mx(x) = max_j (ψ_j if ε‖x‖ < ⟪n_j,x⟫ else −T): (a) log(supp r/supp 1) ≥ log ε + mx pointwise;
  (b) layer cake (`lintegral_eq_lintegral_meas_lt`) on −mx over the ball and on Σκ_j a_j, compared
  for each level t using `exists_margin`; result Phi r ≤ −4π log ε − η T, so Phi r < 0 once
  min r_j < δ. Then M9d: maximize Phi on {δ ≤ r_j ≤ 1} (compact, M9b), extend by scaling (M9a),
  apply M8. M6b (spherically convex ω ≠ S² lies in a closed hemisphere) after that.

## Milestones (each: clean build, no sorry, committed and mirrored)

* M1 (2026-11-22) `Alexandrov/Basic.lean`: definitions; normal cone of the ray polytope at a corner =
  its cell (`normalCone_rayPolytope`); curvature = 3·volume(cell ∩ ball); curvature unchanged by
  scaling (`curvature_smul`); cells closed; corners on distinct rays are distinct. Build ok, no sorry.
* M2 (2026-11-22) `Alexandrov/Comparison.lean`: the comparison lemma `exists_cell_volume_lt`
  (maximum principle): if ρ ≤ r with equality on a nonempty set I and strict inequality on a nonempty
  set J, and every cell of r has positive volume, some corner in I has a strictly larger cell for ρ.
  Helpers: boundary point of an open set in a connected set; homogeneity and continuity of the
  farthest-corner function; planes through 0 have volume 0; cells of fixed corners only grow.
  Build ok, no sorry.
* M3 (2026-11-22) `Alexandrov/Uniqueness.lean`: **Step 1 done.** `alexandrov_uniqueness`: same positive
  curvature at every corner ⇒ r' = c • r with c > 0 (scale r' by the largest ratio r'_i/r_i, then the
  comparison lemma rules out any strict ray). Full `lake build` ok (log `logs/build-M3.log`, FINAL ok);
  0 sorry; axioms of `alexandrov_uniqueness`: propext, Classical.choice, Quot.sound; 456 lines.
* M4 (2026-11-22) `Alexandrov/Total.lean`: first piece of Step 2. `sum_curvature`: the curvatures at
  the corners add up to 4π (cells cover space, two cells meet in a plane of volume 0, unit ball volume
  4π/3 from Mathlib). So Σκ_i = 4π is necessary; for the dice κ_i = 4π/N. Full build ok
  (`logs/build-M4.log`, FINAL ok); 0 sorry; standard axioms only; 522 lines.

* M5 (2026-11-24) `Alexandrov/Continuity.lean`: `continuousAt_curvature`: at every r with all r_i > 0,
  the curvature at each corner is continuous in r (dominated convergence; off the tie planes of r,
  which have volume 0, membership in a cell is decided by strict inequalities that persist nearby).
* M7 (2026-11-24) `Alexandrov/Monotone.lean`: moving one corner k outward along its ray, with the others
  fixed, enlarges its cell and shrinks every other cell: `curvature_le_of_raise`
  (κ_k does not decrease), `curvature_le_of_raise_other` (each κ_j, j ≠ k, does not increase).
* M6 (2026-11-24) `Alexandrov/Necessity.lean`: `curvature_lt_of_hemisphere`: for any set C of
  directions that contains a nonzero vector and lies in a closed hemisphere,
  Σ_{n_i ∈ C} κ_i < area of the open π/2-neighbourhood of C. Every nonempty spherically convex
  ω ≠ S² lies in a closed hemisphere, so this gives the necessity half of Alexandrov's condition in its
  stronger (open-neighbourhood) form; convexity is not needed. Proof: the cells of those corners lie in
  the neighbourhood, and a boundary point of the neighbourhood (connectedness of R³∖{0}) shows an open
  piece of it is left over.
  Full build ok (`logs/build-M6.log`, FINAL ok); 0 sorry; standard axioms only; 821 lines.
  Still to add for the textbook wording: "spherically convex ω ≠ S² lies in a closed hemisphere"
  (a separation lemma).

* M8 (2026-11-24) `Alexandrov/Variational.lean`: `curvature_eq_of_maximizer`. With
  `supp n r x = max_j r_j⟪n_j,x⟫` (support function) and
  `gap n κ r r' = Σ κ_j log(r'_j/r_j) − 3∫_{ball} log(supp r' / supp r)` (the change of Oliker's
  functional), if Σκ_j = 4π and gap(r, r') ≤ 0 for every r' > 0, then the curvature at every corner of
  the polytope of r is κ_j. (No sign hypothesis on κ is needed.) Proof: push one corner out by s > 1;
  the integrand lies in [0, log s] and vanishes off its new cell, so κ_j ≤ κ_j(r'_s); s → 1 by M5;
  totals equal by M4. Full build ok (`logs/build-M8.log`, FINAL ok); 0 sorry; standard axioms; 1051 lines.

* M9a (2026-11-24) `Alexandrov/Functional.lean`: the integrand of `gap` is bounded by
  Σ_i |log(r'_i/r_i)| (`abs_log_ratio_le`), hence integrable; gains add along a path (`gap_add`);
  a homothety gains (Σκ − 4π) log c (`gap_smul`). `Phi n κ r = gap n κ 1 r`: `Phi 1 = 0`,
  `gap r r' = Phi r' − Phi r`, `Phi (c • r) = Phi r` when Σκ = 4π. Check script `check.sh`; full build ok
  (`logs/build-M9a.log`, FINAL ok); 0 sorry; standard axioms; 1232 lines.

* M9b (2026-11-24) `Alexandrov/PhiContinuity.lean`: `continuousAt_Phi`: Oliker's functional is
  continuous at every r with positive entries (dominated convergence with a constant bound near r).
  Full build ok (`logs/build-M9b.log`, FINAL ok); 0 sorry; standard axioms.

* M9c part 1 (2026-11-24) `Alexandrov/Margin.lean`: `nbhd n ε I` = directions with
  ⟪n_i,x⟫ > ε‖x‖ for some i ∈ I (`nbhd n 0 I` = open π/2-neighbourhood). `exists_cover`: some ε₀ > 0
  has every direction within ⟪n_j,x⟫ > ε₀‖x‖ of a ray (compact sphere). `exists_margin`: Alexandrov's
  condition Σ_{i∈I} κ_i < area(nbhd n 0 I) for all nonempty proper I survives with one ε > 0 and a
  uniform margin η > 0. Full build ok (`logs/build-M9c1.log`, FINAL ok); 0 sorry; standard axioms.

* M9c part 2 (2026-11-24) `Alexandrov/Coercive.lean`: `Phi_le_of_margin`: on the slice
  0 < r ≤ 1 with some r_i = 1, Phi r ≤ −4π log ε − η·max_j(−log r_j) (pointwise bound
  log(supp r/supp 1) ≥ log ε + mx, then the layer-cake formula on the ball and on the rays, compared
  level by level with the margin). `exists_coercive`: under Alexandrov's condition there is δ > 0
  with Phi r < 0 = Phi 1 on the slice whenever some r_i < δ. Full build ok (`logs/build-M9c2.log`,
  FINAL ok); 0 sorry; standard axioms.

* M9d (2026-11-24) `Alexandrov/Existence.lean`: **Step 2 done.** `alexandrov_existence`: distinct
  unit n_i not in one closed hemisphere, κ_j ≥ 0, Σκ_j = 4π, and Alexandrov's condition
  Σ_{i∈I} κ_i < area(open π/2-neighbourhood of the rays in I) for every nonempty proper I ⇒ there are
  r_i > 0 whose polytope has curvature κ_j at every corner (maximize Phi on the box δ ≤ r ≤ 1, extend by
  scaling and coercivity, apply M8). Full build ok (`logs/build-M9d.log`, FINAL ok); 0 sorry; standard
  axioms. With M3 (uniqueness) and M6 (necessity) this is the whole polyhedral theorem used by #112.

* M6b (2026-11-24) `Alexandrov/Hemisphere.lean`: `exists_halfspace_of_convex`: a convex set K ≠ E3
  closed under positive scaling lies in a closed half-space through 0 (finite-dimensional separation).
  `curvature_lt_of_sphericallyConvex`: necessity in the textbook form: for nonempty ω on the unit
  sphere with convex cone {t·v : t > 0, v ∈ ω} (ω spherically convex; such ω is never all of S²),
  Σ_{n_i∈ω} κ_i < area of the open π/2-neighbourhood of ω. Full build ok (`logs/build-M6b.log`,
  FINAL ok); 0 sorry; standard axioms.

* M10 (2026-11-24) `Alexandrov/Main.lean`: **the whole polyhedral theorem.** For distinct unit n_i
  not in one closed hemisphere and κ_j > 0: `alexandrov_iff`: a polytope with corners r_i n_i (r_i > 0)
  and curvature κ_j at every corner exists ⇔ Σκ_j = 4π and `AlexandrovCondition n κ`
  (Σ_{i∈I} κ_i < area of the open π/2-neighbourhood of the rays in I, every nonempty proper I);
  `alexandrov_unique`: it is unique up to scaling about 0; `alexandrov_necessary` is the ⇒ half.
  Full build ok (`logs/build-M10.log`, FINAL ok); 0 sorry; standard axioms; 1987 lines.

## Next steps: existence (small pieces, variational route of Oliker 2007)

* M8 done (above).
* M6b: spherically convex ω ≠ S² lies in a closed hemisphere (separation), giving the textbook wording.
* M9 (existence of a maximizer), in pieces: M9a gap is a cocycle (gap(r,r'') = gap(r,r') + gap(r',r''))
  and scale invariant, so Φ(r) := gap(r₀, r) is well defined on the slice max r_j = 1; M9b Φ continuous on
  the positive slice; M9c coercivity from Alexandrov's condition (Φ → −∞ as min r_j → 0; several scales
  by induction on the set of collapsing rays); M9d compactness ⇒ a maximizer exists, interior by M9c.
  M9c is the main remaining work.
* M10: assemble: Alexandrov's condition + Σκ = 4π ⇒ existence; corollary for the dice (κ_j = 4π/N).
