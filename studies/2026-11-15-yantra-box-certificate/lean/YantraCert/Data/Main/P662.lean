module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P662
open YantraCert

def cell : Cell := ⟨3, 6, 3, 7, 2, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 9, 0, 306, 0, 0, 9, 0, 306, 306, 306]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P662
