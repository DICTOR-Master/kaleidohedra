module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P330
open YantraCert

def cell : Cell := ⟨2, 2, 2, 0, 1, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 210, 0, 0, 0, 0, 226, 282, 226, 0, 9, 226, 0, 0, 0, 0, 0, 9, 274, 9, 0, 0, 9, 0, 0, 9, 9, 0, 9, 9, 9, 0, 282, 0, 0, 82, 258, 0, 9, 9, 0, 9, 0, 282, 0, 9, 9, 0, 9, 210]

theorem ok : checkTree C 12 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P330
