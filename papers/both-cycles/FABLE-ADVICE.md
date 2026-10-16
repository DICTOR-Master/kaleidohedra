DICTO · dictospheres.com

# Advice on P4, *Both Cycles in One Space*

Claude Fable, 16 October 2026. This is advice only. No paper files were edited. I read Draft 1 (`paper.html` and its figures), the interlock and polar-dharma studies, my earlier reviews, the published Inverted Shells PDF (#32) and the published *Capturing the In-betweens* (v3). Results labelled **float** come from quick checks I ran here on the study data. They are not exact proofs.

## Decisions first

1. **Publish P4 soon. Do not wait for the Kaleidohedra app.** Replace the figures first, and look at the interlock yourself in the Polar Dharma Explorer, which already exists.
2. **Keep the seven-station line-up with the Hecatodihedron.** State it as a choice in one short paragraph. That choice is what gave us the Ogdoecontahedron.
3. **Explore the other line-up as a separate study, and a later paper if it earns one.** Do not add it to P4 now. It changes the toggle story, so it deserves its own treatment.
4. **Use four figures:** a radial ladder, a flat section, an exploded wedge and the kinds gallery redrawn. Drop the two see-through wireframes.
5. **The Engine paper does not change the plan.** P4 goes first.

## A gentle correction on what I said before

You remember my point as "the Hecatodihedron wasn't in the reversed line-up". My point was the other way round. The *published* Spheres of Dharma has six stations (I, ID, D, TI, RT, I·φ³), and the Hecatodihedron is not one of them. It is stage 7 of the TI → RT layer (*In-betweens*). Inverted Shells **added** it as a seventh station. Its polar is the Ogdoecontahedron. If you reciprocate the six published stations alone, you get classical solids only. So this was never an error. It was an extra station, chosen on purpose, and #32 already says so correctly ("taking the six solids and the Hecatodihedron stage as seven stations").

## 1. Publish now, or build and view first?

**Recommendation: publish now, after a viewing session in the existing Explorer. Do not wait for the app.**
*Reason: every claim in P4 is already exact (remainder 0 in ℚ(√5)), so a build adds no proof.*

- **What building and viewing adds to the science:** nothing that is not already proven. It is still a useful independent check. Mistakes in orientation, colour or labels show up at once when you turn the solid by hand.
- **What it adds for readers:** a lot. An interactive view is the clearest way to understand an interlock. A link can go into Version 2.
- **What it costs:** app work across both doors, a smoke test, and pushes against the Vercel limit (each K push uses 3 deploys). It would delay P4 by days, for figures you can make now.
- **The cheap middle way:** the interlock is already the third tab of the Polar Dharma Explorer (`studies/2026-10-16-polar-dharma/explorer`), with an ends/middle switch. Spend half an hour with it before publishing. That is the "viewed" step that matters. Make the new figures from the same data.
- **A physical print** of the full interlock (536 pieces) is a project of its own. Printing one five-fold sector would be a lovely check later. It is not needed for publication.

## 2. The line-up

**Recommendation: keep the seven stations with H in P4. Frame it as a stated choice. Study the alternative separately.**
*Reason: H is the natural choice, since it is the main-route stage. The alternative changes which stations the toggle shares, so it is its own result.*

**How many stations are possible?** The In-betweens data (`studies/2026-10-13-fused-shells/stages-facts.json`) lists exactly 8 convex whole-ring Dharma stages:

- I, ID, D, TI, H, RT and I·φ³;
- and one more that the paper does not name: **TI plus its 12 pentagonal caps, without the Shields, which is the icosahedron 3·I.** It is the truncated icosahedron's parent with its corners restored. Its 12 corners are the RT's five-fold corners.

Float checks:

- the TI corners lie on the edges of 3·I to 2×10⁻¹⁶;
- 3·I lies inside RT, touching it;
- H and 3·I each poke out of the other (by 0.20 and 0.32), so **they cannot both be stations**.

Other candidates fail:

- The dimpled stages are not convex, so their polars are not solids of the same kind.
- The 45 convex partial stages lack full icosahedral symmetry, so they would break the cone cut and the kind counts.

So there are exactly three honest line-ups:

| Line-up | Reversed chain | Toggle settings | "Never both" | Interlock |
|---|---|---|---|---|
| **A. Six published stations** | D ⊂ ID ⊂ PD ⊂ I ⊂ RT ⊂ D·φ³, all classical | unchanged | holds | counts change (not computed); no new solid |
| **B. Seven with H (P4)** | adds the Ogdoecontahedron | ends shares I, D; middle shares ID, RT | holds | 536/12 and 502/11, exact |
| **C. Seven with 3·I** | adds a dodecahedron D/3, between ID and PD; all classical | ends shares I, D; **middle shares ID, RT, D and 3·I** (float) | needs rewording | not computed |

**What survives in every line-up:**

- The two settings themselves.
- The φ^(3/2) mirror spheres.
- The factor-3 exclusion argument.
- The loose-end bend range.

All of these use only I, ID, D and RT. The bend range is set by I's neighbours, ID and RT.

**What changes:**

- The interlock counts and kinds always change.
- In C, the middle setting also shares the dodecahedron, because 3·I is exactly 3 times I and the middle sphere is exactly 3 times the ends sphere. The clean picture "ends shares the ends, middle shares the middle" turns into "the middle setting shares four stations".

That is a real new result. It is too big for a side section of P4.

**How P4 should frame the choice:** add one paragraph in §1, in plain terms:

> "Which closed stages count as stations is a choice. The TI → RT layer has two convex intermediate stages: the Hecatodihedron (stage 7, on the main route) and the icosahedron 3·I (TI with its 12 caps, reached by skipping the Shields). Neither contains the other, so at most one can be a station. Inverted Shells chose the Hecatodihedron, and that choice produced the Ogdoecontahedron. We keep it. The six classical stations alone give classical polars only."

Your point stands, and the paper can say it plainly: going beyond the published six is exactly what led to the discovery. The same reasoning is why line-up C is worth a study.

**One fact P4 should add,** once it has been confirmed with the exact tools: in P4's own middle setting, **the reversed icosahedron is exactly 3·I**. That is the TI-plus-caps stage of the original cycle, an in-between stage that is not one of the seven stations. I checked this in float, and it follows exactly from the factor 3. It explains why the TI → H pyramids pass through whole in that setting.

## 3. Figures

**Recommendation: four figures, all orthographic, at fixed bearings with a two-fold axis up, carrying the DICTO mark.**
*Reason: a reader needs to see one scale picture of the toggle and one exact section of the cut. 3D wireframes give neither.*

- **Fig. 1, the toggle ladder (replaces the radial strip).**
  - Two panels, ends and middle. Each has two vertical log-radius axes, original on the left and reversed on the right, covering one turn only.
  - Draw each station as a short bar from face distance to corner radius, with its abbreviation beside it.
  - Draw one horizontal black bar for each shared station, one dashed line for the toggle sphere, and one for a mirror sphere.
  - Leave out the grey polar lines; they turn into a starburst.
- **Fig. 2, the section (the key figure, replaces Fig. 1).**
  - A flat cut through the centre in a mirror plane, which contains a five-fold, a three-fold and a two-fold axis. It is exact and needs no transparency. Show the ends and middle settings side by side.
  - Draw the original layer boundaries as warm solid lines and the reversed boundaries as cool solid lines. Draw shared surfaces as thick black lines.
  - Fill the regions lightly by original layer, and label the layers at the edge.
  - Mark the 5/3/2 axes. The reader should see at once that the roofs are cut in one setting and the columns in the other.
- **Fig. 3, one exploded wedge for each setting.**
  - Show one five-fold sector (1/12 of the solid). Push its pieces outward along the radius, colour them by original layer, and label them I1·n / I2·n.
  - This shows how the kinds fit together.
- **Fig. 4, the kinds gallery, redrawn.**
  - Keep it, but show every piece at one common scale, or add a scale bar, all at one bearing.
  - Add a small locator inset (the Fig. 2 section with the piece's region shaded).
- **Drop:** both see-through 3D wireframes (`toggle-ends-cut`, `toggle-middle-cut`). They are unreadable at print size.

## 4. Fact-check (against the published #31/#32 PDFs and the study data)

- **Correct:**
  - The six-station wording matches #32.
  - The reversed chain matches #32.
  - The bend-range numbers match #32 (×1.894, ×1.232).
  - Tables 1 and 2 match `interlock-kinds.txt` row by row (counts, corners, faces, exact volumes).
  - The 174 original pieces add up (20+20+12+20+72+30).
- **Overstated:**
  - §2 says the ends setting's "reversed turn nests almost entirely inside the original icosahedron". Six of its seven stations do lie within the icosahedron's corner sphere. But its last layer, RT → D, reaches out to the original dodecahedron and holds about 93% of the turn's volume (float: 7.66 vs 0.59).
  - Suggested rewording: "six of its seven stations lie inside the original icosahedron".
- **Unclear:**
  - §3 says "each cycle is *already* cut into convex pieces". That is true for the reversed cycle (#32's 154 pieces), but not for the original. Its 174 cone-cut pieces are new here, and they are not the Dharma's own 237 pieces.
  - Say "we cut the original cycle the same way (174 pieces, not the Dharma's 237)".
- **Misleading abbreviation:** "Dod" for the 12-faced pieces (5 triangles and 7 pentagons) will be read as "dodecahedron". Use a neutral code, for example "12-face".
- **Missing citation:** §1 relies on *Capturing the In-betweens* (DICTO DOI: 10.5281/zenodo.23345502) for "stage 7". Cite it, as #32 does.
- **Exclusion argument:** it is sound. Add one clause saying why only two pairs exist. Among the stations' polars, only I ↔ D and ID ↔ RT give back stations, since TI → PD and H → O give solids that are not stations. Then "no sphere gives both" is complete.

## 5. The Engine paper

**Recommendation: P4 does not wait for it. Write the Engine paper after P4, and use the interlock as its worked example.**
*Reason: P4's results stand on the study scripts, not on the app. The Engine paper describes tooling, which is a separate claim with a separate audience.*

When the app gains an interlock view, add the link in P4 Version 2 and in the Engine paper.

## Recommended path

1. View the interlock in the Polar Dharma Explorer (both settings), about 30 minutes.
2. Make the four figures from §3 from the existing data, and drop the two wireframes.
3. Apply the §4 fixes and the §2 "choice of stations" paragraph. Check exactly that the middle-setting reversed icosahedron is 3·I before stating it.
4. Publish P4, then a new Collected Works version (the standing rule).
5. Open a study for line-up C (3·I): exact chains, the toggle, and the interlock. Decide on a paper only after you see what it gives.
6. Engine paper after that, with the interlock as an example. Add the app link in P4 v2.
