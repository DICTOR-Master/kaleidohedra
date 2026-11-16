module

public import YantraCert.Data.W.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RW
open YantraCert YantraCert.Deriv

theorem deg_F0 : FcW_G.degLE 10 0 2 = true := by decide +kernel
theorem res_F0 : ZP.eqv (ZP.mul (ZP.const 1099511627776) (ZP.ofSP YantraCert.Data.W.F0)) (ZP.mul (ZP.const 68719476736) (ZP.scaleW 1 16 10 8 1 0 8 1 2 FcW_G)) = true := by decide +kernel
theorem deg_F1 : FcW_H1.degLE 94 10 3 = true := by decide +kernel
theorem res_F1 : ZP.eqv (ZP.mul (ZP.const 153914086704665934422965000391185991426092731525255651046673021110334850669910978950836977558144201721900890587136) (ZP.ofSP YantraCert.Data.W.F1)) (ZP.mul (ZP.const 2293498615990071511610820895302086940796564989168281123737588839386922876088484808070018553110125686554624) (ZP.scaleW 1 16 94 8 1 10 8 1 3 FcW_H1)) = true := by decide +kernel
theorem deg_F2 : FcW_D.degLE 91 10 2 = true := by decide +kernel
theorem res_F2 : ZP.eqv (ZP.mul (ZP.const 37576681324381331646231689548629392438010920782533117931316655544515344401833735095419183974156299248510959616) (ZP.ofSP YantraCert.Data.W.F2)) (ZP.mul (ZP.const 2239744742177804210557442280568444278121645497234649534899989100963791871180160945380877493271607115776) (ZP.scaleW 1 16 91 8 1 10 8 1 2 FcW_D)) = true := by decide +kernel
theorem deg_T0N : NcW_5.degLE 22 3 0 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 309485009821345068724781056) (ZP.ofSP YantraCert.Data.W.T0N)) (ZP.mul (ZP.const 4835703278458516698824704) (ZP.scaleW 1 16 22 8 1 3 8 1 0 NcW_5)) = true := by decide +kernel
theorem deg_T0D : DcW_5.degLE 32 4 0 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 340282366920938463463374607431768211456) (ZP.ofSP YantraCert.Data.W.T0D)) (ZP.mul (ZP.const 1329227995784915872903807060280344576) (ZP.scaleW 1 16 32 8 1 4 8 1 0 DcW_5)) = true := by decide +kernel

end YantraCert.Deriv.RW
