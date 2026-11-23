/-
# The dice from exact coordinates, and the rolling law on them (M4, M5)

For each die the data file gives exact vertex directions `V v`, heights `c k`
(by vertex type `k`) and face normals `n x`, all in ℤ[√5]. The die is
`{ y : n x · y ≤ 1 for every face x }`; its vertices are `V v / c (type v)`.
Checked by the kernel and transferred to ℝ (`Q5.le_iff`):
* `heights_pos`: every height is positive;
* `support`: `n x · V v ≤ c (type v)` for every face `x` and vertex `v`, with
  equality exactly when `v` is one of the three vertices of face `x`
  (so every listed triangle is a face of the die, with exactly those vertices);
* `fv_type`: the three vertices of a face have the three types 0, 1, 2;
* `roll_edge`: rolling across the edge of type `i` keeps exactly the two
  vertices of the other types: adjacent faces = one simple reflection;
* `corner`: the faces at the vertex of type `k` of face `x` are exactly the
  `2 m(i,j)` faces reached by rolling round that corner with `i, j`
  (`{i, j, k} = {0, 1, 2}`): corners = rank-2 parabolic cosets, valence `2 m`.
The roll tables used here are the ones of `RollingLaw.Dice`, so all theorems
there (group order, Matsumoto, word reduction) are about these dice.
M5, `rolling_law` / `rolling_reduce`: stated for rolls between any two faces of the die.
-/
import RollingLaw.Dice

namespace RollingLaw

open CoxeterSystem (alternatingWord)

namespace Die

/-- Transfer of a kernel check to ℝ. -/
theorem support_of {d c : Q5} {P : Prop} [Decidable P]
    (h : if P then d = c else (Q5.le c d = false ∧ Q5.le d c = true)) :
    d.toReal ≤ c.toReal ∧ (d.toReal = c.toReal ↔ P) := by
  split_ifs at h with hP
  · subst h; simp [hP]
  · have := Q5.lt_of_le_false h.1
    exact ⟨this.le, by simp [hP, this.ne]⟩

/-- A duplicate-free list inside a finite set of the same size is that set. -/
theorem mem_iff_of_card {β : Type*} [Fintype β] [DecidableEq β] (P : β → Prop) [DecidablePred P]
    (l : List β) (hn : l.Nodup) (hl : ∀ y ∈ l, P y) (hc : (Finset.univ.filter P).card = l.length) :
    ∀ y, P y ↔ y ∈ l := by
  have hsub : l.toFinset ⊆ Finset.univ.filter P := fun y hy => by
    simpa using hl y (List.mem_toFinset.mp hy)
  have heq := Finset.eq_of_subset_of_card_le hsub (by rw [hc, List.toFinset_card_of_nodup hn])
  intro y
  constructor
  · intro hy
    have : y ∈ Finset.univ.filter P := by simpa using hy
    rw [← heq] at this; exact List.mem_toFinset.mp this
  · exact hl y

/-- The third edge type. -/
def third (i j : Fin 3) : Fin 3 := ⟨(3 - i.val - j.val) % 3, Nat.mod_lt _ (by decide)⟩

end Die

/-! ## A3: the tetrakis hexahedron -/
namespace A3
open Die

/-- vertex direction `V v` -/
def vtx (v : Fin 14) : List Q5 := Data.A3.vert.getD v.val []
/-- vertex type -/
def ty (v : Fin 14) : Fin 3 := ⟨(Data.A3.vtype.getD v.val 0) % 3, Nat.mod_lt _ (by decide)⟩
/-- the height `c` of the vertex's type -/
def ht (v : Fin 14) : Q5 := Data.A3.height.getD (ty v).val Q5.zero
/-- face normal `n x` -/
def nrm (x : Fin 24) : List Q5 := Data.A3.normal.getD x.val []
/-- the vertex of type `k` of face `x` -/
def fv (x : Fin 24) (k : Fin 3) : Fin 14 :=
  ⟨((Data.A3.fv.getD x.val []).getD k.val 0) % 14, Nat.mod_lt _ (by decide)⟩

theorem heights_pos : ∀ v, 0 < (ht v).toReal := by
  have h : ∀ v, Q5.le (ht v) Q5.zero = false := by decide +kernel
  intro v; simpa [Q5.toReal, Q5.zero] using Q5.lt_of_le_false (h v)

theorem support_q : ∀ (x : Fin 24) (v : Fin 14), if fv x (ty v) = v then Q5.dot (nrm x) (vtx v) = ht v
    else (Q5.le (ht v) (Q5.dot (nrm x) (vtx v)) = false ∧ Q5.le (Q5.dot (nrm x) (vtx v)) (ht v) = true) := by
  decide +kernel

