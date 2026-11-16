module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P407
open YantraCert

def cell : Cell := ⟨13, 6147, 13, 3703, 13, 4257⟩
noncomputable def codes : TC := TC.ofList [0, 9, 25]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P407
