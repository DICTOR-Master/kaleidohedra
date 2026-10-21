# The DICTO Mandala of Shells: exact map (groundwork for #46, DICTO's idea; 2026-10-21)

All of DICTO's shell cycles tested against three operations, T (UP step), φP (golden turned-out step) and ρ (polarity; ρP = Tρ, Lemma 3 of #43), plus scaling.
The work is exact in ℚ(√5) and runs on the node with the #38/#39 machinery (`nc_common.py` of 2026-10-21-new-cycles).
`mapping.py` → `mapping.log` (153 PASS, 0 FAIL) and `mandala-map.json` (124 station nodes, 105 step edges, 20 cycle links, 27 similarity classes, OTT-under-T rows).
`map_figure.py` → `figures/mandala-map.png` is the first draft of the map: nodes are named solids up to scale, arrows are coloured by operation, and the drawing is float.

**Method.** Every station is built exactly from its paper's definition (sizes and contacts as stated there) and checked against the paper's own numbers, e.g. RT edge² = (45 − 18√5)/4, the #34 contacts, Cleo tips = (2/3)D and the GSD tips = D(φ).
For each step A → B we test whether B = c·A, c·T(A), c·P(A), c·polar(A) or c·rect(A) (edge midpoints) for an exact c, comparing corner sets exactly.
The labels mean:
- **T**: B = T(A) with c = 1.
- **φP**: B = φP(A), i.e. c = φ.
- **P**: B = P(A) with c = 1.
- **ρ**: B = s·polar(A), polarity in the sphere of radius² s. For a solid with one corner radius this is also c·T.
- **other**: none of these. The operation is then taken from the paper.

## Status per cycle (all **exact**; no station needed floats)

| Cycle | Steps | Result |
|---|---|---|
| #22 Chain of Karma | I→D→I→D | **ρ** every step (dual at a chosen size; s = (3+√5)/8, (11+5√5)/8, …). Not T (c = 1.894) and not φP (c = 3, √5). The physical operation is face-on placement (pyramids, AXE, CLEO, FUJI). |
| #23 Spheres of Dharma | I→ID→D→TI→H→RT→I·φ³ | I→ID is a scaled rectification (c = φ²). Every other step is **other**: pyramids, cage, Shields, caps, loose nest. |
| #32 Inverted Shells | D→ID→OG→PD→I→RT→D·φ³ | **ρ of #23** as a whole. Its own steps are other, except D→ID, a scaled rectification. |
| #33 Double Vision | union, two settings | Links #23 and #32 by ρ, s = φ²/4 (shares I, D) or 3φ²/4 (shares ID, RT). The settings differ by exactly 3. Within the union, a few steps are ρ; the rest are other. |
| #34 Progenitors | 9 stations | **other**, except I→ID (rect). |
| #35 Vajrayana | 12 stations | **other**. I→Cleo star is a Kleetope with tips = 2P(I) exactly. The star's hull is D′. |
| #38 Universal PiTet | ID→RT→GTI→FPD→ID·10/φ⁴ | **T** at every step (c = 1). |
| #38a Kepler–Poinsot–UP | I→GSD→D(φ)→SSD→I(φ³) | Two stellations: GSD tips = 3P(I) and SSD tips = √5·P(D) exactly. Each is followed by the convex hull. Hull to hull is ρ, as in #22. |
| #39 OG family | OG→KRE→…; OG→TPH→… | Up: **T** at every step. Down: **P** at every step (c = 1). T undoes P on all 4 down steps. |
| Cleo Towers | beats 0,1,2,4,7,12 | **T, T, T², T³, T⁵** exactly. |
| Polar Cleo Towers | ρ (r² = 15 − 5√5) of the above | **P, P, P², P³, P⁵** exactly (ρ turns T into P). |
| #43 OG turned out | OG→φTPH→… | **φP** at every step. |
| #43 its polar | H→T H/φ→… | T × 1/φ at every step (T, then scale). |
| new A: CLEO turned out | ID→FPD→GTI→RT→ID | **φP**. |
| new B: polar of OG up | H→P H→… | **P** (c = 1). |
| new C: OTT turned out | OTT→ID→FPD→GTI→RT | **φP**. |

