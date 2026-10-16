DICTO · dictospheres.com

# Prior-art search log: progenitors study (2026-10-16)

DICTO asked for a thorough search of every claim, including the places we could not read. This log lists each claim, what was searched,
what was found, and what remains unread. "Not found" means not found in the sources listed, nothing more.

## Claims and findings

### A. The DICTO Palintriacontahedron (X; step 12)
- **What it is (exact):** the hull of the icosidodecahedron's 32 face centres pushed to twice their distance; 32 corners, 60 faces, each half a
  rhombic-dodecahedron rhombus (cos 1/3, cos 1/√3 twice); the rhombic triacontahedron's radius ratio reversed.
- **Family (found):** it is a convex hull of a dodecahedron and an icosahedron, a known one-parameter family of pentakis dodecahedra
  (Polytope Wiki: fully symmetric for icosahedron edge between (5 + 3√5)/10 and φ times the dodecahedron edge; Catalan at 3(7 + 5√5)/38).
  **X is the member with icosahedron edge = 3/√5 × dodecahedron edge**: now **exact** (edge² ratio 9/5 in ℚ(√5), `scripts/progenitors_exact.py`).
- **Named members found:** Catalan pentakis dodecahedron (68.62°, 55.69°); biscribed pentakis dodecahedron (McCooey; GeoGebra). X is neither.
- **Name clash:** "Palintriacontahedron" returns nothing.
- **Status:** a distinguished, unnamed member of a known family. Claim only that.

