# Formal triage of DICTO's papers, 22 Nov 2026

Status: study, read-and-sort only; no Lean run, no computation. Sources: concordance.json (papers, strands, names, gaps), each paper's abstract and theorem statements, the Palomar entries (#103, #113, #115, #116) and the Lean packets project (#117). Rows group papers of the same kind; a result is classed by its hardest main claim. Classes judged from statements, not from proofs; effort S/M/L only for B and C.

Classes: A already formal; B within reach of the existing Lean base; C certifiable by finite exact computation checked in Lean; D needs new foundations; E better informal.

## Counts (papers, by class of the paper's main result)

| class | papers |
|---|---|
| A already formal | 5 |
| B within reach of the existing Lean base | 26 |
| C certifiable by finite exact computation checked in Lean | 46 |
| D needs new foundations | 18 |
| E better informal | 19 |

Papers numbered in the table: 114; the rest (books, chapters, the numbering gaps #2-4, #6-7, #9, #21, #46, #82, #118+) carry no separate main theorem.

Honest note on class B: the existing base (Dehn invariant from sets, Niven independence, Q(√5) algebra, local angle conditions) covers the Dehn and golden-field papers. The stacking-law papers are B only in effort: they need a different, small base (words over {c,h}, window frequencies), not the angle base.

## Table: paper | result | class | effort | theme

| paper | result | class | effort | theme |
|---|---|---|---|---|
| #1,#5,#11 | skewed RD, hex-elongated dodecahedron, stretched dodecahedron: space-fillers by coordinates | C | S | Tilings, webs of bonds, one piece |
| #8 | five Platonic solids nest on 13 points in one cubic cell (exact coordinates in Q(√5)) | C | M | Golden cuts and fields |
| #10,#41 | DICTO Jewel with 12 Penrose-rhombus windows; fills space with stellae | C | M | Dehn and filling |
| #12,#16,#42 | Star/Sunstar chain nesting, exact scale factors | C | S | Golden cuts and fields |
| #13,#14,#15,#17,#18 | Dodeca-13, DICTO-Star, Jewel clusters, Kagome hulls, Hexa: clusters close exactly at every edge | C | M | Dehn and filling |
| #19,#20 | AXE, CLEO, FUJI family: gap solids and their dissections | C | M | Dehn and filling |
| #22,#23,#24,#32 | Chain of Karma, Spheres of Dharma, Bodhi Seed, Inverted Shells: nested golden chains, exact ratios | C | M | Golden cuts and fields |
| #25,#26 | Spheroid-13 RD, ATOM-13x13: clusters of 13 on periodic/golden blocks | E | - | (none) |
| #27,#28,#29,#30 | In-betweens, Hecatodihedron, Theaetetus, Fibonacci spine: constructions and tables | E | - | (none) |
| #31,#31a,#34,#34a,#35,#35a,#35b | Ogdoecontahedron family, Progenitors, Vajrayana: new solids by cut rules (convexity, face counts) | C | M | (none) |
| #33 | Double Vision: both golden cycles in one space, Galois twin | C | M | Golden cuts and fields |
| #36,#37,#37a | Golden Bodhi Pyrochlore; OG on octet / gyrated octet | E | - | (none) |
| #38,#38a | Universal PiTet growth rule T = polar of inverted corners; Kepler-Poinsot cycle x phi^3 | B | M | Golden cuts and fields |
| #39,#40 | OG family: Q4=Q8=0, fingerprint W6; nonzero Dehn invariant for nine solids | C | M | Dehn and filling |
| #43 | Kyushindo cores | E | - | (none) |
| #44 | Aristotle's pyramid: which sets of the five face pyramids fill space | D | L | Tilings, webs of bonds, one piece |
| #45 | Reuleaux Platonic solids | E | - | (none) |
| #47 | Every mix of the Platonic solids fills space (one-world) | E | - | (none) |
| #48 | Golden split: Icosaxes at t=1/phi convex truncated octahedron; uniqueness of AXE cut | C | M | Golden cuts and fields |
| #49 | Polyhedral stretching theorem | D | L | Tilings, webs of bonds, one piece |
| #50 | One Move Each: classical space-fillers as one tilt/stretch of a lattice | C | M | Tilings, webs of bonds, one piece |
| #51 | Delian bond: cut octet double cones; unique equal-volume t_D = 1-(2/3)2^(-1/3); edge length (2√6-3)/5 | C | S | Golden cuts and fields |
| #52 | Web of bonds: golden and Delian loops are power diagrams of bcc sites | D | L | Tilings, webs of bonds, one piece |
| #53 | Census of ten two-kind networks; unlike bond never breaks; flip formula | D | L | Tilings, webs of bonds, one piece |
| #54 | One turn is a gnomon: twelve stations of the golden cycle, volumes exact in Q(√5) | C | M | Golden cuts and fields |
| #55 | David and Goliath: A15 at lambda=3/4, exact cells | C | M | Tilings, webs of bonds, one piece |
| #56 | Sonsam and Lahdeli: keying lemma; twinned octet walk | D | M | Tilings, webs of bonds, one piece |
| #57 | Rule of Halves: pieces of tetrahedral/octahedral holes congruent to pieces of pure stackings, all stackings | B | M | Stacking laws |
| #58,#59,#60 | Series summary; Icosaxes Hexa; Janus c/h pyrochlore | E | - | (none) |
| #61 | Swap Rule: piece volume V(t|t') = A(t)+B(t'), any stacking | B | M | Stacking laws |
| #62 | Shadows of 4D: no shadow is regular deltahedron; n-gon bipyramid only n<=5 | C | M | Queens and 4D / sweeps |
| #63 | White Queen 600-cell: 62 slice patterns, exactly 12 triangle-only | C | L | Queens and 4D / sweeps |
| #64 | Swap Rule in crystals (four families, up to six layers) | C | S | Stacking laws |
| #65 | Red Queen 120-cell: five Platonic pyramids are cores; atlas of 124 patterns | C | L | Queens and 4D / sweeps |
| #66 | Hexagonality Law: every piece total is a straight line in h | B | M | Stacking laws |
| #67 | Random stackings and faults: Theorems 1, 2 (additive volume totals; fault cost) | B | M | Stacking laws |
| #68 | Polytype ANNNI: property linear in h iff J2=J3=0 | B | S | Stacking laws |
| #69 | Fibonacci stacking: h = 1/phi^2, no two h adjacent; law on approximants (bridge) | B | S | Stacking laws |
| #70,#71,#72,#73 | Hexagonality Law in real materials II-V: counting theorems (hole pairs, eclipsed bonds h/2, Pauling-3 counts) plus predictions | B | S | Stacking laws |
| #74 | Spin ice/kagome on every stacking; Loop Equality (conjecture, then #102) | B | M | Loops |
| #75 | HexOct: two tiles for every stacking | B | M | Stacking laws |
| #76 | Between the Queens: stages by cuts 1/3 etc., slice counts | C | M | Queens and 4D / sweeps |
| #77 | Face to Face: apexes of face-to-face tilings by five pyramids make whole solids | D | L | Tilings, webs of bonds, one piece |
| #78 | TI Star: pentakis dodecahedron hull, nesting of the turn (s=2, phi) | C | M | Golden cuts and fields |
| #79,#80,#81,#85 | Star cores: polar-spike fill, gains of T, core cycles, valley law (exact angle lemmas) | B | M | Golden cuts and fields |
| #83 | HexOct knitting: one plane meets every layer once per repeat at thirds | B | S | Stacking laws |
| #84 | Window Law: mean of g-layer quantity is Σ F(u) f_u; contains Hexagonality Law | B | M | Stacking laws |
| #86 | HexOct family | E | - | (none) |
| #87 | Vacuus solids: Star law volume; fins and struts | B | M | Fair dice |
| #88 | Every Platonic solid has exactly two golden cuts; truncated triangle with ratio phi | C | M | Golden cuts and fields |
| #89 | Golden pairs are slices of 4D solids (tesseract, 24-cell, 120-cell); Theorem A no cube section | C | L | Golden cuts and fields |
| #90 | Field obstruction: distance fields Q(√5) vs Q(√2,√5)... Galois twins of golden cube depths; 6D lifts | B | M | Golden cuts and fields |
| #91 | All-golden 4D polytopes P x P* sweep; Q(√5); no icosahedral lattice in R^6 | B | M | Golden cuts and fields |
| #92 | Pyramid tilings by regular tetrahedra and octahedra: classified exactly (Barlow stackings) | D | L | Tilings, webs of bonds, one piece |
| #93 | Cube-polar pairs: CsCl tiling is the only tiling by P_mu and Q_mu | D | L | Tilings, webs of bonds, one piece |
| #94 | Silent golden station: Q4(P_mu)=0 iff mu=phi; volume product; Lindelof | B | M | Golden cuts and fields |
| #95 | Pentagons for the kites: OG cut; nonzero Dehn invariant | C | S | Dehn and filling |
| #96 | Reading the voids: OG nonzero Dehn invariant, adaptor volumes | B | S | Dehn and filling |
| #97 | Narcissus keyed: layers on two joins give non-periodic tilings (17 keyed copies) | D | L | Tilings, webs of bonds, one piece |
| #98 | Narcissus: symmetry, space-filling alone | D | M | Tilings, webs of bonds, one piece |
| #99 | Plato's five in the octet: nest O>I>D>C>T, exact edge ratios | C | S | Golden cuts and fields |
| #100 | Dehn test picks lone tilers: D(S(mu)) formulas for cube-octahedron, CO-RD, tetrahedron sweeps | B | M | Dehn and filling |
| #101 | Held by shape alone: octet layer locked octahedra (computer check) | E | - | (none) |
| #102 | Loop Equality: closed non-backtracking loops same in every stacking (proved) | D | L | Loops |
| #103 | DICTO Yantra: unique admissible Sri Yantra; exact rational yantra, 43 triangles | A | - | Yantra |
| #104 | Scutoid tissues 4D: sweep counts of simple 4-polytopes (116/366/116 ...) | D | L | Queens and 4D / sweeps |
| #105 | 1:2 truncated octahedron: 4D Vacuus of the permutohedron | E | - | (none) |
| #106 | One world for Platonic solids (survey) | E | - | (none) |
| #107,#108 | Vacuus of the Queens; Atlas of the chains (Coxeter polytopes) | D | L | Queens and 4D / sweeps |
| #109 | Silent Running: twisted silence in degree k for 600-cell orbits | D | L | Queens and 4D / sweeps |
| #110 | Walls of Silence: 1200+1200+600 copies in 120-cell; index law | D | L | Queens and 4D / sweeps |
| #111 | Fair dice: Prop 1 existence on 12 lines; Theorem 2 fair 14-face die mu closed form; 20-face die (R/r)^2=11/3 | C | M | Fair dice |
| #112 | Aequi: polar identity; Alexandrov equal-mass condition; finite test (cites Alexandrov) | D | L | Fair dice |
| #113 | Dehn Canon (Theorems 1-6, Lean, Palomar) | A | - | Dehn and filling |
| #114 | Scutoid tissues: births=deaths=cells, swaps per birth <F>/2-3 (Morse-type count) | D | L | Queens and 4D / sweeps |
| #115 | GET A/B Grünbaum k=10 (Lean for GET B; Palomar) | A | - | Dehn and filling |
| #116 | Dehn-Hadwiger 4D (Lean; Palomar) | A | - | Dehn and filling |
| #117 | Dehn packets Theorem 4 (a),(b),(c) lead (Lean in progress) | A | - | Dehn and filling |

## Proposed themed formal works (ranked by value / effort)

Each work = one Lean library plus a short blueprint paper, released together and registered on Palomar. Titles are working names for DICTO to choose.

### 1. Stacking laws (working title: The Laws of Stacking)
- Certifies: #57 Rule of Halves, #61 Swap Rule, #66 Hexagonality Law, #84 Window Law (the master statement; #66 is its g = 1 case), #67 Theorems 1-2 (totals and fault cost), #68 (linear iff J2=J3=0), #69 Fibonacci stacking (h = 1/phi^2, no two h adjacent), #70-73 counting theorems, #83 knitting plane.
- Foundations (new but small): infinite and finite words over {c,h}, window frequencies, mean of a g-layer function, Fibonacci substitution frequency (phi from the substitution matrix). All combinatorial; no geometry beyond the stated piece volumes F(x,y) as hypotheses. Piece-volume congruences of #57/#61 stay as stated inputs at first (class D part), so the work proves the laws, not the volumes.
- Effort: M (the Window Law and #69 are S each; #57/#61 geometry is the only L part and is left out of v1).
- Serves: the bridge periodic to aperiodic (#69 is the bridge theorem, Fibonacci vs every periodic approximant, the same law); geometry gives laws; the one clean "law of everything" statement.

### 2. Dehn and filling (working title: The Dehn Canon II: What Fills Space)
- Certifies: #113, #115, #116 (already formal, re-exported), #117 Theorem 4 (in progress), plus #100 (D(S(mu)) formulas for the cube-octahedron, CO-RD and tetrahedron sweeps, so which members can be lone tilers), #95/#96/#39/#40 (nonzero Dehn invariant of the OG family), the capped cubes, Dehn screens, the Jewel (#10).
- Foundations: exactly the existing base. Missing, from the packets LEADS: invariance of wedgeAngle under isometries and scalings; deriving angle tables from coordinates; Dehn invariant of a cut tetrahedron (#100 Proposition 2.1: 6a(1 - sum c_i) tensor arccos(1/3)), then sweeps by piecewise-linear pieces.
- Effort: M (finish #117 is S-M; #100 and OG nonzero: M).
- Serves: geometry gives laws (Dehn test as the law deciding which solids tile); one keyed piece (Dehn test rules out all but the lone tilers); already half-built, and registrable at once.

### 3. Golden cuts and fields (working title: Golden Cuts and Their Fields)
- Certifies: #88 (two golden cuts per Platonic solid, truncated triangle ratio phi), #90 (field obstruction: Q(√5) for D, I, T, O cuts; Galois twins for the cube's depths t_G, t_L share a minimal polynomial), #91 (the D x I sweep lies in Q(√5), no icosahedral lattice in R^6), #94 (Q4 = 0 iff mu = phi), #99 (nest edge ratios), #54 (gnomon volumes), #51 (Delian bond t_D, edge (2√6-3)/5), #48 (golden split).
- Foundations: Q(√5), Q(√2), Q(√2,√5) arithmetic and minimal polynomials (existing algebra), vertex lists as exact data, a convexity-by-inequalities certificate, volumes by exact sum over a triangulation. Class C: decide / norm_num over number fields.
- Effort: M for the field and polynomial parts (#90, #94, #51, #99 are S each); L for the 4D slices (#89).
- Serves: geometry gives laws (the field decides which cuts exist); the twin rule; makes the "Galois twin" a theorem anyone can check.

### 4. Fair dice (working title: Aequi, Machine-Checked)
- Certifies: #111 Proposition 1 (each of the twelve axis lines has a fair member, face solid angle 4 pi/N), Theorem 2 (fair 14-face die, closed form), Theorem 3 (20-face die (R/r)^2 = 11/3), #87 Vacuus volume (Star law). From #112: Lemma 1 (polar identity) and Proposition 2 (finite test for equal masses) only; Theorem A (existence and uniqueness, Alexandrov) cited, not proved.
- Foundations: solid angle of a polyhedral cone from the set (needs the spherical excess; partly shared with the wedge-angle lemma of work 2), exact trigonometric algebra (cos 2pi/7 minimal polynomial). Alexandrov is D and is left as a named hypothesis.
- Effort: M for #111; L if Alexandrov is ever attempted.
- Serves: show how things are built (a die whose fairness is a certificate); popular and easy to explain; modest connection to the bridge, none to the keyed piece.

### 5. Loops and the one piece (working title: One Piece, Any Stacking)
- Certifies: #102 Loop Equality (every site of every stacking has the closed non-backtracking loop counts of diamond; Corollaries to spin ice and sphere packings), #97 Theorem 1-2 (Narcissus fills in layers with free straight/turned joins, so uncountably many non-periodic tilings), #98 (Narcissus symmetry and tiling).
- Foundations: graphs of the close-packed stackings as locally finite graphs from a layer sequence; non-backtracking walk counts; for #97, a tiling of space by one polytope given by half-spaces plus a layer-gluing lemma (new: general polytope tilings, class D).
- Effort: L (#102 combinatorial, perhaps M if the proof is local; #97 L).
- Serves: the bridge and the one-piece aim directly (this is the work closest to DICTO's aim "one keyed piece forcing aperiodic stacking"), but it is the heaviest; do it after 1 and 2 so the stacking words and the tiling base exist.

### 6. Queens and four dimensions (working title: Exact Atlas of the Queens)
- Certifies: #63 (62 slice patterns, exactly 12 triangle-only), #65 (124 patterns), #76 (stage cuts 1/3), #62 (no regular deltahedron shadow), #109/#110 (silences, wall counts), #104/#114 (sweep counts 116/366/116 ...; swaps per birth <F>/2 - 3 as a Morse count).
- Foundations: coordinates of the 600-cell and 120-cell in Q(√5) (120 and 600 points, finite enumeration), slice pattern computation by finite exact checks, 4D polytopes (the Dehn 4D work supplies only the invariant, not the polytope theory); the general sweep theorem needs Morse-type counting (D).
- Effort: L; many finite certificates are heavy for `decide`, so use certificates generated outside and checked in Lean.
- Serves: geometry gives laws (the swap count law) and show how things are built; lowest value per effort now.

### Not formalised (class E, keep as story)
Cluster pictures and named solids (#13-#37 family: Dodeca-13, Spheroid-13, Hecatodihedron, Bodhi Seed), #43, #45, #47, #58-60, #86, #101, #105, #106. Their numbers are exact but they are catalogues; they should remain informal and cite the formal works where a theorem sits inside.

### Ranking (value / effort)
1. Stacking laws (M, highest value: the bridge theorem and the Window Law, new small base, many papers certified).
2. Dehn and filling (M, half built, immediately registrable, three entries already on Palomar).
3. Golden cuts and fields (M, reuses the existing algebra, certifies a large block of the golden strand).
4. Fair dice (M, popular, small base, one external dependency).
5. Loops and the one piece (L, closest to DICTO's central aim, do after 1-2).
6. Queens and four dimensions (L, most computation, lowest value per effort).

First step ready: take the Window Law (#84) main theorem plus Hexagonality Law (#66) and Fibonacci h = 1/phi^2 (#69) as a self-contained Lean statement over words; no geometry needed.
