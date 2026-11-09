# Harmonic gaps (2026-11-09): #38a and #42 by 3D waves

DICTO proposed solving these by 3D waves (harmonics) on 9 Nov 2026. The two open points:
(A) #38a, The DICTO Kepler–Poinsot–UP Cycle (DICTO DOI 10.5281/zenodo.23464021): "whether its [reciprocal cycle's] shells fill by one pattern";
(B) #42, The DICTO Sunstar (DICTO DOI 10.5281/zenodo.23497702): "what fills the space between the great star and the Sunstar inside it".

**A: NO.** The reciprocal cycle does not fill by one pattern. Its great dodecahedron step is the small stellated shell of #38a itself, filled by the same pattern: GD = D1 + 12 spires + 30 valley tetrahedra, and its 20 dents are the 20 inward pyramids. Its great icosahedron step does not fit a shell at all. The great icosahedron's 12 points stand over the core's corners, not its faces, and it spans a whole turn, from I to I2 = φ³I. It breaks through the dodecahedral hull of its reciprocal shell and cuts the cycle's caps and spires. **Status: settled (exact + harmonic).**

**B: NO SOLID FILLS THE GAP WHOLE.** What fills between the great star and the small Sunstar is the 1/φ³ Sunstar Lattice itself: 118 neighbouring pieces in 9 kinds (dodecahedra and Dogstars), each trimmed by the great star's 12 planes. None is whole, and no whole stellation cell, lattice piece or icosahedral solid fills the gap. The gap is 89.3% of the great star. Its harmonic content is 99.15% icosahedral, which is the great star's own tone. The rest comes from the Sunstar's cube, at degrees 4, 8 and 14, where nothing icosahedral sounds. **Status: settled (exact census + harmonic).**

## A. #38a: the reciprocal cycle

Frame of #38a: I is the icosahedron of edge 1. GSD = I + 20 spikes, with its hull D1. SSD = D1 + 12 spires, with its hull I2 = φ³I.

Exact results (`scripts/a_exact.py`, `data/a_exact.log`, 17 PASS, FINAL ok):
- The SSD's 12 face planes are D1's own faces. The GSD's 12 face planes are the faces of d0 = D1/φ³, the previous turn's hull: each such plane holds a 5-ring of I's corners and a pentagram of D1's corners. **Here the two shells differ, and the reciprocation turns on this difference.**
- Polar reciprocation about the unit sphere maps the convex chain onto itself: [D1*, I*] = k[I, D1] with k = 14 − 6√5, and [I2*, D1*] = k[D1, I2] with k = 26√5 − 58.
- The reciprocal of SSD is k·GD(D1), the great dodecahedron on D1 with corners I2. It lies in the SSD shell. **GD(D1) = D1 + 12 spires + 30 valley tetrahedra exactly, and I2 − GD = the 20 inward pyramids.** Its volume is 235/4 + 105√5/4, which matches the classical formula with edge φ³. The great dodecahedron is therefore a stage of that shell's own fill, as the excavated dodecahedron is in the great shell.
- The reciprocal of GSD is k·GI(I), the great icosahedron on I with corners I2. Its 12 corners, the poles of the GSD planes, are φ³ × D1* and lie **strictly outside I*** (all 12), the hull of its reciprocal shell. GI(I) has volume 95/4 + 43√5/4, which matches the classical formula with short edge φ.
- GI(I) against the cycle's own pieces:
  - I, all 20 CLEO and all 30 AXE lie inside, so the excavated dodecahedron lies whole in GI.
  - Each cap keeps 3 − √5 = 2/φ².
  - Each spire keeps 2√5 − 4 = 2/φ³.
  - No inward pyramid or valley tetrahedron of the small shell enters.
  - These parts sum exactly to GI's volume (a partition check).

  GI is therefore not a union of the cycle's pieces.

