module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_9 : Q_9.within 27 = true := by decide +kernel
theorem tzN_9 : (Ex.frac T Q_9).1.zdeg 1 = true := by decide +kernel
theorem tzD_9 : (Ex.frac T Q_9).2.zdeg 1 = true := by decide +kernel
theorem tN_9 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_9).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_9 (ZP.mul TG_9 (ZP.prod [ZP.pow ea9_0 3])))) = true := by decide +kernel
theorem tD_9 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_9).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_9 (ZP.mul TG_9 (ZP.prod [ZP.pow eb9_0 1, ZP.pow eb9_1 1])))) = true := by decide +kernel

end YantraCert.Deriv
