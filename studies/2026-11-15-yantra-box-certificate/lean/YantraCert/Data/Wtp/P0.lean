module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P0
open YantraCert

def cell : Cell := ⟨1, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 33, 0, 0, 33, 33, 0, 33, 33, 0, 0, 0, 0, 1, 0, 1, 9, 9, 0, 0, 1, 0, 9, 0, 9, 9, 0, 1, 0, 1, 9, 0, 0, 0, 0, 41, 41, 1, 0, 0, 0, 0, 41, 9, 0, 0, 0, 41, 41, 0, 41, 41, 25, 0, 0, 41, 9, 0, 0, 0, 41, 0, 1, 25, 0, 41, 0, 1, 25, 25, 9, 0, 0, 0, 41, 0, 33, 41, 1, 0, 0, 0, 0, 41, 41, 0, 0, 0, 41, 0, 1, 41, 0, 41, 9, 0, 25, 25, 0, 0, 0, 41, 41, 41, 0, 0, 0, 41, 9, 0, 41, 9, 0, 0, 41, 41, 0, 41, 41, 82]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P0
