# Special geometry of the human sacrum: the real bone measured, the traditions checked (12 Nov 2026)

DICTO · dictospheres.com. Study folder `studies/2026-11-12-sacrum-geometry` (scripts `scripts/`, data `data/`, figures `figures/`;
full run log `data/sacrum-full.log`: 18 of 18 controls ok, FINAL ok).

**Conclusion.** The sacrum is a real, measurable wedge: an inverted triangle seen from the front (triangle fit IoU 0.82 ± 0.04 on 60 CT
sacra, apex angle 52 ± 5°, not equilateral), wedged downward between the hip bones (auricular planes converge downward by 18 ± 10°)
and wider in front than behind (they converge backward by 32 ± 15°, so it is not a keystone in the horizontal plane). Its front
face is curved close to a circular arc (radius about 65–85 mm); a logarithmic spiral fits no better, and its growth rate is not the
golden one. No proportion of the sacrum sits at φ: across 14 sacral ratios the rate of "near a notable constant" (25–30 % at ±2 %)
is the same as for the lumbar vertebrae and as for random numbers, and φ turns up as often as chance (2.5 % against 3.2 %).
The "sacred" in the name is documented as Greek (Hippocratic, then Galen); why it was sacred is not settled by any source.

## Question

DICTO's idea, in his words: "special geometries of the human bones and skeleton, I think the first bone to start on would be the
sacrum, as it has a sacred position in several ancient spiritual and even geometric traditions". Approved as A + C: (A) measure a
real sacrum exactly; (C) check the traditions, separate the documented from the repeated, and test every geometric claim with A's numbers.

## Data and provenance

| source | what | licence | count used |
|---|---|---|---|
| BodyParts3D 4.0 (The Database Center for Life Science, DBCLS, Japan), `partof_BP3D_4.0_obj_99.zip` from https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/ | sacrum FJ3393 (FMA16202), L5 FJ3168, L4 FJ3165, right hip bone FJ3152, left hip bone FJ3288, right scapula FJ3384 | CC BY 4.0 (current licence page; the 2013 OBJ headers still say CC BY-SA 2.1 JP) | 1 specimen (one adult male body) |
| TotalSegmentator small set v2.0.1 (Wasserthal J. et al., Radiology: Artificial Intelligence 2023), Zenodo record 10047263 | masks sacrum, vertebrae_L5, vertebrae_L4, hip_left, hip_right per CT; meta.csv (age, sex) | CC BY 4.0 | 60 of 102 CTs (36 m, 23 f, 1 unrecorded); 29 had no sacrum, 9 had it cut by the scan edge, 4 lacked L5 or a hip bone |

SHA256 (BodyParts3D): zip `9fbc713fffeee924a5a657d9813d84d7eb957bded63adb854931dd5e3eb61c97`; FJ3393 `fd95a0b26f450e4939858c9effb7b14e589874c9210edfdb92e8f4552dd484de`;
FJ3168 `884ef6993f9578f86a6441ca7016f647f22778a9ab850189e1863d5f4112001d`; FJ3165 `e30bc2a914a50d097dc5824cacbe54be10fc68c9f43cd9ef023519bc146cab61`;
FJ3152 `708e42cba3d1817230c98410c80742875d56bb5b3e688a566f62509c7a63e424`; FJ3288 `981411a910d502c80e454cc95128a9812a1284202295d1ebc7ab5020a08d83aa`;
FJ3384 `cb68b2e01a22989f20e602d5036a3f1fb28448fe647f599b9bbd61edfbff2320`; partof_element_parts.txt `3f5f6df1028eb122b30de77c711597b6bb8e5541658e5985859fd228adbf88ea`.
TotalSegmentator: the 3.2 GB zip was not downloaded; `scripts/fetch_ts.py` reads only the needed members by HTTP range requests
(zip CRC32 checked on every read); every file's SHA256 is in `data/provenance-totalsegmentator.tsv`. The CT masks are 1.5 mm voxels.
Downloads went into a fresh empty folder on the compute machine and were treated as untrusted data (python -I, paths as arguments).

