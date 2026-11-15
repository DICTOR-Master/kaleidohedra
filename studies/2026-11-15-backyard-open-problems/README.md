# Open problems in DICTO's own back yard: scoping and pilots (15 November 2026)

**Verdict: the order and the first job.**

1. **Grünbaum's zone question at k = 10** (rhombic monohedral parallelohedra). This fits DICTO's golden-rhombus work best, and the proof would be constructive.
   - The pilot's method reproduces Grünbaum's own k = 8 examples (the doubly indented icosahedra D1 and D2).
   - Depth ≤ 2 from the triacontahedron finds 29 sphere-like candidates with every zone of 10 faces. None tiles by translation.
   - **First job to run:** `byzone-deep`, the same search on the six icosahedral axes, taken deeper with two changes: only moves that keep the face count at 30, and Grünbaum's condition that adjacent faces are not coplanar. Every hit is then re-checked exactly in Q(√5).
2. **The 40 sporadic rational tetrahedra** (Chentouf–Sun). The pilot already settles one part of this:
   - **2 of the 40 are classical tilers.** Sommerville's fig. 8 tetrahedron is the B̃3 Coxeter simplex, and Sommerville's fig. 9 tetrahedron is a member of Goldberg's second family.
   - **The other 38 have no face-to-face tiling.** This uses the edge-length-graph test of Bongiovanni et al. Their edge-length ties are numerical so far.
   - So the open question is now only about **non-face-to-face** tilings of those 38.
3. **Goldberg's pentahedra, the pyramid part.** Start with the right pyramids over a rectangle, a two-parameter family. Its square slice is Duval's theorem. The pilot's Dehn screen of 106 square-base pyramids found Dehn zero only at the two controls.

**Blind Palomar pre-scores** (one fresh agent, given only PalomarPolicy @ 28bd48b and `blind/inputs/B-backyard.md`):

| Statement | Notability / literature |
|---|---|
| T1: all 40 tetrahedra decided | **4 / 4** |
| G1: an explicit k = 10 example | **4 / 3** |
| P1: square-base pyramids classified | **4 / 3** |
| P2: right rectangle pyramids classified | **4 / 4** |
| T2: a partial answer for the tetrahedra | 3 / 3 |
| G2: no example among 30-face golden solids | 3 / 3 |

The partial and negative forms fall below the floor. Only complete answers clear it.

**Status:** desk study plus three pilots on the compute host, each under 1 minute, all with FINAL ok. No full run was started, nothing is left running, and nothing was submitted.

---

## (a) Which of the 40 sporadic rational tetrahedra tile space?

**Statement.** Chentouf and Sun, "Tetrahedra tiling problem", arXiv:2312.01654 v1 (4 Dec 2023), Theorem 1.2 (p. 2): the sporadic tetrahedra that tile form a subset of a set A of 40. In §1.1 they write: "The goal of this paper, not fully attained, is to determine which rational tetrahedra tile space."
- The 59 sporadic tetrahedra come from Kedlaya, Kolpakov, Poonen and Rubinstein (arXiv:2011.14232, Table 3).
- The question is older: Senechal, "Which tetrahedra fill space?", Math. Mag. 54 (1981) 227–243.
- "Tile" means congruent copies, mirror images allowed, not necessarily face to face.

**Source discrepancy (checked).** The printed set A on p. 2 has **42** entries. It includes (3/20, 11/20, 11/20, 1/4, 1/3, 2/3) and (11/60, 31/60, 11/20, 1/4, 3/10, 7/10), which §3.1 says Corollary 2.13 (an LP test) rules out. The authors' code list `L` (Y. Sun, criteria.py, github.com/KimiSun18/TetrahedraUROP @ d30c9ab) has the correct 40. We use that list as data. The repository has no licence, so no code was copied.

