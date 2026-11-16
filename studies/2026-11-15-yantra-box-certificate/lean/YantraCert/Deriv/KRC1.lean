module

public import YantraCert.Data.C1.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RC1
open YantraCert YantraCert.Deriv

theorem deg_F0 : FcC1_G.degLE 8 0 2 = true := by decide +kernel
theorem res_F0 : ZP.eqv (ZP.mul (ZP.const 65536) (ZP.ofSP YantraCert.Data.C1.F0)) (ZP.mul (ZP.const 16384) (ZP.scaleW 1 4 8 2 1 0 6 1 2 FcC1_G)) = true := by decide +kernel
theorem deg_F1 : FcC1_H1.degLE 54 10 3 = true := by decide +kernel
theorem res_F1 : ZP.eqv (ZP.mul (ZP.const 324518553658426726783156020576256) (ZP.ofSP YantraCert.Data.C1.F1)) (ZP.mul (ZP.const 39614081257132168796771975168) (ZP.scaleW 1 4 54 2 1 10 6 1 3 FcC1_H1)) = true := by decide +kernel
theorem deg_F2 : FcC1_D.degLE 57 10 2 = true := by decide +kernel
theorem res_F2 : ZP.eqv (ZP.mul (ZP.const 20769187434139310514121985316880384) (ZP.ofSP YantraCert.Data.C1.F2)) (ZP.mul (ZP.const 5070602400912917605986812821504) (ZP.scaleW 1 4 57 2 1 10 6 1 2 FcC1_D)) = true := by decide +kernel
theorem deg_T0N : NcC1_2.degLE 22 4 1 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 17592186044416) (ZP.ofSP YantraCert.Data.C1.T0N)) (ZP.mul (ZP.const 274877906944) (ZP.scaleW 1 4 22 2 1 4 6 1 1 NcC1_2)) = true := by decide +kernel
theorem deg_T0D : DcC1_2.degLE 36 6 2 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 4722366482869645213696) (ZP.ofSP YantraCert.Data.C1.T0D)) (ZP.mul (ZP.const 18446744073709551616) (ZP.scaleW 1 4 36 2 1 6 6 1 2 DcC1_2)) = true := by decide +kernel
theorem deg_T1N : NcC1_3.degLE 38 7 2 = true := by decide +kernel
theorem res_T1N : ZP.eqv (ZP.mul (ZP.const 75557863725914323419136) (ZP.ofSP YantraCert.Data.C1.T1N)) (ZP.mul (ZP.const 147573952589676412928) (ZP.scaleW 1 4 38 2 1 7 6 1 2 NcC1_3)) = true := by decide +kernel
theorem deg_T1D : DcC1_3.degLE 57 10 3 = true := by decide +kernel
theorem res_T1D : ZP.eqv (ZP.mul (ZP.const 20769187434139310514121985316880384) (ZP.ofSP YantraCert.Data.C1.T1D)) (ZP.mul (ZP.const 5070602400912917605986812821504) (ZP.scaleW 1 4 57 2 1 10 6 1 3 DcC1_3)) = true := by decide +kernel
theorem deg_T2N : NcC1_5.degLE 14 3 0 = true := by decide +kernel
theorem res_T2N : ZP.eqv (ZP.mul (ZP.const 268435456) (ZP.ofSP YantraCert.Data.C1.T2N)) (ZP.mul (ZP.const 33554432) (ZP.scaleW 1 4 14 2 1 3 6 1 0 NcC1_5)) = true := by decide +kernel
theorem deg_T2D : DcC1_5.degLE 18 4 0 = true := by decide +kernel
theorem res_T2D : ZP.eqv (ZP.mul (ZP.const 68719476736) (ZP.ofSP YantraCert.Data.C1.T2D)) (ZP.mul (ZP.const 4294967296) (ZP.scaleW 1 4 18 2 1 4 6 1 0 DcC1_5)) = true := by decide +kernel
theorem deg_T3N : NcC1_11.degLE 14 2 1 = true := by decide +kernel
theorem res_T3N : ZP.eqv (ZP.mul (ZP.const 268435456) (ZP.ofSP YantraCert.Data.C1.T3N)) (ZP.mul (ZP.const 33554432) (ZP.scaleW 1 4 14 2 1 2 6 1 1 NcC1_11)) = true := by decide +kernel
theorem deg_T3D : DcC1_11.degLE 36 6 2 = true := by decide +kernel
theorem res_T3D : ZP.eqv (ZP.mul (ZP.const 4722366482869645213696) (ZP.ofSP YantraCert.Data.C1.T3D)) (ZP.mul (ZP.const 18446744073709551616) (ZP.scaleW 1 4 36 2 1 6 6 1 2 DcC1_11)) = true := by decide +kernel
theorem deg_T4N : NcC1_33.degLE 0 0 0 = true := by decide +kernel
theorem res_T4N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.C1.T4N)) (ZP.mul (ZP.const 1) (ZP.scaleW 1 4 0 2 1 0 6 1 0 NcC1_33)) = true := by decide +kernel
theorem deg_T4D : DcC1_33.degLE 18 4 0 = true := by decide +kernel
theorem res_T4D : ZP.eqv (ZP.mul (ZP.const 68719476736) (ZP.ofSP YantraCert.Data.C1.T4D)) (ZP.mul (ZP.const 4294967296) (ZP.scaleW 1 4 18 2 1 4 6 1 0 DcC1_33)) = true := by decide +kernel
theorem deg_T5N : NcC1_34.degLE 21 4 1 = true := by decide +kernel
theorem res_T5N : ZP.eqv (ZP.mul (ZP.const 4398046511104) (ZP.ofSP YantraCert.Data.C1.T5N)) (ZP.mul (ZP.const 274877906944) (ZP.scaleW 1 4 21 2 1 4 6 1 1 NcC1_34)) = true := by decide +kernel
theorem deg_T5D : DcC1_34.degLE 21 4 1 = true := by decide +kernel
theorem res_T5D : ZP.eqv (ZP.mul (ZP.const 4398046511104) (ZP.ofSP YantraCert.Data.C1.T5D)) (ZP.mul (ZP.const 274877906944) (ZP.scaleW 1 4 21 2 1 4 6 1 1 DcC1_34)) = true := by decide +kernel
theorem deg_T6N : NcC1_35.degLE 18 4 0 = true := by decide +kernel
theorem res_T6N : ZP.eqv (ZP.mul (ZP.const 68719476736) (ZP.ofSP YantraCert.Data.C1.T6N)) (ZP.mul (ZP.const 4294967296) (ZP.scaleW 1 4 18 2 1 4 6 1 0 NcC1_35)) = true := by decide +kernel
theorem deg_T6D : DcC1_35.degLE 18 4 0 = true := by decide +kernel
theorem res_T6D : ZP.eqv (ZP.mul (ZP.const 68719476736) (ZP.ofSP YantraCert.Data.C1.T6D)) (ZP.mul (ZP.const 4294967296) (ZP.scaleW 1 4 18 2 1 4 6 1 0 DcC1_35)) = true := by decide +kernel

end YantraCert.Deriv.RC1
