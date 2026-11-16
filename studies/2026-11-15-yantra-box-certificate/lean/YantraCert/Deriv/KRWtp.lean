module

public import YantraCert.Data.Wtp.Polys
public import YantraCert.Deriv.Data
public import YantraCert.ZPoly2

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.RWtp
open YantraCert YantraCert.Deriv

theorem deg_F0 : FcWtp_G.degLE 10 10 2 = true := by decide +kernel
theorem res_F0 : ZP.eqv (ZP.mul (ZP.const 9765625) (ZP.ofSP YantraCert.Data.Wtp.F0)) (ZP.mul (ZP.const 9765625) (ZP.scaleW 3 5 10 1 1 10 2 1 2 FcWtp_G)) = true := by decide +kernel
theorem deg_F1 : FcWtp_H1.degLE 94 57 3 = true := by decide +kernel
theorem res_F1 : ZP.eqv (ZP.mul (ZP.const 504870979341447555463506281780983186990852118469774723052978515625) (ZP.ofSP YantraCert.Data.Wtp.F1)) (ZP.mul (ZP.const 504870979341447555463506281780983186990852118469774723052978515625) (ZP.scaleW 3 5 94 1 1 57 2 1 3 FcWtp_H1)) = true := by decide +kernel
theorem deg_F2 : FcWtp_D.degLE 91 58 2 = true := by decide +kernel
theorem res_F2 : ZP.eqv (ZP.mul (ZP.const 4038967834731580443708050254247865495926816947758197784423828125) (ZP.ofSP YantraCert.Data.Wtp.F2)) (ZP.mul (ZP.const 4038967834731580443708050254247865495926816947758197784423828125) (ZP.scaleW 3 5 91 1 1 58 2 1 2 FcWtp_D)) = true := by decide +kernel
theorem deg_T0N : NcWtp_2.degLE 38 23 1 = true := by decide +kernel
theorem res_T0N : ZP.eqv (ZP.mul (ZP.const 363797880709171295166015625) (ZP.ofSP YantraCert.Data.Wtp.T0N)) (ZP.mul (ZP.const 363797880709171295166015625) (ZP.scaleW 3 5 38 1 1 23 2 1 1 NcWtp_2)) = true := by decide +kernel
theorem deg_T0D : DcWtp_2.degLE 60 38 2 = true := by decide +kernel
theorem res_T0D : ZP.eqv (ZP.mul (ZP.const 867361737988403547205962240695953369140625) (ZP.ofSP YantraCert.Data.Wtp.T0D)) (ZP.mul (ZP.const 867361737988403547205962240695953369140625) (ZP.scaleW 3 5 60 1 1 38 2 1 2 DcWtp_2)) = true := by decide +kernel
theorem deg_T1N : NcWtp_7.degLE 0 0 1 = true := by decide +kernel
theorem res_T1N : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Wtp.T1N)) (ZP.mul (ZP.const 1) (ZP.scaleW 3 5 0 1 1 0 2 1 1 NcWtp_7)) = true := by decide +kernel
theorem deg_T1D : DcWtp_7.degLE 4 2 1 = true := by decide +kernel
theorem res_T1D : ZP.eqv (ZP.mul (ZP.const 625) (ZP.ofSP YantraCert.Data.Wtp.T1D)) (ZP.mul (ZP.const 625) (ZP.scaleW 3 5 4 1 1 2 2 1 1 DcWtp_7)) = true := by decide +kernel
theorem deg_T2N : NcWtp_32.degLE 1 2 1 = true := by decide +kernel
theorem res_T2N : ZP.eqv (ZP.mul (ZP.const 5) (ZP.ofSP YantraCert.Data.Wtp.T2N)) (ZP.mul (ZP.const 5) (ZP.scaleW 3 5 1 1 1 2 2 1 1 NcWtp_32)) = true := by decide +kernel
theorem deg_T2D : DcWtp_32.degLE 0 0 0 = true := by decide +kernel
theorem res_T2D : ZP.eqv (ZP.mul (ZP.const 1) (ZP.ofSP YantraCert.Data.Wtp.T2D)) (ZP.mul (ZP.const 1) (ZP.scaleW 3 5 0 1 1 0 2 1 0 DcWtp_32)) = true := by decide +kernel
theorem deg_T3N : NcWtp_35.degLE 32 18 0 = true := by decide +kernel
theorem res_T3N : ZP.eqv (ZP.mul (ZP.const 23283064365386962890625) (ZP.ofSP YantraCert.Data.Wtp.T3N)) (ZP.mul (ZP.const 23283064365386962890625) (ZP.scaleW 3 5 32 1 1 18 2 1 0 NcWtp_35)) = true := by decide +kernel
theorem deg_T3D : DcWtp_35.degLE 32 18 0 = true := by decide +kernel
theorem res_T3D : ZP.eqv (ZP.mul (ZP.const 23283064365386962890625) (ZP.ofSP YantraCert.Data.Wtp.T3D)) (ZP.mul (ZP.const 23283064365386962890625) (ZP.scaleW 3 5 32 1 1 18 2 1 0 DcWtp_35)) = true := by decide +kernel

end YantraCert.Deriv.RWtp
