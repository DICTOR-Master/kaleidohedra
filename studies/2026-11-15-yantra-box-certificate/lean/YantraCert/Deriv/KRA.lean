module

public import YantraCert.Data.A.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RA
open YantraCert YantraCert.Deriv

theorem deg_T0N : NcA_35.degLE 8 4 0 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 16777216) (ZP.ofSP YantraCert.Data.A.T0N)) (ZP.mul (ZP.const 16777216) (ZP.scaleW 1 8 8 1 1 4 6 1 0 NcA_35)) = true := by decide +kernel
theorem deg_T0D : DcA_35.degLE 9 4 0 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 134217728) (ZP.ofSP YantraCert.Data.A.T0D)) (ZP.mul (ZP.const 134217728) (ZP.scaleW 1 8 9 1 1 4 6 1 0 DcA_35)) = true := by decide +kernel

end YantraCert.Deriv.RA
