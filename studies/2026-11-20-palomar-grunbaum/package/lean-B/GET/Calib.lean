module

public import GET.Certs

@[expose] public section

/-! Calibration of `EveryZoneHas`: the zones of the cube have 4 faces and those of the rhombic dodecahedron 6. -/

namespace GET

open ZPhi GrunbaumK10

theorem ev_lit (a b c : ℤ) : ev ![⟨a, 0⟩, ⟨b, 0⟩, ⟨c, 0⟩] = !₂[(a : ℝ), b, c] := by
  unfold ev; congr 1; funext x; fin_cases x <;> simp [rv, toReal]

theorem cube_cert : ZoneCert cubeX 4 cubeZ := by decide +kernel

theorem rd_cert : ZoneCert rdX 6 rdZ := by decide +kernel

theorem cubeX_eq : (fun i => (cubeX i).toPar) = cubeFaces := by
  funext i
  fin_cases i <;> simp [cubeX, cubeFaces, XPar.toPar, ev_lit]

theorem rdX_eq : (fun i => (rdX i).toPar) = rhombicDodecahedronFaces := by
  funext i
  fin_cases i <;> simp [rdX, rhombicDodecahedronFaces, XPar.toPar, ev_lit]

theorem cube_zones : EveryZoneHas cubeFaces 4 := cubeX_eq ▸ everyZoneHas_of_cert _ _ _ cube_cert

theorem rd_zones : EveryZoneHas rhombicDodecahedronFaces 6 := rdX_eq ▸ everyZoneHas_of_cert _ _ _ rd_cert

end GET
