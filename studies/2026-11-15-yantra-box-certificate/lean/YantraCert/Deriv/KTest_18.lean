module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_18 : Q_18.within 27 = true := by decide +kernel
theorem tzN_18 : (Ex.frac T Q_18).1.zdeg 1 = true := by decide +kernel
theorem tzD_18 : (Ex.frac T Q_18).2.zdeg 1 = true := by decide +kernel
theorem tN_18 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_18).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_18 (ZP.mul TG_18 (ZP.prod [ZP.pow ea18_0 1])))) = true := by decide +kernel
theorem tD_18 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_18).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_18 (ZP.mul TG_18 (ZP.prod [ZP.pow eb18_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