**One model is not a population.** BodyParts3D is one man's body. The 60 CT sacra are a population, but an uncontrolled one
(clinical scans, ages 20s–90s, automatic segmentations at 1.5 mm). Neither source labels the coccyx separately; BodyParts3D has no
coccyx part, and the distal tip of both looks like sacrum plus coccyx, so every length "to the tip" may include the coccyx (see Limits).

## Method (`scripts/sacrum_geom.py`)

- Masks → meshes by marching cubes (Gaussian σ 0.6 voxel, level 0.5); meshes sampled at 12 points/mm².
- Frame from the neighbours: left = hip-bone centroid difference; up = towards the L5 centroid; front = left × up.
  S1 end plate = largest patch of sacrum faces facing L5 within 20 mm of the midline and 25 mm of L5; B = its centroid; promontory =
  its most anterior midline point; tip = midline point farthest from B. Sacral frame: chord axis B–tip, front ⟂ chord.
- Front view: front-most depth per 0.5 mm pixel. Full outline = whole silhouette; pelvic face = front-facing pixels (normal·front > 0.5)
  below the end plate. Triangle, curved triangle (three circular-arc sides) and wedge (general quadrilateral) fitted by max IoU.
- Anterior foramina = pits deeper than 2 mm under a 7 mm grey closing of the depth map; paired left/right (same level ± 7 mm, mirrored ± 10 mm),
  four pairs at least 8 mm apart. Segment boundaries: promontory, the four pair levels (Gray: the foramina lie at the ends of the four
  transverse ridges), tip. Lengths along the chord and along the anterior midline arc.
- Curvature: the anterior midline profile (front-facing points, |x| < 3 mm, 1 mm bins; end-face points trimmed until the end point is
  within 1 mm of the circle through the rest, at most 10 per end) fitted by a circle and by a logarithmic spiral r = a·e^{bθ} with free centre;
  BIC compares them; 60 bootstrap resamples give 95 % intervals. Golden spiral: b = ln φ/(π/2) = 0.3063.
- Wedge: auricular surface = sacrum faces within (closest gap + 3 mm) of each hip bone; plane fit; total angle between the two planes,
  and its frontal and axial parts (axial negative = narrower behind; frontal negative = narrower below, see the sign note in the script).
- "Near a constant": 12 constants (φ, φ², √φ, √2, √3, √5, 3/2, 4/3, 5/4, 2, π/2, e/2); ratios folded to ≥ 1; near = within ±1 % or ±2 %.
  Chance = the share of [1, 3.5] (log scale) lying within the tolerance of any constant: 18.8 % at ±1 %, 33.7 % at ±2 %; φ alone 1.6 % / 3.2 %.
  The same 8-ratio shape battery (PCA extents, silhouette widths at 25/50/75 %, height/width, perimeter ratio) is run on the sacrum and on
  the non-sacred controls (L5, L4; plus hip bone and scapula for BodyParts3D).
- Uncertainty: foramen level ± 1 mm (the phantom recovers hole centres within 0.95 mm), propagated to every level-based ratio.

## Controls (all ok; `data/sacrum-full.log`)

cone (triangle IoU 0.993, apex 53.26° vs 53.13°, W/H 1.0000); sphere (R 49.992 vs 50, spiral b −0.0001); golden-spiral arc of 69° (b 0.3063
recovered); chance model (Monte Carlo = exact union, ±0.001); sacrum phantom built as a voxel mask through the same marching-cubes path:
curved plate R 110 mm with 4 pairs of radial holes, an L5 block and two hip slabs → frame signs right, R 110.85 (rms 0.09), 4 pairs found,
centres within 0.95 mm, segment ratios within the propagated error (z 0.84), frontal wedge −38.5° vs −39.0°, axial −8.3° vs −8.6°.
Pilot first (≤ 5 min; four reruns, each fixing what a control caught: IPv6 hang, end-face points in the profile, ratio tolerance, S1 start).

## Results

### BodyParts3D sacrum (one specimen; `figures/fig1-bp3d-sacrum.png`)

