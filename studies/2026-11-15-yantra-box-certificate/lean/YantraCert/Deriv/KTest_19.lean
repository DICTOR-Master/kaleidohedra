module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_19 : Q_19.within 27 = true := by decide +kernel
theorem tzN_19 : (Ex.frac T Q_19).1.zdeg 0 = true := by decide +kernel
theorem tzD_19 : (Ex.frac T Q_19).2.zdeg 0 = true := by decide +kernel
theorem tN_19 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_19).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_19 (ZP.mul TG_19 (ZP.prod [])))) = true := by decide +kernel
theorem tD_19 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_19).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_19 (ZP.mul TG_19 (ZP.prod [ZP.pow eb19_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
