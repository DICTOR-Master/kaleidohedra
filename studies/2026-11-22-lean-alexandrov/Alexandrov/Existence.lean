/-
Alexandrov's theorem on prescribed curvature, polyhedral case: existence.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Coercive
import Alexandrov.PhiContinuity

/-!
# Existence (M9d)

**Theorem** (`alexandrov_existence`). Let `n 0, …, n (N-1)` be distinct unit vectors, not all in one
closed hemisphere, and `κ j ≥ 0` with `Σ κ j = 4π` satisfying Alexandrov's condition
`Σ_{i ∈ I} κ i < area (nbhd n 0 I)` for every nonempty proper set `I` of rays (the area of the open
`π/2`-neighbourhood of those rays). Then there are `r i > 0` such that the polytope with corners
`r i • n i` has curvature `κ j` at every corner.

Proof: maximize Oliker's functional `Phi` on the compact box `δ ≤ r i ≤ 1` (continuous there, M9b).
Any `r' > 0` scales into the slice `max r' = 1` without changing `Phi` (M9a); there it is either in the
box, or has some `r i < δ` and then `Phi < 0 = Phi 1` (M9c). So the box maximum is a global maximum,
and M8 gives the curvature.
-/

open MeasureTheory Set Metric Finset Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ} [NeZero N]

theorem alexandrov_existence {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hκ : ∀ j, 0 ≤ κ j) (hsum : ∑ j, κ j = 4 * Real.pi)
    (hA : ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
      ∑ i ∈ I, κ i < 3 * (volume (nbhd n 0 I ∩ ball (0 : E3) 1)).toReal) :
    ∃ r : Fin N → ℝ, (∀ i, 0 < r i) ∧
      ∀ j, curvature (rayPolytope n r) (corner n r j) = ENNReal.ofReal (κ j) := by
  obtain ⟨δ, hδ, hcoer⟩ := exists_coercive hn hspan hκ hsum hA
  set d := min δ 1 with hd
  have hd0 : 0 < d := lt_min hδ one_pos
  have hd1 : d ≤ 1 := min_le_right _ _
  set K : Set (Fin N → ℝ) := Set.Icc (fun _ => d) 1 with hK
  have hKpos : ∀ r ∈ K, ∀ i, 0 < r i := fun r hr i => lt_of_lt_of_le hd0 (hr.1 i)
  have h1K : (1 : Fin N → ℝ) ∈ K := ⟨fun i => by simp [hd1], le_rfl⟩
  have hcont : ContinuousOn (Phi n κ) K := fun r hr =>
    (continuousAt_Phi hspan κ (hKpos r hr)).continuousWithinAt
  obtain ⟨r, hrK, hrmax⟩ := isCompact_Icc.exists_isMaxOn ⟨1, h1K⟩ hcont
  have hrpos := hKpos r hrK
  have hglobal : ∀ r' : Fin N → ℝ, (∀ i, 0 < r' i) → Phi n κ r' ≤ Phi n κ r := by
    intro r' hr'
    obtain ⟨k, -, hk⟩ := Finset.exists_mem_eq_sup' univ_nonempty' r'
    set M := Finset.univ.sup' univ_nonempty' r' with hM
    have hMpos : 0 < M := by rw [hk]; exact hr' k
    have hle : ∀ i, r' i ≤ M := fun i => Finset.le_sup' r' (Finset.mem_univ i)
    set s : Fin N → ℝ := M⁻¹ • r' with hs
    have hsi : ∀ i, s i = M⁻¹ * r' i := fun i => rfl
    have hspos : ∀ i, 0 < s i := fun i => by rw [hsi]; exact mul_pos (inv_pos.2 hMpos) (hr' i)
    have hs1 : ∀ i, s i ≤ 1 := fun i => by
      rw [hsi, inv_mul_le_iff₀ hMpos, mul_one]; exact hle i
    have hsk : s k = 1 := by rw [hsi, ← hk, inv_mul_cancel₀ hMpos.ne']
    have hPs : Phi n κ s = Phi n κ r' := Phi_smul hspan hsum hr' (inv_pos.2 hMpos)
    rw [← hPs]
    by_cases hbox : ∀ i, d ≤ s i
    · exact isMaxOn_iff.1 hrmax s ⟨hbox, hs1⟩
    · push Not at hbox
      obtain ⟨i, hi⟩ := hbox
      have hneg := hcoer s hspos hs1 ⟨k, hsk⟩ ⟨i, lt_of_lt_of_le hi (min_le_left _ _)⟩
      have h1 := isMaxOn_iff.1 hrmax 1 h1K
      rw [Phi_one] at h1
      linarith
  refine ⟨r, hrpos, curvature_eq_of_maximizer hn hinj hspan hrpos κ hsum fun r' hr' => ?_⟩
  rw [gap_eq_Phi_sub hspan κ hrpos hr']
  linarith [hglobal r' hr']

end Alexandrov
