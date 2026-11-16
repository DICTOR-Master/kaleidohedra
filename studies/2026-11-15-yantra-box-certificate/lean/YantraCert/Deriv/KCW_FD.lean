module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_W_D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MW_0 MW_1 MW_2 Fm_D)) (ZP.mul (ZP.const (1)) (ZP.mul FcW_D (ZP.prod [ZP.pow cfWD_0 16]))) = true := by decide +kernel

end YantraCert.Deriv
