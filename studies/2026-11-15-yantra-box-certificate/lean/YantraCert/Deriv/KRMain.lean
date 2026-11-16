module

public import YantraCert.Data.Main.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RMain
open YantraCert YantraCert.Deriv

theorem deg_F0 : Fm_G.degLE 8 0 2 = true := by decide +kernel
theorem res_F0 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.F0)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 8 1 1 0 6 1 2 Fm_G)) = true := by decide +kernel
theorem deg_F1 : Fm_H1.degLE 26 10 3 = true := by decide +kernel
theorem res_F1 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.F1)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 26 1 1 10 6 1 3 Fm_H1)) = true := by decide +kernel
theorem deg_F2 : Fm_D.degLE 26 10 2 = true := by decide +kernel
theorem res_F2 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.F2)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 26 1 1 10 6 1 2 Fm_D)) = true := by decide +kernel
theorem deg_T0N : TN_2.degLE 10 4 1 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T0N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 10 1 1 4 6 1 1 TN_2)) = true := by decide +kernel
theorem deg_T0D : TD_2.degLE 16 6 2 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T0D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 16 1 1 6 6 1 2 TD_2)) = true := by decide +kernel
theorem deg_T1N : TN_3.degLE 18 7 2 = true := by decide +kernel
theorem res_T1N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T1N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 18 1 1 7 6 1 2 TN_3)) = true := by decide +kernel
theorem deg_T1D : TD_3.degLE 26 10 3 = true := by decide +kernel
theorem res_T1D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T1D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 26 1 1 10 6 1 3 TD_3)) = true := by decide +kernel
theorem deg_T2N : TN_5.degLE 6 3 0 = true := by decide +kernel
theorem res_T2N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T2N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 6 1 1 3 6 1 0 TN_5)) = true := by decide +kernel
theorem deg_T2D : TD_5.degLE 6 4 0 = true := by decide +kernel
theorem res_T2D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T2D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 6 1 1 4 6 1 0 TD_5)) = true := by decide +kernel
theorem deg_T3N : TN_7.degLE 1 0 1 = true := by decide +kernel
theorem res_T3N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T3N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 1 1 1 0 6 1 1 TN_7)) = true := by decide +kernel
theorem deg_T3D : TD_7.degLE 3 0 1 = true := by decide +kernel
theorem res_T3D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T3D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 3 1 1 0 6 1 1 TD_7)) = true := by decide +kernel
theorem deg_T4N : TN_11.degLE 6 2 1 = true := by decide +kernel
theorem res_T4N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T4N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 6 1 1 2 6 1 1 TN_11)) = true := by decide +kernel
theorem deg_T4D : TD_11.degLE 16 6 2 = true := by decide +kernel
theorem res_T4D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T4D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 16 1 1 6 6 1 2 TD_11)) = true := by decide +kernel
theorem deg_T5N : TN_30.degLE 10 4 2 = true := by decide +kernel
theorem res_T5N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T5N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 10 1 1 4 6 1 2 TN_30)) = true := by decide +kernel
theorem deg_T5D : TD_30.degLE 10 2 2 = true := by decide +kernel
theorem res_T5D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T5D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 10 1 1 2 6 1 2 TD_30)) = true := by decide +kernel
theorem deg_T6N : TN_32.degLE 1 0 1 = true := by decide +kernel
theorem res_T6N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T6N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 1 1 1 0 6 1 1 TN_32)) = true := by decide +kernel
theorem deg_T6D : TD_32.degLE 0 0 0 = true := by decide +kernel
theorem res_T6D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T6D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 0 1 1 0 6 1 0 TD_32)) = true := by decide +kernel
theorem deg_T7N : TN_33.degLE 0 0 0 = true := by decide +kernel
theorem res_T7N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T7N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 0 1 1 0 6 1 0 TN_33)) = true := by decide +kernel
theorem deg_T7D : TD_33.degLE 6 4 0 = true := by decide +kernel
theorem res_T7D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T7D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 6 1 1 4 6 1 0 TD_33)) = true := by decide +kernel
theorem deg_T8N : TN_34.degLE 10 4 1 = true := by decide +kernel
theorem res_T8N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T8N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 10 1 1 4 6 1 1 TN_34)) = true := by decide +kernel
theorem deg_T8D : TD_34.degLE 10 4 1 = true := by decide +kernel
theorem res_T8D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T8D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 10 1 1 4 6 1 1 TD_34)) = true := by decide +kernel
theorem deg_T9N : TN_35.degLE 6 4 0 = true := by decide +kernel
theorem res_T9N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T9N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 6 1 1 4 6 1 0 TN_35)) = true := by decide +kernel
theorem deg_T9D : TD_35.degLE 6 4 0 = true := by decide +kernel
theorem res_T9D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Main.T9D)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 1 6 1 1 4 6 1 0 TD_35)) = true := by decide +kernel

end YantraCert.Deriv.RMain
