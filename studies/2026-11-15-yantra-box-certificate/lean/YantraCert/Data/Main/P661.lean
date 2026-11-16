module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P661
open YantraCert

def cell : Cell := ⟨4, 13, 4, 13, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 306, 0, 306, 306]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P661
