module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_Wtp_32 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TN_32)) (ZP.mul (ZP.const (1)) (ZP.mul NcWtp_32 (ZP.prod [ZP.pow enWtp32_0 2]))) = true := by decide +kernel
theorem cD_Wtp_32 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TD_32)) (ZP.mul (ZP.const (1)) (ZP.mul DcWtp_32 (ZP.prod []))) = true := by decide +kernel

end YantraCert.Deriv
