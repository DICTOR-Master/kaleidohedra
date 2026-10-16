DICTO · dictospheres.com

# Second review of P4, *Both Cycles in One Space* (Draft 3)

Claude Fable, 16 October 2026. Advice only; no paper files were edited. I read `paper.html`, `both-cycles.pdf`, the four figures, my FABLE-ADVICE.md, the interlock and polar-dharma studies (scripts, data, renders, explorer), the published #32 (*Inverted Shells*) and #31 texts, *Spheres of Dharma*, the TIH paper and the reference library. Checks marked **float** were run here on the study data. They are leads, not proofs.

## Findings first

1. **The science holds.** Tables 1 and 2 add up layer by layer (536 and 502). The 3·I check is exact and on record. The "five of seven inside I" sentence is right (float check below).
2. **Two must-fixes are clerical.** The header says "Draft 1". The bend range is given as float, but #32 already published it exactly.
3. **One claim is too tidy.** "The middle setting does the opposite" hides that the innermost layer is cut in *both* settings, and harder in the middle one.
4. **Two credits are missing.** The cone cut is the Kion construction (*Theaetetus*), as #32 says. Kepler's nested solids (1596) are in the library and are the obvious ancestor a referee will name.
5. **Figures.** Figure 1 should go. The new set below uses the existing three.js pages and the house palette, so the cost is low.

## A. Anything we missed

### Must-fix

- **M1. Header says "Draft 1"** in both HTML and PDF (meta line). Change it to the published version label before upload.
- **M2. Give the bend range exactly, from #32, not as float.** #32 (§4) publishes the two ends exactly: the inner dodecahedron grows by 11/18 + 5√5/18 (= 1.232241), and the outer one shrinks by 5 − 2√5 (1/(5 − 2√5) = 1 + 2√5/5 = 1.894427). So P4's range for scaling I is exactly **[(45√5 − 99)/2, 1 + 2√5/5]** ≈ [0.8115, 1.8944]. Cite #32 for it and drop "(float)". Please re-derive it once with the exact tools before printing. I matched the decimals only.
- **M3. Figure 1, if any part of it stays,** has visible defects:
  - in the ends panel, reversed O and PD are cut off at the bottom edge;
  - "I·φ³" and "O·φ³" labels sit on bars;
  - reversed stations beyond one turn (RT·φ³, PD·φ³) are drawn, though the caption says "one turn";
  - the caption says "dotted lines" for the mirror spheres, but each panel draws only one;
  - the label text "mirror sphere" is struck through by its own line.
  I recommend replacing it (Part B) rather than fixing it.

### Should-fix

- **S1. "The second does the opposite" overstates.** Pieces per original layer, from Tables 1 and 2 (exact counts):

  | Original layer (pieces before cutting) | Ends | Middle |
  |---|---|---|
  | I → ID (20) | 80 | **120** |
  | ID → D (20) | 60 | 20 whole |
  | D → TI (12) | 12 whole | 132 |
  | TI → H (20) | 60 | 20 whole |
  | H → RT (72) | 84 | 180 |
  | RT → I·φ³ (30) | 240 | 30 whole |

  The pattern is real and lovely: the two settings leave *alternate* layers whole (ends: D → TI only; middle: ID → D, TI → H and RT → I·φ³). But I → ID is cut in both, and more in the middle setting.
  - Put this table in §6. It is the cleanest exact summary of "what the toggle moves".
  - Reword the abstract: "the first cuts the outer roofs hardest and leaves the dodecahedron columns whole; the second leaves the roofs, pyramids and tetrahedra whole and cuts the columns".
  - The §5 sentence "the cutting moves to the middle layers" should also name I → ID (120).
- **S2. "One solid" means one turn.** The abstract says "one solid of convex pieces … 536 pieces". The nest is endless, and the count is per turn, I to I·φ³ (a thick shell around the next turn in). Say "one turn of one solid". The README already says this; the abstract does not.
- **S3. Credit the cone cut.** §3 describes it without a source. #32 calls it "the Kion construction of Theaetetus" (DICTO DOI: 10.5281/zenodo.23378070). Cite it the same way.
- **S4. Prior art a referee will name:**
  - **Kepler, *Mysterium Cosmographicum* (1596).** Nested regular solids separated by spheres. It is in the library (`history/Kepler-1596-…pdf`). One sentence in §7 is enough: Kepler nests solids between spheres; here a sphere *reciprocates* one nest into another.
  - **Dechant, Wardman, Keef and Twarock (2014),** nested icosahedral shells in viruses and fullerenes. It is in the library and #32 cites it. It is closer to P4 than Twarock 2015.
  - **The classical dual compound.** Reciprocating in the midsphere makes I and D cross each other. Here the sphere is chosen so that they *nest* and coincide with stations. One clause stops a referee asking "isn't this the compound?"
- **S5. Say which symmetry group counts the kinds.** `geomcheck.kinds` uses the full group Ih (rotations plus reflections, so mirror images are one kind). Add "under the full icosahedral group, mirror images counted as one kind" to §3.
- **S6. The "3 is not a power of φ" step deserves its one-line reason.** For any integer k ≠ 0, φᵏ = (Lₖ + Fₖ√5)/2 is irrational, so it is never 3. A referee will want that clause.

