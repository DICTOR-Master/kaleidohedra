module

public import YantraCert.Deriv.Data
import YantraCert.Deriv.KCW_FH1  -- build order (memory): see scripts/c15_build_order.py

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv
open YantraCert

theorem fin_H1 : ZP.eqv (ZP.mul (ZP.const 1) (Ex.frac T E_H1).1) (ZP.mul (ZP.const (1)) (ZP.mul Fs_H1 (ZP.prod [ZP.pow gH1_0 1, ZP.pow gH1_1 1]))) = true := by decide +kernel
theorem finb_H1 : E_H1.within 27 = true := by decide +kernel

end YantraCert.Deriv
