module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_25 : Q_25.within 27 = true := by decide +kernel
theorem tzN_25 : (Ex.frac T Q_25).1.zdeg 1 = true := by decide +kernel
theorem tzD_25 : (Ex.frac T Q_25).2.zdeg 1 = true := by decide +kernel
theorem tN_25 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_25).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_25 (ZP.mul TG_25 (ZP.prod [ZP.pow ea25_0 1, ZP.pow ea25_1 1])))) = true := by decide +kernel
theorem tD_25 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_25).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_25 (ZP.mul TG_25 (ZP.prod [ZP.pow eb25_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
