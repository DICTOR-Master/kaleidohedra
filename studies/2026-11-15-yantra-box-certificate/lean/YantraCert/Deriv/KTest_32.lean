module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_32 : Q_32.within 27 = true := by decide +kernel
theorem tzN_32 : (Ex.frac T Q_32).1.zdeg 1 = true := by decide +kernel
theorem tzD_32 : (Ex.frac T Q_32).2.zdeg 1 = true := by decide +kernel
theorem tN_32 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_32).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_32 (ZP.mul TG_32 (ZP.prod [ZP.pow ea32_0 2])))) = true := by decide +kernel
theorem tD_32 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_32).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_32 (ZP.mul TG_32 (ZP.prod [ZP.pow eb32_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
