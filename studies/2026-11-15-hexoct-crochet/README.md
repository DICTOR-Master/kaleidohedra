# HexOct in crochet: crocheted cells that fill space (study, 15 November 2026)

**Verdict.** HexOct can be built in crochet as a real three-dimensional crystal: closed, solid crocheted cells that fit whole face to whole face and stack into c and h layers. This is not a flat fabric and not a pattern on a surface. The cells are DICTO's Narcissus (every h layer) and the cube (every c layer), the HexOct pieces at the end of the walk (λ = 3/8, paper #98). Every stacking is filled by them, two cells per ball in every layer. We checked this exactly on periodic blocks of five stackings (3C, 2H, 4H, 6H, 9R): no gaps, no overlaps, and every face meets one whole face of one other cell. Only three flat face shapes are needed, all crocheted in rows of single crochet:
- a square of side L;
- a regular hexagon of side L·√(2/3);
- a right triangle with legs L/√3 and L·√(2/3).

Every join between two layers is the same square. The pattern below gives one Narcissus at L = 9.5 cm. Its sides, computed back from the stitch counts at the stated gauge, are within 0.6 % of the true lengths, and its corner angles within 0.1°. Crochet suits this build better than knitting, for reasons the sources state: one live loop at a time, stitches attach almost anywhere, closed 3D shells are standard practice, and the fabric is denser and less stretchy. None of the sources checked shows crocheted cells that fill space. The strength of the claim is therefore "well-founded and untested": the first test piece (two Narcissus and two cubes, below) decides it.

Status: plan and pattern ready for DICTO's reading; nothing crocheted yet. One-page plan: `plan/DRAFT-hexoct-crochet-plan.pdf` (copy in DICTO's reading folder).

## 1. What is built (three-dimensional)

