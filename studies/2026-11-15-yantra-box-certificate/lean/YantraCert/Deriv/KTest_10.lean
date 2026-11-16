module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_10 : Q_10.within 27 = true := by decide +kernel
theorem tzN_10 : (Ex.frac T Q_10).1.zdeg 0 = true := by decide +kernel
theorem tzD_10 : (Ex.frac T Q_10).2.zdeg 0 = true := by decide +kernel
theorem tN_10 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_10).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_10 (ZP.mul TG_10 (ZP.prod [ZP.pow ea10_0 1])))) = true := by decide +kernel
theorem tD_10 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_10).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_10 (ZP.mul TG_10 (ZP.prod [ZP.pow eb10_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
