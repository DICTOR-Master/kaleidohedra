module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_Wtm_33 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtm_0 MWtm_1 MWtm_2 TN_33)) (ZP.mul (ZP.const (1)) (ZP.mul NcWtm_33 (ZP.prod []))) = true := by decide +kernel
theorem cD_Wtm_33 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtm_0 MWtm_1 MWtm_2 TD_33)) (ZP.mul (ZP.const (1)) (ZP.mul DcWtm_33 (ZP.prod [ZP.pow edWtm33_0 4, ZP.pow edWtm33_1 6]))) = true := by decide +kernel

end YantraCert.Deriv
