module

public import YantraCert.Cover
public import YantraCert.Data.W.Polys
public import YantraCert.Data.W.P0
public import YantraCert.Data.W.P1

@[expose] public section

/-! Chart W: the whole bisection tree covers the unit cube (assembled from 2 subtree files). -/

namespace YantraCert.Data.W
open YantraCert

theorem f0 : C.Covered P0.cell := checkTree_sound C C_deg 13 P0.cell P0.codes P0.ok
theorem f1 : C.Covered P1.cell := checkTree_sound C C_deg 10 P1.cell P1.codes P1.ok
theorem t0 : C.Covered ⟨0, 0, 0, 0, 0, 0⟩ := C.covered_split _ f0 f1

/-- every point of the unit cube is `Good` for this chart -/
theorem covered : C.Covered ⟨0, 0, 0, 0, 0, 0⟩ := t0

end YantraCert.Data.W