### B. The DICTO Hecatogdoecontahedron (the H–O compound; steps 6–8)
- **Exact (new today):** the Hecatodihedron's 20 Shield apexes are exactly the 20 three-fold vertices of the canonical pentakis dodecahedron
  (the truncated icosahedron's polar in its own midsphere, ρ² = 9/4). So **H = convex hull of TI and 20 of its canonical dual's vertices**,
  and the H–O compound has exactly the **same core and hull as the classical TI–PD compound** (core: rectified truncated icosahedron; hull:
  the joined truncated icosahedron jtI, topologically the rhombic enneacontahedron) (`scripts/heca_in_tipd.py`, float comparison of core and hull).
- **Found:** TI–PD compound (MathWorld); rectified truncated icosahedron (Wikipedia, McCooey "Rectified Archimedean Solids"); its dual jtI
  (Wikipedia "Rhombic enneacontahedron": built by pyramids on TI's faces with heights tuned so faces become coplanar); McCooey "Joined
  Truncated Icosahedron" (Archimedean–Catalan hulls).
- **Consequence for #28 (Hecatodihedron):** H is the jtI construction applied to the 20 hexagons only (the Shield height is the joined height).
  #28 checked the TI–PD compound but did not state this; a next version of #28 should cite it. H itself (102 faces) remains not found as a named solid.
- **Name clash:** "Hecatogdoecontahedron" returns nothing.
- **Status:** the compound of two DICTO solids is new as a pair; its core and hull are classical. The interest is the re-pairing, not new core/hull.

### C. The Hypsicles twins (step 11, float)
- **Found:** McCooey "Biscribed Truncated Icosahedron" and "Biscribed Pentakis Dodecahedron" match the twins' core (TI-like, all corners on
  one sphere, all faces on one sphere) and hull (pentakis with all corners on one sphere). Known; cite, claim nothing new.

### D. The golden cycle with both progenitors (steps 4, 7–9, 14)
- Searched for nested golden cycles containing the polar pair of the Hecatodihedron: nothing found beyond DICTO's own Spheres of Dharma papers.
  Related: Kepler 1596 (nested solids), Dechant et al. 2014 (nested icosahedral shells). Status: not found in the sources checked.

### E. Cleo star and D′ = (2/3)·D (step 9)
- The icosahedron's face pyramids flipped outward with apex at twice the face distance: the tips are a dodecahedron's corners (classical: they
  lie on the three-fold axes at one radius). The size relation (2/3 of the Dharma D) is DICTO-specific. Classical relative: kleetope / "first
  stellation" constructions; the 20 Cleo-Icos are Hypsicles' pyramids (Book XIV). Status: elementary, cite as construction, not as discovery.

### F. The Cleo star dissection of D′ (exact, added for the paper)
- **Exact:** D′ = 20 core Cleo-Icos + 20 Cleo spikes + 12 inward pentagonal pyramids + 30 valley tetrahedra, remainder 0 in ℚ(√5); the
  valley tetrahedra are all one shape (`data/progenitors-exact.txt`).
- **Not a stellation (checked):** the spike faces lie in no icosahedron face plane, and the tips sit at 2× the face distance; the first
  stellation (small triambic icosahedron) has its tips at 3/√5 ≈ 1.3416× (the same number as X's edge ratio; noted, not interpreted).
  The great stellated dodecahedron's spikes have side:base φ, not the Cleo-Ico's. So the Cleo star is a non-convex triakis icosahedron
  (a Kleetope of the icosahedron) at one particular height.
- **Searched:** dissections of a dodecahedron into an icosahedron with pyramids/tetrahedra; outward icosahedron pyramids whose tips form a
  dodecahedron. Found only centre-apex pyramid splits (plus.maths.org puzzle 19), Wolfram "Icosahedron-Dodecahedron Sculpture" (pyramids
  moved out to a rhombicosidodecahedron), Mosseri–Sadoc tiles (arXiv 2009.07048, dodecahedral structures from tetrahedra), Conway–Radin–
  Sadun / Hafner dissections into triacontahedron and hexecontahedron pieces. **Not found:** this 82-piece dissection.
- **Status:** the tips forming a dodecahedron is elementary (they lie on the three-fold axes); the exact four-kind filling of D′ was
  not found in the sources checked. Claim only that.

### G. Searches added 16 October (second pass, for "full prior art")
- Reference library (~/Documents/kaleidohedra-references, MANIFEST and texts): grep for Kleetope, pentakis, triakis, nested icosahedral,
  inscribed icosahedron/dodecahedron, first stellation, reciprocation: no matching source.
- George Hart, Virtual Polyhedra: index and the compounds list read; dual compounds are referred to the master index (not opened);
  no TI, PD, ID or RT compound listed there.
- Wenninger, *Dual Models*: table of contents and the Wikipedia list of Wenninger models (PD = dual of TI, W/K30) read; the book itself not.
- Wikipedia / Polytope Wiki / MathWorld: pentakis dodecahedron, triakis icosahedron, great triakis icosahedron, great stellated dodecahedron.
- arXiv (golden nested shells, polar reciprocation sequences): Fang–Irwin 1511.07786 (concentric 600-cells at powers of φ in the
  Elser–Sloane quasicrystal), Steelpillow (stellations ↔ facettings under reciprocation), icosahedral tiling papers; none is the cycle.

## Sources searched (16 October 2026)
- Web search (several queries per claim): Wikipedia (pentakis dodecahedron, rectified truncated icosahedron, rhombic enneacontahedron,
  rhombic triacontahedron, icosidodecahedron, compound of dodecahedron and icosahedron, hexapentakis truncated icosahedron), MathWorld
  (pentakis dodecahedron, TI–PD compound, dodecahedron–icosahedron compound, other compounds), Polytope Wiki (pentakis dodecahedron, read in
  full), Klitzing (pakid), OEIS A380796, McCooey Visual Polyhedra (index; Archimedean–Catalan hulls, Rectified Archimedean solids, Biscribed
  non-chiral solids, read), GeoGebra (biscribed pentakis dodecahedron), coolmath (stellated icosidodecahedron, Wenninger 47), the Geometry
  Junkyard (hecatohedra), arXiv hits (none relevant).
- Reference library (kaleidohedra-references): papers/history/bridges manifests; no pentakis, kleetope or compound-hull source.

## Not read (could not be reached here)
- Wenninger, *Polyhedron Models* (1971) and *Dual Models* (1983): printed only.
- George Hart's Virtual Polyhedra: the compounds list was read, but the master index entries for polyhedron-and-dual compounds were not opened.
- Antiprism and Stella (software catalogues): not run.
- Printed catalogues and journals (Coxeter, Cromwell, Holden, *Structural Topology* beyond Messer 1995).
These are the remaining gaps before any public "new" claim.

### H. The DICTO Metaxyhexecontahedron (named by DICTO 2026-10-16; the gap member between RT and I·φ³) (DICTO 2026-10-16: "one more should fit between RT and the icosahedron")
- **Exact (`scripts/gap_member.py` → `data/gap-member.txt`):** in the Spheres of Dharma the RT → I·φ³ step is loose (the RT reaches 0.8115 of the way). The
  dodecahedron–icosahedron hull family (pentakis-type) has exactly one member touching both: the hull of the RT's 12 five-fold corners and the
  20 face centres of I·φ³. Icosahedron edge : dodecahedron edge = **9/φ⁴** (squared 81(47 − 21√5)/2 = 81/φ⁸), ≈ 1.313082; 60 faces; the RT lies
  inside with its 12 five-fold corners on it, and it lies inside I·φ³ with its 20 three-fold corners at the face centres. Classical members for
  comparison: X (DICTO Palintriacontahedron) 3/√5 ≈ 1.3416, the Catalan pentakis dodecahedron 3(7 + 5√5)/38 ≈ 1.435; the fully symmetric range is
  (5 + 3√5)/10 to φ (Polytope Wiki).
- **Other solids tried in that gap (float, snug around RT, then reach toward I·φ³):** H 0.9948, ID and X 0.9787, deltoidal hexecontahedron 0.9443,
  truncated dodecahedron 0.9325, pentakis dodecahedron 0.9149, rhombicosidodecahedron 0.8754, truncated icosahedron 0.8682; triakis icosahedron and
  dodecahedron too big. None touches both.
- **Searched:** the 9/φ⁴ ratio or 1.3130 with pentakis / dodecahedron–icosahedron hull (web); Polytope Wiki and MathWorld pentakis pages;
  Wassell–Benito (dual pair ratio φ/3), Bridges 2017 (φ²/√5). **Not found** as a named member. Status: an unnamed member of a known family,
  distinguished by touching both RT and I·φ³ in the Dharma nest.
- **Name check:** "Metaxyhexecontahedron" (Greek *metaxý*, Plato's "in-between", + *hexēkonta*, 60 faces): web search 2026-10-16 found no use of the word (results only list the existing hexecontahedra: deltoidal, rhombic, pentagonal, noble unihexagrammic).
- **Layers as pieces (2026-10-16, `gap_chain.py`, polar_pieces.py → `data/gap-pieces.txt`, exact `gap_pieces_exact.py` → `data/gap-pieces-exact.txt`):**
  one piece per face of the inner solid. RT → G: 30 pieces of one kind (6 corners; one rhombus and 6 triangles), each 353/72 − 149√5/72;
  G → I·φ³: 60 pieces of one kind (5 corners, 6 triangles, a triangular bipyramid shape), each 1/8 + √5/18. vol G = 145/12 + 65√5/12; G takes
  0.356 of the step's volume. Like the Dharma, every layer is one kind of piece.

### I. Antiprism run (A. Rossiter, Antiprism 0.29, built on dicto-node 2026-10-16; `antiprism/`)
- **Independent recomputation** (`off_report`, float): all nine exported solids have icosahedral symmetry Ih and the stated counts; the
  Metaxyhexecontahedron: 32 corners, 90 edges (60 + 30 lengths), 60 triangles, dihedrals 138.81° (30) and 166.98° (60), volume 24.1954 (= 145/12 + 65√5/12).
- **Conway sweep** (`sweep.py`, Hart's algorithms in Antiprism `conway`): every string of up to two operators from a, b, d, e, g, j, k, m, o, p, r,
  s, t, z, k3, k5, k6, t3, t5, t6 on I and D (840 forms, 124 distinct structures), compared by structure (face sides and corner orders):
  - **Hecatodihedron and Ogdoecontahedron: no match** (their own structures, also after canonicalization).
  - H–O core = the structure of atI (rectified truncated icosahedron), hull = jtI: confirms #28 V2 and the Hecatogdoecontahedron core/hull.
  - Metaxyhexecontahedron and Palintriacontahedron: the structure of kD (pentakis dodecahedron), as stated (non-canonical members of a known family).
  - Metaxyhexecontahedron's dual: the structure of tI (truncated icosahedron), as stated (non-Archimedean proportions).
- **Status:** combinatorial novelty is checked only within this sweep (two operators); proportions are not part of a Conway structure, so the
  distinguished members (9/φ⁴, 3/√5) are not tested by it. Stella not run.

### J. Hart's master list (2026-10-16)
- G. Hart, *Virtual Polyhedra*, alphabetic list read in full: compounds of every uniform solid with its dual (incl. the truncated icosahedron and dual), dodecahedron–icosahedron compounds, the rhombic enneacontahedron, the pentakis dodecahedron, the kis/stellated forms. **None** of H, O, the Hecatogdoecontahedron, the Metaxyhexecontahedron, the Palintriacontahedron, or a nested golden cycle. Remaining unread: Wenninger in print, Coxeter/Cromwell/Holden in print, Stella.
