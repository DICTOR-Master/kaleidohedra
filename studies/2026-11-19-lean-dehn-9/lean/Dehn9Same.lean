/-
Lean study 9 of the shape-language canon (DICTO, 19 Nov 2026), part AD: the pairs over arccos(1/3) with
invariants of the same sign, decided by adding volumes.

Let θ = arccos(1/3). If dehn P = a ⊗ θ and dehn Q = b ⊗ θ, a similar copy of P at scale s and one of Q at
scale s' have invariants (s a) ⊗ θ, (s' b) ⊗ θ and volumes s³ vol P, s'³ vol Q. If the copies are scissors
congruent, both agree: s a = s' b (θ ∉ ℚπ) and s³ vol P = s'³ vol Q; then a³ vol Q = b³ vol P. So:

* `not_scissorsCongruent_of_cube_ne`: **if a³ vol Q ≠ b³ vol P, no similar copy of P is scissors congruent to a
  similar copy of Q** (any sizes, any positions). The number a³ / vol is the same for all similar copies
  (both scale by s³), and the condition says that it differs between P and Q.

The canon over θ (studies 3 and 7, volumes from part AC):
  tetrahedron: a = 12√2, vol = 8/3;  octahedron: a = −12√2, vol = 4/3;
  cube ∩ octahedron solid, 1 < t < 2: a = 12√2 (2t − 3), vol = (4/3)(t³ − 3(t − 1)³).
With x = 2t − 3 ∈ (−1, 1), a³/vol = 2592√2 · g with g = 4x³ / (12 + 9x − x³); the tetrahedron has g = 1/2 and
the octahedron g = −1 (= the value at t = 1, where the solid is the octahedron).

* `co_tetra_not_scissorsCongruent'`: every solid of the line (1 < t < 2) against the tetrahedron:
  2(2t − 3)³ − (t³ − 3(t − 1)³) = −3 + 9(t − 1)(t − 2)(2t − 3) < 0.
* `co_oct_not_scissorsCongruent'`: every solid of the line against the octahedron:
  (2t − 3)³ + t³ − 3(t − 1)³ = 3(t − 1)(2t² − 7t + 8) > 0.
* `co_co_not_scissorsCongruent`: two different solids of the line (s ≠ t):
  x³(12 + 9y − y³) − y³(12 + 9x − x³) = (x − y)(12(x² + xy + y²) + 9xy(x + y)), and the second factor is > 0 on
  (−1, 1)².
* `luckySeven_tetra_not_scissorsCongruent`: Lucky 7 (t = 1.7566…, inside 7/4 < t < 9/5) against the
  tetrahedron, the open pair of study 8.
* `canon_tet_not_scissorsCongruent`: **any two different solids of `TetFamily` (study 8)**; with
  `canon_table` (study 8) every pair of different nonzero words of the canon is decided (`canon_complete`).

Credits: Dehn's invariant and volume together (the classical pair of scissors-congruence invariants; Sydler
(1965) proved they are complete, which is not used here); studies 1 to 8 and part AC as named at the point of
use; Mathlib `ENNReal.ofReal_eq_ofReal_iff`, `ENNReal.ofReal_mul`; tactics `linear_combination`, `nlinarith`.
No `sorry`.
-/
import DehnCanon.Dehn9Vol

open scoped RealInnerProductSpace Real Pointwise
open Set MeasureTheory Measure Module

namespace DehnCanon

