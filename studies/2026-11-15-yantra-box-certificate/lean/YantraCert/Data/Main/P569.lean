module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P569
open YantraCert

def cell : Cell := ⟨7, 97, 7, 61, 7, 66⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 25, 25, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 25, 25, 25, 25, 0, 0, 9, 0, 0, 41, 41, 41, 0, 9, 0, 0, 0, 9, 0, 25, 41, 25, 41, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 41, 25, 25, 0, 0, 9, 0, 0, 25, 41, 9, 0, 9, 0, 0, 0, 9, 0, 41, 9, 0, 9, 0, 0, 41, 0, 9, 0, 25, 41, 9, 9, 0, 9, 0, 0, 25, 25, 0, 0, 9, 0, 0, 0, 9, 0, 25, 9, 0, 9, 0, 25, 9, 9, 0, 9, 0, 25, 9, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 9, 25, 0, 9, 0, 25, 25, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P569
