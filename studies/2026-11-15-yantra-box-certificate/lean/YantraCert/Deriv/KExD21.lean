module

public import YantraCert.Deriv.KEx

@[expose] public section

set_option maxRecDepth 200000
set_option maxHeartbeats 0

namespace YantraCert.Deriv.KEx
open YantraCert YantraCert.Deriv

theorem zQ21 : D21.zdeg 2 = true := by decide +kernel
theorem gQ21 : (ZP.toSP 26 8 2 (ZP.substH PX PY PZn PZd 2 D21)).degOK = true := by decide +kernel
theorem sQ21 : (ZP.toSP 26 8 2 (ZP.substH PX PY PZn PZd 2 D21)).boxSignN QS 1045958633310927219312709804664751888613212 630290400061572206887148711804214366640362 4345735874637809770754784814922852658776494 1045958633310927219312709804666950911868764 630290400061572206887148711806413389895914 4345735874637809770754784814925051682032046 = 2 := by decide +kernel

end YantraCert.Deriv.KEx
