# Books state only what is right (15 November 2026)

DICTO's rule of 15 November 2026: "as long as what was wrong doesn't go in the book, either described as wrong or right, we need to fix and only quote what is right." His exception, the same day: "unless it is a real turning point for any laws that are subsequently discovered."

Scope: the four unpublished books, read in full (main text, quoted paper sections, captions, tables, status notes, Epilogue, Appendix, the per-chapter checks lines), and the Zenodo description of Space-Fillers. This README is a private record and may name the old error; the books do not.

## Changes

| book | location | old framing | new statement |
|---|---|---|---|
| Space-Fillers | Ch. 1, end "Study:" line | Concordance grid row "CO–RD sweep", column "Dehn", "corrected 4 November 2026" | the grid row and column, with no correction date |
| Space-Fillers | Appendix A, Dehn screen | "A first version, which identified edge lengths in ℚ(√2, √5), failed calibration and was replaced." | sentence removed; the screen as used is described |
| Space-Fillers | Appendix B, exact cover | "A first enumeration of the lattices used wrong off-diagonal ranges ... missed N = 20; it was fixed before any result here." | sentence removed; the calibration (N = 20 and N = 2 found) stands |
| Permutohedron Paradigm | Ch. 7, after Theorem 7.1 (chapters/07-web.html) | "An earlier floating-point count split the 30 congruent slices ... into several apparent types; the exact computation above supersedes it." | "The 30 slices of the first row are congruent, one type, as the exact computation above shows." |
| Permutohedron Paradigm | Epilogue status table, Ch. 13 row | "(i) corrected 13 November" (golden slice periodic along a plane) | "(i) exact in ℚ(φ), 13 November" |
| Permutohedron Paradigm | Appendix checks, Ch. 13 (assemble.py CHECKS 'golden') | "The float slice test of 10 November 2026 is superseded. Theorem 13.2 and the correction to Theorem 13.1 (i): ..." | "Theorem 13.2 and Theorem 13.1 (i): ..." |
| Permutohedron Paradigm | Appendix checks, Ch. 1 and Ch. 4 (CHECKS 'three', 'bonds') | "checked independently on 11 November 2026, all findings fixed" | "checked independently on 11 November 2026" (2 places) |
| Permutohedron Paradigm | Appendix checks, Ch. 15 (CHECKS 'bells') | "proved for every n ... after an independent reader closed one gap" | "proved for every n ... and checked by an independent reader" |
| Permutohedron Paradigm | Ch. 15 (chapters/15-bells.html) | "This corrects a common picture: that an extent is a Hamiltonian cycle on the permutohedron. It is so only when ..." (outside claim, not DICTO's) | "A common picture has an extent as a Hamiltonian cycle on the permutohedron. It is one only when ..." |
| Platonic Solids | Ch. 11, "Claimed, known, open" box (chapters/ch11.html) | "Corrected here: the draft of 11 November said two of the five Euclid cubes, from a floating-point search; it is five." | sentence removed; "all five Euclid cubes of every dodecahedron of the 600-cell" stands in the same box and in §11.3 |
| Brief Geometry plan | Ch. 11 row, claim | "... beside the turn (0.9256148) and not on it; this corrects the grid value in #107." | "... beside the turn (0.9256148) and not on it." |
| Brief Geometry plan | Ch. 11 row, new writing | "the #107 correction is stated once (its version line is DICTO's call)" | "state the exact station μ* = 0.9241387" |
| Brief Geometry plan | Ch. 14 row, new writing | "a correction of a published identification" (Koca, Koca, Al-Ajmi 2011, not DICTO's) | "an exact identification of the projected cell" |

Counts: Space-Fillers 3, Permutohedron Paradigm 7 places (6 rows), Platonic 1, Brief Geometry plan 3. Zenodo description of Space-Fillers: clean, no change.

## Kept

| book | passage | why kept |
|---|---|---|
| Brief Geometry plan | spine paragraph and Coda: "geometry gives laws at the fixed points of its swaps" is false as a universal law (9 of 45 laws at a fixed point) | TURNING POINT: kept. Its failure led to the forced-fixed-point rule (parity, symmetric concavity, extra symmetry) and to the new Kelvin's-cell result (largest wall area, only zero Dehn invariant in the CsCl family). |
| Brief Geometry plan | Ch. 15: "never on" is false in general | TURNING POINT: kept. Led to Theorems A (parity) and B (extra symmetry) of near-but-never-on. |
| Brief Geometry plan | Ch. 12: first test of the at-a-distance proposition negative; "the guess that centrally symmetric shapes fall off faster is false" | TURNING POINT: kept. The test located the far-field orders in the Baumbach–Freyer–Weigert–Winter theorem and gave the coefficient formula c_k. |
| Platonic Solids | Ch. 4: convex open-fans law, then Theorem N for every solid; #87 disc rule beside the ≥3-edge plane rule | Two definitions stated neutrally, not as a correction; Theorem N is told as an extension, not a fix. |
| Platonic Solids | Ch. 3 and #44 §6: Aristotle's regular-tetrahedron claim and Maurolico's correction | History of Aristotle's claim, not DICTO's error. |
| all | true negatives (no member fills space, Admiral Cap pieces do not fill alone, the twin by a (111) mirror fails, open problems) | right statements |
| all | version tags (#47 version 3, #92 Version 2/3 open points closed, "version 2 changes no result"), front status-box revision logs | version history, not error descriptions; status boxes are deleted at publication |
| Space-Fillers | "the proof above replaces" the numerical screen (Ch. 9); earlier numerical checks made exact (#10b, #18); earlier patch searches timed out (Ch. 2) | upgrades of method, nothing stated was wrong |

## Noticed, not changed (outside this rule)

DOI mismatches in quoted references of the Platonic book: #20 as 23754454 and 23357896; #44 as 23529497 and 23529498; #55 as 23632358 and 23632359. #92 §7 numbers its open items (1), (4), (3).

## Builds

Space-Fillers final PDF rebuilt with print.mjs (DOI 10.5281/zenodo.24221378, version 1), FIGCHECK OK. Drafts rebuilt: The Permutohedron Paradigm (110 pp., FIGCHECK OK), The Five Solids (112 pp., FIGCHECK OK), the Brief Geometry plan. Every changed page looked at.
