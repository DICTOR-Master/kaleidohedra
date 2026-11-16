module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_31 : Q_31.within 27 = true := by decide +kernel
theorem tzN_31 : (Ex.frac T Q_31).1.zdeg 2 = true := by decide +kernel
theorem tzD_31 : (Ex.frac T Q_31).2.zdeg 2 = true := by decide +kernel
theorem tN_31 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_31).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_31 (ZP.mul TG_31 (ZP.prod [ZP.pow ea31_0 2])))) = true := by decide +kernel
theorem tD_31 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_31).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_31 (ZP.mul TG_31 (ZP.prod [ZP.pow eb31_0 2, ZP.pow eb31_1 2])))) = true := by decide +kernel

end YantraCert.Deriv