**What has been done since.**
- No paper after 2023 answers it. We checked all OpenAlex citers of KKPR and of Senechal 1981, and web searches; the abstract of the companion paper arXiv:2312.01282 does not concern tilings.
- Bongiovanni, Diaz, Kakkar and Sothanaphan, "The least-area tetrahedral tile of space" (Geom. Dedicata 2019; arXiv:1709.04139, read §§1–6) is **not cited by Chentouf–Sun**, but it bears directly on this question:
  - it gives a complete review of the known tilers (§3: Sommerville Nos. 1–4, Edmonds's (xi), Goldberg's three families with their dihedral angles, Baumgartner's T2);
  - its edge-length graphs (Prop. 4.3) give a face-to-face obstruction that is stronger than Chentouf–Sun's Prop. 2.7.
- Edmonds, "Sommerville's missing tetrahedra", DCG 37 (2007): Sommerville's list of orientation-preserving face-to-face tilers is complete. We know this paper only through Bongiovanni et al. and the blind reviewer; it is paywalled and was not bought.

**Dehn cannot decide this question.** Every rational tetrahedron has Dehn invariant zero, because all its angles lie in ℚπ. Chentouf–Sun say so in §1.1. So the suggested pilot "Dehn ≠ 0 rules one out" cannot rule out any of the 40. We ran #100's Dehn screen on all 40 only as a control of the tool: all zero, as they must be. (Dehn 1901; Debrunner 1980: every tiler has Dehn zero.)

**Pilot `bytetra-pilot2`** (`scripts/tetra_pilot.py`, 18 s, FINAL ok; data `data/tetra-pilot.json`):
- Geometry from the angles: the Gram matrix of the outward normals, solved at 60 digits. The angles re-measured from the vertices agree with the input to better than 1e-40.
- Known tilers built from coordinates: Sommerville 1923 figs 7–10 (read in full), Goldberg's three families (the first as Sommerville's prism thirds; the second and third as its halves through the 2-fold axis, as in Goldberg, JCTA 17 (1974) p. 375), and Edmonds's (xi).

| Class | Count | Which |
|---|---|---|
| Known tiler | **2** | #3 (1/4, 1/2, 1/2, 1/3, 1/3, 1/2) = Sommerville fig. 8 = the B̃3 Coxeter simplex (tiles by reflections). #1 (1/4, 1/3, 1/3, 1/4, 1/2, 2/3) = Sommerville fig. 9 = Goldberg's second/third-family half at a = 1/√3 |
| No face-to-face tiling (Bongiovanni et al. Prop. 4.3); non-face-to-face open | **38** | All the rest. For each, some node of some edge-length graph has no closed walk with angle sum 2π |
| Non-face-to-face excluded (Chentouf–Sun Prop. 2.3) | 0 | Every one of the 40 has a π-combination |
| Chentouf–Sun LP (Cor. 2.13, recomputed) | 0 negative | Agrees with their paper |

The blind reviewer also identified the B̃3 simplex independently.

**What closing needs, and what DICTO's tools do.**
1. **Make the face-to-face exclusion exact.** Prove each edge-length tie (or distinctness) in the cyclotomic field. The lengths are algebraic, so their minimal polynomials can be compared. The rest of the edge-length-graph test is already exact rational arithmetic.
2. **Non-face-to-face tilings of the 38.** In such a tiling an edge lies inside a face, and around it the dihedral angles sum to π. The finite search is DICTO's reversed-neighbour corona search (#92 v3, the forced-neighbour proof):
   - start from the π-combinations along a face;
   - add the lengths, which must fit along the line, and the face shapes, which must fit in the plane;
   - every forced branch either dies, giving a certified obstruction, or closes into a periodic patch, giving a tiling certificate that #100's exact-cover checker (Thm 2.4) verifies on a torus.

   Many of the 38 have π/5 angles (DICTO's icosahedral territory). Any tiler among them must tile non-face-to-face.
3. **Outcome classes:**
   - a full answer, "exactly m tile";
   - a partial answer that names the remaining cases;
   - the reformulation already in hand: "2 tile; the other 38 can only tile non-face-to-face". The blind score for that partial form is 3.

**Lean.**
- The positive cases are classical.
- The obstructions need a formal notion of tiling plus the corona case tree. That is large; the statement alone would take 300–600 lines.
- There is no Dehn invariant in Mathlib, but it is not needed here.

## (b) Grünbaum: rhombic monohedral parallelohedron with every zone of k faces, k ≥ 10

**Statement.** Grünbaum, "The Bilinski dodecahedron, and assorted parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra", Math. Intelligencer 32(4) (2010) 5–15. The author's version 2/3/10, p. 17 (library copy) reads: "Given an even integer k ≥ 4, is there a rhombic monohedral parallelohedron such that every zone has exactly k faces? … No information is available for any k ≥ 10."
- The cube has k = 4, the rhombic dodecahedra K and B have k = 6, and the doubly indented icosahedra D1 and D2 have k = 8.
- Grünbaum's polyhedra are sphere-like with adjacent faces not coplanar (p. 9; blind reviewer's finding). The pilot does not yet impose the coplanarity condition, so the full run adds it.

**What has been done since.**
- No paper answers it. We checked all OpenAlex citers of the paper, including Hungerbühler–Hungerbühler–Pirron, J. Math. Arts 2025 ("New families of monohedral polyhedra"; abstract read, no parallelohedra), and Grünbaum's Supplement (checked in the earlier study).
- Senechal–Taylor, "Parallelohedra, old and new", Acta Cryst. A 79 (2023) 273–279: three new nonconvex parallelohedra, "a counterexample to a statement by Grünbaum". We read only the abstract (closed access, not bought). Which statement it refutes, and whether any of the three has congruent rhombic faces, is unchecked. The free route is a library copy.

