# DICTOnary of Atoms v1.4: completeness audit (17 Nov 2026)

Read-only audit. No paper, book, Concordance or dataset file was edited. Nothing was committed or published.

**Conclusion.** The DICTOnary's catalogue is complete for the dataset inventory (`studies/2026-10-29-quanta-atoms/index.csv`, which stops at #89) plus D133/D134 (#96). It is missing:
- **38 new DICTO solids and pieces.** Proposed numbers are D135–D172. Six of these numbers depend on a decision by DICTO.
- **About 20 kit pieces with descriptive labels only**, not numbered. DICTO decides whether they count as atoms.
- **26 clusters, structures and networks.**
- **13 known or rediscovered shapes** with DICTO names, plus a scope question on unnamed classical building blocks.

Most of the gap is in five places:
- the early kit pieces of #19, #24, #26 and #27 (Hasu, Chatra, Mudra, Diadem and the Dharma blades), and the F21 octet pieces (Weirdstone, Tadpole);
- the keyed forms of #56;
- the Julias and Pimentels of #54;
- the post-#89 papers: #89 (Kepler–Poinsot golden cuts), #91 (Golden OGs), #97/#98 (Narcissus, Covenant), #99 (Sheriff, Lone-star), #105 (1:2 and 2:1 truncated octahedra) and #109 (golden 5-cells);
- names first given in the books (Platonic Solids, Permutohedron Paradigm, Laws of Stacking).

None of the missing shapes is in the *DICTO Solids* dataset. Exact geometry exists in study files, or follows from a closed form, for about two-thirds of the 38.

## Method and sources checked

**Catalogue.** I parsed all 155 drawn entries of `paper.html` (D1–D134 without D118; 8 drawn clusters; 14 drawn Known entries), plus the three "Not drawn here" tables:
- D118;
- 29 clusters and structures;
- 13 Known shapes.

A shape counts as included only if it has its own row. A mention inside another entry, or in the "data, work by work" sections, does not count.

**Papers #8–#110.** I read the HTML of every numbered paper, picking the paper by its own meta line or its first DOI.
- #19, #20 and #27 were read from `studies/*/paper/paper-house.html`.
- #1–#16 (the Kaleidohedra findings, record 23173809) have no HTML. For them I used `k-mix/DISCOVERIES.md` (F12, F15, F16, F20, F21).
- #31a, #34a, #35a and #35b have no HTML. They are covered by their DICTOnary sections.

**Books.** The 11 English `book-*/paper.html`.

**Concordance.** All 253 entries of `concordance.json` key `names`.

**Search methods.** Five passes:
1. Phrases that give a name ("DICTO named", "we call", "DICTO's name", "the names … are DICTO's").
2. Bold and italic terms in the HTML.
3. Every capitalised term in the corpus that is not in an English dictionary and not in the DICTOnary or the Concordance (2,604 terms, reviewed at frequency ≥ 3; the `DICTO …` names at any frequency).
4. The piece tables inside the DICTOnary's own data sections.
5. A grep of the studies (`k-research/studies`) and the app (`k-mix/src`) for geometry.

**Limits.**
- Lower-case descriptive labels used only once ("the notched octahedron") are caught only where they sit in a DICTOnary data table or a status table. Some may remain in long tables of #39–#43 and #79–#85.
- Statuses are quoted from each source's own status or prior-art lines. Where none was found, I say so.

Dates: the Concordance `papers` date, or the version date in the meta line. Publication order is by Zenodo record id.

---

## A. Missing new solids and pieces of DICTO's, with proposed D-numbers (in order of first publication)

"Exact geometry" key:
- **dataset**: a model file in *DICTO Solids*. None of the 38 has one.
- **exact (study)**: exact coordinates or closed-form exact data in the named study, not yet in dataset format.
- **closed form**: the coordinates follow at once from a stated exact construction.
- **float**: app or study coordinates in floating point only.
- **to build**: no geometry file found.

