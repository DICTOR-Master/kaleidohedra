module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P287
open YantraCert

def cell : Cell := ⟨3, 4, 3, 0, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 9, 0, 226, 0, 138, 9, 9, 0, 0, 9, 0, 0, 0, 9, 274, 9, 0, 0, 9, 0, 0, 0, 9, 0, 66, 0, 0, 9, 0, 25, 25, 9, 9, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 9, 9, 9, 9, 0, 0, 9, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 9, 9, 9, 9, 0, 226, 0, 0, 0, 266, 0, 0, 0, 82, 0, 0, 0, 0, 0, 0, 25, 25, 0, 25, 25, 9, 0, 0, 0, 0, 0, 0, 25, 25, 25, 9, 0, 0, 0, 41, 41, 0, 25, 41, 9, 0, 25, 0, 0, 0, 25, 25, 9, 0, 25, 25, 9, 0, 0, 58, 58, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 0, 25, 25, 9, 0, 66, 0, 0, 0, 66, 58, 9, 0, 0, 66, 58, 66, 0, 9, 9, 282, 0, 9, 282]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P287
