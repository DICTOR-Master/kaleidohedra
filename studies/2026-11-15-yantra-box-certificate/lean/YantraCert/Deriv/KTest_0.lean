module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_0 : Q_0.within 27 = true := by decide +kernel
theorem tzN_0 : (Ex.frac T Q_0).1.zdeg 0 = true := by decide +kernel
theorem tzD_0 : (Ex.frac T Q_0).2.zdeg 0 = true := by decide +kernel
theorem tN_0 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_0).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_0 (ZP.mul TG_0 (ZP.prod [ZP.pow ea0_0 1, ZP.pow ea0_1 1, ZP.pow ea0_2 1, ZP.pow ea0_3 2, ZP.pow ea0_4 1, ZP.pow ea0_5 2])))) = true := by decide +kernel
theorem tD_0 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_0).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_0 (ZP.mul TG_0 (ZP.prod [ZP.pow eb0_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
