module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_2 : Q_2.within 27 = true := by decide +kernel
theorem tzN_2 : (Ex.frac T Q_2).1.zdeg 2 = true := by decide +kernel
theorem tzD_2 : (Ex.frac T Q_2).2.zdeg 2 = true := by decide +kernel
theorem tN_2 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_2).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_2 (ZP.mul TG_2 (ZP.prod [ZP.pow ea2_0 1, ZP.pow ea2_1 1, ZP.pow ea2_2 1, ZP.pow ea2_3 1, ZP.pow ea2_4 2, ZP.pow ea2_5 1])))) = true := by decide +kernel
theorem tD_2 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_2).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_2 (ZP.mul TG_2 (ZP.prod [ZP.pow eb2_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
