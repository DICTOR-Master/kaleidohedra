# The Sunstar as rock salt's keyed switch point (2026-10-25)
DICTO: "a different but cohesive structure of bond network, similar but different to the golden and Delian".
#42's Sunstar lattice: dodecahedra on the even cubes of a cube grid (edge 2), Dogstars on the odd cubes = rock salt sites; rock salt's
single switch point (#53) has every cell a cube. Here: dodecahedron = cube + 6 Euclid roofs (Elements XIII.17), Dogstar = cube − the
6 roofs pushed in by its neighbours, so the network is that switch point keyed with the roofs (keying rule: the web stays the cube web).
- proof.py → proof.txt: exact volumes (dodecahedron 10 + 2√5, roof 2φ/3, Dogstar 6 − 2√5 = 4/φ², sum 16); app dodecahedron = cube + roofs
  (Δ 1e-16); cube − neighbours' roofs has 20 corners, volume exact.
- compare_dogstar.py: the app's Dogstar mesh (krp-core dogstarSolid, export.mjs) equals cube − roofs (|Δ| 8.5e-8, float32 mesh).
  The app's 51 listed points include points inside its faces; all 20 corners of cube − roofs are among them.
Prior art: shapes known (#42 with Hart's credit; Euclid's roofs). The reading as a keyed switch point is DICTO's/ours.
