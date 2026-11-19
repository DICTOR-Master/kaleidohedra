# The numbered main catalogue of the Aequi (20 November 2026)

**Verdict: the 149 Aequi of the seven frame groups are numbered and named: Ih 1–4, Oh 1–4, Td 1–3, Th 1–47, T 1–91, 82 of them Aequi Mosaici. All thirteen settled names (book atoms D179–D191, among them CO-14, TC-10, ORD-20 and IRT-50) come out unchanged under one initials rule.** Sixteen pairs of T dice share initials and face count and are told apart by their group number; the conventions that no settled name fixes are listed below for DICTO.

Source: study 2026-11-19-aequi-complete (data/dice/*.json for the 149 frame-group dice, its 80-digit depths, and its per-die renders made by its scripts/render.py from the refined corners). Definitions as in the paper outline papers/2026-11-20-aequi/outline.md (Definitions; Scope check).

## Rules (DICTO, 20 Nov)

- **Main catalogue:** the 149 Aequi whose faces lie on the axes of one cube and one icosahedron sharing their three 2-fold axes, under the frame groups Ih 4, Oh 4, Td 3, Th 47, T 91 (a T die counts once for its two hands).
- **Numbering:** within each symmetry group, groups in the order Ih, Oh, Td, Th, T. Inside a group:
  1. by m (number of kinds of face);
  2. then by face count N;
  3. then by orbit families in the order C6, O8, RD12, D12, I12, RT24 (each die's sorted list of family ranks, compared word by word; a joined orbit such as C6+RT24/30 counts with both its families);
  4. then by the placement of a split orbit: the orbit whose representative has fewer minus signs comes first, so the half RT24/12 through (φ, 1/φ, 1) comes before the half through (φ, 1/φ, −1).
  
  The study's row number is the last key, but it is never needed: steps 1–4 order all 149.
- **Name:** "Aequus ‹initials›-‹N›, ‹group› ‹number›", for example Aequus CO-14, Oh 1.
- **Aequi Mosaici** (singular Aequus Mosaicus): m ≥ 4. They are marked in the Mosaicus column and on the sheets.
- **D-number:** given where the die is a numbered book atom (D179–D191; D192 and D193 are the GET pieces, not dice).

## The initials convention

Source solids and their initials, written in this order (by face count of the source solid, 4, 6, 8, 12, 12, 20, 30; RD before D):

**T** tetrahedron · **C** cube · **O** octahedron · **RD** rhombic dodecahedron · **D** dodecahedron · **I** icosahedron · **RT** rhombic triacontahedron.

Each face orbit is named by its source solid:

| orbit | initial |
|---|---|
| C6 | C |
| O8 | O |
| O8/4 (one tetrahedron of the octahedron) | T |
| RD12 | RD |
| D12 | D |
| O8+I12/20, or O8 and I12 both present as separate orbits | I (the icosahedron's 20) |
| C6+RT24/30, or C6 and RT24 both present as separate orbits | RT (the triacontahedron's 30) |
| I12 without O8 | I |
| RT24, or a half RT24/12, without the whole of C6 + RT24 | RT |
| O8/4a + O8/4b (both tetrahedra, under T) | O |

The order T, C, O, RD, D, I, RT is fixed by the settled names. TC-10 and CO-14 put the solid with fewer faces first, and RDD-24 puts RD before D. Joining O8 with I12 into I is fixed by D191 RDI-32, where under Th the icosahedron's 20 faces split 8 + 12. Calling O8/4 T is fixed by TC-10, TRD-16 and TD-16.

**Settled names reproduced** (catalogue name, D-number):

| settled | catalogue | | settled | catalogue |
|---|---|---|---|---|
| D179 TC-10 | Aequus TC-10, Td 1 | | D186 OD-20 | Aequus OD-20, Th 3 |
| D180 CO-14 (Lucky 7) | Aequus CO-14, Oh 1 | | D187 RDD-24 | Aequus RDD-24, Th 4 |
| D181 TRD-16 | Aequus TRD-16, Td 2 | | D188 DI-32 | Aequus DI-32, Ih 1 |
| D182 TD-16 | Aequus TD-16, T 1 | | D189 DRT-42 | Aequus DRT-42, Ih 2 |
| D183 CRD-18 | Aequus CRD-18, Oh 2 | | D190 IRT-50 | Aequus IRT-50, Ih 3 |
| D184 CD-18 | Aequus CD-18, Th 1 | | D191 RDI-32 | Aequus RDI-32, Th 17 |
| D185 ORD-20 | Aequus ORD-20, Oh 3 | | | |

Depths agree with the book entries: for example, TC-10 has the cube's faces at 1/0.938159706476 = 1.0659… against the tetrahedron's, and RDI-32 has the 8 at 1.002759… and the 12 at 1.010663… against the rhombic dodecahedron.

## Counts

| group | dice | m=2 | m=3 | m=4 | m=5 | m=6 | m=7 | Mosaici |
|---|---|---|---|---|---|---|---|---|
| Ih | 4 | 3 | 1 | | | | | 0 |
| Oh | 4 | 3 | 1 | | | | | 0 |
| Td | 3 | 2 | 1 | | | | | 0 |
| Th | 47 | 10 | 17 | 14 | 5 | 1 | | 20 |
| T | 91 | 8 | 21 | 28 | 22 | 10 | 2 | 62 |
| all | 149 | 26 | 41 | 42 | 27 | 11 | 2 | 82 |

## Cases for DICTO

The settled names do not fix the following. The rule chosen is the one in the table above. data/convention-cases.md lists every die in each case by name.

1. **The example in the outline.** Its Scope check gives "Aequus CO-14, Oh 2" as an example. Under the stated order (m, then N), CO-14 has the fewest faces in Oh, so it is **Oh 1**. CRD-18 is Oh 2. The outline line should read Oh 1; I have not edited the outline.
2. **RT from C6 and RT24 in separate orbits** (20 dice, Th and T): named RT by analogy with D191's I. An example is Aequus ORT-38, Th 19 (C6 + O8 + RT24). The alternative is to keep C apart (CORT-38).
3. **I12 alone named I** (55 dice) and **RT24 or a half of it alone named RT** (23 + 63 dice). These are 12 of the icosahedron's 20 faces, or 24 or 12 of the triacontahedron's 30. Alone they do not form an icosahedron or a triacontahedron (I12 alone forms a pyritohedron-shaped solid). Under the TC-10 precedent (O8/4 is named T, the solid it forms), they could instead take initials of their own; no names are proposed here.
4. **Both tetrahedra under T named O** (8 dice), for example Aequus ORT-20, T 9 (O8/4a + O8/4b + RT24/12).
5. **Sixteen pairs of T dice share initials and N** (TRT-16, TCRT-22, TRDRT-28, TDRT-28, TIRT-28, TCRDRT-34, TCDRT-34, TCIRT-34, TRDDRT-40, TRDIRT-40, TDIRT-40, TCRDDRT-46, TCRDIRT-46, TCDIRT-46, TRDDIRT-52, TCRDDIRT-58). In each pair the tetrahedron O8/4 sits against one or the other half of RT24, through (φ, 1/φ, 1) or (φ, 1/φ, −1). The group number tells them apart, for example Aequus TRT-16, T 3 and T 4. Otherwise every (initials, N) is unique across the catalogue.
6. **The letters DIRT** appear in 41 names (for example Aequus DIRT-62, Ih 4; Aequus RDDIRT-74, Th 47). This is flagged under the dignified-public-names rule. A separator (D·I·RT) or another order would avoid it, but the settled order fixes D before I before RT.

## Checks (scripts/build_catalogue.py, data/build.log: FINAL ok)

- 149 rows; per group Ih 4, Oh 4, Td 3, Th 47, T 91.
- Numbers run contiguously from 1 in every group.
- All 149 full names are unique.
- Every (initials, N) is unique except the 16 T pairs above, and each of those is told apart by its group number.
- All thirteen settled names D179–D191 are reproduced, each matched to its die by group and orbit set.
- 82 Mosaici; by m: 26, 41, 42, 27, 11, 2, as in the outline.
- The tie key never needs the study row (checked: 0 ties after step 4).
- Sheets (scripts/catalogue_sheets.py, data/sheets.log: FINAL ok): eight sheets, every die with both its pictures.

## Files

- data/catalogue.csv, one row per die. Columns:
  - group, number, name, initials, solids, m, N, mosaicus;
  - hands;
  - orbits, with representative directions;
  - faces by orbit, corners;
  - depths, in orbit order with the first orbit = 1, rounded half-even to 12 decimals from the study's 60-digit values;
  - D (book atom number), study_row;
  - source (file in the source study's data/ folder).
- data/catalogue.md: the same table, for reading.
- data/convention-cases.md: the dice under each case above.
- data/build.log, data/sheets.log: run logs.
- figures/catalogue-Ih.png, catalogue-Oh.png, catalogue-Td.png, catalogue-Th-p1.png, catalogue-Th-p2.png, catalogue-T-p1.png, catalogue-T-p2.png, catalogue-T-p3.png: contact sheets in catalogue order.
  - Each panel shows the solid (orbit tones are labels only) and its Vacuus (slate sloping, sand on a mirror).
  - Each caption gives the catalogue name and number, then m, the D-number, "Mosaicus" and "two hands" where they apply.
- scripts/build_catalogue.py (DICE_DIR OUT_DIR) and scripts/catalogue_sheets.py (catalogue.json, the per-die render folder, the source study's render.py, OUT_DIR). Both were run on a compute host, not on the interface machine.

## DICTO's decisions (20 Nov)

- Names whose initials would spell DIRT are written with dots between the initials, as in the D·I·C·T·O key: for example Aequus D·I·RT-62, Ih 4, and RD·I·RT-48, Th 26. All other names, the settled ones included, are unchanged.
- The cube's 6 and the triacontahedron's other 24, as separate face kinds, are named RT (as the icosahedron's 20 are named I in D191 RDI-32).
- Kept: I12 alone named I; RT24 or a half of it alone named RT; both tetrahedra together under T named O.
- The outline's example is CO-14, Oh 1 (corrected there).

FINAL ok
