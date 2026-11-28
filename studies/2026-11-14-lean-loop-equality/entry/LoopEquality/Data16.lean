module

public import Mathlib
public import LoopEquality.Final16

@[expose] public section

/-!
# l = 16: the shape lists and the kernel checks

For the letters `a` of bilayer `-1` and `b` of bilayer `1` (bilayer `0` has letter `0`), `zqOf b` lists one
representative of each class of crossing sets carrying a meeting pair of far arcs (or the half-turn of one); computed by
`studies/2026-11-14-lean-loop-equality/l16/shapes16.py` and checked here by the kernel: every candidate's class is listed
(`hcheck16`), the list is of normalised, distinct four-point sets (`zq_props`), and the shape values sum to zero for
every kind of `v` (`sum16_kernel`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

def zq1 : List ((ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) := [
  ((-3, 0), (0, 0), (0, 3), (3, -3)),
  ((-3, 0), (0, 0), (0, 3), (3, 0)),
  ((-3, 3), (0, -3), (0, 0), (3, 0)),
  ((-3, 3), (0, 0), (0, 3), (3, -3)),
  ((-3, 3), (0, 0), (0, 3), (3, 0)),
  ((-3, 3), (0, 0), (0, 3), (3, 3)),
  ((-3, 3), (0, 0), (3, -3), (3, 0)),
  ((-3, 3), (0, 3), (3, 0), (3, 3)),
  ((-3, 6), (0, 0), (0, 3), (3, 0)),
  ((0, -3), (0, 0), (0, 3), (3, 0)),
  ((0, 0), (0, 3), (0, 6), (3, 0)),
  ((0, 0), (0, 3), (3, -3), (3, 0)),
  ((0, 0), (0, 3), (3, 0), (3, 3)),
  ((0, 0), (0, 3), (3, 0), (6, -3)),
  ((0, 0), (0, 3), (3, 0), (6, 0)),
  ((0, 0), (3, -3), (3, 0), (3, 3)),
  ((0, 3), (3, -3), (3, 0), (3, 3))]

def zq2 : List ((ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) := [
  ((-3, 0), (0, 0), (0, 3), (3, -3)),
  ((-3, 0), (0, 0), (0, 3), (3, 0)),
  ((-3, 3), (0, -3), (0, 0), (3, 0)),
  ((-3, 3), (0, 0), (0, 3), (3, -3)),
  ((-3, 3), (0, 0), (0, 3), (3, 0)),
  ((-3, 3), (0, 0), (0, 3), (3, 3)),
  ((-3, 3), (0, 0), (3, -3), (3, 0)),
  ((-3, 3), (0, 3), (3, 0), (3, 3)),
  ((-3, 6), (0, 0), (0, 3), (3, 0)),
  ((0, -3), (0, 0), (0, 3), (3, 0)),
  ((0, 0), (0, 3), (0, 6), (3, 0)),
  ((0, 0), (0, 3), (3, -3), (3, 0)),
  ((0, 0), (0, 3), (3, 0), (3, 3)),
  ((0, 0), (0, 3), (3, 0), (6, -3)),
  ((0, 0), (0, 3), (3, 0), (6, 0)),
  ((0, 0), (3, -3), (3, 0), (3, 3)),
  ((0, 3), (3, -3), (3, 0), (3, 3))]

def zqOf (b : ZMod 3) : List ((ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) :=
  if b = 1 then zq1 else if b = 2 then zq2 else []

/-- The canonical stacking letters: `a` at bilayer `-1`, `0` at `0`, `b` at `1`, `0` elsewhere. -/
def sig (a b : ZMod 3) (j : ℤ) : ZMod 3 := if j = -1 then a else if j = 1 then b else 0

def Zf (L : List ((ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ))) : Finset (Finset (ℤ × ℤ)) := (L.map toSet).toFinset

def hcheckB (a b : ZMod 3) : Bool :=
  (candQuads (sig a b) 0 (0, 0)).all (fun q => decide (nrm (toSet q) ∈ Zf (zqOf b)) &&
    decide (nrm (gP (0, 0) (toSet q)) ∈ Zf (zqOf b)))

def propsB (b : ZMod 3) : Bool :=
  decide (((zqOf b).map toSet).Nodup) && (zqOf b).all (fun q => dist4B q &&
    (q.1.1 % 3 == 0 && q.1.2 % 3 == 0 && q.2.1.1 % 3 == 0 && q.2.1.2 % 3 == 0 && q.2.2.1.1 % 3 == 0 &&
      q.2.2.1.2 % 3 == 0 && q.2.2.2.1 % 3 == 0 && q.2.2.2.2 % 3 == 0) && decide (nrm (toSet q) = toSet q))

def S16 (a b : ZMod 3) (v : Atom) : ℤ :=
  ((zqOf b).map (fun q => shapeVal4 (sig a b) 0 (0, 0) v q.1 q.2.1 q.2.2.1 q.2.2.2)).sum

set_option maxRecDepth 1000000 in
set_option maxHeartbeats 0 in
theorem hcheck16 : ∀ a b : ZMod 3, hcheckB a b = true := by decide +kernel

set_option maxRecDepth 1000000 in
set_option maxHeartbeats 0 in
theorem zq_props : ∀ b : ZMod 3, propsB b = true := by decide +kernel

set_option maxRecDepth 1000000 in
set_option maxHeartbeats 0 in
/-- **The kernel check of l = 16**: for every letter pattern and every kind of `v`, the shape values sum to zero. -/
theorem sum16_kernel : ∀ a b : ZMod 3, ∀ u : Fin 2,
    S16 a b (0, (0, 0), 0) = 0 ∧ S16 a b (-1, ((a.val : ℤ), (a.val : ℤ)), u) = 0 := by decide +kernel

end LoopEqualityProof
