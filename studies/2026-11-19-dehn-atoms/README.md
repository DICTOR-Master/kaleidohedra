# Dehn atoms: the Dehn invariant of every single-solid atom of The DICTOnary of Atoms (19 November 2026)

**Verdict: of the 202 single-solid atoms in the catalogue (170 numbered in D1–D178, 32 known), 184 have exact corners and were screened (204 solids, since some entries are sets of pieces): 32 have Dehn invariant ZERO, 151 NONZERO, and 1 is a set with mixed pieces (D75, whose core ray is zero and whose 7 towers are nonzero). None was UNDECIDED. D11 is the same solid as D4 (nonzero). 17 were skipped: 14 have only float data, D133 and D134 have no exact form, and there is no vertex data for the Bain disphenoid. The 12 fair dice match the dehn-words study: only the 18-face cube ∩ RD die is zero. Status: high-precision numerical (80 digits). The PSLQ relations are not certified symbolically.**

DICTO · dictospheres.com

**Question (shape language, the dehn-words study carried to the whole DICTOnary):** which atoms can be "said in cubes"? The Dehn invariant answers this. Zero means scissors-congruent to a cube of the same volume (Dehn 1901, Sydler 1965). Nonzero means the atom carries a meaning of its own. Every space-filler has Dehn invariant zero (Debrunner 1980), so a nonzero atom cannot fill space alone. Zero is only a necessary condition for filling space alone.