Harmonic fingerprint (`scripts/a_harmonic.py`, `data/a_harmonic.log`, FINAL ok). Icosahedral symmetry has exactly one invariant at l = 6, so the l = 6 vector q6 of any symmetric direction set is a multiple of one fixed vector. The cosine c6(A, B) is +1 when A and B lie on the same kind of axis and −1 otherwise. This makes "same pattern" a measurable yes/no. A shell's signature is (tips·core faces, tips·hull corners, valley floors·core corners, valley floors·hull faces), and the Cleo pattern needs (+1, +1, +1, +1).

| shell | signature c6 | radial spectrum p6, p10, p12 (r of the star) |
|---|---|---|
| KP-UP 1: I → GSD → D1 | +1 +1 +1 +1 | .012222 .029125 .003638 |
| KP-UP 2: D1 → SSD → I2 | +1 +1 +1 +1 | .016933 .001235 .000005 |
| next turn (×φ³) | +1 +1 +1 +1 | identical to 1e-10 |
| reciprocal: D1 → GD → I2 | +1 +1 +1 +1 | .008936 .002631 .001903 |
| reciprocal: I → GI → I2 | **−1 +1 −1 +1** | .017069 .009159 .000197 |

**The fingerprint drifts at GI, so the answer is NO.** A caution on the restated test: the bare radial spectrum ("same fingerprint after scaling") also differs between the two KP-UP shells (max |Δp_l| = 0.028), and #38a proves that those two shells do fill by one pattern. The radial spectrum is therefore not the yes/no test; the l = 6 incidence signature is. Scaling leaves both unchanged, as expected.

Geometry behind the answer: the Cleo pattern needs a core and hull that are duals of each other (tips over core faces, inward pyramids from hull faces to core corners). GI has an icosahedron as both core and hull, with the hull corners over the core corners. That incidence is reversed at every point, so the pattern cannot be laid at all.

## B. #42: between the great star and the Sunstar

Frame of #42's scripts: cells of edge 2; divide volumes by 64 for the paper's unit. CORE = DOD/φ³. GSD is the great stellated dodecahedron of CORE (63 stellation cells, with DOD's corners). The small Sunstar is CORE plus the 6 Dogstars of the 1/φ³ lattice.

Exact results (`scripts/b_exact.py`, `data/b_exact.log`, FINAL ok):

**Volumes.**
- GSD: 70 − 30√5 = 2.917961.
- Small Sunstar: 1162√5 − 2598 = 0.310990, which is 10.66% of GSD.
- **Gap: 2668 − 1192√5 = 2.606971.** At the paper's unit these are (35 − 15√5)/32, (581√5 − 1299)/32 and (667 − 298√5)/16.

**The big Dogstar.** The small Sunstar is **not** inside the big Dogstar: each small Dogstar has only 5√5/6 − 3/2 = 0.363390 of its volume there, and the rest reaches into the 6 axis wedges and 12 outer spikes. GSD minus the big Dogstar is exactly 6 axis wedges + 12 spikes, as whole cells.

**The 62 stellation cells around CORE.**

| cells | count | part in the gap |
|---|---|---|
| wedges of the big Dogstar | 24 | whole |
| spikes at the cube corners | 8 | whole |
| pyramids | 12 | 13√5/5 − 5 = 0.8138 |
| axis wedges | 6 | 27√5 − 60 = 0.3738 |
| outer spikes | 12 | 25√5/3 − 53/3 = 0.9672 |

So the gap is not a union of whole stellation cells: 32 are whole and 30 are cut.

**The 1/φ³ lattice.** All 37 T_h orbits of the lattice (565 cells) reaching GSD were checked. Their parts inside GSD sum exactly to GSD, so the census is complete. Only the Sunstar's own 7 pieces are whole. The filler is:

| pieces of the 1/φ³ lattice | part inside GSD |
|---|---|
| 8 Dogstars (1,1,1) | 3√5/2 − 5/2 = 0.854 |
| 12 dodecahedra (1,1,0) | 0.639 |
| 12 Dogstars (2,0,1) | 22/3 − 3√5 = 0.625 |
| 6 dodecahedra (2,0,0) | 0.337 |
| 12 dodecahedra (3,0,1) | 0.066 |
| 24 dodecahedra (2,1,1) | 0.059 |
| 8 dodecahedra (2,2,2) | 0.033 |
| 24 Dogstars (2,2,1) | 0.006 |
| 12 dodecahedra (2,2,0) | 0.0006 |

