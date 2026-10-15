DICTO · dictospheres.com

# Final check: *Inverted Shells: The Spheres of Dharma Turned Inside Out* (Draft 3)

Review by Claude Fable, 16 October 2026. The paper was not edited.

**What I checked against:**
- `paper.html` at commit 957db66 (branch `research`, same as `origin/research`). DICTO changed the title during this check, at 05:36.
- The study data and scripts in `studies/2026-10-16-polar-dharma` (README, all `data/*.txt`, scripts), `studies/2026-10-16-flip-test` (`flip-dharma.txt`, `flip.py`) and `studies/_lib`. `test_geomcheck.py` was rerun: 6 checks passed.
- The published PDFs, fetched with `curl -4` from the Zenodo API:
  - Spheres of Dharma v2 (record 23354038, the latest; byte-identical to the earlier copy)
  - TIH (23360858)
  - In-betweens v3 (23360528, concept 23345502)
  - Theaetetus (23378071, concept 23378070)
  - Ogdoecontahedron (23404689, concept 23404688)
  - #30 v2
- Five DOIs on Crossref.
- All 15 figures, which I looked at.

**What agrees, and needs no change:**
- Every exact number in the paper matches `data/`:
  - the six piece volumes
  - the tight scales, the tight end pieces and the closure squared
  - φ⁹ = 38 + 17√5
  - the great stellated dodecahedron's pieces and its volume of 3 icosahedra
  - 6/φ² = 9 − 3√5, 2/15, the play √5·φ³/9, and the rhombicosidodecahedron play
  - the golden-frame radii
  - Hafner ×φ²
  - the point/valley ratio 3φ³/√5
- Table 1 matches `flip-dharma.txt` row for row, and the piece counts match Dharma (236 + core = 237).
- The statements about Dharma (six solids, the Ritsudō cycle, the Tsai cluster) match the published Dharma PDF.
- The TIH facts (102 faces: 12 pentagons, 30 rhombi, 60 triangles; 80 corners; Shields) match the TIH PDF.
- "Seventh stage … each closed stage taken as one solid" matches In-betweens ("Taking each stage as one solid … The Spheres of Dharma's seventh stage").
- In-betweens states that the great stellated dodecahedron is the icosahedron plus 20 CLEO (the spikes), and Theaetetus defines the Kion by the cone cut.
- The paper is consistent with the published Ogdoecontahedron paper and with #30:
  - 80 faces, 102 corners, 180 edges
  - hexagons holding the triangles, kites in the pentakis dodecahedron's faces
  - the Ogdoecontahedron paper names the companion "The Spheres of Dharma Turned Inside Out", which is still the subtitle
  - no station numbers are used, so there is no clash with #30
- The DOIs for Firsching, Croft, Twarock et al., Dechant et al. and Takakura et al. resolve on Crossref, and their authors, journals, volumes and pages are correct. Firsching (in the reference library) does state the reversal of inclusion under polar reciprocation.
- Every reference is cited in the text.
- No remnants of the toggle or the interlock are left. The only trace is the one-sentence pointer before §9, which is correct.
- The figure and section references (Section 4, Section 7, Table 1) all resolve. The captions match the images (see the optional notes O8 and O9).

---

## Blocking

**B1. The wrong stars are said to float (§5).**
> "The great icosahedron does not fit. The great and small stellated dodecahedra float between two sizes. The great stellated dodecahedron fits at exactly one size"

- `polar-stars.txt` says the solids that float (corner radius 1.453085 to 1.701302) are the **great dodecahedron** and the **small stellated dodecahedron**.
- As written, the sentence says the great stellated dodecahedron both floats and locks.
- Replace with: "The great icosahedron does not fit. The great dodecahedron and the small stellated dodecahedron fit, but float between two sizes. The great stellated dodecahedron fits at exactly one size"

**B2. The claim that every script uses the checks module is false (§9).**
> "every study script now calls a shared module (studies/_lib/geomcheck.py) that stops with an error instead of printing a wrong table"

- I checked with grep. Only `polar_pieces.py` imports `geomcheck`. The other 20 scripts in the two study folders do not, including `polar_exact.py`, `polar_round.py`, `polar_dual_pair.py` and `flip.py`.
- The README says the same: "`polar_pieces.py` now uses rules 1 and 4."
- Replace with: "we collected the checks in a shared module (studies/_lib/geomcheck.py) that stops with an error instead of printing a wrong table. The cone-cut script uses it directly. All the study scripts were rerun from scratch before publication, and their outputs were compared with the committed data:"
- Alternatively, wire the module into the other scripts first and keep the sentence.

