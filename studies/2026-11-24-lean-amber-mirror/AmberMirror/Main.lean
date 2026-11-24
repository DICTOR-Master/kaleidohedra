import AmberMirror.Walls

/-! Theorem 3 (iv) of paper #118: the three odd edges of one rhombic face (wall 3). -/

namespace AmberMirror
noncomputable section

/-- the mirror-plane condition of odd edge 1, exactly the row printed by odd_edges.py: ['-3/4+-1/4r5', '1/4+1/4r5', '-1/2', '3/2+1/2r5'] -/
def plane1 (p : V3) : Prop := ((-3/4:ℝ) + (-1/4:ℝ)*s)*p.x + ((1/4:ℝ) + (1/4:ℝ)*s)*p.y + ((-1/2:ℝ))*p.z = ((3/2:ℝ) + (1/2:ℝ)*s)
/-- the mirror-plane condition of odd edge 2, exactly the row printed by odd_edges.py: ['0', '0', '-2', '1+1r5'] -/
def plane2 (p : V3) : Prop := ((-2:ℝ))*p.z = ((1:ℝ) + (1:ℝ)*s)
/-- the mirror-plane condition of odd edge 3, exactly the row printed by odd_edges.py: ['-3/4+-1/4r5', '1/4+1/4r5', '1/2', '3/2+1/2r5'] -/
def plane3 (p : V3) : Prop := ((-3/4:ℝ) + (-1/4:ℝ)*s)*p.x + ((1/4:ℝ) + (1/4:ℝ)*s)*p.y + ((1/2:ℝ))*p.z = ((3/2:ℝ) + (1/2:ℝ)*s)

/-- odd edge 1 (5 cells round it): if every two neighbouring cores along the tree path and round the edge are mirror images in their shared wall, the core of the start cell 33 lies on plane 1. -/
theorem edge1_plane (x : ℕ → V3) (h : ∀ w ∈ edgeWalls1, x w.b = mirror w.c0 w.c1 w.c3 (x w.a)) :
    plane1 (x 33) := by
  obtain ⟨h176x, h176y, h176z⟩ := w176_eq x (h w176 (by simp [edgeWalls1]))
  obtain ⟨h753x, h753y, h753z⟩ := w753_eq x (h w753 (by simp [edgeWalls1]))
  obtain ⟨h754x, h754y, h754z⟩ := w754_eq x (h w754 (by simp [edgeWalls1]))
  obtain ⟨h1x, h1y, h1z⟩ := w1_eq x (h w1 (by simp [edgeWalls1]))
  obtain ⟨h3x, h3y, h3z⟩ := w3_eq x (h w3 (by simp [edgeWalls1]))
  obtain ⟨h348x, h348y, h348z⟩ := w348_eq x (h w348 (by simp [edgeWalls1]))
  obtain ⟨h592x, h592y, h592z⟩ := w592_eq x (h w592 (by simp [edgeWalls1]))
  obtain ⟨h152x, h152y, h152z⟩ := w152_eq x (h w152 (by simp [edgeWalls1]))
  obtain ⟨h4x, h4y, h4z⟩ := w4_eq x (h w4 (by simp [edgeWalls1]))
  unfold plane1
  linear_combination ((1/4:ℝ) + (1/4:ℝ)*s) * h176x + ((1/2:ℝ)) * h176y + ((3/4:ℝ) + (1/4:ℝ)*s) * h176z + ((-1/4:ℝ) + (-1/4:ℝ)*s) * h753x + ((-1/2:ℝ)) * h753y + ((-3/4:ℝ) + (-1/4:ℝ)*s) * h753z + ((-1/4:ℝ) + (-1/4:ℝ)*s) * h754x + ((1/2:ℝ)) * h754y + ((3/4:ℝ) + (1/4:ℝ)*s) * h754z + ((1/4:ℝ) + (1/4:ℝ)*s) * h1x + ((-1/2:ℝ)) * h1y + ((-3/4:ℝ) + (-1/4:ℝ)*s) * h1z + ((-1:ℝ)) * h3x + ((-1/4:ℝ) + (1/4:ℝ)*s) * h348x + ((1/4:ℝ) + (1/4:ℝ)*s) * h348y + ((-1/2:ℝ)) * h348z + ((1/4:ℝ) + (1/4:ℝ)*s) * h592x + ((-1/2:ℝ)) * h592y + ((-1/4:ℝ) + (1/4:ℝ)*s) * h592z + ((-1/4:ℝ) + (-1/4:ℝ)*s) * h152x + ((1/2:ℝ)) * h152y + ((1/4:ℝ) + (-1/4:ℝ)*s) * h152z + ((-1:ℝ)) * h4x + (((-1/16:ℝ))*(x 0).x + ((1/8:ℝ))*(x 0).y + ((-1/16:ℝ))*(x 0).z + ((1/16:ℝ))*(x 165).y + ((-1/16:ℝ))*(x 165).z + ((-1/16:ℝ))*(x 229).x + ((-1/16:ℝ))*(x 229).y + ((-1/8:ℝ))*(x 26).x + ((-1/16:ℝ))*(x 26).y + ((-1/16:ℝ))*(x 26).z + ((1/8:ℝ))*(x 33).x + ((-1/16:ℝ))*(x 33).y + ((1/16:ℝ))*(x 33).z + ((-1/8:ℝ))*(x 85).x + ((-1/16:ℝ))*(x 85).y + ((1/16:ℝ))*(x 85).z + ((3/8:ℝ))) * hs

