module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_13 : Q_13.within 27 = true := by decide +kernel
theorem tzN_13 : (Ex.frac T Q_13).1.zdeg 1 = true := by decide +kernel
theorem tzD_13 : (Ex.frac T Q_13).2.zdeg 1 = true := by decide +kernel
theorem tN_13 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_13).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_13 (ZP.mul TG_13 (ZP.prod [ZP.pow ea13_0 3])))) = true := by decide +kernel
theorem tD_13 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_13).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_13 (ZP.mul TG_13 (ZP.prod [ZP.pow eb13_0 1, ZP.pow eb13_1 1, ZP.pow eb13_2 1])))) = true := by decide +kernel

end YantraCert.Deriv
