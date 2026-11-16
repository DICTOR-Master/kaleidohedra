module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_21 : Q_21.within 27 = true := by decide +kernel
theorem tzN_21 : (Ex.frac T Q_21).1.zdeg 1 = true := by decide +kernel
theorem tzD_21 : (Ex.frac T Q_21).2.zdeg 1 = true := by decide +kernel
theorem tN_21 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_21).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_21 (ZP.mul TG_21 (ZP.prod [ZP.pow ea21_0 1, ZP.pow ea21_1 2, ZP.pow ea21_2 1])))) = true := by decide +kernel
theorem tD_21 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 1 (Ex.frac T Q_21).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_21 (ZP.mul TG_21 (ZP.prod [ZP.pow eb21_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
