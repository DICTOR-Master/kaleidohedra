module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_Wtp_D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 Fm_D)) (ZP.mul (ZP.const (1)) (ZP.mul FcWtp_D (ZP.prod [ZP.pow cfWtpD_0 8, ZP.pow cfWtpD_1 16]))) = true := by decide +kernel

end YantraCert.Deriv