/-- Every listed face lies in a supporting plane of the die and contains exactly its three vertices. -/
theorem support (x : Fin 24) (v : Fin 14) :
    Q5.rdot (nrm x) (vtx v) ≤ (ht v).toReal ∧
    (Q5.rdot (nrm x) (vtx v) = (ht v).toReal ↔ fv x (ty v) = v) := by
  rw [← Q5.toReal_dot]; exact support_of (support_q x v)

theorem fv_type : ∀ (x : Fin 24) (k : Fin 3), ty (fv x k) = k := by decide +kernel

/-- Rolling across the edge of type `i` keeps exactly the vertices of the other two types. -/
theorem roll_edge : ∀ (x : Fin 24) (i k : Fin 3), fv (r i x) k = fv x k ↔ k ≠ i := by
  decide +kernel

theorem corner_q : ∀ (x : Fin 24) (i j : Fin 3), i ≠ j →
    ((List.range (2 * M i j)).map fun t => roll r (alternatingWord i j t) x).Nodup ∧
    (∀ t < 2 * M i j, fv (roll r (alternatingWord i j t) x) (third i j) = fv x (third i j)) := by
  decide +kernel

theorem valence_q : ∀ (x : Fin 24) (i j : Fin 3), i ≠ j →
    (Finset.univ.filter fun y => fv y (third i j) = fv x (third i j)).card = 2 * M i j := by
  decide +kernel

/-- **Corners are rank-2 cosets.** The faces at the corner of type `third i j` of face `x`
are exactly the `2 m(i,j)` faces reached from `x` by rolling round it with `i, j`. -/
theorem corner (x : Fin 24) (i j : Fin 3) (hij : i ≠ j) (y : Fin 24) :
    fv y (third i j) = fv x (third i j) ↔ ∃ t < 2 * M i j, y = roll r (alternatingWord i j t) x := by
  obtain ⟨hn, hl⟩ := corner_q x i j hij
  rw [mem_iff_of_card (fun y => fv y (third i j) = fv x (third i j)) _ hn
    (by simpa using hl) (by simpa using valence_q x i j hij)]
  simp [eq_comm]

