DICTO · dictospheres.com

# Progenitors: the Ogdoecontahedron and its dual as the seed of a new cycle (DICTO 2026-10-16)

DICTO: "let's imagine it and its dual as the progenitors of a new cycle"; then "maybe the truncated icosahedron has a place".

## Step 1, the pair (exact): `scripts/pair_chain.py` → `data/pair-chain.txt`
The Hecatodihedron H and the Ogdoecontahedron O (its polar in the unit sphere) as endless shells of each other: H ⊂ s·O with s = 81/8 − 27√5/8 (H's own corner radius²; 20 corners touch), O ⊂ t·H with t = (170 + 2√5)/361 (O's corner radius²; 12 touch). Round trip s·t = (3375 − 1107√5)/722 ≈ 1.246, not a power of φ.

## Step 2, the quartet TI, H, O, PD (exact): `scripts/quartet.py` → `data/quartet.txt`
TI ⊂ H and O ⊂ PD (given), TI ↔ PD and H ↔ O dual. All six cyclic orders at least scale; none closes on a power of φ.

**Option 1 (kept as an alternative, DICTO 2026-10-16): the 3-cycle.** TI ⊂ H ⊂ O ⊂ PD ⊂ TI, each at its tightest fit, gains exactly (63 − 27√5)/2 = 9/φ⁴ = (3/φ²)² per round: TI ⊂ H and O ⊂ PD touch fully (scale 1), H ⊂ (27/4)φ⁻²·O, PD ⊂ (4/3)φ⁻²·TI. An exact endless cycle governed by 3, not φ — the same 3 that keeps the two toggle settings of *Double Vision* apart.

## Step 3, option 2: a golden closure with classical stations inserted: `scripts/golden_search.py` → `data/golden-search.txt`
All 8,742 cycles through TI, H, O and PD plus any of I, ID, D, RT (each at most once, any order), every solid at the least size holding the previous one: **no golden closure** (no gain per round is exactly a power of φ). The factor 3 runs through the tight fits: D ⊂ 3·I, TI ⊂ 3·I, I ⊂ RT/3, O ⊂ (4/3)·I (90 corners touch), D ⊂ (9/4)·O, O ⊂ (4/9)·RT.
Caveat: the criterion "every step tight" is stricter than the Spheres of Dharma itself, whose I → ID and RT → I·φ³ steps are loose. A golden cycle through the quartet would need some loose steps; that is the next question.

