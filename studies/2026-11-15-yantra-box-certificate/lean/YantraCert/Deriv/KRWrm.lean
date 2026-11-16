module

public import YantraCert.Data.Wrm.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RWrm
open YantraCert YantraCert.Deriv

theorem deg_F0 : FcWrm_G.degLE 10 10 0 = true := by decide +kernel
theorem res_F0 : ZP.eqv (ZP.mul (ZP.const 1073741824) (ZP.ofSP YantraCert.Data.Wrm.F0)) (ZP.mul (ZP.const 67108864) (ZP.scaleW 3 8 10 1 1 10 2 1 0 FcWrm_G)) = true := by decide +kernel

end YantraCert.Deriv.RWrm
