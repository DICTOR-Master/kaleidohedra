module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_30 : Q_30.within 27 = true := by decide +kernel
theorem tzN_30 : (Ex.frac T Q_30).1.zdeg 4 = true := by decide +kernel
theorem tzD_30 : (Ex.frac T Q_30).2.zdeg 4 = true := by decide +kernel
theorem tN_30 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 4 (Ex.frac T Q_30).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_30 (ZP.mul TG_30 (ZP.prod [ZP.pow ea30_0 1, ZP.pow ea30_1 1, ZP.pow ea30_2 4])))) = true := by decide +kernel
theorem tD_30 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 4 (Ex.frac T Q_30).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_30 (ZP.mul TG_30 (ZP.prod [ZP.pow eb30_0 1, ZP.pow eb30_1 2])))) = true := by decide +kernel

end YantraCert.Deriv
