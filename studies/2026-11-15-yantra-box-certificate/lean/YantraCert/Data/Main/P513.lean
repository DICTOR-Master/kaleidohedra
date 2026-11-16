module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P513
open YantraCert

def cell : Cell := ⟨15, 24591, 14, 7409, 14, 8514⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 41, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 41, 0, 41, 9, 41, 0, 9, 0, 25, 41, 41, 0, 9, 0, 25, 0, 41, 0, 9, 0, 0, 41, 25, 41, 41, 9, 0, 0, 41, 0, 0, 9, 25, 9, 25, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 41, 25, 25, 25, 0, 41, 0, 9, 0, 0, 0, 9, 0, 25, 9, 25, 9, 0, 9, 0, 25, 0, 0, 9, 0, 25, 9, 25, 9, 0, 0, 0, 0, 9, 0, 0, 41, 9, 0, 0, 0, 0, 0, 25, 41, 9, 0, 25, 9, 41, 9, 9, 0, 0, 9, 0, 0, 0, 25, 0, 0, 0, 0, 41, 25, 41, 9, 0, 0, 25, 0, 41, 25, 9, 9, 25, 9, 0, 25, 0, 0, 0, 41, 0, 0, 0, 41, 0, 0, 25, 41, 0, 9, 41, 41, 9, 25, 9, 25, 9, 25, 9]

theorem ok : checkTree C 22 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P513
