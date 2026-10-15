DICTO · dictospheres.com

# Boundaries and order of three papers: #30, the Ogdoecontahedron, the Dharma inside out

Review by Claude Fable, 16 October 2026. I read the published #30 (Version 2 PDF, Zenodo record 23397447), Draft 3 of *The DICTO Ogdoecontahedron* (P2), and the draft of *The Spheres of Dharma Turned Inside Out* (P3). I checked them against the study READMEs and data (polar-dharma, ocd-pyrochlore, ogdoecontahedron-bridge, interlock, flip-test; branch `research`) and against the published Hecatodihedron (TIH) and Spheres of Dharma texts in `papers/tih` and `papers/spheres-of-dharma`. No paper files were edited.

**Independent check of P2's numbers.** I rebuilt the Hecatodihedron from scratch (truncated icosahedron of edge 1/φ plus 20 Shield apexes at 3√3/(2φ)), took its polar in the unit sphere and recomputed everything with a float convex hull. Every number matches P2:

- 80 faces (20 hexagons, 60 kites), 102 corners (60 of degree 3, 30 of degree 4, 12 of degree 5) and 180 edges.
- Edge lengths 0.237881 (120 edges) and 0.197124 (60).
- Corner radii² 4/9 (90 corners) and (170 + 2√5)/361 (12).
- Face distances 0.62278 and 0.65295.
- Dihedral angles 156.20° (kite–hexagon) and 156.72° (kite–kite).
- Kite angles 117.85° (twice), 68.62° and 55.69°.
- Volume 1.151868, |t|² = 1.551428.
- Exactly 5 inscribed cubes.
- bcc density 0.774332, the same as (9225 − 3915√5)/608, with no overlap in a 7×7×7 patch.

The edges lie at two distances from the centre (0.65597 and 2/3), which confirms #30's "no midsphere". I also checked the layer volumes in P3 (all six layers, plus the great stellated dodecahedron split) against the layer differences in `polar-step1.txt`. They agree.

## 1. Boundaries: what each paper alone should own

- **#30, the chorus (published).** Five bcc packings meeting round a five-fold axis, the exact chorus, the Fibonacci spine, the ring-clash window and the fork at 12.81. It uses the solid; it does not describe it.
- **P2, the Ogdoecontahedron.** The solid itself:
  - its origin, in two or three sentences;
  - its metric data and face arrangement;
  - its relation to its two neighbours in the nest;
  - its own packings (one diamond network, the bcc packing, the densest lattice packing found);
  - the negative quasicrystal check (the bridge study).

  Everything about the cycle as a whole is left to P3.
- **P3, the Dharma inside out.** The reversed cycle as a structure:
  - the flip test, as the reason for using reciprocation;
  - the full chain and closure;
  - one piece kind per layer (all six layers);
  - the tight nest;
  - the great stellated dodecahedron in the outer gap;
  - the dual pairs in the inner gap;
  - the golden frame and the endless core;
  - the checks module.
- **P4, both cycles in one space (proposed).** The toggle (the sphere of polarity as the free choice, the two settings, "never both", the scale palindrome) and the interlock (536 and 502 pieces, 12 and 11 kinds, named by DICTO).

## 2. Overlaps and where each belongs

