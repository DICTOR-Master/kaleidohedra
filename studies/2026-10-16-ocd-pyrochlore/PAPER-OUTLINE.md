DICTO · dictospheres.com

# Paper outline (draft 1, 2026-10-15)

Status: an outline for DICTO to shape, not a draft text. Voice: "we" for joint work, "DICTO" where the idea is his. Pure geometry, every claim labelled exact or float. Prior art from `FABLE-PRIORART.md` and the README prior-art notes.

## Working titles
1. *A Fibonacci spine in a five-fold chorus of Ogdoecontahedron packings*
2. *Five periodic packings, one quasiperiodic axis: hard-core selection of a Fibonacci window*
3. *The Golden Bodhi Pyrochlore: an exact Fibonacci chain at a five-fold junction of polyhedron packings*

## One-sentence claim
When five periodic packings of one icosahedral polyhedron meet around a five-fold axis, the copies that must be removed near the axis form, exactly, the canonical Fibonacci cut-and-project chain. The window is set by a five-fold ring of copies clashing with itself. Beyond a certain height the minimal removal is no longer unique.

## Framing (from the prior art)
- **Present it as** a new exact instance of known ideas: irrational interfaces as 1D quasicrystals (Sutton; Gratias–Thalal), model sets near irrational lines (Baake & Grimm), and windows shaped by hard-core conditions (Katz & Gratias 1993). It is not a new phenomenon.
- **Claim as not found in the sources checked:**
  - (a) the selection happens *along* a five-fold junction line, not across a planar interface;
  - (b) the window comes from a ring's self-clash, with an exact critical distance;
  - (c) the junction is checked exactly for a hard polyhedron;
  - (d) the fork, a tie between two windows.
- **The polyhedron:** the face arrangement is known (cut-down pentakis dodecahedron = dual of L0(D); confirmed exactly), so we claim only the metric solid as unnamed: regular hexagons, kites 117.85° / 68.62° / 55.69°. It is not canonical.

## Sections
1. **Introduction.** Periodic versus quasiperiodic order. Twinned crystals and irrational interfaces (Sutton, Ranganathan et al., Pauling, Prodan et al.). What is new here, in one paragraph.
2. **The solid.** The DICTO Ogdoecontahedron: 20 regular hexagons and 60 kites, 102 vertices, 180 edges. How it arises (DICTO's polar Dharma chain; the dual of the Hecatodihedron). Its face arrangement and prior names; that it is not canonical. Exact coordinates in ℚ(√5).
3. **Five voices.** The five inscribed cubes from the hexagon bonds, and each cube's periodic face-to-face packing (pyrochlore joints). The chorus: five 72° wedges round a five-fold axis, which is the icosahedral irrational twin (Ranganathan et al. 2006). The silencing rule (whole five-fold orbits).
4. **Exactness.** The packing test in ℚ(√5) (copies apart iff some face has n·(X − Y) ≥ 2d). Overlap-free to radius 10: 2756 sites, 385 silenced, 7465 pairs. Golden ring heights, the lemma (m + nφ)·u.
5. **The core is a model set.** One plane through the axis, a rank-2 lattice with axis slope −φ, a window. The canonical singular Fibonacci chain with window [0, L), L² = 64/81 + 128√5/405; the centre copy is a chain point. Gaps L/S = φ, and the word is a factor of the Fibonacci word.
6. **Why that window.** The ring's self-clash. Exact t_c² = 8/9 + 8√5/45, the same for all plane sites. t_c < L, but no lattice point falls between them for |h| < 12.81, so the chain is exact there.
7. **The fork.** At h = 12.81 the core copy overlaps exactly one off-plane copy (h = 13.80, overlap 0.71% of a copy, exact separation 232/81 − 104√5/81). There are two equally minimal choices: pure Fibonacci or the thinned three-gap chain. The chorus's tie-break takes the thinned chain. Discuss this as a degeneracy of minimal silencing, and compare it with edge choice in singular model sets and phason freedom at irrational interfaces.
8. **The seams.** Vacancies along the five wedge boundaries, growing with area. Diffraction peaks at projected reciprocal vectors (float). There is no slab rule. Clearly marked as float and open.
9. **Discussion.** Relation to Katz & Gratias (hard-core windows), to the 1D lattice gas (Sturmian ground states), and to fivelings and disclinations: our axis is not a disclination but a shared irrational line. Limits: finite build, float steps.
10. **Open questions.** Which rule, if any, keeps the spine pure Fibonacci at every height. Whether the seams are model sets. Other polyhedra with an inscribed-cube five-fold chorus.

## Figures (most already rendered)
- The OCD (study renders).
- The five voices, and the chorus sheet.
- The exact chorus at radius 10, and the boundary vacancies.
- The core plane with the window strip (to make: a lattice-and-strip diagram).
- The ring self-clash at t_c (to make).
- The fork: view down the axis and the overlap close-up (`renders/chorus-fork-*.png`).
- Seam diffraction.
- Supplementary movies: the boundary sweep and the fork.

## Before writing
- [x] dL0D face arrangement confirmed (exact map isomorphism, `data/ocd-dl0d.txt`): known type; claim only the metric solid.
- [~] Katz & Gratias 1993 is closed access: read through open restatements only (README). Same spirit (hard-core window edge), different role (chosen vs forced) and different pairs (translations vs five-fold rotated images). Full text still needed before submission.
- [~] Gratias–Thalal 1988 and Sutton 1988/89/92: closed access, abstracts only (README). Sutton 1989 (degenerate interface variants separated by line defects) is the closest precedent for the fork. No junction treatment found. Full texts needed before submission.
- [x] Catalogues: McCooey scanned in full (553 solids, no match; nearest = 6-truncated pentakis dodecahedron); books ruled out by scope, not read; MathWorld PolyhedronData not checked (README).
- [ ] Decide the fork framing: report it as is, or search for a natural rule that keeps the spine Fibonacci.
- [ ] Decide venue and length. Zenodo DOI only with DICTO's OK.

## Must-cite (verified DOIs)
- Sutton 1988, doi:10.1016/0001-6160(88)90281-7; Sutton 1992, doi:10.1016/0079-6425(92)90008-U.
- Ranganathan, Srivastava & Lord 2006, doi:10.1007/s10853-006-0966-y.
- Katz & Gratias 1993, doi:10.1016/0022-3093(93)90340-4.
- Gratias & Thalal 1988, doi:10.1080/09500838808229611.
- Baake & Grimm 2013, doi:10.1017/CBO9781139025256.
- Lee & Glotzer 2022, doi:10.1038/s41467-022-34891-5.
- Prodan et al. 2017, doi:10.1038/s41598-017-12669-w.
- Rivier & Lawrence 1988, doi:10.1016/0378-4363(88)90122-2.