/-- **Invariant and volume together.** Over the one angle θ = arccos(1/3): if dehn P = a ⊗ θ,
dehn Q = b ⊗ θ and a³ vol Q ≠ b³ vol P, then no similar copy of `P` is scissors congruent to a similar copy
of `Q`. -/
theorem not_scissorsCongruent_of_cube_ne {P Q P' Q' : Set R3} {a b V W : ℝ}
    (hP : IsPoly P) (hQ : IsPoly Q)
    (ha : dehnSet P = edgeTerm a tetDihedral) (hb : dehnSet Q = edgeTerm b tetDihedral)
    (hV : volume P = ENNReal.ofReal V) (hW : volume Q = ENNReal.ofReal W) (hV0 : 0 ≤ V) (hW0 : 0 ≤ W)
    (hne : a ^ 3 * W ≠ b ^ 3 * V)
    (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' := by
  intro hs
  obtain ⟨s, hs0, g, rfl⟩ := hP'
  obtain ⟨s', hs0', g', rfl⟩ := hQ'
  have hd := dehnSet_eq_of_scissorsCongruent ((hP.smul_set hs0).image g)
    ((hQ.smul_set hs0').image g') hs
  rw [dehnSet_image, dehnSet_image, dehnSet_smul_set hs0, dehnSet_smul_set hs0', ha, hb,
    smul_edgeTerm, smul_edgeTerm] at hd
  have hd' := edgeTerm_inj tetDihedral_not_ratPi hd
  have hv := volume_eq_of_scissorsCongruent hs
  rw [volume_similar hs0, volume_similar hs0', hV, hW, ← ENNReal.ofReal_mul (pow_nonneg hs0.le 3),
    ← ENNReal.ofReal_mul (pow_nonneg hs0'.le 3),
    ENNReal.ofReal_eq_ofReal_iff (mul_nonneg (pow_nonneg hs0.le 3) hV0)
      (mul_nonneg (pow_nonneg hs0'.le 3) hW0)] at hv
  apply hne
  have h3 : s' ^ 3 * (a ^ 3 * W - b ^ 3 * V) = 0 := by
    linear_combination (-a ^ 3) * hv + V * ((s * a) ^ 2 + s * a * (s' * b) + (s' * b) ^ 2) * hd'
  have h4 : a ^ 3 * W - b ^ 3 * V = 0 := by
    rcases mul_eq_zero.1 h3 with h | h
    · exact absurd h (pow_pos hs0' 3).ne'
    · exact h
  linarith

/-! ### The arithmetic of the four kinds of pairs -/

/-- The volume of the line, (4/3)(t³ − 3(t − 1)³), is positive for 1 ≤ t ≤ 2. -/
lemma coVol_pos {t : ℝ} (ht1 : 1 ≤ t) (ht2 : t ≤ 2) : 0 < 4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3) := by
  nlinarith [mul_nonneg (sub_nonneg.2 ht1) (sub_nonneg.2 ht2), sq_nonneg (t - 1), sq_nonneg t,
    mul_nonneg (mul_nonneg (sub_nonneg.2 ht1) (sub_nonneg.2 ht1)) (sub_nonneg.2 ht2)]

lemma cube_twelve_sqrt2_pos : 0 < (12 * √2) ^ 3 := by positivity

lemma cond_co_tetra {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) :
    (12 * √2 * (2 * t - 3)) ^ 3 * (8 / 3) ≠ (12 * √2) ^ 3 * (4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3)) := by
  intro h
  have h' : (12 * √2) ^ 3 * (4 / 3 * (2 * (2 * t - 3) ^ 3 - (t ^ 3 - 3 * (t - 1) ^ 3))) = 0 := by
    linear_combination h
  have hp : 0 < (t - 1) * (2 - t) := mul_pos (by linarith) (by linarith)
  have hp1 : (t - 1) * (2 - t) ≤ 1 / 4 := by nlinarith [sq_nonneg (2 * t - 3)]
  have hneg : 2 * (2 * t - 3) ^ 3 - (t ^ 3 - 3 * (t - 1) ^ 3) < 0 := by
    have e : 2 * (2 * t - 3) ^ 3 - (t ^ 3 - 3 * (t - 1) ^ 3) =
        -3 - 9 * ((t - 1) * (2 - t)) * (2 * t - 3) := by ring
    rw [e]
    nlinarith [mul_le_mul_of_nonneg_left (show |2 * t - 3| ≤ 1 from abs_le.2 ⟨by linarith, by linarith⟩)
      hp.le, neg_abs_le (2 * t - 3), le_abs_self (2 * t - 3)]
  rcases mul_eq_zero.1 h' with h0 | h0
  · exact cube_twelve_sqrt2_pos.ne' h0
  · linarith

lemma cond_co_oct {t : ℝ} (ht1 : 1 < t) :
    (12 * √2 * (2 * t - 3)) ^ 3 * (4 / 3) ≠ (-12 * √2) ^ 3 * (4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3)) := by
  intro h
  have h' : (12 * √2) ^ 3 * (4 / 3 * ((2 * t - 3) ^ 3 + (t ^ 3 - 3 * (t - 1) ^ 3))) = 0 := by
    linear_combination h
  have hpos : 0 < (2 * t - 3) ^ 3 + (t ^ 3 - 3 * (t - 1) ^ 3) := by
    have e : (2 * t - 3) ^ 3 + (t ^ 3 - 3 * (t - 1) ^ 3) = 3 * (t - 1) * (2 * t ^ 2 - 7 * t + 8) := by ring
    rw [e]
    have : 0 < 2 * t ^ 2 - 7 * t + 8 := by nlinarith [sq_nonneg (t - 7 / 4)]
    have : 0 < t - 1 := by linarith
    positivity
  rcases mul_eq_zero.1 h' with h0 | h0
  · exact cube_twelve_sqrt2_pos.ne' h0
  · linarith

lemma cond_oct_tetra :
    (-12 * √2) ^ 3 * (8 / 3) ≠ (12 * √2) ^ 3 * (4 / 3) := by
  intro h
  have h' : (12 * √2) ^ 3 * 4 = 0 := by linear_combination -h
  exact absurd h' (by positivity)

/-- The second factor of the line against itself is positive on (−1, 1)² off the diagonal. -/
lemma line_factor_pos {x y : ℝ} (hx1 : -1 < x) (hx2 : x < 1) (hy1 : -1 < y) (hy2 : y < 1) (hxy : x ≠ y) :
    0 < 12 * (x ^ 2 + x * y + y ^ 2) + 9 * x * y * (x + y) := by
  have hd : 0 < (x - y) ^ 2 := by
    have : x - y ≠ 0 := sub_ne_zero.2 hxy
    positivity
  rcases le_or_gt 0 (x * y) with h | h
  · nlinarith [mul_nonneg h (show 0 ≤ x + y + 2 by linarith), sq_nonneg x, sq_nonneg y]
  · have hs : x + y < 1 := by
      rcases lt_or_ge 0 x with hx | hx
      · have : y < 0 := by
          by_contra hy; push Not at hy; nlinarith [mul_nonneg hx.le hy]
        linarith
      · linarith
    nlinarith [mul_nonneg_of_nonpos_of_nonpos h.le (show x + y - 1 ≤ 0 by linarith), sq_nonneg (x + y)]

lemma cond_co_co {s t : ℝ} (hs1 : 1 < s) (hs2 : s < 2) (ht1 : 1 < t) (ht2 : t < 2) (hst : s ≠ t) :
    (12 * √2 * (2 * s - 3)) ^ 3 * (4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3)) ≠
      (12 * √2 * (2 * t - 3)) ^ 3 * (4 / 3 * (s ^ 3 - 3 * (s - 1) ^ 3)) := by
  intro h
  set x := 2 * s - 3 with hx
  set y := 2 * t - 3 with hy
  have h' : (12 * √2) ^ 3 * (1 / 3 * ((x - y) * (12 * (x ^ 2 + x * y + y ^ 2) + 9 * x * y * (x + y)))) = 0 := by
    have es : s = (x + 3) / 2 := by rw [hx]; ring
    have et : t = (y + 3) / 2 := by rw [hy]; ring
    rw [es, et] at h
    linear_combination h
  have hK := line_factor_pos (x := x) (y := y) (by rw [hx]; linarith) (by rw [hx]; linarith)
    (by rw [hy]; linarith) (by rw [hy]; linarith) (fun e => hst (by rw [hx, hy] at e; linarith))
  have hxy : x - y ≠ 0 := fun e => hst (by rw [hx, hy] at e; linarith)
  rcases mul_eq_zero.1 h' with h0 | h0
  · exact cube_twelve_sqrt2_pos.ne' h0
  · rcases mul_eq_zero.1 h0 with h1 | h1
    · norm_num at h1
    · rcases mul_eq_zero.1 h1 with h2 | h2
      · exact hxy h2
      · linarith

/-! ### The pairs -/

lemma vol_co_nonneg {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) : 0 ≤ 4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3) :=
  (coVol_pos ht1.le ht2.le).le

/-- **Every cube ∩ octahedron solid (1 < t < 2) against the regular tetrahedron**: no similar copies are
scissors congruent. (Study 7 had 1 < t < 3/2, the opposite signs; here also 3/2 ≤ t < 2, Lucky 7 among
them.) -/
theorem co_tetra_not_scissorsCongruent' {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) {C T : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hT : IsSimilarCopy tetraSet T) : ¬ ScissorsCongruent C T :=
  not_scissorsCongruent_of_cube_ne (isPoly_co t) isPoly_tetra (dehnSet_co ht1 ht2) dehnSet_tetra_tet
    (volume_co ht1.le ht2) volume_tetra (vol_co_nonneg ht1 ht2) (by norm_num) (cond_co_tetra ht1 ht2) hC hT

/-- **Every cube ∩ octahedron solid (1 < t < 2) against the octahedron.** (Study 7 had 3/2 < t < 2; here
also 1 < t ≤ 3/2.) -/
theorem co_oct_not_scissorsCongruent' {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) {C O : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hO : IsSimilarCopy octSet O) : ¬ ScissorsCongruent C O :=
  not_scissorsCongruent_of_cube_ne (isPoly_co t) isPoly_oct (dehnSet_co ht1 ht2) dehnSet_oct
    (volume_co ht1.le ht2) volume_oct (vol_co_nonneg ht1 ht2) (by norm_num) (cond_co_oct ht1) hC hO

/-- **Two different cube ∩ octahedron solids**: for 1 < s, t < 2 with s ≠ t, no similar copies are
scissors congruent. -/
theorem co_co_not_scissorsCongruent {s t : ℝ} (hs1 : 1 < s) (hs2 : s < 2) (ht1 : 1 < t) (ht2 : t < 2)
    (hst : s ≠ t) {C D : Set R3} (hC : IsSimilarCopy (coSet s) C) (hD : IsSimilarCopy (coSet t) D) :
    ¬ ScissorsCongruent C D :=
  not_scissorsCongruent_of_cube_ne (isPoly_co s) (isPoly_co t) (dehnSet_co hs1 hs2) (dehnSet_co ht1 ht2)
    (volume_co hs1.le hs2) (volume_co ht1.le ht2) (vol_co_nonneg hs1 hs2) (vol_co_nonneg ht1 ht2)
    (cond_co_co hs1 hs2 ht1 ht2 hst) hC hD

/-- The octahedron against the tetrahedron, again, now by volume (study 7 did it by sign). -/
theorem oct_tetra_not_scissorsCongruent' {O T : Set R3} (hO : IsSimilarCopy octSet O)
    (hT : IsSimilarCopy tetraSet T) : ¬ ScissorsCongruent O T :=
  not_scissorsCongruent_of_cube_ne isPoly_oct isPoly_tetra dehnSet_oct dehnSet_tetra_tet volume_oct
    volume_tetra (by norm_num) (by norm_num) cond_oct_tetra hO hT

/-- **Lucky 7 against the tetrahedron** (the fair 14-face die, t = 1.7566…, inside 7/4 < t < 9/5): no
similar copies are scissors congruent. Both invariants are positive multiples of 1 ⊗ arccos(1/3). -/
theorem luckySeven_tetra_not_scissorsCongruent {t : ℝ} (h1 : 7 / 4 < t) (h2 : t < 9 / 5) {C T : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hT : IsSimilarCopy tetraSet T) : ¬ ScissorsCongruent C T :=
  co_tetra_not_scissorsCongruent' (by linarith) (by linarith) hC hT

/-- **The family over arccos(1/3) is pairwise apart**: any two different solids of `TetFamily` (the
octahedron, the tetrahedron, the cube ∩ octahedron solids with t ≠ 3/2) have no scissors-congruent similar
copies. -/
theorem canon_tet_not_scissorsCongruent {P Q P' Q' : Set R3} (hP : TetFamily P) (hQ : TetFamily Q)
    (hPQ : P ≠ Q) (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' := by
  rcases hP with rfl | rfl | ⟨s, hs1, hs2, -, rfl⟩ <;> rcases hQ with rfl | rfl | ⟨t, ht1, ht2, -, rfl⟩
  · exact absurd rfl hPQ
  · exact oct_tetra_not_scissorsCongruent' hP' hQ'
  · exact not_scissorsCongruent_of_cube_ne isPoly_oct (isPoly_co t) dehnSet_oct (dehnSet_co ht1 ht2)
      volume_oct (volume_co ht1.le ht2) (by norm_num) (vol_co_nonneg ht1 ht2)
      (Ne.symm (cond_co_oct ht1)) hP' hQ'
  · exact not_scissorsCongruent_of_cube_ne isPoly_tetra isPoly_oct dehnSet_tetra_tet dehnSet_oct
      volume_tetra volume_oct (by norm_num) (by norm_num) (Ne.symm cond_oct_tetra) hP' hQ'
  · exact absurd rfl hPQ
  · exact not_scissorsCongruent_of_cube_ne isPoly_tetra (isPoly_co t) dehnSet_tetra_tet
      (dehnSet_co ht1 ht2) volume_tetra (volume_co ht1.le ht2) (by norm_num) (vol_co_nonneg ht1 ht2)
      (Ne.symm (cond_co_tetra ht1 ht2)) hP' hQ'
  · exact co_oct_not_scissorsCongruent' hs1 hs2 hP' hQ'
  · exact co_tetra_not_scissorsCongruent' hs1 hs2 hP' hQ'
  · exact co_co_not_scissorsCongruent hs1 hs2 ht1 ht2 (fun e => hPQ (by rw [e])) hP' hQ'

/-- **The canon, complete for nonzero words**: study 8's table and the family over arccos(1/3).
For similar copies, any sizes and positions: (1) no nonzero word is scissors congruent to a zero word;
(2) no two different words over α, β are; (3) no word over θ to a word over α, β; (4) no two different words
over θ. -/
theorem canon_complete :
    (∀ {P Q P' Q' : Set R3}, IsNonzeroWord P → IsZeroWord Q → IsSimilarCopy P P' → IsSimilarCopy Q Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {i j : Fin 5} {P' Q' : Set R3}, i ≠ j → IsSimilarCopy (abWord i) P' → IsSimilarCopy (abWord j) Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {P Q P' Q' : Set R3}, TetFamily P → ABFamily Q → IsSimilarCopy P P' → IsSimilarCopy Q Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {P Q P' Q' : Set R3}, TetFamily P → TetFamily Q → P ≠ Q → IsSimilarCopy P P' →
      IsSimilarCopy Q Q' → ¬ ScissorsCongruent P' Q') :=
  ⟨canon_table.1, canon_table.2.1, canon_table.2.2,
    fun hP hQ hPQ hP' hQ' => canon_tet_not_scissorsCongruent hP hQ hPQ hP' hQ'⟩

end DehnCanon
