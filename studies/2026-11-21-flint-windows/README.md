# Exact edges of the open windows of DICTO's growth rule (gap L29, with L28)

21 November 2026. Papers: The Gains of DICTO's Growth Rule (#80) and Core Cycles (#81). Earlier study: 2026-11-09-b1-walls.

## Question
DICTO's growth rule T(S) = {x : v·x ≤ v·v for every corner v} is applied again and again to two solids. The edge-cut cube has
planes x = ±1 and (±1, ±1, 0)·x ≤ 2s. The edge-cut dodecahedron has its five-fold planes at foot 1 and its two-fold planes at
foot s. In both, the chain closes for small and large s and stays open in a middle window. #80 and #81 give the windows only
on a grid: cube open for 49/80 to 59/80, dodecahedron open for 87/80 to 99/80. Where exactly are the edges? Gap L28 (the claim
"Archimedean chains close in four steps") rests on the same windows.

## Method
1. **Type.** At one depth, floating point reads each step's corners, the planes through each corner, and one independent
   triple of them.
2. **Transport.** That type is solved from its triples (Cramer's rule) in other number systems: arb balls (any precision), exact
   rationals, Q(√5), an exact number field Q[x]/(f), and Q(√5)(s) with the depth s as a symbol.
3. **Edge (edge.py).** Bisect in floating point to the change of regime. Carry the closing side's type across it in arb: the
   slacks whose certified sign flips form the wall. Find their root by the secant method in arb, ramped to 6400 bits. FLINT's
   LLL gives a candidate integer polynomial, FLINT factors it, and FLINT's certified root isolation picks the factor root that
   meets s*. **Proof:** the chain is solved exactly in K = Q[x]/(f) (√5 found inside K and checked to square to 5), and the
   wall determinant comes out exactly zero there, along with every incidence of the earlier steps.
4. **Regimes on whole intervals (sym.py).** The depth stays a symbol. Each coordinate is stored as (A + B√5)/E with A, B, E in
   Q[s] (FLINT fmpq_poly) and the rational gcd taken out; this form is canonical up to a constant. Every incidence must hold
   identically in s. The walls are the genuine real roots of all free-slack numerators and corner determinants: roots of the
   norm A² − 5B², kept where A + B√5 itself vanishes, decided with arb or by exact divisibility. The hop is the pair of walls
   nearest the sample. Closure is tested as an identity in s. So on the whole open hop the type is fixed and the closure holds.
5. **Samples (certify.py).** At rational depths, every corner is computed exactly and checked: tight incidences exactly zero,
   free slacks certified negative, and Euler V − E + F = 2 so that no corner is missing. Then either closure holds exactly,
   or non-closure is certified by a corner with no parallel partner.

**What python-flint did that sympy could not.** Study 2026-11-09-b1-walls did step 4 in sympy. Its runs took over 30 minutes
per step at step 3 to 5 and were stopped (METHOD-FAILED). In FLINT the same symbolic chain of the dodecahedron at 27/25 runs
all eight steps in 35 s, with coordinate degree up to 26. The cube runs in 1 s. FLINT also supplied certified root isolation,
LLL, polynomial factoring and the exact field arithmetic. python-flint 0.9.0 does not expose qqbar. Its role is filled by
fmpz_poly.factor plus certified complex_roots (algebraic number = minimal polynomial + isolating ball) and the exact field
class NF.

## Controls
- **Floating-point map** (map.py, 0.01 grid, 12 steps) reproduces b1-walls. Cube: period 4 from step 0 at 0.50; from step 3 on
  0.51–0.60; open 0.61–0.74; from step 1 on 0.75–0.99; period 2 at 1.00. Dodecahedron: from step 0 on 0.40–1.00; from step 3
  on 1.01–1.08; open 1.09–1.24; from step 1 on 1.25–1.37; period 2 from 1.39. At 1.16 and 1.38 floating point is degenerate.
- **Known edges found again by edge.py:** the dodecahedron's 3 − φ (s² − 5s + 5, b1-walls) and 1, both exact.
- **Known gains found exactly by certify.py:**

  | solid | depth | squared radius gain | gain | source |
  |---|---|---|---|---|
  | cube | 1/2 | 25/4 | 5/2 | #80 |
  | cube | 1 | 9 | 3 | #80 |
  | dodecahedron | 3/4, 1 | 2350 − 1050√5 | 35 − 15√5 = 10/φ⁴ | #80 |
  | dodecahedron | 29/20 | 405 − 180√5 | 15 − 6√5 | #80 |
  | cube | 43/50 | 4.4093410731 | | b1-walls |

## Exact window edges

| solid | edge | exact value | minimal polynomial | isolating interval | wall | proof |
|---|---|---|---|---|---|---|
| cube | lower | 3/5 | 5s − 3 | — | step 1 (48 slacks) | edge.py exact in Q; sym.py hop (1/2, 3/5) ends at 3/5 |
| cube | upper | 3/4 | 4s − 3 | — | step 1 (8 slacks) | edge.py exact; sym.py hop (3/4, 1) starts at 3/4 |
| dodecahedron | lower | s* = 1.08734 39609 18100 83601 00974 44062 56504 61361… | 144s⁶ − 528s⁵ + 640s⁴ − 196s³ − 124s² + 40s + 25 | [27/25, 11/10] (one root; f(27/25) > 0 > f(11/10)) | step 3 (20 slacks) | edge.py exact in K = Q(s*), √5 ∈ K; sym.py hop (1, s*) ends at the same root |
| dodecahedron | upper | 5/4 | 4s − 5 | — | step 1 (20 slacks) | edge.py exact in Q(√5); sym.py hop (5/4, 3 − φ) starts at 5/4 |

Over Q(√5), the dodecahedron's s* is the only real root of the golden cubic

  **12s³ − 4(4 + 3φ)s² + 4(1 + 5φ)s − 5φ² = 0**

whose norm is the sextic above. The cubic's other two roots are 0.93201 ± 0.36685i. The sextic's other real root, 1.32943…,
belongs to the conjugate cubic, not to the chain. b1-walls had bisected this edge to 1.08734394 ± 4·10⁻⁸ and left its
exact form open.

Every edge depth itself closes, checked exactly:

| solid | edge | period | squared radius gain | gain |
|---|---|---|---|---|
| cube | 3/5 | 4, from step 3 | 475719721/121550625 | 21811/11025 |
| cube | 3/4 | 4, from step 1 | 1681/576 | 41/24 |
| dodecahedron | 5/4 | 4, from step 1 | 387/40 − (143/40)√5 | (55 − 13√5)/20 |
| dodecahedron | s* | 4, from step 3 | | |

The dodecahedron at s* closes as the limit of the identity on (1, s*). The corners stay finite there, because the wall's
triple does not degenerate.

So the open windows are exactly:
- **cube: 3/5 < s < 3/4**
- **dodecahedron: s* < s < 5/4**, s* = 1.0873439609…

On the closing side of every edge, the type and the closure identity are proved over the whole hop:

| solid | hop | closure |
|---|---|---|
| cube | (1/2, 3/5) | period 4 from step 3 |
| cube | (3/4, 1) | period 4 from step 1 |
| dodecahedron | (2/5, 1] | period 4 from step 0, constant gain 10/φ⁴ |
| dodecahedron | (1, s*) | period 4 from step 3, gain varying with s |
| dodecahedron | (5/4, 3 − φ) | period 4 from step 1, gain varying with s |
| dodecahedron | (3 − φ, 3/2] | period 2, constant gain 15 − 6√5 |

The hops for (1, s*) and (5/4, 3 − φ) are new; sympy could not reach them.

Inside the windows, at exact samples, there is no closure within 8 steps for the cube (6001/10000, 61/100, 7/10; 749/1000
within 7) and within 7 steps for the dodecahedron (136/125, 11/10, 6/5, 1249/1000). The symbolic type there changes at walls
that crowd together step by step. Around the cube's 7/10 the hop is (0.69940, 0.70008) by step 4, its ends roots of degree 6
and 13. The open-side walls also crowd towards the edges (cube: a step-6 wall at 3/5 + 5·10⁻¹⁰). "Open" remains, as in #80,
"no closure within the steps run", now certified exactly at each sample.

## Verdict
- **L29: CLOSED.** The edges are exact.
  - Cube: 3/5 and 3/4, both rational, proved as walls of step 1 and as ends of proved closing hops.
  - Dodecahedron: 5/4 (rational, wall of step 1) and s*, an algebraic number of degree 6 (degree 3 over Q(√5)), wall of step 3.
  - #80's sentence "closes in four steps for s ≤ 3/5 and for s ≥ 3/4" is exactly right for the cube.
  - For the dodecahedron, "closes for s ≤ 43/40" becomes "closes for s ≤ s*", and the window is (s*, 5/4).
- **L28: answered for the two-family solids, not for the Archimedean claim.** The cube and dodecahedron chains close with
  period 4 (or 2) everywhere outside these exact windows, proved on every hop listed above, and stay open inside. So "close in
  four steps" is false in general. A proof for the Archimedean chains, and the omnitruncates, remains open; sym.py is the tool
  for that next run.

## Proposed home
- #80 next version: Section 6, the exact windows (3/5, 3/4) and (s*, 5/4) with the golden cubic, replacing "not located".
- #81 next version: Section 7 and the "Not decided here" list, the same edges with a pointer to #80.
- Concordance rows L28/L29 to be updated; this study does not edit concordance.json.

## LEADS
1. Archimedean chains (L28): run sym.py on the truncated cube, truncated octahedron and rhombicuboctahedron, cut at a symbolic
   depth, to prove period 4 on whole hops. The omnitruncates are the open case.
2. The gain as a function of s on each closing hop is now an explicit rational function: degree 24 for the cube on (1/2, 3/5),
   degree 40 for the dodecahedron on (1, s*). Its values at the edges are 21811/11025, 41/24 and (55 − 13√5)/20 in radius.
   Do they form a pattern?
3. Inside the windows the walls accumulate at the edges. Is there an infinite sequence of walls converging to 3/5 and to s*,
   and does the chain settle or spread between them?
4. The step-1 walls 3/5, 3/4, 5/4 and 3 − φ are rational or golden, while s* is a step-3 wall of degree 6. A closed form or
   geometric meaning for the golden cubic (which corner meets which plane) would suit #80's text.

## Files
- scripts/fw.py: solids, number systems, transport, LLL.
- scripts/edge.py: one exact edge.
- scripts/sym.py: symbolic chain in Q(√5)(s).
- scripts/certify.py: exact sample.
- scripts/map.py: floating-point map.
- data/: edge-*.log/json, sym-*.txt, cert-*.txt, map-*.txt.
- log.txt: run list.
