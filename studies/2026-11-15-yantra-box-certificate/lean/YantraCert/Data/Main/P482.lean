module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P482
open YantraCert

def cell : Cell := ⟨19, 393446, 19, 237088, 18, 136223⟩
noncomputable def codes : TC := TC.ofList [41]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P482
