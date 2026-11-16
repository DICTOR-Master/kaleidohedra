module

public import YantraCert.Deriv.Data

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem fin_G : ZP.eqv (ZP.mul (ZP.const 1) (Ex.frac T E_G).1) (ZP.mul (ZP.const (1)) (ZP.mul Fs_G (ZP.prod []))) = true := by decide +kernel
theorem finb_G : E_G.within 27 = true := by decide +kernel

end YantraCert.Deriv
