module

public import YantraCert.Data.Wtm.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RWtm
open YantraCert YantraCert.Deriv

theorem deg_T0N : NcWtm_7.degLE 0 0 1 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Wtm.T0N)) (ZP.mul (ZP.const 1) (ZP.scaleW 3 5 0 1 1 0 2 1 1 NcWtm_7)) = true := by decide +kernel
theorem deg_T0D : DcWtm_7.degLE 4 2 1 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 625) (ZP.ofSP YantraCert.Data.Wtm.T0D)) (ZP.mul (ZP.const 625) (ZP.scaleW 3 5 4 1 1 2 2 1 1 DcWtm_7)) = true := by decide +kernel
theorem deg_T1N : NcWtm_11.degLE 24 15 1 = true := by decide +kernel
theorem res_T1N : ZP.eqv (ZP.mul (ZP.const 59604644775390625) (ZP.ofSP YantraCert.Data.Wtm.T1N)) (ZP.mul (ZP.const 59604644775390625) (ZP.scaleW 3 5 24 1 1 15 2 1 1 NcWtm_11)) = true := by decide +kernel
theorem deg_T1D : DcWtm_11.degLE 60 38 2 = true := by decide +kernel
theorem res_T1D : ZP.eqv (ZP.mul (ZP.const 867361737988403547205962240695953369140625) (ZP.ofSP YantraCert.Data.Wtm.T1D)) (ZP.mul (ZP.const 867361737988403547205962240695953369140625) (ZP.scaleW 3 5 60 1 1 38 2 1 2 DcWtm_11)) = true := by decide +kernel
theorem deg_T2N : NcWtm_33.degLE 0 0 0 = true := by decide +kernel
theorem res_T2N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Wtm.T2N)) (ZP.mul (ZP.const 1) (ZP.scaleW 3 5 0 1 1 0 2 1 0 NcWtm_33)) = true := by decide +kernel
theorem deg_T2D : DcWtm_33.degLE 32 18 0 = true := by decide +kernel
theorem res_T2D : ZP.eqv (ZP.mul (ZP.const 23283064365386962890625) (ZP.ofSP YantraCert.Data.Wtm.T2D)) (ZP.mul (ZP.const 23283064365386962890625) (ZP.scaleW 3 5 32 1 1 18 2 1 0 DcWtm_33)) = true := by decide +kernel

end YantraCert.Deriv.RWtm
