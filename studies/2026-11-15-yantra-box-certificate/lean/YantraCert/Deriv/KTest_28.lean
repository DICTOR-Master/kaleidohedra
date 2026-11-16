module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_28 : Q_28.within 27 = true := by decide +kernel
theorem tzN_28 : (Ex.frac T Q_28).1.zdeg 6 = true := by decide +kernel
theorem tzD_28 : (Ex.frac T Q_28).2.zdeg 6 = true := by decide +kernel
theorem tN_28 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 6 (Ex.frac T Q_28).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_28 (ZP.mul TG_28 (ZP.prod [ZP.pow ea28_0 2])))) = true := by decide +kernel
theorem tD_28 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 6 (Ex.frac T Q_28).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_28 (ZP.mul TG_28 (ZP.prod [ZP.pow eb28_0 2, ZP.pow eb28_1 4, ZP.pow eb28_2 2])))) = true := by decide +kernel

end YantraCert.Deriv
