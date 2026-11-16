module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem fin_D : ZP.eqv (ZP.mul (ZP.const 1) (Ex.frac T E_D).1) (ZP.mul (ZP.const (-1)) (ZP.mul Fs_D (ZP.prod [ZP.pow gD_0 2, ZP.pow gD_1 2, ZP.pow gD_2 2, ZP.pow gD_3 1, ZP.pow gD_4 1, ZP.pow gD_5 1, ZP.pow gD_6 4, ZP.pow gD_7 2]))) = true := by decide +kernel
theorem finb_D : E_D.within 27 = true := by decide +kernel

end YantraCert.Deriv
