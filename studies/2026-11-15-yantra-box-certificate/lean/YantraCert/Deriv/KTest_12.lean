module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_12 : Q_12.within 27 = true := by decide +kernel
theorem tzN_12 : (Ex.frac T Q_12).1.zdeg 2 = true := by decide +kernel
theorem tzD_12 : (Ex.frac T Q_12).2.zdeg 2 = true := by decide +kernel
theorem tN_12 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_12).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_12 (ZP.mul TG_12 (ZP.prod [ZP.pow ea12_0 1, ZP.pow ea12_1 3])))) = true := by decide +kernel
theorem tD_12 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_12).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_12 (ZP.mul TG_12 (ZP.prod [ZP.pow eb12_0 1, ZP.pow eb12_1 2, ZP.pow eb12_2 1])))) = true := by decide +kernel

end YantraCert.Deriv
