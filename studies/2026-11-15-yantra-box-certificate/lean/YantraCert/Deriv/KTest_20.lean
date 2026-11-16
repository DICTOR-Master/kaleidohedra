module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_20 : Q_20.within 27 = true := by decide +kernel
theorem tzN_20 : (Ex.frac T Q_20).1.zdeg 3 = true := by decide +kernel
theorem tzD_20 : (Ex.frac T Q_20).2.zdeg 3 = true := by decide +kernel
theorem tN_20 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 3 (Ex.frac T Q_20).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_20 (ZP.mul TG_20 (ZP.prod [ZP.pow ea20_0 1, ZP.pow ea20_1 1, ZP.pow ea20_2 1])))) = true := by decide +kernel
theorem tD_20 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 3 (Ex.frac T Q_20).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_20 (ZP.mul TG_20 (ZP.prod [ZP.pow eb20_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
