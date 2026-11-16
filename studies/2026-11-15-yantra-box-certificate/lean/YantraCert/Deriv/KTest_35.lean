module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_35 : Q_35.within 27 = true := by decide +kernel
theorem tzN_35 : (Ex.frac T Q_35).1.zdeg 0 = true := by decide +kernel
theorem tzD_35 : (Ex.frac T Q_35).2.zdeg 0 = true := by decide +kernel
theorem tN_35 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_35).1)) (ZP.mul (ZP.const (-1)) (ZP.mul TN_35 (ZP.mul TG_35 (ZP.prod [])))) = true := by decide +kernel
theorem tD_35 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 0 (Ex.frac T Q_35).2)) (ZP.mul (ZP.const (-1)) (ZP.mul TD_35 (ZP.mul TG_35 (ZP.prod [])))) = true := by decide +kernel

end YantraCert.Deriv
