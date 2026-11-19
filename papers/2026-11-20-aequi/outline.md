# Paper 2 on the Aequi: outline (draft, 20 November 2026)

Title (DICTO, 20 Nov): **Fair Dice — The Aequi**. Subtitle: **Enumerating the Innumerable**.

Split agreed with DICTO (20 Nov): (1) Equanimity with its twelve dice, as it stands; (2) this paper, on the 149 Aequi of the seven frame groups, plus the search with both icosahedron placements (running); (3) a dataset record of all 4553, with data and contact sheets, is-part-of this paper. The prisms belong in the dataset only.

DICTO's question that frames the paper: "How to enumerate the innumerable." Answer: with a rule instead of a list. Theorem A covers every fair die; the list is complete for the frame axes.

## Definitions (DICTO, 20 Nov)

- **Main catalogue:** an Aequus whose faces lie on the symmetry axes of one cube and one icosahedron sharing their three 2-fold axes (the placement of Equanimity and D191), under one of the seven frame groups. Exactly 149, complete.
- **Order inside the main catalogue** (DICTO, 20 Nov: keep all 149): by number of face kinds, two (26), three (41), then the Aequi Mosaici (82); no cap.
- **Related solids:**
  - the 1083 two-icosahedron dice (faces on the axes of the cube and both icosahedra that fit it; study 2026-11-20-aequi-two-placements), a related section of this paper;
  - the 4404 dice below the frame groups, in the dataset record.
- **Aequi Mosaici** (singular Aequus Mosaicus): Aequi with four or more kinds of face (m ≥ 4); a die with two or three kinds is still read as named solids cut together. Main catalogue: 26 (m = 2), 41 (m = 3), 82 Mosaici; two-icosahedron dice: 30, 88, 965 Mosaici.

## Lead theorem (to check before drafting)

**Theorem A (one fair die per set of face directions).** For any finite set of unit face normals n_1..n_N that satisfies Alexandrov's condition for equal masses 4π/N, there is exactly one convex polytope, up to scale about the centre, whose faces have these normals and each subtend the solid angle 4π/N from the centre. If the normals are invariant under a point group G, so is the die; when G fixes only the centre, the centre is the centroid and the die is an Aequus.

*Route.* A ray from the centre in direction u hits face k when k maximises (n_k·u)/d_k. That set of directions is the normal cone of the polar body at its vertex n_k/d_k. So the solid angle of face k is the integral Gauss curvature of the polar at that vertex. Prescribing equal solid angles therefore means prescribing equal integral curvature at given vertex directions. That is Alexandrov's problem, and its existence and uniqueness are Alexandrov's theorem (1942; variational proof Oliker 2007; optimal-transport proof Bertrand 2016; discrete conditions Semenov 2022). Symmetry follows from uniqueness.

*What it explains in the study.*
- Every one of the 6684 orbit sets with one fixed point gave exactly one die.
- The polar groups gave dice fair about the frame centre, but with the centroid elsewhere.
- The 319 polar sets without a solution are to be tested against Alexandrov's condition.

*Credit.* The theorem is Alexandrov's. Ours, not found in the sources checked (search 20 Nov), is reading a fair die as Alexandrov's problem for the polar.

*Alexandrov's condition (read 20 Nov in Bertrand, arXiv:1505.04821, Theorem 1.2; original: A. D. Aleksandrov, Existence and uniqueness of a convex surface with a given integral curvature, C. R. (Dokl.) Acad. Sci. URSS 35 (1942) 131–134).* With σ the uniform probability measure on the sphere: for every nonempty spherical convex set ω ≠ S², μ(ω) < σ(ω_{π/2}), where ω_{π/2} is the set of points within π/2 of ω. Necessary and sufficient. The body is unique up to dilation about the origin. For a fair die, μ puts mass 1/N at each face normal.

*Consequence for the count.* For the 149 no test of the condition is needed. Existence is shown by construction: the die was found and confirmed to 80 digits. Uniqueness is Alexandrov's. So each admissible orbit set carries exactly one die, and the count is exact, not "seen inside a search box".

*Still to do:*
- Check that the 319 polar sets without a solution fail Alexandrov's condition (they should, since the condition is necessary and sufficient).
- Confirm that Bertrand's and Oliker's statements cover the polytope case as used (Oliker's abstract says so).
- Add the four papers to the reference library.

## Arc (beginning, middle, end; one line per section)

1. **Introduction.** The cube is fair by symmetry. Equanimity found twelve dice that are fair with two kinds of face. Fair dice are innumerable; here is the rule that covers them all and the complete list on the axes of the cube and the icosahedron.
2. **The fair die as Alexandrov's problem.** The polar picture, Theorem A and its consequences: existence, uniqueness, symmetry and the centroid.
3. **The frames and the groups.** The 74 axis directions, the seven frame groups and their face orbits; the definition of an Aequus (as in the study).
4. **The count.** 149 Aequi: Ih 4, Oh 4, Td 3, Th 47, T 91 (two hands); O and I none, because their dice always gain mirrors. By m: 26, 41, 42, 27, 11, 2. Theorem A makes the count exact: one die per admissible orbit set, classified by full symmetry.
5. **Both icosahedron placements.** Results of the running search under Th and T.
6. **The pictures.** A solid and a Vacuus for each of the 149; which Vacuus hide a regular polygon (Equanimity Theorem 6) and which turn without a mirror (as D191 does).
7. **Beyond the frames.** One paragraph pointing to the dataset of 4553 below the frame groups. The prisms are noted as known in idea (Diaconis–Keller; Goucher's fair triangular prism).
8. **Claimed here, and known and used; sources checked.**

## Scope check (every shape and result with its home)

| item | home |
|---|---|
| the twelve axis-line dice and their exact values | Equanimity (cited, not repeated) |
| D191 (RD ∩ icosahedron, two depths) | already in the book atoms; here as one of the 149 (cited by number) |
| D179–D193 Aequi in the book atoms | book; this paper cites their numbers |
| the other Aequi of the 149 (and two-placement dice) in the book | own section as a family, not numbered atoms (DICTO, 20 Nov) |
| the 149 frame-group Aequi | this paper |
| the two-placement dice (Th, T) | this paper, §5 (study running) |
| the 4553 below the frame groups, prisms included | dataset record (is-part-of this paper) |
| Theorem A (Alexandrov reading) | this paper, §2 |
| names and numbers for new dice | numbered within each symmetry group (Ih 1–4, Oh 1–4, Td 1–3, Th 1–47, T 1–91 before the two-placement dice), ordered by number of face kinds m, then by face count N; each keeps its name in the settled form (source-solid initials and face count), with the group number as catalogue number, e.g. "Aequus CO-14, Oh 1" (DICTO, 20 Nov). Numbers are assigned once the two-placement search lands, so they are fixed once. |

## Sources so far

- Diaconis and Keller 1989; Rawlins (patent US 11033806); Van Oosterom and Strackee 1983. All as in Equanimity.
- Alexandrov's problem:
  - Oliker, arXiv:math/0701398 (abstract read)
  - Bertrand, arXiv:1505.04821 (not yet read)
  - Semenov, arXiv:2210.16974 (abstract read)
- Checked for dice prior art on 20 Nov (none has these dice or the Alexandrov link):
  - McCooey's catalogue
  - Michon's Numericana page on dice
  - Sherman (loki3)
  - Taniguchi and Uehara, arXiv:1810.12108
  - Irving and Patel
