module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_17 : Q_17.within 27 = true := by decide +kernel
theorem tzN_17 : (Ex.frac T Q_17).1.zdeg 0 = true := by decide +kernel
theorem tzD_17 : (Ex.frac T Q_17).2.zdeg 0 = true := by decide +kernel
theorem tN_17 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_17).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_17 (ZP.mul TG_17 (ZP.prod [ZP.pow ea17_0 1, ZP.pow ea17_1 1, ZP.pow ea17_2 1, ZP.pow ea17_3 2, ZP.pow ea17_4 1])))) = true := by decide +kernel
theorem tD_17 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_17).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_17 (ZP.mul TG_17 (ZP.prod [ZP.pow eb17_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
