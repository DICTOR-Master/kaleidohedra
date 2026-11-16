module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_W_5 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MW_0 MW_1 MW_2 TN_5)) (ZP.mul (ZP.const (1)) (ZP.mul NcW_5 (ZP.prod [ZP.pow enW5_0 8]))) = true := by decide +kernel
theorem cD_W_5 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MW_0 MW_1 MW_2 TD_5)) (ZP.mul (ZP.const (1)) (ZP.mul DcW_5 (ZP.prod [ZP.pow edW5_0 6]))) = true := by decide +kernel

end YantraCert.Deriv