Things that do not fit the three operations:
- The Dharma family's construction steps (#23, #32, #34, #35): face-on placement, caps, Shields, cage, loose nests and the rectification steps.
- The Kleetope and stellation steps (Cleo star, GSD, SSD), with their convex hulls. Each is "tips = k·P", with k = 2, 3 or √5, so it is P at a non-golden height.

## Links between cycles (exact)
- **#22 = #23 at the hinge.** #22 and #23 share I(1/φ), D(1) and I(φ²).
- **#38a hulls = φ × #22.** The hulls of #38a are φ times the stations of #22: one orbit.
- **One Kleetope rule.** The Cleo star (2P) and the GSD (3P) follow the same rule at two heights: (3/2)φ × Cleo tips = GSD tips. #35's D′ = (2/3)·#22's D(1).
- **#32 = ρ(#23)** station by station, order reversed. #33 is #23 ∪ s·ρ(#23).
- **#34's O comes from #33 middle.** O = (3φ²/4)·ρ(H), the #33 middle-setting polar of #23's H.
- **Sub-sequences.** #34 holds 6 of #23's 7 stations exactly (all but D). #35 holds all 9 stations of #34.
- **One OG.** #39's OG is #32's and #34's OG up to scale.
- **#39's KRE = T(OG) is similar to #34's jtI** (the polar of rTI, built at the stated contacts). Accordingly, new B's P H is similar to #34's rTI.
  This is new here and is shown in the class listing in the log (class 9 and class 8).
- **#38 and #23.** #38's ID and RT are #23's ID and RT up to scale: #23's RT = (9 − 3√5)/2 × T(#23's ID). #38's GTI and FPD are not the TI and PD (exact).
- **Cleo Towers = the #38 orbit** at Fibonacci beats. The Polar Cleo Towers are ρ of it, which is the same orbit, because #38 is self-polar about the GTI sphere (checked k = 0..4).
- **#39 and #43.**
  - The OG turned out is φᵏ × #39 down, beat by beat.
  - Its polar is φ⁻ᵏ T^k(H).
  - New B = ρ(#39 up) = P^k(H).
  - So H is the hinge: T and P from H are polar to P and T from the OG.
- **New A = #38 run backwards**: S_k = (φᵏ/λ)·T^(4−k)(ID), λ = 10/φ⁴.
- **New C = (2/3) × A one beat behind.** The OTT → ID step is itself φP.
- **Classes and duals.** There are 27 similarity classes. Their dual (ρ) pairs: I–D, ID–RT, TI–PD, H–OG, rTI–jtI, GTI–FPD, PHE–P²H, TPP–P³H, DPHP–P⁴H, TPH–T H, TQH–T²H, TQP–T³H, TQHD–T⁴H.

## Missing cell: the DICTO OTT under T (k ≤ 4, exact; T_h symmetry throughout, never icosahedral)

| k | corners | faces | face kinds | T^(k−1) inside T^k | P(T^k) = T^(k−1) |
|---|---|---|---|---|---|
| 0 | 24 | 38: 24 + 8 triangles, 6 four-sided | 3 | – | – |
| 1 | 44 | 24: 12 triangles, 12 octagons | 2 | yes | yes |
| 2 | 68 | 36: 24 four-sided, 12 nonagons | 2 | **no** (8 corners outside) | no |
| 3 | 108 | 68: 8 tri, 24 four-sided, 12 pent, 24 heptagons | 4 | **no** (36 outside) | yes |
| 4 | 98 | 60: 24 four-sided, 24 + 12 hexagons | 3 | **no** (72 outside) | no |

Unlike φP, which makes the OTT icosahedral after one beat, T keeps the OTT pyritohedral. T does not nest from k = 2 on.
Lemma 3 is checked on the OTT: polar(T(OTT)) = P(polar OTT).

## Not done / caveats
- The stars are non-convex. They enter only through their tips and hulls; T, P and ρ are tested on convex hulls only.
- In the #33 unions, a step between the two cycles has no single operation. The cycle-level link is ρ.
- The figure is a first draft. It omits the OTT rows and the #33 unions (they are in the JSON). It draws the KRE and the jtI as one node, and the GSD and SSD as nodes inside the ring.

Run: `python3 mapping.py <five-fold-octet> <ott-rays/cut8-exact.json>` (603 s on the node); `python3 map_figure.py`.

DICTO · dictospheres.com