The exact fractions are in `data/b_exact.json`. (2,1,0) and (1,2,0) are different orbits under T_h; one of them misses GSD entirely.

**Clusters.** Any Sunstar-family cluster on lattice cells (Sunstar-Tetra, -Octa, -Rhombi, -Hexa, -Hexa-Key) is a union of lattice pieces, so none fills the gap either.

Harmonics (`scripts/b_harmonic.py`, `data/b_harmonic.log`, FINAL ok; l ≤ 30; coefficients stable to 7e-16 between two quadratures):
- **The small Sunstar is not star-shaped about its centre.** Its outer radial function encloses 0.021663 more than the solid (7.0%): rays leave it and re-enter. So the gap is not "the region between two radial functions". It is measured by the **angular mass** m(u) = ∫ 1_solid(tu) t² dt, the signed sum of t³/3 over the boundary crossings. This recovers both volumes to 1e-12 and the gap volume from its l = 0 coefficient.
- **Degrees present.**
  - r of GSD has only degrees 0, 6, 10, 12, 16, 18, 20, …, 30. These are all even, since the solid is centrally symmetric. The l = 15, 21, 25, 27 of the chiral group do not appear.
  - The Sunstar has every even l except 2, including l = 4.
- **Symmetry.** By rotating samples, GSD is I_h. Δ = r_GSD − r_Sunstar and the gap mass are exactly T_h (C3, C2, inversion and mirrors, but not C4 or C5). Any filler can therefore have at most T_h, and no icosahedral solid fills the gap alone.
- **Icosahedral and cubic parts.** Projecting with the 120-element I_h average, 99.15% of the gap mass's angular variation (l > 0 power) is icosahedral and 0.85% is pyritohedral. l = 4, 8 and 14 are entirely cubic, and l = 6, 10 and 12 are almost entirely icosahedral (non-icosahedral shares 0.003, 0.0002 and 0.013). The gap carries the great star's tone with the Sunstar's cube as a small overtone, which matches the census: the filler is the cubic lattice clipped by icosahedral planes.

## Checks with numbers (`scripts/sanity.py`, `data/sanity.log`, FINAL ok)
- Icosahedron: Q4 = Q8 = 0, Q6 = 0.6633, Ŵ6 = −0.169754 (Steinhardt–Nelson–Ronchetti). Dodecahedron: Q6 = 0.3685, Ŵ6 = +0.169754, as in the 11-04 fingerprint study.
- Quadrature (planar-triangle Gauss rule on central projections):
  - solid angle 4π to 2e-15;
  - 961 real Y_lm orthonormal to 3e-13;
  - sphere: a00 = √(4π) and every other P_l below 1e-24.
- Cube:
  - volume 8 to 2e-12;
  - only l = 0, 4, 6, 8, …;
  - two quadratures agree to 8e-15;
  - an independent 720,000-ray grid agrees to 8e-6 (the grid is the coarser of the two).
- The fast Legendre recurrence matches scipy's sph_harm_y to 2e-14.
- Exact pipeline:
  - GI and GD volumes from exact cones equal the classical formulas;
  - #38a's piece volumes and #42's 63 cells and 45-cell Dogstar are reproduced;
  - the render's trimmed pieces add up to the exact gap to 1e-6.
- Float survey (`b_explore.py`, 6M points) agrees with the exact fractions to Monte Carlo error.

## Method
- **Exact:** Q(√5) with the Fraction-pair tools q5.py and exactpoly.py (copied from studies/2026-10-18-ocd-octet/scripts), plus g5.py. A star solid is handled as exact cones from the centre over its visible boundary, with every corner snapped to the exact meet of three face planes.
- **Numerical:** radial.py. The visible boundary and the union boundary are found with shapely (precision grid 1e-9, then corners re-snapped to their plane meets). Real spherical harmonics come from a normalised recurrence.
- All runs were on the big machine (each under 20 min; the longest was b_exact.py).

