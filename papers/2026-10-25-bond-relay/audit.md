# Number audit — "The Web of Bonds" draft (#52 proposed), 2026-10-25

Every number in paper.src.html (text, tables, captions, appendices) checked against the two studies.
Sources: **B** = studies/2026-10-25-bond-relay/README.md, **P** = studies/2026-10-25-physical-anchors/README.md (line numbers at commit 7b0fd8b);
check files as named. Decimals were also recomputed from the closed forms (python, double precision) — "recomp".
CSS sizes, reference numbers, page/years/volumes in the reference list (checked against MANIFEST.json / P l.186–200 / #48 and #51 reference lists) are not repeated here.

| # | Number in the paper | Where in paper | Source | Result |
|---|---|---|---|---|
| 1 | w_B − w_S = (φ²/4)(x − 1)/(x + 1) = (L/2)²(2s − 1) | abstract, Main thm (i) | B l.58, l.114; symbolic-checks A6 weight | PASS |
| 2 | w_Q − w_O = (3/8)(2t − 1) | abstract, Main thm (i) | B l.59; symbolic-checks A6 delian weight | PASS |
| 3 | L = φ; s = x/(1 + x); (1, s, 0)·L/2; 1 − s for T(1/x) | §2 | B l.15 | PASS |
| 4 | a = 3(1 − t)/2; Q = (ℤ + ½)³/√2; O = odd points/√2; octet edge 1 | §2 | B l.16, l.59 | PASS |
| 5 | t = 0 Q cells points, t = 1 O cells points | Main thm (i) | B l.61, l.115; samples-checks "delian t=0 / t=1 B1" | PASS |
| 6 | big–small area (√3/8)φ²(x² + 4x + 1)/(1 + x)²; max (3√3/16)φ² ≈ 0.8502; ends (√3/8)φ² ≈ 0.5668 | Table 1, Cor. 2 | B l.67; recomp 0.850231, 0.566821 | PASS |
| 7 | big–big φ²x²/(2(1 + x)²), → φ²/2; small–small φ²/(2(1 + x)²), φ²/2 at x = 0 | Table 1 | B l.68–69; symbolic.json "golden areas" | PASS |
| 8 | square diagonals sL and (1 − s)L, sum φ | Main thm (iii), proof | B l.68–69, l.116 | PASS |
| 9 | ratio x², equal only at x = 1 | Main thm (iii) | B l.82, l.116 | PASS |
| 10 | oct–tet (9√3/4)t² (t ≤ 1/3), (9√3/16)(1 − t)² (t ≥ 1/3); √3/4 at 1/3; slopes 3√3/2 and −3√3/4 | Table 1, Cor. 2, Fig. 1 | B l.70 | PASS |
| 11 | oct–oct (√2/4)(1 − 9t²), √2/4 at 0, dies at 1/3 | Table 1 | B l.71 | PASS |
| 12 | tet–tet (3t − 1)(5 − 3t)/8 = (1 − a²)/2, born 1/3, → 1/2 | Table 1 | B l.72 | PASS |
| 13 | Kelvin big–big = small–small = φ²/8 ≈ 0.32725 | Table 1 caption, Fig. 1 | B l.75; recomp 0.327254 | PASS |
| 14 | x = τ: big–big 1/2, small–small 1/(2φ²) ≈ 0.19098, big–small (√3 + 3√15)/16 ≈ 0.8344 | Table 1 caption, Fig. 1 | B l.76; recomp 0.5, 0.190983, 0.834438 | PASS |
| 15 | Delian bond oct–tet 2^(1/3)√3/8 ≈ 0.2728, tet–tet 1/2 − 2^(1/3)/4 ≈ 0.1850 | Table 1 caption | B l.77; recomp 0.272781, 0.185020 | PASS |
| 16 | w_Q − w_O at Delian bond = 3/8 − 2^(2/3)/4 ≈ −0.02185 | Cor. 5 | B l.128 gives ≈ −0.0218 (truncated); recomp −0.0218503 | PASS (paper gives one more digit: −0.0218 truncated would round to −0.0219, so −0.02185 is used; same value) |
| 17 | oct–tet / tet–tet = 2^(1/3)√3 / (4 − 2·2^(1/3)); unweighted Voronoi t = 1/2 | Cor. 5 | B l.128 | PASS |
| 18 | Coordination tables (8; 14 = 8 + 6; 12; 20 = 12 + 8; 8; 4; 10 = 4 + 6; 6; none) | Cor. 1, Fig. 2 | B l.86–94; samples B3 / app-checks C4 | PASS |
| 19 | 6 squares always own kind | Cor. 1 | B l.96 | PASS |
| 20 | Dual cells: disphenoids 2 big + 2 small, vol 2/3, no flip; bipyramids 2 + 4, vol 8/3; octahedra 6 O 4/3 + tetrahedra 3 O + 1 Q 1/12; RD 6 O + 8 Q vol 2; cubes 8 Q vol 1 + square pyramids 1 O + 4 Q vol 1/6 | Cor. 3 table | B l.100–105; samples-checks B8 lines | PASS |
| 21 | single flip at 1/3; dual = octet at t = 0, cubes at t = 1 | Cor. 3, Fig. 3 | B l.105–107 | PASS |
| 22 | RD long diagonal length 1 (oct–oct = octet edge), short 1/√2 (tet–tet) | Fig. 3 legend/caption | P l.101 (M–M = 1, X–X = 1/√2); B l.59 sites | PASS |
| 23 | Secondary fan: golden in one chamber, Delian crosses one wall at 1/3 | Cor. 4 | B l.127 | PASS |
| 24 | #51 cube Remark w = (x − 1)/(4(x + 1)) at cube edge 1 | Remark | B l.61 | PASS |
| 25 | golden volumes (4/3)(1 + u)³ − 4u³, u = s or 1 − s, sum L³ | Remark | B l.78; samples-checks B4 | PASS |
| 26 | golden x = 0: two types; x = ∞: two types | Main thm (iii) | B l.117 | PASS |
| 27 | app areas match to 10⁻⁹ | proof (ii) | B l.41 (C2 max error < 1e-9) | PASS |
| 28 | Samples: x = 0, 1/3, 1/2, 1, 2, 3, τ, 1/τ, √2, ∞ (10); t = 0, 1/6, 1/4, 1/3, 1/2, 2/3, 1 + 4 stops (11): (2√6 − 3)/15, 1 − ∛6/3, 1 − (2/3)·2^(−1/3), 5/3 − (2/3)√2 | App. B, [S1] | B l.30 | PASS |
| 29 | Stop positions on Fig. 1 axis: eq. RD ≈ 0.1266, Delian ≈ 0.4709 (not printed in text) | Fig. 1 | #51 App. B; recomp 0.126599, 0.470866 | PASS |
| 30 | Check counts 55, 211, 105 (=371); 32, 29 (=61); total 432; 0 FAIL | abstract, App. B, [S1], [S2] | B l.168–171; P l.213–215 | PASS (432 = 371 + 61) |
| 31 | 17 compounds, 9 loop stops, Kelvin/RD sanity | App. B | P l.214 | PASS |
| 32 | Weight = r² + C; bisector plane formula | Thm 2(a), proof | P l.27–35 (A1a–c) | PASS |
| 33 | CsCl B2, 1a/1b, a = φ; fluorite C1, 4a/8c, a = √2, shift (1,0,0)/√2 | Thm 2(b) | P l.94, l.99–100 | PASS |
| 34 | ρ = (x + 2)/(2x + 1) = (2 − s)/(1 + s); ρ = t/(1 − t); t = r_tet/d | Thm 2(c) | P l.55–56, l.60 | PASS |
| 35 | d = (√3/2)φ; d² = 3/8; r_big/d = (1 + s)/3, r_small/d = (2 − s)/3 | proof Thm 2 | P l.55–56, l.59; symbolic-checks A2d, A4a | PASS |
| 36 | Δ/d² = (2s − 1)/3 (golden), 2t − 1 (Delian) | proof Thm 2 | derived from #1, #2, #35; recomp identity | PASS |
| 37 | windows x ∈ [(√3 − 1)/2, √3 + 1], ρ ∈ [√3 − 1, (√3 + 1)/2]; t ∈ [1 − √(2/3), 1/√3], ρ ∈ [√(3/2) − 1, (√3 + 1)/2] | Thm 2(d) | P l.68; symbolic.json maps | PASS |
| 38 | Pauling √3 − 1 ≈ 0.732 (CN 8), √(3/2) − 1 ≈ 0.225 (CN 4) | abstract, Thm 2(d), §5 | P l.69; recomp 0.732051, 0.224745 | PASS |
| 39 | contact ends: oct balls 2r_O = 1, tet balls 2r_Q = 1/√2, big balls 2r_big = φ | proof Thm 2(d) | P l.68–69, symbolic-checks A2e, A4c, A4d | PASS |
| 40 | every x packs; only t ∈ [1/6, 2/3]; |Δ| ≤ φ²/4; −Δ ≤ (1/2)², Δ ≤ (1/(2√2))² | Thm 2(e), proof | P l.70–73; symbolic-checks A3g, A4f | PASS |
| 41 | Stops: x = 0 → ρ = 2; x = ∞ → 1/2; Kelvin → 1; τ → √5/φ² = (3√5 − 5)/2 ≈ 0.8541; octet → 1/2; Delian bond → (3/2)·2^(1/3) − 1 ≈ 0.8899; t = 1/2 → 1; t = 0, 1 no packing; t = 1/6, 2/3 end packings | Cor. 6 | P l.77–90; symbolic.json stops; recomp 0.854102, 0.889882 | PASS |
| 42 | oct–tet area (3√3/2)r_oct² (t ≥ 1/3), 6√3 r_tet² (t ≤ 1/3); BaF₂, Na₂O, K₂O r_oct = 1.42 Å share 5.239 Å² | Cor. 7 | P l.143; compounds.json areas_A2 5.23876 | PASS |
| 43 | Table 2 (5 CsCl-type rows: radii, ρ, x exact and decimal, three areas) | §5 | P l.120–124; scripted row-by-row compare | PASS (all 5 rows identical) |
| 44 | Table 3 (12 fluorite rows: radii, ρ, t, side, oct–tet, like bond, window) | §5 | P l.130–141; scripted row-by-row compare | PASS (all 12 rows identical) |
| 45 | Halides at x ≈ 1.1–2.1, τ ≈ 1.618 among them (between CsBr/TlCl and TlBr/CsI) | §5, Fig. 4 | P l.161 | PASS |
| 46 | 14 faces = 8 at (√3/2)a + 6 at a | §5 | P l.95, l.162 | PASS |
| 47 | cubic ZrO₂ r⁺/r⁻ = 0.61 | §5 | P l.163; recomp 0.6087 | PASS |
| 48 | UO₂ 0.725, CeO₂ 0.703 | §6 | P l.166; recomp 0.7246, 0.7029 | PASS |
| 49 | CR = IR ± 0.14; UO₂, CeO₂, ZrO₂ → t = 0.521, 0.528, 0.559 | §6 | P l.145, l.147; compounds.json CR_sensitivity | PASS |
| 50 | BaF₂ 1.08 > 1 | §6 | P l.167; recomp 1.0840 | PASS |
| 51 | Na₂O 0.697, K₂O 0.965, limit 0.414 | §6 | P l.168; recomp 0.6972, 0.9648 | PASS |
| 52 | Li₂O t = 0.2935 → 0.363 under CR | §6 | P l.139, l.148; compounds.json | PASS |
| 53 | CsCl x = 1.126 → 1.432 under CR; other halides toward x = 1 | §6 | P l.146; compounds.json (1.4315, 1.1023, 1.3176, 1.1118, 1.1646) | PASS |
| 54 | 12 cation neighbours at a/√2, no cation–cation face | §6 | P l.169 | PASS |
| 55 | Left out: NH₄Cl, CuZn/NiAl/FeAl/CoAl, Rb₂O (CN IV) | §6 | P l.152–154 | PASS |
| 56 | Shannon CN VI proxy for Cl⁻, Br⁻, I⁻ | Table 2 note | P l.112 | PASS |
| 57 | nine ask-library queries (5 + 4) | App. A | B l.145 (five); P l.180 (four) | PASS |
| 58 | Study commit 7b0fd8b | meta, [S1], [S2] | `git log -- studies/2026-10-25-*` | PASS |
| 59 | DOIs [1] 10.5281/zenodo.23596362, [2] 10.5281/zenodo.23606828 (concept records) | refs | papers/2026-10-23-golden-split/zenodo-state.json, 2026-10-24-delian-bond/zenodo-state.json (conceptrecid) | PASS |
| 60 | DOIs [3–5, 7–9, 12–19, 21, 22] | refs | P l.186–200 (Crossref-checked), MANIFEST.json entries (Crossref-verified 2026-10-23/25) | PASS |

**Result: 60 / 60 PASS.** One note: the bond study's README rounds w_Q − w_O at the Delian bond to "≈ −0.0218" (truncation of −0.021850…); the paper prints −0.02185, which agrees with both the exact value 3/8 − 2^(2/3)/4 and the README's digits.
Not audited here (outside the studies): the figure-5 app screenshot's own on-screen volumes (2.491, 1.745 — #48's 1 + 2√5/3 and 1 + √5/3, consistent).
