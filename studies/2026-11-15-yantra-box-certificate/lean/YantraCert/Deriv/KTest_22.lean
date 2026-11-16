module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_22 : Q_22.within 27 = true := by decide +kernel
theorem tzN_22 : (Ex.frac T Q_22).1.zdeg 0 = true := by decide +kernel
theorem tzD_22 : (Ex.frac T Q_22).2.zdeg 0 = true := by decide +kernel
theorem tN_22 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_22).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_22 (ZP.mul TG_22 (ZP.prod [ZP.pow ea22_0 1, ZP.pow ea22_1 1, ZP.pow ea22_2 1, ZP.pow ea22_3 4, ZP.pow ea22_4 1])))) = true := by decide +kernel
theorem tD_22 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_22).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_22 (ZP.mul TG_22 (ZP.prod [])))) = true := by decide +kernel

end YantraCert.Deriv
