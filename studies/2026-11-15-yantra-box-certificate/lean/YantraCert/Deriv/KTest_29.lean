module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_29 : Q_29.within 27 = true := by decide +kernel
theorem tzN_29 : (Ex.frac T Q_29).1.zdeg 2 = true := by decide +kernel
theorem tzD_29 : (Ex.frac T Q_29).2.zdeg 2 = true := by decide +kernel
theorem tN_29 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_29).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_29 (ZP.mul TG_29 (ZP.prod [ZP.pow ea29_0 2])))) = true := by decide +kernel
theorem tD_29 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_29).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_29 (ZP.mul TG_29 (ZP.prod [ZP.pow eb29_0 2, ZP.pow eb29_1 2, ZP.pow eb29_2 2])))) = true := by decide +kernel

end YantraCert.Deriv
