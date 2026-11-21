# Bag of tricks (DICTO's methods toolkit, started 21 November 2026)

What we reach for, cheapest decisive test first. Each line: the trick, what it decides, where it was used.

## Tests that decide quickly
- **Dehn packet** (Σ length ⊗ angle mod Qπ): a solid that fills space alone has packet zero; a mixed tiling needs packets cancelling in proportion. Studies 2026-11-04-dehn-screen, 2026-11-21-packet-screen; #113, #116.
- **Edge-ring (local angle) test**: around every edge the angles must sum to 2π (π on a face). Kills tilings the packet allows (B3 permutohedron; the 12:1 and 20:1 icosahedral pairs, 540° rings). 2026-11-21-packet-leads-tiling.
- **Vertex ledger** (solid angles, Gauss–Bonnet on the vertex figure): what is left to fill at a corner. 2026-11-21-scutoid-stand-in.
- **Rationality of arccos(c)/π**: minimal polynomial of c divides Tₙ(x) − 1 (Chebyshev test). 2026-11-21-gap-study.
- **Galois twin rule**: two golden cuts are twins iff an automorphism sends K ↦ −K and √5 ↦ −√5. 2026-11-21-twin-rule-check.
- **Swap Corollary**: a kind-exchanging isometry forces a single switch at λ = 0. #53 v4.

## Exact machinery
- **PSLQ then proof**: find integer relations at high precision, then prove each exactly (sympy, minimal polynomials).
- **python-flint (FLINT 3)**: exact algebraic numbers and certified root isolation. 2026-11-21-flint-windows.
- **Normaliz with e-antic**: exact polytopes over Q(√5). 2026-11-21-normaliz-queens.
- **Interval arithmetic / separating-axis overlap tests** for placements (rigorous, not bare float).
- **SAT tiling search** (Kaplan's method): periodic patches on tori; proves "no periodic tiling with this lattice" or returns one. 2026-11-21-rt-pyramids-sat.
- **Lean 4 + Palomar**: machine-checked proofs, registered (Dehn Canon, Grünbaum, Yantra).

## How we search
- **Tree search with exact scoring** (after Language Agent Tree Search, Zhou et al. 2023): several rival approaches as branches, each scored by exact checks (not by self-judgement), expand the best, drop the rest. First used on the scutoid stand-in, 21 Nov 2026.
- **Pilot first** (≤ 5 min), then a watched job (dbbjob.sh: plan, PROGRESS lines, FINAL ok) on the compute hosts.
- **Controls that pass and fail** in every run (the octet must pass; a known non-filler must fail).
- **Survey map and gap triage**: every Concordance gap marked closed / closable / new paper / not a gap. 2026-11-21-survey-map, 2026-11-21-gap-study.
- **New-tools scan** of recent papers for methods matched to named gaps. 2026-11-21-new-tools.

## How we tell it
- **House style**: papers/HOUSE-STYLE.md (Winston: promise in a sober tone, cycling, fence, signposts, contributions close; Pledge, Turn, Prestige as backbone).