| D (proposed) | DICTO's name | First (#, date) | Kind | Status in its source | Exact geometry |
|---|---|---|---|---|---|
| D135 | Weirdstone (L/R) | finding F21, 2026-10-10 (Kaleidohedra record 23173809); first paper text #77, 2026-10-30 | piece (corner cap of the all-icosahedral octet's tetrahedron: icosahedron ½ + 4 Weirdstones + 6 Tadpoles) | F21: "**not found** as fillings"; app: "Names by DICTO" | float: `k-mix/src/app/octet-data.js`, `krp-core/src/polyhedra/kits13.js` (KIT13_OCTET_WEIRDSTONE, _M); exact matches in `studies/2026-10-27-five-pyramids/data/face-matching-exact.json` |
| D136 | Tadpole (L/R) | F21, 2026-10-10; #77 | piece (edge cap, same tetrahedron) | as D135 | as D135 |
| D137 | Frog Chorus (the gap star) | F21, 2026-10-10 | piece (the closed gap star round each corner of the all-icosahedral octet; volume (33 + 23√5)/48) | F21 as above. **Name clash:** the Concordance gives "frog chorus (five voices)" to #30's five OG packings (Group B) | float: `octet-data.js` (C.frog) |
| D138 | Diadem L/R | #24 The Bodhi Seed (record 23311353; v3 20 Oct 2026) | piece (Bodhi seed Kit B; 2 triangles, 3 quadrilaterals; chiral; vol 0.15674) | #24: names Bodhi seed, Vajra, Crown Jewel, Diadem are DICTO's; abstract: kits "not found" with D17 Crown Jewel and D18 Vajra (fine), which are entered | float, five-place coordinates (#26 Checks): `kits13.js`; values in DICTOnary A.27 |
| D139 | Hasu | #26 ATOM-13×13 (23333183, 20 Oct); defined #19 Fig. 5 | piece (the finned unit: an icosahedron with its share of the Lotus seed's gap pieces, 21 parts, 45 faces; analogue of D8 Dodeca-13 Unit) | #26: "the piece names" are DICTO's; no separate status line | float: `kits13.js` (Icosa-13 kit); exact as a union of the dataset-grade AXE/CLEO/FUJI |
| D140 | Chatra | #26 (23333183) | piece (Bodhi Kit A; 3 triangles, 2 quadrilaterals, 1 pentagon; vol 0.86915; 60 per seed) | #26 piece names DICTO's; #24 says the kits were not found | float (five places): `kits13.js`; DICTOnary A.27 values |
| D141 | Mudra | #26 (23333183) | piece (Bodhi Kit A; quadrilateral pyramid; vol 0.09687) | as D140 | as D140 |
| D142 | Vajra (twist) | #27 Capturing the In-betweens (23345502; v3 14 Oct) | piece (Dharma shell, 20; twisted triangular frustum; vol 0.22215) | DICTOnary A.27 lists it with no entry; the #27 credit line was not found | float: `studies/2026-10-13-fused-shells` (pieces.json, floats only) |
| D143 | Cleo-low 2 | #27 | piece (Dharma, 20; trigonal pyramid on the outer icosahedron's face; vol 0.36892) | as D142 | float (fused-shells) |
| D144 | Vajra-blade | #27 | piece (Dharma, 60; tetrahedron with one mirror; vol 0.011271) | as D142 | float (fused-shells) |
| D145 | Sevenfold-blade | #27 | piece (Dharma, 30; 6 triangles + 1 quadrilateral; vol 5 − 2√5) | as D142 | float (fused-shells); the volume is exact |
| D146 | Triskelion Hex | #19 AXE, CLEO and FUJI (23351291; v2 14 Oct) | piece (FUJI + 3 AXE, round a dodecahedron corner) | #19: "The names are ours"; FUJI is new, so the union is too (no separate line) | closed form (union of D12 FUJI and AXE); `studies/2026-10-14-axe-cleo-fuji` |
| D147 | Triskelion | #19 | piece (CLEO + 3 AXE; exactly the volume of the pentagonal cap J2) | no status line; might be a known dissection, so check before calling it new | closed form (CLEO + AXE) |
| D148 | Julias (G3, G4, G5a, G5b, G6, G8, G9, G10) | #54 One Turn Is a Gnomon, 2026-10-25 | pieces (the cone-section steps of the golden cycle's gnomon; 8 shapes) | #54 §8: "What we did not find is this reading of DICTO's cycle"; each is "a distorted relative of a classical solid" (e.g. G4 of J9). **Decide: one set number (as D74 Cleo Towers) or eight** | exact (study): `studies/2026-10-25-gnomon-shapes` (stations-exact.json, pieces.json) |
| D149 | Pimentel (G11) | #54, 2026-10-25 | piece (60 triangular bipyramids of the closing step; relative of J12) | as D148 | as D148 |
| D150 | Sonsam-K | #56 Sonsam and Lahdeli, 2026-10-25 | piece (keyed Sonsam) | #56: "the two new walks' pieces and the keyed forms were not found in the sources" | exact (study): `studies/2026-10-25-hidden-bonds` (equal_volume_exact.py, export_keyed_gyrated.py) |
| D151 | Lahdeli-K | #56 | piece (keyed Lahdeli) | as D150 | as D150 |
| D152 | Ian Dury-K | #56 | piece (keyed Ian Dury) | as D150 | as D150 |
| D153 | Rhombo-K | #56 | piece (keyed 60° rhombohedron, "a six-pointed star"; the plain 60° rhombohedron is classical) | as D150 | as D150 |
| D154 | Double TI Star | #78 TI Star (23782577, 2026-11-03) | solid (TI with face pyramids, tips at 2× the face centres) | #78: DICTO's name. The D103 entry says only "the doubling form (2×) is the same construction". **Decide: its own atom, or part of D103** | exact (study): `studies/2026-10-30-spiked-ti/data/families-2.json` |
| D155 | Maedate | #85 Eccentric Pieces, 2026-11-02 | piece (joins Kagemusha's two crossing notch spikes; irregular octahedron, 6 corners, 8 triangles) | DICTO named it (#85). No status line found in #85; check | exact (study): `studies/2026-11-01-star-cores-d`, `2026-11-01-star-cores-book/scripts` |
| D156 | Kuwagata | #85, 2026-11-02 | piece (two pyramids with apexes lowered to the notch mirror plane) | as D155 | exact (study): `kuwagata_exact.py`, `data/kuwagata-cycle.json` |
| D157 | Greater Golden Cut Great Dodecahedron | #89, 2026-11-03 | solid (star) | #89 §8: "Not found: golden-ratio truncation of Archimedean, Catalan or Kepler–Poinsot solids as such"; DICTO named the eight | closed form (exact cut depths): `studies/2026-11-03-golden-cuts-beyond-plato/data/s3-kepler-poinsot.json`; no model file |
| D158 | Lesser Golden Cut Great Dodecahedron | #89 | solid (star) | as D157 | as D157 |
| D159 | Greater Golden Cut Great Icosahedron | #89 | solid (star) | as D157 | as D157 |
| D160 | Lesser Golden Cut Great Icosahedron | #89 | solid (star) | as D157 | as D157 |
| D161 | Greater Golden Cut Small Stellated Dodecahedron | #89 | solid (star; x = (7 + √5)/22) | as D157 | as D157 |
| D162 | Lesser Golden Cut Small Stellated Dodecahedron | #89 | solid (star; x = 1/3) | as D157 | as D157 |
| D163 | Greater Golden Cut Great Stellated Dodecahedron | #89 | solid (star) | as D157 | as D157 |
| D164 | Lesser Golden Cut Great Stellated Dodecahedron | #89 | solid (star) | as D157 | as D157 |
| D165 | Lesser Golden OG | #91, 2026-11-03 | solid (OG's combinatorics, at μ = √5) | #91: "New within these checks … the Golden OGs" | exact parameter; construction in `studies/2026-11-03-dual-pairs-dimensions` (s4-og-dharma.json), `2026-11-15-mccooey-comparison`; to build |
| D166 | Greater Golden OG | #91 | solid (μ = (13 + 6√5)/11) | as D165 | as D165 |
| D167 | Narcissus | #97 Narcissus Keyed (24005567, 2026-11-06), defined in #98 (24005929) as "a ten-cornered piece we call Narcissus"; mentioned in #95, 2026-11-05 | piece (self-mirroring heptahedron, h-layer piece at λ ≥ 3/8; fills space alone) | #98: "New within the sources checked: Narcissus as this particular metric heptahedron". #97: "Narcissus is Goldberg's space-filler type 10-XII" (new member of a known type) | exact (Q(√2)): `studies/2026-11-04-narcissus-cube`, `2026-11-05-one-piece-any-stacking` |
| D168 | Covenant | #98, 2026-11-06 (also #97) | solid (two Narcissus joined on hexagons with a 60° turn; convex parallelohedron of 12 parallelograms) | #98: new as "the c = 1/3 member of the four-zone family"; parallelohedra are Fedorov's (1885) | exact (study) as D167 |
| D169 | Sheriff | #99 Plato's Five in the Octet, 2026-11-07 | piece (pentagonal cap of I − D: an icosahedron corner over a dodecahedron face) | #99: "New shapes"; §prior art: "New within the sources checked: … the gap pieces of I − D (Sheriff and Lone-star)" | closed form (corners of I and D) |
| D170 | Lone-star | #99 | piece (thin wedge of I − D) | as D169 | closed form |
| D171 | DICTO 1:2 Truncated Octahedron | #105, 2026-11-11 (computed unnamed in #93, 2026-11-04, as the CsCl pieces at μ = 4/3) | solid (the permutohedron of 1, 2, 4, 5) | #105: sweeps of sections are known (Bowers; Polytope Wiki), but "we found none that names the central one". New as a named, distinguished member. Also the T(1/2) member of the Koca et al. 2015 truncated-octahedron family | closed form (permutations of (1, 2, 4, 5)); `studies/2026-11-10-permutohedron` |
| D172 | DICTO 2:1 Truncated Octahedron | #105 (#93 unnamed) | solid (permutohedron of −5, −1, 1, 5) | as D171. **Decide: two numbers or one pair** | closed form |

