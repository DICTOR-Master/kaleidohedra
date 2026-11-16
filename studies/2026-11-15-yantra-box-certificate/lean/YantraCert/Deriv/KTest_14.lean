module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_14 : Q_14.within 27 = true := by decide +kernel
theorem tzN_14 : (Ex.frac T Q_14).1.zdeg 0 = true := by decide +kernel
theorem tzD_14 : (Ex.frac T Q_14).2.zdeg 0 = true := by decide +kernel
theorem tN_14 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_14).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_14 (ZP.mul TG_14 (ZP.prod [ZP.pow ea14_0 1])))) = true := by decide +kernel
theorem tD_14 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_14).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_14 (ZP.mul TG_14 (ZP.prod [ZP.pow eb14_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
