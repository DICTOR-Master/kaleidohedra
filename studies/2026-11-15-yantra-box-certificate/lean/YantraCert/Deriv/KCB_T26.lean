module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_B_26 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 TN_26)) (ZP.mul (ZP.const (1)) (ZP.mul NcB_26 (ZP.prod [ZP.pow enB26_0 2]))) = true := by decide +kernel
theorem cD_B_26 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 TD_26)) (ZP.mul (ZP.const (1)) (ZP.mul DcB_26 (ZP.prod [ZP.pow edB26_0 2]))) = true := by decide +kernel

end YantraCert.Deriv
