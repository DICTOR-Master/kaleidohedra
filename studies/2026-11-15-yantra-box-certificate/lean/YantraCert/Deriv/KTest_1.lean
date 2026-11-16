module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_1 : Q_1.within 27 = true := by decide +kernel
theorem tzN_1 : (Ex.frac T Q_1).1.zdeg 0 = true := by decide +kernel
theorem tzD_1 : (Ex.frac T Q_1).2.zdeg 0 = true := by decide +kernel
theorem tN_1 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_1).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_1 (ZP.mul TG_1 (ZP.prod [ZP.pow ea1_0 1, ZP.pow ea1_1 1, ZP.pow ea1_2 1, ZP.pow ea1_3 1, ZP.pow ea1_4 4, ZP.pow ea1_5 1])))) = true := by decide +kernel
theorem tD_1 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_1).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_1 (ZP.mul TG_1 (ZP.prod [ZP.pow eb1_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