| quantity | value |
|---|---|
| breadth (full outline) | 118.0 ± 0.5 mm |
| promontory → tip (straight) | 132.9 mm (likely includes the coccyx) |
| outline: triangle / curved triangle / wedge IoU | 0.873 / 0.881 / 0.875 (pelvic face 0.889 / 0.906 / 0.891) |
| best triangle angles | base 64.0°, 63.9°; apex 52.0° (pelvic face 65.0°, 63.4°, 51.5°) |
| S1 end plate area | 1224 mm²; disc gap to L5 10.0 mm |
| foramen pair levels below B | 28.5, 46.7, 66.0, 83.9 mm (left–right level difference ≤ 0.05 mm; midline offset ≤ 0.13 mm) |
| transverse spacing of pairs 1–4 | 41.7, 34.2, 31.3, 29.6 mm (± 1.4) |
| segments S1…S4 along the chord | 26.2, 18.2, 19.3, 17.9 mm (± 1.4); along the arc 32.5, 24.1, 21.1, 18.6 mm |
| S1/S2, S2/S3, S3/S4 (chord) | 1.45 ± 0.14, 0.94 ± 0.10, 1.08 ± 0.12 |
| foramen spacing ratios 1/2, 2/3, 3/4 | 1.22 ± 0.07, 1.09 ± 0.07, 1.06 ± 0.07 |
| curvature, whole front | circle R 64.9 mm (95 % 63.2–66.4), rms 1.57 mm; spiral b 0.007 (95 % 0.002–0.081), rms 1.57; BIC prefers the circle (123.1 vs 127.8) |
| curvature, base to 4th pair | circle R 83.0 mm, rms 1.39; spiral b 0.19 (95 % 0.13–0.23), rms 1.37 |
| base angle (end plate normal vs chord, sagittal) | 4.0° |
| auricular planes | total 47.1°; frontal −36.8° (narrower below); axial −31.5° (wider in front); areas 1488 / 1939 mm², plane rms 2.1 / 2.2 mm |

Reading: S2, S3 and S4 are equal along the chord (18.2, 19.3, 17.9 mm, all within the ± 1.4 mm error): an even step, not a golden
progression (a golden progression needs ratios 1.618; measured 0.94 and 1.08). The foramina are mirror-exact to 0.1 mm and their
spacing narrows downward by 22 %, 9 %, 6 %, so the narrowing slows; no constant ratio.

### 60 CT sacra (TotalSegmentator; `data/population-full.csv`, `figures/fig2…fig4`)

mean ± SD (n): breadth 122.1 ± 6.9 mm (60); promontory → tip 127 ± 18 mm (60); triangle IoU full outline 0.82 ± 0.04, pelvic face
0.86 ± 0.04; curved triangle 0.87 ± 0.04 / 0.90 ± 0.04; wedge 0.85 ± 0.04; triangle apex angle 52.3 ± 5.5° (mean 95 % CI 50.9–53.7°);
pelvic face width/height 0.93 ± 0.12; breadth/length index ×100: men 95.5 ± 12.0 (36), women 102.2 ± 18.9 (23) — women wider, as in every
published series, but lower than published means (men 98–112, women 113–116) because our length may run into the coccyx; curvature circle
R median 72 mm (fit rms median 2.6 mm), circle preferred by BIC in 65 % of sacra, spiral |b| median 0.11 (only 10 % within ± 0.03 of the
golden 0.306); base angle 15 ± 11°; auricular total 39 ± 9°, frontal −18 ± 10° (narrower below), axial −32 ± 15° (wider in front).
Foramen pairs: all four found in 29 of 60 (CT masks at 1.5 mm close the small lower foramina). The population segment ratios are
bimodal (S1/S2 CV 47–108 %), a sign of detection errors, so segment and foramen-spacing ratios are reported from BodyParts3D only.

### The golden-ratio test (`figures/fig3-near-constant-test.png`)

| set | ratios | near any constant, ±2 % | near φ, ±2 % |
|---|---|---|---|
| chance (log-uniform on [1, 3.5]) | — | 33.7 % | 3.2 % |
| 60 sacra, 14 sacral ratios | 522 | 29.5 % | 2.5 % |
| 60 sacra, shape battery | 480 | 44.8 % | 4.6 % |
| 60 L5, shape battery | 475 | 28.2 % | 3.2 % |
| 60 L4, shape battery | 419 | 25.8 % | 2.1 % |
| BodyParts3D sacrum, 14 sacral ratios | 14 | 14 % | 0 % |
| BodyParts3D hip bone / scapula, battery | 8 / 8 | 50 % / 75 % | 0 % / 0 % |

