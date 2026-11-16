module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem zd_D : Fs_D.zdeg 2 = true := by decide +kernel
theorem pull_D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 Fs_D)) (ZP.mul (ZP.const (1)) (ZP.mul Fm_D (ZP.prod [ZP.pow pfD_0 2, ZP.pow pfD_1 2, ZP.pow pfD_2 2]))) = true := by decide +kernel

end YantraCert.Deriv