## Figures (`figures/`)
- `fig-b1-maps.png`: Mollweide maps of r(u) of the great star; the small Sunstar's outer r(u) and its equivalent radius (3m)^(1/3), which differ where rays re-enter; and the gap mass m(u).
- `fig-b2-spectrum.png`: power of the gap mass by degree, split into icosahedral and pyritohedral parts.
- `fig-b3-filler.png`: the great star (see-through) with the small Sunstar (gold core, purple Dogstars); the filler cut open; the 118 trimmed lattice pieces drawn apart, coloured by kind.
- `fig-a1-reciprocal.png`: GD(D1) as the SSD shell's stage; GI(I) breaking through D1.

## Prior art (sources checked, 9 Nov 2026)
- **Classical and used as such:**
  - Kepler and Poinsot for the four stars.
  - Polar reciprocity: Coxeter, *Regular Polytopes*.
  - Coincidences of corners and edges: the great icosahedron shares the small stellated dodecahedron's corners, and the great dodecahedron is the small stellated dodecahedron plus 30 wedges (Wikipedia "Great dodecahedron", "Small stellated dodecahedron"; Wenninger list).
  - Bond-orientational Q_l and W_l: Steinhardt, Nelson and Ronchetti (1983).
  - Radial spherical-harmonic shape descriptors hold only for star-shaped bodies: Ballard and Brown (1982), as cited by the spheroidal-harmonics paper arXiv:2407.03350, and Bullard and Garboczi (NIST).
  - Region-based extension, akin to our angular mass: Mak, Grandison and Morris (2008).
- **Names in #42:** the Dogstar solid is Hart's stellation 8 of the dodecahedron (1996; also Ounsted, Grünbaum–Shephard, Stewart, Walser, Polyhedra-World), as #42 credits. "Great star" is Kepler's great stellated dodecahedron. "Sunstar" and the Star Chain Reaction are DICTO's; #42's own checks (library and web, 8–9 and 20 Oct) found no earlier use, and none was found here.
- **Reference library:** full text of all 262 PDFs on the big machine, searched for: great icosahedron (6 hits: Wikipedia Wenninger list, excavated dodecahedron, dodecahedron–icosahedron compound, polytope compound, deltahedron; Cutler–Schulte 2011); great dodecahedron (8 hits: the same Wikipedia pages, Frettlöh 2011, Messer 1995, Baake–Grimm 2012, Cutler–Schulte); great stellated (11 hits, including de Graaf–van Roij–Dijkstra 2011 and Torquato–Jiao 2012 on dense packings of the great stellated dodecahedron); radial function (0); spherical harmonic (3, all materials physics: Limpijumnong–Lambrecht 1997, Lazicki–Yoo–Evans 2006, Kumar–Waghmare 2023); star-shaped (4: Todhunter 1886, Hales 1998 and 2005, Izmestiev–Schlenker 2010, none on harmonics); Sunstar (1: INDEX.pdf, DICTO's own entry); Steinhardt (30, quasicrystal and tiling papers); Wigner (14, including Hermann 2022/2023 on cubic polyhedra). The full hit lists are in `data/library-search.txt`. None treats the fill of the reciprocal Kepler–Poinsot cycle or the space between a great stellated dodecahedron and a pyritohedral cluster.
- **Web searches (9 Nov):** "great dodecahedron stellation cells small stellated dodecahedron plus wedges same vertices edges" (Wikipedia, Dutch, polytope wiki); "spherical harmonic expansion radial function polyhedron star-shaped particle shape descriptor icosahedral" (arXiv:2407.03350, NIST Bullard–Garboczi, Mak et al. 2008, Ulm). Neither turned up these results.
- **Claimed here (new as far as checked):** the reciprocal cycle's split, with GD as a stage of the SSD shell and GI spanning a whole turn and breaking its reciprocal shell, together with GI's exact cut of the cycle's pieces (2/φ² of each cap, 2/φ³ of each spire); the l = 6 incidence signature as a pattern test; the exact gap of the Star Chain Reaction and its filler census; the small Sunstar's failure to be star-shaped; the gap's harmonic split.

## Inconsistencies found
1. #38a's outlook says the reciprocal "is a cycle of the other two Kepler–Poinsot solids, also gaining φ³ a turn". Its hulls do repeat, but its stars do not nest shell by shell. GD sits in the SSD shell, while GI spans a whole turn and passes through the dodecahedral hull I*. Suggested wording for a next version: "Reciprocation keeps the hulls' cycle (it is self-reciprocal up to scale) but not the shells: the great dodecahedron is a stage of the small stellated shell's own fill, while the great icosahedron spans a whole turn."
2. #38a calls I the core of the great shell, while the GSD's face planes belong to d0 = D1/φ³. This is correct as a construction, but it is the source of the asymmetry above and deserves a sentence.
3. The study brief listed l = 15 among the icosahedral degrees. That is right for the rotation group, but the Kepler–Poinsot solids are centrally symmetric, so only even l appear. The Sunstar is pyritohedral, not icosahedral, so l = 4, 8 and 14 appear in the gap.
4. The brief described the gap as the region between two radial functions. That fails because the small Sunstar is not star-shaped (7% excess); the angular mass replaces it.
5. The 10-08 working note recorded "small Dogstars only 38% inside a Dogstar". The exact value is 5√5/6 − 3/2 = 36.34%.

## LEADS
- GI's own fill of its whole turn [I, I2]: GI cuts the caps at 2/φ² and the spires at 2/φ³. Is GI's turn filled by one new pattern of its own (pieces = GI cells ∩ cycle pieces)?
- The trimmed lattice pieces carry the great star's 12 planes. Do the trimmed pieces of the next Star Chain step (inside the core's great star) repeat these 9 kinds at 1/φ³, giving a self-similar filler?
- Angular mass m(u) as the general harmonic tool for non-star-shaped clusters (Sunstar, Jewel clusters, Hexa-Key).
- The l = 6 incidence signature as a quick test for "same pattern" in other shell cycles (UP, Cleo star, golden nests).

