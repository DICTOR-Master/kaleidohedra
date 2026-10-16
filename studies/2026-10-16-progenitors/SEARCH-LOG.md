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
  **X is the member with icosahedron edge = 3/√5 × dodecahedron edge** (float, 15 digits).
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
- George Hart's Virtual Polyhedra compound pages: search reached the index only; individual compound pages not opened.
- Antiprism and Stella (software catalogues): not run.
- Printed catalogues and journals (Coxeter, Cromwell, Holden, *Structural Topology* beyond Messer 1995).
These are the remaining gaps before any public "new" claim.
