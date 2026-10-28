# Keyed HexOct (2026-10-29)

**Idea (DICTO, 2026-10-29):** data prebuilt as HexOct configurations, connections setting the limits, as the basis of a new kind of programming language. Working name: Keyed HexOct ("HexOct Code").

**Conclusion:** keyed HexOct tiles can compute anything (Wang's theorem applies to every layer); keys on the joints between layers alone give only regular languages. Status: first study done; contacts sampled (not exact); counting layer checked exhaustively. Written up as §8 of Chapter 14 of the book HexOct: The Laws of Stacking (2nd ed., draft).

## Results
1. `scripts/contacts.py` (DBB, `out/contacts_*.out`): face contacts of a tile with every tile within two layers, six stackings (ABC 1, AB 0, ABAC 0, ABAC 1, ABABC 2, ABACBC 1) x five weights (-2/5, -1/3, 0, 1/10, 1/4); unmatched face area 0 in every case.
   - In-layer: the four lattice-axis neighbours (+-1,0), (0,+-1) always share faces (area >= 0.28), plus up to four more.
   - Flat range (lambda <= -7/24): exactly one tile above and one below, through the whole joint, area sqrt(3)/2.
   - Interlocking range: four to six tiles above and below.
2. Joint keys only: a column is a string checked tile by tile, so a keyed set accepts a regular language.
3. Axis-face keys (other faces blank): a layer is a Wang tiling of the square grid, so it can compute anything (Wang 1961) and filling is undecidable (Berger 1966, Robinson 1971).
4. `scripts/counter.py` (`out/counter.out`, figure `out/counter.png`): four keyed tiles; windows 3x8, 4x16 and 5x20 each have exactly one filling, and its rows count in binary.

## Prior art (sources checked)
- Wang 1961; Berger 1966; Robinson 1971; Winfree 1998 (DNA tile self-assembly); Cook, Fu & Schweller 2011 (arXiv 0912.0027, 3D temperature-1 assembly simulates Turing machines).
- Sedlbauer (Wang cubes for aperiodic material samples, dspace5.zcu.cz/bitstream/11025/30825/1/Sedlbauer.pdf); Kari et al. (triangular and hexagonal tile self-assembly, csd.uwo.ca/~lkari/pdfs/trihexfin.pdf); bounded Wang tilings, Sci. Rep. 2023 (PMC10039085); Demaine et al. staged assembly.
- Web searches: "three-dimensional polyhedral tiles matching rules computation Wang cubes self-assembly space-filling polyhedra"; "close-packed stacking layers tiles keyed interlocking computation Wang tiles hexagonal".
- DICTO's reference library (7,730 passages, regex "wang til|self-assembl|wang cube"): Smith-Myers-Kaplan-Goodman-Strauss 2023 (aperiodic monotile); Akpanya et al. 2024 (topologically interlocking tetroctahedrille blocks); the rest colloidal self-assembly.
- Found: no use of close-packed stacking layers, or of tiles from their holes, as a medium for computation.

## Open
Keyed sets that use the interlocking joints (4 to 6 tiles above): the stacking as the clock in the interlocking range.
