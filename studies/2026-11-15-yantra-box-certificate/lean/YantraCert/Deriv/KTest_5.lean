module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_5 : Q_5.within 27 = true := by decide +kernel
theorem tzN_5 : (Ex.frac T Q_5).1.zdeg 0 = true := by decide +kernel
theorem tzD_5 : (Ex.frac T Q_5).2.zdeg 0 = true := by decide +kernel
theorem tN_5 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_5).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_5 (ZP.mul TG_5 (ZP.prod [ZP.pow ea5_0 1])))) = true := by decide +kernel
theorem tD_5 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_5).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_5 (ZP.mul TG_5 (ZP.prod [ZP.pow eb5_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