**Why k = 10 is DICTO's ground.**
- Any two of the six 5-fold axes of the icosahedron span the same golden rhombus. So every solid built from golden rhombohedra on these axes is monohedral.
- The six axes are the largest set of equiangular lines in ℝ³.
- On n of these axes, with every pair of zones crossing twice, every zone has k = 2(n − 1) faces:
  - n = 4 gives k = 6 (Bilinski);
  - n = 5 gives k = 8 (rhombic icosahedron; D1 and D2);
  - n = 6 gives k = 10, with 30 faces, around the rhombic triacontahedron, which does not tile.
- k ≥ 12 would need seven equiangular directions, which do not exist. So k ≥ 12 needs another structure, such as zones crossing more than twice.

**Pilot `byzone-pilot`** (`scripts/zone_pilot.py`, 59 s, FINAL ok; data `data/zone-pilot.json`):
- Solids are sets of golden rhombohedra with corners in ℤⁿ.
- Moves add or remove one rhombohedron. Overlaps are tested by separating axes on the 15 face normals.
- Kept: closed 2-manifolds with Euler characteristic 2 and every zone exactly k.
- Translation test: face pairs that are translates; a candidate lattice from three independent pair translations; covolume equal to the volume; no overlap with nearby translates.

| n (k) | Depth | States | Sphere-like, all zones k | Translation tilers |
|---|---|---|---|---|
| 3 (4) | 0 | 1 | 1 | 1: the rhombohedron (control) |
| 4 (6) | ≤ 1 | 29 | 5 | 5: the Bilinski dodecahedron (control) and four 3-cell forms |
| 5 (8) | ≤ 2 | 3,076 | 17 | **3, all with 8 cells = rhombic icosahedron minus 2: Grünbaum's doubly indented D1 and D2** (positive control met) |
| 6 (10) | ≤ 2 | 11,254 | 29 | **0** (the triacontahedron itself does not tile: negative control met) |

Pilot limits:
- Floating-point arithmetic with a 1e-9 tolerance.
- The coplanarity condition is not imposed yet.
- The 3 k = 8 hits still have to be sorted into D1, D2 and possible mirror or duplicate copies.

**Plan for the full run (`byzone-deep`).**
- Search on n = 6 up to depth 6, restricted to moves that keep 30 faces (indent and bulge at 3-valent corners).
- Use canonical forms up to the icosahedral group as well as translation.
- Add Grünbaum's coplanarity filter.
- Run parallel workers on the compute host.
- Re-check every hit exactly in Q(√5) (overlaps by exact separating axes; volume equals covolume).

**Expected outcomes:**
- an explicit k = 10 tiler (G1, blind score 4);
- or none to depth d. G2 scores 3, and the reviewer notes that it would not settle k = 10, because other face counts and zone patterns are possible.

**Lean.** G1 is feasible but heavy:
- the Challenge: an explicit union of rhombohedra with coordinates in ℤ[φ], and the tiling stated as interiors disjoint plus a covering by translates (roughly 300–500 lines);
- the proof: finite overlap checks plus a volume identity in ℤ[φ].

## (c) Goldberg: are all space-filling pentahedra known? DICTO's part: quadrilateral pyramids

**Statement.** Goldberg, "The space-filling pentahedra. II", JCTA 17 (1974) 375–378, §6 (p. 378), library copy: "It is still not known whether all the space-filling pentahedra have been found. An analytic method seems to be needed to exhaust the possibilities or to show that no others exist." The first list is Goldberg, JCTA 13 (1972) 437–443 (library copy). Its pyramids are 5-II-0, 5-III, 5-IV, 5-VI-0 and 5-VIII-0.

