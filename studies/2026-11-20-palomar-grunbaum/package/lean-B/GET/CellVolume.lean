module

public import GET.Real
public import GET.Statement

@[expose] public section

/-! Pilot of the measure step: the Lebesgue volume of a translated parallelepiped in Euclidean 3-space is `|det|`
(Mathlib's `addHaar_parallelepiped`), and for a golden rhombohedron of the model it is the `|D i j k|` used by the
exact checks. -/

namespace GET

open MeasureTheory ZPhi GrunbaumK10
open scoped Pointwise

/-- `volume (p + parallelepiped v) = |det v|` -/
theorem volume_vadd_parallelepiped (p : Space) (v : Fin 3 → Space) :
    volume (p +ᵥ parallelepiped v) = ENNReal.ofReal |(Matrix.of fun i j => v j i).det| := by
  rw [measure_vadd, ← (EuclideanSpace.basisFun (Fin 3) ℝ).addHaar_eq_volume,
    Measure.addHaar_parallelepiped, Module.Basis.det_apply]
  rfl

/-- an axis as a point of `Space` -/
noncomputable def rAxis (i : Fin 6) : Space := WithLp.toLp 2 (rv (axis i))

/-- the volume of a golden rhombohedron `p + [0,1]eᵢ + [0,1]eⱼ + [0,1]eₖ` is `|det(eᵢ, eⱼ, eₖ)|` -/
theorem volume_cell (p : Space) (i j k : Fin 6) :
    volume (p +ᵥ parallelepiped ![rAxis i, rAxis j, rAxis k]) =
      ENNReal.ofReal |toReal (D i j k)| := by
  rw [volume_vadd_parallelepiped, D, ← toReal_det3, ← Matrix.det_transpose]
  congr 3
  ext a b
  fin_cases a <;> fin_cases b <;> rfl

end GET
