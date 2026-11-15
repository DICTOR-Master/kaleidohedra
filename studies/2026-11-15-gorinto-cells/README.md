# Gorintō cells and their connections (study 2026-11-15)

DICTO, 15 Nov 2026: "why not gorintō cells and connection like EKP"; later the same day: the gorintō network "as a 3-dimensional mandala web", the Buddhist colours of the five rings, and a history section (HISTORY.md).

## Verdict

1. **Two gorintō cells, defined exactly.** (a) *Traditional*: cube, sphere, four-sided roof, hemisphere, jewel, with proportions from the largest measured parts of a documented group of medieval stone gorintō (Bōyama, Ehime; 308 parts). (b) *Platonic*: the five Platonic solids of one circumsphere (radius 1), stacked in gorintō order on one vertical axis, each resting on the one below. Height H = 4/3 + 4/√3 + 2√(4/3 + 8√5/15) = 6.8213523 (degree 8 over ℚ); volume 8.7074489.
2. **Connections in the EKP manner.** Every arrangement below is shrunk until the cells first touch; at that spacing every pair of pieces is separated (separating-axis test on exact data), and every contact is proved touching exactly (gap = 0 symbolically), except four ring radii where the zero holds to 120 digits only. The densest *exact* lattice found is the hexagonal field of columns, spacing √(6 − 6√5/5) = 1.8211860, density 0.4444, where every water icosahedron meets its six neighbours face to face. A numerical lattice search does better (0.5952 with parallel axes, 0.6050 with up and down columns; best found, not proved).
3. **The 3D mandala web** (main result). Thirteen Platonic gorintō: a centre, the four corners of the Tō-ji quincunx in its layer, and crosses of four half a gorintō above and below. This is the 13-node pattern of the EKP cell (a centre and its 12 nearest neighbours of a face-centred lattice), stretched along the axis. It touches first at d = 1.7776701 (exact, degree 16), with three kinds of contact: column (void face on earth face), water corner on wind face, and wind face on water corner. The same rule repeated gives a whole lattice, the layered web (density 0.4039).
4. **Relation to EKP.** The stacked Platonic gorintō does *not* embed in the EKP cell. There the five solids are concentric (the EKP nest holds all five rings about one centre), and no EKP icosahedron can rest on a face of an EKP cube: the cube's axes are two-fold axes of the EKP icosahedron, never three-fold. Taking one solid per cell up a column of EKP cells gives exact gaps 1/φ², 1/φ², 0 and an overlap of 1/φ. The gap of 0 is the octahedron's corner on the midpoint of the stella tetrahedron's top edge; the overlap is Euclid's dodecahedron crossing the wall.
5. **Status.** The arrangements are new as far as this study knows. No literature search on stacked Platonic solids was made beyond the EKP record (#8), so this is **not a priority claim**. The traditional proportions are a composite (see below), not one measured tower.

## 1. The cells

### (a) Traditional gorintō

Shapes from bottom to top (JAANUS "gorintō"; ja.wikipedia 五輪塔): earth 地 cube (方形), water 水 sphere (球形), fire 火 roof (宝形屋根型, a four-sided pyramidal roof), wind 風 hemisphere (半球形), void 空 jewel (宝珠型). The seed syllables, read from the bottom, are a, va, ra, ha, kha (ja.wikipedia 五輪塔; en.wikipedia "Gorintō").

**Proportions.** No free source found gives a canonical ratio system or a full set of per-ring measurements for one stone tower (sources checked below). The model uses the per-part maxima of the 308 gorintō parts of the Bōyama stone group (坊山石造物群, Ikata, Ehime; late Kamakura to early Edo; Bunka Isan Online 211647). These are earth 46.0 high × 53.3 wide, water 40.5 × 50.0, fire 32.0 × 53.0, and wind and void together 34.5 × 26.0 cm. The source warns that the maxima need not come from one tower, and the earth "height" label is missing in the source (order interpreted). The total, 153 cm, lies within the usual 2–3 m and smaller range (JAANUS: most 2–3 m).

| ring | model (cm) | basis |
|---|---|---|
| earth | square block 53.3 × 53.3 × 46.0 | Bōyama maxima |
| water | sphere of diameter 50 cut top and bottom to height 40.5 | Bōyama maxima; the cut is our reading of "height < width" |
| fire | square pyramid, base 53.0, height 32.0 | Bōyama maxima; eaves and curved roof not modelled |
| wind | hemisphere of radius 13, flat side up, resting on the roof's apex | width 26 = kūfū maximum width |
| void | jewel: sphere of radius 9.5 on the wind's flat top, with a tangent cone to a point at 153 cm | our choice inside the remaining 21.5 cm |

Volume 231,016 cm³. Exact arrangements of this model, computed by hand: the column has period 153 cm (jewel point on the next earth's base). The square field has spacing 53.3 cm, with earth blocks sharing whole faces (the fire base, 53.0, keeps a 0.3 cm gap); density 0.531. The ring of eight, each turned to face the centre, has radius (53.3/2)(2 + √2) = 90.99 cm, where neighbouring earth blocks meet along vertical edges.

A measured single object for comparison is the ceramic gorintō-shaped container of 1146 at the Aichi Prefectural Ceramic Museum, total height 37.5 cm (Bunka Isan Online 155368). It is a container (base, body and lid), so its ratios are not those of a stone tower.

### (b) Platonic gorintō

**Rule.** The five solids have one circumsphere of radius 1, as Euclid XIII.18 compares them. Their centres lie on the z-axis, and each rests on the one below:

| ring | solid | rests | height | contact with the one below |
|---|---|---|---|---|
| 地 earth | cube | on a face | 2/√3 = 1.1547 | (ground) |
| 水 water | icosahedron | on a face | √(4/3 + 8√5/15) = 1.5893 | face on face: the triangle on the square; one triangle corner overhangs the square by 0.0297, and no turn fits (shown below) |
| 火 fire | tetrahedron, apex up | on a face | 4/3 | face on face: the icosahedron's top face lies inside the tetrahedron's base (same orientation, centred) |
| 風 wind | octahedron | on a face | 2/√3 = 1.1547 | point: the tetrahedron's apex at the centre of the octahedron's bottom face |
| 空 void | dodecahedron | on a face | √(4/3 + 8√5/15) = 1.5893 | face on face: the pentagon on the triangle (over a corner of the triangle) |

**Orientation.** The cube's edges run along x and y. The icosahedron has a bottom corner at azimuth 0°; the tetrahedron's base is aligned with the icosahedron's top face (60°); the octahedron's bottom face is aligned with the tetrahedron's base; the dodecahedron has a bottom corner over an octahedron top corner (0°). Every piece is symmetric in the plane y = 0, so the cell has one mirror plane (Cs).

**Why the triangle overhangs the square.** A triangle with circumradius 0.6071 and centroid at the centre of a square of half-side 0.5774 fits only if each corner points within 15° of a square diagonal. The three corners are 120° apart, so modulo 90° they span 60° (in steps of 30°), but the allowed window is 30° wide. No turn of the icosahedron fits.

Checks: the four contacts inside the cell have gap exactly 0, and non-adjacent pieces are separated (control in the named run).

Colours: the Buddhist five colours (below) in the renders; DICTO's element colours only in the comparison panel of RENDER-gorinto-cells.png.

## 2. Connections (all spacings for circumradius 1)

Method (as for the EKP network, #8 §5). Two convex pieces overlap iff the translation lies inside their Minkowski difference D = A − B. The facet normals of D are face normals of A or B, or cross products of edge directions. For a family scaled by one parameter, the forbidden values are open intervals, and the first contact is the smallest allowed value. At that value, every pair is checked again on the exact data. Separated pairs have a float margin of at least 1e-7 on exactly computed coordinates. Touching pairs have their exact separating normal rebuilt from exact vertices, and the gap is shown to be 0 by its minimal polynomial ('exact'), or, where sympy timed out, to 120 digits ('digits'). Spacing closed forms come from the binding contact; their minimal polynomials are in data/minpolys.json.

### Columns and lattice fields (axes parallel unless stated)

| arrangement | spacing | minimal polynomial | density | contacts (besides the column) | certified |
|---|---|---|---|---|---|
| column (pagoda stack) | period H = 6.8213523 | degree 8 | – | void top face on next earth base, face–face | exact |
| square field, θ = 0 | 2φ/√3 = 1.8683447 | 9x⁴ − 36x² + 16 | 0.3657 | void–void face–face and edge–edge | exact |
| square field, θ = 45° | 1.7990507 | 81x⁸ − 10800x⁶ + 45360x⁴ − 38400x² + 6400 | 0.3944 | void–void face–face (4) | exact |
| **hexagonal field, θ = 0** | √(6 − 6√5/5) = 1.8211860 | 5x⁴ − 60x² + 144 | **0.4444** | water–water face–face with all six neighbours | exact |
| hexagonal field, θ = 90° | 1.8683447 | 9x⁴ − 36x² + 16 | 0.4223 | void–void face–face and edge–edge | exact |
| body-centred (columns shifted H/2), θ = 0 | 1.7776701 | degree 16 | 0.4039 | water corner on wind face (both ways) | exact |
| body-centred, θ = 45° | 1.7067689 | degree 16 | 0.4382 | fire corner on void face (both ways) | exact + digits |
| up/down checkerboard (stupa field), θ = 0 | 1.7377720 | degree 16 | 0.4227 | up water corner on down wind face, and the reverse | exact |
| up/down checkerboard, θ = 45° | 1.7623135 | 81x⁸ − 4104x⁶ + 17496x⁴ − 17184x² + 16 | 0.4110 | up earth edge on down void edge (edge–edge, 8) | exact |

θ is the angle of the lattice from the cell's mirror direction (x). The up/down field inverts every other column (half turn about a horizontal axis), as stupas might stand on alternate sides of a slope. Inverting them is not denser here (0.4227 against 0.4444).

**Numerical search** (job gorinto-search, 3 × 120 Nelder–Mead starts). Best found, not proved optimal:
- *Columns with any 2D lattice and any column shifts*, best density 0.5952: θ = 31.65°, angle 152.33°, length ratio 1.931, shifts 0.931 H and 0.481 H, spacing 1.5466. Many starts end at 0.59256.
- *Up and down columns* (any offset of the inverted sublattice), best 0.6050.
- *Fully general 3D lattice* (no vertical period forced): the parametrisation failed (best 0.33, below the named fields). This says nothing about the problem; a reduced-basis search is the next method.

The shifted columns interlock: the wide parts (water, void, earth) of one column sit beside the narrow parts (fire apex, wind) of its neighbours. A 2D cross-section shows why: a single gorintō is wide at three heights and narrow at two.

### Rings round a centre (axes vertical, all at one height; member k turned by 360° k/N about its own axis)

| ring | radius | minimal polynomial | first contact | certified |
|---|---|---|---|---|
| 4 round a centre (Tō-ji quincunx) | 1.8211860 | 5x⁴ − 60x² + 144 | centre and member: water–water face–face; members free | exact |
| 5 round a centre | 1.8211860 | same | the same; members free | exact |
| 6 round a centre | 1.9644939 | 45x⁴ − 240x² + 256 | members: water–water corner–corner | exact |
| **8 round a centre (eight-petal pattern)** | 2.5588226 | degree 16 | members: void–void face–corner | digits |
| 8, members turned inward | 2.5588226 | – | void–void edge–corner | digits |
| 8 without centre | 2.5588226 | – | the same as with centre | digits |
| 12 round a centre | 3.7899097 | – | void–void edge–edge | digits |

### The 3D mandala web (main result)

**Rule.** Thirteen Platonic gorintō with vertical axes:
- **centre** at the origin;
- **middle layer**, four at (±d, ±d, 0): the *quincunx* of the Tō-ji lecture hall, where each group of five statues has a centre with four at the north-east, south-east, south-west and north-west (Japan Tourism Agency commentary);
- **upper layer**, four at (±d, 0, +H/2) and (0, ±d, +H/2); **lower layer**, the same at −H/2.

These 12 directions are the 12 nearest neighbours of the face-centred lattice, the pattern of the EKP cell's 13 nodes (centre + 12), stretched along the axis so that each outer gorintō stands half a gorintō higher or lower than the centre.

| version | d | minimal polynomial | contacts |
|---|---|---|---|
| **outer layers parallel (rendered)** | 1.7776701 | degree 16 | upper above lower: void face on earth face (4 column contacts); water corner on wind face (6, both ways) |
| outer layers inverted | 1.7780815 | degree 8 | inverted pairs: void face on earth face; up water corner on down water face (6) |
| layers at ±H (not ±H/2) | 1.2721210 | 81x⁸ − 5400x⁶ + 11340x⁴ − 4800x² + 400 | void–void face–face (12) |
| the whole web (lattice spanned by the 12) | 1.7776701 | degree 16 | same as the 13, density 0.4039 (= body-centred θ = 0) |

So the 13-cell mandala and the infinite web it spans touch first at the same spacing: the mandala is the first shell of the web. In the mandala the thirteen cells meet as EKP's pieces do, without overlap and only through contacts of corners on faces and faces on faces (not every neighbour touches the centre). Unlike the EKP network, which uses two kinds of piece (Kepler stars and icosahedra), it uses only one.

The Womb Realm's central court (centre + 8 on the petals) is the ring of 8 above. The Diamond Realm's nine assemblies (3 × 3) are the middle layer of the square field: the plan of the mandala web shows a 3 × 3 grid of footprints.

### EKP

| question | answer |
|---|---|
| does the Platonic gorintō embed in the EKP cell? | no: in the cell the five are concentric, and no EKP icosahedron can rest on a face of an EKP cube (cube axes are its two-fold axes) |
| one element per cell up an EKP column (cube, icosahedron, stella tetrahedron, octahedron, dodecahedron at z = 0, 2, 4, 6, 8; cell edge 2) | gaps earth–water 1/φ², water–fire 1/φ², fire–wind 0 (octahedron corner on the midpoint of the tetrahedron's top edge), wind–void −1/φ (overlap: the dodecahedron crosses the wall) |
| does the mandala web relate to the EKP network? | same 13-node neighbour pattern (stretched); one kind of cell instead of two; contacts are corners on faces and faces on faces rather than corners only |

## 3. Colours

Buddhist five colours of the rings: **earth yellow, water white, fire red, wind black, void "all colours" (also painted blue)**. Source: ja.wikipedia 五輪塔: 「地輪は黄、水輪は白、火輪は赤、風輪は黒、」「そして空輪は全ての色」, with wooden towers often painted this way and the void ring sometimes blue (see HISTORY.md for the quotation). The blue for void follows that variant; 青 covers blue and blue-green, and the renders use blue (#2f5fae). Water is drawn in a warm stone white (#efe7d6). Wind is near-black (#2c2c30) with light grey edges (#b4b4b4), so its facets read on the white ground. DICTO's element colours (earth green, water blue, fire red, wind yellow, void violet) appear only in the comparison panel.

## 4. Respect

The gorintō is a memorial and sacred object, used for graves and offerings since the late Heian period (JAANUS; ja.wikipedia). This study uses its five-ring order and shapes as a geometric form only. It makes no claim about religious meaning beyond what the cited sources state, and the mandala names (Tō-ji quincunx, eight-petal court, nine assemblies) describe layouts, not doctrine.

## 5. Files

- scripts/gorinto.py: exact Platonic gorintō (sympy) and the separating-axis machinery
- scripts/arrangements.py: named arrangements with exact certification; lattice search
- scripts/minpolys.py: minimal polynomials of the spacings
- scripts/render.py: figures (uses the shared figure library of study 2026-11-13-paradigm-expansion)
- data/named.json, data/search.json, data/minpolys.json; logs/gorinto-*.log (jobs gorinto-named, gorinto-search, gorinto-minpoly, all FINAL ok)
- figures/RENDER-gorinto-cells.png (traditional, Platonic, comparison), RENDER-gorinto-network.png (hexagonal field of columns, 3 × 3 × 2), RENDER-gorinto-ring.png (eight round a centre, oblique and from above), RENDER-gorinto-mandala.png (the 13-cell mandala web, oblique view and plan)
- HISTORY.md: the five elements from India and Greece to the gorintō (sourced, about one page)

Pilot note: the first full named run failed its own control on one case (the inward ring was turned by 1 rad in floats and by π in the exact data); fixed and rerun FINAL ok. A sign error in the rebuilt exact normals, found in the pilot, was fixed before the runs.

## 6. Open / leads

- Exact form and proof of optimality of the best columnar lattice (0.5952) and of the up/down one (0.6050); reduced-basis general 3D lattice search.
- Minimal polynomials of the ring radii N = 8 (inward, no centre) and N = 12 (sympy timed out at 60 s).
- A single measured stone gorintō with all five rings measured (free site reports by prefecture) to replace the Bōyama composite.
- A mandala web with outer layers at another height h, or with the eight-petal ring as the middle layer.

## Sources checked

Gorintō form, proportions, colours:
- JAANUS, "gorintō" (projects.mcah.columbia.edu/jaanus/record/gorintō): shapes, mid-Heian adoption, Chūsonji 1169, sizes 2–3 m; no colours, no Kakuban.
- Wikipedia, "Gorintō" (en): shapes, seed syllables kha, ha, ra, va, a (top to bottom), Kūkai and Kakuban influence; no proportions.
- Wikipedia, 五輪塔 (ja): shapes, seeds, colours (quoted above), oldest dated examples, Kakuban caution; no proportion rule.
- Bunka Isan Online 211647, 坊山石造物群: per-part maxima of 308 parts (used).
- Bunka Isan Online 155368, 陶製五輪塔 (1146): full dimensions of a ceramic container (comparison only).
- City of Kitakyushu, 陶製五輪塔 一括: total 66.8 cm, earth fragment 17.5 cm only.
- Mie Prefecture, 丈六寺の五輪塔 (PDF): height 217.5 cm, 1291; no per-ring dimensions.
- Akita Prefectural Museum research report 11 (1986): ring counts, no complete per-ring table usable.
- Kanagawa Prefecture, 神奈川の中世石造物 (PDF): types, no dimensions.
- City of Kasumigaura PDF: nothing usable.
- Search results only (not opened): Jōhaiji gorintō group (Odawara; totals 1.61–1.76 m), Gifu and Okayama site reports (ratio typologies).

Mandala and Tō-ji:
- Japan Tourism Agency multilingual commentary database (mlit.go.jp/tagengo-db, 001553346.pdf): 21 statues placed by Kūkai as a three-dimensional mandala; 15 of the early 9th century, 6 restored after the 1486 fire; Five Wisdom Buddhas with Dainichi at the centre and the others at NE, SE, SW, NW; Five Great Bodhisattvas and Five Wisdom Kings on either side, with the same layout; Four Heavenly Kings; a guardian deity at each end.
- Search summary (serai.jp, intojapanwaraku.com, mlit): eye-opening ceremony of the statues in 839 (承和6年), after Kūkai's death in 835; not opened directly.
- Wikipedia, "Mandala of the Two Realms" (en): Womb Realm central eight-petal hall with Vairocana at the centre; Kue Diamond Realm in nine sections; Kūkai brought the mandalas in 806.
- Wikipedia, "Tō-ji" (en) and toji.or.jp (en): nothing on the lecture-hall mandala in the text read.

EKP: #8 The Euclid–Kepler–Pacioli Cell (papers/ekp, §§1–5); The Platonic Solids book, Chapter 1 §1.1 and Chapter 11 §11.2. Euclid, Elements XIII.18 (the five in one sphere). History sources are listed in HISTORY.md.
