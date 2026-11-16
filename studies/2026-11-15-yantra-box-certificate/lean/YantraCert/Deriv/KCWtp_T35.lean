module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_Wtp_35 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TN_35)) (ZP.mul (ZP.const (1)) (ZP.mul NcWtp_35 (ZP.prod [ZP.pow enWtp35_0 4, ZP.pow enWtp35_1 6]))) = true := by decide +kernel
theorem cD_Wtp_35 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 TD_35)) (ZP.mul (ZP.const (1)) (ZP.mul DcWtp_35 (ZP.prod [ZP.pow edWtp35_0 4, ZP.pow edWtp35_1 6]))) = true := by decide +kernel

end YantraCert.Deriv
