module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P568
open YantraCert

def cell : Cell := ⟨7, 97, 7, 60, 7, 67⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 9, 0, 25, 0, 25, 9, 9, 0, 0, 9, 0, 0, 0, 9, 25, 9, 0, 0, 9, 0, 25, 25, 9, 9, 0, 0, 0, 25, 25, 9, 0, 0, 0, 25, 25, 25, 9]

theorem ok : checkTree C 10 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P568
