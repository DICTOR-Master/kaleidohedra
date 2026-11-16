module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P588
open YantraCert

def cell : Cell := ⟨4, 12, 3, 5, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 306, 0, 0, 9, 9, 0, 9, 9, 0, 9, 0, 306, 306]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P588
