module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_Wtp_7 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TN_7)) (ZP.mul (ZP.const (4)) (ZP.mul NcWtp_7 (ZP.prod [ZP.pow enWtp7_0 2]))) = true := by decide +kernel
theorem cD_Wtp_7 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TD_7)) (ZP.mul (ZP.const (1)) (ZP.mul DcWtp_7 (ZP.prod []))) = true := by decide +kernel

end YantraCert.Deriv
