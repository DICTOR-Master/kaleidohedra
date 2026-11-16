module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P2
open YantraCert

def cell : Cell := ⟨1, 1, 1, 1, 1, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 1, 0, 0, 9, 9, 0, 9, 9, 0, 1, 0, 0, 9, 9, 0, 9, 9, 0, 114, 0, 34, 0, 0, 0, 9, 9, 0, 9, 9, 0, 114, 0, 9, 0, 9, 9]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P2
