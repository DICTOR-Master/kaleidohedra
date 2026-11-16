module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem zd_H1 : Fs_H1.zdeg 3 = true := by decide +kernel
theorem pull_H1 : ZP.eqv (ZP.mul (ZP.const 1) (ZP.substH PX PY PZn PZd 3 Fs_H1)) (ZP.mul (ZP.const (-1)) (ZP.mul Fm_H1 (ZP.prod [ZP.pow pfH1_0 3, ZP.pow pfH1_1 3, ZP.pow pfH1_2 2]))) = true := by decide +kernel

end YantraCert.Deriv