/-- **The rolling law on the tetrakis hexahedron.** Two shortest rolls between the same two faces
are joined by corner moves. -/
theorem rolling_law {f g : Fin 24} {ω ω' : List (Fin 3)} (h : model.ShortestRoll f g ω)
    (h' : model.ShortestRoll f g ω') : BraidEq M ω ω' :=
  model.rolling_law cs lifts h h'

/-- Every roll is brought to a shortest roll between the same two faces by corner moves and
cancelling back-and-forth rolls. -/
theorem rolling_reduce (f : Fin 24) (ω : List (Fin 3)) :
    ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧ model.ShortestRoll f (roll r ω f) ω' :=
  model.rolling_reduce cs lifts f ω

/-- Between any two faces there is a shortest roll of at most 6 rolls. -/
theorem exists_shortestRoll_le (f g : Fin 24) : ∃ ω, model.ShortestRoll f g ω ∧ ω.length ≤ 6 := by
  obtain ⟨ω, h, w, hw⟩ := model.exists_shortestRoll cs lifts f g
  exact ⟨ω, h, hw ▸ length_le w⟩

/-- Some shortest roll needs exactly 6 rolls (from face 0 to the opposite face). -/
theorem exists_shortestRoll_eq : ∃ g ω, model.ShortestRoll 0 g ω ∧ ω.length = 6 := by
  obtain ⟨x, hx, -⟩ := d_top
  refine ⟨x, model.sw x, ⟨model.roll_sw x, fun η hη => ?_⟩, by rw [model.length_sw, hx]⟩
  rw [model.length_sw, ← hη]; exact model.d_le_length η

end A3

/-! ## B3: the disdyakis dodecahedron -/
namespace B3
open Die

/-- vertex direction `V v` -/
def vtx (v : Fin 26) : List Q5 := Data.B3.vert.getD v.val []
/-- vertex type -/
def ty (v : Fin 26) : Fin 3 := ⟨(Data.B3.vtype.getD v.val 0) % 3, Nat.mod_lt _ (by decide)⟩
/-- the height `c` of the vertex's type -/
def ht (v : Fin 26) : Q5 := Data.B3.height.getD (ty v).val Q5.zero
/-- face normal `n x` -/
def nrm (x : Fin 48) : List Q5 := Data.B3.normal.getD x.val []
/-- the vertex of type `k` of face `x` -/
def fv (x : Fin 48) (k : Fin 3) : Fin 26 :=
  ⟨((Data.B3.fv.getD x.val []).getD k.val 0) % 26, Nat.mod_lt _ (by decide)⟩

theorem heights_pos : ∀ v, 0 < (ht v).toReal := by
  have h : ∀ v, Q5.le (ht v) Q5.zero = false := by decide +kernel
  intro v; simpa [Q5.toReal, Q5.zero] using Q5.lt_of_le_false (h v)

theorem support_q : ∀ (x : Fin 48) (v : Fin 26), if fv x (ty v) = v then Q5.dot (nrm x) (vtx v) = ht v
    else (Q5.le (ht v) (Q5.dot (nrm x) (vtx v)) = false ∧ Q5.le (Q5.dot (nrm x) (vtx v)) (ht v) = true) := by
  decide +kernel

/-- Every listed face lies in a supporting plane of the die and contains exactly its three vertices. -/
theorem support (x : Fin 48) (v : Fin 26) :
    Q5.rdot (nrm x) (vtx v) ≤ (ht v).toReal ∧
    (Q5.rdot (nrm x) (vtx v) = (ht v).toReal ↔ fv x (ty v) = v) := by
  rw [← Q5.toReal_dot]; exact support_of (support_q x v)

theorem fv_type : ∀ (x : Fin 48) (k : Fin 3), ty (fv x k) = k := by decide +kernel

/-- Rolling across the edge of type `i` keeps exactly the vertices of the other two types. -/
theorem roll_edge : ∀ (x : Fin 48) (i k : Fin 3), fv (r i x) k = fv x k ↔ k ≠ i := by
  decide +kernel

theorem corner_q : ∀ (x : Fin 48) (i j : Fin 3), i ≠ j →
    ((List.range (2 * M i j)).map fun t => roll r (alternatingWord i j t) x).Nodup ∧
    (∀ t < 2 * M i j, fv (roll r (alternatingWord i j t) x) (third i j) = fv x (third i j)) := by
  decide +kernel

theorem valence_q : ∀ (x : Fin 48) (i j : Fin 3), i ≠ j →
    (Finset.univ.filter fun y => fv y (third i j) = fv x (third i j)).card = 2 * M i j := by
  decide +kernel

/-- **Corners are rank-2 cosets.** The faces at the corner of type `third i j` of face `x`
are exactly the `2 m(i,j)` faces reached from `x` by rolling round it with `i, j`. -/
theorem corner (x : Fin 48) (i j : Fin 3) (hij : i ≠ j) (y : Fin 48) :
    fv y (third i j) = fv x (third i j) ↔ ∃ t < 2 * M i j, y = roll r (alternatingWord i j t) x := by
  obtain ⟨hn, hl⟩ := corner_q x i j hij
  rw [mem_iff_of_card (fun y => fv y (third i j) = fv x (third i j)) _ hn
    (by simpa using hl) (by simpa using valence_q x i j hij)]
  simp [eq_comm]

/-- **The rolling law on the disdyakis dodecahedron.** Two shortest rolls between the same two faces
are joined by corner moves. -/
theorem rolling_law {f g : Fin 48} {ω ω' : List (Fin 3)} (h : model.ShortestRoll f g ω)
    (h' : model.ShortestRoll f g ω') : BraidEq M ω ω' :=
  model.rolling_law cs lifts h h'

/-- Every roll is brought to a shortest roll between the same two faces by corner moves and
cancelling back-and-forth rolls. -/
theorem rolling_reduce (f : Fin 48) (ω : List (Fin 3)) :
    ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧ model.ShortestRoll f (roll r ω f) ω' :=
  model.rolling_reduce cs lifts f ω

/-- Between any two faces there is a shortest roll of at most 9 rolls. -/
theorem exists_shortestRoll_le (f g : Fin 48) : ∃ ω, model.ShortestRoll f g ω ∧ ω.length ≤ 9 := by
  obtain ⟨ω, h, w, hw⟩ := model.exists_shortestRoll cs lifts f g
  exact ⟨ω, h, hw ▸ length_le w⟩

/-- Some shortest roll needs exactly 9 rolls (from face 0 to the opposite face). -/
theorem exists_shortestRoll_eq : ∃ g ω, model.ShortestRoll 0 g ω ∧ ω.length = 9 := by
  obtain ⟨x, hx, -⟩ := d_top
  refine ⟨x, model.sw x, ⟨model.roll_sw x, fun η hη => ?_⟩, by rw [model.length_sw, hx]⟩
  rw [model.length_sw, ← hη]; exact model.d_le_length η

end B3

/-! ## H3: the disdyakis triacontahedron -/
namespace H3
open Die

/-- vertex direction `V v` -/
def vtx (v : Fin 62) : List Q5 := Data.H3.vert.getD v.val []
/-- vertex type -/
def ty (v : Fin 62) : Fin 3 := ⟨(Data.H3.vtype.getD v.val 0) % 3, Nat.mod_lt _ (by decide)⟩
/-- the height `c` of the vertex's type -/
def ht (v : Fin 62) : Q5 := Data.H3.height.getD (ty v).val Q5.zero
/-- face normal `n x` -/
def nrm (x : Fin 120) : List Q5 := Data.H3.normal.getD x.val []
/-- the vertex of type `k` of face `x` -/
def fv (x : Fin 120) (k : Fin 3) : Fin 62 :=
  ⟨((Data.H3.fv.getD x.val []).getD k.val 0) % 62, Nat.mod_lt _ (by decide)⟩

theorem heights_pos : ∀ v, 0 < (ht v).toReal := by
  have h : ∀ v, Q5.le (ht v) Q5.zero = false := by decide +kernel
  intro v; simpa [Q5.toReal, Q5.zero] using Q5.lt_of_le_false (h v)

theorem support_q : ∀ (x : Fin 120) (v : Fin 62), if fv x (ty v) = v then Q5.dot (nrm x) (vtx v) = ht v
    else (Q5.le (ht v) (Q5.dot (nrm x) (vtx v)) = false ∧ Q5.le (Q5.dot (nrm x) (vtx v)) (ht v) = true) := by
  decide +kernel

/-- Every listed face lies in a supporting plane of the die and contains exactly its three vertices. -/
theorem support (x : Fin 120) (v : Fin 62) :
    Q5.rdot (nrm x) (vtx v) ≤ (ht v).toReal ∧
    (Q5.rdot (nrm x) (vtx v) = (ht v).toReal ↔ fv x (ty v) = v) := by
  rw [← Q5.toReal_dot]; exact support_of (support_q x v)

theorem fv_type : ∀ (x : Fin 120) (k : Fin 3), ty (fv x k) = k := by decide +kernel

/-- Rolling across the edge of type `i` keeps exactly the vertices of the other two types. -/
theorem roll_edge : ∀ (x : Fin 120) (i k : Fin 3), fv (r i x) k = fv x k ↔ k ≠ i := by
  decide +kernel

theorem corner_q : ∀ (x : Fin 120) (i j : Fin 3), i ≠ j →
    ((List.range (2 * M i j)).map fun t => roll r (alternatingWord i j t) x).Nodup ∧
    (∀ t < 2 * M i j, fv (roll r (alternatingWord i j t) x) (third i j) = fv x (third i j)) := by
  decide +kernel

theorem valence_q : ∀ (x : Fin 120) (i j : Fin 3), i ≠ j →
    (Finset.univ.filter fun y => fv y (third i j) = fv x (third i j)).card = 2 * M i j := by
  decide +kernel

/-- **Corners are rank-2 cosets.** The faces at the corner of type `third i j` of face `x`
are exactly the `2 m(i,j)` faces reached from `x` by rolling round it with `i, j`. -/
theorem corner (x : Fin 120) (i j : Fin 3) (hij : i ≠ j) (y : Fin 120) :
    fv y (third i j) = fv x (third i j) ↔ ∃ t < 2 * M i j, y = roll r (alternatingWord i j t) x := by
  obtain ⟨hn, hl⟩ := corner_q x i j hij
  rw [mem_iff_of_card (fun y => fv y (third i j) = fv x (third i j)) _ hn
    (by simpa using hl) (by simpa using valence_q x i j hij)]
  simp [eq_comm]

/-- **The rolling law on the disdyakis triacontahedron.** Two shortest rolls between the same two faces
are joined by corner moves. -/
theorem rolling_law {f g : Fin 120} {ω ω' : List (Fin 3)} (h : model.ShortestRoll f g ω)
    (h' : model.ShortestRoll f g ω') : BraidEq M ω ω' :=
  model.rolling_law cs lifts h h'

/-- Every roll is brought to a shortest roll between the same two faces by corner moves and
cancelling back-and-forth rolls. -/
theorem rolling_reduce (f : Fin 120) (ω : List (Fin 3)) :
    ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧ model.ShortestRoll f (roll r ω f) ω' :=
  model.rolling_reduce cs lifts f ω

/-- Between any two faces there is a shortest roll of at most 15 rolls. -/
theorem exists_shortestRoll_le (f g : Fin 120) : ∃ ω, model.ShortestRoll f g ω ∧ ω.length ≤ 15 := by
  obtain ⟨ω, h, w, hw⟩ := model.exists_shortestRoll cs lifts f g
  exact ⟨ω, h, hw ▸ length_le w⟩

/-- Some shortest roll needs exactly 15 rolls (from face 0 to the opposite face). -/
theorem exists_shortestRoll_eq : ∃ g ω, model.ShortestRoll 0 g ω ∧ ω.length = 15 := by
  obtain ⟨x, hx, -⟩ := d_top
  refine ⟨x, model.sw x, ⟨model.roll_sw x, fun η hη => ?_⟩, by rw [model.length_sw, hx]⟩
  rw [model.length_sw, ← hη]; exact model.d_le_length η

end H3

end RollingLaw
