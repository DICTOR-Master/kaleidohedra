DICTO · dictospheres.com

# Independent check: "A Fibonacci Spine in a Five-fold Chorus of Ogdoecontahedron Packings" (draft 1)

Checked 2026-10-15 against `papers/ocd-chorus/paper.html` (the PDF text matches it) and `studies/2026-10-16-ocd-pyrochlore/` (README steps 17–30, data/*.txt, scripts, FABLE-REPORT.md, FABLE-PRIORART.md, PAPER-OUTLINE.md). No files were changed except this one. Independent recomputations used only `data/chorus-fork.json` (float OCD vertices, axis, target and rival) and the exact expressions. Crossref, arXiv and Zenodo were queried for the references.

---

## (a) Blocking errors

**A1. A voice's joints are not on a pyrochlore lattice (§3).**
- Paper: "Each cube's bond vectors generate a rank-3 lattice, and copies on it meet face to face on hexagons, with joints on a pyrochlore lattice."
- The eight cube bond vectors generate a bcc lattice (README step 2a: "one body-centred cubic lattice packing ... each touches 8 neighbours"). The midpoints of all bcc nearest-neighbour bonds form a **simple cubic** lattice. Recomputed in float from `chorus-fork.json`: each joint has 6 nearest joints at 0.7191 (= bond/√3) and then 12 at 1.0170 (= 0.7191·√2). That is simple cubic; pyrochlore would give a second shell at √3 times the first. The pyrochlore lattice holds the joints of **one diamond sub-network** (README step 1: four tetrahedral hexagons).
- Correct version: "...copies on it meet face to face on eight hexagons. The joints form a simple cubic lattice, and each of the packing's two interpenetrating diamond sub-networks has its joints on a pyrochlore lattice (README steps 1–2a)."

**A2. The data pointer names the wrong steps (header).**
- Paper: "Data, scripts, exact checks and renders: ... steps 17–29."
- The §7 numbers (43/44, 46/47, 45/46, 42/43; rules A–D; 555 against 385; the rival's three clashes) all come from **step 30**. Step 29, which this range ends on, is the retracted "tie" (its heading and Result still say "a tie" and "equally minimal"). A permanent paper would send readers to the wrong claim.
- Correct version: "steps 17–30 (step 30 corrects step 29)". Also add a "superseded by step 30" note at the top of README step 29 and in the prior-art "Not found" list, which still says "the equal-cost fork beyond it (step 29)". FABLE-PRIORART.md Q4 and the overall novelty statement still say "equal-cost fork" too.

**A3. "Below height 12.81" is false as written (abstract, §6).**
- Abstract: "no lattice point lies between them below height 12.81". §6: "No plane lattice point has tc ≤ t < Lcan below height 12.812".
- Heights are signed, and the second departure point is at **−22.71**, which is below 12.812. `chorus-window-why.txt` says "for |height| < 12.812".
- Correct version: "for |h| < 12.81 (between heights −12.81 and +12.81)" in the abstract and §6. Also check the subtitle ("until height 12.8") and §1 ("beyond a height of 12.81") and write "|h|".

**A4. The counts in §5 do not add up, and the abstract overstates "one plane".**
- §5: "In the radius-10 build there are 11 such rings" and "Ten of the 11 rings have their wedge-0 copy in one plane". Later: "the chain points inside the build are exactly the 11 removed copies and the centre".
- The data says two different "11"s:
  - The 11 core rings are those **within 1.05 of the axis**, a cutoff the paper never states (`chorus_heights_exact.py`; `chorus-modelset.txt`). Ten are in the plane and one is off it (1.0042).
  - The plane holds **11 removed copies** (`chorus-window-why.txt`, t = 0.11032 … 1.11313). These are the 10 core-ring copies plus a copy at t = 1.11313, which lies outside the 1.05 cutoff. The gap word LLSLTLSLLS has 11 points.
- As written, a reader concludes that 10 removed copies lie in the plane, which contradicts "11 removed copies".
- The abstract's "The copies removed near the axis lie in one plane on a rank-2 lattice" is false. The ring at 1.0042 is off the plane, and the radius-10 build also removes off-plane copies at 1.084 and 1.136 from the axis (`chorus-exact-r10.txt`). Note that 1.136 > tc.
- Correct version (§5): "Within 1.05 of the axis there are 11 rings of removed copies. Ten have their wedge-0 copy in one plane through the axis, and one (distance 1.0042) does not. The plane holds 11 removed copies in all: these ten and one more at t = 1.11313." Abstract: "Apart from one ring, the copies removed nearest the axis lie in one plane...".

**A5. The headline equation "removed = chain" is off by the centre (abstract, §5).**
- Abstract: "they are exactly the canonical singular Fibonacci cut-and-project chain, window [0, L) ..., the central copy being one of its points". The central copy is **kept**, so the removed copies cannot be exactly a set that contains it.
- §5: "the removed plane copies are exactly those with t below a window edge: there is no kept copy inside". The centre (t = 0, kept) is inside [0, W). The data only shows that no kept copy lies in [0.11032, 1.11313] (`chorus-modelset.txt`).
- Correct version (per `chorus-canonical.txt`: "chain points within the build's height range: 12 = the 11 silent sites + the centre"): "The removed plane copies together with the central copy are exactly the points of the canonical singular Fibonacci chain with window [0, Lcan). The centre, at t = 0 on the closed edge, is kept because its ring is itself." In §5: "the removed plane copies are exactly those with 0 < t < W".

---

## (b) Should fix

**B1. Rule D's cost is mixed up with the minimal cost (§7).**
- Paper: "Pure Fibonacci can be kept, for instance by removing first the ring nearest to clashing with itself, but that rule removes 555 copies instead of 385 ...; it costs one extra ring at every departure point."
- Rule D costs far more than one ring per point. On the patches it removes 330/360/350/325 copies, against 215/230/225/210 for rule A (`chorus-rules.txt`). The "one extra ring" is the integer-program minimum with the target forced silent (`chorus-fork-min.txt`).
- Correct version: "Staying Fibonacci costs at least one extra ring at each departure point (integer program on patches). A simple greedy rule that does it (D) is far from minimal: 555 removals instead of 385 at radius 10."

**B2. The face-separation numbers are not distances (§6, §7).**
- "28/81 − 4√5/27 ≈ 0.014" and "232/81 − 104√5/81 ≈ −0.0068" are max(n·D − 2d) with **unnormalised** face normals (n is a cross product of edge vectors, in `chorus_exact_big.py` / `chorus_window_why.py`). Their size depends on |n|.
- Normalised float values (recomputed from `chorus-fork.json`): the edge copy clears its 72° ring-mate by **0.103**, and the target–rival pair needs **0.046** to separate along the best face normal.
- Fix: either state that only the sign is meaningful (an exact face function with the normals of the data), or give normalised distances.

**B3. "The core is exactly the canonical chain" claims more than was checked beyond the build (§6).**
- Paper: "...up to there the two windows select the same points and the core is exactly the canonical Fibonacci chain, beyond the build's own reach (|h| < 10)."
- What is exact for 10 ≤ |h| < 12.81 is the **window** statement: removal is forced for 0 < t < tc, and no lattice point lies in [tc, L). That no plane copy with t ≥ Lcan is removed by some *other* clash was checked only in the build (|h| < 10) and in float on the h ≈ 12.81 patch (heights 5.8 to 19.8, `chorus-h128.txt`). Heights −12.81 < h < −10 are covered by no patch.
- Correct version: "...the two windows select the same lattice points; the removal pattern itself is checked in the build (|h| < 10)."

**B4. The fork conclusions need their qualifiers in the abstract and the §7 conclusion.**
- "Minimal removal therefore keeps the core copy" rests on integer programs over whole five-fold rings, on finite patches, with a float clash test. Only the clashes at 12.81 are exact; the other three points are float (`chorus-rules.txt` header).
- Add "on finite patches (integer program, float clash test)" to the abstract and to §7's "Hardness with minimal removal therefore departs...". In §7, mark "the pattern is the same" at the other three points as float.

**B5. Xiong et al. is in the reference list but never cited.**
- It is the most recent and most direct prior art: a cut-and-project framework for quasiperiodic interfaces, with generalised Fibonacci sequences in bcc tilt boundaries (README prior art; arXiv record verified).
- Cite it in §1 and §9 next to Sutton, or drop it. Citing it is clearly better.

**B6. The Katz & Gratias contrast is stated as fact but was not read (§9).**
- "exclusion acts between points one lattice shift apart" is, per README, "general knowledge of the field, *not* checked against the 1993 text". The 1993 paper is closed access.
- Soften: "in the standard form of the hard-core condition, exclusion acts between points related by a lattice translation". Alternatively, read the paper first.

**B7. The symbol L means two things.**
- The abstract, Fig. 5 and §7 use L (or [0, L)) for the window length 1.223451. §5 and §7 ("gaps L, S and L + S") use L for the long gap 1.97958.
- Also, S = Lcan **exactly**. (2 + 2φ)u squared is 64/81 + 128√5/405, recomputed; the two agree to 16 digits. The paper prints S = 1.22345 and Lcan = 1.223451 without saying so, which looks like a typo. State the identity, or note it in passing.
- Fix: use W (or Lcan) for the window throughout, and keep L/S/T for gaps.

**B8. The subtitle says the canonical window is "fixed" by the ring clash.**
- Subtitle: "its window fixed by a five-fold ring clashing with itself". The ring clash fixes [0, tc), which §6 shows is *narrower* than the canonical window. The two agree only on lattice points with |h| < 12.81.
- Suggest: "...its window enforced by a five-fold ring clashing with itself up to |h| = 12.8".

**B9. The near-axis removals are not fully accounted for (§5, Limits).**
- State the 1.05 cutoff. Also say that the radius-10 build removes further off-plane copies at 1.084 and 1.136 from the axis (`chorus-exact-r10.txt`), the latter beyond tc. Limits mentions only the 1.0042 ring.

**B10. The companion paper is cited as an unpublished draft with a future date.**
- "The DICTO Ogdoecontahedron (draft, 16 October 2026)". Today is 15 October. A paper with a permanent DOI should cite something a reader can retrieve.
- Publish the OCD paper first and cite its DOI, or write "in preparation" and point to the study README for the coordinates.

**B11. The repo text the paper relies on still carries the retracted tie.**
- README step 29 (heading "a tie", Result "equally minimal"), the README prior-art list ("equal-cost fork") and FABLE-PRIORART.md (Q4 and the overall novelty statement) predate step 30.
- Add a "superseded by step 30" line to each, since the paper links readers there. This goes with A2.

---

## (c) Minor

1. §7: "the rival has two live clashes to the core copy's one". This holds at 12.81, but at −22.71 rule A saw 3 against 1 (`chorus-rules.txt`). Write "more live clashes".
2. Abstract: the rival "also overlaps a third" copy, but §7 says "two further copies". Make them consistent, e.g. "two others, one of them removed anyway".
3. §8: "the strongest peaks within the peak width". 15 of the 16 are within about 0.3, but one is off by 0.401 (`chorus-modelset.txt`). The peak width of 0.3 appears only in the README, not in the data file. Write "15 of the 16 strongest".
4. §2: the kite angles are 117.85° (twice), 68.62° and 55.69°. Say "twice" (recomputed).
5. §2: L0(D) was built from Antiprism's written definition, and the Antiprism program was not run (README). Add a half-sentence.
6. §6: "A copy at distance t" should read "A plane copy at distance t". Optionally add that the 144° ring-mates clear already for t > 0.701 (float, recomputed), so the 72° mate sets tc. The script computes tc from the 72° mate only.
7. §4: "apart" includes touching. "Do not overlap (interiors disjoint)" is clearer.
8. References:
   - Lee & Glotzer: add article number 7362.
   - Hofmeister: add doi:10.1002/(SICI)1521-4079(1998)33:1<3::AID-CRAT3>3.0.CO;2-3.
   - van Enter et al.: online 2019, but vol. 178, issue 3 is dated 2020. Either year is acceptable; prefer "178 (2020) 832–844".
   - Hubbard: the full title spells out "tetracyanoquinodimethane (TCNQ)".
   - "Spheres of Dharma": give the full title. 10.5281/zenodo.23310833 is a concept DOI, which is fine; it resolves to record 23354038.
9. §1: "Pauling (1985) proposed, wrongly," sounds editorial to a referee. Suggest "proposed (a view since superseded)".
10. §9: "One-dimensional lattice gases have Sturmian ground states" should be qualified: "with convex repulsive interactions" (Hubbard), or "in suitably designed models" (van Enter et al.).
11. Terminology: "core", "spine" and "chain" are used for the same object, and "silenced" (§1) for "removed". Define "spine" once and use "removed" throughout.
12. Dates: the paper is dated 15 October, but the study folder and the companion draft carry 16 October.
13. Reproducibility:
    - The radius-10 site file `data/chorus-exact-r10.json`, which §5–7 scripts read, is not committed. `chorus_exact_big.py 10.0` regenerates it; say so in §11.
    - The scripts hard-code `/home/dicto/kaleidohedra/...` and need `studies/2026-10-16-polar-dharma` and `studies/_lib`. Both are tracked; mention them.
14. Fig. 5 caption: "[0, L)" should be "[0, Lcan)" (see B7).

---

## (d) Verified OK

**Numbers (recomputed from the exact forms):**
- u² = 8/81 − 8√5/405 = 0.0545962, u = 0.233658. Also φ³u = 0.98979, the unit used in step 24.
- tc² = 8/9 + 8√5/45, tc = 1.134201. Also recomputed independently in float from the OCD faces: 1.1342011.
- Lcan² = 64/81 + 128√5/405, Lcan = 1.223451. The largest removed t is √(544/81 − 992√5/405) = 1.113132.
- 28/81 − 4√5/27 = 0.01441 and 232/81 − 104√5/81 = −0.00680: values correct (see B2 on their meaning).
- Gaps S = (2+2φ)u = 1.22345, L = (2+4φ)u = 1.97958, T = (4+6φ)u = 3.20304. L/S = φ and T = L + S, both exact.
- Ring heights: (10+16φ)u = 8.3857, (12+18φ)u = 9.6091, (−8−14φ)u = −7.1622 and the rest, all match `chorus-heights-exact.txt`.
- Squared ring distances relative to the innermost are φ², φ⁴, φ⁶ and φ⁸ (data).
- Bond pairs (±1, 0) and ±(1, 2) (data).

**Build table** (`chorus-exact-big.txt`, `-r8.txt`, `-r10.txt`):

| Radius | Sites | Removed | Close pairs | Overlaps | Touching |
|---|---|---|---|---|---|
| 5 | 336 | 80 | 620 | 0 | 620 |
| 8 | 1471 | 240 | 3630 | 0 | 3605 |
| 10 | 2756 | 385 | 7465 | 0 | 7390 |

**Integer programs and counts:**
- Radius-5 integer program: 16 rings (80 copies), the same as greedy, not unique; 72 without symmetry. The 44.4775° angle (`chorus-min-silence.txt`).
- Plane lattice: 73 sites, slope −φ, heights distinct. 11 removed plane copies, with no kept copy in [0.11, 1.113] (`chorus-modelset.txt`).
- Canonical window (`chorus-canonical.txt`):
  - Gap vectors (1, −1) and (1, 0), determinant 1.
  - 54 points to ±45, 33 long and 20 short, a Fibonacci factor.
  - The edge copy at h = −0.756 is kept.
  - Singular chain, centre on the closed edge: matches the data (but see A5 for the wording).
- Ring self-clash for all 15 plane copies with t < 1.6: 11 overlap, 4 clear. tc is the same for every plane site and lies strictly between 1.113132 and Lcan (`chorus-window-why.txt`).
- Departure heights 12.812, −22.71, 34.77 (34.766) and −44.66, with plane coordinates (8, −4) etc. (`chorus-window-why.txt`, `chorus-rules.txt`).

**The fork at 12.81:**
- 1135 sites. The target clears all four ring-mates. Of the 7 copies within 2R it overlaps exactly 1. Rival at h 13.8019, ρ 1.1690, wedge 1, with no self-clash (`chorus-h128.txt`).
- The rival overlaps 14.79 (self-clashing) and 14.04 (ρ 1.91, not self-clashing), exact (`chorus-fork-exact2.txt`).
- Lens volume 0.705%, so the paper's 0.71% is right (`chorus-fork.json`: lensVol/ocdVol).
- Integer-program minima 43/44, 46/47, 45/46 and 42/43 (kept/removed), patches 1130–1155 sites (`chorus-fork-min.txt`). The integer-program script is correct in form: whole rings, self-clashing rings forced, the target's ring fixed each way.
- Rule A reproduces the built 385; rule D gives 555 (`chorus-rules.txt`). The greedy rule removes the rival by count, not by tie-break (`chorus-rules.txt`).

**Seams** (`chorus-boundary.txt`, `chorus-modelset.txt`):
- Counts 5/20/60/95/145/205/275 for r = 3 to 9; density 0.31 to 0.43.
- 66 vacancies; I/N 46.6 against 66 and 11.8 ± 2.0; no slab rule.

**The solid** (recomputed from `chorus-fork.json`):
- V/E/F 102/180/80. Degrees 60×3, 30×4, 12×5. 20 hexagons with equal sides and 60 kites.
- Kite angles 117.85/117.85/68.62/55.69.
- Edge lines at two distances (0.655971 and 0.666667 in these units), so no midsphere.
- The axis vertex has degree 5.
- Face arrangement = cut-down pentakis dodecahedron = dual of L0(D), with controls (`ocd-dl0d.txt`).
- McCooey: 553 solids, no V/E/F match either way, controls pass (`ocd-catalogue.txt`).
- "Not in McCooey", "obtainable by standard operations" and "metric solid not found in any source checked" are worded at the right strength. The printed books are correctly described as ruled out by scope, not read.

**Logic:**
- **Central symmetry.** The OCD is centrally symmetric: every vertex v has −v as a vertex (float check on all 102). So K − K = 2K, and the face-plane overlap test is exact and complete for translates.
- **2R cutoff.** Circumradius R = 0.69520 and 2R = 1.39040. These match the "within 1.390" neighbour radius. Copies farther apart than 2R cannot overlap, so checking closer pairs is complete. Pairs at exactly 2R could only touch.
- **"Cheaper by one ring".** Supported as a statement about finite patches with float clashes; the qualifier is missing in places (B4). The local reason checks out: removing the target leaves the rival–14.04 clash.

**Citations** (Crossref, 13 DOIs): all resolve, and authors, titles, journals, volumes, pages and years match the reference list (exceptions in c8):
- Baake & Grimm
- Gratias & Thalal 57:63–68
- Hubbard 17:494–505
- Katz & Gratias 153–154:187–195
- Lee & Glotzer 13
- Pauling 317:512–514
- Prodan et al. 7:12474
- Ranganathan et al. 41:7696–7703
- Rivier & Lawrence 150:190–202
- Sutton 36:1291–1299, 16:563–574 and 36:167–202
- van Enter et al. 178:832–844

Other records:
- Hofmeister 33:3–25 found on Crossref.
- Xiong, Zou, Zhang & Jiang, arXiv:2603.21158 (March 2026): authors and title match.
- Zenodo 10.5281/zenodo.23360858 (Hecatodihedron, DICTO) resolves.
- 10.5281/zenodo.23310833 (Spheres of Dharma, concept DOI) resolves.

**What the text says about the sources:**
- The in-text statements about Sutton, Gratias–Thalal, Rivier–Lawrence, Ranganathan et al., Prodan et al. and Lee & Glotzer agree with FABLE-PRIORART.md and the README notes. Lee & Glotzer's "floating point, angle gap" is supported there.
- The closed-access caveat in §9 is present and appropriate.
- The "tie" claim is fully gone from the paper; the only "ties" left refer to the greedy tie-break.

---

## (e) Verdict

**Ready for DOI after fixing (a).**

All five blocking items are text corrections; none needs a new computation. The numbers and exact expressions themselves check out. Fix (b) as well before the DOI, especially:
- B1 (rule D cost);
- B2 (unnormalised separations);
- B4 (patch/float qualifiers in the abstract);
- B5 (uncited Xiong);
- B10 (citing an unpublished draft).

A referee would raise each of these.
