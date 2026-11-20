#!/usr/bin/env python3
"""Write DH12Data.lean from the lists made by gen600.py and emit600.py.
usage: make_dh12.py LISTS_FILE OUT_DIR"""
import pathlib
import sys

LISTS = pathlib.Path(sys.argv[1])
D = pathlib.Path(sys.argv[2])
AND = "&" + "&"
head = '''/-
Dehn–Hadwiger study, part 12: the 600-cell's normals, corners and facets, as data (DICTO, 20 Nov 2026).

Generated lists (study scripts `gen600.py`, `emit600.py`, exact ℤ[φ] arithmetic), as flat records `Q8` of eight whole
numbers (a vector `(a₀ + b₀ φ, …, a₃ + b₃ φ)`), so that the kernel checks below run fast: `L8`, the 600 vectors of
`cell600Z` each once; `V8`, the 120 corners of `cell600`, doubled (the corner is `(1/2) • gvec w.toZ`); `recs600`, for
each facet its four corners and the four facets across its four triangles. Everything is checked by `decide +kernel`;
nothing about the lists is assumed.
No `sorry`.
-/
import DehnHadwiger.DH11Cell600Defs

namespace DehnHadwiger

/-- A vector of ℤ[φ]⁴ as eight whole numbers. -/
structure Q8 where
  a0 : ℤ
  b0 : ℤ
  a1 : ℤ
  b1 : ℤ
  a2 : ℤ
  b2 : ℤ
  a3 : ℤ
  b3 : ℤ

/-- The vector as a function `Fin 4 → ℤ × ℤ`. -/
def Q8.toZ (q : Q8) : Fin 4 → ℤ × ℤ := ![(q.a0, q.b0), (q.a1, q.b1), (q.a2, q.b2), (q.a3, q.b3)]

/-- The zero record. -/
def q0 : Q8 := ⟨0, 0, 0, 0, 0, 0, 0, 0⟩

/-- `gdot` on records. -/
def dot8 (p q : Q8) : ℤ × ℤ :=
  (p.a0 * q.a0 + p.b0 * q.b0 + p.a1 * q.a1 + p.b1 * q.b1 + p.a2 * q.a2 + p.b2 * q.b2 + p.a3 * q.a3 + p.b3 * q.b3,
    p.a0 * q.b0 + p.b0 * q.a0 + p.b0 * q.b0 + p.a1 * q.b1 + p.b1 * q.a1 + p.b1 * q.b1 +
      p.a2 * q.b2 + p.b2 * q.a2 + p.b2 * q.b2 + p.a3 * q.b3 + p.b3 * q.a3 + p.b3 * q.b3)

lemma gdot_toZ (p q : Q8) : gdot p.toZ q.toZ = dot8 p q := by
  simp only [gdot, gmul, Q8.toZ, dot8, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
    Matrix.cons_val_three, Prod.mk_add_mk]
  ext <;> simp <;> ring

/-- The key of a vector, for comparisons. -/
def keyZ (z : Fin 4 → ℤ × ℤ) : List ℤ := [(z 0).1, (z 0).2, (z 1).1, (z 1).2, (z 2).1, (z 2).2, (z 3).1, (z 3).2]

/-- The key of a record. -/
def key8 (q : Q8) : List ℤ := [q.a0, q.b0, q.a1, q.b1, q.a2, q.b2, q.a3, q.b3]

lemma eq_of_key {z : Fin 4 → ℤ × ℤ} {q : Q8} (h : keyZ z = key8 q) : z = q.toZ := by
  simp only [keyZ, key8, List.cons.injEq, and_true] at h
  obtain ⟨h0, h1, h2, h3, h4, h5, h6, h7⟩ := h
  funext i; fin_cases i <;> simp [Q8.toZ] <;> ext <;> assumption

'''
tail = f'''
/-- The normal number `i`, read from its list of 60. -/
def L8get (i : ℕ) : Q8 :=
  match i / 60 with
  | 0 => L8_0.getD (i % 60) q0
  | 1 => L8_1.getD (i % 60) q0
  | 2 => L8_2.getD (i % 60) q0
  | 3 => L8_3.getD (i % 60) q0
  | 4 => L8_4.getD (i % 60) q0
  | 5 => L8_5.getD (i % 60) q0
  | 6 => L8_6.getD (i % 60) q0
  | 7 => L8_7.getD (i % 60) q0
  | 8 => L8_8.getD (i % 60) q0
  | 9 => L8_9.getD (i % 60) q0
  | _ => q0

/-- The corner number `i`, doubled, read from its list of 30. -/
def V8get (i : ℕ) : Q8 :=
  match i / 30 with
  | 0 => V8_0.getD (i % 30) q0
  | 1 => V8_1.getD (i % 30) q0
  | 2 => V8_2.getD (i % 30) q0
  | 3 => V8_3.getD (i % 30) q0
  | _ => q0

/-- The checks for the facet `k` with record `r`: the indices are in range; its corners are on it, its neighbours meet
it at the 600-cell's angle, the neighbour across the corner `j` contains the other three corners and gives
`c = (−8 + 6φ)/2` at the corner `j`, and twice the sum of the four neighbours is `(−2 + 6φ)` times its normal. -/
def recOK (k : ℕ) (r : List ℕ) : Bool :=
  ((List.range 4).all fun j => r.getD j 0 < 120 {AND} r.getD (j + 4) 0 < 600 {AND}
      dot8 (L8get k) (V8get (r.getD j 0)) == (2, 0) {AND} dot8 (L8get k) (L8get (r.getD (j + 4) 0)) == (-2, 6)) {AND}
    ((List.range 4).all fun i => (List.range 4).all fun j =>
      dot8 (L8get (r.getD (i + 4) 0)) (V8get (r.getD j 0)) == if i = j then (-8, 6) else (2, 0)) {AND}
    veq (fun m => gmul (2, 0) ((L8get (r.getD (0 + 4) 0)).toZ m + (L8get (r.getD (1 + 4) 0)).toZ m +
        (L8get (r.getD (2 + 4) 0)).toZ m + (L8get (r.getD (3 + 4) 0)).toZ m))
      (fun m => gmul (-2, 6) ((L8get k).toZ m))

/-- `recOK` for the records `rs`, numbered from `k`. -/
def recsOK : List (List ℕ) → ℕ → Bool
  | [], _ => true
  | r :: rs, k => recOK k r {AND} recsOK rs (k + 1)

lemma recsOK_get : ∀ (rs : List (List ℕ)) (k i : ℕ), recsOK rs k = true → i < rs.length →
    recOK (k + i) (rs.getD i []) = true
  | [], _, _, _, h => absurd h (by simp)
  | r :: rs, k, 0, h, _ => by simp only [recsOK, Bool.and_eq_true] at h; simpa using h.1
  | r :: rs, k, i + 1, h, hi => by
    simp only [recsOK, Bool.and_eq_true] at h
    have := recsOK_get rs (k + 1) i h.2 (by simpa using hi)
    rwa [show k + 1 + i = k + (i + 1) by omega] at this

/-! ### Symmetry: three generators of the coordinate changes that keep the normals -/

/-- `gen 0` changes the sign of the first coordinate; `gen 1` and `gen 2` (and higher) are 3-cycles of coordinates. -/
def gen : ℕ → Q8 → Q8
  | 0, q => ⟨-q.a0, -q.b0, q.a1, q.b1, q.a2, q.b2, q.a3, q.b3⟩
  | 1, q => ⟨q.a1, q.b1, q.a2, q.b2, q.a0, q.b0, q.a3, q.b3⟩
  | _ + 2, q => ⟨q.a0, q.b0, q.a2, q.b2, q.a3, q.b3, q.a1, q.b1⟩

/-- A word of generators, applied from the left. -/
def applyW : List ℕ → Q8 → Q8
  | [], q => q
  | g :: w, q => applyW w (gen g q)

/-- The generator `g` maps the normals `ts` (numbered from `k`) to the listed normals. -/
def tabOK (g : ℕ) : List ℕ → ℕ → Bool
  | [], _ => true
  | t :: ts, k => (key8 (gen g (L8get k)) == key8 (L8get t) {AND} t < 600) {AND} tabOK g ts (k + 1)

lemma tabOK_get (g : ℕ) : ∀ (ts : List ℕ) (k i : ℕ), tabOK g ts k = true → i < ts.length →
    key8 (gen g (L8get (k + i))) = key8 (L8get (ts.getD i 0)) ∧ ts.getD i 0 < 600
  | [], _, _, _, h => absurd h (by simp)
  | t :: ts, k, 0, h, _ => by
    simp only [tabOK, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h; simpa using h.1
  | t :: ts, k, i + 1, h, hi => by
    simp only [tabOK, Bool.and_eq_true] at h
    have := tabOK_get g ts (k + 1) i h.2 (by simpa using hi)
    rwa [show k + 1 + i = k + (i + 1) by omega] at this

/-- The corners `c, c + 1, …` are taken by their words to their listed representatives, which are among `reps120`. -/
def cornerOK : List (List ℕ) → List ℕ → ℕ → Bool
  | w :: ws, r :: rs, c => (key8 (applyW w (V8get c)) == key8 (V8get r) {AND} reps120.contains r) {AND} cornerOK ws rs (c + 1)
  | [], [], _ => true
  | _, _, _ => false

lemma cornerOK_get : ∀ (ws : List (List ℕ)) (rs : List ℕ) (c i : ℕ), cornerOK ws rs c = true → i < ws.length →
    key8 (applyW (ws.getD i []) (V8get (c + i))) = key8 (V8get (rs.getD i 0)) ∧ rs.getD i 0 ∈ reps120
  | [], _, _, _, _, h => absurd h (by simp)
  | _ :: _, [], _, _, h, _ => by simp [cornerOK] at h
  | w :: ws, r :: rs, c, 0, h, _ => by
    simp only [cornerOK, Bool.and_eq_true, beq_iff_eq, List.contains_iff_mem] at h; simpa using h.1
  | w :: ws, r :: rs, c, i + 1, h, hi => by
    simp only [cornerOK, Bool.and_eq_true] at h
    have := cornerOK_get ws rs (c + 1) i h.2 (by simpa using hi)
    rwa [show c + 1 + i = c + (i + 1) by omega] at this

/-! ### `cell600Z` against the 600 normals -/

/-- Entry by entry, `cell600Z` is the normal with the listed number. -/
def zipOK : List (Fin 4 → ℤ × ℤ) → List ℕ → Bool
  | z :: zs, i :: is => (keyZ z == key8 (L8get i) {AND} i < 600) {AND} zipOK zs is
  | [], [] => true
  | _, _ => false

lemma zipOK_get : ∀ (zs : List (Fin 4 → ℤ × ℤ)) (is : List ℕ) (p : ℕ), zipOK zs is = true → p < zs.length →
    keyZ (zs.getD p 0) = key8 (L8get (is.getD p 0)) ∧ is.getD p 0 < 600
  | [], _, _, _, h => absurd h (by simp)
  | _ :: _, [], _, h, _ => by simp [zipOK] at h
  | z :: zs, i :: is, 0, h, _ => by
    simp only [zipOK, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h; simpa using h.1
  | z :: zs, i :: is, p + 1, h, hp => by
    simp only [zipOK, Bool.and_eq_true] at h
    simpa using zipOK_get zs is p h.2 (by simpa using hp)

/-- Each normal `k` occurs in `cell600Z` at the listed place. -/
def posOK : List ℕ → ℕ → Bool
  | [], _ => true
  | p :: ps, k => (idx600.getD p 0 == k {AND} p < 2112) {AND} posOK ps (k + 1)

lemma posOK_get : ∀ (ps : List ℕ) (k i : ℕ), posOK ps k = true → i < ps.length →
    idx600.getD (ps.getD i 0) 0 = k + i ∧ ps.getD i 0 < 2112
  | [], _, _, _, h => absurd h (by simp)
  | p :: ps, k, 0, h, _ => by
    simp only [posOK, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h; simpa using h.1
  | p :: ps, k, i + 1, h, hi => by
    simp only [posOK, Bool.and_eq_true] at h
    have := posOK_get ps (k + 1) i h.2 (by simpa using hi)
    rwa [show k + 1 + i = k + (i + 1) by omega] at this

theorem chk_lengths : recs600.length = 600 ∧ tab0.length = 600 ∧ tab1.length = 600 ∧ tab2.length = 600 ∧
    words120.length = 120 ∧ pos600.length = 600 ∧ cell600Z.length = 2112 := by decide +kernel

theorem chk_recs : recsOK recs600 0 = true := by decide +kernel

theorem chk_norm : ((List.range 600).all fun k => dot8 (L8get k) (L8get k) == (8, 0)) = true := by decide +kernel

theorem chk_tabs : tabOK 0 tab0 0 = true ∧ tabOK 1 tab1 0 = true ∧ tabOK 2 tab2 0 = true := by decide +kernel

theorem chk_corners : cornerOK words120 rep120 0 = true := by decide +kernel

theorem chk_reps : (reps120.all fun r => (List.range 600).all fun k => gnonneg ((2, 0) - dot8 (L8get k) (V8get r))) = true := by
  decide +kernel

theorem chk_zip : zipOK cell600Z idx600 = true := by decide +kernel

theorem chk_pos : posOK pos600 0 = true := by decide +kernel
'''
tail += '\nend DehnHadwiger\n'
(D / 'DH12Data.lean').write_text(head + LISTS.read_text() + tail)
print((D / 'DH12Data.lean').stat().st_size)
