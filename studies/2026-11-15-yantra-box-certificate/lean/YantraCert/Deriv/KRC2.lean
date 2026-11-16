module

public import YantraCert.Data.C2.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RC2
open YantraCert YantraCert.Deriv

theorem deg_T0N : NcC2_35.degLE 18 6 0 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 281474976710656) (ZP.ofSP YantraCert.Data.C2.T0N)) (ZP.mul (ZP.const 281474976710656) (ZP.scaleW 1 2 18 27 32 6 6 1 0 NcC2_35)) = true := by decide +kernel
theorem deg_T0D : DcC2_35.degLE 18 6 0 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 281474976710656) (ZP.ofSP YantraCert.Data.C2.T0D)) (ZP.mul (ZP.const 281474976710656) (ZP.scaleW 1 2 18 27 32 6 6 1 0 DcC2_35)) = true := by decide +kernel

end YantraCert.Deriv.RC2