**Undecided, with descriptive labels only.** Not numbered, because the sources give no proper name. The DICTOnary already numbers some labels of this kind (D34 Keyed octahedron, D39 Mirror middle piece Mg, D72 Dented tetrahedron), so these may qualify.
- **#37 kits** (2026-10-20; DICTOnary A.37 lists them with exact volumes): Keyed OG; notched octahedron; notched tetrahedron L/R; middle piece M0; Penrose central core and flanking cores L/R; rest piece; OG cap; grown piece G L/R; adaptor half; WOG (cell − OG; 132 faces); Wstar. The keyed W is left out: per standing instruction, it stays dropped.
- **#95** (2026-11-05), all marked "New pieces; unnamed":
  - pentagonal connector;
  - corner piece of the octet kit, with its dented tetrahedra L/R;
  - Bull-horns adaptor for the cut OG ("New; derived from D33");
  - twin connector, twin corner pieces and twin dented tetrahedra;
  - hexagonal rings L/R and the square piece;
  - the all-equal-edge cut OG ("not found").
- **Golden Ladder book**: the half Admiral Cap (one of D16's two tetrahedra; octahedron = 20 Cleo-Icos + 12 half caps).
- **#57**: the unnamed 9- and 27-corner Janus c/h families. Chucky and Fang are already entered.

---

## B. Missing clusters, structures and networks (DICTO's; no number)

| Name | First (#, date) | Kind | Status in its source | Geometry |
|---|---|---|---|---|
| Sunstar | F12 (2026-10-08); #42, 2026-10-20 | cluster (a dodecahedron with the Dogstars of its six face neighbours; vol (23 − 5√5)/32) | #42 "DICTO's name"; the Sunstar Lattice (Hart) is in Known | exact (`studies` for #42; dataset Dogstar and dodecahedron) |
| Stella–Jewel Lattice | #17 Kagome Hulls, 2026-10-20 (also #41) | structure (Jewels on even cubes, stella octangulas on odd; 3 : 1) | #41: Jewel and lattice not found | exact (D4 + stella) |
| Dodecahedral Chain | #19 (14 Oct) | structure (grown core closed by 12 caps; stages are the great stellated and the excavated dodecahedron) | no separate line | exact (closed form) |
| CLEO sphere | #20 The FUJI Family (14 Oct) | cluster (curved: 20 CLEOs in the triangular windows of six slotted rings, 12 pentagonal pockets) | DICTOnary A.20 heading only | float (app) |
| VENUS | #26, 2026-10-20 | cluster (UNITY closed by 20 VAJRA) | #26: "the clusters and their names … VENUS … are DICTO's"; UNITY is entered | float (kits13); exact pieces D13 + J11 |
| Samsara | #27 (14 Oct); with #22 Chain of Karma | structure (Chain step 2: every icosahedron of the Lotus seed replaced by a Lotus seed; 1,569 pieces) | no separate line | exact (closed form) |
| DICTO-ICOSA star | #29 Theaetetus, 2026-10-20 | cluster (DICTO-Star with a pyramid on each of its 152 free faces; 185 pieces) | #29: name DICTO's; not found | exact (`studies/2026-10-15-icosa-star-hollow`) |
| frog chorus (five voices) / A Fibonacci Spine | #30, 2026-10-20 | structure (five periodic OG packings in five slices round a five-fold axis, a Fibonacci spine on the axis) | DICTOnary A.30 has data but no entry. **Name clash with D137** | exact (#30 study) |
| Double Vision | #33, 2026-10-20 | structure (the golden cycle and its polar twin in one space, cut into one exact solid) | Interlock sets 1/2 are entered; the whole is not | exact (#33 study) |
| Kyushindo Cores (tower-shell series) | #43, 2026-10-21 | structure (shells of towers in Fibonacci beats round exact cores) | Cleo Towers D74/D75 are entered as pieces. **Decide** whether the series is an atom | exact (#43 study) |
| Icosaxes Bloom | #59, 2026-10-27 | cluster (20 Icosaxes on a dodecahedron's corners, first touch, 12 windows) | #59: "Not found … truncated octahedra on the corners of a dodecahedron, the golden stops, or this network"; "DICTO's working names" | exact (`studies/2026-10-27-icosaxes-twenty`) |
| Icosaxes Bud | #59 | cluster (closed round a hollow at 1/φ) | as above | as above |
| Icosaxes Seed | #59 | cluster (one solid, at one third) | as above | as above |
| Lotus Jewel Bloom, Bud, Seed | #59 | clusters (keyed forms). **Decide**: separate entries or with the three above | as above | as above |
| Icosaxes Kagome network | #59 | network (Keyaxes D83 is its piece) | not found (#59) | exact (#59 study) |
| DICTO Janus c/h Pyrochlore | #60, 2026-10-27 | network (Rule of Halves on the pyrochlore network, any stacking) | #60 prior art | exact (#60 study) |
| DICTO Golden Tight Cycles | #91, 2026-11-03 | structure family (nested cycles closing at a power of φ) | #91: new within checks. Spheres of Dharma and Chain of Karma are entered as structures, so a fit | exact (#91 study) |
| DICTO Void set 1 (cut OG), Void set 2 (OG) | #96, 2026-11-05 | piece sets (cut OG + Void Keeper; OG + Golden Skin + prolate rhombohedron) | named inside D133/D134 only. **Decide** whether these get separate entries | exact (#96 study) |
| Keyed Narcissus set (17 keyed copies) | #97, 2026-11-06 | piece set forcing a non-periodic stacking (the "one piece" aim) | #97 Theorem 2; no set name. **Decide** whether to give it a name and entry | exact/SAT (`studies/2026-11-05-one-piece-any-stacking`) |
| 4D Vacuus (of the permutohedron) | #105, 2026-11-11 | structure (the 65 central 3D slices carrying all 150 two-faces) | #105: sweeps known; this reading new | exact (`studies/2026-11-10-permutohedron`) |
| One World | #106, 2026-11-11 | structure (every mix of the five Platonic solids, cuboctahedron and RD on one cubic world) | #106 prior art | exact (#106 study) |
| Karma cells / flat Karma layer | #106 | structure (a dodecahedron as icosahedron + shell on the cubic grid; the plane cutting every Dogstar into a CLEO) | #106 Theorem 3. **Decide**: atom or theorem | exact |
| Angelus / the Angeli | Book *The Platonic Solids* v1.1, 2026-11-15 (study `2026-11-11-twin-vacuus`) | structure family (the Vacuus of a Galois-twin form, √5 → −√5) | the book: "Two names are not yet entries … the DICTOnary takes them up at its next version" | exact (twin-vacuus study) |
| Cleo shells (of the White Queen) | #63, 2026-10-28 | structure (fifteen shells round a 600-cell vertex, core 20 Cleo-Icos) | heading only. **Decide** | exact (#63) |
| HexOct-K (keyed HexOct tiles) | #75, 2026-10-29 | tile set (keys as marks; computing tiles) | DICTO's name; the keys are combinatorial marks, not given geometry. **Decide** | to build |
| TRD DICTOnode (turned node), Node A | Book *Laws of Stacking* ch. 18 (study note, 2026-11-04) | build nodes (sculpture hardware for c/h stackings) | "The TRD DICTOnode and its turned layout are DICTO's work". **Decide**: probably outside the DICTOnary | DICTO's script turned_node_network.py |

Book *The Platonic Solids*, ch. 10, has jewellery settings: earrings, brooch, nest pendant, satellites, claw setting. These are designs built from entered shapes. I propose leaving them out; DICTO decides.

---

## C. Missing known or rediscovered shapes (Known chapter, with discoverer)

| DICTO's name | Standard name and first maker | First in DICTO's work | Kind | Geometry |
|---|---|---|---|---|
| Unborn | pseudoicosahedron, truncated octahedron family x = 1/τ without keys (Koca et al. 2015) | F21 AXE gap (2026-10-23), #48, 2026-10-23 | solid | exact (`krp-core golden-split.js`; #48 study) |
| Tricap | Mosseri–Sadoc tile t3 (Mosseri and Sadoc 1982) | #48 (named in the app/F21 work, 10-23) | piece | exact (closed form) |
| Hound Tooth | Mosseri–Sadoc tile t2 (1982) | #77, 2026-10-30 | piece | exact (`krp-core/src/polyhedra/mosseri-sadoc.js`) |
| Cleo-low | Mosseri–Sadoc t3 at half size (DICTOnary A.27: "Cleo-low has the shape of Mosseri–Sadoc t3 at half size") | #27, 14 Oct | piece | float (fused-shells). **One-name-per-shape:** same shape as Tricap up to scale, and Cleo-low is the earlier name. Decide |
| Inner Eye | excavated dodecahedron (Wenninger 1971, model 28; Ef1g1) = I(1/φ) + 30 AXE + 20 CLEO | #19 Fig. 6 | solid | exact (closed form) |
| White Queen | regular 600-cell {3,3,5} (Schläfli c. 1852) | #63, 2026-10-28 | 4D solid | exact (#63) |
| Red Queen | regular 120-cell {5,3,3} (Schläfli) | #65, 2026-10-28 | 4D solid | exact (#65) |
| cut OG | rectified truncated icosahedron (near-miss Johnson; McCooey) | #95, 2026-11-05 ("Rediscovered … its relation to the OG is new") | solid | exact (#95/#96 studies) |
| Golden Truncated 5-cell (A) | W(A4) orbit polytope of Koca, Koç, Al-Barwani and Al-Farsi (types fixed by their Dynkin labels) | #109, 2026-11-16 (named 11-17, v2) | 4D solid | exact (hull of perms of (φ², φ², φ², φ, 0)) |
| Golden Cantellated 5-cell (B) | as above | #109 | 4D solid | exact (perms of (φ², φ², 1, 1, 0)) |
| DICTO 13-COA (13-Corner Octet Atom) | augmented cuboctahedron (Stewart 1970) | Book *Permutohedron Paradigm* v1, 2026-11-15 (Concordance: draft "The Permutohedron Family", 12 Nov) | solid | exact (closed form) |
| Hemi RD | half rhombic dodecahedron (classical; Polyhedraverse's piece) | Book *Permutohedron Paradigm* | piece | exact |
| OCT-16 / TBP-5 | 16-cell and 5-cell edge-first shadows: the square bipyramid (cell of the known square bipyramidal honeycomb) and a J12-pattern variant | #62, 2026-10-27 | solids (labels) | exact (#62). **Decide**: labels or entries |

Also met, not entered, and not claimed new:
- #62: the equal-edged "12-dented icosahedron" and "augmented dodecahedron". #62 says "neither solid is claimed new".
- #110: the expanded 5-cell "C3".
- "Echo": a role name for the cube, found in the Concordance and a study only, never in a paper.

**Scope question for DICTO.** The Known chapter now lists classical pieces the work builds with even where they have no DICTO name: Bain RD, J1 P, Q/Q′, the brick, the hexagonal prism. The same rule would also admit the classical building blocks of the papers:
- golden Bilinski dodecahedron and Kelvin's truncated octahedron (#26);
- great stellated dodecahedron and excavated dodecahedron (#27 stages);
- rhombic hexecontahedron (Bodhi stage);
- prolate and oblate golden rhombohedra (#44, #96);
- 60° rhombohedron (#56: "classical … no new name");
- Euclid's roof, J2, J11, J63;
- trapezo-rhombic dodecahedron (Laws of Stacking ch. 18);
- McCooey's 6-truncated pentakis dodecahedron.

Either these are added, or the chapter's rule becomes "known shapes DICTO named, rediscovered or used as named connectors".

---

## D. Excluded: not shapes (or not separate shapes)

| Concordance name or term | Reason |
|---|---|
| Delian bond; DICTONIC BONDS; Twinned Delian bond | a position, or pair names (members entered) |
| DICTONIC SOLIDS; DICTO-Kepler golden truncations; DICTO Golden-Regular Cuts; DICTO-GTT-Solids; DICTO Equilibrium Space-Fillers (#88, Bonds book) | family names; members entered |
| DICTO stretched solids (#49) | family name; only D5 entered. #49's other members are unnamed; DICTO can name them |
| Galois twins | alias for the pair D123/D124 |
| HexOct; HexOct family | name of the tile pair and of the family; members D110–D118 entered |
| Janus c/h pieces; TI Star | family names (members D80/D81; D103 and D154) |
| Ritsudō cycle; Nenrin | alias of Spheres of Dharma; a growth mode |
| Fibonacci stacking (joint, #40) | a layer sequence, not a solid |
| golden tetrahedra (Danzer, Mosseri–Sadoc) | generic classical class; individual tiles are entered or listed in C |
| Hexagonality Law, Window Law, Mirror Law, Rule of Halves, Swap Rule, Splash Rules, Turn Theorem, PiTet, OG turned out, Loop Equality | laws, rules, methods |
| DICTO Hopscotch, Antipol, hop, step, jump, turn, emergence/dissolution, Hopscotch Paradigm, Hopscotch Theorem | framework terms |
| Theaetetus (world), Golamandala, Golayantra, Golden Silences, DICTO Transitional Shells, DICTO-TIC | app worlds and app groups |
| Silence Is Golden | chapter title |
| second Vacuus; heart / inherited heart / non-heart; "cats" (#110) | concepts, kinds, role names |
| scutoid tissue; 4D scutoid (#104) | classes of cells, not one shape. Decide only if DICTO wants a class entry |
| DICTO Yantra; Cleo-Octangula; Cleo-Antonius; the 81-triangle Golayantra sphere (#103) | plane figures and slope pairs; outside a catalogue of solids unless DICTO wants it |
| DeltaZip, B1NR, DICTOspheres | sculpture systems |
| Rock-Salt Pieces (Laws of Stacking ch. 19) | the regular pieces of rock salt; no new shape |
| Supercells (#99); cell cores and corner cores (#65) | descriptive groupings |
| Dragon Jewel; Shadow-17; Slice-48; Oktaktis; Humpty Dumpty; Alicia, Unicorn, Bandersnatch; DESHI; Lotus seed; Icosa-13 | already entered under another name, given as aka |

**Not yet published.** These cannot enter until a paper carries them:
- **DICTO Grünbaum–Escher Triacontahedron (GET A, GET B)**: named 2026-11-15, study `2026-11-15-grunbaum-k10`; the prior-art check against Senechal–Taylor 2023 is still pending.

---

## E. Gaps in the Concordance `names` (shapes in papers or books with no name entry)

1. **Pieces.** Hasu; Triskelion; Triskelion Hex; Inner Eye; Chatra; Mudra; Vajra (twist); Cleo-low; Cleo-low 2; Vajra-blade; Sevenfold-blade; Weirdstone; Tadpole; Hound Tooth; Double TI Star.
2. **Clusters and structures.** Dodecahedral Chain; Samsara; CLEO sphere.
3. **4D solids.** Golden Truncated 5-cell; Golden Cantellated 5-cell.
4. **Known or descriptive shapes.**
   - cut OG (rectified truncated icosahedron); Hemi RD; OCT-16; TBP-5; expanded 5-cell C3.
   - the #37 kit pieces (Keyed OG, WOG, Wstar, notched octahedron and tetrahedron, grown piece G, Penrose cores).
   - the #95 unnamed pieces; the keyed Narcissus set; Icosaxes Kagome network (named only inside the Keyaxes entry); TRD DICTOnode and Node A.
5. **Families and name clashes.**
   - Angelus: the Concordance has only "Angeli".
   - Twinned Delian bond and DICTO Equilibrium Space-Fillers: family names.
   - Frog Chorus (F21 gap star): the Concordance holds the name only for #30.
6. **Data faults in `concordance.json`.**
   - the "Angeli" entry has a date ("2026-11-11") in its `d` (D-number) field;
   - "DICTO Void set 1 … set 2" has an empty-string `d`, where other entries use "-";
   - "13-Corner Octet Atom" (`first`: a draft) is the augmented cuboctahedron (Stewart 1970), but is listed as DICTO's without that credit;
   - Narcissus, Echo and Covenant have `first` = a study or chapter title, not a paper number (Narcissus and Covenant: #97/#98; Echo is in no paper).

---

## Decisions needed from DICTO

1. **Families.** One atom or several:
   - Julias G3–G10: one set number or eight;
   - the Golden OGs and the eight Kepler–Poinsot golden cuts: one number each, as proposed;
   - the 1:2 and 2:1 truncated octahedra: two numbers or one pair;
   - Icosaxes and Lotus Jewel Bloom/Bud/Seed: three entries or six;
   - Void sets 1 and 2.
2. **Double TI Star.** Its own atom (D154), or kept inside D103.
3. **Name clashes.**
   - Frog Chorus: the F21 gap star or #30's five OG packings. One name per shape, first name wins, so F21 (10-10) is before #30.
   - Cleo-low (#27) and Tricap (#48): the same shape up to scale.
4. **4D shapes.** Whether the DICTOnary takes them at all: White Queen, Red Queen, the golden 5-cells, the DICTO All-Golden Polytopes (#91, new, unnamed individually), C3.
5. **Descriptive kit labels.** Whether the #37 and #95 kit pieces count as atoms.
6. **Known chapter scope.** Only DICTO-named or rediscovered shapes, or all classical building blocks.
7. **Status lines to settle before numbering.**
   - Triskelion (possibly a known dissection);
   - Maedate and Kuwagata (no prior-art line found in #85);
   - the Dharma blades of #27 (no status line found).

## DICTO's decisions (17 Nov 2026: "yes to all")

1. Families: one D-number per distinct solid; sets of solids go to the Clusters chapter without D-numbers. Julias G3–G10: eight numbers. 1:2 and 2:1 truncated octahedra: two numbers. Icosaxes and Lotus Jewel Bloom/Bud/Seed: six entries. Golden OGs and the eight Kepler–Poinsot golden cuts: one number each. Void sets 1 and 2: Clusters, no D-numbers.
2. Double TI Star: stays inside D103 as its doubled form (no own number).
3. Frog Chorus = the F21 gap star (first name); #30's five OG packings get a plain description. Cleo-low and Tricap: one entry, Cleo-low (#27), note that Tricap (#48) is the same shape at another scale.
4. 4D shapes: yes, a short last chapter; White Queen (600-cell) and Red Queen (120-cell) in silver (classical), golden 5-cells, All-Golden Polytopes and C3 in gold.
5. Descriptive kit labels (#37, #95): not atoms; listed by name inside their kit's entry, no numbers.
6. Known chapter rule: "known shapes DICTO named, rediscovered or used as named connectors"; other classical building blocks cited where used.
7. Status lines (Triskelion, Maedate, Kuwagata, Dharma blades): prior-art check by Claude, no decision needed.
8. Kepler–Poinsot golden cuts D157–D164 (numbers to be re-derived): see-through crystal shells with crisp edges.
