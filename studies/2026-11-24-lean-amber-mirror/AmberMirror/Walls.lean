import AmberMirror.Data

/-! Each wall's mirror, written out: `x b = mirror … (x a)` gives three linear equations with
coefficients in ℚ(√5) (generated; every coefficient checked by `linear_combination`). -/

namespace AmberMirror
noncomputable section

/-- wall 0 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w0_flat : V3.dot (nrm w0.c0 w0.c1 w0.c3) (V3.sub w0.c2 w0.c0) = 0 := by
  simp only [w0, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w0_eq (x : ℕ → V3) (h : x w0.b = mirror w0.c0 w0.c1 w0.c3 (x w0.a)) :
    (x 200).x = ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).y + ((1/2:ℝ))*(x 0).z + ((4:ℝ) + (2:ℝ)*s) ∧
    (x 200).y = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).x + ((1/2:ℝ))*(x 0).y + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).z + ((-3:ℝ) + (-1:ℝ)*s) ∧
    (x 200).z = ((1/2:ℝ))*(x 0).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).z + ((-1:ℝ) + (-1:ℝ)*s) := by
  simp only [w0] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 0).x + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 0).y + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 0).z + ((1/4:ℝ))*(x 200).x + ((85/128:ℝ) + (3/64:ℝ)*s + (-5/32:ℝ)*s^2 + (-3/64:ℝ)*s^3 + (-1/128:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 0).x + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 0).y + ((1/8:ℝ))*(x 0).z + ((1/4:ℝ))*(x 200).y + ((-21/64:ℝ) + (15/64:ℝ)*s + (5/64:ℝ)*s^2 + (1/64:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/16:ℝ) + (-1/16:ℝ)*s)*(x 0).x + ((1/8:ℝ))*(x 0).y + ((-1/4:ℝ))*(x 0).z + ((1/4:ℝ))*(x 200).z + ((11/32:ℝ) + (1/8:ℝ)*s + (1/32:ℝ)*s^2)) * hs

/-- wall 1 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w1_flat : V3.dot (nrm w1.c0 w1.c1 w1.c3) (V3.sub w1.c2 w1.c0) = 0 := by
  simp only [w1, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w1_eq (x : ℕ → V3) (h : x w1.b = mirror w1.c0 w1.c1 w1.c3 (x w1.a)) :
    (x 243).x = ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).y + ((1/2:ℝ))*(x 0).z + ((7/2:ℝ) + (3/2:ℝ)*s) ∧
    (x 243).y = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).x + ((1/2:ℝ))*(x 0).y + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).z + ((-2:ℝ) + (-1:ℝ)*s) ∧
    (x 243).z = ((1/2:ℝ))*(x 0).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).z + ((-3/2:ℝ) + (-1/2:ℝ)*s) := by
  simp only [w1] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 0).x + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 0).y + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 0).z + ((1/4:ℝ))*(x 243).x + ((77/128:ℝ) + (3/64:ℝ)*s + (-3/32:ℝ)*s^2 + (-3/64:ℝ)*s^3 + (-1/128:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 0).x + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 0).y + ((1/8:ℝ))*(x 0).z + ((1/4:ℝ))*(x 243).y + ((-13/64:ℝ) + (7/64:ℝ)*s + (5/64:ℝ)*s^2 + (1/64:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/16:ℝ) + (-1/16:ℝ)*s)*(x 0).x + ((1/8:ℝ))*(x 0).y + ((-1/4:ℝ))*(x 0).z + ((1/4:ℝ))*(x 243).z + ((3/32:ℝ) + (1/8:ℝ)*s + (1/32:ℝ)*s^2)) * hs

