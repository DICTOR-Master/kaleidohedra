# Lean: lead theorem of #117 (22 Nov 2026)

**DICTO's go-ahead:** formalize Theorem 4 of #117 "From Dehn Packets to Scutoids: How the Fullerene Star Fills
Space" (DICTO DOI: 10.5281/zenodo.24411660). Project on the compute host, `~/lean/palomar-packets`; this folder
mirrors its sources (no `.lake`). Toolchain and Mathlib pin as the Dehn Canon (`v4.35.0-rc2`).

## Status box
- Study, not published; no public repository (needs DICTO's approval).
- Built clean from scratch on the compute host: `lake build`, no `sorry`, axioms only propext, Classical.choice,
  Quot.sound (logs/build.log).
- Lemma 2 (angles round an edge, cited from #44) is a hypothesis (`LocalAngleCondition`), not proved here.
- Table 1's angles are entered in their closed forms; their derivation from the solids' coordinates is not formalized.

## What is proved
| file | result | paper |
|---|---|---|
| Packets/Angles.lean | `lemma3`: π, α, β, γ independent over ℚ; exact cos/sin of 2α, 4α, 2β, 2γ; `two_γ_eq` | Lemma 3 |
| Packets/Rings.lean | Table 1 as rational coordinates (`ti_eq`, …); `ring_weight_le`; `theorem4c_lead1/2`, `ring3pi_lead1/2`, `no_ring_lead1/2` | Theorem 4 (c) |
| Packets/Tiling.lean | `theorem4a`, `theorem4b` from `LocalAngleCondition` | Theorem 4 (a), (b) |

Method of Lemma 3: the field argument of the Dehn Canon's study 8 (credited in the file), with Niven's theorem.
Theorem 4 (a), (b): each of the paper's three steps is one weight q + u·a + v·b, nonnegative on every angle still
possible and above 2 on an angle of the piece removed; the ring bound (via Lemma 3) then removes the piece. The
order removes the dodecahedron in step 1 of (b), so the parity case of the paper's step 2 is not needed.

## LEADS
- Formalize Lemma 2 (geometric edge ring), possibly reusing the Canon's `tcone`/`wedgeAngle` framework.
- Derive Table 1's angles from coordinates (arccos forms) to tie the pieces to the solids.
