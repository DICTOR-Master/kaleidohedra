module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_Wrm_G : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MWrm_0 MWrm_1 MWrm_2 Fm_G)) (ZP.mul (ZP.const (1)) (ZP.mul FcWrm_G (ZP.prod [ZP.pow cfWrmG_0 2]))) = true := by decide +kernel

end YantraCert.Deriv
