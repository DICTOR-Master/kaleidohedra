module

public import YantraCert.Data.B.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RB
open YantraCert YantraCert.Deriv

theorem deg_F0 : FcB_G.degLE 8 8 2 = true := by decide +kernel
theorem res_F0 : ZP.eqv (ZP.mul (ZP.const 16777216) (ZP.ofSP YantraCert.Data.B.F0)) (ZP.mul (ZP.const 4194304) (ZP.scaleW 1 8 8 1 1 8 6 1 2 FcB_G)) = true := by decide +kernel
theorem deg_T0N : NcB_5.degLE 7 6 0 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 2097152) (ZP.ofSP YantraCert.Data.B.T0N)) (ZP.mul (ZP.const 2097152) (ZP.scaleW 1 8 7 1 1 6 6 1 0 NcB_5)) = true := by decide +kernel
theorem deg_T0D : DcB_5.degLE 9 6 0 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 134217728) (ZP.ofSP YantraCert.Data.B.T0D)) (ZP.mul (ZP.const 134217728) (ZP.scaleW 1 8 9 1 1 6 6 1 0 DcB_5)) = true := by decide +kernel
theorem deg_T1N : NcB_21.degLE 7 7 1 = true := by decide +kernel
theorem res_T1N : ZP.eqv (ZP.mul (ZP.const 2097152) (ZP.ofSP YantraCert.Data.B.T1N)) (ZP.mul (ZP.const 2097152) (ZP.scaleW 1 8 7 1 1 7 6 1 1 NcB_21)) = true := by decide +kernel
theorem deg_T1D : DcB_21.degLE 11 10 1 = true := by decide +kernel
theorem res_T1D : ZP.eqv (ZP.mul (ZP.const 8589934592) (ZP.ofSP YantraCert.Data.B.T1D)) (ZP.mul (ZP.const 8589934592) (ZP.scaleW 1 8 11 1 1 10 6 1 1 DcB_21)) = true := by decide +kernel
theorem deg_T2N : NcB_26.degLE 25 19 2 = true := by decide +kernel
theorem res_T2N : ZP.eqv (ZP.mul (ZP.const 37778931862957161709568) (ZP.ofSP YantraCert.Data.B.T2N)) (ZP.mul (ZP.const 2361183241434822606848) (ZP.scaleW 1 8 25 1 1 19 6 1 2 NcB_26)) = true := by decide +kernel
theorem deg_T2D : DcB_26.degLE 18 12 0 = true := by decide +kernel
theorem res_T2D : ZP.eqv (ZP.mul (ZP.const 18014398509481984) (ZP.ofSP YantraCert.Data.B.T2D)) (ZP.mul (ZP.const 4503599627370496) (ZP.scaleW 1 8 18 1 1 12 6 1 0 DcB_26)) = true := by decide +kernel
theorem deg_T3N : NcB_30.degLE 13 10 2 = true := by decide +kernel
theorem res_T3N : ZP.eqv (ZP.mul (ZP.const 549755813888) (ZP.ofSP YantraCert.Data.B.T3N)) (ZP.mul (ZP.const 137438953472) (ZP.scaleW 1 8 13 1 1 10 6 1 2 NcB_30)) = true := by decide +kernel
theorem deg_T3D : DcB_30.degLE 10 10 2 = true := by decide +kernel
theorem res_T3D : ZP.eqv (ZP.mul (ZP.const 1073741824) (ZP.ofSP YantraCert.Data.B.T3D)) (ZP.mul (ZP.const 1073741824) (ZP.scaleW 1 8 10 1 1 10 6 1 2 DcB_30)) = true := by decide +kernel
theorem deg_T4N : NcB_34.degLE 11 10 1 = true := by decide +kernel
theorem res_T4N : ZP.eqv (ZP.mul (ZP.const 8589934592) (ZP.ofSP YantraCert.Data.B.T4N)) (ZP.mul (ZP.const 8589934592) (ZP.scaleW 1 8 11 1 1 10 6 1 1 NcB_34)) = true := by decide +kernel
theorem deg_T4D : DcB_34.degLE 11 10 1 = true := by decide +kernel
theorem res_T4D : ZP.eqv (ZP.mul (ZP.const 8589934592) (ZP.ofSP YantraCert.Data.B.T4D)) (ZP.mul (ZP.const 8589934592) (ZP.scaleW 1 8 11 1 1 10 6 1 1 DcB_34)) = true := by decide +kernel
theorem deg_T5N : NcB_35.degLE 8 6 0 = true := by decide +kernel
theorem res_T5N : ZP.eqv (ZP.mul (ZP.const 16777216) (ZP.ofSP YantraCert.Data.B.T5N)) (ZP.mul (ZP.const 16777216) (ZP.scaleW 1 8 8 1 1 6 6 1 0 NcB_35)) = true := by decide +kernel
theorem deg_T5D : DcB_35.degLE 9 6 0 = true := by decide +kernel
theorem res_T5D : ZP.eqv (ZP.mul (ZP.const 134217728) (ZP.ofSP YantraCert.Data.B.T5D)) (ZP.mul (ZP.const 134217728) (ZP.scaleW 1 8 9 1 1 6 6 1 0 DcB_35)) = true := by decide +kernel

end YantraCert.Deriv.RB
