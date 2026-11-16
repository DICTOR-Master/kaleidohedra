module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P212
open YantraCert

def cell : Cell := ⟨3, 3, 2, 0, 2, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 1, 0, 9, 9, 306]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P212