/-- wall 3 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w3_flat : V3.dot (nrm w3.c0 w3.c1 w3.c3) (V3.sub w3.c2 w3.c0) = 0 := by
  simp only [w3, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w3_eq (x : ℕ → V3) (h : x w3.b = mirror w3.c0 w3.c1 w3.c3 (x w3.a)) :
    (x 85).x = ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 0).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).y + ((-1/2:ℝ))*(x 0).z + ((2:ℝ) + (1:ℝ)*s) ∧
    (x 85).y = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).x + ((1/2:ℝ))*(x 0).y + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 0).z + ((-3/2:ℝ) + (-1/2:ℝ)*s) ∧
    (x 85).z = ((-1/2:ℝ))*(x 0).x + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 0).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 0).z + ((1/2:ℝ) + (1/2:ℝ)*s) := by
  simp only [w3] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 0).x + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 0).y + ((-1/16:ℝ) + (1/16:ℝ)*s)*(x 0).z + ((1/4:ℝ))*(x 85).x + ((53/128:ℝ) + (11/64:ℝ)*s + (-1/32:ℝ)*s^2 + (-3/64:ℝ)*s^3 + (-1/128:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 0).x + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 0).y + ((-1/8:ℝ))*(x 0).z + ((1/4:ℝ))*(x 85).y + ((-21/64:ℝ) + (-1/64:ℝ)*s + (5/64:ℝ)*s^2 + (1/64:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((-1/16:ℝ) + (1/16:ℝ)*s)*(x 0).x + ((-1/8:ℝ))*(x 0).y + ((-1/4:ℝ))*(x 0).z + ((1/4:ℝ))*(x 85).z + ((5/32:ℝ) + (-1/8:ℝ)*s + (-1/32:ℝ)*s^2)) * hs

/-- wall 4 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w4_flat : V3.dot (nrm w4.c0 w4.c1 w4.c3) (V3.sub w4.c2 w4.c0) = 0 := by
  simp only [w4, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w4_eq (x : ℕ → V3) (h : x w4.b = mirror w4.c0 w4.c1 w4.c3 (x w4.a)) :
    (x 26).x = ((-1:ℝ))*(x 0).x + ((1:ℝ) + (1:ℝ)*s) ∧
    (x 26).y = ((1:ℝ))*(x 0).y ∧
    (x 26).z = ((1:ℝ))*(x 0).z := by
  simp only [w4] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((1:ℝ))) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-1/2:ℝ) + (1/4:ℝ)*s)*(x 0).x + ((1/4:ℝ))*(x 26).x + ((1/8:ℝ) + (-1/8:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((-1/4:ℝ))*(x 0).y + ((1/4:ℝ))*(x 26).y) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((-1/4:ℝ))*(x 0).z + ((1/4:ℝ))*(x 26).z) * hs

/-- wall 152 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w152_flat : V3.dot (nrm w152.c0 w152.c1 w152.c3) (V3.sub w152.c2 w152.c0) = 0 := by
  simp only [w152, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w152_eq (x : ℕ → V3) (h : x w152.b = mirror w152.c0 w152.c1 w152.c3 (x w152.a)) :
    (x 188).x = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 26).x + ((-1/2:ℝ))*(x 26).y + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 26).z + ((-1:ℝ)) ∧
    (x 188).y = ((-1/2:ℝ))*(x 26).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 26).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 26).z + ((-3/2:ℝ) + (-1/2:ℝ)*s) ∧
    (x 188).z = ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 26).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 26).y + ((1/2:ℝ))*(x 26).z + ((1/2:ℝ) + (1/2:ℝ)*s) := by
  simp only [w152] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((1/4:ℝ))*(x 188).x + ((-1/4:ℝ))*(x 26).x + ((-1/16:ℝ) + (1/16:ℝ)*s)*(x 26).y + ((-1/8:ℝ))*(x 26).z + ((-5/16:ℝ) + (1/16:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/4:ℝ))*(x 188).y + ((-1/16:ℝ) + (1/16:ℝ)*s)*(x 26).x + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 26).y + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 26).z + ((-21/64:ℝ) + (-5/32:ℝ)*s + (-1/16:ℝ)*s^2 + (1/32:ℝ)*s^3 + (1/64:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/4:ℝ))*(x 188).z + ((-1/8:ℝ))*(x 26).x + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 26).y + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 26).z + ((5/32:ℝ) + (5/32:ℝ)*s + (-1/32:ℝ)*s^2 + (-1/32:ℝ)*s^3)) * hs

/-- wall 176 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w176_flat : V3.dot (nrm w176.c0 w176.c1 w176.c3) (V3.sub w176.c2 w176.c0) = 0 := by
  simp only [w176, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w176_eq (x : ℕ → V3) (h : x w176.b = mirror w176.c0 w176.c1 w176.c3 (x w176.a)) :
    (x 273).x = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 33).x + ((1/2:ℝ))*(x 33).y + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 33).z + ((1:ℝ)) ∧
    (x 273).y = ((1/2:ℝ))*(x 33).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 33).y + ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 33).z + ((-3/2:ℝ) + (-1/2:ℝ)*s) ∧
    (x 273).z = ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 33).x + ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 33).y + ((1/2:ℝ))*(x 33).z + ((-1/2:ℝ) + (-1/2:ℝ)*s) := by
  simp only [w176] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((1/4:ℝ))*(x 273).x + ((-1/4:ℝ))*(x 33).x + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 33).y + ((-1/8:ℝ))*(x 33).z + ((1/8:ℝ) + (-1/8:ℝ)*s)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/4:ℝ))*(x 273).y + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 33).x + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 33).y + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 33).z + ((-9/32:ℝ) + (-1/32:ℝ)*s + (1/32:ℝ)*s^2 + (1/32:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/4:ℝ))*(x 273).z + ((-1/8:ℝ))*(x 33).x + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 33).y + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 33).z + ((-1/16:ℝ) + (1/16:ℝ)*s^2)) * hs

