module

public import YantraCert.KBoxData
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

/-! The Krawczyk box's polynomials are the stored main-chart equations (kernel checks). -/

namespace YantraCert.Deriv.KKBox
open YantraCert YantraCert.Deriv

theorem k0 : ZP.eqv (ZP.ofSP YantraCert.KBox.P0) Fm_G = true := by decide +kernel
theorem k1 : ZP.eqv (ZP.ofSP YantraCert.KBox.P1) Fm_H1 = true := by decide +kernel
theorem k2 : ZP.eqv (ZP.ofSP YantraCert.KBox.P2) Fm_D = true := by decide +kernel

end YantraCert.Deriv.KKBox
