module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P438
open YantraCert

def cell : Cell := ⟨19, 393445, 19, 237087, 19, 272446⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 9, 0, 9, 41, 9, 0, 9, 0, 25, 9, 9]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P438
