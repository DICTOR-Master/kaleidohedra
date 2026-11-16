module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P703
open YantraCert

def cell : Cell := ⟨6, 51, 6, 39, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 0, 25, 25, 0, 0, 25, 9, 0, 25, 9, 0, 9, 0, 25, 0, 25, 25, 0, 0, 0, 9, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 0, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 0, 0, 0, 0, 25, 9, 25, 0, 0, 0, 25, 0, 0, 0, 25, 25, 9, 25, 9, 0, 0, 25, 25, 9, 9, 0, 0, 0, 25, 25, 0, 0, 0, 25, 25, 9, 0, 25, 9, 9, 0, 0, 9, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 0, 0, 0, 0, 25, 25, 9, 0, 25, 9, 0, 0, 0, 25, 0, 25, 25, 9, 0, 0, 25, 25, 9]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P703
