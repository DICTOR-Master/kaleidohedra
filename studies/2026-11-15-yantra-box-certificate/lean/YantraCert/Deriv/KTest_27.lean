module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_27 : Q_27.within 27 = true := by decide +kernel
theorem tzN_27 : (Ex.frac T Q_27).1.zdeg 4 = true := by decide +kernel
theorem tzD_27 : (Ex.frac T Q_27).2.zdeg 4 = true := by decide +kernel
theorem tN_27 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 4 (Ex.frac T Q_27).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_27 (ZP.mul TG_27 (ZP.prod [ZP.pow ea27_0 1, ZP.pow ea27_1 1, ZP.pow ea27_2 2])))) = true := by decide +kernel
theorem tD_27 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 4 (Ex.frac T Q_27).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_27 (ZP.mul TG_27 (ZP.prod [ZP.pow eb27_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