### Optional

- **O1. A sentence a layman can hold:** the toggle sphere sits at the geometric mean of the two radii it pairs. In the ends setting, ρ² = (I's corner radius) × (D's face distance). This follows from the polar rule r → ρ²/r. Float check: 0.5878 × 1.1135 = 0.6545 = φ²/4. The middle setting is the same with ID and RT.
- **O2. A nice exact aside from Table 1:** in the ends setting, each ID → D tetrahedron, (1 + √5)/192, is cut into three equal four-sided pyramids, I1·11 = (1 + √5)/576. Check congruence before stating it (same volume is shown; same shape is not).
- **O3. Table 1's code list names HPy, but no HPy appears in Table 1.** Harmless. You could give each table its own list.
- **O4. Figure 2 (section):**
  - Each layer is filled in two alternating tones, and the legend does not say so.
  - In the middle panel, a near-coincident pair of lines runs through D → TI. Name them in the caption, or add a zoom.
  - The axis numerals (2, 3, 5) float far from the solid. Put them at the boundary.
- **O5. Data hygiene:** the TI station's float list holds 8 points that are not corners (`middle-icosa-3I.txt` says so). This is harmless to the radii. Clean it, so that later scripts do not trip on it.
- **O6. Float check of "five of the reversed turn's seven stations lie inside the original icosahedron":** confirmed. D, ID, O and PD lie inside, and the fifth is I itself. RT and D·φ³ lie outside. This came from a hull test on `orig-chain.json` / `flip-ends-chain.json`.

## B. Figures a layman would love, still exact

**Principle.** Show the real solid first, then the explanation. Use the house look DICTO liked on #31 and #32:
- warm background `#f4f1ea`, ink `#2b2620`;
- the same layer colours as the section (I→ID `#4dd0e1`, ID→D `#c792ea`, D→TI `#5fd38a`, TI→H `#f08fc0`, H→RT `#9fd8ff`, RT→I·φ³ `#ff9a52`);
- flat shading, thin dark edges, the "DICTO · dictospheres.com" tag bottom right.

Every render is drawn from float corners of exact pieces. Every caption says so in four words: "(drawn from exact pieces)".

**What already exists (so the cost is low):**
- `render_interlock.html` + `shoot_interlock.mjs`: ends data, orthographic, fixed axes (`views` in `interlock-render.json`), clip plane, a 0.985 shrink for seams, the DICTO tag.
  - Its outer colour `0x8d6e63` is a muddy brown. Swap `WARM` for the house list above.
- `render_kinds.html` + `shoot_kinds.mjs`: one piece per page, shaded. It already looks good (`renders/kinds-ends.png`), but each piece fits its own frame.
- `render_polar.html`: closed, cut, inner and apart modes. `render_toggle.html`: whole and cut. `render_movie.html`: a toggle movie by `frame(t)`.
- Middle data: `interlock-middle.json` has the same `v`, `f` and `o` keys as the ends data. It is in the same frame, so reuse the ends `views`. The middle data has no `g` (reversed layer); add it if you colour by reversed layer.
- `interlock-ends.json` and `interlock-middle.json` carry `vol` per piece. Tag each piece with its kind by matching to `interlock-kinds.txt`. This takes a few lines in `interlock_render_data.py`.

### Proposed set (four figures)

**Fig. 1: "Both cycles, one solid" (hero; replaces the ladder).**
- *Shows:* the interlock for both settings side by side. Each is a quarter cut away, like a cake with a slice removed, so the rings of layers and the seams of the cuts show on a real solid.
- *Why a layman gets it:* it looks like an object, and the eye goes straight to the rings and the shattered or whole bands.
- *Spec:*
  - Two panels, 1200 × 1200 each, so 2400 × 1250 in all.
  - Data: `interlock-render.json` (ends) and `interlock-middle.json`.
  - Drop whole pieces whose centroid lies in the 90° wedge between two mirror planes, both containing the five-fold axis nearest the camera. Dropping whole pieces is honest; clipping makes double-sided artefacts.
  - Orthographic camera on a fixed oblique bearing: dir = normalize(0.8·three-fold + 0.5·five-fold), as in #31's `hstar-oblique`, minus its small symmetry-breaking offset; a two-fold axis up.
  - Fill by original layer; reversed cuts show as seams (0.985 shrink, ink edges). No labels on the image except "Ends: shares I and D" and "Middle: shares ID and RT".
- *Caption:* "The interlock in its two settings, one quarter removed. Colours are the six layers of the Spheres of Dharma; every seam is a cut by the reversed cycle. Ends setting (536 pieces per turn): the outer roofs are cut finely. Middle setting (502): the roofs are whole and the cutting moves inward. Drawn from exact pieces."

