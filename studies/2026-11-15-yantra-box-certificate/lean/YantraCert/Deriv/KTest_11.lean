module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem tw_11 : Q_11.within 27 = true := by decide +kernel
theorem tzN_11 : (Ex.frac T Q_11).1.zdeg 2 = true := by decide +kernel
theorem tzD_11 : (Ex.frac T Q_11).2.zdeg 2 = true := by decide +kernel
theorem tN_11 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_11).1)) (ZP.mul (ZP.const (1)) (ZP.mul TN_11 (ZP.mul TG_11 (ZP.prod [ZP.pow ea11_0 1, ZP.pow ea11_1 2, ZP.pow ea11_2 2, ZP.pow ea11_3 11])))) = true := by decide +kernel
theorem tD_11 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 (Ex.frac T Q_11).2)) (ZP.mul (ZP.const (1)) (ZP.mul TD_11 (ZP.mul TG_11 (ZP.prod [ZP.pow eb11_0 1])))) = true := by decide +kernel

end YantraCert.Deriv