**B3. The PDF is stale, and the header is unstamped (do this at publication).**
- `dharma-inside-out.pdf` was built at 05:27. The title commit (05:36) is not in it: the PDF title is still "The Spheres of Dharma Turned Inside Out".
- The header still reads "Draft 3 · … DICTO DOI: on publication", and the page footer reads "vdraft 3".
- Stamp "Version 1 · DICTO DOI: 10.5281/zenodo.<reserved>", rebuild the PDF, and check the footer.

## Should-fix

**S1. The negative claim about dual pairs is broader than the test (§6 and the abstract).**
> "No icosahedral Archimedean–Catalan pair locks." / abstract: "no locked dual pair"

- `polar_dual_pair.py` tests five Archimedean–Catalan pairs plus the icosahedron and dodecahedron.
- The snub dodecahedron and pentagonal hexecontahedron (a chiral pair) are not in the script, and not in `polar_round.py` either.
- §6: "No icosahedral Archimedean–Catalan pair locks (the five non-chiral pairs were tested; the chiral snub dodecahedron pair was not)."
- Abstract: "no locked dual pair among those tested".

**S2. The flip test is described as a sphere, and the sampling is misstated (§1 and Table 1).**
> "turn every piece of every layer (skin) over through the sphere midway between its two solids, as a physical half-turn about a line on that sphere"; column "Midway sphere covered"; caption "coverage sampled along 240 rays from the centre"

`flip.py` does three things differently:
- It pivots each piece at the point on its own axis halfway between the two solids, and it measures cover on the **midway surface**, which is the point halfway along each ray. Neither is a sphere.
- It samples that surface at **4000** random directions. The 240 rays are used only for the radial gaps. The data file's label "along 240 rays: midway surface covered" is the source of this slip.
- It measures overlap depth only between neighbouring pairs of pieces.

Replacements:
- Text: "turn every piece of every layer (skin) over, as a physical half-turn about a line through the point on the piece's own axis midway between its two solids"
- Column header: "Midway surface covered"
- Caption: "Table 1. The flip test (float; cover of the midway surface, halfway between the two solids along each direction, sampled at 4000 directions; deepest overlap between neighbouring flipped pieces, in the units of the Dharma coordinates)."
- §1 prose: "about a third of the midway surface covered twice".

**S3. Where the great stellated dodecahedron sits in each turn (§8 and the Figure 8 caption).**
> "the great stellated dodecahedron locks at the heart of every turn" / "(orange spikes) at the heart of every turn"

- The star sits in each turn's outer gap, between the triacontahedron and the dodecahedron. It is not at the turn's centre, and Figure 8 shows it in the outer band.
- Replace "at the heart of every turn" with "in the outer gap of every turn" in both places.

**S4. The "rhythmic rather than lucky" paragraph overreads a number (§5).**
> "The fit is rhythmic rather than lucky. The squared ratio … is 3φ³/√5: apart from the fixed √3 and √5 that convert between three-fold and five-fold radii, it is φ³, the step by which the whole cycle closes."

- The value 3φ³/√5 is correct. But it is a fixed property of every great stellated dodecahedron.
- Linearly the ratio is √3·φ^(3/2)/5^(1/4). So the "√5 conversion" is really a fourth root, and the φ³ is not the cycle's step.
- The exact fact is that the chain's outer dodecahedron and its icosahedron stand in the star's own point-to-valley ratio. Nothing shows that the closure step causes this.
- Replace with: "Why it fits: the squared ratio of the star's point radius to its valley radius is exactly 3φ³/√5, a fixed property of the great stellated dodecahedron, and the chain's outer dodecahedron and its icosahedron stand in exactly this ratio."

**S5. The pair scales have no stated frame (abstract and §6).**
> "scaled by 6/φ² and 2/15"; "(from the dual of the standard truncated icosidodecahedron)"

