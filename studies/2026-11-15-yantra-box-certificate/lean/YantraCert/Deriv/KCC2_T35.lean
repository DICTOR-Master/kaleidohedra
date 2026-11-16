module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_C2_35 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MC2_0 MC2_1 MC2_2 TN_35)) (ZP.mul (ZP.const (1)) (ZP.mul NcC2_35 (ZP.prod [ZP.pow enC235_0 4]))) = true := by decide +kernel
theorem cD_C2_35 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MC2_0 MC2_1 MC2_2 TD_35)) (ZP.mul (ZP.const (1)) (ZP.mul DcC2_35 (ZP.prod [ZP.pow edC235_0 4]))) = true := by decide +kernel

end YantraCert.Deriv