**What has been done since.** Duval, "Some symmetric pyramids with trivial Dehn invariant", arXiv:2207.01486 (read §1):
- Theorem 1: among right square pyramids, only the cube's centre pyramid has Dehn zero;
- the same holds for its symmetric halvings T2–T6, a slice of two-parameter families (blind reviewer's finding);
- right triangular and hexagonal pyramids are never Dehn zero.

Other OpenAlex citers of the Goldberg pentahedra papers are Goldberg's own later papers and two applied papers (2019, 2024). MathWorld "Space-Filling Pentahedron" claims no completeness.

**Pilot `bypyr-pilot`** (`scripts/pyramid_pilot.py`, 2 s, FINAL ok; data `data/pyramid-pilot.json`):
- Uses #100's Dehn screen on square-base pyramids with apex (x, y, h) on a grid: x, y ∈ {0, ¼, …, 1} with y ≤ x, and h ∈ {¼, …, 3}.
- **Dehn zero only at the controls:** (0, 0, 1), the cube's centre pyramid, and (1, 1, 2), one third of a cube.
- The right pyramids with h ≠ 1 are nonzero, matching Duval.

**Plan.**
- P2 (right pyramids over a rectangle with half-sides 1 and s, height h): exact dihedral angles. The Dehn-zero locus needs either all angles in ℚπ (a finite cyclotomic search, Conway–Jones as in Duval) or rational relations balanced by the edge lengths, which is Duval's Galois method extended to two parameters.
- Then exact-cover tilings at the surviving points, with #92's pyramid tools.
- Outcome: either "exactly these tile" (P2, blind score 4), or a list of surviving curves.

**Chance and Lean.**
- The chance is medium-low: the analytic step goes beyond Duval.
- Lean is not feasible for the obstruction part, because Mathlib has no Dehn invariant and no Debrunner theorem.

## Ranking

| Question | Chance to close | Palomar fit (blind) | Comfort | Order |
|---|---|---|---|---|
| (b) Grünbaum k = 10 | medium (finite search; method reproduces k = 8) | 4 (G1) | highest: golden rhombohedra, triacontahedron | **1** |
| (a) 40 tetrahedra | full: medium-low; the face-to-face reduction already in hand | 4 (T1); 3 (partial) | high: Dehn, exact cover, corona search | **2** |
| (c) pyramids (P2 first) | medium-low (needs a Duval-type analysis) | 4 (P2) | high: Aristotle's pyramids | **3** |

## Sources checked

**Read in full or at the passages cited:**
- Chentouf–Sun arXiv:2312.01654 v1 (full)
- Sun's criteria.py (data lists only)
- Sommerville, Proc. Edinburgh Math. Soc. 41 (1922/23) 49–57 (full; Cambridge open)
- Bongiovanni–Diaz–Kakkar–Sothanaphan arXiv:1709.04139 (§§1–6)
- Goldberg JCTA 13 (1972) and JCTA 17 (1974) (library, full)
- Grünbaum 2010, v2/3/10 (library, pp. 16–18)
- Duval arXiv:2207.01486 (§1)
- #100 paper and studies 2026-11-04-dehn-screen and 2026-11-04-tetra-sweep
- #92 and #44 (abstracts)
- the earlier studies 2026-11-15-open-problems-to-close and 2026-11-15-palomar-landscape

**Abstract or metadata only:**
- KKPR arXiv:2011.14232
- Chentouf–Sun arXiv:2312.01282
- Hungerbühler–Hungerbühler–Pirron 2025
- Senechal–Taylor 2023 (OpenAlex abstract)
- MathWorld "Rational Tetrahedron", "Space-Filling Tetrahedron", "Space-Filling Pentahedron" (via search)

**Citation searches:**
- OpenAlex citers of Goldberg 1974 (tetrahedra), Senechal 1981, Goldberg pentahedra I and II, Grünbaum 2010 and KKPR
- Crossref lookups for Sommerville, Goldberg (four papers), Senechal and Baumgartner
- Semantic Scholar citers of 2312.01654: none listed

**Web searches:**
- "rhombic monohedral parallelohedron every zone k faces"
- "which rational tetrahedra tile space Chentouf Sun"
- "space-filling pentahedra classification quadrilateral pyramid"
- "Senechal Taylor 2023 nonconvex parallelohedra"
- plus the blind agent's own queries (listed in `blind/blind-B-backyard.json`)

**Not read:**
- Senechal 1981 (Taylor & Francis, paywalled)
- Goldberg 1974 "Three infinite families" (Elsevier open archive, but the site blocked automated download; its families are used as given by Bongiovanni et al. §3 and by Goldberg 1974-II)
- Goldberg 1979, "Convex polyhedral space-fillers of more than twelve faces" (Springer, paywalled): no in-core question taken from it
- Baumgartner 1968/1971 (not found free)
- Edmonds 2007 (Springer, paywalled; known through Bongiovanni et al.)
- Senechal–Taylor 2023 full text (closed)

None was bought. Free routes are an NDL copy or a library visit.

**Correction to the earlier study:** the exact-cover tiling checker is #100's Theorem 2.4, not #102's.

## Files

- `scripts/tetra_pilot.py`, `scripts/zone_pilot.py`, `scripts/pyramid_pilot.py`: the pilots. Each prints PROGRESS lines and a FINAL line.
- `data/tetra-pilot.json`, `data/zone-pilot.json`, `data/pyramid-pilot.json`: the pilot outputs.
- `blind/inputs/B-backyard.md`: the bare statements given to the blind reviewer.
- `blind/blind-B-backyard.json`: the blind reviewer's prompt-04 output.