/-- wall 346 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w346_flat : V3.dot (nrm w346.c0 w346.c1 w346.c3) (V3.sub w346.c2 w346.c0) = 0 := by
  simp only [w346, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w346_eq (x : ℕ → V3) (h : x w346.b = mirror w346.c0 w346.c1 w346.c3 (x w346.a)) :
    (x 200).x = ((1:ℝ))*(x 85).x ∧
    (x 200).y = ((1:ℝ))*(x 85).y ∧
    (x 200).z = ((-1:ℝ))*(x 85).z + ((-4:ℝ) + (-2:ℝ)*s) := by
  simp only [w346] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((1:ℝ))) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((1/4:ℝ))*(x 200).x + ((-1/4:ℝ))*(x 85).x) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/4:ℝ))*(x 200).y + ((-1/4:ℝ))*(x 85).y) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/4:ℝ))*(x 200).z + ((-1/2:ℝ) + (1/4:ℝ)*s)*(x 85).z + ((-1/2:ℝ) + (1/4:ℝ)*s + (1/4:ℝ)*s^2)) * hs

/-- wall 347 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w347_flat : V3.dot (nrm w347.c0 w347.c1 w347.c3) (V3.sub w347.c2 w347.c0) = 0 := by
  simp only [w347, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w347_eq (x : ℕ → V3) (h : x w347.b = mirror w347.c0 w347.c1 w347.c3 (x w347.a)) :
    (x 321).x = ((1:ℝ))*(x 85).x ∧
    (x 321).y = ((1:ℝ))*(x 85).y ∧
    (x 321).z = ((-1:ℝ))*(x 85).z + ((-3:ℝ) + (-1:ℝ)*s) := by
  simp only [w347] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((1:ℝ))) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((1/4:ℝ))*(x 321).x + ((-1/4:ℝ))*(x 85).x) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/4:ℝ))*(x 321).y + ((-1/4:ℝ))*(x 85).y) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/4:ℝ))*(x 321).z + ((-1/2:ℝ) + (1/4:ℝ)*s)*(x 85).z + ((-3/8:ℝ) + (1/4:ℝ)*s + (1/8:ℝ)*s^2)) * hs

/-- wall 348 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w348_flat : V3.dot (nrm w348.c0 w348.c1 w348.c3) (V3.sub w348.c2 w348.c0) = 0 := by
  simp only [w348, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w348_eq (x : ℕ → V3) (h : x w348.b = mirror w348.c0 w348.c1 w348.c3 (x w348.a)) :
    (x 165).x = ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 85).x + ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 85).y + ((1/2:ℝ))*(x 85).z ∧
    (x 165).y = ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 85).x + ((1/2:ℝ))*(x 85).y + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 85).z ∧
    (x 165).z = ((1/2:ℝ))*(x 85).x + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 85).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 85).z := by
  simp only [w348] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((1/4:ℝ))*(x 165).x + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 85).x + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 85).y + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 85).z + ((-3/128:ℝ) + (-1/64:ℝ)*s + (1/32:ℝ)*s^2 + (1/64:ℝ)*s^3 + (-1/128:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/4:ℝ))*(x 165).y + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 85).x + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 85).y + ((-1/8:ℝ))*(x 85).z + ((-3/64:ℝ) + (1/64:ℝ)*s + (3/64:ℝ)*s^2 + (-1/64:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/4:ℝ))*(x 165).z + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 85).x + ((-1/8:ℝ))*(x 85).y + ((-1/4:ℝ))*(x 85).z + ((3/32:ℝ) + (-1/8:ℝ)*s + (1/32:ℝ)*s^2)) * hs

