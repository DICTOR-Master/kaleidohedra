module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_3 : Q_3.within 27 = true := by decide +kernel
theorem tzN_3 : (Ex.frac T Q_3).1.zdeg 3 = true := by decide +kernel
theorem tzD_3 : (Ex.frac T Q_3).2.zdeg 3 = true := by decide +kernel
theorem tN_3 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 3 (Ex.frac T Q_3).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_3 (ZP.mul TG_3 (ZP.prod [ZP.pow ea3_0 1, ZP.pow ea3_1 1, ZP.pow ea3_2 1, ZP.pow ea3_3 1, ZP.pow ea3_4 2, ZP.pow ea3_5 1, ZP.pow ea3_6 1])))) = true := by decide +kernel
theorem tD_3 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 3 (Ex.frac T Q_3).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_3 (ZP.mul TG_3 (ZP.prod [ZP.pow eb3_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
