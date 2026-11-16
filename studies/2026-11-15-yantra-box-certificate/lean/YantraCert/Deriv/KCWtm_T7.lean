module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_Wtm_7 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtm_0 MWtm_1 MWtm_2 TN_7)) (ZP.mul (ZP.const (4)) (ZP.mul NcWtm_7 (ZP.prod [ZP.pow enWtm7_0 2]))) = true := by decide +kernel
theorem cD_Wtm_7 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtm_0 MWtm_1 MWtm_2 TD_7)) (ZP.mul (ZP.const (1)) (ZP.mul DcWtm_7 (ZP.prod []))) = true := by decide +kernel

end YantraCert.Deriv
