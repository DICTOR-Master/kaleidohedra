module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_26 : Q_26.within 27 = true := by decide +kernel
theorem tzN_26 : (Ex.frac T Q_26).1.zdeg 2 = true := by decide +kernel
theorem tzD_26 : (Ex.frac T Q_26).2.zdeg 2 = true := by decide +kernel
theorem tN_26 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_26).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_26 (ZP.mul TG_26 (ZP.prod [ZP.pow ea26_0 1, ZP.pow ea26_1 2])))) = true := by decide +kernel
theorem tD_26 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_26).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_26 (ZP.mul TG_26 (ZP.prod [ZP.pow eb26_0 2, ZP.pow eb26_1 2])))) = true := by decide +kernel

end YantraCert.Deriv
