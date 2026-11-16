module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_Wtp_2 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TN_2)) (ZP.mul (ZP.const (1)) (ZP.mul NcWtp_2 (ZP.prod [ZP.pow enWtp2_0 4, ZP.pow enWtp2_1 6]))) = true := by decide +kernel
theorem cD_Wtp_2 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TD_2)) (ZP.mul (ZP.const (1)) (ZP.mul DcWtp_2 (ZP.prod [ZP.pow edWtp2_0 4, ZP.pow edWtp2_1 8]))) = true := by decide +kernel

end YantraCert.Deriv
