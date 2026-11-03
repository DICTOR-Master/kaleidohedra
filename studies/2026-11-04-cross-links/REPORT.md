# Cross-links audit, 4 November 2026

DICTO's idea: "search any similar correlations between earlier and later papers and make sure nothing is missed; all the strings are drawing together into one purse of gold". Model: the #90 fix (C ∩ μC* = the CsCl weight walk of #48/#53).
Method: crosslinks.py (word overlap, 75 papers + #92 draft), top 25 candidates judged, then a conceptual sweep of families, constants and names. Checks: checks.py, octconj.py (floating point 1e-15) plus short proofs. "Does not cite" = no #N, DOI or title of N in the later paper.

## A. Verified links (most important first)

| # | Pair | What is shared | Status | Fix and where |
|---|---|---|---|---|
| 1 | #77 → #92 (+ #40, #57; #51/#86) | #77's main theorem: in every face-to-face tiling by face pyramids, the pyramids round each apex make up their whole solid, so a T/O tiling is a tiling by whole tetrahedra and octahedra, 2 of each round every edge = #92 step (a) and Lemma 3. #77 left open which tet–oct tilings exist beyond the octet and its stackings; #92 answers it. #92's straight/twisted layers = c/h words of #40, #57/#58. #92's cube of edge 1/√2 = 4T+4O = #51's cube end (t=1) = #86 member A cubes (λ=3/8). | verified (statements compared; volumes √2/4 = 4·√2/48 + 4·√2/24) | #92 draft: credit #77 for the reduction; say #92 settles #77's open question; cite #40/#57; name the cube as #51's Delian cube end / #86's λ=3/8 cubes. |
| 2 | #43 → #80, #78, #79, #81 (+ #90, #91) | #43 Thm 1 S ⊂ (R/r)²·P(S); Thm 2 sharp icosahedral constant 15−6√5; Conj 2 octahedral constant 3. #80's gains (R/r)² = 9, 3, 15−6√5 are these numbers. #43 Lemma 3 polar(P(S)) = T(polar S) = #80's "T is polar reciprocation". #43's "OG turned out" = star chain of #78/#79: Star Halo = s·P(S); #43 Thm 2 keeps the TI star at s=φ inside its halo. | verified (definitions; tan²(π/p)tan²(π/q)) | #80 next version: cite #43 (Lemma 3, constants). #78/#79 next: Star Halo = s·P(S), #43 Thm 2. #91 draft: Table 3 closure (R/r)² is #43's/#80's constant. |
| 3 | #76 → #91 | #91's 600×120 sweep (R=1): the three uniform μ of Table 2 are #76's edge-equalising cuts: truncated 600-cell x=1/3 → μ=(9+√5)/12; bitruncated l=3/5 → (11+3√5)/20; truncated 120-cell t=(5−√5)/10 → (15+8√5)/38. #91's All-Golden bitruncated stage is the golden deformation of #76's midpoint. | verified (1e-16; exact forms match) | #91 draft: cite #76; its exact constructions can make Lemma 6 exact at those stations. |
| 4 | #53 → #91 (+ #52) | #91 §8: 24-cell honeycomb sliced vertex-first = #53's rock-salt lane, λ = (1−h)² − h² = 1−2h; chamfered-cube stop λ = 4−2√3 at h = √3−3/2. Lemma (Aurenhammer, cited in #53): a slice of a Voronoi honeycomb is the power diagram of projected sites with weights −height². Cell-first slice = CsCl lane, λ = 1−2h. | verified (proof + numerics) | #91 draft §8: add the lane identification and the lemma; cite #52/#53 with #48. |
| 5 | #81 → #91, #90 | #81's core turn on S(μ) = P ∩ μP* is the involution ν ↦ (R/r)²/ν (ν = μ/r²); on C·O: μ ↦ 3/μ (fixed √3), vs the CsCl partner μ ↦ 3−μ (fixed 3/2, Kelvin). | verified (algebra from #81's theorem) | #91 draft §2/§7: one paragraph. #90 draft: note the two involutions. |
| 6 | #54 → #90, #91 | #54 Thm B: polar of Icosaxes = cube + 6 pyramids of height 1/φ (Unborn: 1/φ²); along #48 heights x/(1+x), 1/(1+x), sum 1 = RD. polar(S(μ)) = H(μ)/μ, H(μ) = conv(C ∪ μO), height μ−1; RD = H(2). | verified (algebra) | #90, #91 drafts: cite #54 Thm B as the polar side of the C·O sweep. |
| 7 | #34 → #91 (+ #35, #33) | Same tight-cycle criterion. #34: none of 8,742 tight cycles closes on a power of φ (tightest 9/φ⁴). #91: 119 D·I Golden Tight Cycles at φ, all via golden-cut stations. | verified (definitions) | #91 draft §7: cite #34; the golden-cut stations open the φ-closure #34 found shut. |
| 8 | #53 → #89 | DICTO's cut-cube + octahedra filling (#89 §7) = #53's CsCl lane on (1,3); cube edge 2 cut at fraction x: λ = 3−4x; Golden Cut Cubes at λ ≈ 1.6082, 2.0672. | verified | #89 next version: one line. (#90 has it.) |
| 9 | #51, #53 → #86 | #86 member A (λ=3/8) cubes of edge 1/√2 = #51's cube end; member B (λ=−1/8) = the octet switch. | verified (#53 Table 1) | #86 next version. |
| 10 | #69 → #91 (+ #30) | #91 §8's golden-tilt Fibonacci word = #69's c→ch, h→c (share 1/φ²). | verified | #91 draft: cite #69, #30. |
| 11 | #67 → #73 | #73 §5 ice I_sd 37.7 Φ J/mol uses #67 Thm 1 (random stackings; Malkin, Amaya). | verified | #73 next version: cite #67. |
| 12 | #8 → #38a | I(1) ⊂ GSD ⊂ D(φ) = the EKP cell nesting (#8). #12 Star Chain Reaction: suggestive. | verified for #8 | #38a next version. |
| 13 | #85 → #87 | #85's δ = α + α′ angles are the angles of #87's Vacuus fins. | verified (definition) | #87 next version. |

## B. Suggestive
- #48 ↔ #55: one pyritohedral family (0, ±1, ±t): icosahedron t=φ, Unborn t=φ², Goliath t=2. Remark for #55 next version.
- #89/#91 ↔ #51/#53/#57: tesseract honeycomb vertex-first slice meets #53's fluorite lane only at the octet (λ = −1/8).
- #43 Conjecture 2: numerically inradius/circumradius ≥ 1/√3 for octahedral orbit hulls (200,000 points) ⇒ S ⊂ 3·P(S). Could become a theorem in #43/#80 next version.
- #33/#34 ↔ #80 (factor 3): probably coincidence.

## C. Noise (do not re-check)
star-cores-* ↔ star-cores-results (study note); #91 ↔ #90 (already cited); census piece names (Samson, Delilah, Lahdeli, Sonsam, Chucky, Blockhead, Ian Dury, Alice names, Kagemusha, Triskelion; #37a ↔ #79; #80 ↔ #35); already cited (#42↔#17, #42↔#18, #36↔#24); shared references only (#38a↔#36, #86, #47↔#75; #86↔#36); shared classical values (#55/#53/#56 ↔ #84/#64; Kelvin/3/2/φ⁶ ↔ #91; 7−√5 vs 3−√5 #42/#89; 5/2 in #89/#80/#91/#65; small fractions #41/#53/#60; #50↔#48/#52; #37a↔#50/#48; #54↔tih; thirteens catalogue #25/#26/#24/#36; #76↔#66 names; stellated dodecahedra #8/#42/#38a↔#89; #87↔#88/#89).
- NAME CLASH #38a ↔ #89: "golden tetrahedra" = Danzer / Mosseri–Sadoc tiles in #38a, Golden Cut Tetrahedra (GCT) in #89. Use "GCT" / "golden-cut tetrahedra" in #89 next version and #91/#92.

## D. The purse in one sentence
The C·O sweep of #90/#91 holds most of these links: its ends and polar are the CsCl lane (#48, #52, #53, DICTO's cut-cube filling of #89) and #54's polar heights; its reversal is #81's core turn; its closure (R/r)² is #43's sharp constant and #80's gain; the 24-cell honeycomb slices it into #53's CsCl and rock-salt lanes; its 4D form is #76's queen path with golden stops.
