# #112 Fair Dice — The Aequi, Version 2: arc and scope (25 November 2026)

DICTO · plan for the next version of paper #112 (Version 1: 20 November 2026, DICTO DOI 10.5281/zenodo.24383314). Decisions 1–11 agreed by DICTO on 25 November ("proceed").

> **Status box.** Plan only; nothing drafted or published. Every number below is read from the data (picker data of 25 November: 10 725 dice) or from the study named beside it.

## The claim the version leads with

**The catalogue of 10 725 Aequi.** Every fair die whose faces lie on the 122 frame directions (the symmetry axes of one cube and both icosahedra that fit it), with the symmetry groups and face-kind limits stated in §4, is listed, numbered and named; each one is rigorously certified (exactly one fair set of depths in a proved box, the 60-digit depths within 5·10⁻⁶⁰ of it).

## Arc (one line per section)

1. **Introduction.** The cube is fair by symmetry; Diaconis and Keller showed a die can also be fair by continuity; Version 1 gave the rule (Theorem A) and 149 dice; this version gives the full catalogue of 10 725, certified.
2. **The fair die as Alexandrov's problem.** Theorem A as in Version 1, now machine-checked in Lean (#121), and Theorem B: every set of N ≥ 4 face directions summing to zero, not all on one great circle, carries a fair die.
3. **Frames, groups and the Aequi.** The 122 frame directions, the groups searched (the frame groups Ih, Oh, O, Td, Th and T, and 13 smaller groups, D6h to D2), and what an Aequus is.
4. **The catalogue.** 10 725 dice: 1232 (Version 1 and the two-placement dice), 3 Aequi Permutahedra (Nos. 1233–1235), 9490 of catalogue 2 (Nos. 1236–10725); the exact scope of each search and its limits; counts by group and by kinds of face (m = 1: 3, m = 2: 1088, m = 3: 4328, m = 4: 913, m = 5: 3228, m = 6: 773, m = 7: 227, m = 8: 113, m = 9: 41, m = 10: 10, m = 11: 1).
5. **Certification.** Ball arithmetic: the method, the boxes, and the result for every die; the repeats removed (66).
6. **Exact dice.** The shadow-dice theorem (faces projecting onto unions of mirror triangles) and the die with two face kinds at exactly the same depth, both proved exactly.
7. **Designations.** The Aequi Diaconis–Keller (all 1088 dice with two kinds of face, in tribute to Persi Diaconis and Joseph B. Keller; the tribute is ours), the Aequi Permutahedra (fair by symmetry; rolling face to face walks the mirrors), fair by symmetry (m = 1).
8. **The Non-Periodic Table of the Aequi.** One full-width figure: symmetry group by kinds of face, counts and thumbnails, all 10 725.
9. **Names.** Goroawase names read from each number, written "Name #N", with a hyphen after the second syllable from four syllables on (Ini-mimu #1236, Io-nanigo #10725); the picker as the public record of every die.
   **Widened 27 Nov (DICTO: "enumerating the innumerable should include how we made it possible to access 6.8 quadrillion shapes"; "and naming them ... any one"):** section 9 becomes *Every die reached*: one die per choice (Theorem A); a number for every choice computed both ways (set rank, after No. 10 725); a name for every number (the syllable rule and the poem forms Kamigo, Nakashichi, Shimo-no-ku, Haiku); built on demand in the picker; the count per group (6 773 000 493 470 481 possible) kept apart from the proved.
10. **Claimed here, known and used, sources checked.** As in Version 1, extended.
11. **Contributions.** The list of what the version gives.

## Scope check: every result with its home

| item | home |
|---|---|
| catalogue of 10 725, certification, designations, table, names | **this version** |
| Theorem B (existence), exact dice Theorems 1 and 2 | **this version** |
| Theorem A (a) and the polar identity in Lean | #121 (cited) |
| Vacuus kinds of the Aequi (heart, inherited heart, non-heart), quality overlaps | V SF A paper |
| station dice (Theorem 8), polar of an Aequus | stellation and inversions papers |
| Aequi with the five cube placements (10 760, being checked) | a later version |
| the twelve axis-line dice | Equanimity (cited) |

## Next steps

1. Draft from Version 1 (same sections kept where unchanged).
2. Figures: the Non-Periodic Table for all 10 725; a row of example dice from the new groups (house renderer, #118 v2 standard).
3. Data on the Zenodo record: catalogue.csv, every die's depths to 60 digits, the certificates.
4. Draft to DICTO's reading folder; release only on "#112 read ok".
