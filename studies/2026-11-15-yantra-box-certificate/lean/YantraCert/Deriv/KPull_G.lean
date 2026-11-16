module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem zd_G : Fs_G.zdeg 2 = true := by decide +kernel
theorem pull_G : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 2 Fs_G)) (ZP.mul (ZP.const (1)) (ZP.mul Fm_G (ZP.prod [ZP.pow pfG_0 2, ZP.pow pfG_1 2, ZP.pow pfG_2 2]))) = true := by decide +kernel

end YantraCert.Deriv