/-- odd edge 2 (3 cells round it): if every two neighbouring cores along the tree path and round the edge are mirror images in their shared wall, the core of the start cell 33 lies on plane 2. -/
theorem edge2_plane (x : ℕ → V3) (h : ∀ w ∈ edgeWalls2, x w.b = mirror w.c0 w.c1 w.c3 (x w.a)) :
    plane2 (x 33) := by
  obtain ⟨h176x, h176y, h176z⟩ := w176_eq x (h w176 (by simp [edgeWalls2]))
  obtain ⟨h753x, h753y, h753z⟩ := w753_eq x (h w753 (by simp [edgeWalls2]))
  obtain ⟨h754x, h754y, h754z⟩ := w754_eq x (h w754 (by simp [edgeWalls2]))
  obtain ⟨h1x, h1y, h1z⟩ := w1_eq x (h w1 (by simp [edgeWalls2]))
  obtain ⟨h0x, h0y, h0z⟩ := w0_eq x (h w0 (by simp [edgeWalls2]))
  obtain ⟨h346x, h346y, h346z⟩ := w346_eq x (h w346 (by simp [edgeWalls2]))
  obtain ⟨h3x, h3y, h3z⟩ := w3_eq x (h w3 (by simp [edgeWalls2]))
  unfold plane2
  linear_combination ((-1/2:ℝ) + (1/2:ℝ)*s) * h176x + ((-1/2:ℝ) + (-1/2:ℝ)*s) * h176y + ((1:ℝ)) * h176z + ((1/2:ℝ) + (-1/2:ℝ)*s) * h753x + ((1/2:ℝ) + (1/2:ℝ)*s) * h753y + ((-1:ℝ)) * h753z + ((1:ℝ)) * h754x + ((1/2:ℝ) + (-1/2:ℝ)*s) * h754y + ((1/2:ℝ) + (1/2:ℝ)*s) * h754z + ((-1:ℝ)) * h1x + ((-1/2:ℝ) + (1/2:ℝ)*s) * h1y + ((-1/2:ℝ) + (-1/2:ℝ)*s) * h1z + ((2:ℝ)) * h0x + ((-2:ℝ)) * h346x + ((-2:ℝ)) * h3x + (((1/8:ℝ))*(x 0).x + ((1/8:ℝ))*(x 0).y + ((-1/4:ℝ))*(x 0).z + ((-1/4:ℝ))*(x 229).x + ((-1/4:ℝ))*(x 229).y + ((1/8:ℝ))*(x 33).x + ((1/8:ℝ))*(x 33).y + ((1/4:ℝ))*(x 33).z + ((-1/2:ℝ))) * hs

