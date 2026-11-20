# The numbered catalogue of the Seraphim (20 November 2026)

**Verdict: the 1083 two-icosahedron fair dice are numbered and named: Oh 1–53, O 1–31, Td 1–91, Th 1–168, T 1–740, 965 of them Seraphim Mosaici.** The Aequi rules carry over unchanged; the one new rule marks the solids of the second icosahedron placement with a prime. 622 dice share initials and face count with another die and are told apart by their group number. The conventions that no earlier decision fixes are listed below for DICTO.

Name (DICTO, 20 Nov): these dice are the **Seraphim** (one: a **Seraph**), "multi-faced angels". A Seraph with four or more kinds of face is a **Seraph Mosaicus**, plural **Seraphim Mosaici**.

Source: study 2026-11-20-aequi-two-placements (data/dice/*.json for the 1083 dice, depths to 60 digits; its per-die renders, made by its scripts/render.py from the 80-digit corners). Made like the Aequi catalogue (study 2026-11-20-aequi-catalogue: its rules and DICTO's decisions of 20 Nov).

## What the Seraphim are

The Seraphim are fair dice in the solid-angle model: every one of the N faces subtends 4π/N from the centre. Their faces lie on the symmetry axes of a cube and of both icosahedra that fit it with their 2-fold axes on the cube's axes. The two icosahedra (placements A and B) are a quarter turn apart about a cube axis. Every Seraph uses directions of both placements. They were first given in #112 Fair Dice — The Aequi (DICTO DOI: 10.5281/zenodo.24383314), §5.

## Rules

- **Catalogue:** all 1083 dice of the source study, under their full symmetry groups Oh 53, O 31, Td 91, Th 168, T 740. A chiral die (O and T) counts once for its two hands.
- **Numbering:** within each symmetry group, groups in the order Oh, O, Td, Th, T. Inside a group:
  1. by m (number of kinds of face);
  2. then by face count N;
  3. then by orbit families in the order C6, O8, RD12, D12, D12′, I12, I12′, RT24, RT24′. Each die's sorted list of family ranks is compared word by word; an orbit joining the placements, such as D12+D12′/24, counts with both its families;
  4. then by the placement of a split orbit: the orbit whose representative has fewer minus signs comes first. For example, Td 3 (O8/4 + RT24+RT24′/24 through (φ, 1, 1/φ)) comes before Td 4 (the same through (φ, 1, −1/φ)).

  The study's row number is the last key, but it is never needed: steps 1–4 order all 1083 (0 ties).
- **Name:** "Seraph ‹initials›-‹N›, ‹group› ‹number›", for example Seraph CDD′-30, Oh 1.
- **Seraphim Mosaici** (singular Seraph Mosaicus): m ≥ 4. They are marked in the mosaicus column and on the sheets.
- **Two hands:** marked in the hands column and on the sheets, for all O and T dice (771).

## The initials convention

As in the Aequi catalogue, each face orbit is named by its source solid:

**T** tetrahedron · **C** cube · **O** octahedron · **RD** rhombic dodecahedron · **D** dodecahedron · **I** icosahedron · **RT** rhombic triacontahedron.

The new rule is the **prime.** Solids on the axes of the second icosahedron placement (B: D12′ (0, ±1, ±φ), I12′ (0, ±φ, ±1/φ), RT24′ (±φ, ±1, ±1/φ), all cyclic) are written **D′, I′, RT′**. Each primed initial follows its unprimed one, so the order is T, C, O, RD, D, D′, I, I′, RT, RT′. The cube, octahedron and rhombic dodecahedron are the same for both placements, so they take no prime.

**Which placement is primed.** A quarter turn swaps the two placements, so a die could be read with either one as B. The name uses the position in which the first solid, in initials order, that lies on one placement only is unprimed. Examples are Seraph DI′-24, Th 1 (not D′I) and Seraph IRT′-36, Th 3. The source study's stored position is that one for all 1083 dice, so the orbit labels in the table match the names.

| orbit | initial |
|---|---|
| C6 | C |
| O8 | O |
| O8/4 (one tetrahedron of the octahedron) | T |
| O8/4a + O8/4b (both tetrahedra, under T) | O |
| RD12 | RD |
| D12, D12′ | D, D′ |
| O8 and I12 (or I12′) both present | I (or I′): the icosahedron's 20 |
| C6 and RT24 (or RT24′) both present | RT (or RT′): the triacontahedron's 30 |
| I12 or I12′ without O8 | I or I′ |
| RT24, RT24′ or a half of either, without the whole of C6 + that RT24 | RT or RT′ |
| an orbit joining the placements: D12+D12′/24, I12+I12′/24, RT24+RT24′/48 or /24 | both initials: DD′, II′, RTRT′ |

The 8 octahedron directions belong to both icosahedra. When both are complete, they are absorbed into both: O8 + I12 + I12′ is II′. Likewise the 6 cube directions belong to both triacontahedra: C6 + RT24+RT24′/48 is RTRT′ (Seraph RTRT′-54, Oh 8).

**Dots.** Where the initials, primes aside, would spell DIRT, every initial is separated by a dot, as DICTO decided for the Aequi. Examples are Seraph D·I′·RT-48, Th 17 and Seraph RD·D·D′·I·RT·RT′-102, Th 162. This applies to 420 names; all other names are written without dots.

## Counts

| group | dice | m=2 | m=3 | m=4 | m=5 | m=6 | m=7 | m=8 | m=9 | m=10 | m=11 | Mosaici |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oh | 53 | 12 | 19 | 15 | 6 | 1 | | | | | | 22 |
| O | 31 | 5 | 10 | 10 | 5 | 1 | | | | | | 16 |
| Td | 91 | 8 | 21 | 28 | 22 | 10 | 2 | | | | | 62 |
| Th | 168 | 3 | 18 | 42 | 51 | 36 | 15 | 3 | | | | 147 |
| T | 740 | 2 | 20 | 72 | 144 | 186 | 164 | 100 | 41 | 10 | 1 | 718 |
| all | 1083 | 30 | 88 | 167 | 228 | 234 | 181 | 103 | 41 | 10 | 1 | 965 |

The one die with m = 11 is Seraph RDDD′II′RTRT′-110, T 740.

## Cases for DICTO

The Aequi decisions do not fix the following. The rule chosen is the one above. data/convention-cases.md lists every die in each case by name.

1. **The prime and its place.** D′, I′, RT′ for the second placement, each written right after its unprimed initial (for example DD′II′). The alternative is to write all of placement A and then all of placement B (for example DIRTD′I′RT′).
2. **Which placement is primed:** the first one-placement solid is unprimed, as above (affects only Th and T dice; 0 dice needed turning from the study's position).
3. **Joined orbits named by both initials** (175 dice). D12+D12′/24 is the 24 orbit of (φ, 1, 0) under Oh: half of it lies on each dodecahedron, and it is written DD′. Examples are Seraph CDD′-30, Oh 1 and Seraph II′-32, Oh 4.
4. **The shared 8 and 6:** O8 is absorbed into both complete icosahedra (96 dice, for example Seraph II′-32, Oh 4), and C6 into both complete triacontahedra (60 dice, for example Seraph RTRT′-54, Oh 8).
5. **Shared initials and N** (255 names, 622 dice). These dice are told apart by their group number: 191 pairs, 16 triples and 48 quadruples. Under T, a quadruple is typically one tetrahedron set against one or the other half of RT24 and of RT24′, for example Seraph TDRTRT′-40, T 47 to T 50. 47 names are shared across groups: 31 by an O die and a Td die, for example Seraph CRTRT′-30, O 1 and Td 5, and 16 by a Td die and a T die. The O die carries a chiral 24 of RT24 + RT24′; the Td die carries a mirror-symmetric 24.
6. **Other words.** The only words that occur besides DIRT are ODD (14 names, for example Seraph ODD′-32, Oh 3), CORD (9) and COD (7), with primes aside. The Aequi kept CORD and COD without dots, so these are left as they are here. In ODD′ the prime falls on the last letter.

## Checks (scripts/build_catalogue.py, data/build.log: FINAL ok)

- 1083 rows; per group Oh 53, O 31, Td 91, Th 168, T 740.
- Numbers run contiguously from 1 in every group.
- All 1083 full names are unique.
- By m: 30, 88, 167, 228, 234, 181, 103, 41, 10, 1, as in the source study; 965 Mosaici.
- Two hands exactly for the O and T dice (771).
- The tie key never needs the study row (0 ties after step 4).
- The study's stored position is the named one for all 1083 dice.
- Sheets (scripts/catalogue_sheets.py, data/sheets.log: FINAL ok): 30 sheets, 40 dice a sheet, every die with both its pictures.
- Both scripts were run on a compute host, not on the interface machine.

## Files

- data/catalogue.csv, one row per die. Columns:
  - group, number, name, initials, solids, m, N, mosaicus;
  - hands;
  - named_turned (always no);
  - orbits, with representative directions;
  - faces by orbit, corners;
  - depths, in orbit order with the first orbit = 1, rounded half-even to 12 decimals from the study's 60-digit values;
  - study_row;
  - source (file in the source study's data/ folder).
- data/catalogue.md: the same table, for reading.
- data/convention-cases.md: the dice under cases 3, 4 and 2 above.
- data/build.log, data/sheets.log: run logs.
- figures/: contact sheets in catalogue order:
  - catalogue-Oh-p1..p2.png
  - catalogue-O.png
  - catalogue-Td-p1..p3.png
  - catalogue-Th-p1..p5.png
  - catalogue-T-p1..p19.png

  Each panel shows the solid (orbit tones are labels only) and its Vacuus (slate sloping, sand on a mirror). Each caption gives the catalogue name and number, then m, "Mosaicus" and "two hands" where they apply.
- scripts/build_catalogue.py (DICE_DIR OUT_DIR [WORD_LIST]) and scripts/catalogue_sheets.py (catalogue.json, the per-die render folder, the source study's render.py, OUT_DIR).

FINAL ok
