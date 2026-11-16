module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P452
open YantraCert

def cell : Cell := ⟨19, 393445, 19, 237088, 19, 272446⟩
noncomputable def codes : TC := TC.ofList [0, 25, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P452
