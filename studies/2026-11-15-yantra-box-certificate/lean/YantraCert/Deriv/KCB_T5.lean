module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem cN_B_5 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 TN_5)) (ZP.mul (ZP.const (1)) (ZP.mul NcB_5 (ZP.prod [ZP.pow enB5_0 2]))) = true := by decide +kernel
theorem cD_B_5 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.subst MB_0 MB_1 MB_2 TD_5)) (ZP.mul (ZP.const (1)) (ZP.mul DcB_5 (ZP.prod [ZP.pow edB5_0 1]))) = true := by decide +kernel

end YantraCert.Deriv
