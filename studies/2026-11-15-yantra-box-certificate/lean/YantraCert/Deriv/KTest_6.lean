module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_6 : Q_6.within 27 = true := by decide +kernel
theorem tzN_6 : (Ex.frac T Q_6).1.zdeg 1 = true := by decide +kernel
theorem tzD_6 : (Ex.frac T Q_6).2.zdeg 1 = true := by decide +kernel
theorem tN_6 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_6).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_6 (ZP.mul TG_6 (ZP.prod [ZP.pow ea6_0 1, ZP.pow ea6_1 2, ZP.pow ea6_2 2])))) = true := by decide +kernel
theorem tD_6 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_6).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_6 (ZP.mul TG_6 (ZP.prod [ZP.pow eb6_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