| Layer type | Cell | Faces | Cells per ball | How the two cells of one ball join |
|---|---|---|---|---|
| h | Narcissus (DICTO's name, #98) | 1 regular hexagon, 3 squares, 6 right triangles; 10 corners | 2 | on their hexagons; the two together are one convex solid with 12 faces and 11 corners: the twisted cube of #86 (checked) |
| c | cube | 6 squares | 2 | on a square: a brick |

The edge lengths are in ball spacings a, with L = a/√2. The cube and Narcissus each have volume √2/4 a³, which is half a ball's cell.

Face census (scripts/tiling.py, `data/tiling.json`, FINAL OK). Each stacking was checked on a periodic box of 3 × 3 balls × one period:

| Stacking | c/h | Cells | Volume adds up | Random points covered exactly once | Faces: each met by exactly one other whole face | Contacts between layers |
|---|---|---|---|---|---|---|
| 3C ABC | ccc | 54 | yes | 20 000 / 20 000 | 162 / 162 | squares (cube–cube) |
| 2H AB | hh | 36 | yes | 20 000 / 20 000 | 180 / 180 | squares (Narcissus–Narcissus) |
| 4H ABCB | hchc | 72 | yes | 20 000 / 20 000 | 288 / 288 | squares (Narcissus–cube) |
| 6H ABCACB | hcchcc | 108 | yes | 20 000 / 20 000 | 396 / 396 | squares |
| 9R ABACACBCB | hhchhchhc | 162 | yes | 20 000 / 20 000 | 702 / 702 | squares |

Within an h layer, Narcissus meet Narcissus on hexagons and on triangles. Within a c layer, cubes meet on squares. **Across every layer boundary the contact is a square of side L, in every stacking.** For the builder this means:
- one stacking differs from another only in which layers are made of Narcissus pairs and which of cube pairs, and where they sit;
- every layer meets the next on the same square seam.

## 2. Precedents (credits at the point of use)

- **Taimiņa**: the first crocheted hyperbolic plane, 1997 (Wikipedia, Daina Taimiņa). D. Taimiņa, *Crocheting Adventures with Hyperbolic Planes*, A K Peters 2009. D. Taimiņa, "What I learned in 25 years crocheting hyperbolic planes", Bridges 2022 (archive.bridgesmathart.org/2022/bridges2022-6.pdf, opened). This paper also notes knitted models from 1885.
- **Osinga & Krauskopf**, "Crocheting the Lorenz manifold", Math. Intelligencer 26(4) (2004) 25–37. The author page (math.auckland.ac.nz/~hinke/crochet) gives 25,511 stitches, crocheted from computer-generated instructions. Plus magazine (R. Thomas, "Chaotic crochet", 2004) describes the method: bands added with points added or removed, that is, increases and decreases. The finished surface is held by steel wires. Their follow-up "How to crochet a space-filling pancake" (Bridges 2014) is about a surface spreading through space, not a tiling by solids.
- **Crocheted polyhedra**: J. Gilbank (PlanetJune), "Polyhedral Balls" pattern, 2012. All five Platonic solids are made from crocheted faces joined by crochet and stuffed, with sides "relatively flat" and no inserts. L. Magrics, "3D Webs", Bridges 2025, crochet on Platonic-solid scaffolds. S. Dong, "Topological Crochet", Bridges 2025, surfaces from foundation-chain ribbon graphs.
- **Amigurumi**: Edelstein, Peleg, Itzhaky, Ben-Chen, "AmiGo: computational design of amigurumi crochet patterns", SCF 2022 (arXiv 2211.01178). Rows of sc, inc and dec give a flexible shell that takes its final shape from stuffing. K. Seitz, J. Lincke, P. Rein, R. Hirschfeld, *Language and Tool Support for 3D Crochet Patterns*, HPI Technical Report 137 (2021), doi:10.25932/publishup-49253. It covers spiral rounds, and states that increases and decreases are "mainly responsible for reaching any shape".
- **Crochet Coral Reef**: Institute For Figuring, Margaret and Christine Wertheim, from 2005, built on Taimiņa's method (crochetcoralreef.org history page).
- **belcastro & Yackel (eds.)**:
  - *Making Mathematics with Needlework* (A K Peters 2007): the crochet chapter is Ch. 3, "The Sierpinski Variations: Self-Similar Crochet" (contents listing).
  - *Crafting by Concepts* (2011): its blurb includes crochet, but no chapter title names it (contents listing; which chapter is crochet not verified).
- **Bead crochet**: S. Baker and S. Goldstine, "Bead crochet bracelets: what would Escher do?", Bridges 2012 (plane tilings on a torus of beads).
- **Crocheted space-filling cells, 3D lattices or foams: none found** (searches listed below).

## 3. Knitting and crochet compared

| Property | Knitting | Crochet | Source |
|---|---|---|---|
| Live loops while working | the whole row is held open on the needles | one loop on the hook; each stitch is finished and anchored | Madill, *Knitty* Winter 2025 ("one live stitch at a time"); HPI TR 137 ("always one loop around the hook"); Karp, loopholes.blog 2019 |
| Where a new stitch can attach | in the grid of courses and wales | "nearly any place on the crochet fabric", flat or three-dimensional | Markande & Matsumoto, Bridges 2020; HPI TR 137 |
| Closed 3D shells | by rounds and by splitting and rejoining tubes | spiral rounds with increases and decreases; seamless ribbon-graph builds; stuffed shells; joined polyhedral faces | Dong, Bridges 2025; HPI TR 137; AmiGo 2022; Gilbank 2012 |
| Stretch | can stretch over 100 %; elasticity set by the stitch topology | stitches "locked in place", less stretch | Markande & Matsumoto 2020; Singal et al., Nat. Commun. 15 (2024) 2622; Madill 2025 |
| Thickness, yarn | thinner, less yarn | thicker, "almost always" more yarn | Madill 2025 |
| Tensile behaviour | reference (knitted) | higher loads at larger strain; stiffer as a composite reinforcement; varies with the crocheter | Storck, Steenbock, Dotter, Funke, Ehrmann, J. Eng. Fibers Fabr. 18 (2023), doi:10.1177/15589250231203381 (abstract only) |
| Machines | industrial knitting machines | no industrial crochet machine; a one-sided prototype (2023) | HPI TR 137; Storck, Feldmann, Kyosev, CDATP 4(2) (2023) 254–272 |

**Conclusion for HexOct's 3D cells, at its true strength.** The sources support three statements:
- crochet builds closed polyhedral shells from flat faces joined at any edge;
- it holds a shape better than knitting, being denser and less stretchy;
- it can grow in any direction from a single live loop.

Those are the properties a space-filling cell needs. No source shows crocheted cells that fit together to fill space. Whether crocheted Narcissus and cubes hold their angles well enough to stack face to face is an open practical question. The design answers it with firm cores (§5) and a test piece (§6). Knitting is not ruled out for 3D: knitted surfaces exist, and belcastro, "Every topological surface can be knit: a proof", J. Math. Arts 3 (2009) 67–83, is the reference (metadata only seen). But knitting is worked as a sheet, and the sources place the advantage for solid cells with crochet.

## 4. The pattern for one Narcissus (US terms; UK in brackets)

**Gauge assumption.** Single crochet (UK double crochet) in DK cotton, 4.0 mm hook: 18 sts and 20 rows to 10 cm. Swatch 25 sts × 25 rows. If your gauge differs, rerun `scripts/pattern.py <sts per cm> <rows per cm>`: it picks the face size and recomputes every count and check.

**Scale.** Square side L = 9.5 cm, so the ball spacing is a = 13.4 cm. This size was picked from 6 to 10 cm as the one whose whole-stitch counts fit best.

Abbreviations:
- ch: chain;
- sc: single crochet (UK dc);
- sc2tog / sc3tog: single crochet 2 or 3 together (UK dc2tog / dc3tog);
- 2 sc in st: increase.

Every row starts with ch 1, turn (not counted as a stitch).

| Face | How many | Pattern |
|---|---|---|
| Square | 3 (cube: 6) | Ch 18. Row 1: sc in 2nd ch from hook and in each ch (17 sc). Rows 2–19: sc in each st. Fasten off, leaving a 40 cm tail. |
| Hexagon | 1 | Ch 15. Row 1: sc in 2nd ch from hook and across (14 sc). Rows 2, 4, 6, 8, 10, 12, 14: 2 sc in first st, sc to last st, 2 sc in last st (+2 each; row 14 = 28 sc). Rows 3–13 odd: sc across. Rows 15, 17, 19, 21, 23, 25, 27: sc2tog, sc to last 2 sts, sc2tog (−2 each; row 27 = 14 sc). Rows 16–26 even: sc across. 27 rows. |
| Right triangle | 6 | Ch 15. Row 1: sc in 2nd ch from hook and across (14 sc). Mark the first stitch of row 1: that edge stays straight (the right angle). Rows 2–11: sc across, making every decrease at the unmarked (slanted) edge: sc2tog in rows 2, 3, 4, 6, 7, 9, 10 and sc3tog in rows 5, 8, 11. Stitch counts: 14, 13, 12, 11, 9, 8, 7, 5, 4, 3, 1. Fasten off. Three of the six are turned over before sewing: single crochet looks alike on both sides, so one pattern gives both hands. |

**Geometry check** (`data/pattern.json`). Each length is computed back from the counts at the gauge.

| Side | True (cm) | From the stitches (cm) | Error |
|---|---|---|---|
| square, width / height | 9.50 | 9.44 / 9.50 | −0.58 % / 0.00 % |
| hexagon, top and bottom / slanted sides | 7.76 | 7.78 / 7.79 | +0.27 % / +0.43 % |
| triangle, long leg | 7.76 | 7.78 | +0.27 % |
| triangle, short leg | 5.48 | 5.50 | +0.28 % |
| triangle, hypotenuse | 9.50 | 9.53 | +0.27 % |

Two angles were checked as well:
- hexagon corner: 119.95°, true 120°;
- triangle acute angle at the long leg: 35.27°, true 35.26°.

The true ratios hold: the hexagon side and the triangle's long leg are equal, and the triangle's hypotenuse equals the square side. The edges are stepped by single stitches; seams hide the steps.

**Assembly** (edge census of the net: 18 edges, all checked):
1. Sew the six triangles round the hexagon by their long legs (6 seams), alternating the turned-over ones. The net in the plan shows the order.
2. Sew neighbouring triangles together along their short legs (3 seams); the piece now cups.
3. Sew the three squares into an open cube corner (3 seams). This corner sits on a ball.
4. Insert the core (§5) and close by sewing the square rims to the six triangle hypotenuses (6 seams).

Seams are whip stitch through the back loops, with the tails, on the inside, so that faces stay flat for contact. The cube is six squares sewn the same way (12 seams).

Yarn: Narcissus has 555 cm² of face (cube 542 cm²). Weigh your 10 × 10 cm swatch: one cell takes about 5.6 times that weight, plus the seams.

## 5. Rigidity: the cell must keep its angles

A stuffed shell bulges, as AmiGo describes: the shell takes its shape from the stuffing. Bulging faces cannot meet face to face. So each cell is crocheted over a firm core: a folded card or PET-sheet (bottle plastic) polyhedron made from the same net (`fig/net-narcissus.png`), cut slightly undersize to allow for the fabric's thickness.

The dihedral angles of Narcissus are 90°, 120° and 135° only (#98); those of the cube are 90°. A core can be scored and folded to them exactly. How much undersize the core must be depends on the yarn: the test piece will measure it. Light stuffing between core and skin is optional.

## 6. From cells to layers to a stacking

- **h-layer unit.** Two Narcissus joined on their hexagons make the twisted cube: 12 faces, 11 corners. The two cells may be sewn together permanently, or the twisted cube crocheted as one cell. Its 6 isosceles triangles each merge two right triangles; they are coplanar (checked: the union is convex with 12 faces).
- **c-layer unit.** Two cubes joined on a square: a brick.
- **Layers.** Units of one layer sit side by side; triangles meet triangles and squares meet squares. Each layer then rests on the one below on squares only.
- **Any stacking.** Write the stacking in c and h, then build each h layer of Narcissus pairs and each c layer of cube pairs. Figure `fig/block-4H.png` shows 4H (h c h c) in 3D with the layers drawn apart.
- **Test piece 1.** Two Narcissus and two cubes: one h-layer unit on one c-layer unit. It checks the face fit, the core allowance and the square seam between layers.
- **Test piece 2.** A 4H block of 2 × 2 balls × 4 layers: 16 Narcissus and 16 cubes.

## 7. The knitting paper (#83, "HexOct: Knitting Crystals", published Version 5): what stands

Read in Version 5 (front section, Part 1 construction, Part 2 mechanics, Part 3 comfort). The published paper is not edited.

**Unaffected (mathematics, true whatever the craft):**
- Part 1 §1, exact geometry:
  - links of length a at 54.7356°, sheets √(2/3)·a apart;
  - the self-centring lemma: taut links of length a allow at most √(2/3)·a spacing, reached only with the sheet in place;
  - c sheets carry links straight on, and h sheets fold them back;
  - the cells closed off are the octet tetrahedra and octahedra, which are the HexOct pieces at λ = −1/8.
- Part 2: the lattice mechanics of the idealised strut-and-sheet model (equal density, compression and buckling the same in every stacking; see-through area and free shear set by the stacking). These are results about rods and nodes, however made.
- Part 3: the comfort proxies on the same idealised model.

**Depends on knitting being workable:**
- Part 1 §2, the hand build: garter sheets with marked nodes, i-cord links, needle and gauge counts, two test pieces of about 210 m each;
- the machine build (double-needle-bar spacer, one gap at a time);
- the abstract's sentence "any close-packed stacking can be knitted into the fabric's own thickness";
- the title's word "Knitting";
- Parts 2–3 insofar as they speak of a knitted textile (yarn, breathability of a garment): the numbers stand for the idealised lattice, but their use as textile properties assumed the knitted build.

**Note on what is built.** #83 Version 5 builds an open lattice of sheets and links whose empty cells are the λ = −1/8 pieces. The crochet build here makes the cells themselves, as solids (λ = 3/8: Narcissus and cubes). Parts 2–3 model struts, so they do not describe the solid-cell build.

**Proposed wording for the next version** (recorded in the Concordance `next_versions` under `hexoct-knitting`; not applied):
> *Abstract, first sentence:* "This is a crystal built in crochet: closed crocheted cells, Narcissus in every h layer and cubes in every c layer (the HexOct pieces at λ = 3/8, #98), two cells per ball, fitted whole face to whole face, so that the build is the stacking in three dimensions."
> *Construction section:* the pattern of this study:
> - three face shapes in rows of single crochet;
> - the geometry check from the gauge;
> - assembly over a folded core;
> - the h-layer unit (twisted cube) and the c-layer unit (brick);
> - every layer joined to the next on squares.
>
> The strut-and-sheet geometry and its mechanics (Parts 1 §1, 2, 3) stay as the mathematics of the octet lattice of the same stacking, stated without reference to a craft. Version line: "Version 6 gives the construction in crochet."
> *Title:* DICTO's choice (the present title names knitting).

Errata go only in the Concordance and version lines, per the house rule.

## 8. Other HexOct textile items

The HexOct scarf (papers/hexoct-scarf, a two-colour knitting pattern) is a flat stripe pattern by design: one band per layer, coloured c or h. It makes no 3D claim and stands as it is.

## Sources checked (all free; nothing bought)

**Library.** DICTO's reference library (cited/MANIFEST.json, READING-LIST, bridges/ folder, full-text grep for crochet, amigurumi, Taimiņa, knitting). The only hits are the knitting history sources already cited in #83; there is no crochet source. New references were added to docs/SOURCES.md.

**Opened, web:**
- Wikipedia, Daina Taimiņa;
- Bridges 2022 Taimiņa PDF;
- Osinga's crochet page (Auckland);
- Plus magazine "Chaotic crochet";
- Bridges 2014 Osinga–Krauskopf;
- PlanetJune Polyhedral Balls;
- Bridges 2025 Magrics PDF;
- Bridges 2025 Dong PDF;
- AmiGo (ar5iv 2211.01178);
- HPI TR 137 (PDF);
- IFF Crochet Coral Reef history;
- Perlego contents of *Making Mathematics with Needlework*;
- Routledge page of *Crafting by Concepts*;
- Bridges 2012 Baker–Goldstine;
- loopholes.blog "Crochet as warp knitting";
- Knitty Winter 2025 "How to Get Hooked";
- CDATP 2023 Storck–Feldmann–Kyosev;
- Crossref record of Storck et al. 2023 (abstract);
- Bridges 2020 Markande–Matsumoto (and ar5iv 2002.01497);
- PMC Singal et al. 2024;
- Crossref record of belcastro 2009.

**Failed or blocked:** doaj.org (403), journals.sagepub.com (403), hsbi.de (login), nature.com (redirect), textiles.cs.cmu.edu (certificate error), Europe PMC (no record), Ravelry list of *Crafting by Concepts*.

**Web queries:**
- Osinga Krauskopf Lorenz crochet stitches;
- Taimiņa Bridges 2022;
- AmiGo amigurumi;
- crochet cannot be done by machine;
- *Making Mathematics with Needlework* contents;
- *Crafting by Concepts* contents;
- IFF coral reef 2005;
- belcastro "Every topological surface can be knit";
- Markande Matsumoto knotty knits;
- Singal 2024;
- crocheted vs knitted fabric tensile;
- Bridges crocheted polyhedra / Platonic;
- Baker Goldstine bead crochet 2017 (only a 2017 Baker–Wampler scarf paper turned up; not used);
- crochet space-filling polyhedra / truncated octahedron / rhombic dodecahedron (nothing);
- Seitz crochet;
- Guo et al. crochet stitch meshes (listing only, not used);
- Storck crocheted fabrics;
- crochet uses more yarn;
- crochet 3D lattice / foam / Kelvin cells (nothing).

**Own papers:**
- #98 (Narcissus and Covenant);
- #83 Versions 2 and 5;
- #75 tiles (tiles.py of the keyed-hexoct study);
- Concordance Names (HexOct, HexOct c-tile, h-tile, Narcissus, Echo, twisted cube, Covenant).

## Checks (all FINAL OK; run on the compute host)

| Script | What it checks |
|---|---|
| `scripts/faces.py` → `data/faces.json` | the faces of Narcissus and the cube, with side lengths as square roots of exact rationals (1/2, 1/3, 1/6); volumes √2/4 |
| `scripts/tiling.py` → `data/tiling.json` | five stackings: volume, single coverage, face-to-face, contact census |
| `scripts/pattern.py` → `data/pattern.json` | the stitch counts and the back-computed geometry |
| `scripts/figs.py` → `fig/`, `data/fig-checks.json` | net unfolded with true side lengths and no overlap (largest overlap 5e−17); hexagon rows 14→28→14, symmetric; h-tile union convex, 12 faces, 11 corners (twisted cube) |

## Leads
1. Crochet test piece 1 (two Narcissus, two cubes) by DICTO or a crocheter in the family. Measure the face fit and the core allowance, and add photos to the next version of #83.
2. The twisted cube as one crocheted cell (6 squares, 6 isosceles triangles): a pattern with fewer seams for h layers.
3. A crocheted Covenant: two Narcissus turned 60°, 12 parallelogram faces. It fills space alone by translation, so a one-cell-type build is possible.
4. Joining the cells of a layer by crochet itself (join-as-you-go), so that a whole layer is one piece of crochet with cores inside.