/-- odd edge 3 (5 cells round it): if every two neighbouring cores along the tree path and round the edge are mirror images in their shared wall, the core of the start cell 33 lies on plane 3. -/
theorem edge3_plane (x : ℕ → V3) (h : ∀ w ∈ edgeWalls3, x w.b = mirror w.c0 w.c1 w.c3 (x w.a)) :
    plane3 (x 33) := by
  obtain ⟨h176x, h176y, h176z⟩ := w176_eq x (h w176 (by simp [edgeWalls3]))
  obtain ⟨h753x, h753y, h753z⟩ := w753_eq x (h w753 (by simp [edgeWalls3]))
  obtain ⟨h754x, h754y, h754z⟩ := w754_eq x (h w754 (by simp [edgeWalls3]))
  obtain ⟨h1x, h1y, h1z⟩ := w1_eq x (h w1 (by simp [edgeWalls3]))
  obtain ⟨h793x, h793y, h793z⟩ := w793_eq x (h w793 (by simp [edgeWalls3]))
  obtain ⟨h933x, h933y, h933z⟩ := w933_eq x (h w933 (by simp [edgeWalls3]))
  obtain ⟨h347x, h347y, h347z⟩ := w347_eq x (h w347 (by simp [edgeWalls3]))
  obtain ⟨h3x, h3y, h3z⟩ := w3_eq x (h w3 (by simp [edgeWalls3]))
  unfold plane3
  linear_combination ((1/2:ℝ)) * h176x + ((3/4:ℝ) + (1/4:ℝ)*s) * h176y + ((1/4:ℝ) + (1/4:ℝ)*s) * h176z + ((-1/2:ℝ)) * h753x + ((-3/4:ℝ) + (-1/4:ℝ)*s) * h753y + ((-1/4:ℝ) + (-1/4:ℝ)*s) * h753z + ((-3/4:ℝ) + (-1/4:ℝ)*s) * h754x + ((1/4:ℝ) + (1/4:ℝ)*s) * h754y + ((1/2:ℝ)) * h754z + ((1/4:ℝ) + (1/4:ℝ)*s) * h1x + ((1/2:ℝ)) * h1y + ((-3/4:ℝ) + (-1/4:ℝ)*s) * h1z + ((1/4:ℝ) + (1/4:ℝ)*s) * h793x + ((1/2:ℝ)) * h793y + ((3/4:ℝ) + (1/4:ℝ)*s) * h793z + ((-1/4:ℝ) + (-1/4:ℝ)*s) * h933x + ((-1/2:ℝ)) * h933y + ((-3/4:ℝ) + (-1/4:ℝ)*s) * h933z + ((-1/2:ℝ) + (-1/2:ℝ)*s) * h347x + ((-1/2:ℝ) + (-1/2:ℝ)*s) * h3x + (((1/16:ℝ))*(x 0).x + ((-1/16:ℝ))*(x 0).z + ((1/16:ℝ))*(x 229).x + ((1/16:ℝ))*(x 229).y + ((-1/16:ℝ))*(x 243).x + ((1/16:ℝ))*(x 243).y + ((-1/8:ℝ))*(x 243).z + ((-1/16:ℝ))*(x 321).x + ((-1/16:ℝ))*(x 321).y + ((1/16:ℝ))*(x 33).x + ((-1/8:ℝ))*(x 33).y + ((-1/16:ℝ))*(x 33).z) * hs

/-- the algebraic core: the three mirror-plane conditions have no common solution. -/
theorem planes_no_common_point : ¬ ∃ p : V3, plane1 p ∧ plane2 p ∧ plane3 p := by
  rintro ⟨p, h1, h2, h3⟩
  unfold plane1 at h1; unfold plane2 at h2; unfold plane3 at h3
  have : (1:ℝ) = 0 := by
    linear_combination ((-1/2:ℝ) + (1/2:ℝ)*s) * h1 + ((1/4:ℝ) + (-1/4:ℝ)*s) * h2 + ((1/2:ℝ) + (-1/2:ℝ)*s) * h3 + (((-1/4:ℝ))) * hs
  exact one_ne_zero this

/-- the two odd edges with 5 cells round them together force z = 0 -/
theorem plane1_plane3_z (p : V3) (h1 : plane1 p) (h3 : plane3 p) : p.z = 0 := by
  unfold plane1 at h1; unfold plane3 at h3; linear_combination h3 - h1

/-- the odd edge with 3 cells round it forces z = −(1+√5)/2 = −φ -/
theorem plane2_z (p : V3) (h2 : plane2 p) : p.z = -(1 + s)/2 := by
  unfold plane2 at h2; linear_combination (-1/2:ℝ) * h2

/-- **Theorem 3 (iv), certificate form.** No placement of the cores' centres in the cells of the patch makes every two
neighbouring cores mirror images in their shared wall: already the 14 walls of the tree path and of the three odd edges
of wall 3 admit none. -/
theorem no_mirror_placement :
    ¬ ∃ x : ℕ → V3, ∀ w ∈ walls, x w.b = mirror w.c0 w.c1 w.c3 (x w.a) := by
  rintro ⟨x, h⟩
  have sub : ∀ l : List Wall, (∀ w ∈ l, w ∈ walls) → ∀ w ∈ l, x w.b = mirror w.c0 w.c1 w.c3 (x w.a) :=
    fun l hl w hw => h w (hl w hw)
  exact planes_no_common_point ⟨x 33,
    edge1_plane x (sub _ (by simp [edgeWalls1, walls])),
    edge2_plane x (sub _ (by simp [edgeWalls2, walls])),
    edge3_plane x (sub _ (by simp [edgeWalls3, walls]))⟩

end
end AmberMirror