## Step 4 (exact): a golden cycle with both progenitors: `scripts/o_dharma.py` → `data/o-dharma.txt`
DICTO asked whether his pieces (Cleo, FUJI, …) could generate suitable progenitors. The icosidodecahedron is a common core of both: O wraps it
(its 30 corners on O's faces, each ID triangle in an O hexagon), and Theaetetus grows it through Cleo-Icos to H. Placing O on the Dharma's own ID
(scale 3φ²/4, the middle toggle of *Double Vision*) gives **I ⊂ ID ⊂ O ⊂ TI ⊂ H ⊂ RT ⊂ I·φ³**: every step nests exactly, the closure is φ⁹ in volume
(golden, as the Spheres of Dharma). Tight steps: ID ⊂ O (30/30), TI ⊂ H (60/60), H ⊂ RT (80/80); loose: I ⊂ ID, O ⊂ TI, RT ⊂ I·φ³. O and D cross,
so O takes D's place (alternatives, as H and 3·I are). Layer volumes in the file.

Open (DICTO 2026-10-16): "double inverted like a stella octangula" — H and O interpenetrating; neither has a midsphere, so no canonical compound;
natural sizes: O's 90 sphere corners kissing H's 90 tangent faces, or deeper. "Truncated form of Cleo-Icosa" — to clarify (cut at the 12 corners
or at the 20 Cleo-Ico tips of the DICTO-ICOSA star).

## Step 6 (exact): the O–H compound, "double inverted like a stella octangula": `scripts/oh_compound.py` → `data/oh-compound.txt`, `oh-compound.json`
H's 90 rhombi and triangles touch the sphere ρ² = 9/4 (its 12 pentagons lie closer, at 17/8 − √5/40). Taking O as H's polar in that sphere:
O's 90 sphere corners kiss H's faces, O's 12 five-fold corners poke out through H's pentagons, all 80 corners of H poke out of O.
- **Exact:** O's 90 kissing corners are exactly the 90 edge midpoints of the Dharma's own truncated icosahedron; ρ = 3/2 is the TI's midsphere.
- **Common core H ∩ O** (float counts): 90 corners, 92 faces = 12 regular pentagons + 20 regular hexagons + 60 triangles, two edge lengths: the
  rectified truncated icosahedron of the Dharma TI.
- **Hull** (float counts): 92 corners (80 of H, 12 tips of O), 90 quadrilaterals (30 rhombi, 60 others), every face touching the same sphere with
  its normal through a core corner: the polar of the core. Core and hull are a dual pair, as the octahedron and cube are for the stella octangula.
- Known solids: the rectified truncated icosahedron and its dual (Conway aT I and its dual). The H–O compound as their source is to be checked
  in the reference library before any claim.

## Step 7 (exact): core and hull as stations: `scripts/core_hull_in_cycle.py` → `data/core-hull.txt`
**The 182 count (DICTO):** the O–H compound has 102 + 80 = 182 faces and 80 + 102 = 182 corners and is self-dual (its polar in the same sphere
swaps H and O), as the icosahedron–dodecahedron compound has 32 and 32. There every face reaches the core (ID, 32 faces) and every corner the hull
(RT, 32 corners); here 90 pairs only kiss (O's 90 sphere corners on H's 90 tangent faces), so core and hull have 182 − 90 = 92 each.
**Stations:** the golden cycle takes both, exactly: **I ⊂ ID ⊂ O ⊂ rTI ⊂ TI ⊂ H ⊂ hull ⊂ RT ⊂ I·φ³** (O at 3φ²/4). rTI's 90 corners lie on TI's edges;
the hull's corners include H's 80, which lie on RT's faces; TI touches the hull at 60 corners. The cycle now holds the core and hull of both pairs:
ID and RT (icosahedron–dodecahedron), rTI and its dual (Hecatodihedron–Ogdoecontahedron). In this cycle O sits at 3φ²/4, not at its compound size 9/4.

## Step 9 (exact): the Cleo star brings the dodecahedron back: `scripts/cleo_star_station.py` → `data/cleo-star.txt`
DICTO: "the icosahedron with the Cleo-Icosa core and Cleo-Icosa spikes … feels like the dodecahedron should be in there too". The Dharma
icosahedron is 20 Cleo-Icos; with 20 more as spikes it is the Icosa star (volume 2·I). **Its 20 tips are exactly the corners of (2/3)·D**, the
Dharma dodecahedron at two thirds, and that dodecahedron D′ fits (loosely) inside ID and inside O: I ⊂ star ⊂ D′ ⊂ ID ⊂ O ⊂ … — the dodecahedron
returns as the hull of the Cleo star, in the old loose I → ID gap. D′ − star = 35/18 − 17√5/54 is **one connected gap** (cups over the 12 corners
joined by valleys along the 30 edges; float flood fill); cut by the cones over D′'s faces it gives 12 equal pieces.

## Step 10 (exact volumes; float overlap test): 12 inward pyramids: `scripts/inward_pyramids.py` → `data/inward-pyramids.txt`
DICTO: "the 12 five-sided pyramids of Hypsicles pointing inwards". On each pentagonal face of D′ a pentagonal pyramid pointing inward, apex at
the icosahedron corner below: all 12 fit in the star–D′ gap with no overlap of I or the spikes (48,000 sampled interior points, float). Each has
volume 5/108 − √5/324 and height² 29/72 − 61√5/360 (about 0.21 of D′'s own central Hypsicles pyramid's height). Together 5/9 − √5/27 = 38.1% of
the gap; left are the valleys along the 30 edges of I, (25 − 5√5)/18 = 61.9%.

## Step 11: the Hypsicles twins (DICTO: "a special filling variety like Cleo-Icosa"): `scripts/hypsicles_twins.py` (exact part fails, see below)
The Dharma icosahedron (20 Cleo-Icos) and the dodecahedron D″ in the same circumsphere (12 "Cleo-Dodecas", its central pyramids). Hypsicles
(Book XIV): equal inradii, so both pyramids have the same height (float: 0.467086 both).
- **Not golden-exact.** The squared edge ratio is (5 − √5)/6, whose square root is not in ℚ(√5): D″ needs a further square root. So the twins
  cannot be an exact pair of stations in a ℚ(√5) cycle. Everything below is float.
- **Interlocked:** core I ∩ D″ = 60 corners on one sphere, 12 pentagons + 20 hexagons, two edge lengths (a truncated icosahedron with irregular
  hexagons, every face on the common insphere); hull = 32 corners on the common sphere, 60 triangles (a pentakis dodecahedron inscribed in a sphere).
  Core and hull are duals: the third member of the family midsphere compound (ID / RT) · H–O compound (rTI / dual) · Hypsicles twins (TI-like / pentakis-like).
- **Place:** the twins with their hull sit in the loose I → ID gap, the same place as the Cleo star and its hull (2/3)·D, which is golden-exact.

## Step 12 (exact): the full-height icosidodecahedron star and its hull X: `scripts/id_star.py` → `data/id-star.txt`
DICTO: shortening the spikes to fit "feels like cheating; one more solid is needed". The Dharma ID with its central pyramids flipped out at full
height: 20 triangle tips at radius² 3 + 4√5/3, 12 pentagon tips at 5/2 + 11√5/10 (the same points as the Dodeca star's tips: the ID's pentagons
lie in D's face planes). Their hull **X**: 32 corners, 60 triangles, every face with cos² 1/9 (once) and 1/3 (twice), i.e. angles 70.53°, 54.74°,
54.74°: half a rhombic-dodecahedron rhombus. All nine stations lie strictly inside X; X and I·φ³ interlock (X's 20 three-fold corners outside
I·φ³, all 12 of I·φ³'s corners outside X): X bridges one turn to the next. Renders: `renders/id-star.png`.

## Step 13: is X known? (prior-art checks, 2026-10-16)
- **Origin:** X's corners are the ID's 32 face centres pushed to twice their distance; the RT (the ID's dual) puts corners on the same 32 axes at
  distances inversely proportional. The two five-fold : three-fold radius ratios are exact reciprocals (X 0.9106, RT 1.0982): X is the rhombic
  triacontahedron turned inside out. Shape family: pentakis dodecahedron (a dodecahedron with 12 low pentagonal pyramids, lateral edge : base edge =
  √3/2, apex angle arccos(1/3)); not the Catalan one (68.62°, 55.69°, 55.69°; Klitzing "pakid", MathWorld, OEIS A380796).
- **Not the ID's first stellation** (Wenninger 47, the icosahedron–dodecahedron compound): that has the same 32 axes but the RT's ratio, and the RT as hull.
- **Compounds tested (float), no link:** five cubes on X's dodecahedron (30 face planes: none through X's tips, none an X face, X's tip not a triple
  meeting point); ten tetrahedra (20 planes: none through the tips or parallel to an X face); X's face normals lie on no 2- or 3-fold axis.
- **Searched:** Wikipedia and Polytope Wiki pentakis pages, MathWorld, Klitzing, OEIS, a general web search; the reference library holds no pentakis or
  kleetope source. Wenninger's printed catalogues and Hart's compound pages not read. **Status: not found in the sources checked**; name DICTO's.

## Names (DICTO, 2026-10-16; full names carry "DICTO" in front, as the DICTO Hecatodihedron and DICTO Ogdoecontahedron)
- **DICTO Palintriacontahedron** (πάλιν, back/reversed): X of step 12, the hull of the full-height icosidodecahedron star; the rhombic triacontahedron
  turned inside out (same 32 axes, reciprocal radius ratio); 32 corners, 60 faces, each half a rhombic-dodecahedron rhombus.
- **DICTO Hecatogdoecontahedron** (102 + 80, after icosi-dodeca): the compound of the Hecatodihedron and the Ogdoecontahedron of step 6, in the truncated
  icosahedron's midsphere; 182 faces, 182 corners, self-dual; core the rectified truncated icosahedron, hull its dual.

## Step 14 (float): the seam, and the full-cycle render
The Palintriacontahedron lies inside the next turn's D′ (D′·φ³) and fills the next icosahedron's Cleo star almost exactly: all 32 corners inside,
99.46% of its volume (20,000 sample points), so 0.54% pokes out, presumably through the valleys between spikes. The loose I·φ³ → ID·φ³ step is
filled as at the centre (Cleo star, D′). Render of the whole: `renders/full-cycle.png` (`render_full.html`, `shoot_full.mjs`, `data/full-cycle.json`).
