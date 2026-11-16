module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_Wrp_G : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWrp_0 MWrp_1 MWrp_2 Fm_G)) (ZP.mul (ZP.const (1)) (ZP.mul FcWrp_G (ZP.prod [ZP.pow cfWrpG_0 2]))) = true := by decide +kernel

end YantraCert.Deriv
