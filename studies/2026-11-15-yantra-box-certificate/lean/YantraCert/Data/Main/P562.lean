module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P562
open YantraCert

def cell : Cell := ⟨7, 97, 6, 29, 6, 33⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 9, 25, 0, 9, 0, 25, 25, 0, 25, 25, 0, 0, 25, 0, 25, 9, 0, 25, 25, 0, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 0, 0, 9, 25, 0, 9, 0, 25, 25, 25, 0, 0, 9, 25, 0, 9, 25, 0, 0, 0, 0, 9, 25, 9, 0, 0, 9, 25, 9, 0, 25, 0, 25, 9]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P562
