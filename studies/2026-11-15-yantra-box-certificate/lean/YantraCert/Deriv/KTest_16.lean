module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_16 : Q_16.within 27 = true := by decide +kernel
theorem tzN_16 : (Ex.frac T Q_16).1.zdeg 1 = true := by decide +kernel
theorem tzD_16 : (Ex.frac T Q_16).2.zdeg 1 = true := by decide +kernel
theorem tN_16 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_16).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_16 (ZP.mul TG_16 (ZP.prod [ZP.pow ea16_0 1, ZP.pow ea16_1 5])))) = true := by decide +kernel
theorem tD_16 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_16).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_16 (ZP.mul TG_16 (ZP.prod [ZP.pow eb16_0 1, ZP.pow eb16_1 1])))) = true := by decide +kernel

end YantraCert.Deriv
