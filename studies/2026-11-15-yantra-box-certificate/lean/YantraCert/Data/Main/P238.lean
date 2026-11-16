module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P238
open YantraCert

def cell : Cell := ⟨6, 23, 6, 1, 6, 17⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 258, 0, 0, 9, 0, 66, 0, 0, 9, 66, 1, 1, 258, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 9, 25, 9, 1, 0, 0, 9, 0, 41, 41, 1, 1, 0, 0, 9, 0, 41, 25, 1, 0, 0, 0, 0, 0, 0, 0, 25, 25, 0, 25, 25, 9, 0, 0, 0, 41, 41, 0, 0, 0, 41, 41, 0, 9, 41, 41, 9, 0, 0, 0, 0, 0, 9, 0, 25, 58, 25, 0, 66, 25, 9, 0, 0, 0, 0, 9, 0, 0, 25, 41, 0, 25, 41, 41, 0, 0, 9, 0, 0, 25, 25, 25, 41, 9, 9, 0, 0, 0, 41, 25, 0, 41, 25, 9, 9, 9, 306]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P238