No sacral ratio has a population mean within 2 % of φ. φ lies inside the 95 % interval of the mean only for breadth/(base to 4th pair)
(1.56 ± 0.33 SD), together with 3/2 and π/2: the interval is wide, not φ-specific, and individuals spread 21 %. The sacrum battery's higher
"any constant" rate comes from ratios clustered at 1.2–1.4, where four constants crowd together (5/4, √φ, 4/3, e/2 gave 149 of its 269 constant matches);
its φ rate (22/480) is within 2 SD of chance. The scapula, a bone with no sacred tradition, scores highest of all at ±2 %.

## Part C: the traditions, checked

Research by web sources (list below); a research agent gathered and quoted them, and every claim used here is tied to its source.

**The name.** Documented: Greek ἱερὸν ὀστέον, Latin os sacrum. Liddell–Scott–Jones (ἱερός II.10) cites the Hippocratic *On Joints* 45
before Galen (*De usu partium*, "UP 5.8" in LSJ), so the usual line "Galen named it" is doubtful: Galen used an older term. Galen's Kühn
page was not verified. Merriam-Webster: Late Latin os sacrum, translating hieron osteon; English from 1753. The competing explanations:
(a) the bone offered in sacrifice — the dictionary favourite (American Heritage; Etymonline), with Greek sacrificial practice burning
the osphys (sacrum and tail); (b) ἱερός as "mighty" (Homeric sense in LSJ: ἱερὴ ἲς Τηλεμάχοιο, Od. 2.409), hence "great bone" (Wikipedia,
Wiktionary; Brewer 1895 credits a Dr Nash) — the bone is the largest of the spine; (c) the indestructible resurrection bone — a later
merging with the rabbinic luz (Brewer 1895), not in any Greek source; (d) protector of the "sacred" genitals — popular only, no ancient
source found. Oscar Sugar (JAMA 1987; Spine 1995) and Nihal Ojumah & Marios Loukas (2018) call the origin unclear; German *Kreuzbein*
means the croup (Joseph Hyrtl 1880), not the cross; Greek also had *klonis*, Latin *os latum* ("broad bone"). Brian Stross (UT Austin)
reports Mesoamerican names of the bone built on words for the sacred (not read in full). **Verdict: the "sacred" is real and ancient;
its reason is open; (a) and (b) have evidence, (c) and (d) are later additions.**

**Yoga and kundalini.** Documented (Sir John Woodroffe, as Arthur Avalon, *The Serpent Power* 1919, translating Pūrṇānanda's
*Ṣaṭ-cakra-nirūpaṇa*, 1526): the mūlādhāra lotus lies "below the genitals and above the anus" (v.4), holds a square (v.5) and a
"lightning-like triangle" called Traipura (v.8), with the Svayambhu-linga "head downwards" (v.9); the kanda is "two fingers above the
anus". *Haṭha Yoga Pradīpikā* III: the bulb above the anus, Kuṇḍalī coiled on it. **The texts never name the sacrum or the coccyx, and v.8
does not say the triangle points down**; the downward triangle is later iconography (Harish Johari via Hinduism Today; nathas.org), and
"the sacrum is the mūlādhāra" is modern teaching (Richard Rosen, Yoga Journal; Yoga International). Nothing testable in the primary texts.

**Egypt.** Documented: Book of the Dead spell 155, the djed amulet as Osiris's backbone and vertebrae (Art Institute of Chicago cat. 95;
Brooklyn Museum); raising the djed (Hodel-Hoenes 2000; Najovits 2004). Plutarch (*De Iside et Osiride* 15–16) tells of the pillar at
Byblos but never names the djed. The sacrum specifically: Andrew H. Gordon and Calvin W. Schwabe (*The Quick and the Dead*, 2004, after
Schwabe, Adams & Hodge 1982) argue the djed is the **bull's** sacrum and lumbar vertebrae — published, contested, and about cattle, not
people. "The djed's four bars are the human sacrum" is popular repetition (websites; bar counts vary 3–4). Nothing testable for the human bone.