**Method:** `scripts/dehn_mp.py` is the dehn-words tool (studies/2026-11-19-dehn-words), copied unchanged (sha256 396d9f2e…9217). It computes Dehn(P) = Σ L_e ⊗ θ_e at 80 digits. It looks for integer relations among the distinct dihedral angles and π with PSLQ (Ferguson and Bailey's integer-relation algorithm, as implemented in mpmath; tol 1e-50, coefficients ≤ 2000) and reduces the angles to a basis that is independent mod ℚπ. The sum is called ZERO when every basis coefficient sum is below 1e-45, and NONZERO when one is above 1e-6. Anything between is UNDECIDED. `scripts/run_atoms.py` only loads the corners and faces and checks them before the tool runs:
- **Exact model files.** Exact strings in ℚ, ℚ(√d), ℚ(∛2) or ℚ(t), where t is fixed by its minimal polynomial and isolating interval. Each is evaluated at 100 digits.
- **Exact constructions.** Some classical shapes, and the app's exact definitions, are built at 80 digits.
- **AXE, CLEO and FUJI.** These are identified in ℚ(√5) by the dehn-words rule.

Before the Dehn sum, each solid must pass these checks: a closed oriented surface (every edge in exactly two faces, once each way), every face planar to 1e-60, positive volume, and the file's stated volume matched to 1e-12. All 204 solids passed. `scripts/collect.py` builds the table, and `scripts/manifest.py` builds the list from the two catalogue pages. Names and kinds are copied exactly as printed there.

**Calibration (run first, `data/logs/calibration.log`): FINAL ok, 11/11.** Zero: cube, RD, TO, RT, both golden rhombohedra and the RD centre pyramid. Nonzero: tetrahedron, octahedron, icosahedron and dodecahedron. In the same run, AXE, CLEO and FUJI are nonzero and the 12 fair dice match the dehn-words log line for line: cr (18 faces, cube ∩ RD) is zero, and co (Lucky 7) and the other ten are nonzero.

**Cross-checks against earlier results (all agree):**
- The OG family (D28, D45–D52) is nonzero, as in the 4 Nov float screen, now confirmed at 80 digits.
- The Admiral Cap is nonzero.
- Narcissus and every HexOct tile (D110–D118) are zero. These tiles fill space, so they must be.
- The DICTO 1:2 and 2:1 Truncated Octahedra are nonzero, as in chat-handoff lead 10.
- The regular octahedron at the Delian bond is nonzero.
- D1–D3 and the Fedorov/Bain parallelohedra are zero, as every parallelohedron must be.

The margins are wide. The largest ZERO sum is 1.4e-80, and the smallest NONZERO sum is 0.54 (a Cleo Tower piece).

## The ZERO atoms (32 entries, plus the zero core ray of D75)
- D1 DICTO skewed rhombic dodecahedron: relation found: lengths cancel on each of 2 independent angle classes
- D2 DICTO skewed elongated dodecahedron ED F16: relation found: lengths cancel on each of 2 independent angle classes
- D3 DICTO skewed elongated dodecahedron ED F18: relation found: lengths cancel on each of 2 independent angle classes
- D35 W (one-piece glue): relation found: lengths cancel on its one independent angle class
- D36 Tetartoid core (golden envelope network): all dihedrals rational multiples of π (90°, 108°, 144°)
- D56 DICTO Triaktis (OTT triangle ray): all dihedrals rational multiples of π (36°, 72°, 90°, 120°)
- D57 DICTO Tetraktis (OTT rhombic ray): all dihedrals rational multiples of π (72°, 120°)
- D78 Ian Dury: relation found: lengths cancel on its one independent angle class
- D79 Blockhead: all dihedrals rational multiples of π (90°, 120°, 135°)
- D106 Cube Pearl: all dihedrals rational multiples of π (120°, 135°)
- D110 HexOct c-tile (λ = 1/10): relation found: lengths cancel on its one independent angle class
- D111 HexOct h-tile (λ = 1/10): relation found: lengths cancel on its one independent angle class
- D112 A · HexOct 3/8 h-tile, the twisted cube: all dihedrals rational multiples of π (90°, 120°, 135°)
- D113 B · HexOct −1/8 (whole octahedra) c-tile: relation found: lengths cancel on its one independent angle class
- D114 B · HexOct −1/8 (whole octahedra) h-tile: relation found: lengths cancel on its one independent angle class
- D115 C · HexOct −1/8 c-tile: relation found: lengths cancel on its one independent angle class
- D116 C · HexOct −1/8 h-tile: relation found: lengths cancel on its one independent angle class
- D117 D · HexOct −11/24 c-tile: all dihedrals rational multiples of π (90°, 120°, 240°)
- D138 Diadem L/R: all dihedrals rational multiples of π (36°, 60°, 90°, 108°)
- D140 Chatra: all dihedrals rational multiples of π (60°, 72°, 90°, 108°, 120°)
- D141 Mudra: all dihedrals rational multiples of π (36°, 120°, 144°)
- D173 Narcissus: all dihedrals rational multiples of π (90°, 120°, 135°)
- D174 Covenant: all dihedrals rational multiples of π (90°, 120°, 135°)
- D118 E · HexOct 1/10 c-tile: relation found: lengths cancel on its one independent angle class
- half rhombic dodecahedron* (classical): all dihedrals rational multiples of π (60°, 90°, 120°)
- square bipyramid* (classical): all dihedrals rational multiples of π (90°, 120°)
- DICTO all-rhombus block: relation found: lengths cancel on each of 2 independent angle classes
- DICTO flattened rhombohedron: relation found: lengths cancel on each of 2 independent angle classes
- Bain rhombic dodecahedron: relation found: lengths cancel on its one independent angle class
- Fedorov's elongated dodecahedron with regular hexagons* (Fedorov, 1885): relation found: lengths cancel on its one independent angle class
- A · HexOct 3/8 c-tile, brick of two cubes: all dihedrals rational multiples of π (90°)
- D · HexOct −11/24 h-tile, regular hexagonal prism: all dihedrals rational multiples of π (90°, 120°)
- D75 Polar Cleo Towers, core ray only: all dihedrals rational multiples of π (72°, 120°)

**What to notice:**
- **Not found in the earlier screens:** D35 W (one-piece glue) and D78 Ian Dury are zero by a length relation, not because their angles are rational. D36 Tetartoid core, D140 Chatra, D141 Mudra, D79 Blockhead, D106 Cube Pearl and D174 Covenant have only dihedrals that are rational multiples of π (Diadem's 36/60/90/108° were already stated in 2026-11-17-atoms-missing-2).
- **The OTT's rays split by kind.** The OTT's rays D56 Triaktis and D57 Tetraktis are zero, and so is the core ray of D75. Each is cut from a face pyramid of the rhombic triacontahedron, and the dihedrals of those pyramids are 72° and 120° (and 36° and 90° on the cut faces). The OG's rays, D54 Hex Aktis and D55 Deltoid Aktis, are nonzero.
- **Zero is necessary, not sufficient.** Every zero atom passes the necessary condition for filling space alone. The table does not say it fills.
- **The two golden-regular stages of the icosidodecahedron (Zefiro) are nonzero.** The same is true of all 14 Golden Cuts D119–D132.
- **The square bipyramid here** (known-oct-16, "OCT-16") has dihedrals 90° and 120°. It is not the regular octahedron, which is nonzero (see the Delian-bond octahedron).

## Where the corners come from
- **DICTO Solids dataset** (`math-data:` = the math-data research branch, `studies/2026-10-22-math-data-dicto-solids/solids/`): 89 entries (81 numbered + 8 known), joined to their D-numbers through its `index.csv`. The known atoms Icosaxes, Unborn Axes, Delilah, Goliath, David, Alicia, Unicorn and Bandersnatch are listed under their catalogue names.
- **The missing-atoms batches of 17 Nov** (`studies/2026-11-17-atoms-missing`, `-2`, `models/`, with each piece of a set from `models/pieces/`): 76 entries (67 numbered + 9 known). The numbered ones are D5, D9, D14, D15, D19–D21, D32–D36, D39, D42–D44, D53, D58–D64, D67, D68, D72–D75, D110, D135–D162 and D171–D178. The known ones are Tricap (with Cleo-low), Hound Tooth, Unborn, Inner Eye, cut OG, 13-COA, Hemi RD, OCT-16 and TBP-5.
- **Exact constructions** (`run_atoms.py`, `construct`):
  - **Faces joined to the centre.** D54 and D55 are the OG's hexagons and deltoids (20 + 60, each one congruence class). D56 and D57 are the OTT's triangles of the 24-class (classes 8 + 24) and its rhombi (6). The icosahedron face pyramid, the tetrahedron face pyramid Q (Q′ is Q at size φ²/√2, so it has the same Dehn invariant) and the half octahedron P are built the same way.
  - **D16 Admiral Cap.** Built from the definition in the app source: two tetrahedra over one edge of the unit icosahedron, with apex at the octahedron's corner. Its volume φ/12 is checked.
  - **The two icosidodecahedron stages.** Every edge is cut at x = 1/3 and at x = 1/(φ√5): 120 corners, 62 faces.
  - **The Bain rhombic dodecahedron and Fedorov's regular-hexagon elongated dodecahedron.** Zonohedra of the app's Bain directions (1, ±1, ±√2)/2, with (1, 0, 0) added for the second.
  - **The all-rhombus block and the flattened rhombohedron.** Zonohedra of the app's zome directions v, w, d, X. As a check, v, w, d, X together rebuild D1 with the dataset's distinct dihedrals.
  - **The brick of two cubes and the regular hexagonal prism.** Every height of the prism gives the same 90° and 120°.
- **Identified:** D12 FUJI and the known AXE (t6) and CLEO (t4), from `studies/2026-10-14-axe-cleo-fuji/nets/pieces.json` by the dehn-words rule, as in that study.
- **By identity:** D11 DICTO Hexa Jewel is the DICTO Jewel (D4) itself, as the missing-atoms study notes.

## Skipped (17)
- **Data float only** (no exact model file and no exact construction found):
  - D8 DICTO Dodeca-13 Unit (finned unit) (registry floats)
  - D10 DICTO Hexa-Key (registry floats, about 8 digits)
  - D13 VAJRA, D17 Crown Jewel, D18 Vajra (fine) (kits13 registry, 6 digits)
  - D23 Kion (polar-dharma floats)
  - D24 Atraktos, D25 Aetos, D26 Sphen, D27 Sphenion (icosa-star-hollow meshes, 9 digits)
  - D65 Antonius, D66 Penta-cleo (cleo-sphere registry floats)
  - D102 Fallen Humpty (16-digit decimals only)
  - dodecahedron stellation 8 (Hart, 1996) (registry floats)
- **No exact form:** D133 DICTO Void Keeper and D134 DICTO Golden Skin (#96 leaves the exact form open).
- **No vertex data found:** the Bain disphenoid (finding F3).

## Out of scope (71: not single solids)
- **star polyhedron** (8): D163 Greater Golden Cut Great Dodecahedron; D164 Lesser Golden Cut Great Dodecahedron; D165 Greater Golden Cut Great Icosahedron; D166 Lesser Golden Cut Great Icosahedron; D167 Greater Golden Cut Small Stellated Dodecahedron; D168 Lesser Golden Cut Small Stellated Dodecahedron; D169 Greater Golden Cut Great Stellated Dodecahedron; D170 Lesser Golden Cut Great Stellated Dodecahedron
- **cluster** (22): DICTO Dodeca-13; DICTO Hexa; DICTO Jewel-Tetra; DICTO Jewel-Octa; DICTO Sunstar-Tetra; DICTO Sunstar-Octa; Icosaxes Hexa; Lotus Hexa; DICTO-Star; UNITY (icosidodecahedron + 12 J11); DICTO Stella-Corona; DICTO Spheroid-13 RD; Cleo star; DICTO Jewel-Rhombi; DICTO Sunstar-Rhombi; DICTO Sunstar-Hexa; Icosaxes Bloom; Icosaxes Bud; Icosaxes Seed; Lotus Jewel Bloom; Lotus Jewel Bud; Lotus Jewel Seed
- **structure** (28): DICTO Vacuus Solids (every solid emptied to its fins: SHEETS and STRUTS); Mono-Strut Vacuus (Blockhead, Cube Pearl, DICTO GTI, tetragonal disphenoid* (classical), regular octahedron at the Delian bond, Dodecaxes, Golden Clasp, convex hull of Jessen's orthogonal icosahedron** (Jessen, 1967), truncated octahedron x = φ, TI Star core, truncated octahedron x = 1/φ, White Knight); Mono-Length Vacuus (the cuboctahedron); Disc Vacuus: Kagemusha Pentagon Disc; Disc Vacuus: Lion Disc Vacuus; Isofin Vacuus (5 Platonic, 13 Archimedean, rhombic dodecahedron, rhombic triacontahedron, regular octahedron at the Delian bond); Vacuus of the DICTO 1:2 and 2:1 Truncated Octahedra; Disc Vacuus: twin OG Angelus; Euclid–Kepler–Pacioli (EKP) cell; Euclid–Kepler–Pacioli network; Star Chain Reaction; Jewel chain; Kagome hulls (six hull networks); DICTO Icosa-13; Icosahedral octet; Chain of Karma; Spheres of Dharma; DICTO ATOM-13×13; DICTO Interlock set 1 and set 2 (piece sets); Golden Bodhi Pyrochlore; DICTO Kepler–Poinsot–UP cycle; DICTO Void set 1 (piece set); DICTO Void set 2 (piece set); The kits of #37 (piece sets on the octet truss); The kits of #95 (piece sets for the cut OG); Sunstar Lattice (dodecahedra and stellations 8); Gray's cage of twelve icosahedra* (Gray, 2002); Bodhi seed
- **structure family** (1): Angeli (the Vacuus of a Galois twin; Angelus for one)
- **compound** (1): DICTO Hecatogdoecontahedron
- **curved** (2): Reuleaux octahedron, Reuleaux cube, Reuleaux icosahedron, Reuleaux dodecahedron (balls on the cube, octahedron, dodecahedron, icosahedron corners; names by look); Reuleaux tetrahedron
- **four-dimensional solid** (4): Golden Truncated 5-cell; Golden Cantellated 5-cell; Valley Charge; expanded 5-cell* (Elte, 1912; as an orbit of the 600-cell: Koca, Koç, Al-Barwani and Al-Farsi, 2006)
- **four-dimensional solids (a family)** (1): DICTO All-Golden Polytopes
- **four-dimensional solids (three)** (1): the Red Queen's dual cats A*, B*, C3*
- **four-dimensional regular solid** (2): {3,3,5} 600-cell* (Schläfli, 1852); {5,3,3} 120-cell* (Schläfli, 1852)
- **four-dimensional uniform solid** (1): 4D permutohedron* (Schoute, 1911)

The eight Golden Cut star polyhedra D163–D170 are left out by kind, and their model files hold decimal corners only.

## The table (all 202 in-scope atoms and the 12 fair dice; `data/dehn-atoms.md`, full detail in `data/dehn-atoms.json`)
Faces are the solid's own faces after the tool's checks. For a set, each piece has its own row.

| No. | Name (as in the catalogue) | Faces | Dehn | Reason (zero) / independent angle classes (nonzero) | Corners from |
|---|---|---|---|---|---|
| D1 | DICTO skewed rhombic dodecahedron | 12 | ZERO | relation found: lengths cancel on each of 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-skewed-rhombic-dodecahedron.json |
| D2 | DICTO skewed elongated dodecahedron ED F16 | 12 | ZERO | relation found: lengths cancel on each of 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-skewed-ed-16.json |
| D3 | DICTO skewed elongated dodecahedron ED F18 | 12 | ZERO | relation found: lengths cancel on each of 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-skewed-ed-18.json |
| D4 | DICTO Jewel (EKP windows; first called Dragon Jewel) | 60 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-jewel.json |
| D5 | Stretched dodecahedron | 14 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/dicto-stretched-dodecahedron.json |
| D6 | DICTO Dodeca-13 Wedge | 6 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-dodeca-13-wedge.json |
| D7 | DICTO Dodeca-13 Needle | 4 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-dodeca-13-needle.json |
| D8 | DICTO Dodeca-13 Unit (finned unit) | — | data float only — skipped | | k-mix krp-core dodeca13Data.js (registry floats) |
| D9 | DICTO Dodeca-13 Star | 16 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-dicto-dodeca-13-star.json |
| D10 | DICTO Hexa-Key | — | data float only — skipped | | k-mix krp-core hexaData.js (registry floats, about 8 digits) |
| D11 | DICTO Hexa Jewel | — | same solid as D4 | | the DICTO Jewel itself (#18 defines the Hexa Jewels as exact DICTO Jewels; 2026-11-17-atoms-missing, "Not drawn") |
| D12 | FUJI | 7 | NONZERO | 2 independent angle classes | identified (studies/2026-10-14-axe-cleo-fuji/nets/pieces.json, identified in Q(sqrt5) by the dehn-words rule (each corner to 2e-9)) |
| D13 | VAJRA | — | data float only — skipped | | k-mix krp-core kits13.js KIT13_UNITY_VAJRA (6 digits) |
| D14 | King of Pentacles | 17 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-king-of-pentacles.json |
| D15 | Lotus Jewel (clawed icosahedron) | 36 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-lotus-jewel.json |
| D16 | Admiral Cap (icosahedron edge roof) | 6 | NONZERO | 2 independent angle classes | construction `admiral_cap` — exact definition in the app source (k-mix krp-core edgeRoof.js): two tetrahedra over one edge of the unit icosahedron, apex at the octahedron's corner; checked: volume phi/12, edges 1, sqrt2/2, phi sqrt2/2 |
| D17 | Crown Jewel | — | data float only — skipped | | kits13.js KIT13_BODHI_B4 (6 digits) |
| D18 | Vajra (fine) | — | data float only — skipped | | kits13.js KIT13_BODHI_B1 (6 digits) |
| D19 | Stupa | 6 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-stupa.json |
| D20 | Monkey Staff | 12 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-monkey-staff.json |
| D21 | Shield | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-shield.json |
| D22 | DICTO Truncated-Icosahedral Hecatodihedron | 102 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hecatodihedron.json |
| D23 | Kion | — | data float only — skipped | | studies/2026-10-16-polar-dharma (floats) |
| D24 | Atraktos | — | data float only — skipped | | studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats) |
| D25 | Aetos | — | data float only — skipped | | studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats) |
| D26 | Sphen | — | data float only — skipped | | studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats) |
| D27 | Sphenion | — | data float only — skipped | | studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats) |
| D28 | DICTO Ogdoecontahedron (OG) | 80 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ogdoecontahedron.json |
| D29 | DICTO OCD Stella | 50 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ocd-stella.json |
| D30 | DICTO Metaxyhexecontahedron | 60 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-metaxyhexecontahedron.json |
| D31 | DICTO Palintriacontahedron | 60 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-palintriacontahedron.json |
| D32 | GBPC (Golden Bodhi Pyrochlore Corner) | 4 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/piece-gbpc.json |
| D33 | Bull-horns OG adaptor | 52 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-bull-horns-og-adaptor.json |
| D34 | Keyed octahedron (golden-key octet) | 48 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-keyed-octahedron.json |
| D35 | W (one-piece glue) | 66 | ZERO | relation found: lengths cancel on its one independent angle class | studies/2026-11-17-atoms-missing/models/piece-w.json |
| D36 | Tetartoid core (golden envelope network) | 12 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing/models/piece-tetartoid-core.json |
| D37 | DICTO Belted Triacontahedron (DBT) | 32 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-dbt.json |
| D38 | DICTO OTT (Octahedrally Truncated Triacontahedron) | 38 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ott.json |
| D39 | Mirror middle piece Mg | 22 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-mirror-middle-piece-mg.json |
| D40 | DICTO GTI (golden truncated icosahedron) | 32 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-gti.json |
| D41 | DICTO FPD (flat pentakis dodecahedron) | 60 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-fpd.json |
| D42 | Five-sided Vajra | 15 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-five-sided-vajra.json |
| D43 | Hexagonal Cleo | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-hexagonal-cleo.json |
| D44 | Monkey Staff B | 12 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/piece-monkey-staff-b.json |
| D45 | DICTO KRE | 90 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-kre.json |
| D46 | DICTO PHE | 92 | NONZERO | 3 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-phe.json |
| D47 | DICTO TPP | 180 | NONZERO | 5 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tpp.json |
| D48 | DICTO DPHP | 152 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-dphp.json |
| D49 | DICTO TPH | 132 | NONZERO | 3 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tph.json |
| D50 | DICTO TQH | 140 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tqh.json |
| D51 | DICTO TQP | 162 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tqp.json |
| D52 | DICTO TQHD | 200 | NONZERO | 5 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tqhd.json |
| D53 | DICTO Sunstar-Hexa-Key | 72 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/dicto-sunstar-hexa-key.json |
| D54 | DICTO Hex Aktis | 7 | NONZERO | 2 independent angle classes | construction `hex_aktis` — OG (dataset dicto-ogdoecontahedron) hexagon joined to the centre (build-cleo-towers.py: 20 Hex Aktis + 60 Deltoid Aktis, every apex at the centre) |
| D55 | DICTO Deltoid Aktis | 5 | NONZERO | 3 independent angle classes | construction `deltoid_aktis` — OG (dataset dicto-ogdoecontahedron) deltoid joined to the centre (as D54) |
| D56 | DICTO Triaktis (OTT triangle ray) | 4 | ZERO | all dihedrals rational multiples of π | construction `triaktis` — OTT (dataset dicto-ott) triangle of the 24-class joined to the centre (studies/2026-10-20-ott-rays: 8 Oktaktis + 24 Triaktis + 6 Tetraktis) |
| D57 | DICTO Tetraktis (OTT rhombic ray) | 5 | ZERO | all dihedrals rational multiples of π | construction `tetraktis` — OTT (dataset dicto-ott) rhombus joined to the centre (as D56) |
| D58 | DICTO TQP-252 | 252 | NONZERO | 7 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tqp-252.json |
| D59 | DICTO TQ-320 | 320 | NONZERO | 7 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tq-320.json |
| D60 | DICTO TQP-402 | 402 | NONZERO | 8 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tqp-402.json |
| D61 | DICTO TQ-500 | 500 | NONZERO | 10 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tq-500.json |
| D62 | DICTO TQD-732 | 732 | NONZERO | 14 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tqd-732.json |
| D63 | DICTO TQHD-662 | 662 | NONZERO | 13 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tqhd-662.json |
| D64 | DICTO TQP-672 | 672 | NONZERO | 14 independent angle classes | studies/2026-11-17-atoms-missing/models/dicto-tqp-672.json |
| D65 | Antonius | — | data float only — skipped | | k-mix krp-core cleo-sphere.js ANTONIUS (floats) |
| D66 | Penta-cleo | — | data float only — skipped | | k-mix krp-core cleo-sphere.js PENTA_CLEO (floats) |
| D67 | X (cube of edge φ minus one Euclid roof) (#47) | 9 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/piece-x.json |
| D68 | Y (cube of edge φ plus one Euclid roof) (#47) | 9 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/piece-y.json |
| D69 | Lotus Jewel Axes | 54 | NONZERO | 3 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lotus-jewel-axes.json |
| D70 | Dodecaxes | 54 | NONZERO | 3 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-dodecaxes.json |
| D71 | Samson | 10 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-samson.json |
| D72 | Dented tetrahedron L/R (golden-key octet) | | NONZERO | 2 pieces, each below | |
| | · Dented tetrahedron L (golden-key octet) | 24 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-dented-tetrahedron-left.json |
| | · Dented tetrahedron R (golden-key octet) | 24 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-dented-tetrahedron-right.json |
| D73 | DICTO Fill set 1 / 2 pieces (grown bipyramid, grown tetrahedra L/R) | | NONZERO | 4 pieces, each below | |
| | · DICTO Fill set 1 (DBT) F1, grown bipyramid | 78 | NONZERO | 6 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-dicto-fill-set-1-f1.json |
| | · DICTO Fill set 2 (OTT) F1, grown bipyramid | 90 | NONZERO | 7 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-dicto-fill-set-2-f1.json |
| | · DICTO Fill set 2 (OTT) F2, grown tetrahedron L | 34 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/pieces/piece-dicto-fill-set-2-f2-left.json |
| | · DICTO Fill set 2 (OTT) F3, grown tetrahedron R | 34 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/pieces/piece-dicto-fill-set-2-f3-right.json |
| D74 | Cleo Towers (8 tower pieces) | | NONZERO | 8 pieces, each below | |
| | · Cleo Towers (8 tower pieces): shell 1 on 3 gon | 7 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-1-on-3-gon.json |
| | · Cleo Towers (8 tower pieces): shell 1 on 5 gon | 11 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-1-on-5-gon.json |
| | · Cleo Towers (8 tower pieces): shell 2 on 4 gon | 9 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-2-on-4-gon.json |
| | · Cleo Towers (8 tower pieces): shell 3 on 5 gon | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-3-on-5-gon.json |
| | · Cleo Towers (8 tower pieces): shell 3 on 6 gon | 11 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-3-on-6-gon.json |
| | · Cleo Towers (8 tower pieces): shell 4 on 3 gon | 10 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-4-on-3-gon.json |
| | · Cleo Towers (8 tower pieces): shell 4 on 5 gon | 11 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-4-on-5-gon.json |
| | · Cleo Towers (8 tower pieces): shell 5 on 3 gon | 7 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-cleo-towers-shell-5-on-3-gon.json |
| D75 | Polar Cleo Towers (7 tower pieces + core ray) | | mixed | 8 pieces, each below | |
| | · Polar Cleo Towers (7 tower pieces + core ray): core ray | 5 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-core-ray.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 1 on 4 gon | 9 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-1-on-4-gon.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 2 on 5 gon | 11 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-2-on-5-gon.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 2 on 6 gon | 10 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-2-on-6-gon.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 3 on 4 gon | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-3-on-4-gon.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 4 on 3 gon | 7 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-4-on-3-gon.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 5 on 3 gon | 7 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-5-on-3-gon.json |
| | · Polar Cleo Towers (7 tower pieces + core ray): shell 5 on 5 gon | 11 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing/models/pieces/piece-polar-cleo-towers-shell-5-on-5-gon.json |
| D76 | Sonsam | 13 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-sonsam.json |
| D77 | Lahdeli | 8 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lahdeli.json |
| D78 | Ian Dury | 13 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ian-dury.json |
| D79 | Blockhead | 10 | ZERO | all dihedrals rational multiples of π | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-blockhead.json |
| D80 | Chucky | 13 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-chucky.json |
| D81 | Fang | 7 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-fang.json |
| D82 | Triskelion Tetrahedron | 10 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-triskelion-tetrahedron.json |
| D83 | Keyaxes | 54 | NONZERO | 3 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-keyaxes.json |
| D84 | Ganesha | 17 | NONZERO | 5 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ganesha.json |
| D85 | cell-first section of the 600-cell at height (2 + √5)/2* (Boole Stott, 1900) | 92 | NONZERO | 7 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-humpty-dumpty.json |
| D86 | Kagemusha | 30 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-shadow-17.json |
| D87 | Lion | 80 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lion.json |
| D88 | Jabberwock | 140 | NONZERO | 3 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-jabberwock.json |
| D89 | Tweedledum | 60 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tweedledum.json |
| D90 | Tweedledee | 60 | NONZERO | 6 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-tweedledee.json |
| D91 | Mad Hatter | 218 | NONZERO | 14 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-mad-hatter.json |
| D92 | March Hare | 218 | NONZERO | 14 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-march-hare.json |
| D93 | Jubjub | 56 | NONZERO | 9 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-jubjub.json |
| D94 | Alice | 218 | NONZERO | 11 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-alice.json |
| D95 | White Rabbit | 218 | NONZERO | 13 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-white-rabbit.json |
| D96 | Haigha | 59 | NONZERO | 9 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-haigha.json |
| D97 | Hatta | 59 | NONZERO | 10 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hatta.json |
| D98 | Red King | 52 | NONZERO | 5 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-red-king.json |
| D99 | Walrus | 62 | NONZERO | 8 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-walrus.json |
| D100 | Red Knight | 62 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-red-knight.json |
| D101 | White Knight | 62 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-white-knight.json |
| D102 | Fallen Humpty | — | data float only — skipped | | studies/2026-10-29-quanta-atoms/dicto-fallen-humpty.json (16-digit decimals only) |
| D103 | Golden TI Star | 180 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-golden-ti-star.json |
| D104 | Star Halo | 60 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-star-halo.json |
| D105 | TI Star core | 32 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ti-star-core.json |
| D106 | Cube Pearl | 18 | ZERO | all dihedrals rational multiples of π | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-cube-pearl.json |
| D107 | Golden Clasp | 26 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-golden-clasp.json |
| D108 | Hamlet | 270 | NONZERO | 8 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hamlet.json |
| D109 | Ophelia | 440 | NONZERO | 12 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-ophelia.json |
| D110 | HexOct c-tile (λ = 1/10) | 32 | ZERO | relation found: lengths cancel on its one independent angle class | studies/2026-11-17-atoms-missing/models/piece-hexoct-c-tile.json |
| D111 | HexOct h-tile (λ = 1/10) | 30 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-h-tile.json |
| D112 | A · HexOct 3/8 h-tile, the twisted cube | 12 | ZERO | all dihedrals rational multiples of π | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-twisted-cube.json |
| D113 | B · HexOct −1/8 (whole octahedra) c-tile | 8 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-b-c-tile.json |
| D114 | B · HexOct −1/8 (whole octahedra) h-tile | 10 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-b-h-tile.json |
| D115 | C · HexOct −1/8 c-tile | 10 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-c-c-tile.json |
| D116 | C · HexOct −1/8 h-tile | 14 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-c-h-tile.json |
| D117 | D · HexOct −11/24 c-tile | 18 | ZERO | all dihedrals rational multiples of π | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-d-c-tile.json |
| D119 | Greater Golden Cut Dodecahedron | 32 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-dodecahedron.json |
| D120 | Lesser Golden Cut Dodecahedron | 32 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-dodecahedron.json |
| D121 | Greater Golden Cut Icosahedron | 32 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-icosahedron.json |
| D122 | Lesser Golden Cut Icosahedron | 32 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-icosahedron.json |
| D123 | Greater Golden Cut Cube | 14 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-cube.json |
| D124 | Lesser Golden Cut Cube | 14 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-cube.json |
| D125 | Greater Golden Cut Tetrahedron | 8 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-tetrahedron.json |
| D126 | Lesser Golden Cut Tetrahedron | 8 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-tetrahedron.json |
| D127 | Greater Golden Cut Rhombic Dodecahedron | 26 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-rhombic-dodecahedron.json |
| D128 | Lesser Golden Cut Rhombic Dodecahedron | 26 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-rhombic-dodecahedron.json |
| D129 | Greater Golden Cut Rhombic Triacontahedron | 62 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-rhombic-triacontahedron.json |
| D130 | Lesser Golden Cut Rhombic Triacontahedron | 62 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-rhombic-triacontahedron.json |
| D131 | Greater Golden Cut Snub Dodecahedron L/R | 152 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-greater-golden-cut-snub-dodecahedron.json |
| D132 | Lesser Golden Cut Snub Dodecahedron L/R | 152 | NONZERO | 4 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-lesser-golden-cut-snub-dodecahedron.json |
| D133 | DICTO Void Keeper | — | skipped (no exact form) | | #96 leaves the exact form open (Section 6); no model file |
| D134 | DICTO Golden Skin | — | skipped (no exact form) | | #96 leaves the exact form open (Section 6); a family, one per brick size; no model file |
| D135 | Weirdstone L/R | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-weirdstone.json |
| D136 | Tadpole L/R | 6 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-tadpole.json |
| D137 | Frog Chorus (the gap star) | 164 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-frog-chorus.json |
| D138 | Diadem L/R | | ZERO | 2 pieces, each below | |
| | · Diadem (L) | 5 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/piece-diadem.json |
| | · Diadem (R) | 5 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/pieces/piece-diadem-r.json |
| D139 | Hasu | 15 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing-2/models/piece-hasu.json |
| D140 | Chatra | 6 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/piece-chatra.json |
| D141 | Mudra | 5 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/piece-mudra.json |
| D142 | Vajra (twist) | 8 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-vajra-twist.json |
| D143 | Cleo-low 2 | 4 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-cleo-low-2.json |
| D144 | Vajra-blade | 4 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-vajra-blade.json |
| D145 | Sevenfold-blade | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-sevenfold-blade.json |
| D146 | Triskelion Hex | 13 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-triskelion-hex.json |
| D147 | Triskelion | 10 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-triskelion.json |
| D148 | Julia G3 | 12 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g3.json |
| D149 | Julia G4 | 11 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g4.json |
| D150 | Julia G5a | 7 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g5a.json |
| D151 | Julia G5b | 8 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g5b.json |
| D152 | Julia G6 | 4 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g6.json |
| D153 | Julia G8 | 6 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g8.json |
| D154 | Julia G9 | 5 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g9.json |
| D155 | Julia G10 | 7 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-julia-g10.json |
| D156 | Pimentel G11 | 6 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-pimentel-g11.json |
| D157 | Sonsam-K | 40 | NONZERO | 7 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-sonsam-k.json |
| D158 | Lahdeli-K | 62 | NONZERO | 7 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-lahdeli-k.json |
| D159 | Ian Dury-K | 34 | NONZERO | 6 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-ian-dury-k.json |
| D160 | Rhombo-K | 48 | NONZERO | 6 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-rhombo-k.json |
| D161 | Maedate | 8 | NONZERO | 5 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-maedate.json |
| D162 | Kuwagata | 6 | NONZERO | 4 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-kuwagata.json |
| D171 | Lesser Golden OG | 80 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/dicto-lesser-golden-og.json |
| D172 | Greater Golden OG | 80 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/dicto-greater-golden-og.json |
| D173 | Narcissus | 10 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/piece-narcissus.json |
| D174 | Covenant | 12 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/dicto-covenant.json |
| D175 | Sheriff | 6 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-sheriff.json |
| D176 | Lone-star | 4 | NONZERO | 3 independent angle classes | studies/2026-11-17-atoms-missing-2/models/piece-lone-star.json |
| D177 | DICTO 1:2 Truncated Octahedron | 14 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing-2/models/dicto-1-2-truncated-octahedron.json |
| D178 | DICTO 2:1 Truncated Octahedron | 14 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing-2/models/dicto-2-1-truncated-octahedron.json |
| D118 | E · HexOct 1/10 c-tile | 24 | ZERO | relation found: lengths cancel on its one independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-hexoct-e-c-tile.json |
| Hart 1996, tetrahedral stellations of the dodecahedron, no. 8 | dodecahedron stellation 8* (Hart, 1996) | — | data float only — skipped | | k-mix krp-core sunstar.js DOGSTAR (registry floats) |
| Mosseri–Sadoc t6 (scaled by 1/φ) | Mosseri–Sadoc tile t6* (Mosseri and Sadoc, 1982) | 4 | NONZERO | 2 independent angle classes | identified (studies/2026-10-14-axe-cleo-fuji/nets/pieces.json, the dehn-words rule) |
| Mosseri–Sadoc t4 (scaled by 1/φ) | Mosseri–Sadoc tile t4* (Mosseri and Sadoc, 1982) | 4 | NONZERO | 2 independent angle classes | identified (studies/2026-10-14-axe-cleo-fuji/nets/pieces.json, the dehn-words rule) |
| — | icosahedron face pyramid* (classical; Mackay, 1962) | 4 | NONZERO | 1 independent angle class | construction `cleo_icos` |
| — | truncated octahedron x = φ* (Koca et al., 2015) | 14 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-icosaxes.json |
| — | truncated octahedron x = 1/φ* (Koca et al., 2015) | 14 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-unborn-axes.json |
| U5; W2 | regular octahedron at the Delian bond* (classical) | 8 | NONZERO | 1 independent angle class | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-delilah.json |
| — | convex hull of Jessen's orthogonal icosahedron* (Jessen, 1967) | 20 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-goliath.json |
| — | tetragonal disphenoid* (classical) | 4 | NONZERO | 2 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-david.json |
| — | cell-first section of the 600-cell at height 0* (Boole Stott, 1900) | 158 | NONZERO | 6 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-alicia.json |
| — | cell-first section of the 600-cell at height (3 + √5)/2* (Boole Stott, 1900) | 80 | NONZERO | 7 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-unicorn.json |
| — | cell-first section of the 600-cell at height (5 + 3√5)/4* (Boole Stott, 1900) | 52 | NONZERO | 5 independent angle classes | math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-bandersnatch.json |
| — | regular-hexagon stage of the icosidodecahedron* (Zefiro, 2011) | 62 | NONZERO | 2 independent angle classes | construction `id_stage_third` |
| — | regular-decagon stage of the icosidodecahedron* (Zefiro, 2011) | 62 | NONZERO | 2 independent angle classes | construction `id_stage_golden` |
| Mosseri–Sadoc t3 (half size) | Mosseri–Sadoc tile t3* (Mosseri and Sadoc, 1982) | | NONZERO | 2 pieces, each below | |
| | · Tricap (Mosseri-Sadoc t3) | 4 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/known-tricap.json |
| | · Cleo-low | 4 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/known-cleo-low.json |
| Mosseri–Sadoc t2 | Mosseri–Sadoc tile t2* (Mosseri and Sadoc, 1982) | 4 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/known-hound-tooth.json |
| — | pseudoicosahedron* (Koca et al., 2015) | 20 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/known-unborn.json |
| Wenninger 28 | excavated dodecahedron* (Coxeter, Du Val, Flather and Petrie, 1938) | 60 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing-2/models/known-inner-eye.json |
| — | rectified truncated icosahedron* (classical; near-miss Johnson solid, McCooey) | 92 | NONZERO | 2 independent angle classes | studies/2026-11-17-atoms-missing-2/models/known-cut-og.json |
| — | augmented cuboctahedron* (Stewart, 1970) | 13 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing-2/models/known-dicto-13-coa.json |
| — | half rhombic dodecahedron* (classical) | 8 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/known-hemi-rd.json |
| — | square bipyramid* (classical) | 8 | ZERO | all dihedrals rational multiples of π | studies/2026-11-17-atoms-missing-2/models/known-oct-16.json |
| — | triangular bipyramid* (classical) | 6 | NONZERO | 1 independent angle class | studies/2026-11-17-atoms-missing-2/models/known-tbp-5.json |
| — | DICTO all-rhombus block | 6 | ZERO | relation found: lengths cancel on each of 2 independent angle classes | construction `all_rhombus_block` |
| — | DICTO flattened rhombohedron | 6 | ZERO | relation found: lengths cancel on each of 2 independent angle classes | construction `flattened_rhombohedron` |
| — | Bain disphenoid | — | skipped (no data) | | no vertex data found (finding F3; not in the dataset or the app registry) |
| — | Bain rhombic dodecahedron | 12 | ZERO | relation found: lengths cancel on its one independent angle class | construction `bain_rd` |
| — | Fedorov's elongated dodecahedron with regular hexagons* (Fedorov, 1885) | 12 | ZERO | relation found: lengths cancel on its one independent angle class | construction `regular_hex_ed` |
| J1 | Half octahedron P (#47 connector) | 5 | NONZERO | 1 independent angle class | construction `half_octahedron` |
| — | Tetrahedron face pyramid Q and Q' (#44, #47 connectors) | 4 | NONZERO | 1 independent angle class | construction `tetra_face_pyramid` |
| — | A · HexOct 3/8 c-tile, brick of two cubes | 6 | ZERO | all dihedrals rational multiples of π | construction `brick` |
| — | D · HexOct −11/24 h-tile, regular hexagonal prism | 8 | ZERO | all dihedrals rational multiples of π | construction `hex_prism` |
| fair die | tc (10 faces, #111) | 10 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-tc.json |
| fair die | co (14 faces, #111) | 14 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-co.json |
| fair die | tr (16 faces, #111) | 16 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-tr.json |
| fair die | td (16 faces, #111) | 16 | NONZERO | 2 independent angle classes | studies/2026-11-18-fair-32-die/data/verts-td.json |
| fair die | cr (18 faces, #111) | 18 | ZERO | all dihedrals rational multiples of π | studies/2026-11-18-fair-32-die/data/verts-cr.json |
| fair die | cd (18 faces, #111) | 18 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-cd.json |
| fair die | or (20 faces, #111) | 20 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-or.json |
| fair die | od (20 faces, #111) | 20 | NONZERO | 2 independent angle classes | studies/2026-11-18-fair-32-die/data/verts-od.json |
| fair die | rdd (24 faces, #111) | 24 | NONZERO | 2 independent angle classes | studies/2026-11-18-fair-32-die/data/verts-rdd.json |
| fair die | di (32 faces, #111) | 32 | NONZERO | 2 independent angle classes | studies/2026-11-18-fair-32-die/data/verts-di.json |
| fair die | dt (42 faces, #111) | 42 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-dt.json |
| fair die | it (50 faces, #111) | 50 | NONZERO | 1 independent angle class | studies/2026-11-18-fair-32-die/data/verts-it.json |

## LEADS
1. **Exact models for the 14 float-only atoms.** D8, D10, D13, D17, D18, D23–D27, D65, D66, D102 and the dodecahedron stellation 8 need exact models, built the way the two missing-atoms batches built theirs (snap to the exact frame, then check every stated value exactly). Then rerun `run_atoms.py` on them. The Hexa-Key already has an exact recognition in studies/2026-11-13-platonic-fans-law, with exact volume 6φ³, and an exact construction route in studies/2026-10-20-dicto-jewel/jewel_exact.py.
2. **Fill tests for the zero atoms with no recorded tiling.** Zero is only necessary. Candidates: W (one-piece glue), Tetartoid core, Triaktis, Tetraktis, the polar core ray, Ian Dury, Blockhead, Cube Pearl, Chatra, Mudra, Diadem, Covenant. Read each one's paper first: several may already be proved fillers.
3. **The two length-relation zeros, W and Ian Dury.** Write each Dehn sum in closed form, with the exact angle relation and the exact length balance, as was done for the HexOct pieces on 4 Nov.
4. **Certification.** Turn the PSLQ relations used for the ZERO verdicts into exact identities among the arccos values (several are rational angles already). The Lean canon studies give the route.

## Files
- `scripts/dehn_mp.py`: the dehn-words tool, unchanged.
- `scripts/manifest.py`: the in-scope list and the source of each atom's corners.
- `scripts/run_atoms.py`: loading, constructions, checks and screening.
- `scripts/collect.py`: the tables.
- `data/manifest.json`, `data/dehn-atoms.json`, `data/dehn-atoms.md`.
- `data/out/atom-NNN.json`: one raw result per atom (checks, distinct dihedrals, independent classes, the largest coefficient sum).
- `data/logs/`: `calibration.log` (the tool's own run: calibration, words, dice), `all.log` (one line per solid), `pilot.log`, `collect.log`.

Credit: DICTO (the question: the shape language and its Dehn words); the computation is with Claude (Anthropic). Method: the dehn-words tool; PSLQ by Ferguson and Bailey; Dehn (1901), Sydler (1965), Debrunner (1980).