## Concordance ledger lines (ready to paste into `ledger.entries`)
```json
{"question": "#38a: do the reciprocal cycle's shells fill by one pattern", "method": "a_exact.py (exact Q(sqrt5): polars, GD/GI as exact cones, piece census) + a_harmonic.py (l = 6 incidence signature, radial spectra l <= 30)", "status": "SETTLED", "result": "NO: GD(D1) = D1 + 12 spires + 30 valley tets (= SSD shell, same pattern); GI(I) spans the whole turn I -> phi^3 I, tips over core corners (signature -1,+1,-1,+1), breaks through I*, keeps 2/phi^2 of each cap and 2/phi^3 of each spire", "retry": "never", "study": "2026-11-09-harmonic-gaps", "date": "2026-11-09"}
{"question": "#42: what fills between the great star and the Sunstar", "method": "b_exact.py (exact census: 63 stellation cells, 37 T_h orbits of the 1/phi^3 lattice) + b_harmonic.py (angular mass m(u), l <= 30)", "status": "SETTLED", "result": "gap 2668 - 1192 sqrt5 (cells of edge 2) = 89.3% of GSD; filled by 118 pieces of the 1/phi^3 Sunstar Lattice in 9 kinds, each trimmed by the great star, none whole; no whole stellation cell or icosahedral solid fills it; small Sunstar not star-shaped (7.0% excess); gap mass 99.15% icosahedral, l = 4, 8, 14 cubic", "retry": "only the self-similar lead (trimmed kinds repeating at 1/phi^3)", "study": "2026-11-09-harmonic-gaps", "date": "2026-11-09"}
```
Gap rows: gaps.loose #38a "do its shells fill by one pattern" → closed (NO, this study); #42 "what fills between the great star and the Sunstar" → closed (trimmed 1/φ³ lattice, no whole filler).