**The luz.** Documented: Bereshit Rabbah 28:3 (R. Yoḥanan for R. Shimon b. Yehotzadak): "the luz of the spine" from which the dead are
raised; Hadrian and R. Yehoshua b. Ḥananya grind, burn and soak it and it survives; Kohelet Rabbah 12:5. Its place varies by later
source: top of the spine, "the coccyx at the bottom of the eighteen vertebrae", Zohar's "head of a snake"; Julius Preuss and Saul Lieberman:
coccyx. Scholarship: Fielding H. Garrison 1910; Edward Reichman & Fred Rosner 1996; Robert Shapiro 1987. **The sources say spine or coccyx,
never sacrum; "luz = os sacrum" is Brewer 1895.** Vesalius's mockery of the luz was not verified from the Fabrica text. Nothing testable.

**Sacred-geometry claims.** No source found states a numerical golden-ratio claim for the sacrum (only generic body-φ claims); no
pentagram/"five" claim with sourced text. Documented anatomy behind the popular images: Gray's "large, triangular bone ... inserted like a
wedge between the two hip bones"; "keystone of the body" (Kenhub) against Ibrahim Kapandji's "suspended" sacrum (Rick Serola 2019, hammock
not keystone).

### The testable claims, tested with Part A

| claim | source type | test | result |
|---|---|---|---|
| the sacrum is a (downward) triangle | anatomy (Gray) + popular | triangle IoU | holds approximately: 0.82 ± 0.04 (pelvic face 0.86); a curved triangle fits better (0.87–0.90) |
| the front face is equilateral | derived claim | apex angle 60°? | **no**: 52.3 ± 5.5° (mean CI 50.9–53.7°); BodyParts3D 52.0° |
| breadth/length = φ (index 162) | generic popular | sacral index | **no**: 95–102 here, 98–116 in published series |
| segments in golden progression | none found; derived | S1/S2…S3/S4 = 1.618? | **no**: BodyParts3D 1.45 ± 0.14, 0.94 ± 0.10, 1.08 ± 0.12; S2–S4 are equal steps |
| sacral curve a golden spiral | popular "spiral" images | spiral b = 0.306? | **no**: circle fits as well or better (BIC, 65 % of sacra); BodyParts3D b 0.007 (whole) / 0.19 (to S4) with intervals excluding 0.306; 10 % of CT sacra within ± 0.03 |
| keystone, vertical (wedged from above) | anatomy | frontal auricular wedge | **holds**: converges downward 18 ± 10° (BodyParts3D 37°) |
| keystone, horizontal | popular "keystone of the body" | axial auricular wedge | **fails**: wider in front, converging backward 32 ± 15° (BodyParts3D 31°); Kapandji's suspended sacrum fits |
| four pairs of foramina, mirror-symmetric | anatomy (Gray) | detection | holds: 4 pairs, mirror to 0.1 mm (BodyParts3D); in CT found fully in 29/60 |

## Sources checked (Part C), grouped

- Etymology: Merriam-Webster sacrum; American Heritage sacrum; Etymonline (403, mirrors only); Wiktionary sacrum and ἱερός (Beekes 2010);
  LSJ transcription biblebento.com/dictionary/G2413.html (lsj.gr and Perseus refused); studylight (403); Wikipedia Sacrum and Talk:Sacrum;
  Brewer 1895 (words.fromoldbooks.org); Sugar 1995 coccyx.org/medabs/sugar.htm; Sugar 1987 JAMA doi:10.1001/jama.1987.03390150077038 (citation);
  Ojumah & Loukas 2018 (PDF 404, snippets); AAOS Now 2026 (login wall); jamanetwork 376514 (wrong article); Glossarium Graeco-Arabicum
  (unreadable PDF); IntraText Hippocrates *On Joints* (certificate error); Wellcome / UIowa catalogue records for *De ossibus* (no Kühn page);
  van Straten 1988 (not verified); useless: LLMpedia, studyguides.com, an IPFS mirror, wordsdefined.
