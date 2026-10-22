# Report for DICTO: math-data dataset (first build 2026-10-22, second pass 2026-10-23)

Created by DICTO · dictospheres.com · CC BY-SA 4.0. Branch `math-data-dataset` (local only, not pushed). Nothing on Zenodo, the
apps, the papers, DISCOVERIES.md or the website was changed.

## Second pass (2026-10-23), DICTO's decisions

- **Status labels confirmed by DICTO 2026-10-23** (see Inventory totals).
- **One name per shape: the first name DICTO chose wins; a shape with an established literature name keeps that name with DICTO's
  beside it (DICTO 2026-10-23).** So Oktaktis (#43) is merged into Cleo-Icos (named first, #29): its index.csv row is deleted and the
  Cleo-Icos row notes "appears in #43 as the OTT's octahedral ray, there called Oktaktis (DICTO DOI: 10.5281/zenodo.23532013)"; its
  Polyhedraverse id OTT_CLEO_ICOS is listed beside ICOSA_FACE_PYRAMID.
- **Non-filling published packings added** (`packings-nonfilling/`): OG on bcc (#31), OCD Stella on bcc (#31a), DBT on the gyrated
  octet and OTT on the octet (#37a). Every density equals its paper exactly: (9225 − 3915√5)/608 = 77.43%, 151/2 − 267√5/8 = 87.12%,
  493/6 − 73√5/2 = 55.02%, 176/3 − 26√5 = 52.89%. **No value disagreed with a paper; none was left out.** The OCD Stella packing
  needed the solid itself, so the DICTO OCD Stella (#31a) is now in `solids/`, built exactly from the planes the paper states (golden
  envelope of inradius 2/3, 20 three-fold planes at squared distance 14/27 − 10√5/243, the bcc Voronoi cell); it matches the paper
  (48 corners, 50 faces 6/24/20, volume (−4064 + 2240√5)/729, pyritohedral; companion C 72 corners, (−18880 + 9760√5)/2187) and the
  study's float corners (corner matching). Choices, from the papers: the OG's bcc packing is the one whose joint hexagons point along
  (±1, ±1, ±1) (one of its five, #31); the OTT is given on the octet (#37a: the same density in every stacking); the DBT on the gyrated
  octet with the next layer as its mirror twin (= the half-turn about (1,1,1), checked exactly).
- **Unit volume as a second common size**: every solid keeps its paper frame and also has `unit_volume` (scale s = V^(−1/3), exact
  symbolic; corners as 15-place decimals) and `solids/<slug>-unit-volume.off`. Centre: the exact corner centroid, which is the paper
  frame's origin for 21 solids; the Dodeca-13 Wedge and Needle are scaled about their corner centroid.
- **Check of Jewel-Tetra / Jewel-Octa (#41) against the F15 clusters** (DJ_TETRAHEDRAL_CLUSTER, DJ_OCTAHEDRAL_CLUSTER, Polyhedraverse
  in kaleidohedra krp-core): **the same solids.** Built from the #41 study's definitions (the Jewel of jewel_exact.py, cells as in
  cluster_exact.py), corner matching up to rotation/reflection and scale: Jewel-Tetra 131 corners ↔ 131 (surface 228 faces both),
  Jewel-Octa 188 corners ↔ 188 (170 surface corners, 288 faces both), max deviation < 1e-15, scale φ/2 (Polyhedraverse's display
  scale), identity rotation; the face sets coincide too. index.csv still lists them as separate rows (not changed, as asked).

## What is in it

- **23 solids**, all exact in ℚ(√5), each with exact corners + 15-digit decimals, faces wound outward, f-vector, symmetry, exact
  volume and edge lengths, normalisation, source and published values:
  - OG family first: DICTO Hecatodihedron (#28), DICTO Ogdoecontahedron (#31), DICTO GTI and FPD (#38), DICTO KRE, PHE, TPP, DPHP,
    TPH, TQH, TQP, TQHD (#39), DICTO Metaxyhexecontahedron (#35a), DICTO Palintriacontahedron (#35b), DBT and OTT (#37a).
  - Then in finding order: DICTO skewed rhombic dodecahedron (F1), skewed ED F16 and F18 (F7), DICTO Jewel (F10/#41), Dodeca-13
    Wedge and Needle (F13).
  - Added 2026-10-23: DICTO OCD Stella (F31a/#31a).
- **3 packings** (published fills): the skewed RD (DICTO FCC) and both skewed EDs, each tiling space by translation.
- **4 packings that do not fill space** (published): OG bcc 77.43%, OCD Stella bcc 87.12%, DBT gyrated octet 55.02%, OTT octet 52.89%.
- **A unit-volume copy of every solid** (JSON key `unit_volume` + `-unit-volume.off`).
- **check.py: 550 checks, 550 passed, 0 failed** (23 solids, 3 fills, 4 non-fills, unit-volume copies; about 2 minutes on dicto-node).
  It also failed, as it should, on corrupted copies (reversed face, moved corner, wrong group order, an extra overlapping piece; and
  on 2026-10-23 a shrunken non-filling lattice, a wrong published percentage, a moved unit-volume corner: 9 checks failed).

## Inventory totals (index.csv)

116 rows: **101 new, 4 rediscovered, 11 known** (Oktaktis merged into Cleo-Icos; the F15 Jewel clusters merged into Jewel-Tetra and Jewel-Octa and the F16 Sunstar clusters into Sunstar-Tetra and Sunstar-Octa, DICTO's choice of the concise #41/#42 names; 2026-10-23). Some rows group several named shapes
(Cleo Towers: 8 pieces; Polar Cleo Towers: 7 + core ray; the four new Reuleaux bodies; DICTO Fill set pieces: 4; dented tetrahedron
L/R; Q and Q′). Counting those one by one: **122 new, 4 rediscovered, 12 known, 138 named shapes in all**. By kind (rows): 36 solids,
47 pieces, 14 clusters, 16 structures, 1 compound, 2 curved bodies. Of the 138, 23 are in this dataset.

Rediscovered: regular-hexagon ED (F5, Grünbaum 2010), Dogstar (Hart 1996, stellation 8), Sunstar Lattice (Hart's honeycomb),
Bodhi seed (partly: Kabai's cluster layer). The status column copies the wording of DISCOVERIES.md and the papers; it makes no new
claim. The labels set from the text, DICTO all-rhombus block and DICTO flattened rhombohedron as "known" (a parallelepiped and a
rhombohedron, parts of F1), Oktaktis as "known" (#43: exactly the Cleo-Icos shape; now merged into the Cleo-Icos row) and Cleo-Icos as
"known shape, DICTO's name", are confirmed by DICTO 2026-10-23.

## Checked against the published papers

Downloaded the latest published PDFs from Zenodo (records listed in `published/records.json`) and compared exactly:
- #28: H has 80 corners, 180 edges, 102 faces (60 triangles, 30 rhombi, 12 pentagons); volume (−365 + 189√5)/4 ≈ 14.4042 (paper: 14.4042).
- #31: OG 102, 180, 80; 60 kites, 20 hexagons; volume (−1000 + 1240√5)/1539; squared edges 2/9 − 2√5/27 and 86/3249 + 2√5/361: all equal.
  The OG built by the #39 construction is the #31 OG scaled (corner-matching test, scale² = 27/8 + 9√5/8), and its volume at that
  size is (525 + 185√5)/57, as #39 states.
- #38: T⁴(ID) = (35 − 15√5)·ID = (10/φ⁴)·ID exactly.
- #39: all eight f-vectors (92/180/90, 180/270/92, 212/390/180, 270/420/152; 80/210/132, 132/270/140, 140/300/162, 162/360/200) and
  the exact volumes of the study's exact_upward/exact_downward.json (the paper's Tables) equal.
- #35a, #35b: closed forms, 32/90/60, volumes 410/27 + 550√5/81 and 50/3 + 50√5/9, both squared edge lengths: equal.
- #37a: DBT (−872 + 440√5)/81, 30/60/32, D3d; OTT (−608 + 320√5)/81, 24 corners, 38 faces, Th: equal.
- #31 (bcc packing) and #31a (OCD Stella and its packing), #37a (DBT on the gyrated octet, OTT on the octet): densities and the OCD
  Stella's values as in the second-pass section above: all equal.
- F1/F7 (archive): volumes φ², φ² + 2, φ³ + ½; face counts: equal. #41: Jewel volume 12 on cells of edge 2 (here 3 + 3√5/2 at
  cell edge φ): equal. #13: wedge φ³/20, needle (45 − 19√5)/600 at edge 1: equal.

**Disagreements with a published paper: none found** in these values. Observation only (not a paper): in DISCOVERIES.md on master the
table rows F30 and F38 have their Credit/Verified/Status/First-recorded cells empty.

## Not in Polyhedraverse (dataset solids)

DICTO GTI, DICTO FPD, DICTO Ogdoecontahedron, DICTO KRE, PHE, TPP, DPHP, TPH, TQH, TQP, TQHD, DICTO Metaxyhexecontahedron, DICTO
Palintriacontahedron, DICTO DBT, DICTO OTT, DICTO OCD Stella (16 of 23). Taken from Polyhedraverse and proved exact: Jewel (DRAGON_JEWEL), Dodeca-13
Wedge and Needle, skewed RD, ED F16, ED F18; the Hecatodihedron (TRANS_DHARMA_80, stored with 6 decimals) was built exactly from #28
and matched to it corner for corner (max deviation 1.7e-5).

## Named, published, but not yet in the dataset (what remains)

- No exact geometry obtained in this pass: DICTO Hexa, Hexa-Key,
  Hexa Jewel (Polyhedraverse floats are approximate, e.g. −0.5000000091; need the study's exact data), Jewel and Sunstar clusters
  (#41, #42), Stretched dodecahedron (F11), Lotus Jewel (F21), FUJI and the 13s pieces (Polyhedraverse stores 7-digit floats), Kion,
  Atraktos, Aetos, Sphen, Sphenion (#29), GBPC and Bull-horns (#36), the #37 kit pieces, Fill set pieces and Mg (#37a), Five-sided
  Vajra, hexagonal Cleo, Monkey Staff B (#38), the #43 towers and the TQ series (TQP-252 … TQP-672; built only in a node pickle).
- #43 rays and Aktis (Triaktis, Tetraktis, Deltoid Aktis, Hex Aktis): tried; Polyhedraverse stores them turned, in coordinates outside
  ℚ(√5), so they need the study's exact frame.
- Packings still to add (published fills): Jewel + stella octangula (F10b/#41), Hexa + Hexa-Key 5 : 3 (F18), dodecahedra + Dogstars
  (#42), the #37/#37a kits, the #47 mixes, Spheroid-13 RD (F25). The checker handles convex pieces only; the non-convex fills need a
  convex split of each piece first.
- Non-filling packings not in the four DICTO named (not added): the OCD Stella crystals with icosahedra or octahedra (#31a), the OG on
  the octet (45.89%, #40), the densest lattice packings found by search (float values only).
- Out of format: the Reuleaux bodies (#45) are curved; the Hecatogdoecontahedron (#34a) is a compound (its two components are here).

## Unpublished names left out of the dataset and the inventory

DICTO Ball set 1 (B1, T1, T2), Tetoktjiru (Oktjiru, Tetjiru), the tetrapod clusters (TETRAPOD_FIVE_TO, TETRAPOD_FOUR_RD), DICTO Hexa
roof, DICTO square-faced block, DICTO leaning hexagonal prism, Pentagonal pocket (CLEO sphere), Kepler Star Diadem (app only), the #46
Mandala of Shells, the swept dodecahedra (#49 draft), the DICTO stretched solids (stretch-studies branch), DICTO Square and DICTO
Seal studies, Heikegani, scutoid pieces.

## Open questions for you

None left from the first build: the status labels are confirmed, the non-filling packings and the unit-volume size are in, and the
Jewel-Tetra/-Octa are the F15 clusters: merged into one row each, keeping the #41 names (DICTO 2026-10-23: "#41 more concise"),
with the F15 names noted. The same for the F16 Sunstar clusters = #42 Sunstar-Tetra/-Octa (corner match, scale φ/2; check script
scratchpad/ss/congruence_sunstar.py; DICTO 2026-10-23: keep the #42 names).
