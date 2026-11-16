module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P333
open YantraCert

def cell : Cell := ⟨4, 10, 3, 3, 3, 4⟩
noncomputable def codes : TC := TC.ofList [0, 306, 306]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P333
