module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_Wtp_G : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 Fm_G)) (ZP.mul (ZP.const (1)) (ZP.mul FcWtp_G (ZP.prod [ZP.pow cfWtpG_0 2]))) = true := by decide +kernel

end YantraCert.Deriv