- Yoga: Woodroffe *The Serpent Power* (archive.org djvu text); *Haṭha Yoga Pradīpikā* (Pancham Sinh, sacred-texts mirrors hyp04, hyp05;
  sacred-texts.com 403); Hinduism Today (Johari/Weltevrede 2018); nathas.org; Yoga Journal (Rosen); Yoga International; yoganerd blog;
  asivanayoga; Google Arts & Culture; Scribd copies (not used).
- Egypt: Wikipedia Djed and Ankh; Art Institute of Chicago cat. 95; Brooklyn Museum 117868; Plutarch on LacusCurtius; kemetexpert; Ancient
  Origins; UCL Petrie blog; pyramidofman; satyori; worldhistoryedu; globalegyptianmuseum. Not checked: Pyramid Texts; Wilkinson, Pinch, Griffiths.
- Luz: Sefaria API Bereshit Rabbah 28:3; Wikipedia Luz (bone); Garrison 1910 (scan too large), NYPL record; Cambridge Vesalius exhibition
  (connection refused); BIU Santé Fabrica outline; encyclopedia.com "Luz of the Spine"; mayimachronim blog. Not checked: Leviticus Rabbah 18:1.
- Mesoamerica: Stross PDF (sufipathoflove.com, unreadable); Scribd abstract.
- Geometry / keystone: Serola, The American Chiropractor 2019; Kenhub sacrum; MSU pelvis pages; musculoskeletalkey; Journal of Prolotherapy;
  sacred-geometry pages (graveworm, ancient-origins, Substack, Joanne Avison podcast) — no sacrum numbers.
- Anatomical numbers: Gray's via academickids (Bartleby 403); Bergman et al., anatomyatlases.org (segment counts: 5 in 77 %, 6 in 21.7 %);
  Turner 1886 *Challenger* report (PDF unreadable); Mysore study (search.bvsalud.org sea-198427: index m 101.3, f 116.2); IJCAP 9(4) (index
  classes); Bangladesh 172 sacra (banglajol BJA 20502: m 97.9, f 112.7); Yoon et al. 2016 Clin Orthop Surg (PMC5114254); Kolesova et al. 2017
  (PMC5768563); Cihan et al. 2023 Cureus (PMC9927799); DOAJ/JCDR 2013 (403).

## Limits

- Lengths to the tip may include the coccyx (no separate coccyx label in either source); hence low sacral indices and S5 not measured
  (S4/(S5 + tip) = 0.36 in BodyParts3D is kept in the data only).
- CT masks are automatic segmentations at 1.5 mm; small foramina close; some profiles wander (arc max 350 mm): medians are quoted where outliers exist.
- The frontal-wedge key in the data is named `..._pos_narrower_below` but its sign is the reverse (negative = narrower below; the phantom
  control and the anatomy both confirm); the axial key is right.
- After the full run one line was added to both scripts (`sys.stdout.reconfigure(line_buffering=True)`) so that PROGRESS lines reach the
  log live under `python -I`; it changes no number.

## LEADS (next bones)

1. Coccyx: separate it (CT data with a coccyx label, or a curvature/width break) and redo the sacral index and S5.
2. Hyoid and patella: small, free-floating bones with clear shapes (hyoid U-arc, patella triangle) — the same outline and constant tests.
3. Skull: the cranial vault as a sphere/ellipsoid and the orbits; well-documented sacred-geometry claims (Vitruvius, Leonardo) to test.
4. Femur neck angle and the pelvis as a whole: the pelvic inlet as an ellipse/heart, its documented sex difference.
5. Whole spine: the 33 (or 24 + sacrum + coccyx) count claims and the cervical/lumbar curves as arcs vs spirals, with this study's controls.
6. A higher-resolution sacrum set (CT at ≤ 0.8 mm, or cadaver scans) to measure all four foramen pairs in a population.

Credits: BodyParts3D, © The Database Center for Life Science, CC BY 4.0. TotalSegmentator dataset, Jakob Wasserthal et al., CC BY 4.0.
Study idea: DICTO. Measurement and analysis: Claude Code (Opus) with DICTO.
