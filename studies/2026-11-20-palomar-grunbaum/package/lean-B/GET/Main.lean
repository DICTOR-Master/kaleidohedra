module

public import GET.SphereB

@[expose] public section

/-! The assembled facts about GET B: a polyhedron of spherical type whose 30 faces are congruent golden rhombi,
every zone of 10 faces, tiling space face to face by the translates of its lattice. -/

namespace GET

open ZPhi GrunbaumK10 Set
open scoped Pointwise

/-- faces that meet properly have different carriers -/
theorem carrier_ne_of_meet {F G : Parallelogram} (hF : F.Nondegenerate) (h : MeetProperly F G) :
    F.carrier ≠ G.carrier := by
  intro heq
  have hm : ∀ a, F.corners a ∈ F.carrier ∩ G.carrier := fun a =>
    ⟨corner_mem_carrier F a, heq ▸ corner_mem_carrier F a⟩
  have hu : F.u ≠ 0 := hF.ne_zero 0
  rcases h with h | ⟨a, b, _, h⟩ | ⟨a, b, _, h⟩
  · have := hm 0; rw [h] at this; exact this
  · have h0 := hm 0; have h1 := hm 1
    rw [h, mem_singleton_iff] at h0 h1
    apply hu
    have : F.corners 1 = F.corners 0 := h1.trans h0.symm
    simpa [Parallelogram.corners] using this
  · have h0 := hm 0; have h1 := hm 1; have h3 := hm 3
    rw [h] at h0 h1 h3
    unfold Parallelogram.side at h0 h1 h3
    have c0 : F.corners 0 = F.p := rfl
    have c1 : F.corners 1 = F.p + F.u := rfl
    have c3 : F.corners 3 = F.p + F.v := rfl
    rw [c0] at h0
    rw [c1] at h1
    rw [c3] at h3
    generalize F.corners a = x at h0 h1 h3
    generalize F.corners (a + 1) = y at h0 h1 h3
    rw [segment_eq_image'] at h0 h1 h3
    obtain ⟨α, _, hα⟩ := h0
    obtain ⟨β, _, hβ⟩ := h1
    obtain ⟨γ, _, hγ⟩ := h3
    beta_reduce at hα hβ hγ
    have eu : F.u = (β - α) • (y - x) := by
      rw [show F.u = (F.p + F.u) - F.p by abel, ← hβ, ← hα]; module
    have ev' : F.v = (γ - α) • (y - x) := by
      rw [show F.v = (F.p + F.v) - F.p by abel, ← hγ, ← hα]; module
    have e : (γ - α) • F.u + (-(β - α)) • F.v = 0 := by rw [eu, ev']; module
    have := LinearIndependent.pair_iff.mp hF _ _ e
    apply hu
    rw [eu, show β - α = 0 by linarith [this.2], zero_smul]

theorem FB_distinct : ∀ i j, (FB i).carrier = (FB j).carrier → i = j := by
  intro i j h
  by_contra hij
  exact carrier_ne_of_meet (FB_golden i).1.1 (FB_meet i j hij) h

theorem FB_faceToFace : FaceToFace FB (lattice bB) := by
  intro i
  exact ⟨lat (MB i).2, lat_mem _, lat_ne_zero (MB_ok i).2.2.2, (MB i).1, FB_match i⟩

/-- GET B is a polyhedron of spherical type with the faces `FB` -/
theorem PB_spherical : IsSphericalPolyhedron PB FB where
  compact := isCompact_PB
  closure_interior := PB_closure_interior
  frontier_eq := PB_frontier
  nondegenerate := fun i => (FB_golden i).1.1
  distinct := FB_distinct
  meet := FB_meet
  sphere := PB_sphere
  not_coplanar := FB_not_coplanar

theorem PB_tiles : TilesByTranslates PB (lattice bB) := ⟨PB_cover, PB_disjoint⟩

end GET
