module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_C1_33 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MC1_0 MC1_1 MC1_2 TN_33)) (ZP.mul (ZP.const (1)) (ZP.mul NcC1_33 (ZP.prod []))) = true := by decide +kernel
theorem cD_C1_33 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MC1_0 MC1_1 MC1_2 TD_33)) (ZP.mul (ZP.const (1)) (ZP.mul DcC1_33 (ZP.prod [ZP.pow edC133_0 4]))) = true := by decide +kernel

end YantraCert.Deriv
