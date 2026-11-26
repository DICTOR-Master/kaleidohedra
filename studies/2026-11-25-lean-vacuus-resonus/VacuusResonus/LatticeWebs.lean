/-
Lattice webs of the Vacuus and the Resonus (study 2026-11-25-vacuus-resonus-lattice-webs, Theorem 0 and the
cube and rhombic-dodecahedron webs). DICTO, with Claude (Anthropic).
-/
import Mathlib
import VacuusResonus.PolarLink

/-!
# Lattice webs (M4)

A lattice tiling: cells `P + μ`, `μ ∈ Λ`, of a convex, centrally symmetric cell `P` with interior points.
A plane through the centre of `P` is the zero set of a nonzero linear functional `f`; its copies are the planes
`f x = f λ`, `λ ∈ Λ`. Let `h` be the least upper bound of `f` on `P`.

* `plane_meets_cell_iff` (**Theorem 0, the step**): the plane `f x = f λ` meets the interior of the cell
  `P + μ` if and only if `|f (λ - μ)| < h`.
* `web_iff` (**Theorem 0**): every copy that meets the interior of a cell is that cell's own central plane
  if and only if every lattice vector `ν` has `f ν = 0` or `h ≤ |f ν|` (the test `k = 2h/d ≤ 2`).
* `cube_resonus_web`, `cube_vacuus_web`, `rd_web`: the test holds for the cube (lattice `ℤ³`, cell
  `[-1/2, 1/2]³`) with the normals `eᵢ` (Resonus, `h = 1/2`) and `eᵢ ± eⱼ` (Vacuus, `h = 1`), and for the
  rhombic dodecahedron (lattice `D₃`, cell `|xᵢ ± xⱼ| ≤ 1`) with the normals `eᵢ ± eⱼ` (`h = 1`).
* `same_web`: for the normals `eᵢ ± eⱼ` both lattices give the same planes `f x ∈ ℤ`.
-/

namespace VacuusResonus

section General

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

omit [NormedSpace ℝ E] in
/-- The interior of a centrally symmetric set is centrally symmetric. -/
lemma neg_mem_interior {P : Set E} (hs : ∀ x ∈ P, -x ∈ P) {x : E} (hx : x ∈ interior P) :
    -x ∈ interior P := by
  have hpre : (Homeomorph.neg E) ⁻¹' P = P := by
    ext y; constructor
    · intro hy; simpa using hs _ hy
    · intro hy; simpa using hs y hy
  have := (Homeomorph.neg E).preimage_interior P
  rw [hpre] at this
  have hx' : x ∈ (Homeomorph.neg E) ⁻¹' interior P := by rw [this]; exact hx
  simpa using hx'

/-- `0` lies in the interior of a convex, centrally symmetric set with interior points. -/
lemma zero_mem_interior {P : Set E} (hc : Convex ℝ P) (hs : ∀ x ∈ P, -x ∈ P)
    (hi : (interior P).Nonempty) : (0 : E) ∈ interior P := by
  obtain ⟨x, hx⟩ := hi
  have hneg : -x ∈ interior P := neg_mem_interior hs hx
  have h2 := hc.interior (hx) hneg (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (0 : ℝ) ≤ 1 / 2)
    (by norm_num)
  simpa [smul_neg, ← sub_eq_add_neg] using h2

