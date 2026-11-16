module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_7 : Q_7.within 27 = true := by decide +kernel
theorem tzN_7 : (Ex.frac T Q_7).1.zdeg 2 = true := by decide +kernel
theorem tzD_7 : (Ex.frac T Q_7).2.zdeg 2 = true := by decide +kernel
theorem tN_7 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_7).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_7 (ZP.mul TG_7 (ZP.prod [ZP.pow ea7_0 1, ZP.pow ea7_1 2, ZP.pow ea7_2 1])))) = true := by decide +kernel
theorem tD_7 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_7).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_7 (ZP.mul TG_7 (ZP.prod [ZP.pow eb7_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
