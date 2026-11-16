module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_C1_G : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MC1_0 MC1_1 MC1_2 Fm_G)) (ZP.mul (ZP.const (1)) (ZP.mul FcC1_G (ZP.prod []))) = true := by decide +kernel

end YantraCert.Deriv
