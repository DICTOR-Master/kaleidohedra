module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_B_34 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 TN_34)) (ZP.mul (ZP.const (1)) (ZP.mul NcB_34 (ZP.prod [ZP.pow enB34_0 2]))) = true := by decide +kernel
theorem cD_B_34 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 TD_34)) (ZP.mul (ZP.const (1)) (ZP.mul DcB_34 (ZP.prod [ZP.pow edB34_0 2]))) = true := by decide +kernel

end YantraCert.Deriv