| # | Item | Where it appears now | Belongs in | Action |
|---|---|---|---|---|
| 1 | The Spheres of Dharma described as a chain | P2 §1: "The Spheres of Dharma … is an exact cycle of nested icosahedral solids: icosahedron ⊂ icosidodecahedron ⊂ … ⊂ icosahedron φ³ larger". P3 §1 has the same sentence word for word. | P3 | Both papers need one sentence. Fix the wording in both (see B1). |
| 2 | Polar reciprocation and the reversed chain | P2 §1, "Second attempt … The reversed cycle is dodecahedron ⊂ icosidodecahedron ⊂ Ogdoecontahedron ⊂ …". P3 §1, "So the reversed cycle is again a nest … D ⊂ ID ⊂ Ogdoecontahedron ⊂ PD ⊂ I ⊂ RT ⊂ D·φ³" | P3 | P2 keeps the one-line chain, because the solid is defined by it, and drops the duality-swap commentary. P3 keeps the closure φ⁹ and the swapped pairs. |
| 3 | **Flip test** | **Only in P2 §1:** "Every piece of every skin was turned over … No skin closes into a shell … covering only 3–8% … about a third of the sphere covered twice." P3 does not mention it. | **P3** (it concerns Dharma's pieces, not the solid) | Move the full result, ideally the six-row table from the study README, into P3 §1. P2 keeps one sentence: "Flipping Dharma's pieces does not close any layer into a shell (study cited); polar reciprocation does." |
| 4 | The Ogdoecontahedron within the nest (hexagons in the icosidodecahedron's triangle planes, kites in the pentakis dodecahedron's faces) | P2 §3, "Held between two classical solids". P3 §2 repeats it: "its 20 hexagons lie in the planes of the icosidodecahedron's 20 triangles, each hexagon holding a triangle, and its 60 kites lie in the faces of the pentakis dodecahedron". | P2 | These are facts about the solid. P3 can keep one sentence that cites P2. |
| 5 | **The pieces on either side of the Ogdoecontahedron** | P2 §3: "Below it, 12 caps … (−155 + 101√5)/4617; above it, 20 low pyramids … (−22 + 10√5)/81", and P2 Figure 2. P3 §3 has the same two rows in its table, and the same pieces in Fig. 3(b), (c). | **P3** | These results belong to the layer study. Cut P2 §3's third paragraph and Figure 2. If you want to keep a trace, one clause: "each neighbouring layer cuts into one kind of piece (companion paper)". |
| 6 | Naming of the Ogdoecontahedron | P2 §1 and P3 §2 | P2 | P3 cites P2. This is fine as it stands. |
| 7 | **Five cubes, bcc packing, pyrochlore joints** | **Already published in #30 §3:** "The 20 hexagon directions contain exactly five sets of eight that form a cube … they generate a body-centred cubic lattice … each of the packing's two interpenetrating diamond sub-networks has its joints on a pyrochlore lattice." P2 §5 and §6 restate this. | P2 owns the single-packing facts: one diamond network, its no-overlap test, the bcc packing, the exact density 77.43% and the densest packing 0.789260. #30 owns the five voices together. | Leave P2 §5 in place, but P2 must say that the construction was first stated in #30 §3. Otherwise P2 reads as the first report of something already on record. P2 §7's "not found … its exact hexagon-joined packings" is fine. |
| 8 | **Face arrangement** (dual of L0(D); McCooey scan; the 6-truncated pentakis dodecahedron) | #30 §2, published. P2 §4. | P2 (the solid's home), but #30 has priority on record | Keep it in P2 and add "(also reported in #30 §2)". P2 must also carry #30's limit (see S2). |
| 9 | Bridge result (not a patch or cluster of the canonical quasicrystal) | #30 §1 (summary, citing the GitHub study). P2 abstract and §6. | **P2** | P2 becomes the published source (see section 6 below). |
| 10 | Pointer from the five packings to the chorus | P2 §6, last sentences | #30 | This is a correct short pointer. Keep it. |
| 11 | Toggle, and the mention of the interlock | P3 §9 | P4 | See section 3. |
| 12 | Solid figure | P2 Fig. 1; P3 Fig. 2 (the same solid) | P2 | P3 may keep a small figure, or point to P2 instead. Optional. |

## 3. Toggle and interlock: P3 or a fourth paper?

**Recommendation: one fourth paper, *Both Cycles in One Space* (working title), with the toggle and the interlock together. P3 ends at the core (§8).**

- P3 already makes a complete arc: one cycle, reversed, filled, framed, endless. It has 12 sections and 10 figures. The toggle brings in a new free choice (the polarity sphere ρ) and a second object (the original cycle), and that is exactly what the interlock is built on.
- The interlock is exact (remainder 0 in both settings; 12 kinds at the ends setting, 11 at the middle). But its piece kinds are not yet named, and naming them is DICTO's part. P3 should not wait for that, and should not cite results that live only in a GitHub folder ("reported separately (studies/2026-10-16-interlock)").
- The toggle results (the two settings, "never both", the loose-end bound) are short. On their own they would make a thin P4; together with the interlock they make a solid one.
- In P3, replace §9 with one sentence: "The original and reversed cycles can also share one space; that is the subject of a further paper (in preparation)." Remove the toggle clause from the abstract, Figs. 9–10, and the toggle items from §11's "Not found" list. Move all of these into P4.

If DICTO prefers fewer papers, the fallback is to keep the toggle in P3 as written, and drop only the interlock sentence. P4 would then be the interlock alone, restating the two settings in one paragraph with a citation to P3.

## 4. Order of publication and how cross-references should read

**Order: #30 (published) → P2 → P3 → P4.** DICTO's wish to publish P2 first is sound:

- #30 already cites it as the solid's paper.
- Once P2 is cut to the solid (overlap items 3 and 5 above), it depends on P3 for nothing. The reversed chain is one line of classical duality, and its pieces leave P2.
- P3 then builds on P2 by DOI, and P4 builds on P3.

**Cross-references:**

- **P2 → #30:** cite by DICTO DOI 10.5281/zenodo.23396361, as now. Also credit #30 §2–3 for first stating the face arrangement and the five cubes and bcc packing (overlap items 7 and 8).
- **P2 → P3:** "DICTO, *The Spheres of Dharma Turned Inside Out* (in preparation)". Use the title only, and make no claim that rests on it. Do not put a reserved Zenodo DOI in P2 unless P3 will be published within a day or two. A reserved DOI does not resolve until its record is published, so a published paper would carry a dead DOI meanwhile.
- **P3 → P2:** "DICTO, *The DICTO Ogdoecontahedron*, DICTO DOI: 10.5281/zenodo.(P2)". P3 → #30: by DOI, if P3 mentions the packings at all.
- **P4 → P3 and P2:** by DOI.
- **#30 needs no new version** just because P2 gets a DOI. On Zenodo, edit #30's record metadata (allowed without a new version; only files are locked) and add a related identifier: *references* → P2's DOI. Likewise P2 *references* #30, and later P3 *references* P2. Make a #30 Version 3 only if something substantive comes up. If one is ever made, update ref 20 ("in preparation") to P2's DOI, replace ref 19 (the bridge GitHub folder) with P2, and consider the station-number wording (O1).
- **P2 after P3 is published:** again a metadata link only, with no new version needed.

## 5. Problems in P2 (Draft 3)

### Blocking

**B1. P2 restates the published Spheres of Dharma cycle inaccurately (P3 has the same problem).**

- P2 §1 says: "The Spheres of Dharma … is an exact cycle of nested icosahedral solids: icosahedron ⊂ icosidodecahedron ⊂ dodecahedron ⊂ truncated icosahedron ⊂ Hecatodihedron ⊂ rhombic triacontahedron ⊂ icosahedron φ³ larger."
- The published Dharma paper says "an exact, endlessly repeating nesting of six icosahedral solids (the Ritsudō cycle)": I, ID, D, TI, RT, I(φ²-edge). The Hecatodihedron is not one of them. It is the truncated icosahedron to triacontahedron layer closed part-way (stage 7 in *Capturing the In-betweens*; the TIH paper says "arises as the seventh stage").
- P3's abstract, "The Spheres of Dharma nest seven icosahedral solids", contradicts the record directly.
- This matters for honesty too. The Ogdoecontahedron appears only because the Hecatodihedron stage was added as an extra station. Reciprocating the six published stations alone gives a chain of classical solids only.
- Fix, one sentence in each paper: "The Spheres of Dharma nest six solids, I ⊂ ID ⊂ D ⊂ TI ⊂ RT ⊂ I·φ³. Its TI → RT layer closes part-way into the Hecatodihedron (stage 7 of the In-betweens). We include that stage, which gives a seven-station chain." Then "every station becomes classical except one" reads correctly.
- This also removes the puzzle of "seventh stage" sitting beside a list in which the Hecatodihedron is fifth.

**B2. The abstract overstates the quasicrystal result.**

- The abstract says: "On its own it is not a piece of an icosahedral quasicrystal".
- The bridge study tested only the canonical primitive tiling and three standard cluster shells. It says so: "Other 6D lattices (face- or body-centred), other windows, and decorated tilings were not tested." P2 §6 does carry the limit, in a parenthesis.
- Use #30's published wording in the abstract: "it is neither a patch nor a cluster of the canonical (primitive) icosahedral quasicrystal".

### Should-fix

**S1. Move the reversed-cycle pieces and the flip test out of P2** (overlap items 3 and 5). They are correct (the volumes check against the layer differences), but they are P3's results. If they are published in P2 first, P3 duplicates P2.

**S2. Carry #30's limit on the catalogue search.**

- #30 §2 says: "The printed catalogues (Wenninger, Holden, Pugh) were ruled out by scope, not read."
- P2 §4 and §7 say only "not found in our reference library, McCooey's catalogue and web searches". A later paper with a vaguer limit reads as a stronger claim.
- Add the same sentence to P2.

**S3. Credit #30 for prior statements** (overlap items 7 and 8):

- "The five inscribed cubes, the bcc packing and the pyrochlore joints were first stated in #30 §3."
- "The face arrangement was first reported in #30 §2."

**S4. Densest lattice packing.**

- P2 says: "we believe but have not proved it to be the densest".
- Replace the belief with the scope from the study README: "the best of 200 local-search starts, all converging to 0.789260; checked as a packing for lattice coefficients up to 4 (float); not proved densest."

**S5. Data links do not name the branch.**

- `studies/2026-10-16-ocd-pyrochlore` exists only on branch `research` (checked: absent from `origin/master`). P2's header link (repo root, default branch `master`) will not lead a reader there.
- Name `branch research` as #30 does, or better, pin a commit (as ref 12 already does).
- Bundle the cited scripts and data with the Zenodo record, as #30 did. All the cited scripts exist (checked).

### Optional

**O1. Station numbering.**

- #30 calls the solid "the second station of the Spheres of Dharma turned inside out". This counts the inner dodecahedron as 0, as in `polar-step1.txt`.
- In the chain as P2 and P3 write it, a reader counts it as the third.
- P2 and P3 should either avoid station numbers, or say once "station 2, counting the inner dodecahedron as 0" so that #30 reads correctly.

**O2. Add "no midsphere" to P2 §2.** The edges lie at two distances, 0.65597 and 2/3 (my float check). #30 states this property of the solid, so its home paper should state it too.

**O3. Say that L0(D) agrees with the published TIH description.** P2 §4 gives the Hecatodihedron's arrangement as L0(D). The TIH paper describes it as k6tI with 60 coplanar triangle pairs merged into rhombi. One clause saying both describe the same arrangement prevents a reader from thinking they disagree.

**O4. The comparison with the densest sphere packing (74.05%).** It is accurate but adds little. Many convex solids out-pack spheres. Keep it in §5 if wanted, and consider dropping it from the abstract.

**O5. Dates.** The study folders are named 2026-10-16, but the git history shows the work committed on 15 October, as #30 and P2's reference 12 say. This is harmless, but don't quote folder names as dates.

**No contradictions found** between P2 and the published #30, TIH or Spheres of Dharma papers, other than B1 and the station-number wording (O1). The 90-sphere and 12-outer-corner statement matches TIH ("rhombi and triangles at 1.5, pentagons at 1.4384"). The two edge angles match ("only two edge angles"). The flip-test summary matches `flip-dharma.txt`. The bridge summary matches `bridge.txt`.

## 6. Reference 12 (the bridge study, a GitHub folder)

The bridge result is a property of the solid, so P2 should become its published source rather than point to it:

1. In P2 §6, write the result out in four or five sentences with its numbers and scope:
   - the corners lift to integer 6D points at ×171, with perpendicular radius 116 against a window of 1.9;
   - no edge lies along a symmetry axis;
   - the 60-orbit is at 16.47°, against 20.08° (Bergman) and 17.78° (Tsai);
   - no face angle can be made from golden-rhombus or Penrose tile angles with up to 6 tiles;
   - the scope: primitive lattice and canonical window only.
2. Include `bridge.py`, `bridge.txt` and the README in P2's Zenodo upload. Move the link from the reference list to the reproducibility section as data: "study and script: commit 3fd407f, studies/2026-10-16-ogdoecontahedron-bridge (also in this record)". The pinned commit URL is good to keep: commit 3fd407f is on both `origin/master` and `origin/research`, so it is permanent.
3. Don't make it a separate paper. It is a short negative check, and P2 is its natural home.

After this, #30's ref 19 is superseded by P2. That needs no new version of #30 (see section 4).

## 7. P3 notes (for later)

- B1 applies ("seven icosahedral solids" in the abstract and §1).
- Add the flip test (section 2, item 3).
- Move §9 and the interlock pointer to P4 (section 3).
- §3's table and the GSD and tight-nest volumes check against the layer differences.
- The checks module section (§10) fits P3 well, because it records the slips honestly.
