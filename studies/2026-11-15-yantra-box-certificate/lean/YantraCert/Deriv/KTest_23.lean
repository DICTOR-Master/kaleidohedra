module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_23 : Q_23.within 27 = true := by decide +kernel
theorem tzN_23 : (Ex.frac T Q_23).1.zdeg 0 = true := by decide +kernel
theorem tzD_23 : (Ex.frac T Q_23).2.zdeg 0 = true := by decide +kernel
theorem tN_23 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_23).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_23 (ZP.mul TG_23 (ZP.prod [])))) = true := by decide +kernel
theorem tD_23 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_23).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_23 (ZP.mul TG_23 (ZP.prod [ZP.pow eb23_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
