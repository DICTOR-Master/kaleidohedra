module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P451
open YantraCert

def cell : Cell := ⟨19, 393444, 18, 118544, 18, 136223⟩
noncomputable def codes : TC := TC.ofList [25]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P451
