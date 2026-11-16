module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P656
open YantraCert

def cell : Cell := ⟨7, 110, 6, 48, 6, 31⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 9, 0, 9, 9, 26, 0, 0, 9, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 0, 25, 0, 25, 25, 0, 25, 9, 0, 0, 25, 25, 0, 25, 9, 0, 9, 0, 0, 0, 9, 0, 25, 25, 26, 0, 0, 0, 25, 25, 0, 25, 9, 0, 0, 25, 25, 0, 25, 9, 0, 0, 0, 0, 26, 0, 0, 0, 25, 25, 0, 25, 9, 26, 0, 9, 9, 26, 0, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 25, 9, 9, 0, 26, 9, 9, 9, 0, 0, 26, 0, 0, 9, 0, 26, 0, 0, 0, 25, 25, 0, 25, 9, 0, 26, 0, 25, 9, 26, 0, 26, 0, 0, 0, 26, 9, 9, 26]

theorem ok : checkTree C 12 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P656
