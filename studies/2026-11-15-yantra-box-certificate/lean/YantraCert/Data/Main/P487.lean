module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P487
open YantraCert

def cell : Cell := ⟨20, 786892, 20, 474178, 20, 544895⟩
noncomputable def codes : TC := TC.ofList [0, 9, 25]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P487
