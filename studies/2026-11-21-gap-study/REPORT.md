# Gap study: closing the gaps of the Concordance (21 November 2026)

For DICTO, not for publication. Nothing was published, deployed or put on Zenodo; concordance.json and the paper folders are untouched.

## 1. Where it stands

| | Closed already | Settled tonight | Closable now | Needs a new paper | Not a real gap |
|---|---|---|---|---|---|
| Grid (16 empty cells) | 10 | 2 | 0 | 1 | 3 |
| Ranked problems (15) | 8 | 0 | 6 | 1 | 0 |
| Loose points (44 open) | 4 | 0 | 23 | 16 | 1 |
| **Total** | **22** | **2** | **29** | **18** | **4** |

Waiting results (112): 55 already published (stale goes_to), 5 with a target that no longer fits (W19, W27, W35, W88, W95), 7 to check wording, 27 open, 18 done.
One real empty grid cell remains: rhombic triacontahedron × centre pyramids (do its pyramids tile space?).

## 2. Every gap with its verdict
===== TABLE grid
| # | Solid × theme | Verdict | Why, or where it is settled |
|---|---|---|---|
| G1 | Dodecahedron × CH | CLOSED ALREADY | #99 puts the dodecahedron inside every octahedron of the octet (five-chains O > I > D > C > T), and every close-packed stacking is made of regular octahedra and tetrahedra (#57, #92 v3). So it sits in every c/h stacking; one sentence to write, cell should read "99 + 57". |
| G2 | Icosahedron × CH | CLOSED ALREADY | Same: #99 (icosahedron in every octahedron) with #57 / #92 v3; #47's slab already uses icosahedra in octet octahedra (Admiral Caps). |
| G3 | Tetrahedron × TWIN | CLOSED ALREADY | The Golden Ladder v6, Theorem 1A (c) (study 2026-11-04-golden-twins): the twins of both golden cuts over-cut (sigma(x1) = phi^2, sigma(x2) = 1/2 + sqrt5/10, both > 1/2): no twin solid. Cell should read "GL Thm 1A: none". |
| G4 | Octahedron × TWIN | CLOSED ALREADY | Same theorem (triangle faces, k = 1): no twin solid. |
| G5 | Rhombic dodecahedron × TWIN | CLOSABLE NOW, SETTLED TONIGHT | Tonight (golden_twins_rhombic.py, FINAL ok): the RD's two golden cuts (#89 Theorem 3) ARE Galois twins of each other, like the cube's, under the extension of Double Vision that fixes sqrt2 and sends sqrt3, sqrt5 to their negatives (it sends K to -K). Under the Golden Ladder's convention (sqrt2 and sqrt5 negated, sqrt3 fixed) and every other embedding: no solid. |
| G6 | Rhombic dodecahedron × CH | CLOSED ALREADY | HexOct v12, "The Turned Twin" (study 2026-11-04-trd, read ok): on every Barlow stacking a c ball has an RD cell, an h ball a TRD cell; RD = 1/2 polar(CO), TRD = 1/2 polar(anticuboctahedron). Also #97/#98: Narcissus (a half RD) stacks any word. |
| G7 | Rhombic dodecahedron × DEHN | CLOSED ALREADY | Study 2026-11-04-rt-pyramids (ranked 9): RD centre-pyramid angles 60, 90, 120 degrees, all rational in pi: Dehn zero; the pyramids tile (#93 Theorem C). Recomputed tonight as a control. |
| G8 | Cuboctahedron × PYR | CLOSED ALREADY | #92 v2, Theorem 10 (ranked 1 already says so; the grid cell is stale). |
| G9 | Cuboctahedron × TWIN | NOT A REAL GAP | No golden cut exists on the CO (#89) and its corners are rational, so Double Vision fixes it: nothing to twin. |
| G10 | Cuboctahedron × CH | CLOSED ALREADY | #92 v3/v4: whole COs form at straight corners, anticuboctahedra at twisted ones, at most a quarter of the corners are centres; study 2026-11-04-cuboctahedron-pyramids: anticuboctahedra + octahedra fill hcp (integer program; also in #92's text). |
| G11 | Cuboctahedron × DEHN | CLOSED ALREADY | Its pyramids are the regular tetrahedron and the half-octahedron, #44's T + O set (#92 v2 Theorem 10). Confirmed exactly tonight: Dehn(T) = 6 sqrt2 (x) t, Dehn(S) = -6 sqrt2 (x) t, t = arccos(1/3); a set has Dehn zero exactly when it has as many tetrahedra as half-octahedra. |
| G12 | Rhombic triacontahedron × PYR | NEEDS A NEW PAPER | Do the RT centre pyramids tile space? Dehn zero (rational angles 72, 120 degrees); the 4 Nov search reached 31 pieces and its long-run logs were lost (run audit, 10 Nov). Open; a monotile-clue candidate (ledger: watch list). New direction 1. |
| G13 | Rhombic triacontahedron × CH | NOT A REAL GAP | Five-fold symmetry is not a site symmetry of any close-packed stacking; the RT has no cell or hole role there, and placing it inside octahedra would be decoration (Occam). |
| G14 | Rhombic triacontahedron × 4D | CLOSED ALREADY | Its lift is six-dimensional: The Golden Ladder v8, Chapter 7: the RT is the central section of the Voronoi cell of D6 (s2 checks). Tonight's float screen found NO RT among the shadows, central sections or corner layers of the 600-cell, 120-cell and their rectifications along corner, edge, 2-face and cell axes (rt_4d_screen.py; controls RD and CO pass). Cell should read "GL ch 7 (6D)". |
| G15 | Icosidodecahedron × CH | NOT A REAL GAP | As for the RT: no layer role; ID inside I inside O is decoration only. |
| G16 | Icosidodecahedron × DEHN | CLOSABLE NOW, SETTLED TONIGHT | Tonight (pyramid_dehn.py, FINAL ok): no combination of the ID's centre pyramids, with any integer multiplicities, has Dehn invariant zero, so (by #44 Lemma 1) no set of them fills space. |

===== TABLE q
| Solid × theme | Cell now | Reading |
|---|---|---|
| Cube × CH | 86 (?) | Rock-salt pieces on stackings (cubes in cubic stretches, study 2026-11-06-premise-challenge, ledger row 58) is the likely link; keep "?" until a paper states it. |
| Cuboctahedron × NEST | ? | Needs DICTO's word on what a nest means for the CO; nothing in the studies. |
| Cuboctahedron × 4D | 91 (?) | Classical and confirmed tonight (float control): the 24-cell's central section perpendicular to a corner is the CO. Drop the "?" and credit it as classical. |
| Rhombic triacontahedron × TWIN | 33 (?) | Tonight: no Galois conjugate of either RT golden cut is a real cut (all three non-trivial embeddings). If the cell means the cuts, it reads "none". |
| Rhombic triacontahedron × DEHN | 38 (?) | RT Dehn zero (studies 2026-11-19-dehn-atoms calibration, 2026-11-04-rt-pyramids); the centre-pyramid count is zero too. Cite those studies in place of "38 (?)". |
| Icosidodecahedron × TWIN | 33 (?) | Not computed tonight (the ID has only golden-regular cuts, #89). |

===== TABLE ranked
| # | Ranked problem | Verdict | Why, or where it is settled |
|---|---|---|---|
| R1 | The cuboctahedron's centre pyramids | CLOSED ALREADY | #92 v2 Theorem 10 (published). |
| R2 | The second dual sweeps, cuboctahedron–rhombic dodecahedron and icosidodecahedron–triacontahedron | CLOSED ALREADY | Study 2026-11-09-dual-sweeps (premise corrected). No waiting row names a home for it: propose #89/#91 next version. |
| R3 | The reversed neighbour (#92 open point 1, #93 open point 1) | CLOSED ALREADY | #92 v3 Theorem 12 and #93 v2 Theorem E, both published. |
| R4 | #91 Lemma 6 exact | CLOSABLE NOW | Exact Q(sqrt5) builds of the three #76 stations; one exact engine (Normaliz with e-antic, study 2026-11-21-new-tools item 1) serves it. Direction 5. |
| R5 | #43 Conjecture 2 (octahedral constant 3) | CLOSED ALREADY | #43 v2 Theorem 4 (published). |
| R6 | The Hexagonality Law for the Laves big atom (#66, #67) | CLOSED ALREADY | Study 2026-11-12-laves-three-layer-swap; home #66/#67 next versions (waiting row 81). |
| R7 | Star and Star Halo of the classical solids | CLOSABLE NOW | Regular part DONE (study 2026-11-09-regular-stars-census, 25 of 25 exact); the 13 Archimedean and 13 Catalan solids remain, census scripts exist. Home: Star Cores v3. |
| R8 | Galois twins of every golden cut | CLOSED ALREADY | The Golden Ladder v6 Theorem 1A; extended tonight to the RD (twins) and RT (none). |
| R9 | Dehn counts of the rhombic dodecahedron, cuboctahedron, triacontahedron and icosidodecahedron pyramids | NEEDS A NEW PAPER | All isohedral cases answered (cube, RD, RT Dehn zero); CO and ID settled tonight; what is left is the RT tiling question. Direction 1. |
| R10 | The TRD as the rhombic dodecahedron's h partner | CLOSED ALREADY | HexOct v12 "The Turned Twin" chapter; the TRD DICTOnode clock positions made exact on 21 Nov (Rhombiverse repository). |
| R11 | #53 Observation 1 (diagonal swap) | CLOSABLE NOW | Observations 1, 2, 4 proved (studies 2026-11-08-switch-theorem, 2026-11-09-cscl-zincblende); Observation 3 left: tabulate tau_A + tau_B against site symmetry on the twelve networks (small). |
| R12 | The golden split in the other AXE networks (#48) | CLOSABLE NOW | Method and uniqueness theorem of #48 exist; run the split at t = phi on the other AXE networks (medium). |
| R13 | Archimedean stretches (#49) | CLOSED ALREADY | Study 2026-11-12-permutohedron-equal-edges with PRIOR-ART.md; published in The Permutohedron Paradigm Ch 14 (17, 101, 4427). #49 v2 still to cite it. |
| R14 | The loose step O ⊂ rTI (#35) | CLOSABLE NOW | Test every #88/#91 golden-cut station S for O inside S inside rTI exactly (medium). |
| R15 | Joining the fill thread to the cuts and the sweep | CLOSABLE NOW | Largely joined since: Space-Fillers and Lattice Moves v1, #106 One World, #47 v3 Theorem 2. Left: #47 question 3 (a three-periodic C + T + O filling), a SAT search on tori. |

===== TABLE loose
| # | From | Open point | Verdict | Why, or where it is settled |
|---|---|---|---|---|
| L1 | #92, #93 | reversed neighbour of the T and C6 pyramids; undecided rows of #92 Table 2; tilings not face to face (#93: 7 edge and 3 face combinations); TRD centre… | CLOSABLE NOW | Three of four parts closed (#92 v3 Thm 12, Table 2; #93 v2 Thm E and the uncountable R12 tilings). Left: the 10 non-face-to-face combinations of #93 and the TRD pyramid control + prior art: one SAT batch. |
| L3 | #48 | golden split in the other AXE networks; printed keyed sets | CLOSABLE NOW | As ranked 12; printed keyed sets are a build task. |
| L4 | #35 | closing solid for the loose step O ⊂ rTI; the 9/φ⁴ coincidence; a physical build | CLOSABLE NOW | As ranked 14; the 9/phi^4 coincidence = #34's tightest cycle (cite); the build is not mathematics. |
| L5 | #36 | golden fill G′ of the bcc gap | NEEDS A NEW PAPER | Paused: needs DICTO's definition of the golden fill G' first (9 Nov triage question). |
| L6 | #36 | golden Bull-horns adaptor; rhombic division of the 72-piece gap; Cleo-Ico adapters; oblique layers at the seams | CLOSABLE NOW | The Bull-horns adaptor for the cut OG is in #95 (published); the rhombic division of the 72-piece gap and the Cleo-Ico adapters remain (hole_piece_cut.py). |
| L7 | #30 | spine = thinned cut-and-project chain; seams as model sets; off-plane core rings; other solids with five inscribed cubes | NEEDS A NEW PAPER | Spine as a thinned cut-and-project chain, seams as model sets: bridge aim. Direction 2. |
| L8 | #40 | space DBT and OTT leave on mixed stackings; OG on aperiodic stackings with diffraction | CLOSABLE NOW | Leftover volume per layer type follows the Window Law (#84); diffraction from the exact Fibonacci spectrum (ledger row 21). Direction 2. |
| L9 | #41 | third level of Hexas; physical puzzle | NEEDS A NEW PAPER | Queued: needs DICTO's definition of a third-level Hexa first. |
| L11 | #43 | Conjectures 1 and 2; shell 5 exact; the full flip | NEEDS A NEW PAPER | Conjecture 1 beyond k = 40 needs the New-Face (inradius) lemma, a new idea; shell 5 exact and the full flip are small exact builds. |
| L12 | #43 | shell ratios against Tsai clusters and virus capsids | CLOSABLE NOW | Desk comparison with published Tsai-cluster and capsid radii (small); Occam: only if one line links it to #43's theorem. |
| L13 | #45 | Conjecture 1 (largest width) | CLOSABLE NOW | Width w(u) = h(u) + h(-u) piecewise on the fundamental triangle, critical points exactly (medium). |
| L14 | #47 | smallest kit; face to face; periodic in three directions (C + T + O without connectors ANSWERED 6 Nov: yes, never face to face) | NEEDS A NEW PAPER | C + T + O without connectors answered (#47 v3); smallest kit: five connectors in the hybrid slab, no lower bound proof; three-periodicity open. |
| L15 | #49 | Archimedean stretches and caps; prior art for the five-fold stretch | CLOSED ALREADY | Listed and prior art checked (study 2026-11-12-permutohedron-equal-edges; Paradigm Ch 14). Write into #49 v2. |
| L16 | #50 | catalogue of perfect points; which dissection fillers (Hill, Sommerville, Goldberg) the moves reach | CLOSABLE NOW | Perfect points as walls of the move sliders; match Hill, Sommerville, Goldberg lists (medium). |
| L17 | #51 | one solid per bond that fills alone; printed Samson and Delilah | CLOSABLE NOW | Delian bond answered: O(t) is never Dehn-zero except at the RD (study 2026-11-04-dehn-screen). Screen the pieces of the other bonds with dehn_mp.py (small). |
| L18 | #52 | scale anomaly; web of the keyed bond | NEEDS A NEW PAPER | Needs DICTO's choice (keys as a second colour of bond, or their own network). |
| L19 | #53 | Observations 1–4; exact walks of three-kind networks; a common reason for the switch points | CLOSABLE NOW | Observations 1, 2, 4 proved; Observation 3 and three-kind walks remain (ranked 11). |
| L20 | #54 | a shorter run as a classical gnomon; capped cubes at other sizes | CLOSABLE NOW | Small exact checks (shorter run, capped cubes). |
| L21 | #55 | weight walks of σ, Z, C15 and other Frank–Kasper phases; 4D two-kind walks | CLOSABLE NOW | Feed sigma, Z, C15 site lists to the #57 census engine (medium). |
| L22 | #56, #57 | self-keyed Blockhead; three-kind walk; keyed Chucky and Fang | NEEDS A NEW PAPER | Keyed Blockhead, Chucky, Fang: keying is paused (DICTO 12 Nov); the three-kind walk goes with row 19. |
| L23 | #61 | Swap Rule for s < 1/4 | NEEDS A NEW PAPER | Proved on [1/8, 1/4] (#104 Thm 3). Below: study 2026-11-09-b1-walls found a constant shift delta_tet = -(1 - 4s)^3/(54 s) in a middle zone and clashes below. Direction 3. |
| L26 | #76 | exact atlas in Q(√5); proof of part (3) | CLOSABLE NOW | Exact atlas in Q(sqrt5) (Normaliz/e-antic or own Q(sqrt5) hull). Direction 5. |
| L27 | #78 | why the prime 89; matching the dodecahedra to the Red Queen's nine layers | NEEDS A NEW PAPER | "Why 89" answered (#80); the nine-layer match needs DICTO's meaning of "layer". |
| L28 | #80 | proof that Archimedean chains close in four steps; omnitruncates; the quasi-regular formula | CLOSABLE NOW | Platonic chains mapped (b1-walls): period 4 on most depths, exact on two hops, but a NON-closing window exists, so "close in four steps" is false in general; Archimedean and omnitruncate chains remain. |
| L29 | #80, #81 | exact edges of the open windows (cube s 49/80–59/80; dodecahedron 87/80–99/80) | CLOSABLE NOW | Regimes located numerically (cube non-closing 0.62-0.74, dodecahedron 1.10-1.24, matching the open windows); exact symbolic stepping failed at step 6, so exact edges need root isolation (FLINT qqbar, new-tools item 7). |
| L30 | #86 | proof over whole stretches (exact at 402 weights) | CLOSED ALREADY | Study 2026-11-09-b1-walls: #86 tower walls DONE, exact at every wall and one point of every hop. Home #86 next version. |
| L31 | #87 | other centres for solids of low symmetry | NEEDS A NEW PAPER | Needs DICTO's choice of centre for low-symmetry solids. |
| L32 | #87 | cardboard sheets for the other solids | NOT A REAL GAP | Cardboard sheets are a build task, not an open point of the mathematics. |
| L33 | #91 | Lemma 6 in general; off-base prism sections; exact stations of the tilted slice; TRD outside the cubic sweep; the factor 2 between 342 and 171 — resta… | CLOSABLE NOW | Lemma 6, tilted slice, factor 2: exact Q(sqrt5) stations. Direction 5. |
| L34 | #89, #91 | sections of the ten Schläfli–Hess star polytopes | CLOSABLE NOW | The 10 Schlafli-Hess polytopes now have exact flags (regular-stars-census); #89's "no section" search was float only: redo exactly. Direction 5. |
| L35 | #90 | structure over Q(√2, √5) beyond natural projections | NEEDS A NEW PAPER | Needs DICTO's choice of picture (9 Nov triage question). |
| L36 | #8 | database search for the 1b + 12j point set | CLOSABLE NOW | Desk search of free prototype databases for the 1b + 12j point set (small). |
| L37 | #62 | six all-triangle 600-cell slices (28, 30, 32, 42, 48, 72 vertices); equilateral forms of five patterns | CLOSABLE NOW | Exact heights of the six all-triangle 600-cell slices (incidence events). Direction 5. |
| L38 | #104 | Theorem 3 below λ = −9s/8 and for s < 1/8; stackings without the four-layer condition | NEEDS A NEW PAPER | Same as row 23. Direction 3. |
| L39 | #105 | the golden slice of the permutohedron honeycomb counted exactly (Lead 1); the heart for an even number of values (Lead 2); a physical build of the hea… | CLOSABLE NOW | Lead 2 (the heart for an even number of values), medium. |
| L40 | #108 | the second Vacuus and the residents (Observations 4, 5) stated as observations, not proved | CLOSABLE NOW | Observation 5 made exact (study 2026-11-13-platonic-residents-exact); Observation 4 (the second Vacuus) remains, medium. |
| L41 | #104, #108 | are the balance laws (#104 Theorem 4, #108 Theorem 1) classical (Stanley's balanced complexes)? | CLOSED ALREADY | Study 2026-11-15-stanley-check: in substance yes (Bayer-Billera 1985); to be said at #104 and #108 next versions. |
| L42 | #105 | whether turned or mirrored copies of the DICTO 1:2 Truncated Octahedron fill space (§5) | CLOSED ALREADY | Dehn invariant -12 sqrt2 (x) beta, nonzero (#100 Thm 1.1 with Debrunner; also in #113). Into #105 next version. |
| L43 | #111 | which axis lines put the regular polygon in the lengths (four do); the fields of the radii of T ∩ D and of the 42- and 50-face dice; lines with faces … | CLOSABLE NOW | The fields of the radii are exact algebra (small); the physical fair point of a print is not mathematics. |
| L44 | #112 | a structural reason for the diameter certificate; witnesses of N − 1 directions; closed forms; the Vacuus of the 149 Aequi (only D191 checked); both p… | CLOSABLE NOW | The Vacuus of the 149 Aequi and both placements under subgroups of Oh are computations (medium); Aequi as Wulff shapes would be new work. |
| L45 | #113 | the ten other fair dice in Lean; does the fair 18-face die fill space (Debrunner in Lean); Sydler's converse in Lean; convex hulls; an exact t for Luc… | NEEDS A NEW PAPER | Lean developments (ten dice, Debrunner, Sydler's converse): each a formal project. |
| L46 | #114 | swaps per birth against ⟨F⟩/2 − 3 in a public three-dimensional grain map swept by planes (§7); the Sun, Earth's plates, clouds and froth not confirme… | NEEDS A NEW PAPER | Open lead on real data; the scutoid streams were shelved 16 Nov. |
| L47 | study 2026-11-20-palomar-next-prescore | Sydler's converse (in Lean, and the 4D analogue of Jessen); E1 as a general theorem (formal Wallace–Bolyai–Gerwien, box to cube, then every zonotope o… | NEEDS A NEW PAPER | E2 is published as #116 (20 Nov); E1 fell below Palomar's floor; Sydler's converse in Lean is a large formal project. |
| L48 | study 2026-11-20-600cell-5cell-zero | how the cap solid and the √2 tip 600-cell relate to the earlier 600-cell work (Part 2); whether the edge partition by 120 facets is known; a 4D union … | NEEDS A NEW PAPER | Part 2 being checked; a 4D union that fills space and an actual dissection to the 4-cube are new work. Direction 4. |


## 3. Settled tonight (exact sympy on the compute host; scripts in scripts/, logs in data/)
1. **Icosidodecahedron × Dehn:** no integer combination of its triangle and pentagon centre pyramids has Dehn invariant zero, so no set of them fills space (#44 Lemma 1). The φ-part forces 3n3 = 5n5; the 1-part is then m·δ with δ/π irrational. Controls: cube and RD pyramids zero, tetrahedron not.
2. **Rhombic dodecahedron × Galois twin (new):** its two golden cuts (#89 Thm 3) are exact twins under the map fixing √2 and negating √3, √5 (K ↦ −K). Under the Golden Ladder's convention (√2, √5 negated) there is no twin. DICTO to choose the convention.
3. **Rhombic triacontahedron × twin:** none of the conjugates of either golden cut is a real cut (24 exact sign certificates).
4. **Cuboctahedron × Dehn** (confirmed): Dehn(T) = 6√2⊗t, Dehn(S) = −6√2⊗t; zero iff n3 = n4 (#44's T + O set).
5. **Rhombic triacontahedron × 4D** (float screen only): no RT among the shadows, sections or layers of the 600-cell, 120-cell or their rectifications; its lift is 6D (Golden Ladder v8, Ch 7). By-product to confirm: the 120-cell's cell-first shadow may be a truncated RT.

## 4. Proposed homes for waiting results
- A Brief Geometry of Space: W63, 64, 66, 75, 77, 78, 79, 89, 91, 98, 101.
- The Golden Cycle v5: W19, W35, W97. Golden Ladder v9: tonight's twins, W89.
- Space-Fillers v2: W39, W92 (check W37, W58). HexOct next: W9, 36, 75 (check W32).
- Centre Pyramids / #44 next: tonight's ID and CO results, W11.
- Next versions: #38 W99 · #49 W62 · #66/#67 W81 · #100 W90 · #104 W85, W93 · #105 W69, W94 · #108 W72, 85, 86.
- Paradigm v2: W87. Platonic v2: check W72–74; W80.
- W111, W112 still say "awaits DICTO", but #103 v8 is published with Proposition 17.

## 5. New directions (every title DICTO's to choose)
1. **Dehn count of the 31 classical solids:** the zero-Dehn lattice of each solid's pyramids, then which tile. Closes the DEHN and PYR cells, ranked 9, W27, W39. Prior art: Chentouf–Sun arXiv:2312.01654; Kedlaya–Kolpakov–Poonen–Rubinstein arXiv:2011.14232.
2. **The Fibonacci stack as a cut-and-project crystal (aim 1):** the A/B/C positions as a Z/3 cocycle over the golden rotation. Closes loose 7, 8, W21, W57.
3. **The Swap Rule below a quarter (aim 2):** constant shift δ_tet = −(1−4s)³/(54s) for 1/5 ≤ s < 1/4. Closes loose 23, 38.
4. **Regular polytopes filling 4-space together:** Dehn–Hadwiger-zero unions from #116, then which tile. Closes loose 47, 48; joins the Queens to the fill thread.
5. **The golden stations of the Queens, exactly:** one exact Q(√5) engine (Normaliz with e-antic). Closes ranked 4 and loose 26, 33, 34, 37.

## 6. LEADS
1. Homes for tonight's results (Centre Pyramids / #44; Golden Ladder Ch 7).
2. DICTO's call: the Double Vision convention over Q(√2, √3, √5).
3. Rewrite the grid cells as in table 2 at the next Concordance version.
4. Update stale waiting rows; mark W111, W112 published.
5. RT pyramid tiling: rerun the search with watched logs.
6. Confirm the 120-cell cell-first shadow exactly.
7. Closable-now queue: bonds Dehn screen, #53 Observation 3, the SAT batch, the star census, O ⊂ S ⊂ rTI, the AXE split.
===== WAITING by flag
STALE (55): W1, W2, W3, W4, W5, W6, W7, W8, W12, W13, W14, W15, W16, W17, W18, W20, W21, W22, W23, W24, W25, W26, W28, W29, W30, W31, W33, W34, W38, W41, W42, W43, W47, W54, W55, W56, W57, W61, W62, W65, W67, W68, W69, W70, W71, W76, W83, W84, W94, W98, W100, W102, W108, W111, W112
STALE-T (5): W19, W27, W35, W88, W95
CHECK (7): W32, W37, W58, W72, W73, W74, W99
OPEN (27): W9, W11, W36, W39, W40, W59, W63, W64, W66, W75, W77, W78, W79, W80, W81, W82, W85, W86, W87, W89, W90, W91, W92, W93, W97, W101, W110
DONE (18): W10, W44, W45, W46, W48, W49, W50, W51, W52, W53, W60, W96, W103, W104, W105, W106, W107, W109

counts: grid CLOSED ALREADY 10, CLOSABLE NOW, SETTLED TONIGHT 2, CLOSABLE NOW 0, NEEDS A NEW PAPER 1, NOT A REAL GAP 3 | ranked CLOSED ALREADY 8, CLOSABLE NOW, SETTLED TONIGHT 0, CLOSABLE NOW 6, NEEDS A NEW PAPER 1, NOT A REAL GAP 0 | loose CLOSED ALREADY 4, CLOSABLE NOW, SETTLED TONIGHT 0, CLOSABLE NOW 23, NEEDS A NEW PAPER 16, NOT A REAL GAP 1 | total CLOSED ALREADY 22, CLOSABLE NOW, SETTLED TONIGHT 2, CLOSABLE NOW 29, NEEDS A NEW PAPER 18, NOT A REAL GAP 4
grid {'CA': 10, 'SET': 2, 'NR': 3, 'NP': 1}
ranked {'CA': 8, 'CN': 6, 'NP': 1}
loose {'CN': 23, 'NP': 16, 'CA': 4, 'NR': 1}
total {'CA': 22, 'SET': 2, 'NR': 4, 'NP': 18, 'CN': 29}
waiting {'STALE': 55, 'OPEN': 27, 'DONE': 18, 'STALE-T': 5, 'CHECK': 7}
FINAL ok
