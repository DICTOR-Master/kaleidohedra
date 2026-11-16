module

public import YantraCert.Deriv.Data
import YantraCert.Deriv.KSteps  -- build order (memory): see scripts/c15_build_order.py

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_Wtp_H1 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWtp_0 MWtp_1 MWtp_2 Fm_H1)) (ZP.mul (ZP.const (-1)) (ZP.mul FcWtp_H1 (ZP.prod [ZP.pow cfWtpH1_0 12, ZP.pow cfWtpH1_1 18]))) = true := by decide +kernel

end YantraCert.Deriv
