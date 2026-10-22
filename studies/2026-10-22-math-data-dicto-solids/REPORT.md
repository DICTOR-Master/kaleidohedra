# Report for DICTO: math-data dataset, first build (2026-10-22)

Created by DICTO · dictospheres.com · CC BY-SA 4.0. Branch `math-data-dataset` (local only, not pushed). Nothing on Zenodo, the
apps, the papers, DISCOVERIES.md or the website was changed.

## What is in it

- **22 solids**, all exact in ℚ(√5), each with exact corners + 15-digit decimals, faces wound outward, f-vector, symmetry, exact
  volume and edge lengths, normalisation, source and published values:
  - OG family first: DICTO Hecatodihedron (#28), DICTO Ogdoecontahedron (#31), DICTO GTI and FPD (#38), DICTO KRE, PHE, TPP, DPHP,
    TPH, TQH, TQP, TQHD (#39), DICTO Metaxyhexecontahedron (#35a), DICTO Palintriacontahedron (#35b), DBT and OTT (#37a).
  - Then in finding order: DICTO skewed rhombic dodecahedron (F1), skewed ED F16 and F18 (F7), DICTO Jewel (F10/#41), Dodeca-13
    Wedge and Needle (F13).
- **3 packings** (published fills): the skewed RD (DICTO FCC) and both skewed EDs, each tiling space by translation.
- **check.py: 364 checks, 364 passed, 0 failed** (22 solids, 3 packings; about 1 minute on dicto-node). It also failed, as it should,
  on corrupted copies (reversed face, moved corner, wrong group order, an extra overlapping piece).

## Inventory totals (index.csv)

121 rows: **105 new, 4 rediscovered, 12 known**. Some rows group several named shapes (Cleo Towers: 8 pieces; Polar Cleo Towers:
7 + core ray; the four new Reuleaux bodies; DICTO Fill set pieces: 4; dented tetrahedron L/R; Q and Q′). Counting those one by one:
**126 new, 4 rediscovered, 13 known, 143 named shapes in all**. By kind (rows): 36 solids, 48 pieces, 18 clusters, 16 structures,
1 compound, 2 curved bodies. Of the 143, 22 are in this dataset.

Rediscovered: regular-hexagon ED (F5, Grünbaum 2010), Dogstar (Hart 1996, stellation 8), Sunstar Lattice (Hart's honeycomb),
Bodhi seed (partly: Kabai's cluster layer). The status column copies the wording of DISCOVERIES.md and the papers; it makes no new
claim. Four labels are my reading and need your OK (see open questions).

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
- F1/F7 (archive): volumes φ², φ² + 2, φ³ + ½; face counts: equal. #41: Jewel volume 12 on cells of edge 2 (here 3 + 3√5/2 at
  cell edge φ): equal. #13: wedge φ³/20, needle (45 − 19√5)/600 at edge 1: equal.

**Disagreements with a published paper: none found** in these values. Observation only (not a paper): in DISCOVERIES.md on master the
table rows F30 and F38 have their Credit/Verified/Status/First-recorded cells empty.

## Not in Polyhedraverse (dataset solids)

DICTO GTI, DICTO FPD, DICTO Ogdoecontahedron, DICTO KRE, PHE, TPP, DPHP, TPH, TQH, TQP, TQHD, DICTO Metaxyhexecontahedron, DICTO
Palintriacontahedron, DICTO DBT, DICTO OTT (15 of 22). Taken from Polyhedraverse and proved exact: Jewel (DRAGON_JEWEL), Dodeca-13
Wedge and Needle, skewed RD, ED F16, ED F18; the Hecatodihedron (TRANS_DHARMA_80, stored with 6 decimals) was built exactly from #28
and matched to it corner for corner (max deviation 1.7e-5).

## Named, published, but not yet in the dataset (what remains)

- No exact geometry obtained in this pass: DICTO OCD Stella (#31a; needs the GBPC adapter hull of the bcc packing), DICTO Hexa, Hexa-Key,
  Hexa Jewel (Polyhedraverse floats are approximate, e.g. −0.5000000091; need the study's exact data), Jewel and Sunstar clusters
  (#41, #42), Stretched dodecahedron (F11), Lotus Jewel (F21), FUJI and the 13s pieces (Polyhedraverse stores 7-digit floats), Kion,
  Atraktos, Aetos, Sphen, Sphenion (#29), GBPC and Bull-horns (#36), the #37 kit pieces, Fill set pieces and Mg (#37a), Five-sided
  Vajra, hexagonal Cleo, Monkey Staff B (#38), the #43 towers and the TQ series (TQP-252 … TQP-672; built only in a node pickle).
- #43 rays and Aktis (Triaktis, Tetraktis, Deltoid Aktis, Hex Aktis): tried; Polyhedraverse stores them turned, in coordinates outside
  ℚ(√5), so they need the study's exact frame.
- Packings still to add (published fills): Jewel + stella octangula (F10b/#41), Hexa + Hexa-Key 5 : 3 (F18), dodecahedra + Dogstars
  (#42), the #37/#37a kits, OCD Stella crystals (#31a), the #47 mixes, Spheroid-13 RD (F25). The checker handles convex pieces only;
  the non-convex fills need a convex split of each piece first.
- Out of format: the Reuleaux bodies (#45) are curved; the Hecatogdoecontahedron (#34a) is a compound (its two components are here).

## Unpublished names left out of the dataset and the inventory

DICTO Ball set 1 (B1, T1, T2), Tetoktjiru (Oktjiru, Tetjiru), the tetrapod clusters (TETRAPOD_FIVE_TO, TETRAPOD_FOUR_RD), DICTO Hexa
roof, DICTO square-faced block, DICTO leaning hexagonal prism, Pentagonal pocket (CLEO sphere), Kepler Star Diadem (app only), the #46
Mandala of Shells, the swept dodecahedra (#49 draft), the DICTO stretched solids (stretch-studies branch), DICTO Square and DICTO
Seal studies, Heikegani, scutoid pieces.

## Open questions for you

1. Status labels I set from the text, please confirm: DICTO all-rhombus block and DICTO flattened rhombohedron as "known" (they are a
   parallelepiped and a rhombohedron, parts of F1); Oktaktis as "known" (#43 says it is exactly the Cleo-Icos shape); Cleo-Icos as
   "known shape, DICTO's name".
2. Jewel-Tetra/-Octa (#41) and the F15 Jewel clusters are listed separately; I did not test whether they are the same solids.
3. Should non-filling published packings go in too (OG bcc 77.43%, OCD Stella 87.12%, DBT 55.02%, OTT 52.89%)? Left out, as the
   agreed scope says fills.
4. Each solid is in its own paper's frame. Do you want a second, common normalisation (e.g. unit edge or unit volume) as well?
