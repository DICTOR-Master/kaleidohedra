# Number audit — #54 (proposed) "What Each Step Adds" draft v1, 2026-10-25

Every number in paper.src.html checked. Sources: **G** = studies/2026-10-24-gnomon-cycle (gnomon-all12.txt, gnomon-exact.txt, gnomon-table.txt, README),
**K** = studies/2026-10-23-shadow-forms/polar (keyed-polar-exact.txt, keyed_polar1.py output, polarfill1.txt), **C** = this folder's checks.txt
(26 PASS, ALL PASS), **P** = papers #34/#35/#28/#48 and collected/collected.html (DOIs). All scripts re-run on dicto-big-brother 2026-10-25.

| # | Number in the paper | Where | Source | Result |
|---|---|---|---|---|
| 1 | I edge 1/φ, V(I) = (5/12)(√5 − 1) = −5/12 + (5/12)√5 | §2, Table 1 | C "I is the icosahedron of edge 1/φ"; G | PASS |
| 2 | Table 1 volumes, 12 rows | Table 1 | G gnomon-all12.txt (rerun identical) | PASS |
| 3 | Table 1 V/I exact, 11 rows; decimals 4.4086 … 76.0132 | Table 1 | G; C "Table 1 column V/I" | PASS |
| 4 | strict growth in this order | Table 1 caption | G PASS line; C | PASS |
| 5 | snap grid (1/16)ℤ, error < 10⁻⁶; 32 face planes → 32 poles; ρ² = 9/4 | §2 | gnomon_all12.py (assert 1e-6; PASS 32) | PASS |
| 6 | method reproduces TI, H, RT, I·φ³ at same scale | §2, App. | G 4 PASS lines | PASS |
| 7 | Cleo star = 2I; gnomon I | Thm A(i), abstract | G exact; C | PASS (already in #35 — cited [5]) |
| 8 | M = φ⁸I, φ⁸ = (47 + 21√5)/2; I·φ³ = φ⁹I = (38 + 17√5)I = φ·M; last gnomon φ⁷I | Thm A(ii) | G; C | PASS |
| 9 | RT = 81I/φ²; M/RT = φ¹⁰/81; I·φ³/RT = φ¹¹/81 | Thm A(iii) | G pairs list; C | PASS |
| 10 | 66 ratios, exactly 10 neat, all among I, star, RT, M, I·φ³; list in Table 2 caption | Thm A(iv) | G pairs list (10 lines); C exhaustive test | PASS |
| 11 | 11 gnomons, exactly 4 neat: I, (3/4)φ⁻²I, 18φ⁻⁴I, φ⁷I | Thm A(v), Fig. 1 | G; C exhaustive (Fibonacci/Lucas) | PASS |
| 12 | gnomon exact forms and decimals (Table 2) | Table 2 | C printed lines; G decimals | PASS |
| 13 | step ratios 2.0000 … 1.6180 (Table 2); float survey 1.01–3.23 | Table 2, §1 | G gnomon-all12 step column; README (float survey) | PASS (exact range 1.0114–3.2265) |
| 14 | sum of gnomons (φ⁹ − 1)I | Thm A(v) | C | PASS |
| 15 | 60 corners of TI, 90 edges; 20 Shields; 60 pieces in M → I·φ³; 20 Cleo-Icos | §3 | TI classical; #28 (Shield); Progenitors README Step 13 (60 of one kind); #35 | PASS |
| 16 | OG at 3φ²/4; D′ = (2/3)D | Table 1 | Progenitors README Steps 4, 9 | PASS |
| 17 | Icosaxes perms (±1/2, ±φ/2, 0); Unborn Axes perms (±1/(2φ), ±φ/2, 0) at (φ/2)(1,1,1) + φℤ³ | §4 | keyed_polar_exact.py; #48 | PASS |
| 18 | Tricap (3 − √5)/24 = 1/(12φ²); 8 Tricaps 1 − √5/3 ≈ 0.2546 | §4, abstract | K (1); C | PASS |
| 19 | √5 = (1 + 2√5/3) − 8/(12φ²); 2 = (1 + √5/3) + 8/(12φ²); sum φ³ | §4 | K (3a–3d); C | PASS |
| 20 | Tricap base corners = Unborn corners, apex on cube of Unborn's dodecahedron, dents inside I, pairwise apart | §4 | K (2a, 2a', 2c, 2e) | PASS |
| 21 | polar heights x/(1+x), 1/(1+x), sum 1 | Thm B(i) | C sympy | PASS |
| 22 | heights 1/φ, 1/φ²; 1/φ + 1/φ² = 1 | Thm B(ii) | K (4a, 4b); C | PASS |
| 23 | apex 2/φ; cube corners 2√3/φ² ≈ 1.323, 2√3/√5 | Thm B(ii), (iv) | C; keyed_polar1 output 1.236068, 1.323169, 1.549193 | PASS |
| 24 | dent apex (1,1,1)/(2φ); base (0, 1/2, φ/2) etc.; hexagon x+y+z = φ²/2 | proof B(iv) | C | PASS |
| 25 | dent-wall pole √(10 − 2√5) = 4 sin 36° ≈ 2.351; angle ≈ 37.38° | Thm B(iv) | C (exact distance; angle float from exact vectors); open-work 10-24 "2.35 vs 1.32, 37°" | PASS |
| 26 | Kelvin x = 1: heights 1/2 | Remarks | C | PASS |
| 27 | edge angles 136.35°, 153.43°, 150.77°, 131.81°; no combination 360° | Remarks | K polarfill1.txt (float) | PASS (float, labelled) |
| 28 | Tricap polar edges 3 + 3, ratio 1 : tan 72°, tan²72° = 5 + 2√5 | Remarks, Fig. 2 | K (5a, 5b); C | PASS |
| 29 | check counts 4, 9, 1, 15, 26 = 55 | abstract, App. | G, K, C outputs | PASS |
| 30 | (n+1)² = n² + n + (n+1); 9 + 3 + 4 = 16 | In short, §1 | C symbolic; arithmetic (n = 3) | PASS |
| 31 | DOIs #48 23596362, #23 23310833, #34 23413184, #28 23360857, #35 23429911, #35a 23430864 | refs | collected.html v24 entries; doi.org resolves (302) | PASS |
| 32 | Crossref: 10.24200/squjs.vol21iss2pp139-149 (Koca et al. 2016, 21, 139); 10.1017/CBO9780511569371 (Wenninger, Dual Models, 1983); 10.5962/bhl.title.11332 (Thompson 1917) | refs | api.crossref.org 2026-10-25 | PASS |
| 33 | study commits afd8a42, 4b05e6f, 4cac277; 4c18a0b, e9aed63 | refs | git log | PASS |

