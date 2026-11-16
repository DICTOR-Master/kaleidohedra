module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_33 : Q_33.within 27 = true := by decide +kernel
theorem tzN_33 : (Ex.frac T Q_33).1.zdeg 0 = true := by decide +kernel
theorem tzD_33 : (Ex.frac T Q_33).2.zdeg 0 = true := by decide +kernel
theorem tN_33 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_33).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_33 (ZP.mul TG_33 (ZP.prod [ZP.pow ea33_0 2, ZP.pow ea33_1 2, ZP.pow ea33_2 6])))) = true := by decide +kernel
theorem tD_33 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_33).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_33 (ZP.mul TG_33 (ZP.prod [ZP.pow eb33_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
