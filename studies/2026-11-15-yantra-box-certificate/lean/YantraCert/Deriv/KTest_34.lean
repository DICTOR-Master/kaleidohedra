module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_34 : Q_34.within 27 = true := by decide +kernel
theorem tzN_34 : (Ex.frac T Q_34).1.zdeg 1 = true := by decide +kernel
theorem tzD_34 : (Ex.frac T Q_34).2.zdeg 1 = true := by decide +kernel
theorem tN_34 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_34).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_34 (ZP.mul TG_34 (ZP.prod [ZP.pow ea34_0 1, ZP.pow ea34_1 1])))) = true := by decide +kernel
theorem tD_34 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_34).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_34 (ZP.mul TG_34 (ZP.prod [ZP.pow eb34_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
