module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_15 : Q_15.within 27 = true := by decide +kernel
theorem tzN_15 : (Ex.frac T Q_15).1.zdeg 1 = true := by decide +kernel
theorem tzD_15 : (Ex.frac T Q_15).2.zdeg 1 = true := by decide +kernel
theorem tN_15 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_15).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_15 (ZP.mul TG_15 (ZP.prod [ZP.pow ea15_0 3])))) = true := by decide +kernel
theorem tD_15 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_15).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_15 (ZP.mul TG_15 (ZP.prod [ZP.pow eb15_0 1, ZP.pow eb15_1 1])))) = true := by decide +kernel

end YantraCert.Deriv