/-- wall 592 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w592_flat : V3.dot (nrm w592.c0 w592.c1 w592.c3) (V3.sub w592.c2 w592.c0) = 0 := by
  simp only [w592, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w592_eq (x : ℕ → V3) (h : x w592.b = mirror w592.c0 w592.c1 w592.c3 (x w592.a)) :
    (x 188).x = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 165).x + ((1/2:ℝ))*(x 165).y + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 165).z + ((1/2:ℝ) + (1/2:ℝ)*s) ∧
    (x 188).y = ((1/2:ℝ))*(x 165).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 165).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 165).z + ((-2:ℝ) + (-1:ℝ)*s) ∧
    (x 188).z = ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 165).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 165).y + ((1/2:ℝ))*(x 165).z + ((3/2:ℝ) + (1/2:ℝ)*s) := by
  simp only [w592] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-1/4:ℝ))*(x 165).x + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 165).y + ((1/8:ℝ))*(x 165).z + ((1/4:ℝ))*(x 188).x + ((1/16:ℝ) + (-1/16:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/16:ℝ) + (-1/16:ℝ)*s)*(x 165).x + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 165).y + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 165).z + ((1/4:ℝ))*(x 188).y + ((-25/64:ℝ) + (-5/32:ℝ)*s + (1/32:ℝ)*s^3 + (1/64:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/8:ℝ))*(x 165).x + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 165).y + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 165).z + ((1/4:ℝ))*(x 188).z + ((9/32:ℝ) + (1/32:ℝ)*s + (-1/32:ℝ)*s^2 + (-1/32:ℝ)*s^3)) * hs

/-- wall 753 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w753_flat : V3.dot (nrm w753.c0 w753.c1 w753.c3) (V3.sub w753.c2 w753.c0) = 0 := by
  simp only [w753, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w753_eq (x : ℕ → V3) (h : x w753.b = mirror w753.c0 w753.c1 w753.c3 (x w753.a)) :
    (x 273).x = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 229).x + ((1/2:ℝ))*(x 229).y + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 229).z + ((2:ℝ)) ∧
    (x 273).y = ((1/2:ℝ))*(x 229).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 229).y + ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 229).z + ((-3:ℝ) + (-1:ℝ)*s) ∧
    (x 273).z = ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 229).x + ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 229).y + ((1/2:ℝ))*(x 229).z + ((-1:ℝ) + (-1:ℝ)*s) := by
  simp only [w753] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-1/4:ℝ))*(x 229).x + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 229).y + ((-1/8:ℝ))*(x 229).z + ((1/4:ℝ))*(x 273).x + ((5/32:ℝ) + (-1/8:ℝ)*s + (-1/32:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/16:ℝ) + (-1/16:ℝ)*s)*(x 229).x + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 229).y + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 229).z + ((1/4:ℝ))*(x 273).y + ((-69/128:ℝ) + (-3/64:ℝ)*s + (1/32:ℝ)*s^2 + (3/64:ℝ)*s^3 + (1/128:ℝ)*s^4)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((-1/8:ℝ))*(x 229).x + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 229).y + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 229).z + ((1/4:ℝ))*(x 273).z + ((-5/64:ℝ) + (-1/64:ℝ)*s + (5/64:ℝ)*s^2 + (1/64:ℝ)*s^3)) * hs

/-- wall 754 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w754_flat : V3.dot (nrm w754.c0 w754.c1 w754.c3) (V3.sub w754.c2 w754.c0) = 0 := by
  simp only [w754, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w754_eq (x : ℕ → V3) (h : x w754.b = mirror w754.c0 w754.c1 w754.c3 (x w754.a)) :
    (x 243).x = ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 229).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 229).y + ((1/2:ℝ))*(x 229).z + ((2:ℝ) + (1:ℝ)*s) ∧
    (x 243).y = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 229).x + ((1/2:ℝ))*(x 229).y + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 229).z + ((-3/2:ℝ) + (-1/2:ℝ)*s) ∧
    (x 243).z = ((1/2:ℝ))*(x 229).x + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 229).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 229).z + ((-1/2:ℝ) + (-1/2:ℝ)*s) := by
  simp only [w754] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 229).x + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 229).y + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 229).z + ((1/4:ℝ))*(x 243).x + ((11/32:ℝ) + (1/32:ℝ)*s + (-3/32:ℝ)*s^2 + (-1/32:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 229).x + ((-5/16:ℝ) + (1/16:ℝ)*s)*(x 229).y + ((1/8:ℝ))*(x 229).z + ((1/4:ℝ))*(x 243).y + ((-3/16:ℝ) + (1/8:ℝ)*s + (1/16:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/16:ℝ) + (-1/16:ℝ)*s)*(x 229).x + ((1/8:ℝ))*(x 229).y + ((-1/4:ℝ))*(x 229).z + ((1/4:ℝ))*(x 243).z + ((1/8:ℝ) + (1/8:ℝ)*s)) * hs

