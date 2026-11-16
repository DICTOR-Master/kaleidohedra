module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_24 : Q_24.within 27 = true := by decide +kernel
theorem tzN_24 : (Ex.frac T Q_24).1.zdeg 1 = true := by decide +kernel
theorem tzD_24 : (Ex.frac T Q_24).2.zdeg 1 = true := by decide +kernel
theorem tN_24 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_24).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_24 (ZP.mul TG_24 (ZP.prod [])))) = true := by decide +kernel
theorem tD_24 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_24).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_24 (ZP.mul TG_24 (ZP.prod [ZP.pow eb24_0 1, ZP.pow eb24_1 1])))) = true := by decide +kernel

end YantraCert.Deriv
