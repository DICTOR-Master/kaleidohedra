module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cF_W_H1 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MW_0 MW_1 MW_2 Fm_H1)) (ZP.mul (ZP.const (-1)) (ZP.mul FcW_H1 (ZP.prod [ZP.pow cfWH1_0 18]))) = true := by decide +kernel

end YantraCert.Deriv
