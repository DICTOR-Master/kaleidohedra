DICTO · dictospheres.com

# Space-Fillers and Lattice Moves: proposal for Version 1 (content and figures)

7 November 2026 · for DICTO's decision · PROPOSAL, not the build. Nothing in the book or any paper has been changed.

DICTO on the 4-chapter draft: "ok so far needs a lot more content perhaps from other papers and needs lots of beautiful example figures".

**My pick, one line:** grow the book from 4 chapters (about 20 pp) to 10 chapters in three parts plus a picture atlas (about 105 pp). It takes seven published papers that have no book of their own (#25, #26, #41, #42, #17, #18) and two that DICTONIC Bonds now holds as its Part I, "Filling" (#47, #50). Every other filling in the series appears once, as an atlas plate that cites its home book. Five overlaps need DICTO's decision (Section 4).

---

## 1. Method and sources checked

- Papers: every `papers/*/paper.html`. Publication state from each folder's `zenodo-state.json`. Papers from before 20 October have no state file in their folder; for them I used their DOI in the Concordance.
- Concordance: `dicto-concordance/concordance.json`, keys `papers` (93 entries), `strands` (I read the threads fill, bonds, kepler, cycles, og, stack, pyr, cuts and sweep), `destinations_2026_11_04`, `destinations_2026_11_05`, `gaps`, `overlaps_note`. I also used `dicto-concordance/waiting-triage-2026-11-07.md`.
- Books: I searched the HTML of every book, chapter files included, for each paper's number (#n) and DOI, and I read each book's chapter headings, its "Sources by chapter" and its "Papers referred to, not in this book". The books were: book-bonds (DICTONIC Bonds), book-golden-cycle, book-golden-ladder, book-laws-of-stacking (HexOct, local v9 draft with Chapters 17–18), book-queens (Alicia), book-star-cores, book-quanta-of-space and book-quanta-dictonary. book-centre-pyramids has drafts only, and so does `plan-book-platonic-lattices` (a plan of 6 November, "OK in principle" 7 November). The Japanese editions were left out because they are translations.
- Quanta of Space I gives every paper a short catalogue entry. Its chapter "Bonds" ("How pieces fill space together") lists #8–#51. I count those entries as an overview, not as a chapter home, so they create no overlap.
- Studies: `studies/` (224 folders), searched by name for filling, Dehn, interlock, Admiral, tetra sweep, shear, Jewel, Sunstar, rd13, Narcissus, octet, gravel and halo. Render and figure scripts: every `*render*`, `*figure*`, `fig*.py` and `*plate*` file under studies/ and papers/ (about 150).
- Memory: open-work (Centre Pyramids chapters 11-02; #86 belongs with HexOct, 11-02; Space-Fillers approved as a new record 11-07).

## 2. Content survey: papers whose main result is a space-filling

"Home" means the book that holds the paper as a chapter. "Cited" means the book only refers to it. Every DOI below is a DICTO DOI (10.5281/zenodo.…). For the chapter papers I give the concept record.

### 2a. No book holds these yet → chapters of Space-Fillers

| # | Title | DOI | Result | Home now | Recommendation |
|---|---|---|---|---|---|
| 25 | DICTO Spheroid-13 RD | 23332821 | An RD and its 12 face neighbours fill space by translation alone. 8 of the 183 index-13 sublattices of fcc work, and all 8 are turns of one block. DICTO's rounded block keeps the tiling. | none (Quanta entry) | **Chapter** |
| 26 | DICTO ATOM-13×13 | 23333183 | Thirteen polyhedral thirteens side by side: seven periodic ones (RD, Bain RD, Bilinski, skewed RD, hexagonal ED, TO and Jewel blocks) that fill space as blocks, and six golden ones. | none (Quanta entry; Golden Cycle cites) | **Chapter** (with #25). The golden half is told briefly and points to The Golden Cycle |
| 41 | The DICTO Jewel | 23496353 | Exact proof: Jewels and stella octangulas fill space in the rock-salt pattern, 3 : 1 by volume. Jewel volume 3/16. The Jewel-Tetra, Jewel-Octa and Jewel-Rhombi are single solids. | none (Star Cores and Quanta cite) | **Chapter** (see overlap O2) |
| 42 | The DICTO Sunstar | 23497702 | Exact in ℚ(√5): dodecahedra and Dogstars fill space. The Dogstar (volume φ/2) is Hart's stellation #8, credited. | none, although six books cite it | **Chapter** (O2) |
| 17 | Kagome Hulls | 23376317 | In the Stella–Jewel and Sunstar lattices, hull-shaped clusters share pieces corner to corner, as in the kagome and pyrochlore nets. | none (Bonds cites) | **Chapter**, together with #18 (O2) |
| 18 | The DICTO Hexa | 23376320 | Eight overlapping exact Jewels make the Hexa. Hexas and Hexa-Keys fill space as a checkerboard, 5 : 3. No shear makes eight Jewels meet face to face. | none (Bonds cites) | **Chapter**, together with #17 (O2) |
| — | Concordance waiting items 4, 28, 30, 31, 33, 37, 41 and part of 39 | unpublished | The four existing draft chapters: Dehn sweeps, truncated tetrahedra, the Admiral network, interlocking | this draft | **Keep** (Chapters 1, 2, 9, 10) |

### 2b. Held by DICTONIC Bonds Part I "Filling" → overlap O1 (my pick: move them here)

| # | Title | DOI | Result | Home now | Recommendation |
|---|---|---|---|---|---|
| 47 | Every Mix of the Platonic Solids Fills Space | 23551326 | Every one of the 31 non-empty sets of Platonic solids fills space with one kit of seven connectors (P, Q, Q′, Admiral Caps, Dogstar, X, Y). v3: octet and cube slabs stack with no connector, never face to face. | **Bonds Ch. 1** | **Move here** (Ch. 8). The current Ch. 3 (Admiral network) and Ch. 4 (Admiral slab) already rest on it |
| 50 | One Move Each | 23606894 | Classical cut-and-glue space-fillers (Bain RD, elongated dodecahedron type, Bilinski, 60° rhombohedron) are each one setting of Kaleidohedra's three lattice moves. It also holds DICTO's findings F1 (skewed RD), F5 (route to the regular-hexagon ED) and F7 (golden skewed EDs). | **Bonds Ch. 2** | **Move here** (Ch. 3). This paper is the "Lattice Moves" of the title |

The early Kaleidohedra findings #1, #5 and #7 (record 23173809) are housed through #50 and do not count as separate items. #10, #15 and #16 are housed through #41, #18 and #17.

### 2c. Well housed elsewhere → cite only (atlas plate, one line, DICTO DOI)

| # | Title | DOI | Filling result | Home |
|---|---|---|---|---|
| 20 | The FUJI Family | 23357896 (see note N1) | Cleo-Icos with Antonius: a space-filling pair from the golden rhombohedron | Golden Ladder Ch. 3A |
| 48 | The Golden Split | 23596362 | Icosaxes and Unborn Axes: two convex space-fillers at the golden point | Bonds Ch. 3 **and** Golden Ladder Ch. 3B (existing double, O6) |
| 88 | Every Platonic Solid Has Exactly Two Golden Cuts | 23896439 | The octahedron's golden pair is Icosaxes and Unborn Axes, which fill space | Golden Ladder Ch. 4 |
| 89 | All Five Golden Pairs Are Slices of 4D Solids | 23917931 | DICTO's filling by cut cubes and octahedra, a section of the rectified tesseractic honeycomb | Golden Ladder Ch. 6 |
| 51 | The Delian Bond | 23606828 | The octet cut by one sliding plane, from RDs to cubes; Samson and Delilah | Bonds Ch. 4 |
| 52, 53 | The Web of Bonds / Global Web | 23629252 / 23631140 | Tilings as power diagrams with one sliding weight | Bonds Ch. 5–6 |
| 55 | David and Goliath | 23632358 | A15 tiling pair: Goliath = hull of Jessen's icosahedron, David a small tetrahedron | Bonds Ch. 7 |
| 56 | Sonsam and Lahdeli | 23635823 | The Delian bond on the twinned octet | Bonds Ch. 8 |
| 57 | The Rule of Halves | 23647898 | Every close-packed stacking is tiled by pieces borrowed whole or in halves | Bonds Ch. 11 **and** HexOct Ch. 1 (existing double, O6) |
| 75 | HexOct: Two Tiles for Every Stacking | 23737639 | Two layer tiles, c and h, build every stacking | HexOct Ch. 14 |
| 86 | The HexOct Family | 23896076 | The tower move joins the c-tile; five single-solid tile pairs A–E | HexOct cites only. DICTO 11-02: it belongs with HexOct, so it should become a HexOct chapter there |
| 98 | Narcissus and Covenant | 24005929 | Narcissus fills space alone; Covenant is a parallelohedron | HexOct Ch. 16 |
| 97 | Narcissus Keyed | 24005567 | 17 keyed Narcissus copies force a non-periodic stacking | **no chapter anywhere** (HexOct cites it) → O4 |
| 44 | Aristotle's Pyramid | 23529497 | Only the cube's pyramid, or the tetrahedron's with the octahedron's, fill space | Queens Ch. 2 **and** planned Centre Pyramids Ch. 2 (O6) |
| 77 | Face to Face | 23779962 | In face-to-face pyramid tilings the pyramids round each apex make up their whole solid | Queens Ch. 4 |
| 92 | Aristotle's Pyramid in Layers | 23931608 | Face-to-face tilings by the octet's pyramids are exactly the stackings | **no chapter** (HexOct and GL cite it). Decided 11-04: to be folded into #44, i.e. Centre Pyramids → O3 |
| 93 | One Double Pyramid, Two Splits | 23933666 | CsCl and Delian pairs tile one way only; RD centre pyramids tile freely | **no chapter** (HexOct cites it) → O3 |
| 62 | Shadows of the Fourth Dimension | 23687223 | OCT-16 fills space alone | Queens Ch. 5 |
| 36, 37, 37a, 40, 95 | OG gap pieces and OG kits (octet, gyrated octet, every stacking, pentagon cut) | 23451210, 23457016, 23484012, 23490114, 23968270 | Exact space-filling kits around OG, which cannot fill alone | **no chapter** (Quanta entries). The planned OG volume (destinations 11-04, triage item 19) → O5 |
| 96 | Reading the Voids | 23968272 | Exact Dehn obstruction for OG adaptors; nearly golden fills | no chapter; planned OG volume / methods → O5 |
| 8, 99 | EKP Cell; Plato's Five in the Octet | 23284106; 24012439 | Nests inside periodic cells (the octet fills; the nests do not) | planned Platonic Lattices book. Cite |

### 2d. Looked at and left out: main result is not a space-filling

#13 Dodeca-13 and #14 DICTO-Star (finite clusters closed exactly), #30 Fibonacci Spine (a packing), #45 Reuleaux, #49 Stretching Theorem (a sweep, not a tiling; the paper only cites interlocking literature), #59 Icosaxes Hexa (a cluster), #61/#64 Swap Rule, #83 Knitting (a slice), and #87 Vacuus.

Leads that are not ready, kept out of v1: early findings F2, F6 and F9 (Kaleidohedra record only; `studies/2026-10-16-sheared-spacefillers` has exact volumes for F1 and F7 only); #11, the stretched dodecahedron (a K finding with no paper; whether it fills must be checked first); item 39, the golden truncated tetrahedra (census timed out; the list of seven cut vectors stays in Ch. 2 as now); `2026-11-06-octet-gravel` (float, Platonic-lattices thread); triage item 58, the rock-salt pieces (HexOct). The negative result of `2026-11-02-halo-fillers` (no new halo fills) gets at most one line in the appendix as a screen calibration, following the no-negative-fill-tests rule.

## 3. Proposed outline (reading order)

| | Chapter | Sources | What it shows (one line) | Est. pp |
|---|---|---|---|---|
| | **Opening · Bricks, partners, locks and moves** | draft opening, extended | Four ways a solid can belong to a filling: alone, with partners, locked by its neighbours, or carried by a move. Ends with a map of the book and of the series' fillings | 5 |
| **I** | **Alone** | | | |
| 1 | The Dehn test picks out the lone tilers of two sweeps | draft Ch. 1 (items 28, 33) | Dehn zero on the cube–octahedron sweep only at Kelvin's TO and the cube; on CO–RD the edge count leaves only the RD | 6 |
| 2 | Truncated tetrahedra that fill space | draft Ch. 2 (33, 41, 39) | Dehn zero ⇔ cuts sum to one edge ⇔ octet ratio. 13 integer cuts tile as piece + mirror. Conjecture; seven golden cut vectors | 7 |
| 3 | One move each: lattice moves build the classical space-fillers | **#50** (from Bonds Ch. 2) with F1, F5, F7 | Kaleidohedra's three lattice moves give the Bain RD, the ED type, the Bilinski dodecahedron, the 60° rhombohedron, DICTO's skewed RD and the golden skewed EDs exactly | 11 |
| 4 | Blocks of thirteen | **#25** + **#26** (periodic half) | A centre and its 12 neighbours as one tile: the Spheroid-13 RD fills by translation alone (8 of 183 sublattices), and seven periodic thirteens tile as blocks | 10 |
| **II** | **Together** | | | |
| 5 | The DICTO Jewel and the stella octangula | **#41** | Rock-salt filling 3 : 1, proved exactly; the Jewel-Tetra, Jewel-Octa and Jewel-Rhombi | 9 |
| 6 | The Sunstar: dodecahedra and Dogstars | **#42** | Hart's Dogstar proved exactly (φ/2); dodecahedra and Dogstars fill space; the Sunstar clusters | 8 |
| 7 | One level up: Kagome Hulls and the Hexa | **#17** + **#18** | Clusters in both rock-salt lattices share pieces as in kagome and pyrochlore; Hexas and Hexa-Keys fill 5 : 3; no shear joins eight Jewels | 7 |
| 8 | Every mix of the Platonic solids fills space | **#47** (from Bonds Ch. 1) | All 31 mixes with one kit of seven connectors; slabs stack with no connector | 11 |
| 9 | The Admiral Cap network: only the mixture fills | draft Ch. 3 (37, 4) | No kind fills alone (Dehn); at most 8/12 edges match; layered ground states with one free bit per layer | 5 |
| **III** | **Held** | | | |
| 10 | Held by shape alone: interlocking in the octet and Admiral slabs | draft Ch. 4 (30, 31) | Octet (111) layer: octahedra locked, tetrahedra free; the Admiral slab is locked except for its surface pyramids. Points to HexOct Ch. 18 for the HexOct layers | 5 |
| | **Atlas · Every filling in the series at a glance** | cited-only papers of 2c | One plate per filling housed elsewhere: picture, one-line result, DICTO DOI and home book. Same model as Star Cores' "Every shape at a glance" | 14 |
| | Appendix · The three tests and their calibrations | draft appendix | Dehn, the edge-angle count and the interlocking LP, with calibrations (β-tin, Dyskin) | 4 |
| | Sources by chapter · Papers referred to · Index · About the author | | house back matter, as in the other books | 5 |
| | **Total** | | | **≈ 107** |

If DICTO keeps #47 and #50 in Bonds (O1 answered "no"), Chapters 3 and 8 shrink to a short summary page each, the book is about 85 pp, and the "Lattice Moves" half of the title rests on the atlas.

## 4. Overlaps DICTO must decide (one pick each)

- **O1. #47 and #50: Bonds Part I or Space-Fillers?** Bonds' own Part I is titled "Filling", and neither paper is about bonds. **Pick: move both here.** Bonds' next version keeps a one-page pointer in their place, as the OG papers did for #95.
- **O2. #41, #42, #17, #18: Space-Fillers or the planned Platonic Lattices book?** Concordance thread "kepler". The Platonic Lattices plan names EKP #8, #99, the Dodeca-13 and the crossed nest, but not these four. **Pick: Space-Fillers**, because each main result is a filling. Platonic Lattices cites them.
- **O3. #92 and #93: Centre Pyramids or Space-Fillers?** **Pick: Centre Pyramids**, as its Ch. 2 "Aristotle: pyramids that fill space" next to #44 (decided 11-04 for #92). Space-Fillers gives each an atlas plate.
- **O4. #97 Narcissus Keyed: HexOct, the planned one-piece paper, or Space-Fillers?** **Pick: a HexOct chapter right after Ch. 16** (Narcissus and Covenant), with an atlas plate here.
- **O5. OG kits (#36, #37, #37a, #40, #95, #96): the planned OG volume or Space-Fillers?** **Pick: the OG volume.** These are kits around a solid that does not fill (Dehn ≠ 0, #96). Atlas plates here.
- **O6. Doubles already in the published books (not this book's, found by the survey):** #48 is Bonds Ch. 3 and Golden Ladder Ch. 3B; #57 is Bonds Ch. 11 and HexOct Ch. 1; #58 is the Bonds Ch. 10 and the HexOct Prologue; #44 is Queens Ch. 2 and is planned as Centre Pyramids Ch. 2. Each breaks the one-book rule. Space-Fillers only cites them. DICTO decides which home each keeps.
- **O7. Interlocking split.** The Dyskin test is used in Ch. 10 here and in HexOct v9 Ch. 18 "Locked Layers". **Pick:** the method and its calibration live in this book's appendix. HexOct keeps its own tile results and cites the method.

## 5. Figure plan

**House look (from the current scripts):** gold `#d9a520`, violet/purple `#7b4fa8`, blue `#3f7fc4`, and a teal glass for connectors. Light ground for chapter figures and the dark ground `(20,15,11)` of #47's `stack_figure.py` for plates. One piece solid and its neighbours as see-through crystal (about 0.32 opacity, light edges). Helpers and connectors (Admiral Caps, Dogstars, stellas, roofs, X/Y, P/Q) as coloured glass. Every figure carries the corner mark "DICTO · dictospheres.com" (as `mark()` in `studies/2026-11-04-pyramid-tilings/figs.py`) and the gold emblem `papers/dicto-logo.png`, or `studies/2026-11-04-dehn-screen/dicto-mark.png`, where it fits. Run `papers/figcheck.mjs` and look at every figure page before printing. Renders go on compute-host as foreground pilots first (≤ 5 min), with no chains.

**Renderers to reuse:**
- (R1) matplotlib Poly3DCollection with lit faces and a mark: `studies/2026-11-04-dehn-screen/scripts/render_together.py` and `render_rhombo.py`, and `studies/2026-11-04-pyramid-tilings/figs.py`.
- (R2) z-buffer PIL renderer for non-convex pieces: `studies/2026-10-22-platonic-mix-step1/pieces_figure.py` and `stack_figure.py`, `studies/2026-10-23-exact-vs-dissection/render.py`.
- (R3) crisp-edge solid renderer: `studies/2026-11-02-hexoct-connected/scripts/build_render.py` (`View`, `render3d`, `save_img`).
- (R4) sweep geometry by half-space intersection: `studies/2026-11-04-harmonic-fingerprint/scripts/fig_sweeps.py`.
- (R5) web screenshots: `papers/thirteens/fig/shots.mjs`.

| Ch. | Existing figures to reuse | New figures (2–4) | Script / data |
|---|---|---|---|
| Opening | none | **F0** a four-panel plate: Kelvin TO cells (one gold, the rest crystal); Jewel gold with stellas as violet glass; Admiral slab, caps as teal glass; cube block → sheared block | R1, R2; data from the chapters below |
| 1 | none (the studies hold no renders) | **1a** sweep strip octahedron → TO → CO → cube at 9 stations, Dehn-zero members gold, the rest grey glass, with Dehn's ledger plotted below. **1b** CO–RD strip with the stretch 1 ≤ μ ≤ 4/3 shaded, B3 permutohedron and RD marked. **1c** edge-angle count: dihedral wedges round one edge closing to 360° (RD) and failing (B3). **1d** four TO cells, see-through, one solid | R4 + R1; `studies/2026-11-04-rt-pyramids` |
| 2 | none | **2a** the move T ∩ (2(−T)+t): the big inverted tetrahedron slid to 4 positions over the small one, cut piece gold (before/after strip). **2b** a tiling patch, piece gold and mirror violet, exploded along one axis. **2c** gallery of the 13 integer cuts, labelled with cut vectors. **2d** the β-tin tiler (μ = 2), a few cells | R1; `studies/2026-11-04-tetra-sweep/data/tiling-N20.json`, `patch-R8.json`, `tile-tetra.json`, `golden-cuts.json` |
| 3 | `bain-rd.png`, `bilinski.png`, `ed-type.png`, `f7-skewed-eds.png`, `regular-hexagon-ed.png`, `rhombohedron-60.png` (#50 `figures/`) | **3a** the lattice move as a before/after pair: a 3×3×3 cube block and its sheared image, one cell gold, the rest crystal. **3b** move map: the three sliders and where each classical filler sits (2D diagram). **3c** a skewed-RD honeycomb, a few cells exploded | R2 (`exact-vs-dissection/render.py`, its exact data); `studies/2026-10-16-sheared-spacefillers/data/exact-volumes.txt` |
| 4 | #25: `rd13-blocks.png`, `rd13-rounded.png`, `rd13-rounded-open.png`, `centres.png`, `thickness.png`, `free-vs-exact.png`. #26 `fig/`: `rd13-`, `bainrd13-`, `bilinski13-`, `skewedrd13-`, `hexed-`, `to13-`, `jewel13-blocks/closed.png` | **4a** layer-by-layer stack: three layers of Spheroid-13 blocks drawn apart, one block solid. **4b** the index-13 sublattice in fcc, a 2D projection with the √10 block translations. **4c** a one-page gallery of the seven periodic thirteens | `studies/2026-10-13-rd13-block/render.py` (+ `rd13-round-*.json`); R5; R1 |
| 5 | #41 `figures/lattice.jpg`, `clusters.jpg`, `cube-key.jpg` | **5a** exploded rock-salt 2×2×2 block: Jewels gold and solid, stellas violet glass. **5b** carving before/after: Euclid's dodecahedron with the six neighbouring stellas cutting it, then the Jewel. **5c** the Jewel-Tetra, Jewel-Octa and Jewel-Rhombi side by side | R2/R3; `studies/2026-10-20-dicto-jewel/jewel-exact.json`, `cluster-exact.json` |
| 6 | #42 `figures/lattice.jpg`, `chain.jpg`, `clusters.jpg`, `hexa-key.jpg` | **6a** dodecahedra gold, Dogstars as teal glass, a block exploded. **6b** the Dogstar as a cube minus six roofs (before/after). **6c** the Jewel and Sunstar lattices side by side, same view | R2/R3; `studies/2026-10-20-sunstar` |
| 7 | `kagome-hulls/renders/*` (20 cluster renders: rhombo8, octa6, cubocta12/13, cube14, rd33 in Jewel, Sunstar and network forms); `hexa/renders/*` (`C-cube-34`, `parts-A/B`, `network-patch`, `two-cubes`) | **7a** Hexa and Hexa-Key checkerboard, a few cells, one Hexa solid. **7b** a kagome-hull network as a thin see-through slab with shared pieces in gold | R3; `kagome-hulls/data`, `hexa/data` |
| 8 | #47 `figures/connectors.png`, `layer-cake.png`, `seam-cto.png`, `stack-dicto.png` (+ v3 Fig. 5) | **8a** the 31 mixes as small multiples, one slab thumbnail each. **8b** one exploded "all five" slab: Dodeca, Icosa, Cube, Tetra, Octa opaque in their element colours, connectors as glass. **8c** the seven connectors redrawn as glass beside the solids they serve | `studies/2026-10-22-platonic-mix-step1/stack_figure.py`, `pieces_figure.py`, `seam_figure.py`, `mixes3.py` |
| 9 | none | **9a** a Pacioli icosahedron in its octahedron, the six Admiral Caps pulled apart. **9b** two twin turns side by side, matched and unmatched edges coloured (8/12). **9c** a ground-state stack: layers drawn apart, the free bit per layer written as a word | `studies/2026-11-04-network-fingerprint/scripts/build_admiral_octet.py`, `twin_ground_state.py`; R1 |
| 10 | none | **10a** octet (111) slab with octahedra solid gold and one tetrahedron lifted out along its free direction (arrow). **10b** Admiral slab: locked caps and icosahedra solid, the 4 free surface pyramids lifted off. **10c** Dyskin's calibration layer of tetrahedra | `studies/2026-11-04-hopf-interlock/interlock_pieces.py`, `interlock_rot.py`, `admiral-network-pieces.json`; R1 |
| Atlas | Reused from the home papers: `golden-split/figures/fig3-fill.png` (#48); `delian-bond/fig4-delian-fill.png` (#51); `david-goliath/fig1-david-goliath.png` (#55); `keyed-switch/fig1–3` (#56); `two-tiles/stack.png`, `tiles.png` (#75); `hexoct-family/family-plate.png` (#86); `hexoct-narcissus/narcissus-together.png` (#98); `keyed-narcissus/fig1-keyed-narcissus.png` (#97); `aristotles-pyramid/face-pyramids.jpg` (#44); `pyramid-tilings/layer-stacks.png` (#92); `cubic-pairings/bipyramid-cuts.png` (#93); `bull-horns/octet-*.png` (#37); `og-polytypes/stacks.jpg` (#40); `og-pentagons/octet-kit.png` (#95); `golden-bodhi-pyrochlore/slab.jpg` (#36); `reading-the-voids/fig3-room-adaptor.png` (#96); `book-golden-ladder/figures/ch3A/*` (#20), `ch4/*` (#88), `ch6/fig2-sections.png` (#89); OCT-16 from `4d-shadows` (#62) | Only where a source figure lacks the mark or the house look: a re-render with the same script and one solid among crystal neighbours | the source scripts listed in each paper's data line |

About 30 new figures and about 45 reused, so roughly one picture every 1.5 pages.

## 6. Notes

- **N1.** In the Concordance, the DOIs of #19 (23753305), #20 (23754454) and #27 (23752452) are the concept records of Alicia, Quanta of Space and The Golden Cycle (`in_book: true`). Alicia lists #20 under its own record, 10.5281/zenodo.23357896. The atlas should cite 23357896; check this before printing.
- **N2.** The cover is still DICTO's to make ("Cover by DICTO").
- **N3.** The status box of the draft must be updated with the new chapter list once DICTO decides O1–O7. Chapters taken from other books need "ask before chapters-into-book" (DICTO's yes to this proposal covers it).