- These factors depend on the starting coordinate list (`polar_exact.py` uses the usual even-permutation list) and on the sphere in which the dual is taken. Neither is stated, so a reader cannot reproduce them.
- In the abstract, drop the scales and keep the play: "…fits in reverse order (as polarity demands), with play exactly √5·φ³/9."
- In §6, add the frame: "(the truncated icosidodecahedron from the even permutations of (±1/φ, ±1/φ, ±(3+φ)), (±2/φ, ±φ, ±(1+2φ)), (±1/φ, ±φ², ±(3φ−1)), (±(2φ−1), ±2, ±(2+φ)), (±φ, ±3, ±2φ), and the disdyakis triacontahedron as its polar in the unit sphere)".

**S6. Hafner's tetrahedra have not been checked against his paper (§10).**
> "Hafner (2007) dissects … using 60 tetrahedra, each 1/6 of a prolate golden rhombohedron"

- The README records the Hafner source as "(link only)". The paper is not in the reference library.
- I could not open it either: the old VisMath path returns 403, and no archive copy exists.
- The ×φ² comparison rests on this description.
- Either confirm it against Hafner's text, or say what it rests on: "using 60 tetrahedra, each, as he describes, 1/6 of a prolate golden rhombohedron".
- Also confirm "Visual Mathematics 9 (2007) no. 2". The volume and issue could not be verified online.

**S7. The golden frame is only partly the stellation (§7).**
> "The frame that holds the cycle is its outer dodecahedron's own first stellation."

- The rectangles' 30 long edges are the small stellated dodecahedron's edges. Their 30 short edges are icosahedron edges, which are not edges of the stellation.
- Replace with: "The long edges of the frame that holds the cycle are the edges of its outer dodecahedron's own first stellation."

## Optional

**Wording and labels:**
- **O1.** §1: "a cap on each icosidodecahedron pentagon (its triangles lie in the hexagons)". Here "its" can be read as the cap's own triangles. Use "(the icosidodecahedron's triangles lie in the hexagons and give no piece)".
- **O2.** §5: "(Kepler; our In-betweens paper, …, #27)". The "#27" is site numbering that readers will not know; drop it.
- **O3.** §3 table: "Kepler's pyramid on each icosahedron face". No source is given for the attribution. Write "a triangular pyramid on each icosahedron face" (the README calls them "Kepler's pyramids" only informally).

**Float labels:**
- **O4.** §4: "×1.894", "×1.232" and the inradii list carry no float label. Add "(float)" once, e.g. "…grow ×1.894 (float)…". Alternatively, give 1.232 as exact (11/18 + 5√5/18 appears just after). The README notes 1.894 = φ³/√5 as float-checked only.

**References:**
- **O5.** Use the published full titles, as #30 does:
  - "Spheres of Dharma: a second endless golden cycle of the icosahedral solids, through the icosidodecahedron, the fullerene cage and the rhombic triacontahedron"
  - "Capturing the In-betweens: a Study of Transitional Polyhedral Shells"
  - "Theaetetus: an icosahedron held exactly by its Cleo-Icos, grown to the DICTO Hecatodihedron in two exact stories"
  - The TIH is cited by its version DOI (23360858), while the others use concept DOIs. This is consistent with #30 and the Ogdoecontahedron paper, so leave it.
- **O6.** Poinsot: the usual form is "J. École Polytechnique 4 (cahier 10) (1810) 16–48".

**Data:**
- **O7.** The header points only to GitHub. As with Dharma, TIH, Theaetetus and the Ogdoecontahedron, bundle the scripts, data and `_lib` with the Zenodo record, and say "included with this record and at …".

**Figures:**
- **O8.** Figure 5(c) calls the pyramids "indigo". In the render they are pale lavender-blue; "lavender" reads truer.
- **O9.** Figure 4(a) reuses `cut.jpg` from Figure 1(b). This is acceptable for a side-by-side comparison, but Figure 1 could instead show `closed`, `apart` and a different view.

**Search limit:**
- **O10.** §10's "Not found" list: for consistency with the Ogdoecontahedron paper and #30, you may add "Printed catalogues were not read". This is less important here, because P3 claims no new solid.

---

## Verdict

**Not ready to publish yet.** B1 is a factual error in the text. B2 is a false statement about the method that any reader can check in the repository. B3 is the stamp and rebuild, needed in any case.

All are one-line fixes. With B1–B3 and S1–S7 applied, the paper is ready: every exact number checks against the data, every statement about the published papers matches the record, and the references are correct.
