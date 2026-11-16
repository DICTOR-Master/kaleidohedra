module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P604
open YantraCert

def cell : Cell := ⟨7, 111, 6, 45, 6, 31⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 25, 0, 9, 25, 0, 25, 25, 0, 0, 25, 0, 25, 9, 9, 0, 0, 0, 0, 9, 25, 0, 9, 25, 0, 0, 25, 25, 0, 25, 25, 0, 0, 0, 25, 9, 0, 25, 9, 9, 0, 0, 0, 58, 9, 9, 0, 0, 0, 25, 25, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 9, 25, 0, 9, 25, 0, 0, 25, 25, 0, 25, 25, 0, 0, 0, 25, 9, 0, 25, 9, 9, 0, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 25, 25, 0, 0, 25, 25, 0, 25, 9, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 0, 0, 0, 0, 0, 25, 9, 0, 25, 9, 9, 9, 0, 0, 0, 0, 25, 9, 0, 25, 9, 9, 9, 9]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P604