/-- **The plane `f x = t` meets the interior of `P` exactly when `|t| < h`.** -/
theorem plane_meets_interior_iff {P : Set E} (hc : Convex ℝ P) (hs : ∀ x ∈ P, -x ∈ P)
    (hi : (interior P).Nonempty) {f : E →L[ℝ] ℝ} (hf : f ≠ 0) {h : ℝ} (hh : IsLUB (f '' P) h) (t : ℝ) :
    (∃ x ∈ interior P, f x = t) ↔ |t| < h := by
  have h0 := zero_mem_interior hc hs hi
  have hub : ∀ p ∈ P, f p ≤ h := fun p hp => hh.1 ⟨p, hp, rfl⟩
  constructor
  · -- an interior point can move a little in a direction where `f` grows
    rintro ⟨x, hx, rfl⟩
    obtain ⟨v, hv⟩ : ∃ v, f v ≠ 0 := by
      by_contra hcon; push Not at hcon; exact hf (ContinuousLinearMap.ext hcon)
    have key : ∀ y ∈ interior P, f y < h := by
      intro y hy
      obtain ⟨r, hr, hball⟩ := Metric.isOpen_iff.1 isOpen_interior y hy
      have hvn : 0 < ‖v‖ := norm_pos_iff.2 (fun h0 => hv (by simp [h0]))
      set ε := r / (2 * ‖v‖) with hε
      have hεpos : 0 < ε := by positivity
      have hmem : ∀ s : ℝ, s = ε ∨ s = -ε → y + s • v ∈ P := by
        intro s hs'
        apply interior_subset; apply hball
        rw [Metric.mem_ball, dist_eq_norm, add_sub_cancel_left, norm_smul]
        have : |s| = ε := by rcases hs' with rfl | rfl <;> simp [abs_of_pos hεpos]
        rw [Real.norm_eq_abs, this, hε]
        field_simp; nlinarith
      rcases lt_or_gt_of_ne hv with hlt | hgt
      · have := hub _ (hmem (-ε) (Or.inr rfl))
        simp only [map_add, map_smul, smul_eq_mul] at this
        nlinarith
      · have := hub _ (hmem ε (Or.inl rfl))
        simp only [map_add, map_smul, smul_eq_mul] at this
        nlinarith
    have hxneg : -x ∈ interior P := neg_mem_interior hs hx
    have a1 := key x hx
    have a2 := key (-x) hxneg
    rw [map_neg] at a2
    exact abs_lt.2 ⟨by linarith, a1⟩
  · -- scale a point of `P` where `f` exceeds `|t|` towards the centre
    intro ht
    obtain ⟨_, ⟨p, hp, rfl⟩, hpt⟩ := (lt_isLUB_iff hh).1 ht
    have hfp : 0 < f p := lt_of_le_of_lt (abs_nonneg t) hpt
    set c := t / f p with hc'
    have hcabs : |c| < 1 := by
      rw [hc', abs_div, abs_of_pos hfp, div_lt_one hfp]; exact hpt
    refine ⟨c • p, ?_, by rw [map_smul, smul_eq_mul, hc']; field_simp⟩
    -- `c • p` lies on the open segment from `0` to `p` or to `-p`
    have hseg : ∀ q ∈ P, ∀ s : ℝ, 0 ≤ s → s < 1 → s • q ∈ interior P := by
      intro q hq s hs0 hs1
      rcases eq_or_lt_of_le hs0 with rfl | hspos
      · simpa using h0
      have := hc.openSegment_interior_closure_subset_interior h0 (subset_closure hq)
      apply this
      refine ⟨1 - s, s, by linarith, hspos, by ring, by simp⟩
    rcases le_or_gt 0 c with hc0 | hc0
    · exact hseg p hp c hc0 (lt_of_abs_lt hcabs)
    · have := hseg (-p) (hs p hp) (-c) (by linarith) (by linarith [neg_abs_le c, abs_lt.1 hcabs])
      simpa using this

/-- **Theorem 0, the step.** The copy `f x = f lam` meets the interior of the cell `P + μ` exactly when
`|f (lam - μ)| < h`. -/
theorem plane_meets_cell_iff {P : Set E} (hc : Convex ℝ P) (hs : ∀ x ∈ P, -x ∈ P)
    (hi : (interior P).Nonempty) {f : E →L[ℝ] ℝ} (hf : f ≠ 0) {h : ℝ} (hh : IsLUB (f '' P) h)
    (lam μ : E) :
    (∃ x ∈ interior ((fun y => y - μ) ⁻¹' P), f x = f lam) ↔ |f (lam - μ)| < h := by
  rw [← plane_meets_interior_iff hc hs hi hf hh]
  have hint : interior ((fun y => y - μ) ⁻¹' P) = (fun y => y - μ) ⁻¹' interior P :=
    ((Homeomorph.subRight μ).preimage_interior P).symm
  rw [hint]
  constructor
  · rintro ⟨x, hx, hfx⟩; exact ⟨x - μ, hx, by rw [map_sub, map_sub, hfx]⟩
  · rintro ⟨y, hy, hfy⟩
    exact ⟨y + μ, by simpa using hy, by rw [map_sub] at hfy; rw [map_add]; linarith⟩

/-- **Theorem 0 (the exact test).** Every copy of the plane that meets the interior of a cell is that cell's
own central plane if and only if every lattice vector `ν` has `f ν = 0` or `h ≤ |f ν|`. -/
theorem web_iff {P : Set E} (hc : Convex ℝ P) (hs : ∀ x ∈ P, -x ∈ P)
    (hi : (interior P).Nonempty) {f : E →L[ℝ] ℝ} (hf : f ≠ 0) {h : ℝ} (hh : IsLUB (f '' P) h)
    (Λ : AddSubgroup E) :
    (∀ lam ∈ Λ, ∀ μ ∈ Λ, (∃ x ∈ interior ((fun y => y - μ) ⁻¹' P), f x = f lam) → f lam = f μ) ↔
      ∀ ν ∈ Λ, f ν = 0 ∨ h ≤ |f ν| := by
  simp_rw [plane_meets_cell_iff hc hs hi hf hh]
  constructor
  · intro H ν hν
    by_contra hcon; push Not at hcon
    have := H ν hν 0 Λ.zero_mem (by simpa using hcon.2)
    exact hcon.1 (by simpa using this)
  · intro H lam hl μ hm hlt
    rcases H (lam - μ) (Λ.sub_mem hl hm) with h0 | hge
    · rw [map_sub] at h0; linarith
    · exact absurd hlt (not_lt.2 hge)

end General

section Concrete

/-- The cube `[-1/2, 1/2]³`. -/
def cube : Set E3 := {x | ∀ i, |x i| ≤ 1 / 2}

/-- The rhombic dodecahedron `|xᵢ + xⱼ| ≤ 1`, `|xᵢ - xⱼ| ≤ 1` (`i ≠ j`). -/
def rd : Set E3 := {x | ∀ i j, i ≠ j → |x i + x j| ≤ 1 ∧ |x i - x j| ≤ 1}

/-- The lattice `ℤ³`. -/
def Z3 : AddSubgroup E3 where
  carrier := {x | ∀ i, ∃ z : ℤ, x i = z}
  zero_mem' := fun i => ⟨0, by simp⟩
  add_mem' := by
    intro a b ha hb i; obtain ⟨u, hu⟩ := ha i; obtain ⟨v, hv⟩ := hb i
    exact ⟨u + v, by simp [hu, hv]⟩
  neg_mem' := by
    intro a ha i; obtain ⟨u, hu⟩ := ha i; exact ⟨-u, by simp [hu]⟩

/-- The lattice `D₃` (face-centred cubic): integer points with even coordinate sum. -/
def D3 : AddSubgroup E3 where
  carrier := {x | (∀ i, ∃ z : ℤ, x i = z) ∧ ∃ z : ℤ, x 0 + x 1 + x 2 = 2 * z}
  zero_mem' := ⟨fun i => ⟨0, by simp⟩, ⟨0, by simp⟩⟩
  add_mem' := by
    rintro a b ⟨ha, u, hu⟩ ⟨hb, v, hv⟩
    refine ⟨fun i => ?_, u + v, ?_⟩
    · obtain ⟨p, hp⟩ := ha i; obtain ⟨q, hq⟩ := hb i; exact ⟨p + q, by simp [hp, hq]⟩
    · simp only [PiLp.add_apply]; push_cast; linarith
  neg_mem' := by
    rintro a ⟨ha, u, hu⟩
    refine ⟨fun i => ?_, -u, ?_⟩
    · obtain ⟨p, hp⟩ := ha i; exact ⟨-p, by simp [hp]⟩
    · simp only [PiLp.neg_apply]; push_cast; linarith

/-- The normal `eᵢ + s eⱼ` as a functional. -/
noncomputable def pairF (i j : Fin 3) (s : ℝ) : E3 →L[ℝ] ℝ :=
  EuclideanSpace.proj i + s • EuclideanSpace.proj j

lemma pairF_apply (i j : Fin 3) (s : ℝ) (x : E3) : pairF i j s x = x i + s * x j := by
  simp [pairF]

lemma abs_apply_le_norm (x : E3) (i : Fin 3) : |x i| ≤ ‖x‖ := by
  simpa [Real.norm_eq_abs] using PiLp.norm_apply_le x i

lemma int_test {h : ℝ} (hh : h ≤ 1) {t : ℝ} (ht : ∃ z : ℤ, t = z) : t = 0 ∨ h ≤ |t| := by
  obtain ⟨z, rfl⟩ := ht
  rcases eq_or_ne z 0 with rfl | hz
  · simp
  · right; have : (1 : ℝ) ≤ |(z : ℝ)| := by
      rw [← Int.cast_abs]; exact_mod_cast Int.one_le_abs hz
    linarith

lemma convex_cube : Convex ℝ cube := by
  intro x hx y hy a b ha hb hab i
  have h1 := abs_le.1 (hx i); have h2 := abs_le.1 (hy i)
  simp only [PiLp.add_apply, PiLp.smul_apply, smul_eq_mul]
  rw [abs_le]; constructor <;> nlinarith

lemma convex_rd : Convex ℝ rd := by
  intro x hx y hy a b ha hb hab i j hij
  obtain ⟨h1, h2⟩ := hx i j hij; obtain ⟨h3, h4⟩ := hy i j hij
  rw [abs_le] at h1 h2 h3 h4
  simp only [PiLp.add_apply, PiLp.smul_apply, smul_eq_mul]
  refine ⟨abs_le.2 ⟨?_, ?_⟩, abs_le.2 ⟨?_, ?_⟩⟩ <;> nlinarith [h1.1, h1.2, h2.1, h2.2, h3.1, h3.2, h4.1, h4.2]

lemma ball_sub_cube : Metric.ball (0 : E3) (1 / 2) ⊆ cube := by
  intro x hx i
  have := abs_apply_le_norm x i
  rw [Metric.mem_ball, dist_zero_right] at hx; linarith

lemma ball_sub_rd : Metric.ball (0 : E3) (1 / 2) ⊆ rd := by
  intro x hx i j _
  have hi := abs_apply_le_norm x i; have hj := abs_apply_le_norm x j
  rw [Metric.mem_ball, dist_zero_right] at hx
  exact ⟨(abs_add_le _ _).trans (by linarith), (abs_sub _ _).trans (by linarith)⟩

lemma interior_cube : (interior cube).Nonempty :=
  ⟨0, interior_mono ball_sub_cube (by rw [Metric.isOpen_ball.interior_eq]; simp)⟩

lemma interior_rd : (interior rd).Nonempty :=
  ⟨0, interior_mono ball_sub_rd (by rw [Metric.isOpen_ball.interior_eq]; simp)⟩

lemma symm_cube : ∀ x ∈ cube, -x ∈ cube := fun x hx i => by simpa using hx i

lemma symm_rd : ∀ x ∈ rd, -x ∈ rd := by
  intro x hx i j hij
  obtain ⟨h1, h2⟩ := hx i j hij
  simp only [PiLp.neg_apply]
  exact ⟨by rw [← neg_add, abs_neg]; exact h1, by rw [neg_sub_neg, abs_sub_comm]; exact h2⟩

lemma single_apply' (i l : Fin 3) (c : ℝ) : (EuclideanSpace.single i c : E3) l = if l = i then c else 0 := by
  simp [PiLp.single_apply]

/-- **The cube's Resonus continues** (`ℤ³`, normal `eᵢ`, `h = 1/2`). -/
theorem cube_resonus_web (i : Fin 3) :
    ∀ lam ∈ Z3, ∀ μ ∈ Z3, (∃ x ∈ interior ((fun y => y - μ) ⁻¹' cube),
      EuclideanSpace.proj i x = EuclideanSpace.proj i lam) →
      EuclideanSpace.proj i lam = EuclideanSpace.proj i μ := by
  have hf : (EuclideanSpace.proj i : E3 →L[ℝ] ℝ) ≠ 0 := by
    intro h0; have := congrArg (fun g => g (EuclideanSpace.single i (1 : ℝ))) h0; simp at this
  have hlub : IsLUB ((EuclideanSpace.proj i : E3 →L[ℝ] ℝ) '' cube) (1 / 2) := by
    refine IsGreatest.isLUB ⟨⟨EuclideanSpace.single i (1 / 2), fun l => ?_, by simp⟩, ?_⟩
    · rw [single_apply']; split_ifs <;> norm_num
    · rintro _ ⟨x, hx, rfl⟩; exact (le_abs_self _).trans (hx i)
  refine (web_iff convex_cube symm_cube interior_cube hf hlub Z3).2 ?_
  intro ν hν; exact int_test (by norm_num) (hν i)

/-- **The cube's Vacuus continues** (`ℤ³`, normals `eᵢ ± eⱼ`, `h = 1`). -/
theorem cube_vacuus_web (i j : Fin 3) (hij : i ≠ j) (s : ℝ) (hs : s = 1 ∨ s = -1) :
    ∀ lam ∈ Z3, ∀ μ ∈ Z3, (∃ x ∈ interior ((fun y => y - μ) ⁻¹' cube), pairF i j s x = pairF i j s lam) →
      pairF i j s lam = pairF i j s μ := by
  have hf : pairF i j s ≠ 0 := by
    intro h0; have := congrArg (fun g => g (EuclideanSpace.single i (1 : ℝ))) h0
    simp [pairF_apply, hij.symm] at this
  have hlub : IsLUB (pairF i j s '' cube) 1 := by
    refine IsGreatest.isLUB ⟨⟨EuclideanSpace.single i (1 / 2) + EuclideanSpace.single j (s / 2), fun l => ?_, ?_⟩, ?_⟩
    · simp only [PiLp.add_apply, single_apply']
      split_ifs with h1 h2 <;> rcases hs with rfl | rfl <;> norm_num
      exact absurd (h1.symm.trans h2) hij
    · simp only [pairF_apply, PiLp.add_apply, single_apply']
      simp only [hij, hij.symm, ite_true, ite_false]
      rcases hs with rfl | rfl <;> norm_num
    · rintro _ ⟨x, hx, rfl⟩
      rw [pairF_apply]
      have h1 := abs_le.1 (hx i); have h2 := abs_le.1 (hx j)
      rcases hs with rfl | rfl <;> linarith
  refine (web_iff convex_cube symm_cube interior_cube hf hlub Z3).2 ?_
  intro ν hν
  obtain ⟨a, ha⟩ := hν i; obtain ⟨b, hb⟩ := hν j
  refine int_test le_rfl ?_
  rw [pairF_apply, ha, hb]
  rcases hs with rfl | rfl
  · exact ⟨a + b, by push_cast; ring⟩
  · exact ⟨a - b, by push_cast; ring⟩

/-- **The rhombic dodecahedron's planes continue** (`D₃`, normals `eᵢ ± eⱼ`, `h = 1`; here the Resonus and the
Vacuus are the same six planes). -/
theorem rd_web (i j : Fin 3) (hij : i ≠ j) (s : ℝ) (hs : s = 1 ∨ s = -1) :
    ∀ lam ∈ D3, ∀ μ ∈ D3, (∃ x ∈ interior ((fun y => y - μ) ⁻¹' rd), pairF i j s x = pairF i j s lam) →
      pairF i j s lam = pairF i j s μ := by
  have hf : pairF i j s ≠ 0 := by
    intro h0; have := congrArg (fun g => g (EuclideanSpace.single i (1 : ℝ))) h0
    simp [pairF_apply, hij.symm] at this
  have hlub : IsLUB (pairF i j s '' rd) 1 := by
    refine IsGreatest.isLUB ⟨⟨EuclideanSpace.single i 1, fun a b hab => ?_, ?_⟩, ?_⟩
    · simp only [single_apply']
      split_ifs <;> simp_all
    · simp [pairF_apply, hij.symm]
    · rintro _ ⟨x, hx, rfl⟩
      rw [pairF_apply]
      obtain ⟨h1, h2⟩ := hx i j hij
      rcases hs with rfl | rfl
      · linarith [le_abs_self (x i + x j)]
      · linarith [le_abs_self (x i - x j)]
  refine (web_iff convex_rd symm_rd interior_rd hf hlub D3).2 ?_
  intro ν hν
  obtain ⟨a, ha⟩ := hν.1 i; obtain ⟨b, hb⟩ := hν.1 j
  refine int_test le_rfl ?_
  rw [pairF_apply, ha, hb]
  rcases hs with rfl | rfl
  · exact ⟨a + b, by push_cast; ring⟩
  · exact ⟨a - b, by push_cast; ring⟩

lemma exists_third (i j : Fin 3) : ∃ k, k ≠ i ∧ k ≠ j := by
  fin_cases i <;> fin_cases j <;> decide

/-- **One web for both tilings.** For the normals `eᵢ ± eⱼ` the copies of the plane by `ℤ³` (the cube's
Vacuus) and by `D₃` (the rhombic dodecahedron's planes) are the same planes `f x = m`, `m ∈ ℤ`. -/
theorem same_web (i j : Fin 3) (hij : i ≠ j) (s : ℝ) (hs : s = 1 ∨ s = -1) :
    pairF i j s '' Z3 = Set.range (Int.cast : ℤ → ℝ) ∧ pairF i j s '' D3 = Set.range (Int.cast : ℤ → ℝ) := by
  have hZ : ∀ ν ∈ Z3, pairF i j s ν ∈ Set.range (Int.cast : ℤ → ℝ) := by
    intro ν hν
    obtain ⟨a, ha⟩ := hν i; obtain ⟨b, hb⟩ := hν j
    rw [pairF_apply, ha, hb]
    rcases hs with rfl | rfl
    · exact ⟨a + b, by push_cast; ring⟩
    · exact ⟨a - b, by push_cast; ring⟩
  obtain ⟨k, hki, hkj⟩ := exists_third i j
  -- `m eᵢ + m eₖ` lies in `D₃ ⊆ ℤ³` and has `f = m`
  have hwit : ∀ m : ℤ, (EuclideanSpace.single i (m : ℝ) + EuclideanSpace.single k (m : ℝ) : E3) ∈ D3 ∧
      pairF i j s (EuclideanSpace.single i (m : ℝ) + EuclideanSpace.single k (m : ℝ)) = m := by
    intro m
    refine ⟨⟨fun l => ?_, m, ?_⟩, ?_⟩
    · simp only [PiLp.add_apply, single_apply']
      split_ifs with h1 h2 h2
      · exact absurd (h2.symm.trans h1) hki
      · exact ⟨m, by simp⟩
      · exact ⟨m, by simp⟩
      · exact ⟨0, by simp⟩
    · simp only [PiLp.add_apply, single_apply']
      fin_cases i <;> fin_cases k <;> simp_all <;> ring
    · simp only [pairF_apply, PiLp.add_apply, single_apply']
      simp [hki.symm, hij.symm, hkj.symm]

  have hD : (D3 : Set E3) ⊆ Z3 := fun x hx => hx.1
  constructor
  · apply le_antisymm
    · rintro _ ⟨ν, hν, rfl⟩; exact hZ ν hν
    · rintro _ ⟨m, rfl⟩; exact ⟨_, hD (hwit m).1, (hwit m).2⟩
  · apply le_antisymm
    · rintro _ ⟨ν, hν, rfl⟩; exact hZ ν (hD hν)
    · rintro _ ⟨m, rfl⟩; exact ⟨_, (hwit m).1, (hwit m).2⟩

end Concrete

end VacuusResonus