/-- wall 793 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w793_flat : V3.dot (nrm w793.c0 w793.c1 w793.c3) (V3.sub w793.c2 w793.c0) = 0 := by
  simp only [w793, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w793_eq (x : ℕ → V3) (h : x w793.b = mirror w793.c0 w793.c1 w793.c3 (x w793.a)) :
    (x 351).x = ((1/2:ℝ))*(x 243).x + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 243).y + ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 243).z ∧
    (x 351).y = ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 243).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 243).y + ((1/2:ℝ))*(x 243).z ∧
    (x 351).z = ((-1/4:ℝ) + (-1/4:ℝ)*s)*(x 243).x + ((1/2:ℝ))*(x 243).y + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 243).z := by
  simp only [w793] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-5/16:ℝ) + (1/16:ℝ)*s)*(x 243).x + ((-1/8:ℝ))*(x 243).y + ((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 243).z + ((1/4:ℝ))*(x 351).x + ((-9/64:ℝ) + (-9/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((-1/8:ℝ))*(x 243).x + ((-1/4:ℝ))*(x 243).y + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 243).z + ((1/4:ℝ))*(x 351).y + ((9/32:ℝ) + (-1/32:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((-1/32:ℝ) + (1/32:ℝ)*s^2)*(x 243).x + ((1/16:ℝ) + (-1/16:ℝ)*s)*(x 243).y + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 243).z + ((1/4:ℝ))*(x 351).z + ((-9/128:ℝ) + (-9/64:ℝ)*s + (-1/16:ℝ)*s^2 + (1/64:ℝ)*s^3 + (1/128:ℝ)*s^4)) * hs

/-- wall 933 is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/
theorem w933_flat : V3.dot (nrm w933.c0 w933.c1 w933.c3) (V3.sub w933.c2 w933.c0) = 0 := by
  simp only [w933, nrm, V3.dot, V3.cross, V3.sub, proj, φ]; ring
theorem w933_eq (x : ℕ → V3) (h : x w933.b = mirror w933.c0 w933.c1 w933.c3 (x w933.a)) :
    (x 351).x = ((1/2:ℝ))*(x 321).x + ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 321).y + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 321).z + ((2:ℝ) + (1:ℝ)*s) ∧
    (x 351).y = ((-1/4:ℝ) + (1/4:ℝ)*s)*(x 321).x + ((1/4:ℝ) + (1/4:ℝ)*s)*(x 321).y + ((-1/2:ℝ))*(x 321).z + ((-3/2:ℝ) + (-1/2:ℝ)*s) ∧
    (x 351).z = ((1/4:ℝ) + (1/4:ℝ)*s)*(x 321).x + ((-1/2:ℝ))*(x 321).y + ((1/4:ℝ) + (-1/4:ℝ)*s)*(x 321).z + ((-7/2:ℝ) + (-3/2:ℝ)*s) := by
  simp only [w933] at h
  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := ((6:ℝ) + (2:ℝ)*s))
    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination (((15/16:ℝ) + (1/4:ℝ)*s + (1/16:ℝ)*s^2)) * hs)
    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)
  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez
  refine ⟨?_, ?_, ?_⟩
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ex + (((-5/16:ℝ) + (1/16:ℝ)*s)*(x 321).x + ((-1/8:ℝ))*(x 321).y + ((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 321).z + ((1/4:ℝ))*(x 351).x + ((13/64:ℝ) + (-7/64:ℝ)*s + (-5/64:ℝ)*s^2 + (-1/64:ℝ)*s^3)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ey + (((-1/8:ℝ))*(x 321).x + ((-1/4:ℝ))*(x 321).y + ((-1/16:ℝ) + (1/16:ℝ)*s)*(x 321).z + ((1/4:ℝ))*(x 351).y + ((3/32:ℝ) + (1/8:ℝ)*s + (1/32:ℝ)*s^2)) * hs
  · linear_combination ((3/8:ℝ) + (-1/8:ℝ)*s) * ez + (((1/32:ℝ) + (-1/32:ℝ)*s^2)*(x 321).x + ((-1/16:ℝ) + (1/16:ℝ)*s)*(x 321).y + ((-25/64:ℝ) + (-1/64:ℝ)*s + (1/64:ℝ)*s^2 + (1/64:ℝ)*s^3)*(x 321).z + ((1/4:ℝ))*(x 351).z + ((-77/128:ℝ) + (-3/64:ℝ)*s + (3/32:ℝ)*s^2 + (3/64:ℝ)*s^3 + (1/128:ℝ)*s^4)) * hs

end
end AmberMirror
