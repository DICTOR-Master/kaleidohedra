module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_B_G : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 Fm_G)) (ZP.mul (ZP.const (1)) (ZP.mul FcB_G (ZP.prod []))) = true := by decide +kernel

end YantraCert.Deriv
