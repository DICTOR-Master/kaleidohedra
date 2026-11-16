module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_8 : Q_8.within 27 = true := by decide +kernel
theorem tzN_8 : (Ex.frac T Q_8).1.zdeg 0 = true := by decide +kernel
theorem tzD_8 : (Ex.frac T Q_8).2.zdeg 0 = true := by decide +kernel
theorem tN_8 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_8).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_8 (ZP.mul TG_8 (ZP.prod [ZP.pow ea8_0 1, ZP.pow ea8_1 1])))) = true := by decide +kernel
theorem tD_8 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_8).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_8 (ZP.mul TG_8 (ZP.prod [ZP.pow eb8_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
