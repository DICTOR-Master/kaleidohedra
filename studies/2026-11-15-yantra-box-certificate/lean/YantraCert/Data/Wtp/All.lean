module

public import YantraCert.Cover
public import YantraCert.Data.Wtp.Polys
public import YantraCert.Data.Wtp.P0
public import YantraCert.Data.Wtp.P1
public import YantraCert.Data.Wtp.P2
public import YantraCert.Data.Wtp.P3
public import YantraCert.Data.Wtp.P4
public import YantraCert.Data.Wtp.P5
public import YantraCert.Data.Wtp.P6
public import YantraCert.Data.Wtp.P7
public import YantraCert.Data.Wtp.P8
public import YantraCert.Data.Wtp.P9
public import YantraCert.Data.Wtp.P10

@[expose] public section

/-! Chart Wt+: the whole bisection tree covers the unit cube (assembled from 11 subtree files). -/

namespace YantraCert.Data.Wtp
open YantraCert

theorem f0 : C.Covered P0.cell := checkTree_sound C C_deg 13 P0.cell P0.codes P0.ok
theorem f1 : C.Covered P1.cell := checkTree_sound C C_deg 4 P1.cell P1.codes P1.ok
theorem f2 : C.Covered P2.cell := checkTree_sound C C_deg 9 P2.cell P2.codes P2.ok
theorem f3 : C.Covered P3.cell := checkTree_sound C C_deg 6 P3.cell P3.codes P3.ok
theorem f4 : C.Covered P4.cell := checkTree_sound C C_deg 8 P4.cell P4.codes P4.ok
theorem f5 : C.Covered P5.cell := checkTree_sound C C_deg 9 P5.cell P5.codes P5.ok
theorem f6 : C.Covered P6.cell := checkTree_sound C C_deg 5 P6.cell P6.codes P6.ok
theorem f7 : C.Covered P7.cell := checkTree_sound C C_deg 2 P7.cell P7.codes P7.ok
theorem f8 : C.Covered P8.cell := checkTree_sound C C_deg 8 P8.cell P8.codes P8.ok
theorem f9 : C.Covered P9.cell := checkTree_sound C C_deg 8 P9.cell P9.codes P9.ok
theorem f10 : C.Covered P10.cell := checkTree_sound C C_deg 9 P10.cell P10.codes P10.ok
theorem t0 : C.Covered ⟨2, 2, 2, 3, 2, 2⟩ := C.covered_split _ f4 f5
theorem t1 : C.Covered ⟨2, 3, 2, 3, 2, 2⟩ := C.covered_split _ f8 f9
theorem t2 : C.Covered ⟨2, 2, 2, 3, 1, 1⟩ := C.covered_split _ t0 f6
theorem t3 : C.Covered ⟨2, 3, 2, 3, 1, 1⟩ := C.covered_split _ t1 f10
theorem t4 : C.Covered ⟨2, 2, 1, 1, 1, 1⟩ := C.covered_split _ f3 t2
theorem t5 : C.Covered ⟨2, 3, 1, 1, 1, 1⟩ := C.covered_split _ f7 t3
theorem t6 : C.Covered ⟨1, 1, 1, 1, 1, 1⟩ := C.covered_split _ t4 t5
theorem t7 : C.Covered ⟨1, 1, 1, 1, 0, 0⟩ := C.covered_split _ f2 t6
theorem t8 : C.Covered ⟨1, 1, 0, 0, 0, 0⟩ := C.covered_split _ f1 t7
theorem t9 : C.Covered ⟨0, 0, 0, 0, 0, 0⟩ := C.covered_split _ f0 t8

/-- every point of the unit cube is `Good` for this chart -/
theorem covered : C.Covered ⟨0, 0, 0, 0, 0, 0⟩ := t9

end YantraCert.Data.Wtp
