module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P456
open YantraCert

def cell : Cell := ⟨21, 1573783, 20, 474176, 20, 544894⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 9, 0, 0, 25, 0, 0, 0, 25, 0, 0, 0, 25, 0, 9, 25, 25, 25, 25, 9, 25]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P456
