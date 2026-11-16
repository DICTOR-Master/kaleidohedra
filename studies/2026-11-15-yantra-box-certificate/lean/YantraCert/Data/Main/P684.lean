module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P684
open YantraCert

def cell : Cell := ⟨6, 51, 5, 17, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 0, 0, 25, 25, 25, 0, 9, 0, 0, 25, 0, 25, 9, 0, 25, 25, 0, 0, 0, 9, 25, 0, 25, 25, 0, 0, 9, 25, 0, 0, 25, 25, 25, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 25, 0, 25, 9, 0, 9, 0, 0, 0, 0, 25, 25, 9, 0, 0, 0, 25, 0, 9, 25, 25, 9, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 0, 0, 9, 0, 25, 25, 0, 0, 25, 25, 58, 0, 0, 9, 0, 25, 25, 0, 0, 25, 0, 25, 9, 0, 25, 25]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P684
