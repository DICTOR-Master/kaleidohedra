module

public import YantraCert.Data.W.Polys

@[expose] public section

namespace YantraCert.Data.W.P0
open YantraCert

def cell : Cell := ⟨1, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 25, 9, 25, 0, 0, 0, 0, 1, 25, 0, 1, 25, 9, 25, 0, 0, 9, 25, 0, 9, 25, 1, 0, 0, 0, 0, 0, 0, 0, 1, 25, 0, 1, 25, 9, 25, 0, 0, 0, 0, 1, 25, 41, 9, 25, 0, 0, 9, 25, 0, 9, 25, 1, 0, 0, 0, 0, 0, 9, 25, 0, 9, 25, 0, 0, 9, 25, 0, 9, 25, 1, 0, 0, 0, 0, 9, 25, 0, 9, 25, 0, 0, 9, 25, 0, 9, 25, 1]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.W.P0
