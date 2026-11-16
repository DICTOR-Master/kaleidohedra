module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_4 : Q_4.within 27 = true := by decide +kernel
theorem tzN_4 : (Ex.frac T Q_4).1.zdeg 1 = true := by decide +kernel
theorem tzD_4 : (Ex.frac T Q_4).2.zdeg 1 = true := by decide +kernel
theorem tN_4 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_4).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_4 (ZP.mul TG_4 (ZP.prod [ZP.pow ea4_0 1, ZP.pow ea4_1 3, ZP.pow ea4_2 3, ZP.pow ea4_3 12, ZP.pow ea4_4 1])))) = true := by decide +kernel
theorem tD_4 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_4).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_4 (ZP.mul TG_4 (ZP.prod [ZP.pow eb4_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