**Fig. 2: "The toggle as rings" (replaces the ladder's job; it is exact).**
- *Shows:* the full flat section z = 0 (all 360°, not a quarter) of the *stations only*, no pieces. Original stations are warm closed outlines with their layers lightly filled. Reversed stations are cool outlines. Shared stations are thick ink. The toggle sphere is a dashed circle labelled ρ = φ/2 or ρ = √3·φ/2. Two panels.
- *Why a layman gets it:* tree rings. Two families of rings, and in each setting two rings coincide. You see "the cycles share I and D here, ID and RT there" with no log axis.
- *Spec:* reuse the section-cutting code in `p4_figures.py`, applied to the station hulls in `orig-chain.json` and the reversed chains at both settings. The section has two-fold symmetry, so draw it full. 2200 × 1150. Label rings at the right edge (I, ID, D …), never on the lines. Keep the layer fill alpha around 0.25, so the cool outlines read.
- *Caption:* "One flat cut through the centre, both cycles. Warm rings are the original stations, cool rings the reversed ones. The dashed circle is the sphere of reciprocation; where it sits decides which rings coincide (thick). (a) ρ² = φ²/4: I and D shared. (b) ρ² = 3φ²/4: ID and RT shared. No sphere gives both. Exact section."
- The current Fig. 2 (quarter section of pieces) can then become a **small technical inset** of Fig. 2, or move into Fig. 3.

**Fig. 3: "Layer by layer: where the toggle cuts" (the peel).**
- *Shows:* two rows (ends, middle) × six tiles, one per original layer, inside to outside. Each tile shows that layer's pieces alone, half removed (the same wedge rule as Fig. 1), seen on the same bearing. Under each tile is its exact piece count from the S1 table: 80 · 60 · 12 · 60 · 84 · 240, and 120 · 20 · 132 · 20 · 180 · 30.
- *Why a layman gets it:* you can see at once which shells are whole and which are shattered, and that the pattern flips. This is the "exploded view" that works. The earlier per-chamber explode failed because it scattered nine pieces; this keeps each layer intact as a shell.
- *Spec:* the same page with `?layer=k&set=ends|middle`. Tiles 500 × 500, so 3000 × 1150 in all. Fill in the layer colour; whole layers have no internal seams, which is the point. Optionally tint each piece by its reversed layer (the COOL map in `render_interlock.html`) for a second version in the record.
- *Caption:* "Each layer of one turn, alone, in the ends (top) and middle (bottom) settings, with its number of interlock pieces (exact). The settings leave alternate layers whole."

**Fig. 4: "The kit" (replaces Figs. 3–4; one per set, or two rows).**
- *Shows:* one piece of each kind, as a set of parts. Each piece is shaded in three.js, **all at one common scale**, with "I1·n · ×60 · shape code" under it. A small locator sits beside each piece: the Fig. 1 hero at about 140 px, with that kind's pieces in colour and the rest pale grey.
- *Why a layman gets it:* "12 kinds of parts build the whole thing" is the most inviting fact in the paper. Seeing where each part lives answers "where does this go?"
- *Spec:*
  - `render_kinds.html` with a new `&s=<fixed half-width>`, set by the largest piece (I1·1 / I2·1), so sizes compare truly.
  - Keep its current lighting and colours.
  - Locator: hero page with `&hi=<kind>`, which needs the kind tag (see above).
  - Grid 4 × 3 (ends) and 4 × 3 with one empty slot (middle), 2000 × 1700 each.
  - Add a 1-unit scale bar.
- *Caption:* "The parts of Interlock set 1 (Dharma-Ends): 12 kinds, 536 pieces per turn, one of each shown at a common scale with its count; the small view shows where that kind sits. Drawn from exact pieces; exact volumes in Table 1."

**Optional Fig. 5 / online only:** a 6-second loop from `render_movie.html?toggle`, the sphere sliding between the settings. Use it for the website and the Zenodo record, not the PDF.

**Keep / drop:**
- *Drop* the ladder from the paper. Keep `p4-ladder.png` in the study record.
- *Keep* the quarter section as an inset (Fig. 2b) or in the record.
- *Retire* the matplotlib galleries in favour of Fig. 4, keeping their locator idea.

**Rules check:** pure geometry, no Zome framing, DICTO tag on every image, orthographic fixed bearings, and "drawn from exact pieces" / "exact section" in the captions. Counts and volumes come only from `interlock-kinds.txt`.

## Recommended next steps

1. Fix M1 and M2: the version label, and the exact bend range with a #32 citation, re-derived once exactly.
2. Add the S1 per-layer table to §6 and reword the abstract and §5 as in S1; say "per turn" (S2).
3. Add the credits: Kion / *Theaetetus* (S3); Kepler 1596, Dechant et al. 2014 and a dual-compound clause (S4). Add the Ih and φᵏ clauses (S5, S6).
4. On dicto-node, as one logged background job: tag kinds in the render JSON; add the `wedge`, `layer`, `hi` and `s` parameters; swap in the house palette; shoot Figs. 1–4.
5. DICTO picks among the renders, especially the hero bearing, before the captions are final.
6. Rebuild the PDF, check every number against Tables 1–2 and #32, publish, then the Collected Works version (standing rule).
