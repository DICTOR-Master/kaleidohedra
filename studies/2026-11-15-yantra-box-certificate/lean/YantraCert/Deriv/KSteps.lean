module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem step3 : stepOK T 3 d3 n3 K3 = true := by decide +kernel
theorem step4 : stepOK T 4 d4 n4 K4 = true := by decide +kernel
theorem step5 : stepOK T 5 d5 n5 K5 = true := by decide +kernel
theorem step6 : stepOK T 6 d6 n6 K6 = true := by decide +kernel
theorem step7 : stepOK T 7 d7 n7 K7 = true := by decide +kernel
theorem step8 : stepOK T 8 d8 n8 K8 = true := by decide +kernel
theorem step9 : stepOK T 9 d9 n9 K9 = true := by decide +kernel
theorem step10 : stepOK T 10 d10 n10 K10 = true := by decide +kernel
theorem step11 : stepOK T 11 d11 n11 K11 = true := by decide +kernel
theorem step12 : stepOK T 12 d12 n12 K12 = true := by decide +kernel
theorem step13 : stepOK T 13 d13 n13 K13 = true := by decide +kernel
theorem step14 : stepOK T 14 d14 n14 K14 = true := by decide +kernel
theorem step15 : stepOK T 15 d15 n15 K15 = true := by decide +kernel
theorem step16 : stepOK T 16 d16 n16 K16 = true := by decide +kernel
theorem step17 : stepOK T 17 d17 n17 K17 = true := by decide +kernel
theorem step18 : stepOK T 18 d18 n18 K18 = true := by decide +kernel
theorem step19 : stepOK T 19 d19 n19 K19 = true := by decide +kernel
theorem step20 : stepOK T 20 d20 n20 K20 = true := by decide +kernel
theorem step21 : stepOK T 21 d21 n21 K21 = true := by decide +kernel
theorem step22 : stepOK T 22 d22 n22 K22 = true := by decide +kernel
theorem step23 : stepOK T 23 d23 n23 K23 = true := by decide +kernel
theorem step24 : stepOK T 24 d24 n24 K24 = true := by decide +kernel
theorem step25 : stepOK T 25 d25 n25 K25 = true := by decide +kernel
theorem step26 : stepOK T 26 d26 n26 K26 = true := by decide +kernel
theorem witH1_0 : ZP.eqv (Ex.frac T W_onepu2).1 (ZP.mul gH1_0 hH1_0) = true := by decide +kernel
theorem witbH1_0 : W_onepu2.within 27 = true := by decide +kernel
theorem witH1_1 : ZP.eqv (Ex.frac T W_k4pk8).1 (ZP.mul gH1_1 hH1_1) = true := by decide +kernel
theorem witbH1_1 : W_k4pk8.within 27 = true := by decide +kernel
theorem witD_0 : ZP.eqv (Ex.frac T W_Qmb1).1 (ZP.mul gD_0 hD_0) = true := by decide +kernel
theorem witbD_0 : W_Qmb1.within 27 = true := by decide +kernel
theorem witD_1 : ZP.eqv (Ex.frac T W_t).1 (ZP.mul gD_1 hD_1) = true := by decide +kernel
theorem witbD_1 : W_t.within 27 = true := by decide +kernel
theorem witD_2 : ZP.eqv (Ex.frac T W_Qmb1).1 (ZP.mul gD_2 hD_2) = true := by decide +kernel
theorem witbD_2 : W_Qmb1.within 27 = true := by decide +kernel
theorem witD_3 : ZP.eqv (Ex.frac T W_Rmb1).1 (ZP.mul gD_3 hD_3) = true := by decide +kernel
theorem witbD_3 : W_Rmb1.within 27 = true := by decide +kernel
theorem witD_4 : ZP.eqv (Ex.frac T W_Rmb1).1 (ZP.mul gD_4 hD_4) = true := by decide +kernel
theorem witbD_4 : W_Rmb1.within 27 = true := by decide +kernel
theorem witD_5 : ZP.eqv (Ex.frac T W_onepu2).1 (ZP.mul gD_5 hD_5) = true := by decide +kernel
theorem witbD_5 : W_onepu2.within 27 = true := by decide +kernel
theorem witD_6 : ZP.eqv (Ex.frac T W_onept2).1 (ZP.mul gD_6 hD_6) = true := by decide +kernel
theorem witbD_6 : W_onept2.within 27 = true := by decide +kernel
theorem witD_7 : ZP.eqv (Ex.frac T W_c138).1 (ZP.mul gD_7 hD_7) = true := by decide +kernel
theorem witbD_7 : W_c138.within 27 = true := by decide +kernel

end YantraCert.Deriv
