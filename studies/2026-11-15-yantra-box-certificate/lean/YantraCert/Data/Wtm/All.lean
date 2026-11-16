module

public import YantraCert.Cover
public import YantraCert.Data.Wtm.Polys
public import YantraCert.Data.Wtm.P0

@[expose] public section

/-! Chart Wt-: the whole bisection tree covers the unit cube (assembled from 1 subtree files). -/

namespace YantraCert.Data.Wtm
open YantraCert

theorem f0 : C.Covered P0.cell := checkTree_sound C C_deg 9 P0.cell P0.codes P0.ok

/-- every point of the unit cube is `Good` for this chart -/
theorem covered : C.Covered ⟨0, 0, 0, 0, 0, 0⟩ := f0

end YantraCert.Data.Wtm
