module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P367
open YantraCert

def cell : Cell := ⟨9, 383, 9, 228, 8, 132⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 0, 25, 0, 0, 0, 25, 25, 25, 9, 25, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 41, 25, 41, 25, 0, 9, 25, 0, 0, 41, 0, 25, 0, 9, 41, 0, 9, 0, 25, 41, 25, 9, 0, 0, 41, 0, 0, 9, 0, 0, 25, 0, 0, 41, 25, 9, 25, 0, 9, 0, 41, 25, 9, 25, 9, 0, 0, 0, 0, 0, 25, 0, 0, 9, 0, 41, 0, 0, 0, 41, 25, 41, 41, 41, 9, 41, 0, 0, 0, 0, 25, 0, 9, 0, 0, 0, 9, 0, 41, 25, 41, 25, 25, 0, 9, 25, 0, 0, 0, 0, 9, 0, 41, 0, 0, 9, 25, 0, 9, 0, 41, 25, 41, 0, 25, 0, 9, 0, 0, 25, 0, 9, 0, 41, 9, 9, 0, 9, 0, 25, 0, 0, 0, 25, 0, 0, 41, 25, 9, 25, 9, 9, 0, 25, 25, 25]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P367