Notes: saved gnomon-table.txt has one extra line ("RT/I x phi^2 = 81 + 0 sqrt5") not printed by gnomon_table.py; the value is check #9.
Wording (re-audited v1b): "DICTO proposed that the polar has no spikes over the dents" (was "doubted"); grep doubt|ask|question|wonder: only the tool name ask-library remains; no "asked"/"question" for DICTO's ideas; no "new"; Júlia Pimentel credited as "the gnomon method as described to DICTO" (no published source recorded — flagged for DICTO).

## Version 2 (2026-10-25): Part A rebuilt on studies/2026-10-25-gnomon-shapes (**S** = gnomon-shapes.txt / README; re-run on dicto-big-brother, output IDENTICAL, 63 PASS)

| # | Number / claim in v2 | Where | Source | Result |
|---|---|---|---|---|
| 34 | only similar stations I ~ I·φ³, linear ratio φ³ = 2 + √5, volume φ⁹ | Thm A (i), abstract | S §5, PASS "only similar pair of stations" | PASS |
| 35 | corner counts: I, I·φ³ 12; Cleo star, RT, M 32; others distinct | proof Thm A | S §1 (12,32,20,30,102,90,60,80,92,32,32,12) | PASS |
| 36 | Thm A (iv) scope "within the turn from I"; (v) every whole turn from any station is a gnomon (step 12 → Cleo star·φ³ ~ Cleo star) | Thm A | S §5 step 12 line | PASS (scope narrowed vs coordinator wording: in the endless cycle the first step of the next turn also makes a whole similar to an earlier station) |
| 37 | Table 3 piece counts 20; 12 + 30; 12; 12; 60 + 20; 60; 20; 12; 60; 30; 60 | Table 3 | S §2, README table | PASS |
| 38 | Table 3 face/corner descriptions (15 corners 5 tri + 7 pent; 11 corners 1 pent + 5 quad + 5 tri; 8 corners 5 quad + 2 tri; 2 hexagons + 6 quads; 6 corners 1 rhombus + 6 tri; bipyramid 6 tri) | Table 3 | S §2 face counts | PASS |
| 39 | separate parts 20, 1, 1, 12, 1, 60, 20, 12, 12, 1, 1 | Table 3 | S §2 "region = … connected part(s)"; README (step 1: 20 parts, step 2: one gap per #35) | PASS |
| 40 | added volumes per step (= Table 2) | Table 3 | S §2 = C | PASS |
| 41 | single pieces: I/20; (1/80)φ⁻²I; (9/10)φ⁻⁴I; (1/60)φ⁷I | Table 3, §4 | S §2 | PASS |
| 42 | no piece kind similar across steps except spike = core Cleo-Ico (k = 1); no piece similar to a station; types: pyramids in 1, 2, 7, 8, 9, tetrahedra in 1, 2, 6 | §3 Shapes | S §3, §4, README | PASS |
| 43 | check total 63 + 4 + 9 + 1 + 15 + 26 = 118 | abstract, App. | outputs | PASS |
| 44 | sources [12] Mix Vale 2026-06-22, [13] Portal Tela 2026-05-12, journal not named | credit, refs | S README (as recorded; not opened here) | PASS (as recorded) |
| 45 | Heron's general definition quoted in Heath's commentary on II Def. 2 | §1, [7] | Heath vol. I not in the library; not read here — flagged | OPEN for DICTO |

Wording v2: "proposed", "theorised", "concluded" ("the nature of the beast" — DICTO concluded the volume reading missed the shape); no asked/question/wonder/doubt; unnamed pieces marked "(unnamed; DICTO decides)"; DICTO's names kept exactly (Cleo-Ico, Shields, inward pentagonal pyramids, valley tetrahedra). Number "#54" (no "proposed"). Figure 2 legend reworded to "added volume" (classical gnomon = shape).

## Version 3 (2026-10-25): DICTO's names Julias / Pimentels; title

| # | Change | Source | Result |
|---|---|---|---|
| 46 | Title "One Turn Is a Gnomon: the Golden Cycle Step by Step, and the Polar of the Keyed Pair" (no working-title mark; footer too) | coordinator, DICTO accepted | done |
| 47 | Table 3: G1 Cleo-Icos, G2 DICTO's fill of D′, G7 Shields keep names; Julia G3, G4, G5a, G5b, G6, G8, G9, G10; Pimentels G11 | DICTO 2026-10-25 via coordinator | done |
| 48 | nine previously unnamed kinds (G3, G4, G5a, G5b, G6, G8, G9, G10, G11), not seven: v2 conclusion said "seven kinds" — corrected | S README "Technical names" (9 rows), classify_pieces.txt (9 kinds outside G1, G2, G7) | PASS (fixed) |
| 49 | technical descriptions and nearest forms (dodecahedral cap; J9; triangular prism with edge cut; hexagonal frustum; truncation corner; J2; J1; hip roof; J12); edge lengths 2–7 | S README table; classify_pieces.txt edge-length counts (2, 3, 4, 7, 3, 3, 2, 5, 4, 6) | PASS (G7 Shield and G8 have 2; G5a has 7) |
| 50 | piece counts 12, 12, 60, 20, 60, 12, 60, 30, 60 | classify_pieces.txt | PASS |
| 51 | cone-section sentence (shape forced by the two nested solids; cones over all faces divide the shell exactly) | S README l.65; gnomon-shapes.txt "pieces sum to layer" PASS | PASS |
| 52 | Johnson 1966, Can. J. Math. 18, 169–200, doi:10.4153/CJM-1966-021-8 | Crossref 2026-10-25 | PASS |
| 53 | credit "the names Julias and Pimentels are DICTO's" | coordinator | done |
